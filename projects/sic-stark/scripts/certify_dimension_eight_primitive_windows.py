#!/usr/bin/env python3
"""Arb windows for the eight independent primitive d=8 squared overlaps.

These enclosures rigorously match the analytic values to the isolated
candidate roots.  They deliberately do not claim height rigidity: the
primitive ray field has Shintani index four, so a powered-algebraicity
theorem is still required before closeness can imply equality.
"""

from __future__ import annotations

import argparse
from fractions import Fraction

from flint import arb, ctx, fmpz_poly

from certify_dimension_eight_lower_conductor import overlap_log
from certify_dimension_five_double_sine import _arb_fraction


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--digits", type=int, default=35)
    parser.add_argument("--tolerance", default="1e-8")
    arguments = parser.parse_args()
    tolerance = Fraction(arguments.tolerance)
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")

    ctx.dps = arguments.digits
    ctx.cap = 6
    beta = (7 + 3 * arb(5).sqrt()) / 2
    # Absolute polynomial of the primitive squared-overlap ray field,
    # coefficients in ascending order.
    polynomial = fmpz_poly(
        [
            1,
            -120,
            5712,
            -142424,
            2026392,
            -16477496,
            69873072,
            -102354552,
            -147141404,
            218292184,
            502952016,
            -8584488,
            -708115064,
            -592829448,
            55289008,
            470768344,
            512914950,
            470768344,
            55289008,
            -592829448,
            -708115064,
            -8584488,
            502952016,
            218292184,
            -147141404,
            -102354552,
            69873072,
            -16477496,
            2026392,
            -142424,
            5712,
            -120,
            1,
        ]
    )
    roots = polynomial.complex_roots()
    real_roots = [
        root.real
        for root, multiplicity in roots
        if multiplicity == 1 and root.imag.contains(0)
    ]
    if len(real_roots) != 16:
        raise RuntimeError("primitive polynomial needs sixteen real roots")

    windows = {
        (0, 1): (Fraction(6910937, 10**6), Fraction(6910938, 10**6)),
        (0, 3): (Fraction(2061122, 10**6), Fraction(2061123, 10**6)),
        (2, 7): (Fraction(7992821, 10**6), Fraction(7992822, 10**6)),
        (3, 6): (
            Fraction(16483891, 10**6),
            Fraction(16483892, 10**6),
        ),
        (3, 7): (
            Fraction(11105600, 10**6),
            Fraction(11105601, 10**6),
        ),
        (4, 5): (
            Fraction(18237810, 10**6),
            Fraction(18237811, 10**6),
        ),
        (4, 7): (
            Fraction(15206346, 10**6),
            Fraction(15206347, 10**6),
        ),
        (5, 5): (
            Fraction(43562131, 10**6),
            Fraction(43562132, 10**6),
        ),
    }
    maximum_log_difference = arb(0)
    for characteristic, (left, right) in windows.items():
        logarithm, panels = overlap_log(
            *characteristic, beta, tolerance
        )
        candidates = [
            root
            for root in real_roots
            if root > _arb_fraction(left) and root < _arb_fraction(right)
        ]
        if len(candidates) != 1:
            raise RuntimeError(
                f"window {characteristic} has {len(candidates)} roots"
            )
        candidate = candidates[0]
        difference = 2 * logarithm - candidate.log()
        if abs(difference).upper() > maximum_log_difference.upper():
            maximum_log_difference = abs(difference)
        print(
            f"LOG_SQUARED_OVERLAP_{characteristic[0]}_"
            f"{characteristic[1]}={2 * logarithm} PANELS={panels}"
        )
        print(
            f"CANDIDATE_ROOT_{characteristic[0]}_{characteristic[1]}="
            f"{candidate}"
        )
        print(
            f"LOG_DIFFERENCE_{characteristic[0]}_{characteristic[1]}="
            f"{difference} CONTAINS_ZERO={difference.contains(0)}"
        )
        if not difference.contains(0):
            raise RuntimeError("analytic and candidate balls are disjoint")

    print(f"MAXIMUM_LOG_DIFFERENCE={maximum_log_difference}")
    print("PRIMITIVE_ANALYTIC_WINDOWS_CERTIFIED=1")
    print("PRIMITIVE_POWERED_ALGEBRAICITY_STILL_REQUIRED=1")


if __name__ == "__main__":
    main()
