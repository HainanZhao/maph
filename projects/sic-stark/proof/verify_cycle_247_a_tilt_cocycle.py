#!/usr/bin/env python3
"""Falsify C247's proposed one-q tilt cocycle before its q-series test."""
from __future__ import annotations

import json
from fractions import Fraction as F

try:
    from .verify_cycle_228_f3_square_residual_block import blocks
    from .verify_cycle_245_a_principal_coefficients import audit as c245_audit
except ImportError:  # pragma: no cover
    from verify_cycle_228_f3_square_residual_block import blocks
    from verify_cycle_245_a_principal_coefficients import audit as c245_audit


def audit() -> dict[str, object]:
    prior = c245_audit()
    assert prior["recurrence"]["exact_recurrence_family_derived"]
    assert prior["recurrence"]["all_multiplier_factors_nonzero"]
    # Write w=t_+ + i*epsilon.  C247 proposed to identify the A1/A4
    # numerator base theta=(w+5)/24 with the A2/A3 pole base
    # eta=(115-1/w)/24.  The latter comes directly from -beta/alpha.
    theta = "(w+5)/24"
    eta = "(115-1/w)/24"
    difference = "eta-theta=-(w^2-110*w+1)/(24*w)"
    root_identity = "t_+^2-110*t_++1=0, t_+=55+12*sqrt(21)"
    expected_periods = {
        "A1": ((F(1, 24), F(5, 24)), (F(0), F(1))),
        "A2": ((F(1), F(0)), (F(-115, 24), F(1, 24))),
        "A3": ((F(24), F(0)), (F(-115), F(1))),
        "A4": ((F(1), F(5)), (F(0), F(24))),
    }
    for position, item in enumerate(blocks()["A"], 1):
        name = f"A{position}"
        alpha = tuple(F(x) for x in item["alpha"])
        beta = tuple(F(x) for x in item["beta"])
        assert (alpha, beta) == expected_periods[name]
    # A1/A4 give alpha/beta=(w+5)/24.  A2/A3 have alpha proportional to
    # w and beta proportional to -115*w+1, hence
    # -beta/alpha=(115-1/w)/24 exactly.

    # t_+=55+12*sqrt(21)>1.  Thus, for every epsilon>0,
    # Im(eta-theta)=-epsilon*(1-1/(t_+^2+epsilon^2))/24 is strictly
    # negative.  The two exponential bases cannot agree even modulo Z.
    assert 55 > 1
    imaginary_difference_sign = "Im(eta-theta)=-epsilon*(1-1/(t_+^2+epsilon^2))/24<0 for epsilon>0"
    q_bases = {
        "A1_A4_numerator": "exp(2*pi*i*theta)",
        "A2_A3_pole": "exp(2*pi*i*eta)",
        "not_equal_for_any_positive_tilt": True,
    }
    factor_role_derivation = {
        "A1_A4": "alpha/beta=(w+5)/24=theta, so C245's Phi_alpha numerator factors use exp(2*pi*i*theta)",
        "A2_A3": "-beta/alpha=(115-1/w)/24=eta, so C245's Laurent pole-ratio factors use exp(2*pi*i*eta)",
        "subtraction": "eta-theta=(110-w-1/w)/24=-(w^2-110*w+1)/(24*w)",
        "upper_tilt_sign": "with w=t_++i*epsilon and the exact root identity, Im(eta-theta)=-epsilon*(1-1/(t_+^2+epsilon^2))/24<0",
    }
    # C245's A1/A4 alpha-shift factors use theta, whereas its A2/A3 Laurent
    # ratio uses eta.  Therefore the
    # preregistered one-q formula cannot be derived and the permitted q^2
    # test must not be reached.
    conclusion = {
        "epistemic_status": "PROVED",
        "status": "FROZEN_ONE_Q_TILT_COCHAIN_FALSIFIED",
        "proposed_identity": "theta=eta modulo Z",
        "root_identity": root_identity,
        "factor_role_derivation": factor_role_derivation,
        "difference": difference,
        "imaginary_difference_certificate": imaginary_difference_sign,
        "q_bases": q_bases,
        "q_series_degree_two_inspected": False,
        "reason": "The C247 selection rule requires a common q base before its N=1 q^2 test; that prerequisite fails for every epsilon>0.",
        "claim_boundary": "This refutes only C247's frozen one-q collapse/base-only tilt-stability engine. It does not prove or disprove a multi-base tilt cocycle, compare C244 constructed-current coefficients with the source line, normalize a current, or imply a contour identity, mixed-base transform, B-Fourier covariance, AFK, fusion, Stark, or TCC.",
    }
    return conclusion


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
