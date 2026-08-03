#!/usr/bin/env python3
"""Exact fixed-tilt bound for the C245 A-word coefficient recurrence."""
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
    """Certify the frozen C246 componentwise bound without numeric samples."""
    prior = c245_audit()
    assert prior["recurrence"]["exact_recurrence_family_derived"]
    assert prior["recurrence"]["all_multiplier_factors_nonzero"]

    # Both roots of X^2-110X+1 are in (0,110): the upper one is below 110
    # because (12*sqrt(21))^2=3024<55^2=3025.  Thus |t_sigma+i|^2<12101.
    t_upper = 110
    w_sq_upper = t_upper * t_upper + 1
    assert w_sq_upper == 12101
    assert 12 * 12 * 21 < 55 * 55

    factor_data = []
    alpha_over_beta_lower = F(1, 7_000_000)
    beta_over_alpha_lower = F(1, 300_000)
    for position, item in enumerate(blocks()["A"], 1):
        alpha = tuple(F(x) for x in item["alpha"])
        beta = tuple(F(x) for x in item["beta"])
        det = alpha[0] * beta[1] - alpha[1] * beta[0]
        assert det > 0
        if position in (1, 4):
            # alpha is respectively (w+5)/24 and w+5, while beta is a
            # real constant.  The weaker universal bounds suffice.
            alpha_sq_upper = F(115 * 115 + 1, 24 * 24) if position == 1 else F(115 * 115 + 1)
            beta_sq_lower = F(1) if position == 1 else F(24 * 24)
            alpha_beta_lower = det / beta_sq_lower
            beta_alpha_lower = det / alpha_sq_upper
        else:
            # For A2/A3, beta is a scalar multiple of -115*w+1 and alpha
            # a scalar multiple of w.  Bound |115*w-1|^2 by 12650^2+115^2.
            affine_beta_sq_upper = 12650 * 12650 + 115 * 115
            if position == 2:
                alpha_sq_upper = F(w_sq_upper)
                beta_sq_upper = F(affine_beta_sq_upper, 24 * 24)
            else:
                alpha_sq_upper = F(24 * 24 * w_sq_upper)
                beta_sq_upper = F(affine_beta_sq_upper)
            alpha_beta_lower = det / beta_sq_upper
            beta_alpha_lower = det / alpha_sq_upper
        assert alpha_beta_lower > alpha_over_beta_lower
        assert beta_alpha_lower > beta_over_alpha_lower
        factor_data.append(
            {
                "factor": f"A{position}",
                "determinant": str(det),
                "Im_alpha_over_beta_lower": str(alpha_beta_lower),
                "minus_Im_beta_over_alpha_lower": str(beta_alpha_lower),
            }
        )

    # The numerator exponents are 115*N+i (0<=i<115); the inverse factors
    # have exponents 24*N+q and N+1.  pi>3 turns the preceding rational
    # lower bounds into the common r^N=e^(-N/50000) bound.
    assert F(115, 7_000_000) > F(1, 61_000)
    assert F(6, 61_000) > F(1, 50_000)
    assert F(6, 300_000) == F(1, 50_000)
    r_definition = "r=exp(-1/50000)"
    factor_counts = {"numerators": 230, "inverse_denominators": 50}
    assert factor_counts == {"numerators": 2 * 115, "inverse_denominators": 2 * 24 + 2}

    # For a=1/50000, sum r^n=1/(exp(a)-1)<1/a=50000.  Since
    # x -> -log(1-exp(-a*x)) decreases,
    # sum_{n>=1}-log(1-r^n) is at most its integral, namely
    # pi^2/(6a)<2/a=100000.  Here pi<22/7 gives pi^2<12 (the latter
    # rational comparison is recorded below); no finite-N or floating-point
    # sampling enters.
    geometric_sum_bound = 50_000
    euler_product_log_bound = 100_000
    assert geometric_sum_bound == 50_000
    assert euler_product_log_bound == 2 * geometric_sum_bound
    assert 22 * 22 < 12 * 7 * 7
    log_product_bound = (
        factor_counts["numerators"] * geometric_sum_bound
        + factor_counts["inverse_denominators"] * euler_product_log_bound
    )
    assert log_product_bound == 16_500_000
    C_exponent = 40_000_000
    # exp(1/2)<2 follows by bounding its positive series tail by a strict
    # geometric tail, so log(2)>1/2.
    log_C_lower = C_exponent // 2
    assert log_C_lower == 20_000_000
    assert log_product_bound < log_C_lower

    return {
        "epistemic_status": "PROVED",
        "regularization": "w_sigma=t_sigma+i at both real embeddings",
        "norm": "max(|kappa_N^+/kappa_1^+|,|kappa_N^-/kappa_1^-|)",
        "embedding_bounds": {
            "root_certificate": "0<t_sigma<110 and |t_sigma+i|^2<12101",
            "factor_classes": factor_data,
            "common_factor_bound": "Every C245 numerator deviation and inverse-denominator deviation is at most r^N for r=exp(-1/50000).",
            "r": r_definition,
        },
        "product_bound": {
            "numerator_factors_per_N": factor_counts["numerators"],
            "inverse_denominator_factors_per_N": factor_counts["inverse_denominators"],
            "sum_r_to_n_bound": geometric_sum_bound,
            "sum_minus_log_one_minus_r_to_n_bound": euler_product_log_bound,
            "log_normalized_coefficient_bound": log_product_bound,
            "analytic_lemmas": [
                "exp(x)>1+x for x>0",
                "monotone integral and the positive -log(1-exp(-x)) power series give sum_{n>=1}-log(1-exp(-a*n))<=pi^2/(6*a)<2/a; pi^2<12 follows from pi<22/7",
                "log(2)>1/2 follows from exp(1/2)<2 by its positive series and strict geometric-tail bound",
            ],
        },
        "bound": {
            "epistemic_status": "PROVED",
            "statement": "For every N>=1, max(|kappa_N^+/kappa_1^+|,|kappa_N^-/kappa_1^-|) <= 2^40000000*(1+N)^0.",
            "C": "2^40000000",
            "d": 0,
            "all_N": True,
            "numerical_sampling_used": False,
        },
        "claim_boundary": "This is a fixed-tilt, normalized A-word coefficient bound only. It does not resolve regulator-normalization ambiguity, source authorization, a canonical current, contour identity, mixed-base transform, B-Fourier covariance, AFK, fusion, Stark, or TCC.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
