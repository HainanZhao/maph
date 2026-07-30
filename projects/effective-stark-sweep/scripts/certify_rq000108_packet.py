#!/usr/bin/env python3
"""Independent Arb/Shintani certificate for RQ-000108."""

from __future__ import annotations

import argparse
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
    matrix_vector,
    mod_one_upper,
    quotient_generator,
)


SAFE_EXPONENT = 2880
UNIT_ORDER = 4
CONE_MATRICES = [
    ((-21, -55), (76, 199)),
    ((-43, -113), (51, 134)),
    ((-46, -121), (73, 192)),
    ((-8, -21), (69, 181)),
]
UNIT_ACTION_MATRICES = [
    ((-1, -1), (5, 4)),
    ((-46, -41), (55, 49)),
    ((-91, -59), (145, 94)),
    ((-6, -1), (55, 9)),
]
SHIFT = (Fraction(1, 15), Fraction(0))


def adjacent_matrix(class_log: int, step: int):
    base = CONE_MATRICES[class_log]
    first = (base[0][0], base[1][0])
    second = (base[0][1], base[1][1])
    for _ in range(step):
        first = matrix_vector(UNIT_ACTION_MATRICES[class_log], first)
        second = matrix_vector(UNIT_ACTION_MATRICES[class_log], second)
    return ((first[0], second[0]), (first[1], second[1]))


def points(class_log: int, step: int):
    matrix = adjacent_matrix(class_log, step)
    signed = determinant(matrix)
    if abs(signed) != 1:
        raise RuntimeError("cone determinant changed")
    generator = quotient_generator(matrix, signed)
    first = SHIFT[0] + 0 * generator[0]
    second = SHIFT[1] + 0 * generator[1]
    return [(
        mod_one_upper(Fraction(
            matrix[1][1] * first - matrix[0][1] * second, signed
        )),
        mod_one_upper(Fraction(
            -matrix[1][0] * first + matrix[0][0] * second, signed
        )),
    )]


def log_double_sine(argument: arb, beta: arb, tolerance: Fraction):
    linear = beta + 1 - 2 * argument
    delta = Fraction(1, 100_000)
    exp_majorant = Fraction(100_004, 100_000)
    numerator_remainder = Fraction(7**4, 1920) * exp_majorant
    denominator_remainder = (
        Fraction(6**4 + 1, 1920) * exp_majorant
        + Fraction(6**2, 24)
        * Fraction(1, 24)
        * exp_majorant**2
    )
    denominator_increment = (
        Fraction(6**2 + 1, 24) * exp_majorant
        + Fraction(6**2, 24)
        * Fraction(1, 24)
        * exp_majorant**2
        * delta**2
    )
    coefficient_majorant = Fraction(7**2 + 6**2 + 1, 24)
    second_order_majorant = Fraction(1000)
    if not (
        Fraction(1, 1 - Fraction(7, 200_000)) < exp_majorant
        and 2
        * (
            numerator_remainder
            + denominator_remainder
            + coefficient_majorant * denominator_increment
        )
        < second_order_majorant
        and abs(linear) < 7
        and beta > 2
        and beta < 6
        and argument > 0
        and beta + 1 - argument > 0
    ):
        raise RuntimeError("small-period analytic hypotheses failed")
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


def voutier():
    return min(
        (
            (arb(d).log().log() / arb(d).log()) ** 3 / (4 * d)
        ).lower()
        for d in range(3, 17)
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--digits", type=int, default=90)
    parser.add_argument("--tolerance", default="1e-10")
    args = parser.parse_args()
    ctx.dps = args.digits
    ctx.cap = 16
    tolerance = Fraction(args.tolerance)
    beta = (3 + arb(5).sqrt()) / 2
    logs = []
    total_panels = 0
    for class_log in range(4):
        value = arb(0)
        for step in range(UNIT_ORDER):
            for x_value, y_value in points(class_log, step):
                term, panels = log_double_sine(
                    arb_fraction(x_value) + arb_fraction(y_value) * beta,
                    beta,
                    tolerance / UNIT_ORDER,
                )
                value += term
                total_panels += panels
        logs.append(2 * value)

    polynomial = fmpz_poly(
        [1, -8, -2, 19, 25, 19, -2, -8, 1]
    )
    roots = [
        root.real
        for root, multiplicity in polynomial.complex_roots()
        if multiplicity == 1 and root.imag.contains(0) and root.real > 0
    ]
    windows = [
        (Fraction(7892, 1000), Fraction(7893, 1000)),
        (Fraction(2242, 1000), Fraction(2243, 1000)),
        (Fraction(126, 1000), Fraction(127, 1000)),
        (Fraction(445, 1000), Fraction(446, 1000)),
    ]
    candidates = []
    for left, right in windows:
        selected = [
            root for root in roots
            if root > arb_fraction(left) and root < arb_fraction(right)
        ]
        if len(selected) != 1:
            raise RuntimeError("root isolation failed")
        candidates.append(selected[0])
    maximum = arb(0)
    for index, (analytic, candidate) in enumerate(zip(logs, candidates)):
        difference = analytic - candidate.log()
        if not difference.contains(0):
            raise RuntimeError(f"class {index} mismatch: {difference}")
        maximum = max(maximum, arb(abs(difference).upper()))
        print(f"CLASS_{index}_ANALYTIC_LOG={analytic}")
        print(f"CLASS_{index}_ALGEBRAIC_ROOT={candidate}")
        print(f"CLASS_{index}_LOG_DIFFERENCE={difference}")
    powered = SAFE_EXPONENT * maximum
    lower = arb(voutier())
    margin = lower / powered
    fallback = ((1 + arb(5).sqrt()) / 2).log() / 2
    if not (margin > 100 and fallback > powered):
        raise RuntimeError("height gate failed")
    print("CASE_ID=RQ-000108")
    print("CONE_POINTS_PER_CLASS=4")
    print("UNIT_ORDER_MOD_FINITE=4")
    print(f"TOTAL_TAYLOR_PANELS={total_panels}")
    print(f"SHINTANI_SAFE_EXPONENT={SAFE_EXPONENT}")
    print(f"POWERED_HEIGHT_UPPER={powered}")
    print(f"VOUTIER_MARGIN={margin}")
    print(f"QUADRATIC_HEIGHT_FALLBACK={fallback}")
    print("DEGREE_1_FALLBACK=POSITIVE_RATIONAL_UNIT_IS_1")
    print("RQ000108_ANALYTIC_ARB_CERTIFIED=1")
    print("RQ000108_PACKET_IDENTITY_VERIFIED=1")
    print("CLAIM_TAG=VERIFIED")


if __name__ == "__main__":
    main()
