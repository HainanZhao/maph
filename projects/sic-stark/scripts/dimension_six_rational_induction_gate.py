#!/usr/bin/env python3
"""Exact rational-character obstruction for the primitive d=6 packet.

The primitive ray characters are chi_1 and chi_5 on C_6.  Every
Q-valued character is fixed by inversion, so rational-character
Artin induction can see chi_1 + chi_5 but not chi_1 - chi_5.  This
script verifies that statement by exact linear algebra over Q.
"""

from __future__ import annotations

from fractions import Fraction


Vector = tuple[Fraction, ...]


def rank(rows: list[Vector]) -> int:
    matrix = [list(row) for row in rows]
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
                if matrix[row][column]
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
            multiple = matrix[row][column]
            if multiple:
                matrix[row] = [
                    entry - multiple * pivot_entry
                    for entry, pivot_entry in zip(
                        matrix[row], matrix[pivot_row], strict=True
                    )
                ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def add(left: Vector, right: Vector) -> Vector:
    return tuple(a + b for a, b in zip(left, right, strict=True))


def subtract(left: Vector, right: Vector) -> Vector:
    return tuple(a - b for a, b in zip(left, right, strict=True))


def main() -> None:
    # Values are represented in Q(sqrt(-3)) as separate rational and
    # sqrt(-3) coefficient vectors.  zeta_6 = (1 + sqrt(-3))/2.
    chi_one_real = (
        Fraction(1),
        Fraction(1, 2),
        Fraction(-1, 2),
        Fraction(-1),
        Fraction(-1, 2),
        Fraction(1, 2),
    )
    chi_one_imaginary = (
        Fraction(0),
        Fraction(1, 2),
        Fraction(1, 2),
        Fraction(0),
        Fraction(-1, 2),
        Fraction(-1, 2),
    )
    chi_five_real = chi_one_real
    chi_five_imaginary = tuple(-entry for entry in chi_one_imaginary)

    primitive_even = add(chi_one_real, chi_five_real)
    primitive_odd = subtract(chi_one_imaginary, chi_five_imaginary)

    rational_irreducibles = [
        # chi_0
        tuple(Fraction(1) for _ in range(6)),
        # chi_3
        tuple(Fraction((-1) ** exponent) for exponent in range(6)),
        # chi_1 + chi_5
        primitive_even,
        # chi_2 + chi_4
        (
            Fraction(2),
            Fraction(-1),
            Fraction(-1),
            Fraction(2),
            Fraction(-1),
            Fraction(-1),
        ),
    ]

    inversion_pairs = ((1, 5), (2, 4))
    for index, character in enumerate(rational_irreducibles):
        for left, right in inversion_pairs:
            if character[left] != character[right]:
                raise AssertionError(
                    f"rational character {index} is not inversion invariant"
                )

    rational_rank = rank(rational_irreducibles)
    even_augmented_rank = rank(rational_irreducibles + [primitive_even])
    odd_augmented_rank = rank(rational_irreducibles + [primitive_odd])

    if rational_rank != 4:
        raise AssertionError(f"unexpected rational character rank {rational_rank}")
    if even_augmented_rank != rational_rank:
        raise AssertionError("primitive even packet escaped rational span")
    if odd_augmented_rank != rational_rank + 1:
        raise AssertionError("primitive odd packet lies in rational span")

    # The orientation functional extracts the inversion-odd coordinate.
    # It annihilates every Q-valued character and not chi_1 - chi_5.
    orientation_functional = (
        Fraction(0),
        Fraction(1),
        Fraction(0),
        Fraction(0),
        Fraction(0),
        Fraction(-1),
    )

    def dot(left: Vector, right: Vector) -> Fraction:
        return sum(
            (a * b for a, b in zip(left, right, strict=True)),
            start=Fraction(0),
        )

    rational_orientation_values = [
        dot(orientation_functional, character)
        for character in rational_irreducibles
    ]
    primitive_odd_orientation = dot(orientation_functional, primitive_odd)
    if any(rational_orientation_values):
        raise AssertionError("rational character detected orientation")
    if primitive_odd_orientation == 0:
        raise AssertionError("orientation functional missed primitive odd packet")

    print("RATIONAL_CHARACTER_BASIS_RANK=4")
    print("PRIMITIVE_EVEN_PACKET_IN_RATIONAL_SPAN=1")
    print("PRIMITIVE_ODD_PACKET_IN_RATIONAL_SPAN=0")
    print(f"RATIONAL_ORIENTATION_VALUES={rational_orientation_values}")
    print(f"PRIMITIVE_ODD_ORIENTATION={primitive_odd_orientation}")
    print("RATIONAL_ARTIN_INDUCTION_CAN_ORIENT_CHI_1=0")


if __name__ == "__main__":
    main()
