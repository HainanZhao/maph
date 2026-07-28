#!/usr/bin/env python3
"""Exact rank audit for the conductor-three to conductor-six lifts.

The double-sine duplication formula splits the known conductor-three
invariant into four conductor-six orbit products.  This script verifies
the four distinct orbits and proves by rational linear algebra that the
single distribution relation cannot determine any selected lift.
"""

from __future__ import annotations

from fractions import Fraction
import json


Point = tuple[int, int]


def step(point: Point, modulus: int) -> Point:
    a, b = point
    return ((5 * a + b) % modulus, (-a) % modulus)


def orbit(start: Point, modulus: int) -> tuple[Point, ...]:
    result: list[Point] = []
    current = start
    while current not in result:
        result.append(current)
        current = step(current, modulus)
    if current != start:
        raise AssertionError("orbit failed to close at its initial point")
    return tuple(result)


def matrix_rank(rows: list[list[Fraction]]) -> int:
    matrix = [row[:] for row in rows]
    if not matrix:
        return 0
    row_count = len(matrix)
    column_count = len(matrix[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(pivot_row, row_count)
                if matrix[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / scale for entry in matrix[pivot_row]]
        for row in range(row_count):
            if row == pivot_row:
                continue
            coefficient = matrix[row][column]
            if coefficient:
                matrix[row] = [
                    entry - coefficient * pivot_entry
                    for entry, pivot_entry in zip(
                        matrix[row], matrix[pivot_row]
                    )
                ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def main() -> None:
    starts = ((0, 1), (0, 4), (3, 1), (3, 4))
    lifts = tuple(orbit(start, 6) for start in starts)
    expected = (
        ((0, 1), (1, 0), (5, 5)),
        ((0, 4), (4, 0), (2, 2)),
        ((3, 1), (4, 3), (5, 2)),
        ((3, 4), (1, 3), (2, 5)),
    )
    assert lifts == expected
    lower_orbit = orbit((0, 1), 3)
    assert all(
        tuple((a % 3, b % 3) for a, b in lift) == lower_orbit
        for lift in lifts
    )

    # In logarithmic coordinates ell_j=log(P_{6,j}), duplication gives
    # log(P_3)=ell_1+ell_2+ell_3+ell_4.  Its coefficient matrix has rank
    # one; adjoining any selected coordinate functional raises the rank,
    # so that coordinate is not determined by the distribution relation.
    distribution = [[Fraction(1)] * 4]
    distribution_rank = matrix_rank(distribution)
    selected_coordinate = [[Fraction(1), Fraction(0), Fraction(0), Fraction(0)]]
    augmented_rank = matrix_rank(distribution + selected_coordinate)
    assert distribution_rank == 1
    assert augmented_rank == 2

    null_directions = (
        (1, -1, 0, 0),
        (1, 0, -1, 0),
        (1, 0, 0, -1),
    )
    assert all(sum(direction) == 0 for direction in null_directions)
    assert any(direction[0] != 0 for direction in null_directions)

    print(
        json.dumps(
            {
                "schema": "sic-stark-dimension-six-lift-obstruction-v1",
                "lower_orbit": lower_orbit,
                "lift_orbits": lifts,
                "distribution_relation": (
                    "log(P3)=log(P6_1)+log(P6_2)+log(P6_3)+log(P6_4)"
                ),
                "distribution_matrix_rank": distribution_rank,
                "augmented_with_selected_coordinate_rank": augmented_rank,
                "nullspace_dimension": 3,
                "selected_lift_determined": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
