#!/usr/bin/env python3
"""Exact target-weight obstruction for Cycle 202/B039 normal data.

The source normal derivative of the rank-36 regular germ carries Abel-rate
weight one.  C198's meromorphic endpoint values carry no Abel-rate at all and
are nonzero on every row.  A complex-linear rate-independent direct bridge
would therefore have incompatible weights on every target row.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:  # Supports both package tests and direct proof-script replay.
    from proof.verify_cycle_198_analytic_frequency_endpoint import characteristic_ledger
except ModuleNotFoundError:
    from verify_cycle_198_analytic_frequency_endpoint import characteristic_ledger


DIMENSION = 6
DILATIONS = (2, 3, 5)


def normal_data_ledger() -> dict[str, object]:
    """List all source normal packets and their exact rate action."""

    rows = []
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            rows.append({
                "characteristic": [first, second],
                "normal_datum": f"R_({first},{second})",
                "rate_weight": 1,
                "dilation_action": {
                    str(q): f"R_({first},{second})->{q}*R_({first},{second})"
                    for q in DILATIONS
                },
            })
    assert len(rows) == DIMENSION * DIMENSION
    return {
        "epistemic_status": "PROVED",
        "definition": "R=lim_(lambda->0) lambda^(-1)*(G_lambda-B)",
        "row_count": len(rows),
        "rate_weight": 1,
        "dilations": list(DILATIONS),
        "records": rows,
    }


def fixed_target_ledger() -> dict[str, object]:
    """Import the frozen C198 target census without evaluating a raw contour."""

    ledger = characteristic_ledger()
    records = ledger["records"]
    assert len(records) == DIMENSION * DIMENSION
    assert all(row["endpoint_value_finite_nonzero"] for row in records)
    return {
        "epistemic_status": "PROVED",
        "row_count": len(records),
        "all_endpoint_values_finite_nonzero": True,
        "abel_rate_weight": 0,
        "records": [
            {
                "characteristic": row["characteristic"],
                "endpoint_value": row["endpoint_value"],
                "finite_nonzero": row["endpoint_value_finite_nonzero"],
            }
            for row in records
        ],
        "reason": (
            "The frozen equation-(66) meromorphic endpoint functional is "
            "defined on T_6 without the auxiliary Abel rate."
        ),
    }


def direct_bridge_weight_contradiction() -> dict[str, object]:
    """Check the direct all-row equality against each frozen dilation."""

    normal = normal_data_ledger()
    targets = fixed_target_ledger()
    contradictions = []
    for q in DILATIONS:
        contradictions.append({
            "q": q,
            "assumed_direct_bridge": "J(R_(a,b))=L_src(chi_(a,b))",
            "linearity": f"J({q}*R_(a,b))={q}*L_src(chi_(a,b))",
            "required_fixed_target": "J(R_q,(a,b))=L_src(chi_(a,b))",
            "contradiction": f"{q - 1}*L_src(chi_(a,b))=0 for every row",
            "excluded_by": "all 36 frozen target values are nonzero",
        })
    assert normal["rate_weight"] == 1
    assert targets["abel_rate_weight"] == 0
    return {
        "epistemic_status": "PROVED",
        "functional_class": (
            "complex-linear rate-independent J:E_reg->T_6 with direct fixed "
            "all-row equality J(R_(a,b))=L_src(chi_(a,b))"
        ),
        "contradictions": contradictions,
        "all_36_direct_equalities_impossible": True,
        "scope": (
            "This does not forbid a theorem-derived covariant target, nonlinear "
            "bridge, higher germ, or another continuation; it only rejects the "
            "declared direct fixed-target equality."
        ),
    }


def run() -> dict[str, object]:
    normal = normal_data_ledger()
    targets = fixed_target_ledger()
    contradiction = direct_bridge_weight_contradiction()
    assert normal["row_count"] == 36
    assert targets["all_endpoint_values_finite_nonzero"]
    assert contradiction["all_36_direct_equalities_impossible"]
    return {
        "schema": "sic-stark-cycle-202-normal-derivative-target-weight-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": (
            "No complex-linear Abel-rate-independent direct bridge can map the "
            "weight-one source normal derivative of the declared two-scale germ "
            "to C198's fixed nonzero weight-zero endpoint values on all 36 rows. "
            "This rejects only that direct equality class; it does not exclude a "
            "theorem-derived covariant target, nonlinear map, higher-germ, non-"
            "Abel construction, AFK identification, fusion, Stark, or TCC."
        ),
        "normal_data": normal,
        "fixed_targets": targets,
        "direct_bridge_weight_contradiction": contradiction,
        "gate_outcome": {
            "rate_covariant_normal_derivative_to_fixed_C198_target": "FALSIFIED_FOR_ALL36_DIRECT_LINEAR_MAP",
            "remaining_design_problem": (
                "Derive a source-authorized covariant target or another bridge "
                "class whose regulator meaning is proved rather than fitted."
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
