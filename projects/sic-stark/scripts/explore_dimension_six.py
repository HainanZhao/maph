#!/usr/bin/env python3
"""Numerical reconnaissance for the dimension-six principal ghost.

This is intentionally an exploratory calculation.  It evaluates the
published three-double-sine formula, reconstructs the normalized Weyl
operator, and records the orbit structure that a later exact certificate
would have to explain.
"""

from __future__ import annotations

import cmath
import math
from functools import lru_cache
from itertools import permutations, product

import numpy

from explore_dimension_four_double_sine import double_sine


DIMENSION = 6
BETA = (5 + math.sqrt(21)) / 2


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


def zauner_orbits() -> list[list[tuple[int, int]]]:
    unseen = {
        (first, second)
        for first in range(DIMENSION)
        for second in range(DIMENSION)
    }
    orbits = []
    while unseen:
        seed = min(unseen)
        orbit = []
        value = seed
        while value not in orbit:
            orbit.append(value)
            unseen.discard(value)
            first, second = value
            value = (
                (-first - second) % DIMENSION,
                first % DIMENSION,
            )
        orbits.append(orbit)
    return orbits


def structured_table(
    primitive: tuple[float, float, float], lower: float
) -> list[list[float]]:
    """Return the observed four-parameter d=6 table.

    The three entries of ``primitive`` occupy the three primitive
    modulus-six ray pairs.  ``lower`` supplies every singular stratum
    through its first three powers.
    """

    first, second, third = primitive
    return [
        [
            math.sqrt(7),
            -first,
            lower,
            -1,
            lower**-1,
            -first**-1,
        ],
        [
            -first**-1,
            -lower**-2,
            -second,
            -third,
            -lower**-2,
            -first,
        ],
        [
            lower**-1,
            -third,
            lower**-3,
            -second,
            lower,
            lower**2,
        ],
        [
            -1,
            -second,
            -third,
            -1,
            third**-1,
            -second**-1,
        ],
        [
            lower,
            -lower**-2,
            lower**-1,
            second**-1,
            lower**3,
            third**-1,
        ],
        [
            -first,
            -first**-1,
            lower**2,
            -third**-1,
            second**-1,
            -lower**2,
        ],
    ]


def maximum_minor(matrix: numpy.ndarray) -> float:
    return max(
        abs(numpy.linalg.det(matrix[numpy.ix_(rows, columns)]))
        for first_row in range(DIMENSION)
        for second_row in range(first_row + 1, DIMENSION)
        for first_column in range(DIMENSION)
        for second_column in range(first_column + 1, DIMENSION)
        for rows in [(first_row, second_row)]
        for columns in [(first_column, second_column)]
    )


def finite_stark_polynomial(value: float) -> float:
    return (
        value**3
        + (2 - 5 * BETA) * value**2
        + (35 * BETA - 11) * value
        + 13
        - 78 * BETA
    )


def main() -> None:
    table = [
        [principal_overlap(first, second) for second in range(DIMENSION)]
        for first in range(DIMENSION)
    ]
    matrix = reconstruct(table)
    square = matrix @ matrix
    singular_values = numpy.linalg.svd(matrix, compute_uv=False)
    primitive = (
        -table[0][1],
        -table[1][2],
        -table[1][3],
    )
    lower = table[0][2]
    table_model_error = max(
        abs(table[row][column] - structured_table(primitive, lower)[row][column])
        for row in range(DIMENSION)
        for column in range(DIMENSION)
    )
    ordering_trials = []
    for permutation in permutations(primitive):
        for inversion_bits in product((0, 1), repeat=3):
            candidate = tuple(
                value**(-1 if inversion else 1)
                for value, inversion in zip(permutation, inversion_bits)
            )
            for lower_inversion in (0, 1):
                candidate_lower = lower ** (-1 if lower_inversion else 1)
                ordering_trials.append(
                    (
                        maximum_minor(
                            reconstruct(
                                structured_table(candidate, candidate_lower)
                            )
                        ),
                        abs(
                            candidate[0]
                            * candidate[1]
                            / candidate[2]
                            - candidate_lower**2
                        ),
                        permutation,
                        inversion_bits,
                        lower_inversion,
                    )
                )
    ordering_trials.sort(key=lambda item: item[0])

    print(f"dimension = {DIMENSION}")
    print(f"beta = {BETA:.15f}")
    print(f"distinct double-sine arguments = {cached_double_sine.cache_info().currsize}")
    print("overlap table:")
    for row in table:
        print(" ".join(f"{entry:+.12f}" for entry in row))
    print("Zauner orbits and overlap values:")
    for orbit in zauner_orbits():
        values = [table[first][second] for first, second in orbit]
        print(
            f"{orbit}: "
            + ", ".join(f"{value:+.12f}" for value in values)
        )
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
    print(
        "structured four-parameter table residual = "
        f"{table_model_error:.3e}"
    )
    print(
        "lower-stratum relation residual = "
        f"{lower**2 + lower**-2 - (BETA - 2):+.3e}"
    )
    print(
        "component norm-compatibility residual = "
        f"{primitive[0] * primitive[1] / primitive[2] - lower**2:+.3e}"
    )
    print("primitive trace values and finite Stark residuals:")
    for value in primitive:
        trace = value**2 + value**-2
        print(
            f"value={value:.12f} trace={trace:.12f} "
            f"residual={finite_stark_polynomial(trace):+.3e}"
        )
    print("best primitive-packet reorderings:")
    for (
        residual,
        norm_residual,
        permutation,
        inversion_bits,
        lower_inversion,
    ) in ordering_trials[:12]:
        labels = tuple(primitive.index(value) for value in permutation)
        print(
            f"residual={residual:.3e} "
            f"norm_residual={norm_residual:.3e} "
            f"permutation={labels} inversions={inversion_bits} "
            f"lower_inversion={lower_inversion}"
        )


if __name__ == "__main__":
    main()
