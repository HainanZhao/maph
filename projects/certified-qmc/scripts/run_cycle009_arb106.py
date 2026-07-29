#!/usr/bin/env python3
"""Run/resume the frozen Cycle-009 Arb-106 certified CBC experiment."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from contextlib import ExitStack
from datetime import datetime, timezone
from fractions import Fraction
from hashlib import sha256
import json
from math import prod
import os
from pathlib import Path
import platform
import struct
import subprocess
import sys
import tempfile
import time


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

from flint import ctx

from src.arb_power2_fastcbc import (
    arb_power2_candidate_scores,
    initial_running_product,
    update_running_product,
)
from src.certificate import canonical_sha256
from src.chunked_table import (
    ZERO_HASH,
    append_record,
    canonical_bytes,
    file_sha256,
    read_chain,
)
from src.crt import balanced_reconstruct, choose_moduli
from src.native_cycle009 import BINARY, build_cycle009_ntt
from src.power2_fastcbc import power2_candidate_classes
from src.scaled_integer import (
    candidate_difference_bound,
    error_numerator_bound,
    factor_denominator,
)


MODULUS = 65536
DIMENSION = 50
PRECISION = 106
COMPARISONS_PER_STAGE = MODULUS // 4 - 1
TOTAL_COMPARISONS = (DIMENSION - 1) * COMPARISONS_PER_STAGE
MAXIMUM_PASSING_EXACT = 802
PREREG_V1 = ROOT / "certificates" / "cycle-009-preregistration.json"
PREREG_V2 = (
    ROOT / "certificates" / "cycle-009-preregistration-v2-arb106.json"
)
SCHEDULE_PATH = ROOT / "certificates" / "cycle-009-prime-schedule-40.json"
COMPILED_GATE = (
    ROOT / "certificates" / "cycle-009-compiled-ntt-gate.json"
)
INTEGRATED_GATE = (
    ROOT / "certificates" / "cycle-009-integrated-preflight.json"
)
QUARANTINE_RECORD = (
    ROOT / "docs" / "cycle009-premature-smoke-quarantine.md"
)
DEFAULT_RELEASE_CERTIFICATE = (
    ROOT / "certificates" / "cycle-018-zenodo-deposition.json"
)
TRACE_STRUCT = struct.Struct("<HHHHbHB")


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def canonical_sha(value: object) -> str:
    return sha256(canonical_bytes(value)).hexdigest()


def load_self_hashed(path: Path, field: str) -> dict:
    value = json.loads(path.read_text())
    supplied = value.pop(field)
    if canonical_sha(value) != supplied:
        raise ValueError(f"{path.name} self-hash mismatch")
    value[field] = supplied
    return value


def verify_release_boundary(path: Path) -> dict:
    certificate = load_self_hashed(path, "certificate_sha256")
    if (
        certificate.get("published") is not True
        or certificate.get("announcement_permitted") is not True
        or not certificate.get("doi")
    ):
        raise ValueError("Cycle 009 may start only after published DOI")
    return certificate


def verify_prerequisites(release_certificate: Path) -> tuple[dict, list[dict]]:
    release = verify_release_boundary(release_certificate)
    prereg_v1 = load_self_hashed(PREREG_V1, "checkpoint_sha256")
    prereg_v2 = load_self_hashed(PREREG_V2, "checkpoint_sha256")
    compiled = load_self_hashed(COMPILED_GATE, "certificate_sha256")
    integrated = load_self_hashed(
        INTEGRATED_GATE, "certificate_sha256"
    )
    if prereg_v1["decision_protocol"]["comparison_count"] != TOTAL_COMPARISONS:
        raise ValueError("Cycle-009 comparison count changed")
    if (
        prereg_v2["unchanged_acceptance_gate"][
            "maximum_passing_count"
        ]
        != MAXIMUM_PASSING_EXACT
        or prereg_v2["primary_decision_architecture"][
            "double_double_enabled"
        ]
        is not False
    ):
        raise ValueError("Cycle-009 Arb-first gate changed")
    if not compiled["gate"][
        "cycle009_compiled_ntt_correctness_gate_passed"
    ]:
        raise ValueError("compiled Cycle-009 NTT gate is not passed")
    if compiled["kernel"]["source_sha256"] != file_sha256(
        ROOT / "native" / "cycle009_ntt.c"
    ):
        raise ValueError("compiled Cycle-009 source changed after gate")
    if not integrated["gate"]["cycle009_integrated_preflight_passed"]:
        raise ValueError("Cycle-009 integrated preflight is not passed")
    schedule = json.loads(SCHEDULE_PATH.read_text())
    if (
        schedule["schedule_sha256"]
        != prereg_v2["unchanged_crt_budget"]["schedule_sha256"]
        or len(schedule["primes"]) != 40
    ):
        raise ValueError("Cycle-009 prime schedule mismatch")
    return release, schedule["primes"]


def build_run_manifest(
    release_certificate: Path,
    release: dict,
    prime_records: list[dict],
) -> dict:
    binary = build_cycle009_ntt()
    linked = subprocess.check_output(["ldd", str(binary)], text=True)
    payload = {
        "schema": "certified-qmc-cycle009-run-manifest-v1",
        "run_id": "cycle-009-arb106-n65536-d50",
        "created_at_utc": utc_now(),
        "target": {
            "N": MODULUS,
            "dimension": DIMENSION,
            "weights": "gamma_j=1/j^2",
            "first_component": 1,
            "candidate_order": "5^a mod N, ascending exponent",
            "candidate_count_per_stage": MODULUS // 4,
            "comparison_count": TOTAL_COMPARISONS,
        },
        "decision_layer": {
            "shadow": "python-flint compiled Arb",
            "precision_bits": PRECISION,
            "double_double_enabled": False,
            "exact_fallback": (
                "balanced CRT of compiled valuation-stratified "
                "score-residue differences"
            ),
            "maximum_passing_exact_crt_escalations": (
                MAXIMUM_PASSING_EXACT
            ),
        },
        "kernel": {
            "binary": str(binary.relative_to(ROOT)),
            "binary_sha256": file_sha256(binary),
            "source": "native/cycle009_ntt.c",
            "source_sha256": file_sha256(
                ROOT / "native" / "cycle009_ntt.c"
            ),
            "compiler": subprocess.check_output(
                ["cc", "--version"], text=True
            ).splitlines()[0],
            "flags": (
                "-O3 -std=c11 -Wall -Wextra -Wpedantic "
                "-D_POSIX_C_SOURCE=200809L"
            ),
            "cpu_model": cpu_model(),
            "platform": platform.platform(),
            "linked_libraries": [
                line.strip() for line in linked.splitlines()
            ],
            "representation": "plain __int128 modular remainder",
        },
        "prerequisites": {
            str(path.relative_to(ROOT)): file_sha256(path)
            for path in (
                PREREG_V1,
                PREREG_V2,
                SCHEDULE_PATH,
                COMPILED_GATE,
                INTEGRATED_GATE,
                QUARANTINE_RECORD,
                release_certificate,
            )
        },
        "release_boundary": {
            "doi": release["doi"],
            "record_url": release["record_url"],
            "certificate_sha256": release["certificate_sha256"],
        },
        "prime_schedule": {
            "count": len(prime_records),
            "sha256": file_sha256(SCHEDULE_PATH),
            "two_overflow_prime_indices": [38, 39],
        },
        "checkpoint": {
            "one append-only hash-chained STAGE record per dimension": True,
            "score_encoding": "N/4 unsigned u64le residues per prime",
            "trace_encoding": (
                "u16 stage, u16 comparison, u16 incumbent, "
                "u16 challenger, i8 sign, u16 selected, u8 resolution"
            ),
            "resolution_codes": {"arb": 1, "exact_crt": 2},
        },
    }
    payload["run_manifest_sha256"] = canonical_sha(payload)
    return payload


def cpu_model() -> str:
    for line in Path("/proc/cpuinfo").read_text().splitlines():
        if line.lower().startswith("model name"):
            return line.split(":", 1)[1].strip()
    return platform.processor() or "UNKNOWN"


def write_exact(path: Path, payload: dict) -> None:
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if path.exists():
        if path.read_text() != rendered:
            raise ValueError(f"resume metadata mismatch: {path.name}")
    else:
        path.write_text(rendered)


def validate_resume(
    output: Path, run_manifest: dict
) -> tuple[list[dict], list[int], dict[str, int]]:
    write_exact(output / "run-manifest.json", run_manifest)
    records = read_chain(output / "manifest.jsonl")
    prefix = [1]
    histogram = {
        "double_double_resolved": 0,
        "arb_resolved": 0,
        "exact_crt_resolved": 0,
        "exact_equalities": 0,
    }
    expected_stage = 2
    for record in records:
        if record["event"] == "SEAL":
            if record is not records[-1]:
                raise ValueError("SEAL is not final")
            result = output / record["result_path"]
            if file_sha256(result) != record["result_sha256"]:
                raise ValueError("Cycle-009 sealed result hash mismatch")
            return records, prefix, histogram
        if record["event"] != "STAGE" or record["stage"] != expected_stage:
            raise ValueError("Cycle-009 checkpoint sequence mismatch")
        if record["run_manifest_sha256"] != run_manifest[
            "run_manifest_sha256"
        ]:
            raise ValueError("checkpoint/run-manifest mismatch")
        stage_dir = output / f"stages/d{expected_stage:02d}"
        trace = stage_dir / "branch-trace.bin"
        if file_sha256(trace) != record["branch_trace_sha256"]:
            raise ValueError("Cycle-009 branch-trace hash mismatch")
        for prime_file in record["prime_score_files"]:
            path = output / prime_file["path"]
            if (
                path.stat().st_size != prime_file["bytes"]
                or file_sha256(path) != prime_file["sha256"]
            ):
                raise ValueError("Cycle-009 score-file hash mismatch")
        prefix.append(int(record["winning_component"]))
        histogram = {
            key: int(value)
            for key, value in record["cumulative_histogram"].items()
        }
        expected_stage += 1
    return records, prefix, histogram


def score_path(output: Path, stage: int, prime_index: int) -> Path:
    return (
        output
        / "stages"
        / f"d{stage:02d}"
        / f"p{prime_index:02d}.bin"
    )


def produce_one_score_file(
    output: Path,
    stage: int,
    prime_index: int,
    prime_record: dict,
    prefix: list[int],
) -> dict:
    final = score_path(output, stage, prime_index)
    final.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        dir=final.parent,
        prefix=f".p{prime_index:02d}-",
        delete=False,
    ) as temporary:
        temporary_path = Path(temporary.name)
    try:
        subprocess.run(
            [
                str(BINARY),
                str(MODULUS),
                str(prime_record["prime"]),
                str(prime_record["primitive_root"]),
                ",".join(str(value) for value in prefix),
                str(temporary_path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        if temporary_path.stat().st_size != (MODULUS // 4) * 8:
            raise ValueError("Cycle-009 score-file size mismatch")
        os.replace(temporary_path, final)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()
    return {
        "prime_index": prime_index,
        "prime": str(prime_record["prime"]),
        "path": str(final.relative_to(output)),
        "bytes": final.stat().st_size,
        "sha256": file_sha256(final),
    }


def produce_stage_scores(
    output: Path,
    stage: int,
    prime_records: list[dict],
    prefix: list[int],
    workers: int,
) -> list[dict]:
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [
            pool.submit(
                produce_one_score_file,
                output,
                stage,
                index,
                record,
                prefix,
            )
            for index, record in enumerate(prime_records)
        ]
        results = [future.result() for future in futures]
    return sorted(results, key=lambda row: row["prime_index"])


def read_score(
    streams: list, candidate_exponent: int
) -> list[int]:
    offset = candidate_exponent * 8
    result = []
    for stream in streams:
        stream.seek(offset)
        raw = stream.read(8)
        if len(raw) != 8:
            raise EOFError("Cycle-009 score residue is absent")
        result.append(struct.unpack("<Q", raw)[0])
    return result


def exact_compare(
    streams: list,
    primes: list[int],
    work_count: int,
    bound: int,
    left_exponent: int,
    right_exponent: int,
) -> tuple[int, bool]:
    left = read_score(streams, left_exponent)
    right = read_score(streams, right_exponent)
    differences = [
        (left[index] - right[index]) % primes[index]
        for index in range(len(primes))
    ]
    value = balanced_reconstruct(
        differences[:work_count],
        primes[:work_count],
        bound=bound,
    )
    for index in (38, 39):
        if value % primes[index] != differences[index]:
            raise ArithmeticError(
                "Cycle-009 exact fallback overflow-prime failure"
            )
    sign = (value > 0) - (value < 0)
    return sign, value == 0


def arb_compare(left, right) -> int | None:
    if left.upper() < right.lower():
        return -1
    if right.upper() < left.lower():
        return 1
    return None


def run_tournament(
    output: Path,
    stage: int,
    balls: list,
    prime_records: list[dict],
    bound: int,
    work_count: int,
) -> tuple[int, dict[str, int], dict, dict[str, float]]:
    stage_dir = output / "stages" / f"d{stage:02d}"
    trace_final = stage_dir / "branch-trace.bin"
    stage_histogram = {
        "double_double_resolved": 0,
        "arb_resolved": 0,
        "exact_crt_resolved": 0,
        "exact_equalities": 0,
    }
    primes = [int(row["prime"]) for row in prime_records]
    tournament_start = time.perf_counter()
    exact_wall = 0.0
    paths = [
        score_path(output, stage, index)
        for index in range(len(prime_records))
    ]
    with ExitStack() as stack:
        streams = [
            stack.enter_context(path.open("rb")) for path in paths
        ]
        with tempfile.NamedTemporaryFile(
            dir=stage_dir,
            prefix=".trace-",
            delete=False,
        ) as trace:
            trace_temporary = Path(trace.name)
            incumbent = 0
            for comparison_index, challenger in enumerate(
                range(1, MODULUS // 4)
            ):
                predecision = incumbent
                sign = arb_compare(
                    balls[incumbent], balls[challenger]
                )
                if sign is None:
                    exact_start = time.perf_counter()
                    sign, equality = exact_compare(
                        streams,
                        primes,
                        work_count,
                        bound,
                        incumbent,
                        challenger,
                    )
                    exact_wall += time.perf_counter() - exact_start
                    resolution = 2
                    stage_histogram["exact_crt_resolved"] += 1
                    if equality:
                        stage_histogram["exact_equalities"] += 1
                else:
                    resolution = 1
                    stage_histogram["arb_resolved"] += 1
                if sign > 0:
                    incumbent = challenger
                trace.write(
                    TRACE_STRUCT.pack(
                        stage,
                        comparison_index,
                        predecision,
                        challenger,
                        sign,
                        incumbent,
                        resolution,
                    )
                )
    os.replace(trace_temporary, trace_final)
    if sum(
        stage_histogram[key]
        for key in ("arb_resolved", "exact_crt_resolved")
    ) != COMPARISONS_PER_STAGE:
        raise ArithmeticError("Cycle-009 stage histogram mismatch")
    trace_metadata = {
        "path": str(trace_final.relative_to(output)),
        "bytes": trace_final.stat().st_size,
        "record_count": COMPARISONS_PER_STAGE,
        "record_size": TRACE_STRUCT.size,
        "sha256": file_sha256(trace_final),
    }
    tournament_wall = time.perf_counter() - tournament_start
    return (
        incumbent,
        stage_histogram,
        trace_metadata,
        {
            "tournament_wall_seconds": tournament_wall,
            "exact_crt_wall_seconds": exact_wall,
            "arb_comparison_wall_seconds": tournament_wall - exact_wall,
        },
    )


def add_histograms(
    left: dict[str, int], right: dict[str, int]
) -> dict[str, int]:
    return {key: int(left[key]) + int(right[key]) for key in left}


def final_exact_merit(
    output: Path,
    prefix: list[int],
    records: list[dict],
    prime_records: list[dict],
) -> dict:
    if len(prefix) != DIMENSION:
        raise ValueError("final vector is incomplete")
    stage_record = next(
        record
        for record in records
        if record.get("event") == "STAGE"
        and record.get("stage") == DIMENSION
    )
    exponent = int(stage_record["winning_exponent"])
    primes = [int(row["prime"]) for row in prime_records]
    summand_residues = []
    for index in range(len(primes)):
        path = score_path(output, DIMENSION, index)
        with path.open("rb") as stream:
            stream.seek(exponent * 8)
            summand_residues.append(struct.unpack("<Q", stream.read(8))[0])
    weights = [
        Fraction(1, index * index)
        for index in range(1, DIMENSION + 1)
    ]
    denominator_product = prod(
        factor_denominator(MODULUS, weight) for weight in weights
    )
    error_residues = [
        (
            summand_residues[index]
            - (MODULUS * denominator_product) % primes[index]
        )
        % primes[index]
        for index in range(len(primes))
    ]
    bound = error_numerator_bound(MODULUS, weights)
    moduli = choose_moduli(primes[:38], bound)
    numerator = balanced_reconstruct(
        error_residues[: len(moduli)],
        primes[: len(moduli)],
        bound=bound,
    )
    overflow = []
    for index in (38, 39):
        equal = numerator % primes[index] == error_residues[index]
        overflow.append({"prime_index": index, "equal": equal})
    if not all(row["equal"] for row in overflow):
        raise ArithmeticError("final merit overflow-prime failure")
    denominator = MODULUS * denominator_product
    value = Fraction(numerator, denominator)
    return {
        "claim_tag": "VERIFIED",
        "generator": prefix,
        "generator_sha256": canonical_sha(prefix),
        "minimal_work_prime_count": len(moduli),
        "proved_numerator_bound": str(bound),
        "scaled_numerator": str(numerator),
        "scaled_denominator": str(denominator),
        "reduced_numerator": str(value.numerator),
        "reduced_denominator": str(value.denominator),
        "overflow_checks": overflow,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--release-certificate",
        type=Path,
        default=DEFAULT_RELEASE_CERTIFICATE,
    )
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    if args.workers < 1:
        raise ValueError("workers must be positive")
    release_certificate = args.release_certificate.resolve()
    release, prime_records = verify_prerequisites(release_certificate)
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    run_manifest_path = output / "run-manifest.json"
    if run_manifest_path.exists():
        run_manifest = load_self_hashed(
            run_manifest_path, "run_manifest_sha256"
        )
        binary = build_cycle009_ntt()
        if (
            file_sha256(binary)
            != run_manifest["kernel"]["binary_sha256"]
            or file_sha256(ROOT / run_manifest["kernel"]["source"])
            != run_manifest["kernel"]["source_sha256"]
        ):
            raise ValueError("Cycle-009 resume kernel mismatch")
        for path, expected in run_manifest["prerequisites"].items():
            if file_sha256(ROOT / path) != expected:
                raise ValueError("Cycle-009 resume prerequisite mismatch")
    else:
        run_manifest = build_run_manifest(
            release_certificate, release, prime_records
        )
    records, prefix, cumulative = validate_resume(
        output, run_manifest
    )
    if records and records[-1]["event"] == "SEAL":
        print(output / "cycle-009-result.json")
        return

    previous_total_wall = sum(
        float(record.get("stage_wall_seconds", 0.0))
        for record in records
        if record.get("event") == "STAGE"
    )
    previous_arb_wall = sum(
        float(record.get("arb_wall_seconds", 0.0))
        for record in records
        if record.get("event") == "STAGE"
    )
    start_wall = time.perf_counter()
    arb_wall = previous_arb_wall
    with ctx.workprec(PRECISION):
        state = initial_running_product(MODULUS)
        for index, component in enumerate(prefix, start=1):
            state = update_running_product(
                state,
                component,
                Fraction(1, index * index),
            )
        candidates = power2_candidate_classes(MODULUS)
        if len(candidates) != MODULUS // 4:
            raise ArithmeticError("candidate count mismatch")

        for stage in range(len(prefix) + 1, DIMENSION + 1):
            stage_start = time.perf_counter()
            prime_files = produce_stage_scores(
                output,
                stage,
                prime_records,
                prefix,
                args.workers,
            )
            arb_score_start = time.perf_counter()
            returned_candidates, balls = arb_power2_candidate_scores(
                MODULUS,
                state,
                Fraction(1, stage * stage),
                precision=PRECISION,
            )
            if returned_candidates != candidates:
                raise ArithmeticError("Arb candidate order mismatch")
            arb_score_elapsed = time.perf_counter() - arb_score_start
            previous_weights = [
                Fraction(1, index * index)
                for index in range(1, stage)
            ]
            bound = candidate_difference_bound(
                MODULUS,
                previous_weights,
                Fraction(1, stage * stage),
            )
            primes = [int(row["prime"]) for row in prime_records]
            work_count = len(choose_moduli(primes[:38], bound))
            (
                winning_exponent,
                stage_histogram,
                trace_metadata,
                tournament_timing,
            ) = run_tournament(
                output,
                stage,
                balls,
                prime_records,
                bound,
                work_count,
            )
            arb_elapsed = (
                arb_score_elapsed
                + tournament_timing["arb_comparison_wall_seconds"]
            )
            arb_wall += arb_elapsed
            winning_component = candidates[winning_exponent]
            state = update_running_product(
                state,
                winning_component,
                Fraction(1, stage * stage),
            )
            prefix.append(winning_component)
            cumulative = add_histograms(
                cumulative, stage_histogram
            )
            stage_record = {
                "sequence": len(records),
                "event": "STAGE",
                "stage": stage,
                "run_manifest_sha256": run_manifest[
                    "run_manifest_sha256"
                ],
                "prefix_sha256": canonical_sha(prefix),
                "winning_exponent": winning_exponent,
                "winning_component": winning_component,
                "candidate_difference_bound": str(bound),
                "exact_work_prime_count": work_count,
                "stage_histogram": stage_histogram,
                "cumulative_histogram": cumulative,
                "branch_trace_path": trace_metadata["path"],
                "branch_trace_sha256": trace_metadata["sha256"],
                "branch_trace_bytes": trace_metadata["bytes"],
                "prime_score_files": prime_files,
                "arb_score_wall_seconds": arb_score_elapsed,
                **tournament_timing,
                "arb_wall_seconds": arb_elapsed,
                "stage_wall_seconds": time.perf_counter() - stage_start,
            }
            previous = (
                records[-1]["line_sha256"] if records else ZERO_HASH
            )
            appended = append_record(
                output / "manifest.jsonl",
                stage_record,
                previous,
            )
            records.append(appended)

    total_wall = previous_total_wall + time.perf_counter() - start_wall
    if cumulative["double_double_resolved"] != 0:
        raise ArithmeticError("primary Arb run entered DD layer")
    if (
        cumulative["arb_resolved"]
        + cumulative["exact_crt_resolved"]
        != TOTAL_COMPARISONS
    ):
        raise ArithmeticError("final comparison count mismatch")
    merit = final_exact_merit(
        output, prefix, records, prime_records
    )
    passed = cumulative["exact_crt_resolved"] < 803
    result = {
        "schema": "certified-qmc-cycle009-arb106-result-v1",
        "recorded_at_utc": utc_now(),
        "claim_tags": {
            "search_decisions": "VERIFIED" if passed else "NUMERICAL",
            "final_vector_merit": "VERIFIED",
            "timings": "NUMERICAL",
        },
        "run_manifest_sha256": run_manifest["run_manifest_sha256"],
        "comparison_count": TOTAL_COMPARISONS,
        "histogram": cumulative,
        "exact_crt_escalation_rate": (
            cumulative["exact_crt_resolved"] / TOTAL_COMPARISONS
        ),
        "acceptance": {
            "predicate": "exact_crt_resolved<803",
            "passed": passed,
        },
        "timing": {
            "total_wall_seconds": total_wall,
            "arb_wall_seconds": arb_wall,
            "arb_fraction_of_total_wall_time": arb_wall / total_wall,
        },
        "final_merit": merit,
        "boundary": (
            "A passing decision gate certifies the frozen tournament. "
            "Regardless of that gate, the final vector merit is exact."
        ),
    }
    result["certificate_sha256"] = canonical_sha256(result)
    result_path = output / "cycle-009-result.json"
    result_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    seal = {
        "sequence": len(records),
        "event": "SEAL",
        "run_manifest_sha256": run_manifest["run_manifest_sha256"],
        "result_path": result_path.name,
        "result_sha256": file_sha256(result_path),
        "comparison_count": TOTAL_COMPARISONS,
        "acceptance_passed": passed,
    }
    previous = records[-1]["line_sha256"]
    append_record(output / "manifest.jsonl", seal, previous)
    print(result_path)


if __name__ == "__main__":
    main()
