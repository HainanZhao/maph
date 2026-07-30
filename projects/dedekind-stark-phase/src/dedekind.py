"""Exact classical Dedekind sums and one fixed Rademacher convention."""

from __future__ import annotations

from fractions import Fraction
from math import gcd


def sawtooth(value: Fraction) -> Fraction:
    """Return ((x)): zero on integers, x-floor(x)-1/2 otherwise."""
    floor = value.numerator // value.denominator
    fractional = value - floor
    if fractional == 0:
        return Fraction(0)
    return fractional - Fraction(1, 2)


def dedekind_sum(h: int, k: int) -> Fraction:
    """Return s(h,k) for k>0 using the exact sawtooth definition."""
    if k <= 0:
        raise ValueError("k must be positive")
    if gcd(h, k) != 1:
        raise ValueError("h and k must be coprime")
    h %= k
    return sum(
        (
            sawtooth(Fraction(r, k))
            * sawtooth(Fraction(h * r, k))
            for r in range(1, k)
        ),
        Fraction(0),
    )


def rademacher_phi(a: int, b: int, c: int, d: int) -> int:
    """Rademacher phi on SL(2,Z).

    Convention:
      c != 0: (a+d)/c - 12 sign(c) s(a,|c|)
      c == 0: b/d

    The result is integral. This fixes a computational convention; a
    later phase theorem must still prove that this is the relevant
    multiplier normalization.
    """
    if a * d - b * c != 1:
        raise ValueError("matrix must lie in SL(2,Z)")
    if c == 0:
        if d not in (-1, 1) or b % d:
            raise ValueError("invalid upper-triangular SL(2,Z) matrix")
        return b // d
    sign = 1 if c > 0 else -1
    value = Fraction(a + d, c) - 12 * sign * dedekind_sum(a, abs(c))
    if value.denominator != 1:
        raise ArithmeticError("Rademacher phi failed integrality")
    return value.numerator
