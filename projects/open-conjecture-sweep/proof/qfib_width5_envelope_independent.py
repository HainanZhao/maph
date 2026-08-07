#!/usr/bin/env python3
"""Independent symbolic check of the explicit width-five envelope constants."""

from __future__ import annotations

import json

import sympy as sp


t, a, d = sp.symbols("t a d", integer=True)
b = a + d
Q = lambda x: x**3 / sp.Integer(180) + 11 * x**2 / sp.Integer(120) + 9 * x / sp.Integer(20)
LOW = sp.Rational(91, 360)
HIGH = sp.Integer(1)
SHIFTS = (
    (0, 1),
    (a, -1),
    (b, -1),
    (2 * a + b, 1),
    (a + 3 * b, 1),
    (2 * a + 3 * b, -1),
)
BREAKS = (0, a, b, 2 * a + b, a + 3 * b, 2 * a + 3 * b)


def envelope(number_active: int) -> sp.Expr:
    value = 0
    for shift, sign in SHIFTS[:number_active]:
        value += Q(t - shift) + LOW if sign > 0 else -(Q(t - shift) + HIGH)
    return sp.expand(value)


def nonnegative_coefficients(expression: sp.Expr) -> bool:
    A, D = sp.symbols("A D", nonnegative=True)
    shifted = sp.Poly(sp.expand(expression.subs({a: A + 34, d: D + 1})), A, D)
    return all(coefficient >= 0 for coefficient in shifted.coeffs())


def main() -> None:
    h = [None] + [envelope(index) for index in range(1, 7)]
    expected = (
        sp.Integer(91),
        2 * a**3 + 33 * a**2 + 162 * a - 269,
        2 * a**3 + 6 * a**2 * d + 33 * a**2 + 6 * a * d**2
        + 66 * a * d + 162 * a - 629,
        22 * a**3 + 30 * a**2 * d - 33 * a**2 + 6 * a * d**2
        - 66 * a * d - 162 * a - 538,
        3 * (2 * a * b * (a + b - 11) - 149),
        3 * (2 * a * b - 269),
    )

    # The six printed constants are direct endpoint (or limiting-endpoint)
    # evaluations, with the continuous midpoint used in the last interval.
    points = (
        0,
        a,
        b,
        None,
        2 * a + 3 * b,
        (5 * a + 7 * b - 12) / 2,
    )
    assert sp.expand(360 * h[1].subs(t, points[0]) - expected[0]) == 0
    assert sp.expand(360 * h[2].subs(t, points[1]) - expected[1]) == 0
    assert sp.expand(360 * h[3].subs(t, points[2]) - expected[2]) == 0

    fourth_left = sp.expand(360 * h[4].subs(t, 2 * a + b))
    fourth_right = sp.expand(360 * h[4].subs(t, a + 3 * b))
    assert sp.expand(fourth_right - expected[3]) == 0
    assert nonnegative_coefficients(fourth_left - expected[3])

    assert sp.expand(360 * h[5].subs(t, points[4]) - expected[4]) == 0
    assert sp.expand(360 * h[6].subs(t, points[5]) - expected[5]) == 0

    # Independent shape checks for the endpoint-minimum arguments.
    assert sp.Poly(sp.diff(h[1], t), t).all_coeffs()[0] > 0
    assert sp.expand(sp.diff(h[2], t, 2)) == a / 30

    derivative3 = sp.diff(h[3], t)
    assert sp.Poly(derivative3, t).LC() < 0
    assert nonnegative_coefficients(sp.expand(360 * derivative3.subs(t, b)))
    assert nonnegative_coefficients(sp.expand(360 * derivative3.subs(t, 2 * a + b)))

    assert sp.expand(sp.diff(h[4], t, 2)) == -a / 30

    derivative5 = sp.diff(h[5], t)
    assert sp.Poly(derivative5, t).LC() > 0
    assert nonnegative_coefficients(sp.expand(-360 * derivative5.subs(t, a + 3 * b)))
    assert nonnegative_coefficients(sp.expand(-360 * derivative5.subs(t, 2 * a + 3 * b)))

    assert sp.expand(360 * sp.diff(h[6], t) + 12 * a * b) == 0
    assert all(nonnegative_coefficients(value) for value in expected[1:])

    print(
        json.dumps(
            {
                "constants_checked": 6,
                "domain": "a>=34,d>=1",
                "shape_checks": 6,
                "status": "PASS",
                "sympy_version": sp.__version__,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
