#!/usr/bin/env python3
"""Certify a finite range of the F_4 reflection-family conjecture.

The recurrence is evaluated modulo two primes larger than every scanned
``b``.  A nonzero residue is an exact certificate that the integer
coefficient is nonzero.  Rare double-zero residues are resolved by the
exact binomial formula.  The rigorous positive-tail theorem reduces the
otherwise infinite ``b`` range to a finite interval for each ``a``.
"""

from __future__ import annotations

import argparse
import sys
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.fourier_suppression import (  # noqa: E402
    four_mode_reflection_closed_sum,
    reflection_positive_tail_start,
)


PRIMES = (1_000_000_007, 1_000_000_009)


def modular_inverses(limit: int, prime: int) -> list[int]:
    """Return inverses of 1, ..., limit modulo ``prime``."""
    inverses = [0] * (limit + 1)
    if limit:
        inverses[1] = 1
    for value in range(2, limit + 1):
        inverses[value] = (
            prime
            - (prime // value) * inverses[prime % value] % prime
        )
    return inverses


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--a-limit", type=int, default=1000)
    parser.add_argument("--progress-every", type=int, default=100)
    args = parser.parse_args()
    if args.a_limit < 1:
        parser.error("--a-limit must be positive")
    if args.progress_every < 0:
        parser.error("--progress-every must be nonnegative")

    b_limit = reflection_positive_tail_start(args.a_limit)
    if b_limit >= min(PRIMES):
        parser.error("the modular primes must exceed the recurrence range")

    inverse_tables = [
        modular_inverses(b_limit, prime) for prime in PRIMES
    ]
    previous_rows = [[1] * (b_limit + 1) for _ in PRIMES]
    double_residue_candidates = 0

    for a in range(1, args.a_limit + 1):
        central = comb(2 * a, a)
        rows: list[list[int]] = []
        for prime_index, prime in enumerate(PRIMES):
            row = [0] * (b_limit + 1)
            row[0] = row[1] = (
                (-central if a % 2 else central) % prime
            )
            inverses = inverse_tables[prime_index]
            previous = previous_rows[prime_index]
            for b in range(2, b_limit + 1):
                numerator = (
                    (2 * b - 1) * row[b - 1]
                    - (b - 1) * row[b - 2]
                    + 4 * (b - 1) * previous[b - 2]
                )
                row[b] = numerator * inverses[b] % prime
            rows.append(row)

        finite_limit = reflection_positive_tail_start(a)
        for b in range(1, finite_limit):
            expected_zero = a % 2 == 1 and b == 2 * a
            residues_zero = all(row[b] == 0 for row in rows)
            if expected_zero:
                if not residues_zero:
                    raise AssertionError(
                        f"proved zero failed recurrence at a={a}, b={b}"
                    )
                continue
            if not residues_zero:
                continue

            double_residue_candidates += 1
            if four_mode_reflection_closed_sum(a, b) == 0:
                raise AssertionError(
                    f"off-line exact zero at a={a}, b={b}"
                )

        previous_rows = rows
        if args.progress_every and a % args.progress_every == 0:
            print(f"certified through a={a}")

    print(
        "Conjecture T3 certified for "
        f"1 <= a <= {args.a_limit} and every positive b."
    )
    print(
        "Above each finite recurrence range, positivity follows from "
        "the alternating-term growth theorem."
    )
    print(
        "Double-zero modular candidates requiring exact resolution: "
        f"{double_residue_candidates}"
    )


if __name__ == "__main__":
    main()
