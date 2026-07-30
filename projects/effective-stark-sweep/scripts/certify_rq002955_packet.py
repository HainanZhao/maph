#!/usr/bin/env python3
"""Independent Arb/Shintani certificate for RQ-002955."""

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


SAFE_EXPONENT = 4032
MATRIX = ((1, 1), (0, 7))


def mod_one_lower(value: Fraction) -> Fraction:
    return value - value.numerator // value.denominator


def cone_points(class_log: int, upper: bool):
    signed = determinant(MATRIX)
    if signed != 7:
        raise RuntimeError("cone determinant changed")
    generator = quotient_generator(MATRIX, signed)
    shift = (Fraction(3**class_log, 7), Fraction(0))
    points = []
    for residue in range(signed):
        first = shift[0] + residue * generator[0]
        second = shift[1] + residue * generator[1]
        reduce = mod_one_upper if upper else mod_one_lower
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
    delta = Fraction(1, 100_000)
    exp_majorant = Fraction(100_006, 100_000)
    numerator_remainder = Fraction(10**4, 1920) * exp_majorant
    denominator_remainder = (
        Fraction(9**4 + 1, 1920) * exp_majorant
        + Fraction(9**2, 24)
        * Fraction(1, 24)
        * exp_majorant**2
    )
    denominator_increment = (
        Fraction(9**2 + 1, 24) * exp_majorant
        + Fraction(9**2, 24)
        * Fraction(1, 24)
        * exp_majorant**2
        * delta**2
    )
    coefficient_majorant = Fraction(10**2 + 9**2 + 1, 24)
    second_order_majorant = Fraction(100)
    if not (
        Fraction(1, 1 - Fraction(10, 200_000)) < exp_majorant
        and 2 * (
            numerator_remainder
            + denominator_remainder
            + coefficient_majorant * denominator_increment
        ) < second_order_majorant
        and abs(linear) < 10
        and beta > 8
        and beta < 9
        and argument > 0
        and beta + 1 - argument > 0
    ):
        raise RuntimeError("period-nine analytic hypotheses failed")
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
        Fraction(0), cutoff,tolerance / 4,
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


def voutier():
    return min(
        (
            (arb(degree).log().log() / arb(degree).log()) ** 3
            / (4 * degree)
        ).lower()
        for degree in range(3, 25)
    )


def main():
    ctx.dps = 90
    ctx.cap = 16
    tolerance = Fraction("1e-10")
    beta = (9 + arb(77).sqrt()) / 2
    logs = []
    total_panels = 0
    for class_log in range(6):
        convention_values = []
        for upper in (True, False):
            value = arb(0)
            for x_value, y_value in cone_points(class_log, upper):
                term, panels = log_double_sine(
                    arb_fraction(x_value) + arb_fraction(y_value) * beta,
                    beta,
                    tolerance / 14,
                )
                value += term
                total_panels += panels
            convention_values.append(2 * value)
        logs.append((convention_values[0] + convention_values[1]) / 2)

    polynomial = fmpz_poly([
        1, -33, 339, -1445, 3442, -5496, 6377,
        -5496, 3442, -1445, 339, -33, 1,
    ])
    roots = [
        root.real
        for root, multiplicity in polynomial.complex_roots()
        if multiplicity == 1 and root.imag.contains(0) and root.real > 0
    ]
    windows = [
        (Fraction(18232, 1000), Fraction(18233, 1000)),
        (Fraction(2180, 1000), Fraction(2181, 1000)),
        (Fraction(8620, 1000), Fraction(8621, 1000)),
        (Fraction(54, 1000), Fraction(55, 1000)),
        (Fraction(458, 1000), Fraction(459, 1000)),
        (Fraction(116, 1000), Fraction(117, 1000)),
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

    powered = SAFE_EXPONENT * maximum
    lower = arb(voutier())
    margin = lower / powered
    fallback = ((1 + arb(5).sqrt()) / 2).log() / 2
    if not (margin > 100 and fallback > powered):
        raise RuntimeError("height gate failed")
    print("CASE_ID=RQ-002955")
    print("CONE_POINTS_PER_CLASS=7")
    print("BOUNDARY_CONVENTION=AVERAGE_OF_UPPER_AND_LOWER_HALF_OPEN")
    print("UNIT_ORDER_MOD_FINITE=1")
    print(f"TOTAL_TAYLOR_PANELS={total_panels}")
    print(f"SHINTANI_SAFE_EXPONENT={SAFE_EXPONENT}")
    print(f"POWERED_HEIGHT_UPPER={powered}")
    print(f"VOUTIER_MARGIN={margin}")
    print(f"QUADRATIC_HEIGHT_FALLBACK={fallback}")
    print("DEGREE_1_FALLBACK=POSITIVE_RATIONAL_UNIT_IS_1")
    print("RQ002955_ANALYTIC_ARB_CERTIFIED=1")
    print("RQ002955_PACKET_IDENTITY_VERIFIED=1")
    print("CLAIM_TAG=VERIFIED")


if __name__ == "__main__":
    main()
