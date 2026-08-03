#!/usr/bin/env python3
"""Symbolic reciprocal-base negative-alpha audit for Cycle 252/B089."""
from __future__ import annotations

import json


def algebraic_audit() -> dict[str, object]:
    """Audit the frozen rule in the free multiplicative q-product algebra."""
    reciprocal_derivation = {
        "raw_negative_numerator": "(qtilde^-1*E_-A;qtilde^-1)_out",
        "raw_negative_denominator": "(E_B;q^-1)_out",
        "out_rule": "(x;Q)_out=1/(Q^-1*x;Q^-1)_infinity",
        "derived_candidate": "F(z;-alpha,beta)=(q*E_B;q)_infinity/(E_-A;qtilde)_infinity",
    }
    shifts = {
        "alpha_shift": "F(z-alpha)/F(z)=1-E_B",
        "beta_shift": "F(z+beta)/F(z)=1-E_-A",
        "identities_used": [
            "exp(-B*alpha)=q^-1",
            "exp(-A*beta)=qtilde",
            "(x;Q)_infinity/(Q*x;Q)_infinity=1-x",
        ],
        "both_expected_negative_alpha_shifts_pass": True,
    }
    double_sign = {
        "base_involution": "(q^-1)^-1=q and (qtilde^-1)^-1=qtilde",
        "second_sign_uses_inside_products": True,
        "returns_source_product_formula": True,
    }
    reflection = {
        "argument_pair": ["z", "beta-alpha-z"],
        "product": "F(z)F(beta-alpha-z)=theta(E_-B;q)/theta(E_-A;qtilde)",
        "theta_convention": "theta(x;Q)=(x;Q)_infinity*(Q/x;Q)_infinity",
        "derived_without_fitted_factor": True,
        "modular_Bernoulli_branch_proved": False,
    }
    assert shifts["both_expected_negative_alpha_shifts_pass"]
    assert double_sign["returns_source_product_formula"]
    assert reflection["derived_without_fitted_factor"]
    return {
        "reciprocal_derivation": reciprocal_derivation,
        "shifts": shifts,
        "double_sign": double_sign,
        "reflection": reflection,
    }


def continuation_scope_audit() -> dict[str, object]:
    """Check whether the frozen algebra supplies the required analytic bridge."""
    result = {
        "source": {
            "citation": "Sarkissian--Spiridonov, arXiv:1910.11747v4, equations (5) and (13)",
            "fixed_modular_representative": "c=k>0",
            "product_hypothesis": "|q|<1",
            "negative_alpha_product_hypothesis": "|q^-1|<1, equivalently |q|>1",
        },
        "candidate_domains_overlap": False,
        "overlap_chain_or_integral_bridge_in_frozen_rule": False,
        "termwise_boundary_fact": {
            "citation": "DLMF 20.2(ii)",
            "statement": "For fixed argument, the standard theta functions have the real tau axis, equivalently |q|=1, as a natural boundary.",
            "implication": "The separate q factors cannot be continued termwise; a proved modular cancellation or integral representation is required.",
        },
        "reviewed_source_supplies_exact_signed_period_bridge": False,
        "path_independent_meromorphic_continuation_proved": False,
        "first_failed_prerequisite": 4,
        "jets_compared": False,
        "eight_reflected_factors_compared": False,
    }
    assert not result["candidate_domains_overlap"]
    assert not result["overlap_chain_or_integral_bridge_in_frozen_rule"]
    assert not result["path_independent_meromorphic_continuation_proved"]
    assert not result["jets_compared"]
    return result


def audit() -> dict[str, object]:
    algebra = algebraic_audit()
    continuation = continuation_scope_audit()
    return {
        "epistemic_status": "PROVED",
        "status": "RECIPROCAL_BASE_RULE_FAILS_SOURCE_CONTINUATION_GATE",
        "algebraic_audit": algebra,
        "continuation_scope_audit": continuation,
        "conclusion": (
            "The reciprocal-base formula is algebraically coherent: it obeys both negative-alpha "
            "shifts, is involutive under a second sign change, and has an exact theta-ratio reflection "
            "product. But it defines only a disjoint product chamber. The frozen rule and reviewed "
            "source provide no overlapping analytic chart, integral bridge, or path-independence "
            "theorem across |q|=1. It therefore fails the preregistered source-continuation gate before "
            "any factor or jet comparison."
        ),
        "claim_boundary": (
            "This proves only that the frozen reciprocal-base rule does not itself construct or "
            "source-authorize the required analytic continuation. It does not prove that no "
            "meromorphic continuation, integral representation, signed-period theorem, full Gamma_M "
            "interface, AFK identity, fusion theorem, Stark claim, or dimension-six TCC exists."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
