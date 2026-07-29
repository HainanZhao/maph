#!/usr/bin/env python3
"""Rigorous magnitude identification for the discriminant-eight d=7 tuple.

The generic AFK six-factor expansion has alternating periods
alpha=2+sqrt(2) and alpha/2.  This script encloses its absolute value
directly with Arb, matches the eight distinct nontrivial magnitudes to
isolated algebraic roots, and applies the existing Shintani/Voutier
height-rigidity gate.
"""

from __future__ import annotations

import argparse
import math
from fractions import Fraction

from flint import arb, ctx, fmpz_poly

from certify_dimension_five_double_sine import (
    _arb_fraction,
    _certified_simpson,
    _near_integrand,
    _tail_integrand,
)


DIMENSION = 7
AT = ((239, -140), (70, -41))
WORD = (4, 2, 4, 2, 4, 2, 0)


def certified_floor(value: arb) -> int:
    candidate = math.floor(float(value))
    if not (value > candidate and value < candidate + 1):
        raise RuntimeError(f"floor not separated for {value}")
    return candidate


def fundamental_log_double_sine(
    argument: arb,
    beta: arb,
    tolerance: Fraction,
) -> tuple[arb, int]:
    """Enclose log |S_2(argument|beta,1)| in the fundamental strip."""

    linear = beta + 1 - 2 * argument
    if linear.contains(0) and abs(linear).upper() < _arb_fraction(tolerance):
        return arb(0), 0

    # Uniform rational majorants for 3/2 < beta < 7/2,
    # |linear| < 9/2, and delta=10^-4.  They follow from the same
    # positive sinh-series estimate used by the d=5--8 certificates.
    delta = Fraction(1, 10_000)
    exponential_majorant = Fraction(4000, 3999)
    numerator_remainder = (
        Fraction(625, 1920) * exponential_majorant
    )
    denominator_remainder = (
        Fraction(2401, 16 * 1920) * exponential_majorant
        + Fraction(1, 1920) * exponential_majorant
        + (
            Fraction(49, 4 * 24)
            * Fraction(1, 24)
            * exponential_majorant**2
        )
    )
    denominator_increment = (
        Fraction(53, 4 * 24) * exponential_majorant
        + (
            Fraction(49, 4 * 24)
            * Fraction(1, 24)
            * exponential_majorant**2
            * delta**2
        )
    )
    second_order_majorant = Fraction(3)
    if not (
        numerator_remainder < Fraction(1, 3)
        and denominator_remainder < Fraction(1, 8)
        and denominator_increment < Fraction(3, 5)
        and (
            2
            * (
                Fraction(1, 3)
                + Fraction(1, 8)
                + Fraction(3, 2) * Fraction(3, 5)
            )
            < second_order_majorant
        )
    ):
        raise RuntimeError("maximal d=7 Taylor majorant check failed")
    if not (
        abs(linear) < arb(9) / 2
        and beta > arb(3) / 2
        and beta < arb(7) / 2
    ):
        raise RuntimeError("maximal d=7 near-zero hypotheses failed")

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

    complement = beta + 1 - argument
    if not (
        argument > arb(1) / 100
        and complement > arb(1) / 100
        and argument < 5
        and complement < 5
    ):
        raise RuntimeError("maximal d=7 tail hypotheses failed")
    cutoff = Fraction(36)
    tail = _certified_simpson(
        _tail_integrand(argument, beta),
        Fraction(0),
        cutoff,
        tolerance / 4,
    )
    tail_remainder = (
        _arb_fraction(Fraction(1, 9))
        * (-_arb_fraction(cutoff)).exp()
    )
    return (
        near_value
        - linear / beta
        + tail.value
        + arb(0, tail_remainder.upper()),
        near_panels + tail.panels,
    )


def log_abs_double_sine(
    argument: arb,
    beta: arb,
    tolerance: Fraction,
) -> tuple[arb, int]:
    log_factor = arb(0)
    while argument <= 0:
        sine = (arb.pi() * argument / beta).sin()
        if sine.contains(0):
            raise RuntimeError("double-sine shift met zero")
        log_factor -= abs(2 * sine).log()
        argument += 1
    while argument >= beta + 1:
        argument -= 1
        sine = (arb.pi() * argument / beta).sin()
        if sine.contains(0):
            raise RuntimeError("double-sine shift met zero")
        log_factor += abs(2 * sine).log()
    value, panels = fundamental_log_double_sine(
        argument, beta, tolerance
    )
    return log_factor + value, panels


def log_abs_q_pochhammer(
    argument: arb,
    period: arb,
    count: int,
) -> arb:
    result = arb(0)
    if count >= 0:
        indices = range(count)
        sign = 1
    else:
        indices = range(1, -count + 1)
        sign = -1
    for index in indices:
        shifted = (
            argument + index * period
            if count >= 0
            else argument - index * period
        )
        sine = (arb.pi() * shifted).sin()
        if sine.contains(0):
            raise RuntimeError("q-Pochhammer factor met zero")
        result += sign * abs(2 * sine).log()
    return result


def period_data(alpha: arb) -> tuple[list[arb], list[arb]]:
    rows = [
        [arb(AT[0][0]), arb(AT[0][1])],
        [arb(AT[1][0]), arb(AT[1][1])],
    ]
    for index in range(len(WORD) - 1):
        rows.append([
            -rows[index][0] + WORD[index] * rows[index + 1][0],
            -rows[index][1] + WORD[index] * rows[index + 1][1],
        ])
    periods = [row[0] * alpha + row[1] for row in rows]
    ratios = [
        periods[index] / periods[(index + 1) % len(periods)]
        for index in range(len(periods))
    ]
    return periods, ratios


def overlap_log_abs(
    first: int,
    second: int,
    alpha: arb,
    tolerance: Fraction,
) -> tuple[arb, int]:
    periods, ratios = period_data(alpha)
    z_value = (
        periods[0] * second - periods[1] * first
    ) / DIMENSION
    finite_numerator = (
        -AT[1][0] * first + (AT[0][0] - 1) * second
    )
    if finite_numerator % DIMENSION:
        raise RuntimeError("nonintegral outer finite-product count")
    finite_count = finite_numerator // DIMENSION
    result = -log_abs_q_pochhammer(
        (second * alpha - first) / DIMENSION,
        alpha,
        finite_count,
    )
    panels = 0
    for index in range(len(WORD) - 1):
        argument = z_value / periods[index + 2]
        period = ratios[index + 1]
        shift = certified_floor(-argument) + certified_floor(period / 2)
        result += log_abs_q_pochhammer(
            argument / period,
            -1 / period,
            -shift,
        )
        value, used = log_abs_double_sine(
            argument + shift + 1,
            period,
            tolerance / (len(WORD) - 1),
        )
        result += value
        panels += used
    return result, panels


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--digits", type=int, default=50)
    parser.add_argument("--tolerance", default="2e-12")
    arguments = parser.parse_args()
    tolerance = Fraction(arguments.tolerance)
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")

    ctx.dps = arguments.digits
    ctx.cap = 6
    alpha = 2 + arb(2).sqrt()

    scalar_polynomial = fmpz_poly([
        1, 4, -2, -22, -18, 16, 41, 16, -18, -22, -2, 4, 1
    ])
    quartic_polynomial = fmpz_poly([1, 2, 1, 2, 1])
    scalar_roots = [
        root.real
        for root, multiplicity in scalar_polynomial.complex_roots()
        if multiplicity == 1 and root.imag.contains(0)
    ]
    quartic_roots = [
        root.real
        for root, multiplicity in quartic_polynomial.complex_roots()
        if multiplicity == 1 and root.imag.contains(0)
    ]
    if len(scalar_roots) != 6 or len(quartic_roots) != 2:
        raise RuntimeError("candidate real-root count changed")

    targets = {
        (0, 1): (scalar_roots, Fraction(-2739, 1000), Fraction(-2738, 1000)),
        (0, 2): (scalar_roots, Fraction(-405, 1000), Fraction(-404, 1000)),
        (0, 3): (scalar_roots, Fraction(2086, 1000), Fraction(2087, 1000)),
        (0, 4): (scalar_roots, Fraction(479, 1000), Fraction(480, 1000)),
        (0, 5): (scalar_roots, Fraction(-2472, 1000), Fraction(-2471, 1000)),
        (0, 6): (scalar_roots, Fraction(-366, 1000), Fraction(-365, 1000)),
        (1, 3): (quartic_roots, Fraction(-1884, 1000), Fraction(-1883, 1000)),
        (3, 2): (quartic_roots, Fraction(-532, 1000), Fraction(-531, 1000)),
    }

    maximum_log_difference = arb(0)
    for characteristic, (roots, left, right) in targets.items():
        candidates = [
            root
            for root in roots
            if root > _arb_fraction(left) and root < _arb_fraction(right)
        ]
        if len(candidates) != 1:
            raise RuntimeError(
                f"window {characteristic} has {len(candidates)} roots"
            )
        candidate = candidates[0]
        analytic, panels = overlap_log_abs(
            *characteristic, alpha, tolerance
        )
        algebraic = abs(candidate).log()
        difference = analytic - algebraic
        if abs(difference).upper() > maximum_log_difference.upper():
            maximum_log_difference = abs(difference)
        print(
            f"LOG_ABS_OVERLAP_{characteristic[0]}_{characteristic[1]}="
            f"{analytic} PANELS={panels}"
        )
        print(
            f"ALGEBRAIC_ROOT_{characteristic[0]}_{characteristic[1]}="
            f"{candidate}"
        )
        print(
            f"LOG_DIFFERENCE_{characteristic[0]}_{characteristic[1]}="
            f"{difference} CONTAINS_ZERO={difference.contains(0)}"
        )
        if not difference.contains(0):
            raise RuntimeError("analytic and algebraic balls are disjoint")

    shintani_safe_exponent = 16128
    powered_height_upper = shintani_safe_exponent * maximum_log_difference
    voutier_lower = None
    for degree in range(3, 25):
        degree_ball = arb(degree)
        bound = (
            (degree_ball.log().log() / degree_ball.log()) ** 3
            / (4 * degree)
        )
        if voutier_lower is None or bound.lower() < voutier_lower.lower():
            voutier_lower = bound
    print(f"MAXIMUM_LOG_DIFFERENCE={maximum_log_difference}")
    print(f"SHINTANI_SAFE_EXPONENT={shintani_safe_exponent}")
    print(f"POWERED_HEIGHT_UPPER_BOUND={powered_height_upper}")
    print(f"VOUTIER_MINIMUM_DEGREE_3_TO_24={voutier_lower}")
    print(f"HEIGHT_GAP_CERTIFIED={powered_height_upper < voutier_lower}")
    if not powered_height_upper < voutier_lower:
        raise RuntimeError("intervals are not sharp enough for height rigidity")
    print("DIMENSION_SEVEN_DISCRIMINANT_EIGHT_MAGNITUDES_CERTIFIED=1")


if __name__ == "__main__":
    main()
