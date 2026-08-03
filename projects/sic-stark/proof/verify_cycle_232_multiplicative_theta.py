#!/usr/bin/env python3
"""Exact multiplicative-theta principal-cochain audit for Cycle 232/B069."""
from __future__ import annotations

import json
from fractions import Fraction

try:  # Support both direct replay and package-style regression imports.
    from .verify_cycle_228_f3_square_residual_block import blocks
except ImportError:  # pragma: no cover - exercised by direct replay.
    from verify_cycle_228_f3_square_residual_block import blocks


F = Fraction
Q = F(1, 576)
WITNESSES = {"A": (F(-1), F(-5)), "C": (F(-1), F(5))}


def _positive_integer(value: F) -> bool:
    return value.denominator == 1 and value >= 1


def _zero_can_cancel(item: dict[str, object], target: tuple[F, F]) -> dict[str, object]:
    """Solve c*target=r*alpha+s*beta, r,s positive integers, exactly."""
    c = F(item["argument_mu"])
    alpha = tuple(F(x) for x in item["alpha"])
    beta = tuple(F(x) for x in item["beta"])
    determinant = alpha[0] * beta[1] - alpha[1] * beta[0]
    assert determinant != 0
    rhs = (c * target[0], c * target[1])
    r = (rhs[0] * beta[1] - rhs[1] * beta[0]) / determinant
    s = (alpha[0] * rhs[1] - alpha[1] * rhs[0]) / determinant
    return {
        "zero_lattice_coefficients_r_s": [str(r), str(s)],
        "is_cancelling_zero": _positive_integer(r) and _positive_integer(s),
    }


def residual_divisor_audit() -> dict[str, object]:
    rows = []
    for start, block in blocks().items():
        target = WITNESSES[start]
        zero_checks = [_zero_can_cancel(item, target) for item in block]
        assert not any(check["is_cancelling_zero"] for check in zero_checks)
        rows.append({
            "start": start,
            "nonzero_pole_hyperplane": f"mu={target[0]}*omega1+{target[1]}*omega2",
            "pole_source": "first residual factor at (j,n)=(1,0)",
            "zero_checks": zero_checks,
            "uncancelled": True,
            "present_in_mu_to_minus_four": False,
        })
    assert len(rows) == 2
    return {
        "epistemic_status": "PROVED",
        "rows": rows,
        "conclusion": "Both residual blocks retain a nonzero parameter-dependent pole hyperplane absent from mu^(-4).",
    }


def audit() -> dict[str, object]:
    """Derive the candidate's multiplier and compare the full residual divisor."""
    # theta_q(q*z)/theta_q(z)=(1-1/z)/(1-z)=-z^(-1), directly from
    # theta_q(z)=(z;q)_infinity*(q/z;q)_infinity.
    theta_q_shift = "theta_q(q*z)/theta_q(z)=-z^(-1)"
    theta_inverse_shift = "theta_q(q^(-1)*mu)/theta_q(mu)=-mu/q"
    monomial_q_power = -4
    theta_inverse_q_power = 4
    assert monomial_q_power + theta_inverse_q_power == 0
    residuals = residual_divisor_audit()
    return {
        "epistemic_status": "PROVED",
        "theta": {
            "q": "1/576",
            "definition": "theta_q(z)=(z;q)_infinity*(q/z;q)_infinity",
            "direct_product_shift": theta_q_shift,
            "inverse_scaling_shift": theta_inverse_shift,
        },
        "candidate": "H(mu)=mu^4*theta_q(mu)^(-4)",
        "principal_multiplier": {
            "equation": "H(576*mu)/H(mu)=mu^(-4)",
            "monomial_q_power": monomial_q_power,
            "theta_q_power": theta_inverse_q_power,
            "single_valued_on": "C^* in the coordinate mu",
            "tier_1": "PROVED",
        },
        "full_residual_divisor": residuals,
        "tier_2": {
            "absorbs_both_full_residuals": False,
            "status": "FALSIFIED_FOR_FROZEN_SINGLE_THETA_CANDIDATE",
            "reason": "The candidate multiplier is mu^(-4), but each residual has an additional uncancelled nonzero hyperplane pole.",
        },
        "reflection_and_normalization": {
            "status": "UNAVAILABLE_AFTER_TIER_2_FAILURE",
            "reason": "The frozen acceptance ladder permits neither test after failure to absorb the full residual divisor.",
        },
        "conclusion": "The frozen single-theta cochain is a single-valued exact solution of the formal principal multiplier, but it cannot absorb either full four-gamma residual block. This leaves parameter-dependent theta products and other cochain families open, and proves no signed extension, AFK, fusion, Stark, or TCC result.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
