#!/usr/bin/env python3
"""Search prime-power exponent families using the smallest Lucas box."""

from __future__ import annotations

import argparse
import sys
from itertools import product
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.erdos700 import (  # noqa: E402
    reciprocal_defect,
    search_near_multiple_via_smallest_box,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--primes", type=int, nargs="+", default=(2, 3, 5))
    parser.add_argument("--max-exponent", type=int, default=12)
    parser.add_argument("--max-box-size", type=int, default=200_000)
    args = parser.parse_args()

    if len(set(args.primes)) != len(args.primes):
        parser.error("primes must be distinct")
    radical = 1
    for p in args.primes:
        radical *= p
    if reciprocal_defect(radical) >= 0:
        parser.error("the supplied prime kernel is not reciprocal-supercritical")

    complete = 0
    incomplete = 0
    candidates_tested = 0
    witness_cases = []
    largest_complete = None
    most_candidates = None

    exponent_range = range(1, args.max_exponent + 1)
    for exponents in product(exponent_range, repeat=len(args.primes)):
        multiple = 1
        for p, exponent in zip(args.primes, exponents):
            multiple *= p**exponent
        result = search_near_multiple_via_smallest_box(
            multiple, args.max_box_size
        )
        if not result.complete:
            incomplete += 1
            continue

        complete += 1
        candidates_tested += result.candidate_multipliers_tested
        record = (
            multiple,
            exponents,
            result.pivot_prime,
            result.box_size,
            result.candidate_multipliers_tested,
        )
        if largest_complete is None or multiple > largest_complete[0]:
            largest_complete = record
        if (
            most_candidates is None
            or result.candidate_multipliers_tested > most_candidates[4]
        ):
            most_candidates = record
        if result.witness_multipliers:
            witness_cases.append(
                (multiple, exponents, result.witness_multipliers[:10])
            )

    print(f"prime kernel={tuple(args.primes)}, defect={reciprocal_defect(radical)}")
    print(f"complete cases={complete}, incomplete cases={incomplete}")
    print(f"compatible candidate multipliers tested={candidates_tested}")
    print(f"witness cases={witness_cases}")
    print(f"largest complete case={largest_complete}")
    print(f"case with most compatible candidates={most_candidates}")


if __name__ == "__main__":
    main()
