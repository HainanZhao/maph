#!/usr/bin/env python3
"""Exact Heisenberg descents behind the dimension-six cyclic route.

For a level-N finite Heisenberg representation, Weyl labels u,v with
det(u,v)=N/6 have commutator a primitive sixth root.  If their sixth
powers generate an abelian subgroup of order N/6, the trivial joint
eigenspace has dimension six and carries the standard level-six Weyl
representation.

Two invariant lattices occur naturally in the d=6 problem:

* N=24, with lattice 2*O_K of index 4;
* N=504, with lattice (2*sqrt(21))*O_K of index 84.

Both lattices are preserved by L and A=L^3.  This script certifies the
indices, commutator phases, central subgroup orders, and block
dimensions using only exact integer arithmetic.
"""

from __future__ import annotations

import json
import math


DIMENSION = 6
L_MATRIX = ((5, -1), (1, 0))
A_MATRIX = ((115, -24), (24, -5))
IDENTITY = ((1, 0), (0, 1))


def matrix_add(
    left: tuple[tuple[int, int], tuple[int, int]],
    right: tuple[tuple[int, int], tuple[int, int]],
) -> tuple[tuple[int, int], tuple[int, int]]:
    return tuple(
        tuple(left[row][column] + right[row][column] for column in range(2))
        for row in range(2)
    )


def matrix_scale(
    scalar: int,
    matrix: tuple[tuple[int, int], tuple[int, int]],
) -> tuple[tuple[int, int], tuple[int, int]]:
    return tuple(
        tuple(scalar * matrix[row][column] for column in range(2))
        for row in range(2)
    )


def matrix_multiply(
    left: tuple[tuple[int, int], tuple[int, int]],
    right: tuple[tuple[int, int], tuple[int, int]],
) -> tuple[tuple[int, int], tuple[int, int]]:
    return tuple(
        tuple(
            sum(left[row][middle] * right[middle][column] for middle in range(2))
            for column in range(2)
        )
        for row in range(2)
    )


def determinant(
    matrix: tuple[tuple[int, int], tuple[int, int]],
) -> int:
    return (
        matrix[0][0] * matrix[1][1]
        - matrix[0][1] * matrix[1][0]
    )


def smith_invariants(
    matrix: tuple[tuple[int, int], tuple[int, int]],
) -> tuple[int, int]:
    first = math.gcd(*(abs(entry) for row in matrix for entry in row))
    second = abs(determinant(matrix)) // first
    assert second % first == 0
    return first, second


def image_order_modulus(
    matrix: tuple[tuple[int, int], tuple[int, int]],
    modulus: int,
) -> int:
    first, second = smith_invariants(matrix)
    return (
        modulus // math.gcd(modulus, first)
    ) * (
        modulus // math.gcd(modulus, second)
    )


def descent_record(
    *,
    level: int,
    lattice: tuple[tuple[int, int], tuple[int, int]],
    name: str,
) -> dict[str, object]:
    index = abs(determinant(lattice))
    assert index == level // DIMENSION
    assert matrix_multiply(L_MATRIX, lattice) == matrix_multiply(
        lattice,
        L_MATRIX,
    )
    assert matrix_multiply(A_MATRIX, lattice) == matrix_multiply(
        lattice,
        A_MATRIX,
    )

    # If X=D_(column 1), Y=D_(column 2), their commutator is the
    # level-N root to the determinant of the label matrix.
    commutator_exponent = determinant(lattice) % level
    assert math.gcd(commutator_exponent, level) == index
    assert level // math.gcd(commutator_exponent, level) == DIMENSION

    central_lattice = matrix_scale(DIMENSION, lattice)
    central_order = image_order_modulus(central_lattice, level)
    assert central_order == index
    block_dimension = level // central_order
    assert block_dimension == DIMENSION

    return {
        "name": name,
        "ambient_heisenberg_level": level,
        "invariant_lattice": [list(row) for row in lattice],
        "lattice_smith_invariants": list(smith_invariants(lattice)),
        "lattice_index": index,
        "lattice_preserved_by_L": True,
        "lattice_preserved_by_A": True,
        "weyl_commutator_exponent_mod_level": commutator_exponent,
        "weyl_commutator_order": DIMENSION,
        "sixth_power_central_lattice": [
            list(row) for row in central_lattice
        ],
        "sixth_power_central_smith_invariants": list(
            smith_invariants(central_lattice)
        ),
        "sixth_power_central_subgroup_order": central_order,
        "trivial_central_character_block_dimension": block_dimension,
        "trivial_central_character_preserved_by_L": True,
        "trivial_central_character_preserved_by_A": True,
    }


def main() -> None:
    assert matrix_multiply(
        matrix_multiply(L_MATRIX, L_MATRIX),
        L_MATRIX,
    ) == A_MATRIX

    level_24_lattice = matrix_scale(2, IDENTITY)

    # beta has matrix L, so multiplication by
    # 2*sqrt(21)=4*beta-10 is represented by 4L-10I.
    level_504_lattice = matrix_add(
        matrix_scale(4, L_MATRIX),
        matrix_scale(-10, IDENTITY),
    )
    assert level_504_lattice == ((10, -4), (4, -10))
    assert determinant(level_504_lattice) == -84

    records = [
        descent_record(
            level=24,
            lattice=level_24_lattice,
            name="native_modular_level_2O_K",
        ),
        descent_record(
            level=504,
            lattice=level_504_lattice,
            name="inter_level_2sqrt21_O_K",
        ),
    ]
    # In the standard level-24 clock/shift model, the trivial central
    # block has the explicit basis
    #
    #   v_a = |2a> + |2a+12>,  a mod 6.
    #
    # The two-step shift sends v_a to v_(a+1), while the square of the
    # clock has eigenvalue zeta_24^(4a)=zeta_6^a.  This is the standard
    # six-dimensional Weyl representation (up to the harmless choice of
    # commutator orientation).
    level_24_basis_supports = [
        [2 * index, 2 * index + 12]
        for index in range(DIMENSION)
    ]
    assert all(
        sorted(
            [
            (support + 2) % 24
            for support in level_24_basis_supports[index]
            ]
        )
        == level_24_basis_supports[(index + 1) % DIMENSION]
        for index in range(DIMENSION)
    )
    assert all(
        (4 * index) % 24 == 4 * index
        for index in range(DIMENSION)
    )
    result = {
        "schema": "sic-stark-dimension-six-heisenberg-descent-v1",
        "field": "Q(sqrt(21))",
        "zauner_matrix": [list(row) for row in L_MATRIX],
        "stabilizer": [list(row) for row in A_MATRIX],
        "records": records,
        "common_block_dimension": DIMENSION,
        "level_24_trivial_block": {
            "basis_supports": level_24_basis_supports,
            "two_step_shift_action": "v_a -> v_(a+1)",
            "clock_square_action": "v_a -> zeta_6^a*v_a",
        },
        "finite_weyl_bridge_exists": True,
        "analytic_operator_restriction_identified": False,
        "conclusion": (
            "The native level-24 modular representation and the fixed "
            "index-504 inter-level correspondence both contain a "
            "canonical six-dimensional trivial-central-character block "
            "carrying the level-six Weyl commutator and preserved by L "
            "and A.  Closing TCC now requires proving that the "
            "regularized Shintani--Faddeev transfer operator preserves "
            "one of these blocks and restricts to the AFK ghost."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
