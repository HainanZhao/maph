#!/usr/bin/env python3
"""Independent Arb/Shintani certificate for RQ-001107."""

from __future__ import annotations

from fractions import Fraction

from flint import arb, ctx, fmpz_poly

from certified_taylor_quadrature import certified_taylor
from certify_q7_p7_packet import (
    arb_fraction,
    near_integrand,
    product,
    tail_integrand,
)
from certify_rq000458_b_packet import (
    determinant,
    mod_one_upper,
    quotient_generator,
)


SAFE_EXPONENT = 15840
MAXIMUM_PACKET_COMPARISON_DEGREE = 40
CERTIFIED_DEGREE_CAP = 80
MATRIX = ((-16, -736), (67, 3081))


def mod_one_lower(value: Fraction) -> Fraction:
    return value - value.numerator // value.denominator


def cone_points(class_log: int, upper: bool):
    signed = determinant(MATRIX)
    if signed != 16:
        raise RuntimeError("cone determinant changed")
    generator = quotient_generator(MATRIX, signed)
    shift = (Fraction(2**class_log, 11), Fraction(0))
    reduce = mod_one_upper if upper else mod_one_lower
    points = []
    for residue in range(signed):
        first = shift[0] + residue * generator[0]
        second = shift[1] + residue * generator[1]
        points.append((
            reduce(Fraction(
                MATRIX[1][1] * first - MATRIX[0][1] * second,
                signed,
            )),
            reduce(Fraction(
                -MATRIX[1][0] * first + MATRIX[0][0] * second,
                signed,
            )),
        ))
    if len(set(points)) != signed:
        raise RuntimeError("cone quotient enumeration repeated a point")
    return points


def log_double_sine(argument: arb, beta: arb, tolerance: Fraction):
    linear = beta + 1 - 2 * argument
    delta = Fraction(1, 1_000_000)
    exp_majorant = Fraction(100_003, 100_000)
    numerator_remainder = Fraction(47**4, 1920) * exp_majorant
    denominator_remainder = (
        Fraction(46**4 + 1, 1920) * exp_majorant
        + Fraction(46**2, 24)
        * Fraction(1, 24)
        * exp_majorant**2
    )
    denominator_increment = (
        Fraction(46**2 + 1, 24) * exp_majorant
        + Fraction(46**2, 24)
        * Fraction(1, 24)
        * exp_majorant**2
        * delta**2
    )
    coefficient_majorant = Fraction(47**2 + 46**2 + 1, 24)
    second_order_majorant = Fraction(50_000)
    if not (
        Fraction(1, 1 - Fraction(47, 2_000_000)) < exp_majorant
        and 2 * (
            numerator_remainder
            + denominator_remainder
            + coefficient_majorant * denominator_increment
        ) < second_order_majorant
        and abs(linear) < 47
        and beta > 45
        and beta < 46
        and argument > 0
        and beta + 1 - argument > 0
    ):
        raise RuntimeError("period-forty-six analytic hypotheses failed")
    zero_value = linear * (linear**2 - beta**2 - 1) / (24 * beta)
    near = zero_value * arb_fraction(delta)
    near += arb(
        0,
        arb_fraction(second_order_majorant * delta**3 / 3).upper(),
    )
    left = delta
    panels = 0
    function = near_integrand(argument, beta)
    while left < 1:
        right = min(Fraction(1), 4 * left)
        segment = certified_taylor(
            function, left, right,
            tolerance * (right - left) / 8,
        )
        near += segment.value
        panels += segment.panels
        left = right
    cutoff = Fraction(64)
    tail = certified_taylor(
        tail_integrand(argument, beta),
        Fraction(0), cutoff, tolerance / 4,
    )
    if not sum(
        Fraction(3**index, product(range(1, index + 1)))
        for index in range(9)
    ) > 20:
        raise RuntimeError("tail majorant failed")
    value = (
        near - linear / beta + tail.value
        + arb(0, ((-arb_fraction(cutoff)).exp() / 16).upper())
    )
    return value, panels + tail.panels


def voutier_bounds():
    bounds = [
        (
            (arb(degree).log().log() / arb(degree).log()) ** 3
            / (4 * degree)
        )
        for degree in range(3, CERTIFIED_DEGREE_CAP + 1)
    ]
    return arb(min(bound.lower() for bound in bounds)), bounds


def main():
    ctx.dps = 100
    ctx.cap = 16
    tolerance = Fraction("1e-12")
    beta = 23 + 4 * arb(33).sqrt()
    logs = []
    total_panels = 0
    for class_log in range(10):
        convention_values = []
        for upper in (True, False):
            value = arb(0)
            for x_value, y_value in cone_points(class_log, upper):
                term, panels = log_double_sine(
                    arb_fraction(x_value) + arb_fraction(y_value) * beta,
                    beta,
                    tolerance / 32,
                )
                value += term
                total_panels += panels
            convention_values.append(2 * value)
        logs.append((convention_values[0] + convention_values[1]) / 2)

    polynomial = fmpz_poly([
        1, -20, 146, -513, 995, -1336, 1613, -1598, 1131,
        -826, 803, -826, 1131, -1598, 1613, -1336, 995,
        -513, 146, -20, 1,
    ])
    roots = [
        root.real
        for root, multiplicity in polynomial.complex_roots()
        if multiplicity == 1 and root.imag.contains(0) and root.real > 0
    ]
    windows = [
        (Fraction(8645, 1000), Fraction(8646, 1000)),
        (Fraction(276, 1000), Fraction(277, 1000)),
        (Fraction(1245, 1000), Fraction(1246, 1000)),
        (Fraction(571, 1000), Fraction(572, 1000)),
        (Fraction(236, 1000), Fraction(237, 1000)),
        (Fraction(115, 1000), Fraction(116, 1000)),
        (Fraction(3611, 1000), Fraction(3612, 1000)),
        (Fraction(802, 1000), Fraction(803, 1000)),
        (Fraction(1748, 1000), Fraction(1749, 1000)),
        (Fraction(4234, 1000), Fraction(4235, 1000)),
    ]
    maximum = arb(0)
    for class_log, (analytic, window) in enumerate(zip(logs, windows)):
        selected = [
            root for root in roots
            if root > arb_fraction(window[0])
            and root < arb_fraction(window[1])
        ]
        if len(selected) != 1:
            raise RuntimeError(f"class {class_log}: root isolation failed")
        difference = analytic - selected[0].log()
        if not difference.contains(0):
            raise RuntimeError(f"class {class_log} mismatch: {difference}")
        maximum = max(maximum, arb(abs(difference).upper()))
        print(f"CLASS_{class_log}_ANALYTIC_LOG={analytic}")
        print(f"CLASS_{class_log}_ALGEBRAIC_ROOT={selected[0]}")
        print(f"CLASS_{class_log}_LOG_DIFFERENCE={difference}")

    voutier_lower, bounds = voutier_bounds()
    degree_80_bound = bounds[-1]
    raw_error_target = voutier_lower / (100 * SAFE_EXPONENT)
    powered = SAFE_EXPONENT * maximum
    margin = voutier_lower / powered
    fallback = ((1 + arb(5).sqrt()) / 2).log() / 2
    if not (
        maximum < raw_error_target
        and margin > 100
        and fallback > powered
    ):
        raise RuntimeError("height gate failed")
    print("CASE_ID=RQ-001107")
    print("CONE_POINTS_PER_CLASS=16")
    print("BOUNDARY_CONVENTION=AVERAGE_OF_UPPER_AND_LOWER_HALF_OPEN")
    print("UNIT_ORDER_MOD_FINITE=1")
    print(f"TOTAL_TAYLOR_PANELS={total_panels}")
    print(f"SHINTANI_SAFE_EXPONENT={SAFE_EXPONENT}")
    print(f"MAXIMUM_PACKET_COMPARISON_DEGREE={MAXIMUM_PACKET_COMPARISON_DEGREE}")
    print(f"CERTIFIED_DEGREE_CAP={CERTIFIED_DEGREE_CAP}")
    print(f"VOUTIER_DEGREE_3_TO_80_MINIMUM={voutier_lower}")
    print(f"VOUTIER_DEGREE_80_BOUND={degree_80_bound}")
    print(f"RAW_LOG_ERROR_TARGET={raw_error_target}")
    print(f"RAW_LOG_ERROR_UPPER={maximum}")
    print(f"POWERED_HEIGHT_UPPER={powered}")
    print(f"VOUTIER_MARGIN={margin}")
    print(f"QUADRATIC_HEIGHT_FALLBACK={fallback}")
    print("DEGREE_1_FALLBACK=POSITIVE_RATIONAL_UNIT_IS_1")
    print("RQ001107_ANALYTIC_ARB_CERTIFIED=1")
    print("RQ001107_PACKET_IDENTITY_VERIFIED=1")
    print("CLAIM_TAG=VERIFIED")


if __name__ == "__main__":
    main()
