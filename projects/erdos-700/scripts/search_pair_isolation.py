#!/usr/bin/env python3
"""Falsify pair isolation in structured reciprocal-supercritical families.

Pair isolation asserts that some two prime-base pass sets have intersection
of size at most one in 1 <= t <= (M-1)/2.
"""

from __future__ import annotations

import argparse
import sys
from itertools import combinations, product
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.erdos700 import (  # noqa: E402
    near_multiple_lucas_residue_box,
    reciprocal_defect,
    search_near_multiple_via_smallest_box,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--primes", type=int, nargs="+", required=True)
    parser.add_argument("--max-exponent", type=int, default=10)
    parser.add_argument("--max-box-size", type=int, default=500_000)
    args = parser.parse_args()

    primes = tuple(sorted(args.primes))
    if len(primes) < 3 or len(set(primes)) != len(primes):
        parser.error("at least three distinct primes are required")
    radical = 1
    for p in primes:
        radical *= p
    if reciprocal_defect(radical) >= 0:
        parser.error("the prime kernel must be reciprocal-supercritical")

    isolated = 0
    unresolved = 0
    fully_resolved = 0
    largest_minimum = -1
    largest_minimum_cases = []
    counterexamples = []

    exponent_range = range(1, args.max_exponent + 1)
    for exponents in product(exponent_range, repeat=len(primes)):
        multiple = 1
        for p, exponent in zip(primes, exponents):
            multiple *= p**exponent

        boxes = {
            p: near_multiple_lucas_residue_box(multiple, p)
            for p in primes
        }
        pairs = sorted(
            combinations(primes, 2),
            key=lambda pair: min(
                boxes[pair[0]].allowed_residue_count,
                boxes[pair[1]].allowed_residue_count,
            ),
        )

        resolved_counts = {}
        has_unresolved_pair = False
        certified_isolated = False
        for pair in pairs:
            result = search_near_multiple_via_smallest_box(
                multiple,
                max_box_size=args.max_box_size,
                required_primes=pair,
            )
            if not result.complete:
                has_unresolved_pair = True
                continue
            count = len(result.witness_multipliers)
            resolved_counts[pair] = count
            if count <= 1:
                certified_isolated = True
                break

        if certified_isolated:
            isolated += 1
            continue
        if has_unresolved_pair:
            unresolved += 1
            continue

        fully_resolved += 1
        minimum = min(resolved_counts.values())
        record = (multiple, exponents, minimum, tuple(resolved_counts.items()))
        if minimum > largest_minimum:
            largest_minimum = minimum
            largest_minimum_cases = [record]
        elif minimum == largest_minimum:
            largest_minimum_cases.append(record)
        if minimum > 1:
            counterexamples.append(record)
            if len(counterexamples) >= 20:
                break

    print(
        f"kernel={primes}, defect={reciprocal_defect(radical)}, "
        f"exponents=1..{args.max_exponent}"
    )
    print(f"certified pair-isolated cases={isolated}")
    print(f"unresolved cases={unresolved}")
    print(f"fully resolved non-isolated candidates={fully_resolved}")
    print(f"largest resolved minimum={largest_minimum}")
    print(f"largest-minimum cases={largest_minimum_cases[:10]}")
    print(f"counterexamples={counterexamples}")


if __name__ == "__main__":
    main()
