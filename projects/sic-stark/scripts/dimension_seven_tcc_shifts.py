#!/usr/bin/env python3
"""Numerical audit of both formal d=7 TCC shifts."""

from __future__ import annotations

import cmath
import json
import math

import numpy

from explore_dimension_seven import principal_overlap


DIMENSION = 7


def overlap_table() -> list[list[float]]:
    result = [
        [
            principal_overlap(first, second)
            for second in range(DIMENSION)
        ]
        for first in range(DIMENSION)
    ]
    result[0][0] = math.sqrt(DIMENSION + 1)
    return result


def reconstruct(
    table: list[list[float]], determinant: int
) -> numpy.ndarray:
    tau = -cmath.exp(math.pi * 1j / DIMENSION)
    omega = cmath.exp(2 * math.pi * 1j / DIMENSION)
    matrix = numpy.zeros((DIMENSION, DIMENSION), dtype=complex)
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            transformed_first = first
            transformed_second = (determinant * second) % DIMENSION
            for column in range(DIMENSION):
                row = (column + transformed_first) % DIMENSION
                matrix[row, column] += (
                    table[first][second]
                    * tau ** (transformed_first * transformed_second)
                    * omega ** (transformed_second * column)
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


def audit_shift(
    shift: int, determinant: int, table: list[list[float]]
) -> dict[str, object]:
    congruence = determinant * (2 * shift + 13) % DIMENSION
    if congruence != 1:
        raise AssertionError("twist-shift congruence failed")
    matrix = reconstruct(table, determinant)
    singular_values = numpy.linalg.svd(matrix, compute_uv=False)
    return {
        "shift": shift,
        "twist": "I" if determinant == 1 else "diag(1,-1)",
        "twist_determinant": determinant,
        "twist_shift_congruence": congruence,
        "trace_residual": abs(numpy.trace(matrix) - 1),
        "idempotency_residual": float(
            numpy.max(numpy.abs(matrix @ matrix - matrix))
        ),
        "maximum_minor_residual": maximum_minor(matrix),
        "singular_values": [float(value) for value in singular_values],
    }


def main() -> None:
    table = overlap_table()
    audits = [
        audit_shift(1, 1, table),
        audit_shift(0, -1, table),
    ]
    if any(
        audit["idempotency_residual"] > 1e-8
        or audit["maximum_minor_residual"] > 1e-8
        for audit in audits
    ):
        raise AssertionError("one of the two d=7 shift audits failed")
    print(
        json.dumps(
            {
                "schema": "sic-stark-dimension-seven-shifts-v1",
                "dimension": DIMENSION,
                "audits": audits,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
