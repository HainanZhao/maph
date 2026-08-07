#!/usr/bin/env python3
"""Exact checks for the width-four q-Fibonomial unimodality proof.

The proof uses this script only for the finite cases m=1,...,7.  The script
also checks the partition formula by direct enumeration and independently
constructs the defining polynomial quotient for m=1,...,24.  All arithmetic
is integer arithmetic and the script has no third-party dependencies.
"""
from __future__ import annotations


def p(parts_sum: int) -> int:
    """Number of solutions x+2y+3z=parts_sum with x,y,z >= 0."""
    if parts_sum < 0:
        return 0
    return (parts_sum * parts_sum + 6 * parts_sum + 12) // 12


def difference(degree: int, a: int, b: int) -> int:
    """[q^degree] (1-q) W_m for a=F_(m+1), b=F_(m+2)."""
    return p(degree) - p(degree - a) - p(degree - b) + p(degree - (2 * a + b))


def multiply(left: list[int], right: list[int]) -> list[int]:
    """Multiply two polynomials stored in ascending coefficient order."""
    product = [0] * (len(left) + len(right) - 1)
    for i, left_coefficient in enumerate(left):
        for j, right_coefficient in enumerate(right):
            product[i + j] += left_coefficient * right_coefficient
    return product


def multiply_by_q_integer(polynomial: list[int], length: int) -> list[int]:
    """Multiply by 1+q+...+q^(length-1) using a sliding window."""
    assert length >= 1
    product = [0] * (len(polynomial) + length - 1)
    window = 0
    for degree in range(len(product)):
        if degree < len(polynomial):
            window += polynomial[degree]
        if degree >= length:
            window -= polynomial[degree - length]
        product[degree] = window
    return product


def exact_quotient(numerator: list[int], denominator: list[int]) -> list[int]:
    """Divide ascending integer polynomials when denominator[0] is one."""
    assert denominator and denominator[0] == 1
    remainder = numerator[:]
    quotient_degree = len(numerator) - len(denominator)
    assert quotient_degree >= 0
    quotient = [0] * (quotient_degree + 1)
    for degree in range(quotient_degree + 1):
        coefficient = remainder[degree]
        quotient[degree] = coefficient
        for offset, denominator_coefficient in enumerate(denominator):
            remainder[degree + offset] -= coefficient * denominator_coefficient
    assert all(coefficient == 0 for coefficient in remainder)
    return quotient


def direct_width_four(a: int, b: int) -> list[int]:
    """Construct [a]_q[b]_q[a+b]_q[a+2b]_q/([2]_q[3]_q)."""
    numerator = [1]
    for length in (a, b, a + b, a + 2 * b):
        numerator = multiply_by_q_integer(numerator, length)
    denominator = multiply([1, 1], [1, 1, 1])
    return exact_quotient(numerator, denominator)


def main() -> None:
    fibonacci = [0, 1]
    for _ in range(30):
        fibonacci.append(fibonacci[-1] + fibonacci[-2])

    # Independent verification of the closed formula for p(t).
    for parts_sum in range(301):
        enumerated = sum(
            1
            for z in range(parts_sum // 3 + 1)
            for y in range((parts_sum - 3 * z) // 2 + 1)
        )
        assert p(parts_sum) == enumerated, (parts_sum, p(parts_sum), enumerated)

    expected_minima = [0, 0, 0, 0, 1, 1, 1]
    for m, expected in enumerate(expected_minima, start=1):
        a, b = fibonacci[m + 1], fibonacci[m + 2]
        midpoint = (3 * a + 4 * b - 7) // 2
        actual = min(difference(degree, a, b) for degree in range(midpoint + 1))
        assert actual == expected, (m, a, b, midpoint, actual, expected)

    # A structurally separate quotient construction checks the reduced
    # coefficient-difference formula beyond the finite range used in proof.
    for m in range(1, 25):
        a, b = fibonacci[m + 1], fibonacci[m + 2]
        coefficients = direct_width_four(a, b)
        assert coefficients == coefficients[::-1], m
        midpoint = (len(coefficients) - 1) // 2
        for degree in range(midpoint + 1):
            previous = coefficients[degree - 1] if degree else 0
            assert coefficients[degree] - previous == difference(degree, a, b), (
                m,
                degree,
            )

    print("PARTITION_FORMULA_PASSED_T0_TO_300")
    print("SMALL_CASES_PASSED_M1_TO_7")
    print("DIRECT_QUOTIENT_CROSSCHECK_PASSED_M1_TO_24")


if __name__ == "__main__":
    main()
