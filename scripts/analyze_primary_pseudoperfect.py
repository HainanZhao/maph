#!/usr/bin/env python3
"""Analyze Lucas failure depths for a primary pseudoperfect number."""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.erdos700 import factorize, lucas_first_failure  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("multiple", type=int)
    parser.add_argument(
        "--factors",
        type=int,
        nargs="+",
        help="explicit distinct prime factors, useful when trial division is slow",
    )
    args = parser.parse_args()

    m = args.multiple
    primes = tuple(args.factors) if args.factors else tuple(factorize(m))
    product = 1
    for p in primes:
        product *= p
    if product != m or len(set(primes)) != len(primes):
        parser.error("the supplied factors must be distinct and have product M")
    if 1 + sum(m // p for p in primes) != m:
        parser.error("M does not satisfy the primary-pseudoperfect identity")

    candidates = {0}
    for p in primes:
        summand = m // p
        candidates |= {value + summand for value in tuple(candidates)}
    candidates = {
        value for value in candidates if 1 <= value <= (m - 1) // 2
    }

    n = m * (m - 1)
    failure_histogram: Counter[int] = Counter()
    deepest: list[tuple[int, int, tuple[int, ...]]] = []
    full_survivors: list[int] = []

    for t in candidates:
        positions = {
            p: lucas_first_failure(n, m * t, p)
            for p in primes
        }
        finite_positions = tuple(
            position for position in positions.values() if position is not None
        )
        if not finite_positions:
            full_survivors.append(t)
            continue
        first_position = min(finite_positions)
        failure_histogram[first_position] += 1
        killers = tuple(
            p for p, position in positions.items() if position == first_position
        )
        deepest.append((first_position, t, killers))

    print(f"M={m}")
    print(f"prime factors={primes}")
    print(f"subset-sum candidates={len(candidates)}")
    print(f"first-failure-position histogram={dict(sorted(failure_histogram.items()))}")
    print(f"full survivors={sorted(full_survivors)}")
    print("deepest candidates:")
    for position, t, killers in sorted(deepest, reverse=True)[:10]:
        print(
            f"  t={t}, original digit={position}, "
            f"shifted digit ordinal={position}, killers={killers}"
        )


if __name__ == "__main__":
    main()
