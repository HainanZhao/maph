#!/usr/bin/env python3
"""Certify the affine-line structure behind the F_4, N=11 residual zeros.

The calculation is exact and uses only the Python standard library plus
the project's exact phase-histogram routine.

For an occupation line

    r(x) = (r0, r1, r2, x),  s(x) = (s0, s1, s2, x+d),

the unnormalised amplitude divided by x! is a polynomial on each residue
class x modulo four.  Its degree is at most r0+r1+r2.  We interpolate
those polynomials in q=(x-x0)/4, take the exact gcd of their real and
imaginary parts, and compare it with the claimed common factor.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from fractions import Fraction
from math import factorial
from pathlib import Path
from typing import Callable, Sequence

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.fourier_suppression import phase_histogram  # noqa: E402


Polynomial = list[Fraction]  # coefficients in ascending degree
Occupation = tuple[int, int, int, int]


def trim(polynomial: Polynomial) -> Polynomial:
    while len(polynomial) > 1 and polynomial[-1] == 0:
        polynomial.pop()
    return polynomial


def polynomial_add(left: Polynomial, right: Polynomial) -> Polynomial:
    result = [Fraction(0)] * max(len(left), len(right))
    for index, coefficient in enumerate(left):
        result[index] += coefficient
    for index, coefficient in enumerate(right):
        result[index] += coefficient
    return trim(result)


def polynomial_scale(polynomial: Polynomial,
                     scalar: Fraction) -> Polynomial:
    return trim([scalar * coefficient for coefficient in polynomial])


def polynomial_multiply(left: Polynomial,
                        right: Polynomial) -> Polynomial:
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for left_index, left_coefficient in enumerate(left):
        for right_index, right_coefficient in enumerate(right):
            result[left_index + right_index] += (
                left_coefficient * right_coefficient
            )
    return trim(result)


def polynomial_divmod(
    dividend: Polynomial,
    divisor: Polynomial,
) -> tuple[Polynomial, Polynomial]:
    remainder = trim(dividend[:])
    divisor = trim(divisor[:])
    if divisor == [0]:
        raise ZeroDivisionError("polynomial division by zero")

    quotient = [Fraction(0)] * max(1, len(remainder) - len(divisor) + 1)
    while remainder != [0] and len(remainder) >= len(divisor):
        degree = len(remainder) - len(divisor)
        coefficient = remainder[-1] / divisor[-1]
        quotient[degree] = coefficient
        for index, divisor_coefficient in enumerate(divisor):
            remainder[degree + index] -= coefficient * divisor_coefficient
        trim(remainder)
    return trim(quotient), trim(remainder)


def polynomial_gcd(left: Polynomial, right: Polynomial) -> Polynomial:
    left = trim(left[:])
    right = trim(right[:])
    while right != [0]:
        _, remainder = polynomial_divmod(left, right)
        left, right = right, remainder
    if left == [0]:
        return left
    return polynomial_scale(left, Fraction(1, 1) / left[-1])


def polynomial_from_roots(roots: Sequence[Fraction]) -> Polynomial:
    result = [Fraction(1)]
    for root in roots:
        result = polynomial_multiply(result, [-root, Fraction(1)])
    return result


def forward_differences(values: Sequence[Fraction]) -> list[Fraction]:
    current = list(values)
    leading_differences: list[Fraction] = []
    while current:
        leading_differences.append(current[0])
        current = [
            current[index + 1] - current[index]
            for index in range(len(current) - 1)
        ]
    return leading_differences


def interpolate_at_nonnegative_integers(
    values: Sequence[Fraction],
) -> Polynomial:
    """Return p with p(j)=values[j], in the ordinary power basis."""
    polynomial = [Fraction(0)]
    binomial_basis = [Fraction(1)]
    for degree, difference in enumerate(forward_differences(values)):
        if degree:
            binomial_basis = polynomial_scale(
                polynomial_multiply(
                    binomial_basis,
                    [Fraction(-(degree - 1)), Fraction(1)],
                ),
                Fraction(1, degree),
            )
        polynomial = polynomial_add(
            polynomial,
            polynomial_scale(binomial_basis, difference),
        )
    return trim(polynomial)


@dataclass(frozen=True)
class AffineLine:
    name: str
    input_at: Callable[[int], Occupation]
    output_at: Callable[[int], Occupation]
    minimum_x: int
    fixed_input_particles: int
    common_roots: tuple[int, ...]


LINES = (
    AffineLine(
        "L_A",
        lambda x: (0, 1, 3, x),
        lambda x: (1, 3, 2, x - 2),
        2,
        4,
        (2, 5, 7),
    ),
    AffineLine(
        "L_B",
        lambda x: (0, 1, 3, x),
        lambda x: (1, 3, 3, x - 3),
        3,
        4,
        (7,),
    ),
    AffineLine(
        "L_C",
        lambda x: (0, 3, 3, x),
        lambda x: (1, 1, 2, x + 2),
        0,
        6,
        (-2, -1, 0, 3, 5),
    ),
    AffineLine(
        "L_D",
        lambda x: (1, 1, 2, x),
        lambda x: (1, 1, 3, x - 1),
        1,
        4,
        (1, 2, 7),
    ),
)


def first_admissible_with_residue(minimum: int, residue: int) -> int:
    return minimum + (residue - minimum) % 4


def normalized_amplitude(line: AffineLine,
                         x: int) -> tuple[Fraction, Fraction]:
    histogram = phase_histogram(line.input_at(x), line.output_at(x))
    return (
        Fraction(histogram[0] - histogram[2], factorial(x)),
        Fraction(histogram[1] - histogram[3], factorial(x)),
    )


def factor_string(roots: Sequence[int]) -> str:
    factors = []
    for root in roots:
        if root == 0:
            factors.append("x")
        elif root > 0:
            factors.append(f"(x-{root})")
        else:
            factors.append(f"(x+{-root})")
    return "".join(factors)


def certify_line(line: AffineLine) -> tuple[int, ...]:
    for residue in range(4):
        x0 = first_admissible_with_residue(line.minimum_x, residue)
        samples = [
            normalized_amplitude(line, x0 + 4 * q)
            for q in range(line.fixed_input_particles + 2)
        ]
        real_polynomial = interpolate_at_nonnegative_integers(
            [sample[0] for sample in samples[:-1]]
        )
        imaginary_polynomial = interpolate_at_nonnegative_integers(
            [sample[1] for sample in samples[:-1]]
        )

        # The final sample is independent of the interpolation data.
        check_q = line.fixed_input_particles + 1
        for polynomial, expected_value in zip(
            (real_polynomial, imaginary_polynomial),
            samples[-1],
        ):
            actual_value = sum(
                coefficient * check_q**degree
                for degree, coefficient in enumerate(polynomial)
            )
            if actual_value != expected_value:
                raise AssertionError(
                    f"{line.name}, residue {residue}: degree bound failed"
                )

        common_divisor = polynomial_gcd(
            real_polynomial, imaginary_polynomial
        )
        expected_divisor = polynomial_from_roots(
            [Fraction(root - x0, 4) for root in line.common_roots]
        )
        if common_divisor != expected_divisor:
            raise AssertionError(
                f"{line.name}, residue {residue}: unexpected gcd\n"
                f"actual={common_divisor}\nexpected={expected_divisor}"
            )

    admissible_roots = tuple(
        root for root in line.common_roots if root >= line.minimum_x
    )
    for root in admissible_roots:
        histogram = phase_histogram(
            line.input_at(root), line.output_at(root)
        )
        if histogram[0] != histogram[2] or histogram[1] != histogram[3]:
            raise AssertionError(f"{line.name}: root {root} is not dark")
    return admissible_roots


def certify_hidden_histogram_identity() -> None:
    """Certify the identity using seven values in each residue class.

    After division by x!, every histogram component on either side is
    a polynomial of degree at most six for fixed x modulo four.  Seven
    equal values therefore prove equality throughout that residue.
    """
    degree_bound = 6
    for residue in range(4):
        for q in range(degree_bound + 1):
            x = residue + 4 * q
            left = phase_histogram(
                (0, 1, 3, x + 2),
                (1, 3, 2, x),
            )
            right = phase_histogram(
                (0, 3, 3, x),
                (1, 1, 2, x + 2),
            )
            normalized_difference = tuple(
                Fraction(left[index] - right[index], factorial(x))
                for index in range(4)
            )
            if normalized_difference != (0, 0, 0, 0):
                raise AssertionError(
                    f"histogram identity failed at x={x}"
                )


def main() -> None:
    print("Exact affine-line certificates")
    for line in LINES:
        roots = certify_line(line)
        print(
            f"{line.name}: gcd={factor_string(line.common_roots)}; "
            f"admissible dark x={','.join(map(str, roots))}"
        )

    certify_hidden_histogram_identity()
    print(
        "Hidden histogram identity certified by degree <= 6 and "
        "7 exact samples in each of 4 residue classes."
    )


if __name__ == "__main__":
    main()
