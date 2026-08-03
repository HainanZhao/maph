#!/usr/bin/env python3
"""Exact direct-embedding audit for Cycle 239/B076.

The audit is deliberately literal: it tests whether the frozen C228 word is
itself the kernel of the one frozen S--S rarefied beta theorem.  It does not
try to manufacture the theorem's complementary factors or a new composition.
"""
from __future__ import annotations

import json
from fractions import Fraction

try:
    from .verify_cycle_226_signed_product_groupoid import NODES, f3, node_name
    from .verify_cycle_228_f3_square_residual_block import blocks
except ImportError:  # pragma: no cover - direct replay
    from verify_cycle_226_signed_product_groupoid import NODES, f3, node_name
    from verify_cycle_228_f3_square_residual_block import blocks


F = Fraction


def _slope(item: dict[str, object]) -> Fraction:
    return F(str(item["argument_mu"]))


def _factor_has_period_constant(item: dict[str, object]) -> bool:
    # C228 pins every displayed ordinary-gamma argument to c*mu, without a
    # period constant.  No source shift is admitted in this direct audit.
    return False


def _audit_block(start: str, block: list[dict[str, object]]) -> dict[str, object]:
    slopes = [_slope(item) for item in block]
    assert len(block) == 4
    assert all(slope > 0 for slope in slopes)
    assert not any(_factor_has_period_constant(item) for item in block)

    # The two C228 F3 residual pairs have source raw states start and F3(start).
    # Equation (17) supplies those pairs; no equality of their two rarefied
    # lens data is printed by the source.
    edge_states = [start, node_name(f3(NODES[start]))]
    assert len(set(edge_states)) == 2

    negative_slope_partner_present = {
        str(slope): (-slope in slopes) for slope in sorted(set(slopes))
    }
    assert not any(negative_slope_partner_present.values())

    conditions = {
        "one_fixed_rarefied_lens_state": {
            "required_by_source": "all twelve numerator factors use one fixed Gamma_M(mu,m;omega1,omega2)",
            "C228_exact_data": {"equation_17_source_states": edge_states},
            "satisfied": False,
            "reason": "the two retained F3 residual pairs come from distinct raw rarefied states; no frozen source theorem identifies them as one fixed Gamma_M system",
        },
        "six_plus_minus_pairs": {
            "required_by_source": "Gamma_M(a_j+mu,n_j+m) Gamma_M(a_j-mu,n_j-m) for j=1,...,6",
            "C228_exact_data": {
                "factor_count": len(block),
                "all_affine_period_constants_zero": True,
                "positive_mu_slopes": [str(slope) for slope in slopes],
                "negative_slope_partner_present": negative_slope_partner_present,
            },
            "satisfied": False,
            "reason": "an unshifted displayed factor can match a_j plus/minus mu only with a_j=0, which requires its opposite-slope companion at the same source lane; none occurs",
        },
        "complete_kernel_and_denominator": {
            "required_by_source": "twelve numerator Gamma_M factors and Gamma_M(plus/minus 2mu,plus/minus 2m) in the denominator",
            "C228_exact_data": {"retained_word_factor_count": len(block), "displayed_denominator": False},
            "satisfied": False,
            "reason": "the frozen word is not the displayed beta kernel; adding its eight missing numerator factors or its denominator is prohibited",
        },
        "balancing": {
            "required_by_source": "sum a_j=omega1+omega2 and sum n_j=r-1",
            "satisfied": False,
            "reason": "there is no complete six-parameter kernel to which the source balancing equations can be assigned",
        },
        "contour_and_discrete_sum": {
            "required_by_source": "the source sum over Z_k+nu and a separating convergent contour for the completed kernel",
            "satisfied": False,
            "reason": "without the source kernel there is no source-defined pole separation or contour to test",
        },
        "word_output": {
            "required_by_source": "the evaluated product over ell<j is mapped to the required reversed residual word with all data retained",
            "satisfied": False,
            "reason": "the integral is inapplicable, so its parameter-only output cannot be identified with the free-mu ordered word",
        },
    }
    assert not any(item["satisfied"] for item in conditions.values())
    return {"start": start, "conditions": conditions, "direct_embedding": False}


def audit() -> dict[str, object]:
    rows = [_audit_block(start, block) for start, block in blocks().items()]
    assert [row["start"] for row in rows] == ["A", "C"]
    assert not any(row["direct_embedding"] for row in rows)
    return {
        "epistemic_status": "PROVED",
        "source_identity": {
            "citation": "Sarkissian--Spiridonov, arXiv:1910.11747v4, equation (42)",
            "identity_kind": "rarefied hyperbolic beta integral / star-triangle form",
            "fixed_period_system_count": 1,
            "numerator_pair_count": 6,
            "numerator_factor_count": 12,
            "denominator_required": True,
            "balancing_required": True,
            "contour_and_discrete_sum_required": True,
            "output_is_parameter_only": True,
        },
        "blocks": rows,
        "status": "FALSIFIED_DIRECT_RAREFIED_BETA_KERNEL_EMBEDDING",
        "conclusion": "Neither C228 residual word is the kernel or output of the frozen rarefied beta theorem. The direct application fails the fixed-lens, plus/minus-pair, complete-kernel, balancing, contour, and output conditions. This contains only this literal theorem application; a different multi-kernel identity or a separately proved composition theorem remains open.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
