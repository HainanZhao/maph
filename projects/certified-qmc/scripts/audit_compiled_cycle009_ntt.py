#!/usr/bin/env python3
"""Bank the compiled valuation-stratified NTT correctness gate."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import struct
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.certificate import canonical_sha256
from src.native_cycle009 import (
    BINARY,
    build_cycle009_ntt,
    compiled_candidate_scores,
)
from src.ntt_prime import generate_ntt_prime_schedule
from src.power2_fastcbc import (
    direct_power2_candidate_scores,
    power2_candidate_classes,
    stratified_ntt_candidate_scores,
)


SOURCE = ROOT / "native" / "cycle009_ntt.c"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def vector_digest(values: list[int]) -> str:
    hasher = sha256()
    for value in values:
        hasher.update(struct.pack("<Q", value))
    return hasher.hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    binary = build_cycle009_ntt()
    schedule = generate_ntt_prime_schedule(2)
    cases = []
    for exponent in range(3, 13):
        modulus = 1 << exponent
        prefix_length = min(8, exponent + 1)
        prefix = [
            pow(5, index, modulus)
            for index in range(prefix_length)
        ]
        weights = [
            f"1/{index * index}"
            for index in range(1, prefix_length + 2)
        ]
        for prime_record in schedule:
            prime = int(prime_record["prime"])
            root = int(prime_record["primitive_root"])
            compiled = compiled_candidate_scores(
                modulus,
                prime,
                root,
                prefix,
                binary=binary,
            )
            candidates, python_scores = (
                stratified_ntt_candidate_scores(
                    modulus, prefix, weights, prime, root
                )
            )
            if compiled != python_scores:
                raise ArithmeticError(
                    f"compiled/Python NTT mismatch at N={modulus}"
                )
            direct_checked = modulus <= 256
            if direct_checked:
                direct_candidates, direct_scores = (
                    direct_power2_candidate_scores(
                        modulus, prefix, weights, prime
                    )
                )
                if (
                    direct_candidates != candidates
                    or direct_scores != compiled
                ):
                    raise ArithmeticError(
                        f"compiled/direct mismatch at N={modulus}"
                    )
            expected_candidates = power2_candidate_classes(modulus)
            if candidates != expected_candidates:
                raise ArithmeticError("candidate-order mismatch")
            cases.append(
                {
                    "N": modulus,
                    "prefix": prefix,
                    "new_dimension": prefix_length + 1,
                    "prime": str(prime),
                    "primitive_root": str(root),
                    "candidate_count": len(candidates),
                    "candidate_sha256_u64le": vector_digest(candidates),
                    "score_sha256_u64le": vector_digest(compiled),
                    "compiled_equals_python_ntt_all_candidates": True,
                    "compiled_equals_direct_all_candidates": (
                        True if direct_checked else None
                    ),
                }
            )

    linked = subprocess.check_output(["ldd", str(BINARY)], text=True)
    payload = {
        "schema": "certified-qmc-cycle009-compiled-ntt-gate-v1",
        "recorded_at_utc": utc_now(),
        "claim_tag": "VERIFIED",
        "kernel": {
            "source": str(SOURCE.relative_to(ROOT)),
            "source_sha256": digest(SOURCE),
            "binary": str(BINARY.relative_to(ROOT)),
            "binary_sha256": digest(BINARY),
            "compiler": subprocess.check_output(
                ["cc", "--version"], text=True
            ).splitlines()[0],
            "flags": (
                "-O3 -std=c11 -Wall -Wextra -Wpedantic "
                "-D_POSIX_C_SOURCE=200809L"
            ),
            "representation": "plain __int128 modular remainder",
            "linked_libraries": [
                line.strip() for line in linked.splitlines()
            ],
        },
        "coverage": {
            "moduli": [1 << exponent for exponent in range(3, 13)],
            "prime_count": len(schedule),
            "case_count": len(cases),
            "all_candidates_checked_per_case": True,
            "direct_oracle_through_N": 256,
            "independent_python_ntt_through_N": 4096,
        },
        "cases": cases,
        "gate": {
            "compiled_equals_python_ntt_all_cases": True,
            "compiled_equals_direct_on_tractable_cases": True,
            "cycle009_compiled_ntt_correctness_gate_passed": True,
        },
    }
    payload["certificate_sha256"] = canonical_sha256(payload)
    output = args.output.resolve()
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(output)


if __name__ == "__main__":
    main()
