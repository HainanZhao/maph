#!/usr/bin/env python3
"""Rigorous Arb enclosures for the four nontrivial lower d=8 overlaps."""

from __future__ import annotations

import argparse
from fractions import Fraction

from flint import arb, ctx, fmpz_poly

from certify_dimension_five_double_sine import (
    _arb_fraction,
    _certified_simpson,
    _near_integrand,
    _tail_integrand,
)


def fundamental_log_double_sine(
    argument: arb,
    beta: arb,
    tolerance: Fraction,
) -> tuple[arb, int]:
    """Enclose the reciprocal-convention logarithm in its basic strip."""

    linear = beta + 1 - 2 * argument
    if linear.contains(0) and abs(linear).upper() < _arb_fraction(tolerance):
        return arb(0), 0

    # Here beta<7 and |linear|<8.  The positive sinh series, at
    # delta=10^-4, gives the rational majorants checked below.  They are
    # the d=8 analogue of the d=5 and d=7 enclosure lemmas.
    delta = Fraction(1, 10_000)
    exponential_majorant = Fraction(2000, 1999)
    numerator_remainder = (
        Fraction(4096, 1920) * exponential_majorant
    )
    denominator_remainder = (
        Fraction(2401, 1920) * exponential_majorant
        + Fraction(1, 1920) * exponential_majorant
        + (
            Fraction(49, 24)
            * Fraction(1, 24)
            * exponential_majorant**2
        )
    )
    denominator_increment = (
        Fraction(50, 24) * exponential_majorant
        + (
            Fraction(49, 24)
            * Fraction(1, 24)
            * exponential_majorant**2
            * delta**2
        )
    )
    coefficient_majorant = Fraction(8, 3)
    second_order_majorant = Fraction(20)
    if not (
        numerator_remainder < Fraction(11, 5)
        and denominator_remainder < Fraction(7, 5)
        and denominator_increment < Fraction(21, 10)
        and (
            2
            * (
                Fraction(11, 5)
                + Fraction(7, 5)
                + coefficient_majorant * Fraction(21, 10)
            )
            < second_order_majorant
        )
    ):
        raise RuntimeError("dimension-eight Taylor majorant check failed")
    if not (
        abs(linear) < 8
        and beta > 6
        and beta < 7
        and delta <= Fraction(1, 10_000)
    ):
        raise RuntimeError("dimension-eight near-zero hypotheses failed")

    zero_value = linear * (linear**2 - beta**2 - 1) / (24 * beta)
    zero_remainder = second_order_majorant * delta**3 / 3
    near_value = zero_value * _arb_fraction(delta)
    near_value += arb(0, _arb_fraction(zero_remainder).upper())

    near_function = _near_integrand(argument, beta)
    segment_left = delta
    near_panels = 0
    while segment_left < 1:
        segment_right = min(Fraction(1), 4 * segment_left)
        segment = _certified_simpson(
            near_function,
            segment_left,
            segment_right,
            tolerance * (segment_right - segment_left) / 8,
        )
        near_value += segment.value
        near_panels += segment.panels
        segment_left = segment_right

    cutoff = Fraction(60)
    complement = beta + 1 - argument
    if not (
        argument > arb(1) / 100
        and complement > arb(1) / 100
        and argument < 8
        and complement < 8
    ):
        raise RuntimeError("dimension-eight tail hypotheses failed")
    tail = _certified_simpson(
        _tail_integrand(argument, beta),
        Fraction(0),
        cutoff,
        tolerance / 4,
    )
    # For v>=60 and z,beta+1-z<8, v/z+1>8.5.  Each exponential
    # denominator exceeds 3/4 and v+z>60, so the difference of the two
    # tail terms is less than 1/16.
    tail_remainder = (
        _arb_fraction(Fraction(1, 16))
        * (-_arb_fraction(cutoff)).exp()
    )
    return (
        near_value
        - linear / beta
        + tail.value
        + arb(0, tail_remainder.upper()),
        near_panels + tail.panels,
    )


def log_double_sine(
    argument: arb, beta: arb, tolerance: Fraction
) -> tuple[arb, int]:
    log_factor = arb(0)
    while argument <= 0:
        sine = (arb.pi() * argument / beta).sin()
        log_factor -= (2 * sine).log()
        argument += 1
    while argument >= beta + 1:
        argument -= 1
        sine = (arb.pi() * argument / beta).sin()
        log_factor += (2 * sine).log()
    value, panels = fundamental_log_double_sine(
        argument, beta, tolerance
    )
    return log_factor + value, panels


def overlap_log(
    first: int,
    second: int,
    beta: arb,
    tolerance: Fraction,
) -> tuple[arb, int]:
    third = (-first - second) % 8
    arguments = (
        1 + (second * beta - first) / 8,
        1 + (first * beta - third) / 8,
        1 + (third * beta - second) / 8,
    )
    total = arb(0)
    panels = 0
    for argument in arguments:
        value, used = log_double_sine(
            argument, beta, tolerance / 3
        )
        total += value
        panels += used
    return total, panels


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--digits", type=int, default=40)
    parser.add_argument("--tolerance", default="1e-10")
    arguments = parser.parse_args()
    tolerance = Fraction(arguments.tolerance)
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")

    ctx.dps = arguments.digits
    ctx.cap = 6
    beta = (7 + 3 * arb(5).sqrt()) / 2
    polynomial = fmpz_poly([1, -8, 12, 8, -22, 8, 12, -8, 1])
    roots = polynomial.complex_roots()
    real_roots = [
        root.real
        for root, multiplicity in roots
        if multiplicity == 1 and root.imag.contains(0)
    ]
    if len(real_roots) != 4:
        raise RuntimeError("lower-conductor polynomial needs four real roots")

    windows = {
        (0, 2): (Fraction(2005, 1000), Fraction(2006, 1000)),
        (0, 6): (Fraction(498, 1000), Fraction(499, 1000)),
        (2, 2): (Fraction(172, 1000), Fraction(173, 1000)),
        (4, 6): (Fraction(5795, 1000), Fraction(5796, 1000)),
    }
    maximum_log_difference = arb(0)
    for characteristic, (left, right) in windows.items():
        logarithm, panels = overlap_log(
            *characteristic, beta, tolerance
        )
        candidates = [
            root
            for root in real_roots
            if root > _arb_fraction(left) and root < _arb_fraction(right)
        ]
        if len(candidates) != 1:
            raise RuntimeError(
                f"window {characteristic} has {len(candidates)} roots"
            )
        candidate = candidates[0]
        difference = logarithm - candidate.log()
        if abs(difference).upper() > maximum_log_difference.upper():
            maximum_log_difference = abs(difference)
        print(
            f"LOG_OVERLAP_{characteristic[0]}_{characteristic[1]}="
            f"{logarithm} PANELS={panels}"
        )
        print(
            f"CANDIDATE_ROOT_{characteristic[0]}_{characteristic[1]}="
            f"{candidate}"
        )
        print(
            f"LOG_DIFFERENCE_{characteristic[0]}_{characteristic[1]}="
            f"{difference} CONTAINS_ZERO={difference.contains(0)}"
        )
        if not difference.contains(0):
            raise RuntimeError("analytic and algebraic balls are disjoint")

    print(f"MAXIMUM_LOG_DIFFERENCE={maximum_log_difference}")
    # The exact modulus-12 Shintani audit clears every algebraicity and
    # distribution denominator with exponent 576.  The powered analytic
    # value and powered candidate are units in the same degree-eight field.
    shintani_safe_exponent = 576
    powered_height_upper = shintani_safe_exponent * maximum_log_difference
    voutier_bounds = []
    for degree in range(3, 9):
        degree_ball = arb(degree)
        bound = (
            (degree_ball.log().log() / degree_ball.log()) ** 3
            / (4 * degree)
        )
        voutier_bounds.append(bound)
    voutier_lower = voutier_bounds[0]
    for bound in voutier_bounds[1:]:
        if bound.lower() < voutier_lower.lower():
            voutier_lower = bound
    quadratic_lower = ((1 + arb(5).sqrt()) / 2).log() / 2
    height_lower = (
        voutier_lower
        if voutier_lower.lower() < quadratic_lower.lower()
        else quadratic_lower
    )
    print(f"SHINTANI_SAFE_EXPONENT={shintani_safe_exponent}")
    print(f"POWERED_HEIGHT_UPPER_BOUND={powered_height_upper}")
    print(f"VOUTIER_MINIMUM_DEGREE_3_TO_8={voutier_lower}")
    print(f"QUADRATIC_UNIT_HEIGHT_LOWER_BOUND={quadratic_lower}")
    print(f"UNIT_HEIGHT_LOWER_DEGREES_2_TO_8={height_lower}")
    print(
        "HEIGHT_GAP_CERTIFIED="
        f"{powered_height_upper < height_lower}"
    )
    if not powered_height_upper < height_lower:
        raise RuntimeError("intervals are not sharp enough for rigidity")
    print("LOWER_CONDUCTOR_ANALYTIC_WINDOWS_CERTIFIED=1")
    print("LOWER_CONDUCTOR_ROOT_IDENTITIES_CERTIFIED=1")


if __name__ == "__main__":
    main()
