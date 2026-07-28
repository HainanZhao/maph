#!/usr/bin/env python3
"""Numerical audit of the canonical dimension-eight principal ghost."""

from __future__ import annotations

import cmath
import math
from functools import lru_cache

import numpy

from explore_dimension_four_double_sine import double_sine


DIMENSION = 8
BETA = (7 + 3 * math.sqrt(5)) / 2


@lru_cache(maxsize=None)
def cached_double_sine(argument: float) -> float:
    return double_sine(argument, BETA, 1.0)


def principal_overlap(first: int, second: int) -> float:
    if first == second == 0:
        return math.sqrt(DIMENSION + 1)
    third = (-first - second) % DIMENSION
    exponent = (
        DIMENSION * (first + second)
        + first * second
        + min(DIMENSION, first + second)
    )
    arguments = (
        1 + (second * BETA - first) / DIMENSION,
        1 + (first * BETA - third) / DIMENSION,
        1 + (third * BETA - second) / DIMENSION,
    )
    return (-1) ** exponent * math.prod(
        cached_double_sine(argument) for argument in arguments
    )


def reconstruct(table: list[list[float]]) -> numpy.ndarray:
    tau = -cmath.exp(math.pi * 1j / DIMENSION)
    omega = cmath.exp(2 * math.pi * 1j / DIMENSION)
    matrix = numpy.zeros((DIMENSION, DIMENSION), dtype=complex)
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            for column in range(DIMENSION):
                row = (column + first) % DIMENSION
                matrix[row, column] += (
                    table[first][second]
                    * tau ** (first * second)
                    * omega ** (second * column)
                    / (DIMENSION * math.sqrt(DIMENSION + 1))
                )
    return matrix


def maximum_minor(matrix: numpy.ndarray) -> float:
    return max(
        abs(
            matrix[first_row, first_column]
            * matrix[second_row, second_column]
            - matrix[first_row, second_column]
            * matrix[second_row, first_column]
        )
        for first_row in range(DIMENSION)
        for second_row in range(first_row + 1, DIMENSION)
        for first_column in range(DIMENSION)
        for second_column in range(first_column + 1, DIMENSION)
    )


def main() -> None:
    table = [
        [principal_overlap(first, second) for second in range(DIMENSION)]
        for first in range(DIMENSION)
    ]
    matrix = reconstruct(table)
    square = matrix @ matrix
    singular_values = numpy.linalg.svd(matrix, compute_uv=False)

    print(f"dimension = {DIMENSION}")
    print(f"beta = {BETA:.16f}")
    print(
        "distinct double-sine arguments = "
        f"{cached_double_sine.cache_info().currsize}"
    )
    print("normalized overlap table:")
    for row in table:
        print(" ".join(f"{entry:+.12f}" for entry in row))
    print(f"trace residual = {abs(numpy.trace(matrix) - 1):.3e}")
    print(
        "maximum idempotency residual = "
        f"{numpy.max(numpy.abs(square - matrix)):.3e}"
    )
    print(f"maximum 2-minor residual = {maximum_minor(matrix):.3e}")
    print(
        "singular values = "
        + " ".join(f"{value:.12e}" for value in singular_values)
    )


if __name__ == "__main__":
    main()
