"""Exact supplied-tuple arithmetic for the SIC/Kopp multiplier bridge."""

from __future__ import annotations

from fractions import Fraction

from dedekind import rademacher_phi


Matrix2 = tuple[tuple[int, int], tuple[int, int]]


def mod_one(value: Fraction) -> Fraction:
    """Return the representative of value modulo Z in [0,1)."""
    return value - value.numerator // value.denominator


def sic_rademacher_invariant(matrix: Matrix2) -> int:
    """Return the Psi convention used in the SIC bridge papers."""
    (a, b), (c, d) = matrix
    phi = rademacher_phi(a, b, c, d)
    if c == 0:
        return phi
    product = c * (a + d)
    if product == 0:
        raise ValueError("SIC Psi convention requires nonzero c(a+d)")
    return phi - (3 if product > 0 else -3)


def kopp_theta_exponent(
    matrix: Matrix2, first: Fraction, second: Fraction
) -> Fraction:
    """Return the theta-character exponent modulo one."""
    (a, b), (c, d) = matrix
    if a * d - b * c != 1:
        raise ValueError("matrix must lie in SL(2,Z)")
    value = Fraction(1, 2) * (
        (c - d + 1) * first
        + (-a + b + 1) * second
        - c * d * first * first
        + 2 * (a - 1) * d * first * second
        - (a - 2) * b * second * second
    )
    return mod_one(value)


def kopp_total_multiplier_exponent(
    matrix: Matrix2, first: Fraction, second: Fraction
) -> Fraction:
    """Return the exponent of psi^-2 chi_r^-1 modulo one."""
    psi = sic_rademacher_invariant(matrix)
    theta = kopp_theta_exponent(matrix, first, second)
    return mod_one(-Fraction(psi, 12) - theta)
