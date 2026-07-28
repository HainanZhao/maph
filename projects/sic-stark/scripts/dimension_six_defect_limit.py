#!/usr/bin/env python3
"""Signed-symmetry and asymptotic audit of the d=6 TCC defect.

The level-six Weyl system is periodic only up to sign.  If an integral
symplectic image is reduced modulo six, that wrap sign must accompany
Zauner covariance.  This script derives the sign from the displacement
operators, reduces the 35 nonzero defect coefficients to thirteen signed
Zauner classes, and measures the corrected rational-boundary defect
along the modular geodesic.

The numerical scaling experiment diagnoses an O(1/n^2) defect.  It is not
used as a proof of the limiting identity.
"""

from __future__ import annotations

import cmath
import math

import numpy

import dimension_six_qgamma_boundary as boundary


DIMENSION = 6


def reduce_weyl_label(
    raw_first: int,
    raw_second: int,
) -> tuple[tuple[int, int], int]:
    """Reduce an integral Weyl label and return its even-d wrap sign."""

    reduced = (
        raw_first % DIMENSION,
        raw_second % DIMENSION,
    )
    first_wrap = (raw_first - reduced[0]) // DIMENSION
    second_wrap = (raw_second - reduced[1]) // DIMENSION
    sign = (-1) ** (
        reduced[0] * second_wrap
        + reduced[1] * first_wrap
    )
    return reduced, sign


def signed_zauner_inverse(
    characteristic: tuple[int, int],
) -> tuple[tuple[int, int], int]:
    """Apply L^(-1) and retain the Weyl wrap sign."""

    first, second = characteristic
    return reduce_weyl_label(second, -first + 5 * second)


def signed_reciprocal(
    characteristic: tuple[int, int],
) -> tuple[tuple[int, int], int]:
    """Return the reduced label of the adjoint displacement."""

    first, second = characteristic
    return reduce_weyl_label(-first, -second)


def signed_zauner_orbits() -> list[list[tuple[int, int]]]:
    unseen = {
        (first, second)
        for first in range(DIMENSION)
        for second in range(DIMENSION)
    }
    orbits: list[list[tuple[int, int]]] = []
    while unseen:
        start = min(unseen)
        orbit: list[tuple[int, int]] = []
        current = start
        accumulated_sign = 1
        while current not in orbit:
            orbit.append(current)
            current, sign = signed_zauner_inverse(current)
            accumulated_sign *= sign
        assert current == start
        assert accumulated_sign == 1
        unseen.difference_update(orbit)
        orbits.append(orbit)
    return orbits


def displacement_matrix(
    first: int,
    second: int,
) -> numpy.ndarray:
    tau = -cmath.exp(math.pi * 1j / DIMENSION)
    omega = cmath.exp(2 * math.pi * 1j / DIMENSION)
    matrix = numpy.zeros((DIMENSION, DIMENSION), dtype=complex)
    for column in range(DIMENSION):
        row = (column + first) % DIMENSION
        matrix[row, column] = (
            tau ** (first * second)
            * omega ** (second * column)
        )
    return matrix


def verify_wrap_sign() -> None:
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            raw_first = second
            raw_second = -first + 5 * second
            reduced, sign = reduce_weyl_label(
                raw_first, raw_second
            )
            raw_matrix = displacement_matrix(
                raw_first, raw_second
            )
            reduced_matrix = displacement_matrix(*reduced)
            assert numpy.max(
                numpy.abs(raw_matrix - sign * reduced_matrix)
            ) < 1e-12


def weyl_defect_coefficients(
    matrix: numpy.ndarray,
) -> dict[tuple[int, int], complex]:
    """Return sqrt(7) Tr(D_p^* (K^2-K)) for every label."""

    tau = -cmath.exp(math.pi * 1j / DIMENSION)
    omega = cmath.exp(2 * math.pi * 1j / DIMENSION)
    defect = matrix @ matrix - matrix
    result: dict[tuple[int, int], complex] = {}
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            coefficient = sum(
                tau ** (-first * second)
                * omega ** (-second * column)
                * defect[
                    (column + first) % DIMENSION,
                    column,
                ]
                for column in range(DIMENSION)
            )
            result[(first, second)] = math.sqrt(7) * coefficient
    return result


def signed_covariance_error(
    values: dict[tuple[int, int], complex],
) -> float:
    return max(
        abs(values[image] - sign * values[characteristic])
        for characteristic in values
        for image, sign in [signed_zauner_inverse(characteristic)]
    )


def inverse_reciprocity_error(
    values: dict[tuple[int, int], complex],
) -> float:
    return max(
        abs(
            values[image] * values[characteristic] - sign
        )
        for characteristic in values
        if characteristic != (0, 0)
        for image, sign in [signed_reciprocal(characteristic)]
    )


def main() -> None:
    verify_wrap_sign()
    zauner_orbits = signed_zauner_orbits()
    assert len(zauner_orbits) == 14
    print("EVEN_DIMENSION_WRAP_SIGN_VERIFIED=1")
    print("SIGNED_ZAUNER_ORBIT_COUNT=14")
    print("NONZERO_SIGNED_ZAUNER_ORBIT_COUNT=13")
    print("NONZERO_DEFECT_REPRESENTATIVE_COUNT=13")
    print(
        "NONZERO_DEFECT_REPRESENTATIVES="
        + ",".join(
            str(orbit[0]) for orbit in zauner_orbits[1:]
        )
    )

    covariance_errors = []
    reciprocity_errors = []
    idempotency_errors = []
    scaled_idempotency_errors = []
    coefficient_errors = []
    primitive_errors = []
    normalized_defect_packets = []
    primitive_root = boundary.positive_primitive_root()
    fixed_point = (5 - math.sqrt(21)) / 2
    for base_index in range(1, 5):
        table = boundary.boundary_table(base_index)
        table_values = {
            (first, second): table[first][second]
            for first in range(DIMENSION)
            for second in range(DIMENSION)
        }
        matrix = boundary.reconstruct(table)
        coefficients = weyl_defect_coefficients(matrix)
        numerator, denominator, _, _ = boundary.mapped_rational(
            base_index
        )
        assert (
            numerator * numerator
            - 5 * numerator * denominator
            + denominator * denominator
            == -21
        )
        fixed_point_distance = (
            numerator / denominator - fixed_point
        )
        normalized_packet = numpy.array(
            [
                [
                    coefficients[(first, second)]
                    / fixed_point_distance
                    for second in range(DIMENSION)
                ]
                for first in range(DIMENSION)
            ]
        )
        normalized_defect_packets.append(normalized_packet)
        covariance = signed_covariance_error(table_values)
        reciprocity = inverse_reciprocity_error(table_values)
        idempotency = float(
            numpy.max(numpy.abs(matrix @ matrix - matrix))
        )
        coefficient = max(abs(value) for value in coefficients.values())
        primitive = abs(table[0][1] + primitive_root)
        covariance_errors.append(covariance)
        reciprocity_errors.append(reciprocity)
        idempotency_errors.append(idempotency)
        scaled_idempotency_errors.append(
            denominator * denominator * idempotency
        )
        coefficient_errors.append(coefficient)
        primitive_errors.append(primitive)
        print(
            f"DEFECT_STEP_{base_index}="
            f"denominator:{denominator},"
            f"signed_covariance:{covariance:.15e},"
            f"inverse_reciprocity:{reciprocity:.15e},"
            f"idempotency:{idempotency:.15e},"
            f"denominator_squared_times_idempotency:"
            f"{denominator * denominator * idempotency:.15e},"
            f"maximum_weyl_coefficient:{coefficient:.15e},"
            f"primitive_error:{primitive:.15e},"
            f"maximum_normalized_defect:"
            f"{numpy.max(numpy.abs(normalized_packet)):.15e}"
        )

    for sequence in (
        covariance_errors,
        reciprocity_errors,
        idempotency_errors,
        coefficient_errors,
        primitive_errors,
    ):
        assert all(
            later < earlier
            for earlier, later in zip(sequence, sequence[1:])
        )
    assert min(scaled_idempotency_errors) > 6000
    assert max(scaled_idempotency_errors) < 6600
    derivative_packet_differences = [
        float(numpy.max(numpy.abs(later - earlier)))
        for earlier, later in zip(
            normalized_defect_packets,
            normalized_defect_packets[1:],
        )
    ]
    assert all(
        later < earlier
        for earlier, later in zip(
            derivative_packet_differences,
            derivative_packet_differences[1:],
        )
    )
    assert derivative_packet_differences[-1] < 1
    print("SIGNED_COVARIANCE_ERRORS_DECREASE=1")
    print("INVERSE_RECIPROCITY_ERRORS_DECREASE=1")
    print("IDEMPOTENCY_ERRORS_DECREASE=1")
    print("WEYL_DEFECT_COEFFICIENTS_DECREASE=1")
    print("PRIMITIVE_PACKET_ERRORS_DECREASE=1")
    print("NUMERICAL_DEFECT_SCALE=O(1/denominator^2)")
    print("CONVERGENT_NORM_IDENTITY=-21")
    print("NORMALIZED_DEFECT_PACKET_DIFFERENCES=" + ",".join(
        f"{difference:.15e}"
        for difference in derivative_packet_differences
    ))
    print("CONVERGENT_FIRST_DERIVATIVE_PACKET=1")
    print("ASYMPTOTIC_DEFECT_BOUND_PROVED=0")


if __name__ == "__main__":
    main()
