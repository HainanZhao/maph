#!/usr/bin/env python3
"""Test elementary Eisenstein/Newton-polygon routes for Conjecture T3e.

For a monic polynomial f of degree n, the single-edge Dumas criterion
applies at p when its p-adic Newton polygon is the primitive segment from
(0, v_p(f(0))) to (n, 0).  This script searches for that sufficient
criterion, including ordinary Eisenstein as a special case.

The unshifted search is exhaustive in p: the constant term is (2a)! for
even a and (2a-1)! for the odd residual, so only p <= 2a can contribute.
The optional shifted search is explicitly bounded in both shift and prime;
it is a diagnostic, not an exhaustive exclusion of shifted criteria.
"""

from __future__ import annotations

import argparse
from math import comb, gcd

from audit_reflection_irreducibility import (
    conjecturally_irreducible_part,
    reflection_integer_coefficients,
)
from search_reflection_irreducibility_certificates import primes_through


def valuation(value: int, prime: int) -> int | None:
    """Return v_p(value), with None standing for v_p(0) = infinity."""
    if value == 0:
        return None
    result = 0
    while value % prime == 0:
        value //= prime
        result += 1
    return result


def has_primitive_single_edge(coefficients: list[int], prime: int) -> bool:
    """Test the elementary one-segment Dumas irreducibility criterion."""
    degree = len(coefficients) - 1
    constant_valuation = valuation(coefficients[0], prime)
    if constant_valuation in (None, 0):
        return False
    if gcd(degree, constant_valuation) != 1:
        return False

    # Avoid fractions: v_i >= v_0 (n-i)/n.
    for index, coefficient in enumerate(coefficients[:-1]):
        coefficient_valuation = valuation(coefficient, prime)
        if coefficient_valuation is not None and (
            degree * coefficient_valuation
            < constant_valuation * (degree - index)
        ):
            return False
    return True


def shift_polynomial(coefficients: list[int], shift: int) -> list[int]:
    """Return ascending coefficients of f(b + shift)."""
    result = [0] * len(coefficients)
    for degree, coefficient in enumerate(coefficients):
        for new_degree in range(degree + 1):
            result[new_degree] += (
                coefficient
                * comb(degree, new_degree)
                * shift ** (degree - new_degree)
            )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-a", type=int, default=60)
    parser.add_argument(
        "--shift-max-a",
        type=int,
        default=25,
        help="search integer shifts only through this a (zero disables)",
    )
    parser.add_argument(
        "--shift-radius-factor",
        type=int,
        default=2,
        help="for shifted rows search |shift| <= factor*a",
    )
    parser.add_argument(
        "--shift-prime-factor",
        type=int,
        default=4,
        help="for shifted rows search primes <= factor*a + 10",
    )
    args = parser.parse_args()

    direct_hits: list[tuple[int, int]] = []
    shifted_hits: list[tuple[int, int, int]] = []
    for a in range(2, args.max_a + 1):
        residual = conjecturally_irreducible_part(
            a,
            reflection_integer_coefficients(a),
        )
        for prime in primes_through(2 * a):
            if has_primitive_single_edge(residual, prime):
                direct_hits.append((a, prime))

        if a <= args.shift_max_a:
            radius = args.shift_radius_factor * a
            prime_limit = args.shift_prime_factor * a + 10
            primes = primes_through(prime_limit)
            for shift in range(-radius, radius + 1):
                shifted = shift_polynomial(residual, shift)
                for prime in primes:
                    if has_primitive_single_edge(shifted, prime):
                        shifted_hits.append((a, shift, prime))

    print(f"unshifted primitive-single-edge hits: {direct_hits}")
    print(
        "shifted bounded hits "
        f"(a<={args.shift_max_a}, "
        f"|shift|<={args.shift_radius_factor}a, "
        f"p<={args.shift_prime_factor}a+10): {shifted_hits}"
    )


if __name__ == "__main__":
    main()
