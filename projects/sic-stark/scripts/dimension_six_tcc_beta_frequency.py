#!/usr/bin/env python3
"""Match d=6 TCC output frequencies to helical beta-transform labels.

With <p,q>=p_2 q_1-p_1 q_2 and

    L=[[5,-1],[1,0]],

the shift-one TCC character is

    omega_6^<p,(I+L)q>
      = omega_6^(-u*a-(u+v)*b),

while shift zero gives

    omega_6^<p,Lq>
      = omega_6^(-(u+v)*a-v*b).

The helical dual map sends a beta mode (N,ell) to finite frequencies

    p_a = N-2,  p_b=ell  (mod 6),

because n=5(N-2) and p_a=-n modulo six.  This script proves that the
resulting label maps are bijections for both formal TCC shifts.
"""

from __future__ import annotations

import json


DIMENSION = 6
L_MATRIX = ((5, -1), (1, 0))
IDENTITY = ((1, 0), (0, 1))


def matrix_add(
    left: tuple[tuple[int, int], tuple[int, int]],
    right: tuple[tuple[int, int], tuple[int, int]],
) -> tuple[tuple[int, int], tuple[int, int]]:
    return tuple(
        tuple(
            left[row][column] + right[row][column]
            for column in range(2)
        )
        for row in range(2)
    )


def matrix_vector(
    matrix: tuple[tuple[int, int], tuple[int, int]],
    vector: tuple[int, int],
) -> tuple[int, int]:
    return (
        matrix[0][0] * vector[0] + matrix[0][1] * vector[1],
        matrix[1][0] * vector[0] + matrix[1][1] * vector[1],
    )


def symplectic(
    left: tuple[int, int],
    right: tuple[int, int],
) -> int:
    return left[1] * right[0] - left[0] * right[1]


def frequency_coefficients(
    output: tuple[int, int],
    matrix: tuple[tuple[int, int], tuple[int, int]],
) -> tuple[int, int]:
    base = symplectic(output, matrix_vector(matrix, (0, 0)))
    first = (
        symplectic(output, matrix_vector(matrix, (1, 0))) - base
    ) % DIMENSION
    second = (
        symplectic(output, matrix_vector(matrix, (0, 1))) - base
    ) % DIMENSION
    return first, second


def beta_labels(frequency: tuple[int, int]) -> tuple[int, int]:
    first_frequency, second_frequency = frequency
    return (
        (first_frequency + 2) % DIMENSION,
        second_frequency,
    )


def main() -> None:
    shift_matrices = {
        "0": L_MATRIX,
        "1": matrix_add(IDENTITY, L_MATRIX),
    }
    records: dict[str, list[dict[str, object]]] = {}
    for shift, matrix in shift_matrices.items():
        shift_records = []
        seen_frequencies: set[tuple[int, int]] = set()
        seen_beta_labels: set[tuple[int, int]] = set()
        for first_output in range(DIMENSION):
            for second_output in range(DIMENSION):
                output = (first_output, second_output)
                frequency = frequency_coefficients(output, matrix)
                labels = beta_labels(frequency)
                seen_frequencies.add(frequency)
                seen_beta_labels.add(labels)
                shift_records.append(
                    {
                        "tcc_output": list(output),
                        "finite_frequency_a_b": list(frequency),
                        "beta_N_mod_6": labels[0],
                        "helical_ell_mod_6": labels[1],
                    }
                )
        assert len(seen_frequencies) == DIMENSION * DIMENSION
        assert len(seen_beta_labels) == DIMENSION * DIMENSION
        records[shift] = shift_records

    # Closed formulas.
    for record in records["1"]:
        first_output, second_output = record["tcc_output"]
        assert record["finite_frequency_a_b"] == [
            (-first_output) % DIMENSION,
            (-first_output - second_output) % DIMENSION,
        ]
        assert record["beta_N_mod_6"] == (
            2 - first_output
        ) % DIMENSION
        assert record["helical_ell_mod_6"] == (
            -first_output - second_output
        ) % DIMENSION
    for record in records["0"]:
        first_output, second_output = record["tcc_output"]
        assert record["finite_frequency_a_b"] == [
            (-first_output - second_output) % DIMENSION,
            (-second_output) % DIMENSION,
        ]
        assert record["beta_N_mod_6"] == (
            2 - first_output - second_output
        ) % DIMENSION
        assert record["helical_ell_mod_6"] == (
            -second_output
        ) % DIMENSION

    result = {
        "schema": "sic-stark-dimension-six-tcc-beta-frequency-v1",
        "symplectic_convention": "<p,q>=p2*q1-p1*q2",
        "helical_beta_frequency_map": (
            "(N,ell)->(N-2,ell) mod 6"
        ),
        "shift_one_closed_map": (
            "(u,v)->(N,ell)=(2-u,-u-v) mod 6"
        ),
        "shift_zero_closed_map": (
            "(u,v)->(N,ell)=(2-u-v,-v) mod 6"
        ),
        "records": records,
        "shift_one_map_is_bijective": True,
        "shift_zero_map_is_bijective": True,
        "conclusion": (
            "The specialized beta transform covers exactly the 36 "
            "Fourier characters required by each formal TCC shift.  "
            "There is no remaining frequency, sign, or label mismatch; "
            "the sole analytic task is evaluation of the helical alias "
            "sum at these residue classes."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
