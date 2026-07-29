#!/usr/bin/env python3
"""Pre-register the nonduplicated Cycle-018 usability computation."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.crt import choose_moduli
from src.scaled_integer import balanced_crt_bits, error_numerator_bound


FIDELITY_SPEC = (
    ROOT / "data" / "cycles-016-017-fidelity-spec-v2.json"
)
FIDELITY_PREREG = (
    ROOT / "data" / "cycles-016-017-preregistration-v2.json"
)
SCHEDULE = ROOT / "data" / "primes-schedule-v1.json"
OUTPUT_SPEC = ROOT / "data" / "cycle-018-usability-spec.json"
OUTPUT_PREREG = (
    ROOT / "data" / "cycle-018-usability-preregistration.json"
)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: object) -> str:
    return sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")
    ).hexdigest()


def main() -> None:
    if len(sys.argv) != 2 or not sys.argv[1].endswith("Z"):
        raise SystemExit(
            "usage: prepare_usability_grid.py FROZEN_AT_UTC"
        )
    frozen_at = sys.argv[1]
    fidelity = json.loads(FIDELITY_SPEC.read_text())
    schedule = json.loads(SCHEDULE.read_text())
    primes = [
        int(row["p"]) for row in schedule["primes"][:3738]
    ]

    fidelity_tables = {
        (table["source_id"], int(table["N"])): table
        for table in fidelity["tables"]
    }
    budgets = {}
    for modulus in (2**10, 2**15, 2**20):
        for power in (1, 3):
            weights = [
                Fraction(1, index**power)
                for index in range(1, 257)
            ]
            bound = error_numerator_bound(modulus, weights)
            count = len(choose_moduli(primes, bound))
            budgets[(modulus, power)] = {
                "proved_numerator_bound_bits": bound.bit_length(),
                "proved_balanced_crt_bits": balanced_crt_bits(bound),
                "work_prime_count": count,
                "incremental_updates_per_table": (
                    modulus * 256 * count
                ),
            }

    tables = []
    for source_id in (
        "unsw-fixed-29102",
        "unsw-extensible-39102",
    ):
        for modulus in (2**10, 2**15, 2**20):
            source = fidelity_tables[(source_id, modulus)]
            for power in (1, 3):
                budget = budgets[(modulus, power)]
                tables.append(
                    {
                        "table_id": (
                            f"{source_id}-n{modulus}-j{power}-"
                            "usability"
                        ),
                        "source_id": source_id,
                        "source_citation": source["source_citation"],
                        "source_path": source["source_path"],
                        "source_snapshot_sha256": source[
                            "source_snapshot_sha256"
                        ],
                        "source_file_sha256": source[
                            "source_file_sha256"
                        ],
                        "N": modulus,
                        "dimension": 256,
                        "weight_power": power,
                        "work_prime_count": budget[
                            "work_prime_count"
                        ],
                    }
                )

    spec = {
        "schema": "certified-qmc-chunked-production-spec-v1",
        "run_id": "cycle-018-usability-v1",
        "frozen_at_utc": frozen_at,
        "prefix_block_size": 256,
        "parallel_workers": 4,
        "prime_schedule": "data/primes-schedule-v1.json",
        "prime_schedule_manifest": (
            "certificates/cycle-014-prime-schedule-manifest.json"
        ),
        "preregistrations": [
            "data/cycle-018-usability-preregistration.json",
            "data/cycles-016-017-preregistration-v2.json",
            "data/workstream-b-production-freeze.json",
        ],
        "throughput_monitor": {
            "claim_tag": "NUMERICAL",
            "pilot_median_aggregate_ns_per_update":
                "2.482743143245874",
            "maximum_aggregate_ns_per_update":
                "4.34480050068027950",
            "drift_fraction": "0.75",
            "minimum_updates_before_enforcement": 5_000_000_000,
            "failure_exit_code": 76,
            "action": "PAUSE_AND_INVESTIGATE",
            "inherits": (
                "human-authorized Cycles 016-017 v2 VPS monitor"
            ),
        },
        "tables": tables,
        "logical_dimensions": [16, 64, 256],
        "intermediate_prefix_policy": (
            "Dimensions other than 16,64,256 are necessary "
            "incremental state and are not members of the frozen "
            "usability table grid."
        ),
        "boundary": (
            "This computation contains only j^-1 and j^-3. Every "
            "j^-2 usability entry must be reused from the sealed "
            "fidelity artifact and authenticated by hash."
        ),
    }
    OUTPUT_SPEC.write_text(
        json.dumps(spec, indent=2, sort_keys=True) + "\n"
    )

    prereg = {
        "schema": (
            "certified-qmc-cycle-018-usability-"
            "preregistration-v1"
        ),
        "frozen_at_utc": frozen_at,
        "production_started": False,
        "production_spec": {
            "path": str(OUTPUT_SPEC.relative_to(ROOT)),
            "sha256": digest(OUTPUT_SPEC),
        },
        "fidelity_predecessor": {
            "spec_path": str(FIDELITY_SPEC.relative_to(ROOT)),
            "spec_sha256": digest(FIDELITY_SPEC),
            "preregistration_path": str(
                FIDELITY_PREREG.relative_to(ROOT)
            ),
            "preregistration_sha256": digest(FIDELITY_PREREG),
            "required_state_before_cycle_018_compute": (
                "fidelity-v2 is sealed and its Cycles 016-017 exit "
                "gate certificate passes"
            ),
        },
        "grid": {
            "families": [
                "unsw-fixed-29102",
                "unsw-extensible-39102",
            ],
            "N": [2**10, 2**15, 2**20],
            "dimensions": [16, 64, 256],
            "weight_powers": [1, 2, 3],
            "logical_entries": 54,
            "computed_nonduplicated_entries": 36,
            "reused_j2_entries": 18,
        },
        "weight_denominator_budgets": {
            f"N{modulus}-j{power}": budget
            for (modulus, power), budget in budgets.items()
        },
        "schedule": {
            "path": str(SCHEDULE.relative_to(ROOT)),
            "sha256": digest(SCHEDULE),
            "available_work_primes": 3738,
            "maximum_required_work_primes": max(
                budget["work_prime_count"]
                for budget in budgets.values()
            ),
            "extension_required": False,
        },
        "reuse_gate": {
            "rule": (
                "For all 18 j^-2 entries, source file hash, N, "
                "dimension, weight power, generator-prefix hash, "
                "residue chunk hashes, and reconstructed rational "
                "must be inherited from fidelity-v2; recomputation "
                "is forbidden."
            ),
            "certificate_required_before_packaging": True,
        },
        "halt_conditions": [
            "fidelity predecessor is unsealed or fails its exit gate",
            "any source, schedule, or preregistration hash mismatch",
            "any overflow-prime or selected-entry replay failure",
            "throughput above the versioned VPS ceiling",
            "any attempted j^-2 recomputation",
        ],
        "boundary": (
            "Prime counts include the corrected weight-denominator "
            "term and are fixed before Cycle-018 computation."
        ),
    }
    prereg["preregistration_sha256"] = canonical_sha(prereg)
    OUTPUT_PREREG.write_text(
        json.dumps(prereg, indent=2, sort_keys=True) + "\n"
    )
    print(
        json.dumps(
            {
                "spec_sha256": digest(OUTPUT_SPEC),
                "preregistration_file_sha256": digest(OUTPUT_PREREG),
                "work_prime_counts": {
                    f"N{modulus}-j{power}": value[
                        "work_prime_count"
                    ]
                    for (modulus, power), value in budgets.items()
                },
                "schedule_extension_required": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
