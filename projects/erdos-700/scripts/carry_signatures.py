#!/usr/bin/env python3
"""Summarize the first Lucas failure covering each multiplier."""

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
    args = parser.parse_args()
    m = args.multiple
    if m < 4:
        parser.error("multiple must be at least 4")

    n = m * (m - 1)
    primes = tuple(factorize(m))
    signatures: Counter[tuple[tuple[int, int], ...]] = Counter()
    uncovered = []

    for t in range(1, (m - 1) // 2 + 1):
        k = m * t
        failures = tuple(
            (p, position)
            for p in primes
            if (position := lucas_first_failure(n, k, p)) is not None
        )
        signatures[failures] += 1
        if not failures:
            uncovered.append(t)

    print(f"M={m}, factors={factorize(m)}, multipliers checked={(m - 1) // 2}")
    print(f"Uncovered multipliers: {uncovered[:30]}")
    print("Most common first-failure signatures:")
    for signature, count in signatures.most_common(20):
        print(f"  {count:>8}  {signature}")


if __name__ == "__main__":
    main()
