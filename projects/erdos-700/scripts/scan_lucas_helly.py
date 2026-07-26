#!/usr/bin/env python3
"""Measure how many prime bases are needed to certify no common witness."""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.erdos700 import (  # noqa: E402
    factorize,
    lucas_nonzero,
    reciprocal_defect,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=10_000)
    args = parser.parse_args()

    histogram: Counter[int] = Counter()
    record_degree = 0
    record_examples = []

    for multiple in range(4, args.limit + 1):
        if reciprocal_defect(multiple) >= 0:
            continue
        primes = tuple(factorize(multiple))
        n = multiple * (multiple - 1)
        pass_masks = []
        for t in range(1, (multiple - 1) // 2 + 1):
            mask = 0
            for index, p in enumerate(primes):
                if lucas_nonzero(n, multiple * t, p):
                    mask |= 1 << index
            pass_masks.append(mask)

        full_mask = (1 << len(primes)) - 1
        if any(mask == full_mask for mask in pass_masks):
            print(f"RECIPROCAL-THRESHOLD WITNESS M={multiple}")
            return

        degree = None
        certificate = None
        for size in range(1, len(primes) + 1):
            for indices in combinations(range(len(primes)), size):
                subset = sum(1 << index for index in indices)
                if not any(mask & subset == subset for mask in pass_masks):
                    degree = size
                    certificate = tuple(primes[index] for index in indices)
                    break
            if degree is not None:
                break

        assert degree is not None and certificate is not None
        histogram[degree] += 1
        if degree > record_degree:
            record_degree = degree
            record_examples = [(multiple, primes, certificate)]
        elif degree == record_degree:
            record_examples.append((multiple, primes, certificate))

    print(f"supercritical cover-degree histogram={dict(sorted(histogram.items()))}")
    print(f"maximum degree={record_degree}")
    print(f"record examples={record_examples[:20]}")


if __name__ == "__main__":
    main()
