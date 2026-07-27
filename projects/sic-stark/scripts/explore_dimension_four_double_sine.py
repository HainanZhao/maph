#!/usr/bin/env python3
"""Numerically audit the dimension-four double-sine unit relation."""

from __future__ import annotations

import math


def simpson_integral(function, start: float, stop: float, steps: int) -> float:
    """Integrate with the composite Simpson rule."""

    if steps <= 0 or steps % 2:
        raise ValueError("steps must be a positive even integer")
    width = (stop - start) / steps
    total = function(start) + function(stop)
    for index in range(1, steps):
        total += (4 if index % 2 else 2) * function(start + index * width)
    return total * width / 3


def _near_zero_integrand(
    argument: float, first_period: float, second_period: float, value: float
) -> float:
    return (
        math.sinh(
            ((first_period + second_period) / 2 - argument) * value
        )
        / (
            2
            * value
            * math.sinh(first_period * value / 2)
            * math.sinh(second_period * value / 2)
        )
        - (first_period + second_period - 2 * argument)
        / (first_period * second_period * value**2)
    )


def _tail_term(
    argument: float, first_period: float, second_period: float, value: float
) -> float:
    return math.exp(-argument) / (
        math.expm1(-first_period * (value / argument + 1))
        * math.expm1(-second_period * (value / argument + 1))
        * (value + argument)
    )


def fundamental_double_sine(
    argument: float, first_period: float, second_period: float
) -> float:
    """Evaluate Shintani's double sine inside its fundamental strip."""

    if abs(first_period + second_period - 2 * argument) < 1e-14:
        return 1.0
    cutoff = 1e-5
    near_zero = simpson_integral(
        lambda value: _near_zero_integrand(
            argument, first_period, second_period, value
        ),
        cutoff,
        1.0,
        12000,
    )
    near_zero += cutoff * _near_zero_integrand(
        argument, first_period, second_period, cutoff
    )
    complement = first_period + second_period - argument
    tail = simpson_integral(
        lambda value: math.exp(-value)
        * (
            _tail_term(
                argument, first_period, second_period, value
            )
            - _tail_term(
                complement, first_period, second_period, value
            )
        ),
        0.0,
        35.0,
        24000,
    )
    boundary = -(
        first_period + second_period - 2 * argument
    ) / (first_period * second_period)
    return math.exp(near_zero + boundary + tail)


def double_sine(
    argument: float, first_period: float, second_period: float
) -> float:
    """Evaluate the real double sine using its period shifts."""

    factor = 1.0
    while argument <= 0:
        factor /= 2 * math.sin(math.pi * argument / first_period)
        argument += second_period
    while argument >= first_period + second_period:
        argument -= second_period
        factor *= 2 * math.sin(math.pi * argument / first_period)
    return factor * fundamental_double_sine(
        argument, first_period, second_period
    )


def dimension_four_unit() -> float:
    """Return the positive unit ``x=-triple_double_sine(0,1)``."""

    dimension = 4
    beta = (3 + math.sqrt(5)) / 2
    arguments = (
        1 + beta / dimension,
        1 - 3 / dimension,
        1 + (3 * beta - 1) / dimension,
    )
    return math.prod(double_sine(value, beta, 1.0) for value in arguments)


def main() -> None:
    unit = dimension_four_unit()
    target = math.sqrt(3 + math.sqrt(5))
    print(f"x = {unit:.15f}")
    print(f"x + x^-1 = {unit + 1 / unit:.15f}")
    print(f"sqrt(3+sqrt(5)) = {target:.15f}")
    print(
        "reciprocal-relation residual = "
        f"{unit + 1 / unit - target:+.3e}"
    )


if __name__ == "__main__":
    main()
