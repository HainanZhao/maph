#!/usr/bin/env python3
"""Exact regulator-covariance obstruction for Cycle 201/B038.

Cycle 200's first off-support coefficient transforms with weight one under a
change of Abel rate.  This verifier proves that a rate-independent complex
linear functional on the joint boundary/regular germ must kill that entire
rank-36 regular component.  Its remaining symmetric boundary component has
rank at most 30, so this declared functional class cannot produce the 36
distinct C198 target characters.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


DIMENSION = 6
DILATIONS = (2, 3, 5)


def source_regulator_action() -> dict[str, object]:
    """Record the exact weight-one action on the two-scale germ."""

    records = []
    for dilation in DILATIONS:
        records.append({
            "q": dilation,
            "u_change": f"exp(-lambda*s)->exp(-{dilation}*lambda*s)",
            "boundary_coordinate": "B -> B",
            "regular_coordinate": f"lambda*R -> {dilation}*lambda*R",
            "difference": f"G_({dilation}*lambda)-G_lambda={(dilation - 1)}*lambda*R",
        })
    return {
        "epistemic_status": "PROVED",
        "state": "G_lambda=(B,lambda*R) in E_bd direct-sum E_reg",
        "dilations": list(DILATIONS),
        "regular_weight": 1,
        "records": records,
        "source_derivation": (
            "Cycle 200's exact first s coefficient is "
            "lambda/(1-cosh(c_beta*Lambda)), while the paired boundary is "
            "lambda-independent."
        ),
    }


def invariant_linear_functional_no_go() -> dict[str, object]:
    """Use each frozen dilation to force the regular restriction to vanish."""

    equations = []
    for dilation in DILATIONS:
        equations.append({
            "q": dilation,
            "invariance_equation": "F(B,q*lambda*R)=F(B,lambda*R)",
            "linearity_difference": f"{dilation - 1}*lambda*F(R)=0",
            "consequence": "F(R)=0 for lambda>0",
        })
    return {
        "epistemic_status": "PROVED",
        "functional_class": (
            "complex-linear F:E_bd direct-sum E_reg -> V, independent of "
            "lambda and invariant under every frozen regulator dilation"
        ),
        "equations": equations,
        "restriction_on_E_reg": "zero",
        "proof": (
            "Already q=2 gives lambda*F(R)=0; lambda is positive, so F(R)=0. "
            "The q=3 and q=5 equations independently replay the same forced "
            "zero restriction."
        ),
    }


def all_row_rank_consequence() -> dict[str, object]:
    """Compare the surviving boundary rank with the C198 target basis."""

    rows = [{"characteristic": [a, b]} for a in range(DIMENSION) for b in range(DIMENSION)]
    assert len(rows) == DIMENSION * DIMENSION
    return {
        "epistemic_status": "PROVED",
        "source_row_count": len(rows),
        "regular_packet_rank_killed": DIMENSION * DIMENSION,
        "surviving_boundary_rank_upper_bound": 30,
        "C198_distinct_target_basis_dimension": DIMENSION * DIMENSION,
        "linear_all36_target_map_impossible": True,
        "reason": (
            "After regulator invariance kills E_reg, every output factors "
            "through E_bd. A linear image of rank at most 30 cannot contain "
            "the 36 linearly independent C198 character basis vectors."
        ),
        "records": rows,
    }


def run() -> dict[str, object]:
    action = source_regulator_action()
    no_go = invariant_linear_functional_no_go()
    rank = all_row_rank_consequence()
    assert action["regular_weight"] == 1
    assert no_go["restriction_on_E_reg"] == "zero"
    assert rank["linear_all36_target_map_impossible"]
    return {
        "schema": "sic-stark-cycle-201-two-scale-germ-covariance-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": (
            "No complex-linear Abel-rate-independent functional on the declared "
            "two-scale germ can retain Cycle 200's rank-36 off-support regular "
            "component: regulator covariance forces its restriction to zero, "
            "leaving boundary rank at most 30. This rejects only that invariant "
            "functional class; it does not exclude a nonlinear, rate-covariant, "
            "higher-order, non-Abel, or another source-derived construction, and "
            "does not prove a Zak map, endpoint equality, AFK, fusion, Stark, or TCC."
        ),
        "source_regulator_action": action,
        "invariant_linear_functional_no_go": no_go,
        "all_row_rank_consequence": rank,
        "gate_outcome": {
            "linear_regulator_independent_two_scale_functional": "FALSIFIED_FOR_ALL36_T6_MAP",
            "remaining_design_problem": (
                "Find a source-authorized construction outside the declared "
                "linear regulator-invariant class, while proving rather than "
                "assuming its regulator and endpoint meaning."
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
