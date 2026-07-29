#!/usr/bin/env python3
"""Freeze generic NTT and composite-2^m CBC mapping validations."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import argparse
import json
from pathlib import Path
import platform
import random
import sys
from time import perf_counter_ns

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))

from src.ntt import direct_cyclic_convolution, ntt_cyclic_convolution
from src.ntt_prime import generate_ntt_prime_schedule
from src.power2_fastcbc import (
    direct_power2_candidate_scores,
    power2_strata,
    stratified_ntt_candidate_scores,
)


PREFIX = [1, 275, 179, 319, 299, 451, 417, 167]
WEIGHTS = [Fraction(1, j * j) for j in range(1, 10)]


def digest(values) -> str:
    return sha256(
        "".join(f"{index}:{value}\n" for index, value in enumerate(values))
        .encode("ascii")
    ).hexdigest()


def timed(function, repeats: int):
    samples = []
    result = None
    for _ in range(repeats):
        start = perf_counter_ns()
        result = function()
        samples.append(perf_counter_ns() - start)
    return result, {
        "tag": "NUMERICAL",
        "repeats": repeats,
        "minimum_ns": min(samples),
        "median_ns": sorted(samples)[len(samples) // 2],
        "samples_ns": samples,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ntt-output", type=Path)
    parser.add_argument("--mapping-output", type=Path)
    args = parser.parse_args()
    prime_record = generate_ntt_prime_schedule(1)[0]
    prime = int(prime_record["prime"])
    root = int(prime_record["primitive_root"])

    source = random.Random(20260803)
    convolution_rows = []
    for length in (1, 2, 4, 8, 16, 32, 64, 256):
        left = [source.randrange(prime) for _ in range(length)]
        right = [source.randrange(prime) for _ in range(length)]
        direct = direct_cyclic_convolution(left, right, prime)
        transformed = ntt_cyclic_convolution(left, right, prime, root)
        if direct != transformed:
            raise ArithmeticError("NTT convolution mismatch")
        convolution_rows.append(
            {
                "length": length,
                "result_sha256": digest(direct),
                "equal_to_quadratic_convolution": True,
            }
        )
    ntt_result = {
        "schema": "certified-qmc-radix2-ntt-validation-v1",
        "date": "2026-07-29",
        "tag": "VERIFIED",
        "prime": str(prime),
        "primitive_root": root,
        "seed": 20260803,
        "convolutions": convolution_rows,
        "claim_boundary": (
            "Validates the pure-Python radix-two transform and cyclic "
            "convolution over one audited prime; not an optimized NTT."
        ),
    }

    direct_candidates, direct_scores = direct_power2_candidate_scores(
        1024, PREFIX, WEIGHTS, prime
    )
    fast_candidates, fast_scores = stratified_ntt_candidate_scores(
        1024, PREFIX, WEIGHTS, prime, root
    )
    if (direct_candidates, direct_scores) != (fast_candidates, fast_scores):
        raise ArithmeticError("power-two mapping mismatch")

    benchmarks = []
    for modulus in (256, 1024, 4096):
        direct_pair, direct_timing = timed(
            lambda modulus=modulus: direct_power2_candidate_scores(
                modulus, PREFIX, WEIGHTS, prime
            ),
            3,
        )
        fast_pair, fast_timing = timed(
            lambda modulus=modulus: stratified_ntt_candidate_scores(
                modulus, PREFIX, WEIGHTS, prime, root
            ),
            3,
        )
        if direct_pair != fast_pair:
            raise ArithmeticError("benchmark score mismatch")
        benchmarks.append(
            {
                "modulus": modulus,
                "candidate_classes": modulus // 4,
                "direct": direct_timing,
                "stratified_ntt": fast_timing,
                "minimum_speedup": (
                    direct_timing["minimum_ns"]
                    / fast_timing["minimum_ns"]
                ),
                "all_scores_equal": True,
            }
        )

    mapping_result = {
        "schema": "certified-qmc-power2-fastcbc-map-v1",
        "date": "2026-07-29",
        "tag": "VERIFIED_MAPPING",
        "group": "U(2^m)=<-1> x <5>, m>=3",
        "kernel_symmetry": "P(k)=P(-k), F(k)=F(-k)",
        "candidate_classes": "5^a modulo 2^m, 0<=a<2^(m-2)",
        "frozen_case": {
            "modulus": 1024,
            "prefix": PREFIX,
            "new_dimension": 9,
            "weight_model": "gamma_j=1/j^2",
            "prime": str(prime),
            "candidate_count": len(direct_candidates),
            "candidate_sha256": digest(direct_candidates),
            "score_sha256": digest(direct_scores),
            "all_scores_equal_to_direct_enumeration": True,
            "strata": power2_strata(1024),
        },
        "benchmark": benchmarks,
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
        "claim_boundary": (
            "The modular score mapping is VERIFIED. Timings are local "
            "NUMERICAL observations; exact multi-prime fast CBC and "
            "certified branch selection remain open."
        ),
    }

    for path, result in (
        (args.ntt_output, ntt_result),
        (args.mapping_output, mapping_result),
    ):
        rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if path:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(rendered, encoding="utf-8")
        else:
            print(rendered, end="")


if __name__ == "__main__":
    main()
