#!/usr/bin/env python3
"""Exact quotient-ring TCC certificate for the maximal-order d=8 tuple."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import combinations


# Basis monomials are z^a d^b x^c.  The distinguished real roots satisfy
#
# x^8-2x^6-2x^4-2x^2+1=0,
# d^2=(3x^7-2x^6-5x^5+4x^4-7x^3+4x^2-9x+6)/2,
# z^4=sqrt(2)z^2-1,
#
# where sqrt(2)=(-x^7+x^5+5x^3+3x)/2.  The last identity glues the
# common real quadratic subfield of the overlap and cyclotomic fields.
Monomial = tuple[int, int, int]
Element = dict[Monomial, Fraction]
ONE_MONOMIAL: Monomial = (0, 0, 0)


def polynomial(coefficients: dict[int, Fraction | int]) -> Element:
    return {
        (0, 0, exponent): Fraction(coefficient)
        for exponent, coefficient in coefficients.items()
        if coefficient
    }


X_EIGHT = polynomial({6: 2, 4: 2, 2: 2, 0: -1})
SQRT_TWO = polynomial({
    7: Fraction(-1, 2), 5: Fraction(1, 2),
    3: Fraction(5, 2), 1: Fraction(3, 2),
})
D_SQUARE = polynomial({
    7: Fraction(3, 2), 6: -1, 5: Fraction(-5, 2), 4: 2,
    3: Fraction(-7, 2), 2: 2, 1: Fraction(-9, 2), 0: 3,
})
D_SQUARE_INVERSE = polynomial({
    7: Fraction(-1, 2), 5: Fraction(1, 2),
    3: Fraction(3, 2), 2: 1, 1: Fraction(3, 2), 0: 1,
})
CYCLIC_D_FACTOR = polynomial({
    7: Fraction(1, 2), 6: Fraction(-1, 2),
    5: Fraction(-1, 2), 4: 1, 3: -2, 2: 1,
    1: -2, 0: Fraction(3, 2),
})
X_INVERSE_POLYNOMIAL = polynomial({
    7: -1, 5: 2, 3: 2, 1: 2,
})
U_INVERSE = polynomial({6: -1, 4: 2, 2: 2, 0: 2})


def clean(value: Element) -> Element:
    return {
        monomial: coefficient
        for monomial, coefficient in value.items()
        if coefficient
    }


def add(first: Element, second: Element) -> Element:
    result: defaultdict[Monomial, Fraction] = defaultdict(Fraction)
    for source in (first, second):
        for monomial, coefficient in source.items():
            result[monomial] += coefficient
    return clean(dict(result))


def negate(value: Element) -> Element:
    return {
        monomial: -coefficient
        for monomial, coefficient in value.items()
    }


def subtract(first: Element, second: Element) -> Element:
    return add(first, negate(second))


def scale(value: Element, coefficient: Fraction | int) -> Element:
    factor = Fraction(coefficient)
    return clean({
        monomial: factor * entry for monomial, entry in value.items()
    })


def shifted(value: Element, shift: Monomial) -> Element:
    result: defaultdict[Monomial, Fraction] = defaultdict(Fraction)
    for monomial, coefficient in value.items():
        combined = tuple(
            monomial[index] + shift[index] for index in range(3)
        )
        for reduced, reduced_coefficient in reduce_monomial(combined):
            result[reduced] += coefficient * reduced_coefficient
    return clean(dict(result))


@lru_cache(maxsize=None)
def reduce_monomial(
    monomial: Monomial,
) -> tuple[tuple[Monomial, Fraction], ...]:
    z_power, d_power, x_power = monomial
    if x_power >= 8:
        reduced = (z_power, d_power, x_power - 8)
        return tuple(shifted(X_EIGHT, reduced).items())
    if d_power >= 2:
        reduced = (z_power, d_power - 2, x_power)
        return tuple(shifted(D_SQUARE, reduced).items())
    if z_power >= 4:
        first = shifted(SQRT_TWO, (z_power - 2, d_power, x_power))
        second = dict(reduce_monomial(
            (z_power - 4, d_power, x_power)
        ))
        return tuple(subtract(first, second).items())
    return ((monomial, Fraction(1)),)


def multiply(first: Element, second: Element) -> Element:
    result: defaultdict[Monomial, Fraction] = defaultdict(Fraction)
    for left, left_coefficient in first.items():
        for right, right_coefficient in second.items():
            product = tuple(
                left[index] + right[index] for index in range(3)
            )
            for monomial, coefficient in reduce_monomial(product):
                result[monomial] += (
                    left_coefficient * right_coefficient * coefficient
                )
    return clean(dict(result))


def power(value: Element, exponent: int) -> Element:
    result = {ONE_MONOMIAL: Fraction(1)}
    base = value
    while exponent:
        if exponent & 1:
            result = multiply(result, base)
        base = multiply(base, base)
        exponent //= 2
    return result


def variable(index: int) -> Element:
    monomial = [0, 0, 0]
    monomial[index] = 1
    return {tuple(monomial): Fraction(1)}


ONE = {ONE_MONOMIAL: Fraction(1)}
ZETA = variable(0)
X = variable(2)
D = multiply(
    CYCLIC_D_FACTOR,
    subtract(ZETA, power(ZETA, 7)),
)
U = power(X, 2)
X_INVERSE = X_INVERSE_POLYNOMIAL
D_INVERSE = multiply(D, D_SQUARE_INVERSE)
A = multiply(X, D)
A_INVERSE = multiply(X_INVERSE, D_INVERSE)


TABLE = [
    [scale(ONE, 3), negate(A), U, A_INVERSE, negate(ONE),
     A, U_INVERSE, negate(A_INVERSE)],
    [negate(A_INVERSE), negate(A_INVERSE), negate(A_INVERSE), negate(A),
     negate(D), negate(D), D, D_INVERSE],
    [U_INVERSE, negate(A_INVERSE), U_INVERSE, negate(D_INVERSE), U_INVERSE,
     negate(A_INVERSE), U, negate(D_INVERSE)],
    [A, negate(A_INVERSE), negate(D_INVERSE), A, negate(D_INVERSE),
     negate(D), A, negate(D_INVERSE)],
    [negate(ONE), negate(D_INVERSE), U_INVERSE, negate(D), negate(ONE),
     D_INVERSE, U, D],
    [A_INVERSE, negate(D), negate(A_INVERSE), negate(D_INVERSE), D,
     A_INVERSE, D, negate(A)],
    [U, D, U_INVERSE, A, U, D, U, A],
    [negate(A), D, negate(D_INVERSE), negate(D_INVERSE), D_INVERSE,
     negate(A_INVERSE), A, negate(A)],
]


def sum_elements(values) -> Element:
    result: Element = {}
    for value in values:
        result = add(result, value)
    return result


def ghost_matrix(determinant: int) -> list[list[Element]]:
    matrix = [[{} for _ in range(8)] for _ in range(8)]
    tau = negate(ZETA)
    omega = power(ZETA, 2)
    for row in range(8):
        for column in range(8):
            first = (row - column) % 8
            terms = []
            for second in range(8):
                transformed = (determinant * second) % 8
                wrap = (
                    -1
                    if determinant == -1 and second and first % 2
                    else 1
                )
                term = multiply(
                    TABLE[first][second],
                    multiply(
                        power(tau, first * transformed),
                        power(omega, transformed * column),
                    ),
                )
                terms.append(term if wrap == 1 else negate(term))
            matrix[row][column] = scale(sum_elements(terms), Fraction(1, 24))
    return matrix


def audit_shift(shift: int, determinant: int) -> None:
    matrix = ghost_matrix(determinant)
    square = [
        [
            sum_elements(
                multiply(matrix[row][middle], matrix[middle][column])
                for middle in range(8)
            )
            for column in range(8)
        ]
        for row in range(8)
    ]
    nonzero_idempotency = sum(
        subtract(square[row][column], matrix[row][column]) != {}
        for row in range(8)
        for column in range(8)
    )
    trace = sum_elements(matrix[index][index] for index in range(8))
    nonzero_minors = 0
    minor_count = 0
    for first_row, second_row in combinations(range(8), 2):
        for first_column, second_column in combinations(range(8), 2):
            minor_count += 1
            minor = subtract(
                multiply(
                    matrix[first_row][first_column],
                    matrix[second_row][second_column],
                ),
                multiply(
                    matrix[first_row][second_column],
                    matrix[second_row][first_column],
                ),
            )
            nonzero_minors += minor != {}
    print(f"SHIFT_{shift}_TRACE_IS_ONE={int(trace == ONE)}")
    print(f"SHIFT_{shift}_NONZERO_IDEMPOTENCY_ENTRIES={nonzero_idempotency}")
    print(f"SHIFT_{shift}_MINOR_COUNT={minor_count}")
    print(f"SHIFT_{shift}_NONZERO_MINORS={nonzero_minors}")
    if trace != ONE or nonzero_idempotency or nonzero_minors:
        raise AssertionError(f"exact shift {shift} certificate failed")


def main() -> None:
    assert multiply(X, X_INVERSE) == ONE
    assert multiply(U, U_INVERSE) == ONE
    assert subtract(power(D, 2), D_SQUARE) == {}
    assert multiply(D, D_INVERSE) == ONE
    assert multiply(A, A_INVERSE) == ONE
    assert subtract(
        power(ZETA, 4),
        subtract(multiply(SQRT_TWO, power(ZETA, 2)), ONE),
    ) == {}
    print(f"QUOTIENT_CACHE_INITIAL={reduce_monomial.cache_info().currsize}")
    audit_shift(1, 1)
    audit_shift(0, -1)
    print(f"QUOTIENT_CACHE_FINAL={reduce_monomial.cache_info().currsize}")
    print("DIMENSION_EIGHT_MAXIMAL_EXACT_TCC_CERTIFIED=1")


if __name__ == "__main__":
    main()
