#!/usr/bin/env python3
"""Exact audit of the Cycle-2 local event-map counterexample.

The script verifies the compact bump's C2 endpoint matching, exact mass, and
the resulting vector-field and level-speed differences. It does not replace
the arbitrary-local-state argument in the written proof.
"""

from __future__ import annotations

from fractions import Fraction
import json


def multiply(a: tuple[Fraction, ...], b: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] += ai * bj
    return tuple(out)


def derivative(a: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple((i + 1) * a[i + 1] for i in range(len(a) - 1))


def evaluate(a: tuple[Fraction, ...], x: Fraction) -> Fraction:
    value = Fraction(0)
    for coefficient in reversed(a):
        value = value * x + coefficient
    return value


def integral_zero_to(a: tuple[Fraction, ...], endpoint: Fraction) -> Fraction:
    return sum(
        coefficient * endpoint ** (degree + 1) / (degree + 1)
        for degree, coefficient in enumerate(a)
    )


def audit() -> None:
    length = Fraction(1, 2)
    # In t=x-1/4 coordinates, h=t^3(length-t)^3.
    t_cubed = (Fraction(0), Fraction(0), Fraction(0), Fraction(1))
    remaining_cubed = (
        length**3,
        -3 * length**2,
        3 * length,
        Fraction(-1),
    )
    bump = multiply(t_cubed, remaining_cubed)

    first = derivative(bump)
    second = derivative(first)
    for endpoint in (Fraction(0), length):
        if (evaluate(bump, endpoint), evaluate(first, endpoint), evaluate(second, endpoint)) != (0, 0, 0):
            raise AssertionError(("C2 endpoint", endpoint))

    mass = integral_zero_to(bump, length)
    if mass != Fraction(1, 17920):
        raise AssertionError(("mass", mass))

    epsilon = Fraction(1, 7)
    kernel_trace_delta = epsilon * mass / 2
    local_u = Fraction(2)
    local_ux = Fraction(-1)
    vector_field_delta = -local_u * kernel_trace_delta
    level_speed_delta = -vector_field_delta / local_ux

    if kernel_trace_delta != Fraction(1, 250880):
        raise AssertionError(("kernel trace", kernel_trace_delta))
    if vector_field_delta != -epsilon * mass:
        raise AssertionError(("vector field", vector_field_delta))
    if level_speed_delta != -epsilon * mass:
        raise AssertionError(("level speed", level_speed_delta))

    ray_checks = 0
    # Check the exact completed-square identity with sqrt(D)=s rational.
    for s in (Fraction(1, 5), Fraction(2, 7), Fraction(3, 11)):
        diffusivity = s * s
        for wx in (Fraction(-7, 3), Fraction(-1, 2), Fraction(5, 4)):
            for wxx in (Fraction(-4, 9), Fraction(0), Fraction(8, 5)):
                for competition in (Fraction(0), Fraction(2, 3)):
                    direct = (
                        diffusivity * (wxx + wx * wx)
                        + 1
                        - competition
                        + 2 * s * wx
                    )
                    completed = (
                        diffusivity * wxx
                        + diffusivity * (wx + 1 / s) ** 2
                        - competition
                    )
                    if direct != completed:
                        raise AssertionError(("critical ray", direct, completed))
                    ray_checks += 1

    print(json.dumps({
        "status": "PASS",
        "bump_mass": f"{mass.numerator}/{mass.denominator}",
        "epsilon": f"{epsilon.numerator}/{epsilon.denominator}",
        "level_speed_delta": f"{level_speed_delta.numerator}/{level_speed_delta.denominator}",
        "critical_ray_checks": ray_checks,
    }, sort_keys=True))


if __name__ == "__main__":
    audit()
