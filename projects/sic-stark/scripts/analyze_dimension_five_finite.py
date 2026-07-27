#!/usr/bin/env python3
"""Exact finite-algebra audit for the dimension-five principal ghost."""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import combinations


ZERO = (Fraction(0),) * 8
ONE = (Fraction(1),) + ZERO[1:]


def add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def neg(value):
    return tuple(-a for a in value)


def multiply(left, right):
    """Multiply in Q(zeta_5,sqrt(6)), basis zeta^j and sqrt(6)zeta^j."""

    out = [Fraction(0)] * 8
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            if not a or not b:
                continue
            si, zi = divmod(i, 4)
            sj, zj = divmod(j, 4)
            coefficient = a * b * (6 if si + sj == 2 else 1)
            square_root_part = (si + sj) % 2
            power = (zi + zj) % 5
            if power < 4:
                out[4 * square_root_part + power] += coefficient
            else:
                for reduced_power in range(4):
                    out[4 * square_root_part + reduced_power] -= coefficient
    return tuple(out)


def inverse(value):
    columns = [
        multiply(value, tuple(Fraction(i == j) for i in range(8)))
        for j in range(8)
    ]
    matrix = [
        [columns[column][row] for column in range(8)] + [ONE[row]]
        for row in range(8)
    ]
    for column in range(8):
        pivot = next(
            row for row in range(column, 8) if matrix[row][column]
        )
        matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
        scale = matrix[column][column]
        matrix[column] = [entry / scale for entry in matrix[column]]
        for row in range(8):
            if row == column or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(matrix[row], matrix[column])
            ]
    return tuple(matrix[row][-1] for row in range(8))


def power(value, exponent):
    out = ONE
    while exponent:
        if exponent & 1:
            out = multiply(out, value)
        value = multiply(value, value)
        exponent //= 2
    return out


def polynomial_add(left, right):
    out = dict(left)
    for monomial, coefficient in right.items():
        out[monomial] = add(out.get(monomial, ZERO), coefficient)
        if out[monomial] == ZERO:
            del out[monomial]
    return out


def polynomial_multiply(left, right):
    out = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(
                a + b for a, b in zip(left_monomial, right_monomial)
            )
            out = polynomial_add(
                out,
                {monomial: multiply(left_coefficient, right_coefficient)},
            )
    return out


def polynomial_scale(coefficient, polynomial):
    return {
        monomial: multiply(coefficient, value)
        for monomial, value in polynomial.items()
        if multiply(coefficient, value) != ZERO
    }


def variable(index, exponent=1):
    monomial = [0] * 4
    monomial[index] = exponent
    return {tuple(monomial): ONE}


def constant(value):
    return {(0, 0, 0, 0): value}


def field_rank(rows):
    matrix = [row[:] for row in rows]
    rank = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (
                row
                for row in range(rank, len(matrix))
                if matrix[row][column] != ZERO
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_inverse = inverse(matrix[rank][column])
        matrix[rank] = [
            multiply(pivot_inverse, value) for value in matrix[rank]
        ]
        for row in range(len(matrix)):
            if row == rank or matrix[row][column] == ZERO:
                continue
            coefficient = matrix[row][column]
            matrix[row] = [
                add(value, neg(multiply(coefficient, pivot_value)))
                for value, pivot_value in zip(matrix[row], matrix[rank])
            ]
        rank += 1
    return rank


def fraction_text(value):
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def main():
    zeta = (Fraction(0), Fraction(1)) + ZERO[2:]
    sqrt_six = ZERO[:4] + (Fraction(1),) + ZERO[5:]
    minus_one = neg(ONE)
    x, y, z, w = [variable(index) for index in range(4)]
    xi, yi, zi, wi = [variable(index, -1) for index in range(4)]

    table = [
        [constant(sqrt_six), x, y, yi, xi],
        [xi, polynomial_scale(minus_one, zi), wi,
         polynomial_scale(minus_one, zi), x],
        [yi, wi, wi, y, polynomial_scale(minus_one, z)],
        [y, polynomial_scale(minus_one, zi), yi, w, w],
        [x, xi, polynomial_scale(minus_one, z), w,
         polynomial_scale(minus_one, z)],
    ]

    tau = power(zeta, 3)
    matrix = [[{} for _ in range(5)] for _ in range(5)]
    for first in range(5):
        for second in range(5):
            for column in range(5):
                row = (column + first) % 5
                phase = multiply(
                    power(tau, first * second),
                    power(zeta, second * column),
                )
                matrix[row][column] = polynomial_add(
                    matrix[row][column],
                    polynomial_scale(phase, table[first][second]),
                )

    minors = []
    labels = []
    for first_row, second_row in combinations(range(5), 2):
        for first_column, second_column in combinations(range(5), 2):
            minors.append(
                polynomial_add(
                    polynomial_multiply(
                        matrix[first_row][first_column],
                        matrix[second_row][second_column],
                    ),
                    polynomial_scale(
                        minus_one,
                        polynomial_multiply(
                            matrix[first_row][second_column],
                            matrix[second_row][first_column],
                        ),
                    ),
                )
            )
            labels.append(
                [[first_row, second_row], [first_column, second_column]]
            )

    monomials = sorted(set().union(*(minor.keys() for minor in minors)))
    rows = [
        [minor.get(monomial, ZERO) for monomial in monomials]
        for minor in minors
    ]
    certificate = {
        "schema": "sic-stark-dimension-five-finite-v1",
        "coefficient_field": "Q(zeta_5,sqrt(6))",
        "coefficient_basis": [
            "1", "zeta", "zeta^2", "zeta^3",
            "sqrt(6)", "sqrt(6)zeta", "sqrt(6)zeta^2",
            "sqrt(6)zeta^3",
        ],
        "laurent_variables": ["x", "y", "z", "w"],
        "overlap_table": [
            ["sqrt(6)", "x", "y", "y^-1", "x^-1"],
            ["x^-1", "-z^-1", "w^-1", "-z^-1", "x"],
            ["y^-1", "w^-1", "w^-1", "y", "-z"],
            ["y", "-z^-1", "y^-1", "w", "w"],
            ["x", "x^-1", "-z", "w", "-z"],
        ],
        "matrix_scale": "5*sqrt(6); scaling does not change rank",
        "minor_count": len(minors),
        "nonzero_formal_minor_count": sum(bool(minor) for minor in minors),
        "distinct_laurent_monomial_count": len(monomials),
        "minor_linear_span_rank_over_coefficient_field": field_rank(rows),
        "minor_term_counts": [len(minor) for minor in minors],
        "minor_labels": labels,
        "monomials": [list(monomial) for monomial in monomials],
        "minors": [
            {
                ",".join(map(str, monomial)): [
                    fraction_text(value) for value in coefficient
                ]
                for monomial, coefficient in sorted(minor.items())
            }
            for minor in minors
        ],
    }
    print(json.dumps(certificate, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
