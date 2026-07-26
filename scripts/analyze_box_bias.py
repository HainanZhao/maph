#!/usr/bin/env python3
"""Compare Lucas-box entropy, divisibility bias, and cross-base sieving."""

from __future__ import annotations

import argparse
import sys
from fractions import Fraction
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.erdos700 import (  # noqa: E402
    factorize,
    reciprocal_defect,
    search_near_multiple_via_smallest_box,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("multiple", type=int)
    parser.add_argument("--max-box-size", type=int, default=1_000_000)
    args = parser.parse_args()

    result = search_near_multiple_via_smallest_box(
        args.multiple, args.max_box_size
    )
    print(f"M={args.multiple}, factors={factorize(args.multiple)}")
    print(f"reciprocal defect={reciprocal_defect(args.multiple)}")
    if not result.complete:
        print(
            f"incomplete: smallest box at p={result.pivot_prime} "
            f"has size {result.box_size}"
        )
        return

    exponent = factorize(args.multiple)[result.pivot_prime]
    complement = args.multiple // (result.pivot_prime**exponent)
    entropy_main = Fraction(result.box_size, complement)
    bias = Fraction(result.compatible_box_values) - entropy_main
    print(
        f"pivot p={result.pivot_prime}, box size={result.box_size}, "
        f"complement={complement}"
    )
    print(
        f"entropy main term={entropy_main} ({float(entropy_main):.12g}), "
        f"actual compatible values={result.compatible_box_values}, "
        f"bias={bias} ({float(bias):.12g})"
    )
    print(f"half-interval sieve profile={result.sieve_profile}")
    print(f"witness multipliers={result.witness_multipliers}")


if __name__ == "__main__":
    main()
