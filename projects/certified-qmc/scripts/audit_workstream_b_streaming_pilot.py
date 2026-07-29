#!/usr/bin/env python3
"""Run the preregistered incremental prime-major streaming pilot."""

from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
import json
from math import ceil
import os
from pathlib import Path
import platform
import statistics
import struct
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.exact_error import RuleSpec
from src.modular_error import error_numerator_residue
from src.ntt_prime import generate_ntt_prime_schedule
from src.scaled_integer import balanced_crt_bits, error_numerator_bound


PREREG = (
    ROOT
    / "data"
    / "workstream-b-streaming-pilot-preregistration-v2.json"
)
BUDGET = ROOT / "certificates" / "workstream-b-production-budget.json"
SOURCE_SHA256 = (
    "d42503eda84c7fede8d2513d674a9eca4075041dc4cf8c2e0995b46b035b5ce9"
)
OUTPUT = ROOT / "certificates" / "workstream-b-streaming-pilot.json"
BINARY = ROOT / "build" / "native" / "streaming_pilot"
SOURCE = ROOT / "native" / "streaming_pilot.c"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical_digest(value) -> str:
    return sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")
    ).hexdigest()


def parse_generator(path: Path, dimension: int) -> list[int]:
    rows = []
    for line in path.read_text().splitlines():
        fields = line.split()
        if len(fields) != 2:
            raise ValueError("source vector row does not have two columns")
        row, component = map(int, fields)
        if row != len(rows) + 1:
            raise ValueError("source vector dimension column is not sequential")
        rows.append(component)
    if len(rows) != 3600:
        raise ValueError("source vector does not have 3600 rows")
    return rows[:dimension]


def invoke(
    vector: Path,
    primes: Path,
    dimension: int,
    threads: int,
    checkpoint: Path,
) -> dict:
    completed = subprocess.run(
        [
            str(BINARY),
            str(vector),
            str(primes),
            str(dimension),
            str(threads),
            str(checkpoint),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def read_checkpoint(
    path: Path, prime_count: int, dimension: int
) -> list[list[int]]:
    raw = path.read_bytes()
    expected = prime_count * dimension * 8
    if len(raw) != expected:
        raise ValueError("checkpoint byte count mismatch")
    words = struct.unpack(f"={prime_count * dimension}Q", raw)
    return [
        list(words[index * dimension:(index + 1) * dimension])
        for index in range(prime_count)
    ]


def median_fraction(values: list[Fraction]) -> Fraction:
    return sorted(values)[len(values) // 2]


def fidelity_updates_through(
    dimension: int,
    modulus_exponents: list[int],
    families: int,
) -> int:
    """Conservative incremental fidelity work through one global cutoff."""

    weights = [
        Fraction(1, index * index)
        for index in range(1, dimension + 1)
    ]
    return families * sum(
        (2**exponent)
        * dimension
        * ceil(
            balanced_crt_bits(
                error_numerator_bound(2**exponent, weights)
            )
            / 61
        )
        for exponent in modulus_exponents
    )


def mechanical_tier_boundary(
    ns_per_update: Fraction,
    budget: dict,
    prereg: dict,
) -> dict:
    """Apply the prospectively frozen largest-affordable-cutoff rule."""

    maximum_seconds = (
        Fraction(
            prereg["production_decision"]["reference_budget_node_days"]
        )
        * int(prereg["production_decision"]["node_day_seconds"])
    )
    usability_updates = int(
        budget["totals"]["usability_direct_update_lower_bound"]
    )
    modulus_exponents = [
        int(cell["modulus_exponent"])
        for cell in budget["fidelity_max_dimension_cells"]
    ]
    families = int(budget["totals"]["source_families"])

    def projected(dimension: int) -> tuple[int, Fraction]:
        updates = (
            fidelity_updates_through(
                dimension, modulus_exponents, families
            )
            + usability_updates
        )
        seconds = ns_per_update * updates / 1_000_000_000
        return updates, seconds

    low = 16
    high = 3600
    if projected(low)[1] > maximum_seconds:
        return {
            "applied": True,
            "global_dimension_cutoff": None,
            "reason": (
                "even the preregistered minimum cutoff d=16 exceeds "
                "the node-day budget"
            ),
            "usability_updates_retained": usability_updates,
        }
    while low < high:
        midpoint = (low + high + 1) // 2
        if projected(midpoint)[1] <= maximum_seconds:
            low = midpoint
        else:
            high = midpoint - 1
    updates, seconds = projected(low)
    next_projection = None
    if low < 3600:
        next_updates, next_seconds = projected(low + 1)
        next_projection = {
            "dimension": low + 1,
            "updates": next_updates,
            "projected_node_days": float(next_seconds / 86400),
        }
    return {
        "applied": True,
        "global_dimension_cutoff": low,
        "exact_tier": {
            "tag": prereg["no_go_fallback"]["exact_tier_tag"],
            "maximum_dimension": low,
            "updates": updates,
            "projected_node_days": float(seconds / 86400),
        },
        "enclosure_tier": {
            "tag": prereg["no_go_fallback"]["enclosure_tier_tag"],
            "minimum_dimension": low + 1,
            "arb_start_precision_bits": prereg["no_go_fallback"][
                "arb_start_precision_bits"
            ],
            "arb_radius_predicate": prereg["no_go_fallback"][
                "arb_radius_predicate"
            ],
        },
        "first_excluded_projection": next_projection,
        "usability_updates_retained": usability_updates,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    prereg = json.loads(PREREG.read_text())
    if prereg["measurement_started"]:
        raise RuntimeError("preregistration does not precede measurement")
    if digest(args.source) != SOURCE_SHA256:
        raise RuntimeError("source vector SHA-256 mismatch")
    dimension = int(prereg["pilot"]["dimension"])
    modulus = int(prereg["pilot"]["N"])
    generator = parse_generator(args.source, dimension)

    schedule = generate_ntt_prime_schedule(
        prereg["pilot"]["work_primes"]
        + prereg["pilot"]["universal_overflow_check_primes"]
    )
    primes = [int(row["prime"]) for row in schedule]
    threads = os.cpu_count() or 1
    subprocess.run(
        ["make", "-C", str(ROOT / "native"), "all"],
        check=True,
        capture_output=True,
        text=True,
    )

    with tempfile.TemporaryDirectory(prefix="certified-qmc-pilot-") as tmp:
        tmp_path = Path(tmp)
        primes_path = tmp_path / "primes.txt"
        primes_path.write_text(
            "".join(f"{prime}\n" for prime in primes)
        )
        checkpoint = tmp_path / "residues.bin"

        for _ in range(prereg["pilot"]["warmup_runs"]):
            invoke(args.source, primes_path, dimension, threads, checkpoint)

        runs = []
        for _ in range(prereg["pilot"]["measured_runs"]):
            result = invoke(
                args.source,
                primes_path,
                dimension,
                threads,
                checkpoint,
            )
            result["checkpoint_sha256"] = digest(checkpoint)
            runs.append(result)

        residues = read_checkpoint(checkpoint, len(primes), dimension)
        final_checkpoint_sha256 = digest(checkpoint)

    work_updates = runs[0]["work_updates"]
    ns_per_update = [
        Fraction(run["work_ns"], work_updates)
        for run in runs
    ]
    replay_fractions = [
        Fraction(
            run["overflow_ns"] + run["checkpoint_ns"],
            run["work_ns"],
        )
        for run in runs
    ]
    median_ns_per_update = median_fraction(ns_per_update)
    median_replay_fraction = median_fraction(replay_fractions)

    selected_dimensions = (1, 16, 64, 128, 256)
    selected_prime_indices = (
        0,
        prereg["pilot"]["work_primes"] // 2,
        prereg["pilot"]["work_primes"] - 1,
        prereg["pilot"]["work_primes"],
        prereg["pilot"]["work_primes"] + 1,
    )
    residue_checks = []
    all_residues_match = True
    for prime_index in selected_prime_indices:
        prime = primes[prime_index]
        for selected_dimension in selected_dimensions:
            spec = RuleSpec.create(
                modulus,
                generator[:selected_dimension],
                [
                    Fraction(1, index * index)
                    for index in range(1, selected_dimension + 1)
                ],
            )
            oracle = error_numerator_residue(spec, prime)
            native = residues[prime_index][selected_dimension - 1]
            equal = native == oracle
            all_residues_match &= equal
            residue_checks.append(
                {
                    "prime_index": prime_index,
                    "prime": str(prime),
                    "dimension": selected_dimension,
                    "native_residue": str(native),
                    "python_oracle_residue": str(oracle),
                    "equal": equal,
                }
            )

    full_updates = int(
        prereg["incremental_accounting"]["full_grid_work_updates"]
    )
    projected_seconds = (
        median_ns_per_update * full_updates / 1_000_000_000
    )
    projected_node_days = projected_seconds / 86400
    maximum_node_days = Fraction(
        prereg["production_decision"]["reference_budget_node_days"]
    )
    maximum_replay = Fraction(
        prereg["production_decision"][
            "maximum_replay_overhead_fraction"
        ]
    )
    correctness = (
        all_residues_match
        and all(run["checkpoint_replay"] for run in runs)
        and all(run["overflow_primes"] == 2 for run in runs)
        and all(
            run["output_words"] == len(primes) * dimension
            for run in runs
        )
    )
    throughput_pass = projected_node_days <= maximum_node_days
    replay_pass = median_replay_fraction <= maximum_replay
    authorized = correctness and throughput_pass and replay_pass
    if not correctness or not replay_pass:
        disposition = "REDESIGN_REQUIRED"
    elif throughput_pass:
        disposition = "FULL_EXACT_FIDELITY_GRID_AUTHORIZED"
    else:
        disposition = "TWO_TIER_EXACT_ARB_REQUIRED"

    budget = json.loads(BUDGET.read_text())
    if disposition == "TWO_TIER_EXACT_ARB_REQUIRED":
        fallback = mechanical_tier_boundary(
            median_ns_per_update, budget, prereg
        )
    else:
        fallback = {
            "applied": False,
            "reason": (
                "full exact throughput passed"
                if disposition == "FULL_EXACT_FIDELITY_GRID_AUTHORIZED"
                else "correctness or replay failure requires redesign"
            ),
        }
    payload = {
        "schema": "certified-qmc-workstream-b-streaming-pilot-v1",
        "claim_tags": {
            "residue_and_checkpoint_replay": (
                "VERIFIED"
                if correctness
                else "FAILED_ORACLE_OR_REPLAY_CHECK"
            ),
            "timings_and_projection": "NUMERICAL",
            "production_decision": disposition,
        },
        "preregistration": str(PREREG.relative_to(ROOT)),
        "preregistration_sha256": digest(PREREG),
        "production_budget": str(BUDGET.relative_to(ROOT)),
        "production_budget_sha256": digest(BUDGET),
        "source": {
            "url": (
                "https://web.maths.unsw.edu.au/~fkuo/lattice/"
                "lattice-29102-1024.3600"
            ),
            "sha256": SOURCE_SHA256,
            "rows": 3600,
            "generator_prefix": generator,
            "generator_prefix_sha256": canonical_digest(generator),
        },
        "implementation": {
            "source": str(SOURCE.relative_to(ROOT)),
            "source_sha256": digest(SOURCE),
            "binary_sha256": digest(BINARY),
            "arithmetic": "plain __int128 remainder",
            "layout": "prime-major incremental within-column",
            "threads": threads,
            "platform": platform.platform(),
            "processor": platform.processor(),
            "python": platform.python_version(),
        },
        "prime_schedule": {
            "work_count": prereg["pilot"]["work_primes"],
            "overflow_count": 2,
            "schedule_sha256": canonical_digest(schedule),
            "primes": [str(prime) for prime in primes],
        },
        "runs": runs,
        "measurement": {
            "work_updates_per_run": work_updates,
            "median_ns_per_update_fraction": {
                "numerator": str(median_ns_per_update.numerator),
                "denominator": str(median_ns_per_update.denominator),
            },
            "median_ns_per_update": float(median_ns_per_update),
            "full_grid_work_updates": full_updates,
            "projected_node_days": float(projected_node_days),
            "median_replay_overhead_fraction": float(
                median_replay_fraction
            ),
            "final_checkpoint_sha256": final_checkpoint_sha256,
            "state_bytes_per_prime": runs[0]["state_bytes_per_prime"],
        },
        "correctness": {
            "selected_residue_checks": residue_checks,
            "all_selected_residues_match": all_residues_match,
            "all_checkpoint_replays_pass": all(
                run["checkpoint_replay"] for run in runs
            ),
            "overflow_primes_evaluated_for_every_prefix": all(
                run["output_words"] == len(primes) * dimension
                for run in runs
            ),
        },
        "decision": {
            "correctness_pass": correctness,
            "throughput_pass": throughput_pass,
            "replay_overhead_pass": replay_pass,
            "full_exact_fidelity_grid_authorized": authorized,
            "disposition": disposition,
            "frozen_maximum_node_days": float(maximum_node_days),
            "frozen_maximum_replay_overhead_fraction": float(
                maximum_replay
            ),
            "frozen_maximum_ns_per_update": float(
                Fraction(
                    prereg["production_decision"][
                        "maximum_passing_aggregate_ns_per_update"
                    ]
                )
            ),
        },
        "fallback": fallback,
        "budget_reconciliation": {
            "incremental_count_matches_preflight": (
                full_updates
                == budget["totals"]["combined_direct_update_lower_bound"]
            ),
            "per_cell_from_scratch_used": False,
        },
        "boundary": (
            "The residue equalities and checkpoint replay are verified. "
            "Timing is a local numerical observation. Authorization is "
            "the mechanical result of the prospectively frozen predicate."
        ),
    }
    payload["certificate_sha256"] = canonical_digest(payload)
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )
    print(args.output)
    print(json.dumps(payload["measurement"], indent=2, sort_keys=True))
    print(json.dumps(payload["decision"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
