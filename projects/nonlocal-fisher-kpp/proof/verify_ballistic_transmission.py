#!/usr/bin/env python3
"""Exact algebra audit for the frozen step-barrier benchmark.

This checks the coefficient identities and interface matching in Equation
(13) of frozen_barrier_ballistic_transmission.md. It does not prove the
Brownian-bridge limit.
"""

from __future__ import annotations

from fractions import Fraction
import json


Monomial = tuple[int, int, int]
Polynomial = dict[Monomial, Fraction]


def add(*polynomials: Polynomial) -> Polynomial:
    out: Polynomial = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            out[monomial] = out.get(monomial, Fraction(0)) + coefficient
    return {monomial: coefficient for monomial, coefficient in out.items() if coefficient}


def scale(polynomial: Polynomial, coefficient: Fraction) -> Polynomial:
    return {monomial: coefficient * value for monomial, value in polynomial.items()}


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    out: Polynomial = {}
    for (a, b, c), x in left.items():
        for (d, e, f), y in right.items():
            key = (a + d, b + e, c + f)
            out[key] = out.get(key, Fraction(0)) + x * y
    return {monomial: coefficient for monomial, coefficient in out.items() if coefficient}


def main() -> int:
    # C=3, kappa=sqrt(1+C)=2.  Write each exponential branch as a
    # coefficient/exponent pair and check the ODE coefficient exactly.
    c = Fraction(3)
    kappa = Fraction(2)
    left_coefficient = Fraction(2, 3)
    left_exponent = kappa - 1
    right_constant = Fraction(1)
    right_exponential_coefficient = Fraction(-1, 3)
    right_exponent = Fraction(-2)

    left_ode = left_exponent**2 + 2 * left_exponent - c
    right_constant_ode = Fraction(0)
    right_exponential_ode = right_exponent**2 + 2 * right_exponent
    if (left_ode, right_constant_ode, right_exponential_ode) != (0, 0, 0):
        raise AssertionError("drift-two ODE coefficient mismatch")

    left_value = left_coefficient
    left_derivative = left_coefficient * left_exponent
    right_value = right_constant + right_exponential_coefficient
    right_derivative = right_exponential_coefficient * right_exponent
    if (left_value, left_derivative) != (right_value, right_derivative):
        raise AssertionError("interface mismatch")

    # phi=e^x H. Check phi''+(1-C)phi=2phi branch by branch.
    phi_left_exponent = left_exponent + 1
    phi_right_exponents = (Fraction(1), Fraction(-1))
    if phi_left_exponent**2 + 1 - c != 2:
        raise AssertionError("left generalized eigenfunction mismatch")
    for exponent in phi_right_exponents:
        if exponent**2 + 1 != 2:
            raise AssertionError("right generalized eigenfunction mismatch")

    # The free critical-ray Gaussian exponent is an exact polynomial identity:
    # s+t-(2t+s-y)^2/(4t) = y-(s-y)^2/(4t).
    # Derive both sides independently after multiplication by 4t.
    t: Polynomial = {(1, 0, 0): Fraction(1)}
    s: Polynomial = {(0, 1, 0): Fraction(1)}
    y: Polynomial = {(0, 0, 1): Fraction(1)}
    bridge_displacement = add(scale(t, Fraction(2)), s, scale(y, Fraction(-1)))
    left_polynomial = add(
        scale(multiply(t, add(s, t)), Fraction(4)),
        scale(multiply(bridge_displacement, bridge_displacement), Fraction(-1)),
    )
    right_displacement = add(s, scale(y, Fraction(-1)))
    right_polynomial = add(
        scale(multiply(t, y), Fraction(4)),
        scale(multiply(right_displacement, right_displacement), Fraction(-1)),
    )
    if left_polynomial != right_polynomial:
        raise AssertionError("critical-ray exponent mismatch")

    print(json.dumps({
        "status": "PASS",
        "claim_boundary": "Exact step-barrier algebra only; bridge asymptotics remain written proof.",
        "barrier_height": int(c),
        "ballistic_interface_transmission": f"{left_value.numerator}/{left_value.denominator}",
        "left_characteristic_exponent": int(left_exponent),
        "interface_checks": 2,
        "ode_coefficient_checks": 6,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
