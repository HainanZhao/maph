#!/usr/bin/env python3
"""Exact audit of the proposed d=6 fixed-point divisibility lemma.

For A=[[115,-24],[24,-5]], the Mobius displacement factors through the
minimal polynomial of beta=(5+sqrt(21))/2:

    A*tau-tau = -24*(tau^2-5*tau+1)/(24*tau-5).

The numerator has simple roots and the denominator is nonzero at them.
Thus divisibility by A*tau-tau in the local holomorphic ring at beta is
equivalent to vanishing at beta.  Applied entrywise to K(tau)^2-K(tau),
the proposed divisibility lemma is equivalent to the fixed-point TCC
identity, rather than a weaker route to it.
"""

from __future__ import annotations

import json

import sympy


TAU = sympy.Symbol("tau")
MINIMAL_POLYNOMIAL = TAU**2 - 5 * TAU + 1
A = ((115, -24), (24, -5))


def main() -> None:
    numerator = A[0][0] * TAU + A[0][1]
    denominator = A[1][0] * TAU + A[1][1]
    displacement = sympy.cancel(numerator / denominator - TAU)
    expected = sympy.cancel(
        -24 * MINIMAL_POLYNOMIAL / denominator
    )
    assert sympy.cancel(displacement - expected) == 0

    # In Q[tau]/(tau^2-5*tau+1), 24*tau-5 is beta^3 and is a unit.
    beta_cubed = sympy.rem(
        TAU**3, MINIMAL_POLYNOMIAL, domain=sympy.QQ
    )
    assert beta_cubed == denominator
    denominator_norm = sympy.resultant(
        MINIMAL_POLYNOMIAL, denominator, TAU
    )
    assert denominator_norm == 1

    # The fixed points are simple.
    discriminant = sympy.discriminant(MINIMAL_POLYNOMIAL, TAU)
    assert discriminant == 21
    derivative = sympy.diff(MINIMAL_POLYNOMIAL, TAU)
    derivative_norm = sympy.resultant(
        MINIMAL_POLYNOMIAL, derivative, TAU
    )
    assert derivative_norm == -21

    # A'(beta)-1=beta^-6-1 is nonzero.
    mobius_derivative_minus_one_numerator = sympy.rem(
        1 - denominator**2,
        MINIMAL_POLYNOMIAL,
        domain=sympy.QQ,
    )
    derivative_minus_one_norm = sympy.resultant(
        MINIMAL_POLYNOMIAL,
        mobius_derivative_minus_one_numerator,
        TAU,
    )
    assert derivative_minus_one_norm != 0

    result = {
        "schema": "sic-stark-dimension-six-fixed-point-equivalence-v1",
        "stabilizer": A,
        "minimal_polynomial": str(MINIMAL_POLYNOMIAL),
        "mobius_displacement": str(displacement),
        "displacement_factorization": (
            "-24*(tau^2-5*tau+1)/(24*tau-5)"
        ),
        "j_A_at_beta": "beta^3=24*beta-5",
        "denominator_norm": int(denominator_norm),
        "minimal_polynomial_discriminant": int(discriminant),
        "fixed_point_zero_order": 1,
        "local_ring_conclusion": (
            "(A*tau-tau) and (tau-beta) generate the same maximal ideal"
        ),
        "defect_conclusion": (
            "For a holomorphic defect entry F, "
            "(A*tau-tau) divides F iff F(beta)=0."
        ),
        "proof_status": (
            "Fixed-point divisibility is equivalent to the d=6 TCC "
            "identity and cannot be used as an independent proof."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
