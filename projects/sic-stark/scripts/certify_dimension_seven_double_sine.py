#!/usr/bin/env python3
"""Arb enclosures for the eight independent positive d=7 overlaps."""

from __future__ import annotations

import argparse
from fractions import Fraction

from flint import arb, arb_series, ctx, fmpz_poly

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
    """Enclose the reciprocal-convention log S2 in its fundamental strip."""

    linear = beta + 1 - 2 * argument
    if linear.contains(0) and abs(linear).upper() < _arb_fraction(tolerance):
        return arb(0), 0

    # The d=5 Taylor proof extends with |linear|<7 and beta<6.
    # For delta=10^-4 the positive sinh series gives the rational bounds
    # checked below.  They imply an 16*t^2 remainder majorant.
    delta = Fraction(1, 10_000)
    exponential_majorant = Fraction(4000, 3999)
    numerator_remainder = (
        Fraction(2401, 1920) * exponential_majorant
    )
    denominator_remainder = (
        Fraction(1296, 1920) * exponential_majorant
        + Fraction(1, 1920) * exponential_majorant
        + (
            Fraction(36, 24)
            * Fraction(1, 24)
            * exponential_majorant**2
        )
    )
    denominator_increment = (
        Fraction(37, 24) * exponential_majorant
        + (
            Fraction(36, 24)
            * Fraction(1, 24)
            * exponential_majorant**2
            * delta**2
        )
    )
    second_order_majorant = Fraction(16)
    if not (
        numerator_remainder < Fraction(4, 3)
        and denominator_remainder < Fraction(3, 4)
        and denominator_increment < Fraction(8, 5)
        and (
            Fraction(2)
            * (
                Fraction(4, 3)
                + Fraction(3, 4)
                + Fraction(43, 12) * Fraction(8, 5)
            )
            < second_order_majorant
        )
    ):
        raise RuntimeError("dimension-seven Taylor majorant check failed")
    if not (
        abs(linear) < 7
        and beta > 5
        and beta < 6
        and delta <= Fraction(1, 10_000)
    ):
        raise RuntimeError("dimension-seven near-zero hypotheses failed")

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

    cutoff = Fraction(50)
    complement = beta + 1 - argument
    if not (
        argument > arb(1) / 100
        and complement > arb(1) / 100
        and argument < 7
        and complement < 7
    ):
        raise RuntimeError("dimension-seven tail hypotheses failed")
    tail = _certified_simpson(
        _tail_integrand(argument, beta),
        Fraction(0),
        cutoff,
        tolerance / 4,
    )
    # For v>=50 and z,beta+1-z<7, v/z+1>57/7>8.
    # Both exponential denominators exceed 3/4 and v+z>50.
    # The difference of the two terms is <1/14.
    tail_remainder = (
        _arb_fraction(Fraction(1, 14))
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
    first: int, second: int, beta: arb, tolerance: Fraction
) -> tuple[arb, int]:
    third = (-first - second) % 7
    arguments = (
        1 + (second * beta - first) / 7,
        1 + (first * beta - third) / 7,
        1 + (third * beta - second) / 7,
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
    parser.add_argument("--tolerance", default="1e-8")
    arguments = parser.parse_args()
    tolerance = Fraction(arguments.tolerance)
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")

    ctx.dps = arguments.digits
    ctx.cap = 6
    beta = 3 + 2 * arb(2).sqrt()

    # Coefficients are in ascending order.
    absolute_polynomial = fmpz_poly(
        [
            1,
            -74,
            2225,
            -35410,
            323184,
            -1699558,
            4840899,
            -6293634,
            3051967,
            -6576776,
            15317332,
            -15200364,
            11844693,
            -15503642,
            25562877,
            -19215310,
            16910064,
            -19215310,
            25562877,
            -15503642,
            11844693,
            -15200364,
            15317332,
            -6576776,
            3051967,
            -6293634,
            4840899,
            -1699558,
            323184,
            -35410,
            2225,
            -74,
            1,
        ]
    )
    roots = absolute_polynomial.complex_roots()
    real_roots = [
        root.real
        for root, multiplicity in roots
        if multiplicity == 1 and root.imag.contains(0)
    ]
    if len(real_roots) != 16:
        raise RuntimeError("candidate polynomial does not have 16 real roots")

    candidate_windows = {
        (0, 1): (Fraction(5903986, 10**6), Fraction(5903987, 10**6)),
        (0, 2): (Fraction(3172313, 10**6), Fraction(3172314, 10**6)),
        (0, 3): (Fraction(1489129, 10**6), Fraction(1489130, 10**6)),
        (2, 6): (Fraction(6830385, 10**6), Fraction(6830386, 10**6)),
        (3, 6): (Fraction(9552165, 10**6), Fraction(9552166, 10**6)),
        (4, 4): (
            Fraction(12480646, 10**6),
            Fraction(12480647, 10**6),
        ),
        (3, 5): (
            Fraction(12577346, 10**6),
            Fraction(12577347, 10**6),
        ),
        (4, 5): (
            Fraction(22981630, 10**6),
            Fraction(22981631, 10**6),
        ),
    }

    maximum_log_difference = arb(0)
    for characteristic, (window_left, window_right) in candidate_windows.items():
        value, panels = overlap_log(
            *characteristic, beta, tolerance
        )
        squared_value = (2 * value).exp()
        candidates = [
            root
            for root in real_roots
            if (
                root > _arb_fraction(window_left)
                and root < _arb_fraction(window_right)
            )
        ]
        if len(candidates) != 1:
            raise RuntimeError(
                f"window {characteristic} contains {len(candidates)} roots"
            )
        candidate = candidates[0]
        difference = 2 * value - candidate.log()
        if (
            abs(difference).upper()
            > maximum_log_difference.upper()
        ):
            maximum_log_difference = abs(difference)
        print(
            f"LOG_OVERLAP_{characteristic[0]}_{characteristic[1]}="
            f"{value} PANELS={panels}"
        )
        print(
            f"SQUARED_OVERLAP_{characteristic[0]}_{characteristic[1]}="
            f"{squared_value}"
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

    # Shintani's constructive denominator audit gives the safe exponent
    # 16128.  Both the powered analytic invariant and the powered candidate
    # are then units in the same absolute degree-24 Stark field.  Voutier's
    # explicit height bound separates every non-torsion quotient.
    shintani_safe_exponent = 16128
    powered_height_upper = shintani_safe_exponent * maximum_log_difference
    voutier_bounds = []
    for degree in range(3, 25):
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
    print(f"SHINTANI_SAFE_EXPONENT={shintani_safe_exponent}")
    print(f"POWERED_HEIGHT_UPPER_BOUND={powered_height_upper}")
    print(f"VOUTIER_MINIMUM_DEGREE_3_TO_24={voutier_lower}")
    print(
        "HEIGHT_GAP_CERTIFIED="
        f"{powered_height_upper < voutier_lower}"
    )
    if not powered_height_upper < voutier_lower:
        raise RuntimeError("intervals are not sharp enough for height rigidity")


if __name__ == "__main__":
    main()
