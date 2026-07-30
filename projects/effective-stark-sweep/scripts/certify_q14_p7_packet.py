#!/usr/bin/env python3
"""Independent Arb cone certificate for Q(sqrt(14)), p_7 infinity_2.

The ray generator is (3), the totally positive norm-one unit is
15+4*sqrt(14), and a positive cone generator for class (3)^r is
(7-sqrt(14))/3^r.  In coordinates for p_7/(3)^r the two cone rays have
matrix [[1,7],[-1,13]], of determinant 20.  Exact enumeration supplies
20 double-sine arguments per class.  No PARI L-value enters this file.
"""

from __future__ import annotations

import argparse
from fractions import Fraction

from flint import arb, arb_series, ctx, fmpz_poly

from certify_q7_p7_packet import (
    arb_fraction,
    certified_simpson,
    exponential,
    interval,
    near_integrand,
    product,
    sinh,
    tail_integrand,
)


SAFE_EXPONENT = 4032
MATRIX = ((1, 7), (-1, 13))
DETERMINANT = 20


def fundamental_log_double_sine(
    argument: arb,
    beta: arb,
    tolerance: Fraction,
) -> tuple[arb, int]:
    """Enclose log S_2(argument | 1,beta), for beta near 15+4sqrt(14)."""

    linear = beta + 1 - 2 * argument
    if linear.contains(0) and abs(linear).upper() < arb_fraction(tolerance):
        return arb(0), 0

    # The Q(sqrt(7)) certificate's Taylor proof is repeated with
    # |linear|<31 and beta<30.  For delta=10^-6,
    # exp(31*delta/2)<100002/100000.  Positive power-series
    # coefficients give the explicit remainder bounds below.
    delta = Fraction(1, 1_000_000)
    exponential_majorant = Fraction(100_002, 100_000)
    numerator_remainder = (
        Fraction(31**4, 1920) * exponential_majorant
    )
    denominator_remainder = (
        Fraction(30**4, 1920) * exponential_majorant
        + Fraction(1, 1920) * exponential_majorant
        + (
            Fraction(30**2, 24)
            * Fraction(1, 24)
            * exponential_majorant**2
        )
    )
    denominator_increment = (
        Fraction(30**2 + 1, 24) * exponential_majorant
        + (
            Fraction(30**2, 24)
            * Fraction(1, 24)
            * exponential_majorant**2
            * delta**2
        )
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
        and argument > arb(3) / 10
        and beta + 1 - argument > arb(3) / 10
    ):
        raise RuntimeError("large-period analytic hypotheses failed")

    zero_value = (
        linear * (linear**2 - beta**2 - 1) / (24 * beta)
    )
    zero_remainder = second_order_majorant * delta**3 / 3
    near_value = zero_value * arb_fraction(delta)
    near_value += arb(0, arb_fraction(zero_remainder).upper())

    near_function = near_integrand(argument, beta)
    segment_left = delta
    near_panels = 0
    while segment_left < 1:
        segment_right = min(Fraction(1), 4 * segment_left)
        segment = certified_simpson(
            near_function,
            segment_left,
            segment_right,
            tolerance * (segment_right - segment_left) / 8,
        )
        near_value += segment.value
        near_panels += segment.panels
        segment_left = segment_right

    cutoff = Fraction(64)
    tail = certified_simpson(
        tail_integrand(argument, beta),
        Fraction(0),
        cutoff,
        tolerance / 4,
    )
    # For v>=64 and 0.3<z<31, v/z+1>3.  The first nine
    # positive terms of exp(3) exceed 20, so both exponential
    # denominator factors have absolute value >19/20.  Since
    # v+z>64, each term is <1/32 and the difference is <1/16.
    exp_three_partial = sum(
        Fraction(3**index, 1) / product(range(1, index + 1))
        for index in range(9)
    )
    if not exp_three_partial > 20:
        raise RuntimeError("tail exponential majorant check failed")
    tail_remainder = (-arb_fraction(cutoff)).exp() / 16
    tail_value = tail.value + arb(0, tail_remainder.upper())
    boundary = -linear / beta
    return near_value + boundary + tail_value, near_panels + tail.panels


def cone_points(class_log: int) -> list[tuple[Fraction, Fraction]]:
    """Enumerate P(lambda,lambda*epsilon) intersect (1+b) exactly."""

    shift = Fraction(3**class_log, 7)
    points: list[tuple[Fraction, Fraction]] = []
    # In b-coordinates M=[[1,7],[-1,13]], so
    # M^-1=(1/20)[[13,-7],[1,1]].
    for first in range(-100, 101):
        for second in range(-100, 101):
            vector_first = shift + first
            vector_second = Fraction(second)
            x_value = (
                13 * vector_first - 7 * vector_second
            ) / DETERMINANT
            y_value = (
                vector_first + vector_second
            ) / DETERMINANT
            if 0 < x_value <= 1 and 0 < y_value <= 1:
                points.append((x_value, y_value))
    if len(points) != DETERMINANT:
        raise RuntimeError(
            f"class {class_log}: expected 20 cone points, got {len(points)}"
        )
    return sorted(points)


def verify_complement_symmetry(
    points: list[list[tuple[Fraction, Fraction]]],
) -> None:
    for class_log in range(3):
        complements = sorted(
            (1 - x_value, 1 - y_value)
            for x_value, y_value in points[class_log]
        )
        if complements != points[class_log + 3]:
            raise RuntimeError(
                f"cone complement symmetry failed for class {class_log}"
            )


def class_log_value(
    points: list[tuple[Fraction, Fraction]],
    beta: arb,
    tolerance: Fraction,
) -> tuple[arb, int]:
    result = arb(0)
    panels = 0
    for x_value, y_value in points:
        argument = arb_fraction(x_value) + arb_fraction(y_value) * beta
        value, used = fundamental_log_double_sine(
            argument, beta, tolerance / len(points)
        )
        result += value
        panels += used
    return 2 * result, panels


def voutier_lower_bound() -> arb:
    bounds = []
    for degree in range(3, 25):
        degree_ball = arb(degree)
        bounds.append(
            (degree_ball.log().log() / degree_ball.log()) ** 3
            / (4 * degree)
        )
    return arb(min(bound.lower() for bound in bounds))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--digits", type=int, default=80)
    parser.add_argument("--tolerance", default="1e-11")
    arguments = parser.parse_args()
    tolerance = Fraction(arguments.tolerance)
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")

    ctx.dps = arguments.digits
    ctx.cap = 6
    beta = 15 + 4 * arb(14).sqrt()
    point_sets = [cone_points(class_log) for class_log in range(6)]
    verify_complement_symmetry(point_sets)

    polynomial = fmpz_poly([
        1, -26, 115, -24, -23, 6, -105,
        6, -23, -24, 115, -26, 1,
    ])
    real_roots = [
        root.real
        for root, multiplicity in polynomial.complex_roots()
        if multiplicity == 1 and root.imag.contains(0)
    ]
    if len(real_roots) != 6:
        raise RuntimeError("candidate polynomial real-root count changed")
    windows = [
        (Fraction(20431, 1000), Fraction(20432, 1000)),
        (Fraction(189, 1000), Fraction(190, 1000)),
        (Fraction(1090, 1000), Fraction(1091, 1000)),
        (Fraction(48, 1000), Fraction(49, 1000)),
        (Fraction(5289, 1000), Fraction(5290, 1000)),
        (Fraction(916, 1000), Fraction(917, 1000)),
    ]
    candidates = []
    for left, right in windows:
        selected = [
            root
            for root in real_roots
            if root > arb_fraction(left) and root < arb_fraction(right)
        ]
        if len(selected) != 1:
            raise RuntimeError(
                f"isolating window [{left},{right}] selected {len(selected)}"
            )
        candidates.append(selected[0])

    analytic_logs: list[arb] = []
    total_panels = 0
    for class_log in range(3):
        value, panels = class_log_value(
            point_sets[class_log], beta, tolerance
        )
        analytic_logs.append(value)
        total_panels += panels
    analytic_logs.extend([-value for value in analytic_logs[:3]])

    maximum_difference = arb(0)
    for class_log, (analytic, candidate) in enumerate(
        zip(analytic_logs, candidates, strict=True)
    ):
        algebraic = candidate.log()
        difference = analytic - algebraic
        if not difference.contains(0):
            raise RuntimeError(
                f"class {class_log}: analytic and algebraic balls disjoint: "
                f"{difference}"
            )
        maximum_difference = max(
            maximum_difference, arb(abs(difference).upper())
        )
        print(f"CLASS_{class_log}_CONE_POINTS={len(point_sets[class_log])}")
        print(f"CLASS_{class_log}_ANALYTIC_LOG={analytic}")
        print(f"CLASS_{class_log}_ALGEBRAIC_ROOT={candidate}")
        print(f"CLASS_{class_log}_LOG_DIFFERENCE={difference}")

    powered_height_upper = SAFE_EXPONENT * maximum_difference
    voutier_lower = voutier_lower_bound()
    margin = voutier_lower / powered_height_upper
    quadratic_fallback = ((1 + arb(5).sqrt()) / 2).log() / 2
    if not (
        margin > 100
        and quadratic_fallback > powered_height_upper
    ):
        raise RuntimeError("height-rigidity margin did not clear")

    print(f"CONE_LATTICE_MATRIX={MATRIX}")
    print(f"CONE_LATTICE_DETERMINANT={DETERMINANT}")
    print("CONE_POINT_COUNT_PER_CLASS=20")
    print("CONE_COMPLEMENT_SYMMETRY=VERIFIED")
    print(f"TOTAL_SIMPSON_PANELS={total_panels}")
    print(f"SHINTANI_SAFE_EXPONENT={SAFE_EXPONENT}")
    print(f"POWERED_HEIGHT_UPPER={powered_height_upper}")
    print(f"VOUTIER_DEGREE_3_TO_24_LOWER={voutier_lower}")
    print(f"VOUTIER_MARGIN={margin}")
    print(f"QUADRATIC_HEIGHT_FALLBACK={quadratic_fallback}")
    print("DEGREE_1_FALLBACK=POSITIVE_RATIONAL_UNIT_IS_1")
    print("Q14_P7_ANALYTIC_ARB_CERTIFIED=1")
    print("Q14_P7_PACKET_IDENTITY_VERIFIED=1")


if __name__ == "__main__":
    main()
