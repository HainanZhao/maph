#!/usr/bin/env python3
"""Exact finite probe for Cycle 167 affine-fibre transport.

Discovery-only: it verifies the arithmetic interface and explicit obstruction
models; it does not assert a Cycle-166 population bound or an E7/E9 handoff.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from math import comb, gcd


def primitive_parent_count(parameters: tuple[int, ...]) -> int:
    """Count four-subsets after their own least-parameter/gcd normalization."""
    total = 0
    for rows in combinations(sorted(set(parameters)), 4):
        least = rows[0]
        shifts = tuple(value - least for value in rows[1:])
        content = 0
        for value in shifts:
            content = gcd(content, value)
        total += content == 1
    return total


def distinct_parameter_lower_bound(parent_count: int) -> int:
    """Least m compatible with P<=binom(m,4)."""
    if parent_count < 0:
        raise ValueError("negative parent count")
    m = 0
    while comb(m, 4) < parent_count:
        m += 1
    return m


def divisibility_residue(h0: int, r: int, a: int) -> tuple[int, int] | None:
    """Return n=residue mod modulus for a|(h0+r*n), or None if insoluble."""
    if a <= 0:
        raise ValueError("nonpositive numerator")
    divisor = gcd(a, r)
    if h0 % divisor:
        return None
    modulus = a // divisor
    if modulus == 1:
        return 0, 1
    coefficient = (r // divisor) % modulus
    residue = (-h0 // divisor * pow(coefficient, -1, modulus)) % modulus
    return residue, modulus


def eligible_parameters(
    parameters: tuple[int, ...], *, h0: int, r: int, a: int, q: int, h_scale: int
) -> tuple[int, ...]:
    """Exact congruence plus source/target Cycle-67 range intersection."""
    if q <= 0 or h_scale <= 0:
        raise ValueError("invalid range")
    residue = divisibility_residue(h0, r, a)
    if residue is None:
        return ()
    residue_value, modulus = residue
    result = []
    for n in sorted(set(parameters)):
        h = h0 + r * n
        hp = Fraction(q * h, a)
        if n % modulus == residue_value and h_scale <= h <= 2 * h_scale and h_scale <= hp <= 2 * h_scale:
            result.append(n)
    return tuple(result)


def balance(h_scale: int, a: int, depth: int) -> Fraction:
    """The dimensionless transported-error loss H/(aK)."""
    if h_scale <= 0 or a <= 0 or depth <= 0:
        raise ValueError("invalid balance")
    return Fraction(h_scale, a * depth)


def transported_residual(
    *, h: int, j: int, beta: Fraction, y: Fraction, q: int, a: int, shift_error: Fraction
) -> tuple[Fraction, Fraction]:
    """Return source and transported residual under qE=a+shift_error."""
    if (q * h) % a:
        raise ValueError("ineligible h")
    hp = q * h // a
    jp = j + h - hp
    yp = Fraction(a + shift_error, q) * y
    source = j + beta - h * (y - 1)
    target = jp + beta - hp * (yp - 1)
    if target != source - Fraction(h, a) * y * shift_error:
        raise RuntimeError("transport identity")
    return source, target


def exact_examples() -> dict[str, object]:
    parameters = (0, 1, 2, 3, 4)
    parents = primitive_parent_count(parameters)
    if parents > comb(len(parameters), 4):
        raise RuntimeError("deconvolution inequality")
    if distinct_parameter_lower_bound(parents) > len(parameters):
        raise RuntimeError("deconvolution lower bound")
    # All source/target rows are in [20,40], but the only divisible residue is n=4.
    residue_avoid = eligible_parameters((0, 1, 2, 3), h0=26, r=1, a=5, q=4, h_scale=20)
    if residue_avoid:
        raise RuntimeError("residue obstruction model")
    # Every row is divisible by 3, yet its transported row lies below [21,42].
    range_avoid = eligible_parameters((0, 1, 2, 3), h0=21, r=3, a=3, q=2, h_scale=21)
    if range_avoid:
        raise RuntimeError("range obstruction model")
    source, target = transported_residual(
        h=10, j=5, beta=Fraction(0), y=Fraction(3, 2), q=3, a=5, shift_error=Fraction(0)
    )
    if source != 0 or target != 0:
        raise RuntimeError("exact beta transport")
    return {
        "primitive_parent_count": parents,
        "distinct_parameter_lower_bound": distinct_parameter_lower_bound(parents),
        "residue_obstruction": {"eligible_parameters": list(residue_avoid)},
        "range_obstruction": {"eligible_parameters": list(range_avoid)},
        "exact_beta_transport": True,
        "balance_example": str(balance(100, 1, 1)),
    }


if __name__ == "__main__":
    print(exact_examples())
