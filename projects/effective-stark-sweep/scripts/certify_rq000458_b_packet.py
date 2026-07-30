#!/usr/bin/env python3
"""Independent Engine-B Arb certificate for the RQ-000458 packet.

The one-place ray group is C4 x C2.  The Engine-C-aligned packet is
the Fourier component supported on [1,1] and [3,1].  We first enclose
all eight Shintani differenced class logs from exact cone data, then
apply the exact projector

    log X_(a,packet2) = (log X_(a,0) - log X_(a,1))/2.

The fundamental positive unit 15+4*sqrt(14) has order four modulo the
finite ideal, so every ray-class domain is the exact union of four
adjacent fundamental-unit cones.  No PARI L-value or Engine-C unit
enters this certificate.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from math import gcd

from flint import arb, ctx, fmpz_poly

from certified_taylor_quadrature import certified_taylor
from certify_q14_p7_packet import fundamental_log_double_sine as _unused
from certify_q7_p7_packet import (
    arb_fraction,
    near_integrand,
    product,
    tail_integrand,
)


SAFE_EXPONENT = 1152
UNIT_ORDER = 4
CONE_MATRICES = [
    ((2, 2), (-1, 1)),
    ((1, 3), (-3, 11)),
    ((-20, -600), (103, 3089)),
    ((-16, -484), (21, 635)),
    ((-4, -120), (39, 1169)),
    ((1, 3), (-1, 17)),
    ((-5, -151), (9, 271)),
    ((-20, -600), (47, 1409)),
]
UNIT_ACTION_MATRICES = [
    ((15, 28), (8, 15)),
    ((15, 4), (56, 15)),
    ((-73, -20), (376, 103)),
    ((-689, -548), (904, 719)),
    ((-9, -4), (88, 39)),
    ((7, 4), (40, 23)),
    ((-49, -44), (88, 79)),
    ((-17, -20), (40, 47)),
]
AFFINE_SHIFT = (Fraction(1, 12), Fraction(0))


def determinant(matrix: tuple[tuple[int, int], tuple[int, int]]) -> int:
    return (
        matrix[0][0] * matrix[1][1]
        - matrix[0][1] * matrix[1][0]
    )


def matrix_vector(
    matrix: tuple[tuple[int, int], tuple[int, int]],
    vector: tuple[int, int],
) -> tuple[int, int]:
    return (
        matrix[0][0] * vector[0] + matrix[0][1] * vector[1],
        matrix[1][0] * vector[0] + matrix[1][1] * vector[1],
    )


def adjacent_cone_matrix(
    class_code: int,
    unit_step: int,
) -> tuple[tuple[int, int], tuple[int, int]]:
    base = CONE_MATRICES[class_code]
    first = (base[0][0], base[1][0])
    second = (base[0][1], base[1][1])
    action = UNIT_ACTION_MATRICES[class_code]
    for _ in range(unit_step):
        first = matrix_vector(action, first)
        second = matrix_vector(action, second)
    return ((first[0], second[0]), (first[1], second[1]))


def quotient_generator(
    matrix: tuple[tuple[int, int], tuple[int, int]],
    signed_determinant: int,
) -> tuple[int, int]:
    modulus = abs(signed_determinant)
    for bound in range(1, 8):
        for first in range(-bound, bound + 1):
            for second in range(-bound, bound + 1):
                if (first, second) == (0, 0):
                    continue
                first_coordinate = Fraction(
                    matrix[1][1] * first
                    - matrix[0][1] * second,
                    signed_determinant,
                )
                second_coordinate = Fraction(
                    -matrix[1][0] * first
                    + matrix[0][0] * second,
                    signed_determinant,
                )
                order = (
                    first_coordinate.denominator
                    * second_coordinate.denominator
                    // gcd(
                        first_coordinate.denominator,
                        second_coordinate.denominator,
                    )
                )
                if order == modulus:
                    return first, second
    raise RuntimeError("no cyclic quotient generator found")


def mod_one_upper(value: Fraction) -> Fraction:
    remainder = value - value.numerator // value.denominator
    return Fraction(1) if remainder == 0 else remainder


def cone_points(
    class_code: int,
    unit_step: int,
) -> list[tuple[Fraction, Fraction]]:
    matrix = adjacent_cone_matrix(class_code, unit_step)
    signed_determinant = determinant(matrix)
    modulus = abs(signed_determinant)
    if modulus not in (4, 20):
        raise RuntimeError("frozen cone determinant changed")
    generator = quotient_generator(matrix, signed_determinant)
    points = []
    for residue in range(modulus):
        vector_first = AFFINE_SHIFT[0] + residue * generator[0]
        vector_second = AFFINE_SHIFT[1] + residue * generator[1]
        x_value = Fraction(
            matrix[1][1] * vector_first
            - matrix[0][1] * vector_second,
            signed_determinant,
        )
        y_value = Fraction(
            -matrix[1][0] * vector_first
            + matrix[0][0] * vector_second,
            signed_determinant,
        )
        points.append((mod_one_upper(x_value), mod_one_upper(y_value)))
    if len(points) != modulus or len(set(points)) != modulus:
        raise RuntimeError("affine cone enumeration is incomplete")
    return sorted(points)


def fast_log_double_sine(
    argument: arb,
    beta: arb,
    tolerance: Fraction,
) -> tuple[arb, int]:
    """The Q(sqrt(14)) proof with validated order-12 quadrature."""

    linear = beta + 1 - 2 * argument
    if linear.contains(0) and abs(linear).upper() < arb_fraction(tolerance):
        return arb(0), 0
    delta = Fraction(1, 1_000_000)
    exponential_majorant = Fraction(100_002, 100_000)
    numerator_remainder = Fraction(31**4, 1920) * exponential_majorant
    denominator_remainder = (
        Fraction(30**4, 1920) * exponential_majorant
        + Fraction(1, 1920) * exponential_majorant
        + Fraction(30**2, 24)
        * Fraction(1, 24)
        * exponential_majorant**2
    )
    denominator_increment = (
        Fraction(30**2 + 1, 24) * exponential_majorant
        + Fraction(30**2, 24)
        * Fraction(1, 24)
        * exponential_majorant**2
        * delta**2
    )
    coefficient_majorant = Fraction(31**2 + 30**2 + 1, 24)
    second_order_majorant = Fraction(8000)
    if not (
        Fraction(1, 1 - Fraction(31, 2_000_000))
        < exponential_majorant
        and numerator_remainder < 482
        and denominator_remainder < 425
        and denominator_increment < 38
        and 2
        * (
            Fraction(482)
            + Fraction(425)
            + coefficient_majorant * Fraction(38)
        )
        < second_order_majorant
    ):
        raise RuntimeError("large-period Taylor majorant check failed")
    if not (
        abs(linear) < 31
        and beta > 29
        and beta < 30
        and argument > 0
        and beta + 1 - argument > 0
    ):
        raise RuntimeError("large-period analytic hypotheses failed")

    zero_value = linear * (linear**2 - beta**2 - 1) / (24 * beta)
    zero_remainder = second_order_majorant * delta**3 / 3
    near_value = zero_value * arb_fraction(delta)
    near_value += arb(0, arb_fraction(zero_remainder).upper())

    near_function = near_integrand(argument, beta)
    segment_left = delta
    panels = 0
    while segment_left < 1:
        segment_right = min(Fraction(1), 4 * segment_left)
        segment = certified_taylor(
            near_function,
            segment_left,
            segment_right,
            tolerance * (segment_right - segment_left) / 8,
        )
        near_value += segment.value
        panels += segment.panels
        segment_left = segment_right

    cutoff = Fraction(64)
    tail = certified_taylor(
        tail_integrand(argument, beta),
        Fraction(0),
        cutoff,
        tolerance / 4,
    )
    exp_three_partial = sum(
        Fraction(3**index, product(range(1, index + 1)))
        for index in range(9)
    )
    if not exp_three_partial > 20:
        raise RuntimeError("tail exponential majorant check failed")
    tail_remainder = (-arb_fraction(cutoff)).exp() / 16
    tail_value = tail.value + arb(0, tail_remainder.upper())
    boundary = -linear / beta
    return near_value + boundary + tail_value, panels + tail.panels


def class_log_value(
    class_code: int,
    beta: arb,
    tolerance: Fraction,
) -> tuple[arb, int, int]:
    value = arb(0)
    panels = 0
    point_count = 0
    for unit_step in range(UNIT_ORDER):
        points = cone_points(class_code, unit_step)
        point_count += len(points)
        for x_value, y_value in points:
            argument = arb_fraction(x_value) + arb_fraction(y_value) * beta
            term, used = fast_log_double_sine(
                argument,
                beta,
                tolerance / (UNIT_ORDER * len(points)),
            )
            value += term
            panels += used
    return 2 * value, panels, point_count


def voutier_lower_bound() -> arb:
    bounds = []
    for degree in range(3, 17):
        degree_ball = arb(degree)
        bounds.append(
            (degree_ball.log().log() / degree_ball.log()) ** 3
            / (4 * degree)
        )
    return arb(min(bound.lower() for bound in bounds))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--digits", type=int, default=90)
    parser.add_argument("--tolerance", default="1e-10")
    arguments = parser.parse_args()
    tolerance = Fraction(arguments.tolerance)
    ctx.dps = arguments.digits
    ctx.cap = 16
    beta = 15 + 4 * arb(14).sqrt()

    full_logs = []
    total_panels = 0
    for class_code in range(8):
        value, panels, point_count = class_log_value(
            class_code, beta, tolerance
        )
        full_logs.append(value)
        total_panels += panels
        print(f"CLASS_{class_code}_ADJACENT_CONES={UNIT_ORDER}")
        print(f"CLASS_{class_code}_CONE_POINTS={point_count}")
        print(f"CLASS_{class_code}_FULL_ANALYTIC_LOG={value}")

    projected_logs = [
        (full_logs[first_log] - full_logs[first_log + 4]) / 2
        for first_log in range(4)
    ]

    absolute = fmpz_poly(
        [1, -40, 172, 488, 694, 488, 172, -40, 1]
    )
    roots = [
        root.real
        for root, multiplicity in absolute.complex_roots()
        if multiplicity == 1 and root.imag.contains(0) and root.real > 0
    ]
    windows = [
        (Fraction(130, 1000), Fraction(131, 1000)),
        (Fraction(34605, 1000), Fraction(34606, 1000)),
        (Fraction(7685, 1000), Fraction(7686, 1000)),
        (Fraction(28, 1000), Fraction(29, 1000)),
    ]
    candidates = []
    for left, right in windows:
        selected = [
            root
            for root in roots
            if root > arb_fraction(left) and root < arb_fraction(right)
        ]
        if len(selected) != 1:
            raise RuntimeError(
                f"window [{left},{right}] selected {len(selected)} roots"
            )
        candidates.append(selected[0])

    maximum_difference = arb(0)
    for first_log, (analytic, candidate) in enumerate(
        zip(projected_logs, candidates, strict=True)
    ):
        difference = analytic - candidate.log()
        if not difference.contains(0):
            raise RuntimeError(
                f"packet class {first_log}: disjoint balls {difference}"
            )
        maximum_difference = max(
            maximum_difference, arb(abs(difference).upper())
        )
        print(f"PACKET2_CLASS_{first_log}_PROJECTED_LOG={analytic}")
        print(f"PACKET2_CLASS_{first_log}_ALGEBRAIC_ROOT={candidate}")
        print(f"PACKET2_CLASS_{first_log}_LOG_DIFFERENCE={difference}")

    powered_height_upper = SAFE_EXPONENT * maximum_difference
    voutier = voutier_lower_bound()
    margin = voutier / powered_height_upper
    quadratic_fallback = ((1 + arb(5).sqrt()) / 2).log() / 2
    if not (margin > 100 and quadratic_fallback > powered_height_upper):
        raise RuntimeError("height-rigidity margin did not clear")

    print("CASE_ID=RQ-000458")
    print("ENGINE=B")
    print("RAY_STRUCTURE=[4,2]")
    print("PROJECTOR_CHARACTERS=[[1,1],[3,1]]")
    print("UNIT_ORDER_MOD_FINITE=4")
    print(f"TOTAL_TAYLOR_PANELS={total_panels}")
    print(f"SHINTANI_SAFE_EXPONENT={SAFE_EXPONENT}")
    print(f"POWERED_HEIGHT_UPPER={powered_height_upper}")
    print(f"VOUTIER_DEGREE_3_TO_16_LOWER={voutier}")
    print(f"VOUTIER_MARGIN={margin}")
    print(f"QUADRATIC_HEIGHT_FALLBACK={quadratic_fallback}")
    print("DEGREE_1_FALLBACK=POSITIVE_RATIONAL_UNIT_IS_1")
    print("RQ000458_ENGINE_B_ANALYTIC_ARB_CERTIFIED=1")
    print("RQ000458_ENGINE_B_PACKET_IDENTITY_VERIFIED=1")
    print("CLAIM_TAG=VERIFIED")


if __name__ == "__main__":
    main()
