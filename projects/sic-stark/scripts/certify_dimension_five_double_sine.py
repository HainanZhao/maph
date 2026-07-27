#!/usr/bin/env python3
"""Rigorous ball enclosures for the four d=5 double-sine generators.

This script uses python-flint/Arb.  It is deliberately separate from the
ordinary floating-point exploration: its purpose is to supply the analytic
half of a Shintani-power unit-lattice certificate.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction

from flint import arb, arb_series, ctx, fmpz_poly


def _sinh(value):
    if isinstance(value, arb_series):
        return (value.exp() - (-value).exp()) / 2
    return value.sinh()


def _exp(value):
    return value.exp()


def _arb_fraction(value: Fraction) -> arb:
    return arb(value.numerator) / value.denominator


def _interval(left: Fraction, right: Fraction) -> arb:
    left_ball = _arb_fraction(left)
    right_ball = _arb_fraction(right)
    midpoint = (left_ball + right_ball) / 2
    radius = (right_ball - left_ball) / 2
    return midpoint + arb(0, radius.upper())


@dataclass
class CertifiedIntegral:
    value: arb
    panels: int


def _simpson_panel(function, left: Fraction, right: Fraction) -> arb:
    middle = (left + right) / 2
    width = _arb_fraction(right - left)
    return width * (
        function(_arb_fraction(left))
        + 4 * function(_arb_fraction(middle))
        + function(_arb_fraction(right))
    ) / 6


def _fourth_derivative_bound(
    function, left: Fraction, right: Fraction
) -> arb:
    variable = arb_series([_interval(left, right), arb(1)])
    coefficient = function(variable)[4]
    return 24 * abs(coefficient)


def _certified_simpson(
    function,
    left: Fraction,
    right: Fraction,
    tolerance: Fraction,
    *,
    max_depth: int = 28,
) -> CertifiedIntegral:
    """Adaptive Simpson integration with an interval fourth-derivative bound."""

    accepted = arb(0)
    panels = 0
    stack = [(left, right, 0)]
    total_width = right - left
    while stack:
        panel_left, panel_right, depth = stack.pop()
        width = panel_right - panel_left
        try:
            derivative_bound = _fourth_derivative_bound(
                function, panel_left, panel_right
            )
            error = derivative_bound * _arb_fraction(width) ** 5 / 2880
            allowed = tolerance * width / total_width
        except (ValueError, ZeroDivisionError):
            error = arb("nan")
            allowed = Fraction(0)
        if error.is_finite() and error.upper() <= _arb_fraction(allowed):
            accepted += _simpson_panel(function, panel_left, panel_right)
            accepted += arb(0, error.upper())
            panels += 1
            continue
        if depth >= max_depth:
            raise RuntimeError(
                f"integration failed on [{panel_left}, {panel_right}]: "
                f"error {error}"
            )
        middle = (panel_left + panel_right) / 2
        stack.append((middle, panel_right, depth + 1))
        stack.append((panel_left, middle, depth + 1))
    return CertifiedIntegral(accepted, panels)


def _near_integrand(argument: arb, beta: arb):
    linear = beta + 1 - 2 * argument

    def integrand(value):
        return (
            _sinh(linear * value / 2)
            / (
                2
                * value
                * _sinh(beta * value / 2)
                * _sinh(value / 2)
            )
            - linear / (beta * value**2)
        )

    return integrand


def _tail_integrand(argument: arb, beta: arb):
    complement = beta + 1 - argument

    def term(z_value, value):
        return _exp(-z_value) / (
            (_exp(-beta * (value / z_value + 1)) - 1)
            * (_exp(-(value / z_value + 1)) - 1)
            * (value + z_value)
        )

    def integrand(value):
        return _exp(-value) * (
            term(argument, value) - term(complement, value)
        )

    return integrand


def fundamental_log_double_sine(
    argument: arb,
    beta: arb,
    tolerance: Fraction,
) -> tuple[arb, int]:
    """Enclose log S_2^here(argument | beta, 1) in the fundamental strip."""

    linear = beta + 1 - 2 * argument
    if (
        linear.contains(0)
        and abs(linear).upper() < _arb_fraction(tolerance)
    ):
        return arb(0), 0

    # At zero the regularized integrand is even.  Put
    # H_c(t)=sinh(ct/2)/(ct/2).  Its positive series gives, for
    # |c| <= 5 and t <= 1/10000,
    #
    #   |H_c-1-c^2 t^2/24| <= c^4 cosh(|c|t/2)t^4/1920,
    #
    # while cosh(|c|t/2) <= exp(1/4000) <= 4000/3999.  The rational
    # inequalities below then give
    #
    #   |r_linear| <= t^4/3,  |r_denominator| <= t^4/6,
    #   |H_beta H_1-1| <= 3t^2/4,
    #   |(linear^2-beta^2-1)/24| <= 7/4.
    #
    # Hence the difference from the displayed constant term is at most
    # (5/3)(1/3+1/6+(7/4)(3/4))t^2 < 4t^2.  All comparisons here are
    # exact rational checks; this avoids interval division by a ball
    # containing zero.
    delta = Fraction(1, 10_000)
    exponential_majorant = Fraction(4000, 3999)
    numerator_remainder = (
        Fraction(625, 1920) * exponential_majorant
    )
    denominator_remainder = (
        Fraction(256, 1920) * exponential_majorant
        + Fraction(1, 1920) * exponential_majorant
        + (
            Fraction(16, 24)
            * Fraction(1, 24)
            * exponential_majorant**2
        )
    )
    denominator_increment = (
        Fraction(17, 24) * exponential_majorant
        + (
            Fraction(16, 24)
            * Fraction(1, 24)
            * exponential_majorant**2
            * delta**2
        )
    )
    second_order_majorant = Fraction(4)
    if not (
        numerator_remainder < Fraction(1, 3)
        and denominator_remainder < Fraction(1, 6)
        and denominator_increment < Fraction(3, 4)
        and (
            Fraction(5, 3)
            * (
                Fraction(1, 3)
                + Fraction(1, 6)
                + Fraction(7, 4) * Fraction(3, 4)
            )
            < second_order_majorant
        )
    ):
        raise RuntimeError("near-zero rational majorant check failed")
    if not (
        abs(linear) < 5
        and beta > 3
        and beta < 4
        and delta <= Fraction(1, 10_000)
    ):
        raise RuntimeError("near-zero Taylor-majorant hypotheses failed")
    zero_value = (
        linear * (linear**2 - beta**2 - 1) / (24 * beta)
    )
    zero_remainder = second_order_majorant * delta**3 / 3
    near_value = zero_value * _arb_fraction(delta)
    near_value += arb(0, _arb_fraction(zero_remainder).upper())

    # Geometric splitting prevents a wide interval close to zero from
    # destroying the cancellation in the regularized integrand.
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

    cutoff = Fraction(36)
    complement = beta + 1 - argument
    if not (
        argument > arb(1) / 100
        and complement > arb(1) / 100
        and argument < 5
        and complement < 5
    ):
        raise RuntimeError("tail-majorant hypotheses failed")
    tail = _certified_simpson(
        _tail_integrand(argument, beta),
        Fraction(0),
        cutoff,
        tolerance / 4,
    )
    # For the finite list of reduced fifth-arguments, z and beta+1-z
    # lie in (1/100,5).  If v >= 36, then v/z+1 > 41/5.  Each absolute
    # exponential denominator is > 3/4 (already exp(8)>1+8>4), their
    # product is > 1/2, and v+z>36.  Each term is therefore <1/18;
    # integrating the difference against exp(-v) gives exp(-36)/9.
    tail_remainder = (
        _arb_fraction(Fraction(1, 9))
        * (-_arb_fraction(cutoff)).exp()
    )
    tail_value = tail.value + arb(0, tail_remainder.upper())

    boundary = -linear / beta
    return near_value + boundary + tail_value, near_panels + tail.panels


def log_double_sine(
    argument: arb,
    beta: arb,
    tolerance: Fraction,
) -> tuple[arb, int]:
    """Enclose the shifted real double sine logarithm."""

    log_factor = arb(0)
    panels = 0
    while argument <= 0:
        sine = (arb.pi() * argument / beta).sin()
        log_factor -= (2 * sine).log()
        argument += 1
    while argument >= beta + 1:
        argument -= 1
        sine = (arb.pi() * argument / beta).sin()
        log_factor += (2 * sine).log()
    fundamental, used = fundamental_log_double_sine(
        argument, beta, tolerance
    )
    return log_factor + fundamental, panels + used


def overlap_log(
    first: int,
    second: int,
    beta: arb,
    tolerance: Fraction,
) -> tuple[arb, int]:
    third = (-first - second) % 5
    arguments = (
        1 + (second * beta - first) / 5,
        1 + (first * beta - third) / 5,
        1 + (third * beta - second) / 5,
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
    parser.add_argument("--digits", type=int, default=30)
    parser.add_argument("--tolerance", default="1e-8")
    arguments = parser.parse_args()
    tolerance = Fraction(arguments.tolerance)
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")

    ctx.dps = arguments.digits
    ctx.cap = 6
    beta = 2 + arb(3).sqrt()
    characteristics = ((0, 1), (0, 2), (2, 4), (3, 3))
    absolute_polynomial = fmpz_poly(
        [
            1,
            -16,
            95,
            -260,
            355,
            -348,
            388,
            -300,
            195,
            -300,
            388,
            -348,
            355,
            -260,
            95,
            -16,
            1,
        ]
    )
    roots = absolute_polynomial.complex_roots()
    real_roots = [
        root.real
        for root, multiplicity in roots
        if multiplicity == 1 and root.imag.contains(0)
    ]
    if len(real_roots) != 8:
        raise RuntimeError("candidate polynomial does not have eight real roots")

    # Rational isolating intervals select the candidates independently
    # of any undocumented ordering used by complex_roots().
    candidate_windows = {
        (0, 1): (Fraction(3890, 1000), Fraction(3891, 1000)),
        (0, 2): (Fraction(1633, 1000), Fraction(1634, 1000)),
        (2, 4): (Fraction(4313, 1000), Fraction(4314, 1000)),
        (3, 3): (Fraction(5540, 1000), Fraction(5541, 1000)),
    }
    maximum_log_difference = arb(0)
    for first, second in characteristics:
        value, panels = overlap_log(
            first, second, beta, tolerance
        )
        squared_value = (2 * value).exp()
        window_left, window_right = candidate_windows[(first, second)]
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
                f"candidate interval for {(first, second)} "
                f"contains {len(candidates)} roots"
            )
        candidate = candidates[0]
        log_difference = 2 * value - candidate.log()
        if abs(log_difference).upper() > maximum_log_difference.upper():
            maximum_log_difference = abs(log_difference)
        print(
            f"LOG_OVERLAP_{first}_{second}={value} "
            f"PANELS={panels}"
        )
        print(f"SQUARED_OVERLAP_{first}_{second}={squared_value}")
        print(f"CANDIDATE_ROOT_{first}_{second}={candidate}")
        print(
            f"LOG_DIFFERENCE_{first}_{second}={log_difference} "
            f"CONTAINS_ZERO={log_difference.contains(0)}"
        )
        if not log_difference.contains(0):
            raise RuntimeError(
                f"candidate root for {(first, second)} is not enclosed"
            )

    powered_height_upper = 5760 * maximum_log_difference
    voutier_bounds = []
    for degree in range(3, 17):
        d_value = arb(degree)
        bound = (
            (d_value.log().log() / d_value.log()) ** 3
            / (4 * degree)
        )
        voutier_bounds.append(bound)
    voutier_lower = voutier_bounds[0]
    for bound in voutier_bounds[1:]:
        if bound.lower() < voutier_lower.lower():
            voutier_lower = bound
    print(f"MAXIMUM_LOG_DIFFERENCE={maximum_log_difference}")
    print(f"POWERED_HEIGHT_UPPER_BOUND={powered_height_upper}")
    print(f"VOUTIER_MINIMUM_DEGREE_3_TO_16={voutier_lower}")
    print(
        "HEIGHT_GAP_CERTIFIED="
        f"{powered_height_upper < voutier_lower}"
    )
    if not powered_height_upper < voutier_lower:
        raise RuntimeError("intervals are not sharp enough for Voutier rigidity")


if __name__ == "__main__":
    main()
