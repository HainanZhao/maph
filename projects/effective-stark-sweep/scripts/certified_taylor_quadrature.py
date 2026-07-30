"""High-order interval Taylor quadrature for Arb-valued analytic functions.

For a panel centered at m with half-width h, coefficients through order
N-1 are integrated exactly.  Evaluating the formal coefficient of
order N with the constant term ranging over the whole panel encloses
f^(N)/N! everywhere on it, so the integral remainder is bounded by

    sup |[t^N] f(x+t)| * 2*h^(N+1)/(N+1).

This is the direct higher-order analogue of the interval fourth-
derivative Simpson bound used in the banked Q(sqrt(7)) certificate.
"""

from __future__ import annotations

from fractions import Fraction

from flint import arb, arb_series, ctx

from certify_q7_p7_packet import CertifiedIntegral, arb_fraction, interval


def taylor_panel(function, left: Fraction, right: Fraction, order: int) -> arb:
    middle = (left + right) / 2
    half_width = arb_fraction((right - left) / 2)
    variable = arb_series([arb_fraction(middle), arb(1)], order + 1)
    series = function(variable)
    result = arb(0)
    for power in range(0, order, 2):
        result += (
            series[power]
            * 2
            * half_width ** (power + 1)
            / (power + 1)
        )
    return result


def taylor_remainder_bound(
    function,
    left: Fraction,
    right: Fraction,
    order: int,
) -> arb:
    variable = arb_series(
        [interval(left, right), arb(1)], order + 1
    )
    coefficient = abs(function(variable)[order])
    half_width = arb_fraction((right - left) / 2)
    return coefficient * 2 * half_width ** (order + 1) / (order + 1)


def certified_taylor(
    function,
    left: Fraction,
    right: Fraction,
    tolerance: Fraction,
    *,
    order: int = 12,
    max_depth: int = 30,
) -> CertifiedIntegral:
    if order < 2 or order % 2:
        raise ValueError("Taylor quadrature order must be positive and even")
    # The banked Simpson certificates use cap=6 because they need only
    # the fourth coefficient.  Raise the global series cap explicitly
    # before constructing order-N series; otherwise python-flint
    # silently truncates and the Nth coefficient becomes zero.
    ctx.cap = max(ctx.cap, order + 2)
    accepted = arb(0)
    panels = 0
    stack = [(left, right, 0)]
    total_width = right - left
    while stack:
        panel_left, panel_right, depth = stack.pop()
        width = panel_right - panel_left
        try:
            error = taylor_remainder_bound(
                function, panel_left, panel_right, order
            )
            allowed = tolerance * width / total_width
        except (ValueError, ZeroDivisionError):
            error = arb("nan")
            allowed = Fraction(0)
        if error.is_finite() and error.upper() <= arb_fraction(allowed):
            accepted += taylor_panel(
                function, panel_left, panel_right, order
            )
            accepted += arb(0, error.upper())
            panels += 1
            continue
        if depth >= max_depth:
            raise RuntimeError(
                f"Taylor integration failed on "
                f"[{panel_left}, {panel_right}]: error {error}"
            )
        middle = (panel_left + panel_right) / 2
        stack.append((middle, panel_right, depth + 1))
        stack.append((panel_left, middle, depth + 1))
    return CertifiedIntegral(accepted, panels)
