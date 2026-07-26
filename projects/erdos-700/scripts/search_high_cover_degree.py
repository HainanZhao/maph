#!/usr/bin/env python3
"""Search prime-power families for high Lucas cover degree.

For M with distinct prime divisors P, let A_p be the multipliers
1 <= t <= (M-1)/2 that pass the shifted Lucas test in base p.  The Lucas
cover degree is the least size of a subset S of P with intersection
of A_p over p in S empty.

This script looks specifically for degree at least four.  It first certifies
that every triple intersection is nonempty, then searches larger subsets for
the first empty intersection.  All claims are made only from complete finite
box searches.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from itertools import combinations, product
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.erdos700 import (  # noqa: E402
    find_near_multiple_witness,
    reciprocal_defect,
    search_near_multiple_via_smallest_box,
)


def first_witnesses_for_subsets(
    multiple: int,
    primes: tuple[int, ...],
    subset_size: int,
    max_box_size: int,
    max_direct_multiplier: int,
) -> tuple[
    dict[tuple[int, ...], int],
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, ...], ...],
]:
    """Return nonempty, empty, and unresolved selected-base intersections."""
    nonempty: dict[tuple[int, ...], int] = {}
    empty = []
    unresolved = []
    for subset in combinations(primes, subset_size):
        result = search_near_multiple_via_smallest_box(
            multiple,
            max_box_size=max_box_size,
            required_primes=subset,
        )
        if not result.complete:
            witness = find_near_multiple_witness(
                multiple,
                required_primes=subset,
                max_multiplier=max_direct_multiplier,
            )
            if witness is None:
                unresolved.append(subset)
            else:
                nonempty[subset] = witness
        elif result.witness_multipliers:
            nonempty[subset] = result.witness_multipliers[0]
        else:
            empty.append(subset)
    return nonempty, tuple(empty), tuple(unresolved)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--primes", type=int, nargs="+", required=True)
    parser.add_argument("--max-exponent", type=int, default=6)
    parser.add_argument("--max-box-size", type=int, default=500_000)
    parser.add_argument("--max-direct-multiplier", type=int, default=100_000)
    parser.add_argument("--max-results", type=int, default=20)
    args = parser.parse_args()

    primes = tuple(sorted(args.primes))
    if len(primes) < 4:
        parser.error("at least four distinct primes are required")
    if len(set(primes)) != len(primes):
        parser.error("primes must be distinct")

    radical = 1
    for p in primes:
        radical *= p

    full_empty_complete = 0
    triples_complete = 0
    triples_unresolved = 0
    triple_failure = 0
    triple_certificate_histogram: Counter[tuple[int, ...]] = Counter()
    best_triple_survivals = -1
    closest_cases = []
    high_degree = []

    exponent_range = range(1, args.max_exponent + 1)
    for exponents in product(exponent_range, repeat=len(primes)):
        multiple = 1
        for p, exponent in zip(primes, exponents):
            multiple *= p**exponent

        full = search_near_multiple_via_smallest_box(
            multiple,
            max_box_size=args.max_box_size,
        )
        if not full.complete or full.witness_multipliers:
            continue
        full_empty_complete += 1

        triple_witnesses, triple_empty, unresolved = (
            first_witnesses_for_subsets(
                multiple,
                primes,
                3,
                args.max_box_size,
                args.max_direct_multiplier,
            )
        )
        if unresolved:
            triples_unresolved += 1
        survival_count = len(triple_witnesses)
        closest_record = (
            multiple,
            exponents,
            survival_count,
            tuple(sorted(triple_witnesses.items())),
            triple_empty,
            unresolved,
        )
        if survival_count > best_triple_survivals:
            best_triple_survivals = survival_count
            closest_cases = [closest_record]
        elif survival_count == best_triple_survivals:
            closest_cases.append(closest_record)

        if triple_empty:
            triple_failure += 1
            triple_certificate_histogram[triple_empty[0]] += 1
            continue
        if unresolved:
            continue
        triples_complete += 1

        degree = None
        certificate = None
        unresolved_at = None
        for subset_size in range(4, len(primes) + 1):
            _, empty, unresolved = first_witnesses_for_subsets(
                multiple,
                primes,
                subset_size,
                args.max_box_size,
                args.max_direct_multiplier,
            )
            if empty:
                degree = subset_size
                certificate = empty[0]
                break
            if unresolved:
                unresolved_at = subset_size
                break

        if degree is not None:
            high_degree.append(
                (
                    multiple,
                    exponents,
                    degree,
                    certificate,
                    tuple(sorted(triple_witnesses.items())),
                )
            )
            if len(high_degree) >= args.max_results:
                break
        elif unresolved_at is not None:
            triples_unresolved += 1

    print(
        f"prime kernel={primes}, defect={reciprocal_defect(radical)}, "
        f"exponents=1..{args.max_exponent}"
    )
    print(f"complete empty full intersections={full_empty_complete}")
    print(f"cases killed by a triple={triple_failure}")
    print(
        "first empty-triple histogram="
        f"{dict(sorted(triple_certificate_histogram.items()))}"
    )
    print(f"cases with unresolved required subset={triples_unresolved}")
    print(f"cases with every triple certified nonempty={triples_complete}")
    print(f"maximum witnessed triple intersections={best_triple_survivals}")
    print(f"closest cases={closest_cases[:10]}")
    print(f"degree >= 4 results={high_degree}")


if __name__ == "__main__":
    main()
