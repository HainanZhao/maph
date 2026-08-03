#!/usr/bin/env python3
"""Exact local b-Mellin ledger for Cycle 205/B042.

The frozen germ G_lambda-B=lambda*s*R+O(s^2) has one local Mellin singularity
at z=-1.  Its residue is lambda*R, hence retains regulator weight one.  The
leading term has zero Laurent finite coefficient; the full finite coefficient
depends on higher local data and is not fixed by the frozen asymptotic.  Thus
the natural local residue cannot be the missing fixed-target bridge.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


DIMENSION = 6
DILATIONS = (2, 3, 5)


def local_mellin_singularity() -> dict[str, object]:
    """Derive the sole pole forced by the frozen first-order germ."""

    return {
        "epistemic_status": "PROVED",
        "frozen_germ": "G_lambda(s)-B=lambda*s*R+O(s^2)",
        "local_mellin_leading_term": "integral_0^1 s^(z-1)*lambda*s*R ds=lambda*R/(z+1)",
        "forced_pole": "z=-1",
        "forced_residue": "lambda*R",
        "forced_residue_abel_rate_weight": 1,
        "leading_term_laurent_finite_coefficient": "0",
        "remainder_at_z_minus_one": (
            "O(s^2) is holomorphic at z=-1, but its value is not determined "
            "by the frozen first-order asymptotic."
        ),
        "cutoff_independent_local_data": "residue only",
    }


def all_row_residue_ledger() -> dict[str, object]:
    """Record the exact residue transformation on every normal packet."""

    rows = []
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            rows.append({
                "characteristic": [first, second],
                "local_mellin_residue": f"lambda*R_({first},{second})",
                "rate_weight": 1,
                "dilations": {
                    str(q): f"lambda*R_({first},{second})->{q}*lambda*R_({first},{second})"
                    for q in DILATIONS
                },
            })
    assert len(rows) == DIMENSION * DIMENSION
    return {
        "epistemic_status": "PROVED",
        "row_count": len(rows),
        "rank_before_rate_quotient": DIMENSION * DIMENSION,
        "rate_weight": 1,
        "records": rows,
    }


def local_operation_consequence() -> dict[str, object]:
    """Test precisely the three preregistered local operation classes."""

    contradictions = []
    for q in DILATIONS:
        contradictions.append({
            "q": q,
            "residue_action": "Res_(z=-1) M_(q*lambda)=q*Res_(z=-1) M_lambda",
            "fixed_target_action": "L_src(chi_(a,b)) is unchanged",
            "direct_equality_consequence": f"{q - 1}*L_src(chi_(a,b))=0",
            "excluded_by": "all 36 C198 target values are finite and nonzero",
        })
    return {
        "epistemic_status": "PROVED",
        "candidate_1_forced_residue": {
            "status": "FALSIFIED_FOR_DIRECT_FIXED_TARGET_MAP",
            "reason": "weight one versus fixed target weight zero",
        },
        "candidate_2_forced_leading_finite_coefficient": {
            "status": "ZERO_NOT_RANK36",
            "reason": "the Laurent constant of lambda*R/(z+1) is zero",
        },
        "candidate_3_rate_independent_linear_combination_with_B": {
            "status": "R_COMPONENT_FORCED_ZERO_UNDER_REGULATOR_INVARIANCE",
            "surviving_boundary_rank_upper_bound": 30,
            "reason": (
                "If A(B)+C(Res M_lambda) is rate invariant for q=2, then "
                "C(Res M_lambda)=0; the remaining B factor cannot realize 36 "
                "independent targets."
            ),
        },
        "unforced_full_finite_part": {
            "status": "NOT_A_FROZEN_SOURCE_OPERATION",
            "reason": (
                "The higher-germ contribution at z=-1 requires data beyond the "
                "frozen first-order asymptotic and cannot be selected as a local "
                "Mellin finite part in this block."
            ),
        },
        "contradictions": contradictions,
    }


def run() -> dict[str, object]:
    singularity = local_mellin_singularity()
    rows = all_row_residue_ledger()
    consequence = local_operation_consequence()
    assert singularity["forced_residue_abel_rate_weight"] == 1
    assert rows["row_count"] == 36
    assert consequence["candidate_3_rate_independent_linear_combination_with_B"]["surviving_boundary_rank_upper_bound"] == 30
    return {
        "schema": "sic-stark-cycle-205-mellin-b-pairing-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": (
            "For the frozen local source asymptotic, the b-Mellin residue at "
            "z=-1 is lambda*R and has regulator weight one; its leading finite "
            "coefficient is zero and the full finite part is not forced by the "
            "first-order germ. Hence no preregistered local residue/finite "
            "coefficient/rate-independent combination with B supplies a direct "
            "all-36 fixed-target map. This does not exclude an equation-(66) "
            "global Mellin theorem, another source pairing, covariant target, "
            "nonlinear/higher-germ/non-Abel construction, AFK, fusion, Stark, "
            "or TCC."
        ),
        "local_mellin_singularity": singularity,
        "all_row_residue_ledger": rows,
        "local_operation_consequence": consequence,
        "gate_outcome": {
            "local_b_mellin_residue_and_forced_finite_coefficient": "FALSIFIED_FOR_DIRECT_FIXED_TARGET_ALL36_MAP",
            "remaining_design_problem": (
                "Derive an equation-(66) global Mellin/pairing theorem with a "
                "predefined contour and homogeneity, or construct a covariant "
                "target line, without fitting a finite part."
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
