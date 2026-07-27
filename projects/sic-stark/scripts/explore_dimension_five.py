#!/usr/bin/env python3
"""Numerical audit of the dimension-five principal ghost and Stark polynomial."""

from __future__ import annotations

import cmath
import math

from explore_dimension_four_double_sine import double_sine


def principal_overlap(first: int, second: int, beta: float) -> float:
    if first == second == 0:
        return math.sqrt(6)
    third = (-first - second) % 5
    exponent = 5 * (first + second) + first * second + min(
        5, first + second
    )
    arguments = (
        1 + (second * beta - first) / 5,
        1 + (first * beta - third) / 5,
        1 + (third * beta - second) / 5,
    )
    return (-1) ** exponent * math.prod(
        double_sine(argument, beta, 1.0) for argument in arguments
    )


def evaluate_polynomial(coefficients, value):
    out = 0.0
    for coefficient in coefficients:
        out = out * value + coefficient
    return out


def main() -> None:
    beta = 2 + math.sqrt(3)
    table = [
        [principal_overlap(first, second, beta) for second in range(5)]
        for first in range(5)
    ]
    x, y = table[0][1], table[0][2]
    z, w = -table[2][4], table[3][3]
    variables = [x, y, z, w]

    s = math.sqrt(3)
    polynomial = [
        1,
        -(8 + 5 * s),
        53 + 30 * s,
        -(156 + 90 * s),
        225 + 130 * s,
        -(156 + 90 * s),
        53 + 30 * s,
        -(8 + 5 * s),
        1,
    ]
    polynomial_residual = max(
        abs(evaluate_polynomial(polynomial, value * value))
        / sum(
            abs(coefficient * (value * value) ** (8 - index))
            for index, coefficient in enumerate(polynomial)
        )
        for value in variables
    )

    tau = -cmath.exp(math.pi * 1j / 5)
    omega = cmath.exp(2 * math.pi * 1j / 5)
    matrix = [[0j for _ in range(5)] for _ in range(5)]
    for first in range(5):
        for second in range(5):
            for column in range(5):
                row = (column + first) % 5
                matrix[row][column] += (
                    table[first][second]
                    * tau ** (first * second)
                    * omega ** (second * column)
                    / (5 * math.sqrt(6))
                )

    square = [
        [
            sum(matrix[row][middle] * matrix[middle][column]
                for middle in range(5))
            for column in range(5)
        ]
        for row in range(5)
    ]
    idempotency_residual = max(
        abs(square[row][column] - matrix[row][column])
        for row in range(5)
        for column in range(5)
    )
    minor_residual = max(
        abs(
            matrix[first_row][first_column]
            * matrix[second_row][second_column]
            - matrix[first_row][second_column]
            * matrix[second_row][first_column]
        )
        for first_row in range(5)
        for second_row in range(first_row + 1, 5)
        for first_column in range(5)
        for second_column in range(first_column + 1, 5)
    )

    print(f"beta = {beta:.15f}")
    print("positive generators =", " ".join(f"{value:.15f}" for value in variables))
    print(
        "maximum relative reciprocal Stark-polynomial residual = "
        f"{polynomial_residual:.3e}"
    )
    print(f"trace residual = {abs(sum(matrix[i][i] for i in range(5))-1):.3e}")
    print(f"maximum idempotency residual = {idempotency_residual:.3e}")
    print(f"maximum 2-minor residual = {minor_residual:.3e}")


if __name__ == "__main__":
    main()
