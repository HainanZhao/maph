#!/usr/bin/env python3
"""Replay universal supplied-tuple arithmetic on frozen SIC anchors."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cocycle import (  # noqa: E402
    kopp_theta_exponent,
    kopp_total_multiplier_exponent,
    sic_rademacher_invariant,
)


ANCHORS = {
    "d4_disc5": (((21, -8), (8, -3)), 0),
    "d5_disc12": (((56, -15), (15, -4)), 3),
    "d7_disc8": (((239, -140), (70, -41)), 0),
    "d7_disc32": (((204, -35), (35, -6)), 9),
    "d8_disc5": (((377, -144), (144, -55)), 0),
}


def inverse(matrix):
    """Inverse of an SL(2,Z) matrix."""
    (a, b), (c, d) = matrix
    return ((d, -b), (-c, a))


def positive_dimension_five_lift(first: int, second: int) -> int:
    """Exact lift for q(2-sqrt(3))-p_tilde > 0."""
    lifted = first
    while True:
        if lifted < 0:
            return lifted
        if second == 0:
            passed = False
        else:
            passed = (
                2 * second - lifted > 0
                and (2 * second - lifted) ** 2 > 3 * second**2
            )
        if passed:
            return lifted
        lifted -= 5


def main() -> None:
    for label, (matrix, expected) in ANCHORS.items():
        actual = sic_rademacher_invariant(matrix)
        if actual != expected:
            raise AssertionError(f"{label}: Psi {actual} != {expected}")
        print(f"{label}|PSI={actual}|PASS=1")

    d4 = ((21, -8), (8, -3))
    theta = kopp_theta_exponent(d4, Fraction(0), Fraction(1, 4))
    total = kopp_total_multiplier_exponent(
        d4, Fraction(0), Fraction(1, 4)
    )
    if theta != Fraction(1, 4) or total != Fraction(3, 4):
        raise AssertionError("dimension-four multiplier mismatch")
    if (
        kopp_total_multiplier_exponent(
            inverse(d4), Fraction(0), Fraction(1, 4)
        )
        != -total % 1
    ):
        raise AssertionError("dimension-four inversion covariance")
    print("d4_disc5|THETA=1/4|TOTAL=3/4|PASS=1")

    d5 = ((56, -15), (15, -4))
    checked = 0
    for first in range(5):
        for second in range(5):
            if first == second == 0:
                continue
            lifted = positive_dimension_five_lift(first, second)
            theta = kopp_theta_exponent(
                d5, Fraction(lifted, 5), Fraction(second, 5)
            )
            expected_theta = Fraction(
                first * first - 4 * first * second + second * second,
                5,
            ) % 1
            if theta != expected_theta:
                raise AssertionError(
                    f"d5 ({first},{second}): {theta} != {expected_theta}"
                )
            expected_total = (-Fraction(1, 4) - expected_theta) % 1
            actual_total = kopp_total_multiplier_exponent(
                d5, Fraction(lifted, 5), Fraction(second, 5)
            )
            if actual_total != expected_total:
                raise AssertionError("dimension-five total mismatch")
            inverse_total = kopp_total_multiplier_exponent(
                inverse(d5),
                Fraction(lifted, 5),
                Fraction(second, 5),
            )
            if inverse_total != -actual_total % 1:
                raise AssertionError(
                    "dimension-five inversion covariance mismatch"
                )
            checked += 1
    print(f"d5_disc12|CHARACTERISTICS={checked}|PASS=1")
    print("CHARACTER_INVERSION_COVARIANCE=PASS")
    print("SUPPLIED_TUPLE_BRIDGE=PASS")


if __name__ == "__main__":
    main()
