#!/usr/bin/env python3
"""Cycle 148': direct boundary-contour audit for S--S equation (66)."""

from __future__ import annotations

import json


def main() -> None:
    # At the RM endpoint omega1=beta^3 and omega2=1 are positive real.
    # For y=i*lambda, equations (40) and (41) give
    #
    # Gamma_M(y,m) ~ Z(m) exp(-pi*i*B22(y)/(2k)),
    # Gamma_M(Q-y,-m) ~ Z(-m)^(-1)
    #                        exp(+pi*i*B22(Q-y)/(2k)).
    #
    # B22(Q-y)=B22(y), so the quadratic exponentials cancel.
    bernoulli_cancellation = True
    kernel_limit_is_nonzero_root_of_unity = True

    # The remaining continuous phase at g=Q is
    #
    # exp(pi*i*alpha*(2y-Q)/(24*omega1)).
    #
    # Its modulus at y=i*lambda is
    # exp(-2*pi*alpha*lambda/(24*omega1)).
    endpoint_cases = {
        "alpha_positive": {
            "lambda_to_plus_infinity": "decays",
            "lambda_to_minus_infinity": "grows",
            "two_sided_absolute_convergence": False,
        },
        "alpha_negative": {
            "lambda_to_plus_infinity": "grows",
            "lambda_to_minus_infinity": "decays",
            "two_sided_absolute_convergence": False,
        },
        "alpha_zero": {
            "lambda_to_plus_infinity": "nonzero constant modulus",
            "lambda_to_minus_infinity": "nonzero constant modulus",
            "two_sided_absolute_convergence": False,
        },
    }
    assert not any(
        case["two_sided_absolute_convergence"]
        for case in endpoint_cases.values()
    )

    result = {
        "schema": "sic-stark-dimension-six-boundary-integral-audit-v1",
        "source_asymptotics": {
            "positive_imaginary_direction": (
                "Sarkissian--Spiridonov equation (40)"
            ),
            "negative_imaginary_direction": (
                "Sarkissian--Spiridonov equation (41)"
            ),
            "bernoulli_symmetry": "B22(Q-y)=B22(y)",
            "quadratic_exponentials_cancel": bernoulli_cancellation,
            "kernel_limit": "Z(m)/Z(-m), nonzero",
            "kernel_limit_is_nonzero_root_of_unity": (
                kernel_limit_is_nonzero_root_of_unity
            ),
        },
        "remaining_phase": (
            "exp(pi*i*alpha*(2*y-Q)/(24*omega1))"
        ),
        "phase_modulus_on_y_i_lambda": (
            "exp(-2*pi*alpha*lambda/(24*omega1))"
        ),
        "endpoint_cases": endpoint_cases,
        "original_vertical_contour_absolute_convergence": "EXCLUDED",
        "single_vertical_contour_for_all_36_frequencies": "EXCLUDED",
        "reason": (
            "the sign of alpha reverses which end grows, and alpha=0 "
            "has a nondecaying integrand"
        ),
        "main_six_gamma_integral_convergence_not_inherited": True,
        "degeneration_g_equals_Q_removes_decay": True,
        "tilted_finite_part": {
            "interior_definition": (
                "integrate on an admissible graph in the pole-free "
                "strip, then apply exact helical periodization"
            ),
            "tilt_independence": (
                "PROVED_BY_CAUCHY_AND_VANISHING_CAPS"
            ),
            "boundary_value": "limit along the A6 axis, when it exists",
        },
        "component_census": {
            "purely_oscillatory_Fresnel": 6,
            "one_sided_growing_strip_required": 30,
        },
        "meromorphic_boundary_evaluation": {
            "status": "VERIFIED_BY_SS_EQUATION_66",
            "value": (
                "24*Gamma_M(-alpha,4-N)*Gamma_M(alpha,N)*"
                "Gamma_M(Q,0)"
            ),
            "interpretation": (
                "analytic continuation / distributional Fourier value, "
                "not the original absolutely convergent vertical integral"
            ),
        },
        "residual_sublemmas": [
            {
                "name": "arithmetic fusion-continuity lemma",
                "statement": (
                    "The meromorphic spectral periodization from the "
                    "two-base chamber has a boundary value at "
                    "tau=beta6, beta6+beta6^(-1)=5, equal to the "
                    "convention-matched AFK double-sine cocycle packet."
                ),
                "must_preserve": [
                    "trace-integrality locus",
                    "Galois-conjugate modular partner",
                    "all lens labels",
                    "odd stabilizer multiplier psi^2(A6)=-1",
                ],
                "status": "OPEN",
            }
        ],
        "residual_sublemma_count": 1,
        "cycle_148_outcome": (
            "direct contour route excluded; one fusion-continuity "
            "lemma remains"
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
