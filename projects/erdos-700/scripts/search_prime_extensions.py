#!/usr/bin/env python3
"""Vary one prime extension and maximize surviving triple intersections."""

from __future__ import annotations

import argparse
import sys
from itertools import combinations
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.erdos700 import (  # noqa: E402
    factorize,
    find_near_multiple_witness,
    reciprocal_defect,
    search_near_multiple_via_smallest_box,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=int, default=300)
    parser.add_argument("--prime-limit", type=int, default=2_000)
    parser.add_argument("--max-box-size", type=int, default=500_000)
    parser.add_argument("--max-direct-multiplier", type=int, default=100_000)
    args = parser.parse_args()

    base_primes = set(factorize(args.base))
    considered = 0
    resolved_full = 0
    best_score = -1
    best_cases = []

    for extension in range(2, args.prime_limit + 1):
        if extension in base_primes:
            continue
        if factorize(extension) != {extension: 1}:
            continue
        multiple = args.base * extension
        if reciprocal_defect(multiple) >= 0:
            continue
        considered += 1

        full = search_near_multiple_via_smallest_box(
            multiple, max_box_size=args.max_box_size
        )
        if not full.complete or full.witness_multipliers:
            continue
        resolved_full += 1

        primes = tuple(factorize(multiple))
        witnesses = {}
        empty = []
        unresolved = []
        for triple in combinations(primes, 3):
            result = search_near_multiple_via_smallest_box(
                multiple,
                max_box_size=args.max_box_size,
                required_primes=triple,
            )
            if result.complete:
                if result.witness_multipliers:
                    witnesses[triple] = result.witness_multipliers[0]
                else:
                    empty.append(triple)
                continue
            witness = find_near_multiple_witness(
                multiple,
                required_primes=triple,
                max_multiplier=args.max_direct_multiplier,
            )
            if witness is None:
                unresolved.append(triple)
            else:
                witnesses[triple] = witness

        score = len(witnesses)
        record = (
            extension,
            multiple,
            score,
            len(tuple(combinations(primes, 3))),
            tuple(sorted(witnesses.items())),
            tuple(empty),
            tuple(unresolved),
        )
        if score > best_score:
            best_score = score
            best_cases = [record]
        elif score == best_score:
            best_cases.append(record)

        if not empty and not unresolved:
            print(f"DEGREE-AT-LEAST-FOUR CANDIDATE {record}")
            return

    print(
        f"base={args.base}, prime extensions through {args.prime_limit}, "
        f"considered={considered}, complete empty full={resolved_full}"
    )
    print(f"maximum surviving triples={best_score}")
    print(f"best cases={best_cases[:20]}")


if __name__ == "__main__":
    main()
