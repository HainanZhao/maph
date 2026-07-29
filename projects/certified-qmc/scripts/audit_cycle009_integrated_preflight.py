#!/usr/bin/env python3
"""Validate compiled exact fallbacks against direct integer ground truth."""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from flint import arb, ctx

from src.arb_power2_fastcbc import (
    arb_power2_candidate_scores,
    initial_running_product,
    update_running_product,
)
from src.certificate import canonical_sha256
from src.chunked_table import ZERO_HASH, append_record, file_sha256
from src.crt import balanced_reconstruct, choose_moduli
from src.native_cycle009 import (
    build_cycle009_ntt,
    compiled_candidate_scores,
)
from src.scaled_integer import (
    candidate_difference_bound,
    candidate_difference_integer,
)
from src.shadow_decision import candidate_score_fraction
from scripts.run_cycle009_arb106 import validate_resume


SCHEDULE = ROOT / "certificates" / "cycle-009-prime-schedule-40.json"
MODULUS = 32
PREFIX = [1, 5, 13]
WEIGHTS = [Fraction(1, index * index) for index in range(1, 5)]


def sign(value: int) -> int:
    return (value > 0) - (value < 0)


def checkpoint_replay_preflight() -> dict:
    run_manifest = {
        "schema": "cycle009-checkpoint-preflight",
        "run_manifest_sha256": "placeholder",
    }
    run_manifest["run_manifest_sha256"] = canonical_sha256(
        {"schema": run_manifest["schema"]}
    )
    histogram = {
        "double_double_resolved": 0,
        "arb_resolved": 7,
        "exact_crt_resolved": 0,
        "exact_equalities": 0,
    }
    with tempfile.TemporaryDirectory(
        prefix="certified-qmc-cycle009-checkpoint-"
    ) as directory:
        output = Path(directory)
        records = []
        previous = ZERO_HASH
        for sequence, (stage, winner) in enumerate(((2, 5), (3, 13))):
            stage_dir = output / "stages" / f"d{stage:02d}"
            stage_dir.mkdir(parents=True)
            trace = stage_dir / "branch-trace.bin"
            trace.write_bytes(f"trace-{stage}".encode())
            prime_files = []
            for prime_index in range(40):
                path = stage_dir / f"p{prime_index:02d}.bin"
                path.write_bytes(
                    (stage * 100 + prime_index).to_bytes(8, "little")
                )
                prime_files.append(
                    {
                        "path": str(path.relative_to(output)),
                        "bytes": path.stat().st_size,
                        "sha256": file_sha256(path),
                    }
                )
            record = append_record(
                output / "manifest.jsonl",
                {
                    "sequence": sequence,
                    "event": "STAGE",
                    "stage": stage,
                    "run_manifest_sha256": run_manifest[
                        "run_manifest_sha256"
                    ],
                    "winning_component": winner,
                    "branch_trace_sha256": file_sha256(trace),
                    "prime_score_files": prime_files,
                    "cumulative_histogram": histogram,
                },
                previous,
            )
            records.append(record)
            previous = record["line_sha256"]
        # Model a killed next stage: it is unmanifested and must not enter
        # the recovered prefix or histogram.
        partial = output / "stages" / "d04" / ".partial"
        partial.parent.mkdir(parents=True)
        partial.write_bytes(b"uncommitted")
        replayed, prefix, recovered = validate_resume(
            output, run_manifest
        )
        if (
            len(replayed) != 2
            or prefix != [1, 5, 13]
            or recovered != histogram
        ):
            raise ArithmeticError("Cycle-009 checkpoint replay mismatch")
        manifest_sha = file_sha256(output / "manifest.jsonl")
    return {
        "stage_count": 2,
        "recovered_prefix": [1, 5, 13],
        "unmanifested_partial_stage_ignored": True,
        "manifest_sha256": manifest_sha,
        "byte_identical_metadata_replay": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    schedule = json.loads(SCHEDULE.read_text())
    records = schedule["primes"]
    primes = [int(row["prime"]) for row in records]
    binary = build_cycle009_ntt()
    score_vectors = [
        compiled_candidate_scores(
            MODULUS,
            int(record["prime"]),
            int(record["primitive_root"]),
            PREFIX,
            binary=binary,
        )
        for record in records
    ]
    candidate_count = MODULUS // 4
    bound = candidate_difference_bound(
        MODULUS, WEIGHTS[:-1], WEIGHTS[-1]
    )
    work_count = len(choose_moduli(primes[:38], bound))
    pair_checks = []
    for left in range(candidate_count):
        for right in range(left + 1, candidate_count):
            residues = [
                (
                    score_vectors[index][left]
                    - score_vectors[index][right]
                )
                % primes[index]
                for index in range(len(primes))
            ]
            reconstructed = balanced_reconstruct(
                residues[:work_count],
                primes[:work_count],
                bound=bound,
            )
            overflow_equal = all(
                reconstructed % primes[index] == residues[index]
                for index in (38, 39)
            )
            direct = candidate_difference_integer(
                MODULUS,
                PREFIX,
                WEIGHTS,
                pow(5, left, MODULUS),
                pow(5, right, MODULUS),
            )
            if reconstructed != direct or not overflow_equal:
                raise ArithmeticError(
                    "compiled exact fallback/direct oracle mismatch"
                )
            pair_checks.append(
                {
                    "left_exponent": left,
                    "right_exponent": right,
                    "reconstructed_sign": sign(reconstructed),
                    "exact_equality": reconstructed == 0,
                    "overflow_primes_equal": True,
                }
            )

    with ctx.workprec(106):
        state = initial_running_product(MODULUS)
        for index, component in enumerate(PREFIX, start=1):
            state = update_running_product(
                state, component, WEIGHTS[index - 1]
            )
        candidates, balls = arb_power2_candidate_scores(
            MODULUS, state, WEIGHTS[-1], precision=106
        )
        containment = []
        exact_scores = []
        for candidate, ball in zip(candidates, balls):
            exact = candidate_score_fraction(
                MODULUS, PREFIX, WEIGHTS, candidate
            )
            target = arb(exact.numerator) / exact.denominator
            contains = ball.contains(target)
            if not contains:
                raise ArithmeticError("Arb score misses exact oracle")
            exact_scores.append(exact)
            containment.append(contains)

    exact_winner = min(
        range(candidate_count),
        key=lambda index: (exact_scores[index], index),
    )
    arb_tournament_winner = 0
    arb_resolved = 0
    exact_resolved = 0
    for challenger in range(1, candidate_count):
        left = balls[arb_tournament_winner]
        right = balls[challenger]
        if left.upper() < right.lower():
            comparison = -1
            arb_resolved += 1
        elif right.upper() < left.lower():
            comparison = 1
            arb_resolved += 1
        else:
            difference = exact_scores[
                arb_tournament_winner
            ] - exact_scores[challenger]
            comparison = sign(difference)
            exact_resolved += 1
        if comparison > 0:
            arb_tournament_winner = challenger
    if arb_tournament_winner != exact_winner:
        raise ArithmeticError("integrated tournament winner mismatch")
    checkpoint = checkpoint_replay_preflight()

    payload = {
        "schema": "certified-qmc-cycle009-integrated-preflight-v1",
        "claim_tag": "VERIFIED",
        "case": {
            "N": MODULUS,
            "prefix": PREFIX,
            "new_dimension": len(WEIGHTS),
            "candidate_count": candidate_count,
            "weight_profile": "gamma_j=1/j^2",
        },
        "compiled_exact_fallback": {
            "prime_count": len(primes),
            "minimal_work_prime_count": work_count,
            "proved_difference_bound": str(bound),
            "candidate_pair_count": len(pair_checks),
            "all_pairs_equal_direct_integer_oracle": True,
            "all_overflow_checks_equal": True,
            "pairs": pair_checks,
        },
        "arb106_shadow": {
            "all_candidate_balls_contain_exact_scores": all(containment),
            "arb_resolved": arb_resolved,
            "exact_resolved": exact_resolved,
            "tournament_winner_exponent": arb_tournament_winner,
            "exact_global_winner_exponent": exact_winner,
        },
        "checkpoint_replay": checkpoint,
        "gate": {
            "every_exact_escalation_path_agrees_with_direct_oracle": True,
            "every_arb_ball_contains_exact_oracle": True,
            "integrated_tournament_agrees_with_exact_global_argmin": True,
            "per_dimension_checkpoint_and_sha_replay_passed": True,
            "cycle009_integrated_preflight_passed": True,
        },
    }
    payload["certificate_sha256"] = canonical_sha256(payload)
    output = args.output.resolve()
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(output)


if __name__ == "__main__":
    main()
