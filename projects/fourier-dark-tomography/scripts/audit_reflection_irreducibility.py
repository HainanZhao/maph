#!/usr/bin/env python3
"""Audit the irreducibility pattern of the F_4 reflection polynomials.

For

    C_{a,b} = sum_j (-1)^(a+j) binom(2(a-j), a-j)
                    b^(under 2j) / (j!)^2,

clear denominators by setting ``Q_a(b) = (a!)^2 C_{a,b}``.  The resulting
polynomial is monic, integral, and has degree ``2a``.  The observed exact
factorization is

* ``Q_a`` irreducible over Q when ``a`` is even;
* ``Q_a = (b + 1)(b - 2a) R_a`` with ``R_a`` irreducible over Q when
  ``a`` is odd.

By default this script uses only the Python standard library to verify a
finite-field certificate for every 2 <= a <= 59.  Each relevant monic
integer polynomial is irreducible modulo an explicitly recorded prime,
which proves its irreducibility over Q by Gauss's lemma.  The finite-field
test is Rabin's exact criterion, implemented below with elementary modular
polynomial arithmetic.

Passing ``--exact-factor`` additionally repeats the original factorization
audit over Z with SymPy's ``Poly.factor_list``.  That optional mode requires
SymPy; the default certificate audit does not.  SymPy 1.14.0 produced the
initial factorization audit and certificate list.

The recorded range is rigorous finite evidence, not a proof of the pattern
for arbitrary ``a``.
"""

from __future__ import annotations

import argparse
from math import comb, factorial
from typing import Any


# Each entry certifies irreducibility modulo p of Q_a (a even), or of
# Q_a / ((b + 1)(b - 2a)) (a odd).  The primes were found by an
# increasing-prime search and are verified from scratch below.
MOD_P_CERTIFICATES = {
    2: 7,
    3: 7,
    4: 11,
    5: 17,
    6: 17,
    7: 17,
    8: 59,
    9: 131,
    10: 479,
    11: 353,
    12: 271,
    13: 179,
    14: 191,
    15: 61,
    16: 139,
    17: 37,
    18: 37,
    19: 97,
    20: 439,
    21: 61,
    22: 383,
    23: 149,
    24: 269,
    25: 379,
    26: 89,
    27: 61,
    28: 157,
    29: 127,
    30: 1091,
    31: 137,
    32: 137,
    33: 269,
    34: 439,
    35: 1429,
    36: 227,
    37: 3061,
    38: 317,
    39: 167,
    40: 487,
    41: 359,
    42: 2539,
    43: 431,
    44: 647,
    45: 593,
    46: 163,
    47: 127,
    48: 139,
    49: 1559,
    50: 929,
    51: 397,
    52: 491,
    53: 1493,
    54: 911,
    55: 241,
    56: 353,
    57: 433,
    58: 1013,
    59: 1009,
}


def reflection_integer_coefficients(a: int) -> list[int]:
    """Return ascending integer coefficients of the monic polynomial Q_a."""
    if a < 1:
        raise ValueError("a must be positive")

    coefficients = [0] * (2 * a + 1)
    falling = [1]
    a_factorial = factorial(a)

    # At iteration n, ``falling`` stores ascending coefficients of
    # b^(under n).  Only even n = 2j occur in Q_a.
    for n in range(2 * a + 1):
        if n % 2 == 0:
            j = n // 2
            scalar = (
                (-1) ** (a + j)
                * (a_factorial // factorial(j)) ** 2
                * comb(2 * (a - j), a - j)
            )
            for degree, coefficient in enumerate(falling):
                coefficients[degree] += scalar * coefficient

        if n < 2 * a:
            next_falling = [0] * (len(falling) + 1)
            for degree, coefficient in enumerate(falling):
                next_falling[degree] -= n * coefficient
                next_falling[degree + 1] += coefficient
            falling = next_falling

    assert coefficients[-1] == 1
    assert coefficients[0] == (-1) ** a * factorial(2 * a)
    return coefficients


def divide_by_monic(
    coefficients: list[int],
    divisor: list[int],
) -> tuple[list[int], list[int]]:
    """Divide ascending integer coefficient lists by a monic divisor."""
    if not divisor or divisor[-1] != 1:
        raise ValueError("divisor must be monic")
    if len(coefficients) < len(divisor):
        return [0], coefficients[:]

    remainder = coefficients[:]
    quotient = [0] * (len(coefficients) - len(divisor) + 1)
    divisor_degree = len(divisor) - 1
    for degree in range(len(coefficients) - 1, divisor_degree - 1, -1):
        scalar = remainder[degree]
        shift = degree - divisor_degree
        quotient[shift] = scalar
        for index, coefficient in enumerate(divisor):
            remainder[shift + index] -= scalar * coefficient
    return trim(quotient), trim(remainder)


def conjecturally_irreducible_part(
    a: int,
    coefficients: list[int],
) -> list[int]:
    """Remove the two proved linear factors that occur for odd a."""
    if a % 2 == 0:
        return coefficients

    # (b + 1)(b - 2a) = b^2 + (1 - 2a)b - 2a.
    quotient, remainder = divide_by_monic(
        coefficients,
        [-2 * a, 1 - 2 * a, 1],
    )
    if remainder != [0]:
        raise AssertionError(f"expected linear factors failed at a={a}")
    return quotient


def trim(polynomial: list[int]) -> list[int]:
    """Remove high zero coefficients, retaining one zero if necessary."""
    result = polynomial[:]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def multiply_mod(
    left: list[int],
    right: list[int],
    modulus_polynomial: list[int],
    prime: int,
) -> list[int]:
    """Multiply in F_p[b] modulo a monic modulus polynomial."""
    degree = len(modulus_polynomial) - 1
    product = [0] * (len(left) + len(right) - 1)
    for left_degree, left_coefficient in enumerate(left):
        if left_coefficient == 0:
            continue
        for right_degree, right_coefficient in enumerate(right):
            if right_coefficient:
                index = left_degree + right_degree
                product[index] = (
                    product[index]
                    + left_coefficient * right_coefficient
                ) % prime

    for high_degree in range(len(product) - 1, degree - 1, -1):
        scalar = product[high_degree] % prime
        if scalar:
            shift = high_degree - degree
            for index in range(degree):
                product[shift + index] = (
                    product[shift + index]
                    - scalar * modulus_polynomial[index]
                ) % prime
    return trim(product[:degree])


def power_mod(
    base: list[int],
    exponent: int,
    modulus_polynomial: list[int],
    prime: int,
) -> list[int]:
    """Exponentiate in F_p[b] modulo a monic modulus polynomial."""
    result = [1]
    power = base
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = multiply_mod(
                result,
                power,
                modulus_polynomial,
                prime,
            )
        remaining >>= 1
        if remaining:
            power = multiply_mod(
                power,
                power,
                modulus_polynomial,
                prime,
            )
    return result


def remainder_mod(
    dividend: list[int],
    divisor: list[int],
    prime: int,
) -> list[int]:
    """Return the remainder of polynomial division over F_p."""
    remainder = trim([coefficient % prime for coefficient in dividend])
    divisor = trim([coefficient % prime for coefficient in divisor])
    divisor_degree = len(divisor) - 1
    inverse_leading = pow(divisor[-1], -1, prime)

    while len(remainder) - 1 >= divisor_degree and remainder != [0]:
        shift = len(remainder) - len(divisor)
        scalar = remainder[-1] * inverse_leading % prime
        for index, coefficient in enumerate(divisor):
            remainder[shift + index] = (
                remainder[shift + index] - scalar * coefficient
            ) % prime
        remainder = trim(remainder)
    return remainder


def gcd_mod(
    left: list[int],
    right: list[int],
    prime: int,
) -> list[int]:
    """Return the monic polynomial gcd over F_p."""
    left = trim([coefficient % prime for coefficient in left])
    right = trim([coefficient % prime for coefficient in right])
    while right != [0]:
        left, right = right, remainder_mod(left, right, prime)
    inverse_leading = pow(left[-1], -1, prime)
    return [
        coefficient * inverse_leading % prime for coefficient in left
    ]


def prime_divisors(value: int) -> set[int]:
    """Return the distinct prime divisors of a positive integer."""
    divisors: set[int] = set()
    candidate = 2
    remaining = value
    while candidate * candidate <= remaining:
        if remaining % candidate == 0:
            divisors.add(candidate)
            while remaining % candidate == 0:
                remaining //= candidate
        candidate += 1
    if remaining > 1:
        divisors.add(remaining)
    return divisors


def is_irreducible_mod_prime(
    integer_coefficients: list[int],
    prime: int,
) -> bool:
    """Apply Rabin's exact irreducibility criterion over F_p."""
    polynomial = trim(
        [coefficient % prime for coefficient in integer_coefficients]
    )
    degree = len(polynomial) - 1
    if degree < 1 or polynomial[-1] != 1:
        raise ValueError("certificate polynomial must be monic and nonconstant")

    # Rabin: f of degree n is irreducible iff x^(p^n)-x = 0 mod f and
    # gcd(f, x^(p^(n/q))-x) = 1 for every prime q dividing n.
    check_steps = {degree // divisor for divisor in prime_divisors(degree)}
    frobenius_power = [0, 1]
    variable = [0, 1]
    for step in range(1, degree + 1):
        frobenius_power = power_mod(
            frobenius_power,
            prime,
            polynomial,
            prime,
        )
        if step in check_steps:
            difference = frobenius_power[:]
            if len(difference) < 2:
                difference.extend([0] * (2 - len(difference)))
            difference[1] = (difference[1] - 1) % prime
            if len(gcd_mod(polynomial, difference, prime)) != 1:
                return False

    return trim(frobenius_power) == variable


def exact_factor_audit(
    a: int,
    coefficients: list[int],
    sympy_module: Any,
) -> tuple[int, ...]:
    """Factor over Z with optional SymPy and return factor degrees."""
    symbol = sympy_module.Symbol("b")
    polynomial = sympy_module.Poly.from_list(
        list(reversed(coefficients)),
        gens=symbol,
        domain=sympy_module.ZZ,
    )
    unit, factors = polynomial.factor_list()
    if unit not in (1, -1):
        raise AssertionError(f"unexpected factorization unit at a={a}")

    degrees = tuple(
        sorted(
            factor.degree()
            for factor, exponent in factors
            for _ in range(exponent)
        )
    )
    expected = (2 * a,) if a % 2 == 0 else (1, 1, 2 * a - 2)
    if a == 1:
        expected = (1, 1)
    if degrees != expected:
        raise AssertionError(
            f"unexpected factor degrees at a={a}: "
            f"found {degrees}, expected {expected}"
        )
    return degrees


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-a", type=int, default=59)
    parser.add_argument(
        "--exact-factor",
        action="store_true",
        help="also factor over Z with optional SymPy",
    )
    args = parser.parse_args()

    if args.max_a < 1:
        parser.error("--max-a must be positive")
    if args.max_a > max(MOD_P_CERTIFICATES):
        parser.error("recorded mod-p certificates currently stop at a=59")

    sympy_module = None
    if args.exact_factor:
        try:
            import sympy as sympy_module
        except ImportError:
            parser.error(
                "--exact-factor requires SymPy; omit the flag to run "
                "the standard-library certificate audit"
            )

    for a in range(1, args.max_a + 1):
        coefficients = reflection_integer_coefficients(a)
        residual = conjecturally_irreducible_part(a, coefficients)
        reports: list[str] = []

        if a >= 2:
            prime = MOD_P_CERTIFICATES[a]
            if not is_irreducible_mod_prime(residual, prime):
                raise AssertionError(
                    f"mod-{prime} irreducibility certificate failed at a={a}"
                )
            reports.append(f"residual irreducible mod {prime}")
        else:
            reports.append("two proved linear factors")

        if sympy_module is not None:
            degrees = exact_factor_audit(
                a,
                coefficients,
                sympy_module,
            )
            reports.append(f"Z-factor degrees={degrees}")

        print(f"a={a:2d}: " + "; ".join(reports))

    suffix = ""
    if sympy_module is not None:
        suffix = f"; exact factors checked with SymPy {sympy_module.__version__}"
    print(
        f"Certificate audit passed through a={args.max_a}"
        f"{suffix}."
    )


if __name__ == "__main__":
    main()
