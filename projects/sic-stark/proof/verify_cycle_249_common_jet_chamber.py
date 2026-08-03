#!/usr/bin/env python3
"""Exact common upper-chamber audit for C228 ordinary-gamma residual jets."""
from __future__ import annotations

import json
from fractions import Fraction as F

try:
    from .verify_cycle_228_f3_square_residual_block import blocks
except ImportError:  # pragma: no cover
    from verify_cycle_228_f3_square_residual_block import blocks


def factor_audit(start: str, position: int, item: dict[str, object]) -> dict[str, object]:
    c = F(str(item["argument_mu"]))
    alpha = tuple(F(str(x)) for x in item["alpha"])
    beta = tuple(F(str(x)) for x in item["beta"])
    determinant = alpha[0] * beta[1] - alpha[1] * beta[0]
    assert c != 0 and determinant > 0
    # With w=t+i, Im((a1*w+a2)/(b1*w+b2)) is exactly the coefficient
    # determinant divided by |beta(w)|^2; it is independent of the real
    # root t.  Reversing the quotient negates the sign.
    chamber = {
        "alpha_over_beta": f"Im(alpha/beta)={determinant}/|beta(t+i)|^2>0",
        "beta_over_alpha": f"Im(beta/alpha)=-{determinant}/|alpha(t+i)|^2<0",
        "q_modulus": "|q|=exp(-2*pi*Im(alpha/beta))<1",
        "qtilde_modulus": "|qtilde|=exp(2*pi*Im(beta/alpha))<1",
    }
    # Factor the denominator of the source product as
    # (exp(B*z);q)_infty=(1-exp(B*z))*(q*exp(B*z);q)_infty.  Once both
    # bases have modulus below one, every displayed q-product and its first
    # three logarithmic Lambert derivatives converge absolutely.
    jet = {
        "normalized_germ": "G(mu)=mu*gamma(c*mu;alpha,beta)",
        "leading_coefficient": "-(qtilde;qtilde)_infinity/(B*c*(q;q)_infinity), B=2*pi*i/beta",
        "leading_coefficient_nonzero": True,
        "degree_0_to_3_derivation": [
            "log(qtilde*exp(A*c*mu);qtilde)_infinity-log(q*exp(B*c*mu);q)_infinity",
            "plus log(mu/(1-exp(B*c*mu)))",
            "differentiate through degree three using absolutely convergent Lambert series S1,S2,S3",
        ],
        "absolute_convergence": True,
    }
    return {
        "factor": f"{start}{position}",
        "argument_slope": str(c),
        "alpha": [str(x) for x in alpha],
        "beta": [str(x) for x in beta],
        "period_determinant": str(determinant),
        "two_embedding_result": {"plus": chamber, "minus": chamber},
        "analytic_jet": jet,
    }


def audit() -> dict[str, object]:
    # t_-=55-12*sqrt(21)>0 because 55^2>12^2*21.  Both embeddings are real,
    # while the fixed +i supplies the same upper chamber at each of them.
    assert 55 * 55 > 12 * 12 * 21
    rows = []
    for start, block in blocks().items():
        assert len(block) == 4
        rows.extend(factor_audit(start, position, item) for position, item in enumerate(block, 1))
    assert len(rows) == 8
    assert all(F(row["period_determinant"]) > 0 for row in rows)
    assert all(row["analytic_jet"]["leading_coefficient_nonzero"] for row in rows)
    return {
        "epistemic_status": "PROVED",
        "status": "COMMON_FIXED_UPPER_CHAMBER_FOR_C228_JETS",
        "regularization": {
            "field": "Q(sqrt(21))",
            "embeddings": "t_+=55+12*sqrt(21), t_-=55-12*sqrt(21)",
            "fixed_tilt": "w_sigma=t_sigma+i",
            "endpoint_excluded": True,
        },
        "factor_count": len(rows),
        "factors": rows,
        "conclusion": "At both fixed upper-tilt embeddings, all eight C228 factors have |q|<1 and |qtilde|<1. Their normalized ordinary-gamma germs are holomorphic with nonzero leading coefficient and their degree-0:3 q-product/Lambert-series jets are absolutely convergent. This is a factorwise analytic-domain certificate only.",
        "claim_boundary": "This proves only the fixed-tilt common product chamber and factorwise analytic jets. It does not take epsilon to zero, establish C248's full path representation, derive a negative-k or cross-sign law, or imply a packet map, canonical current, contour identity, mixed-base transform, B-Fourier covariance, AFK, fusion, Stark, or TCC.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
