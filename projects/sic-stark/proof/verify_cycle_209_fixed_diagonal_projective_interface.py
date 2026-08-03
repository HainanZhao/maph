#!/usr/bin/env python3
"""Exact fixed-diagonal covariance test for Cycle 209/B046."""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path

try:
    from proof.verify_cycle_198_analytic_frequency_endpoint import characteristic_ledger
    from proof.verify_cycle_206_projective_line_interface import packet_monomial
except ModuleNotFoundError:
    from verify_cycle_198_analytic_frequency_endpoint import characteristic_ledger
    from verify_cycle_206_projective_line_interface import packet_monomial


DIMENSION = 6
WITNESS_T_VALUES = (Fraction(2), Fraction(3))


def source_ratio_audit() -> dict[str, object]:
    """Derive P_(0,1;h)/P_(0,0;h)=t^4 for every source channel."""
    records = []
    for h in range(DIMENSION):
        base = packet_monomial(0, 0, h)
        shifted = packet_monomial(0, 1, h)
        assert base["zeta_6_exponent_mod_6"] == shifted["zeta_6_exponent_mod_6"] == 0
        assert base["t_exponent"] == 0
        assert shifted["t_exponent"] == 4
        records.append({
            "h_channel": h,
            "source_ratio": "P_(0,1;h)(t)/P_(0,0;h)(t)=t^4",
            "source_phase_ratio": "1",
            "t_exponent_difference": 4,
        })
    assert len(records) == DIMENSION
    return {
        "epistemic_status": "PROVED",
        "records": records,
        "all_h_ratio": "t^4",
        "unselected_source_domain": "h in Z/6Z and t>0 with t!=1",
    }


def target_nonvanishing_audit() -> dict[str, object]:
    endpoint = characteristic_ledger()
    rows = endpoint["records"]
    by_label = {tuple(row["characteristic"]): row for row in rows}
    assert len(by_label) == DIMENSION * DIMENSION
    assert all(row["endpoint_value_finite_nonzero"] for row in rows)
    assert by_label[(0, 0)]["endpoint_value_finite_nonzero"]
    assert by_label[(0, 1)]["endpoint_value_finite_nonzero"]
    return {
        "epistemic_status": "PROVED",
        "target_coordinate_count": len(rows),
        "all_target_coordinates_finite_nonzero": True,
        "used_labels": [[0, 0], [0, 1]],
        "target_ratio_value": "NOT_EVALUATED",
    }


def fixed_diagonal_contradiction() -> dict[str, object]:
    values = [value**4 for value in WITNESS_T_VALUES]
    assert values == [Fraction(16), Fraction(81)]
    assert values[0] != values[1]
    return {
        "epistemic_status": "PROVED",
        "assumed_map_family": "J_c(e_(a,b))=c_(a,b)*chi_(a,b), with every c_(a,b) nonzero and independent of h,t",
        "assumed_projective_equality": "[c_(a,b)*P_(a,b;h)(t)]_(a,b)=[L_(a,b)]_(a,b) for every h and every admissible t>0, t!=1",
        "two_label_consequence": "t^4=(L_(0,1)*c_(0,0))/(L_(0,0)*c_(0,1)) for every admissible t",
        "witnesses": [
            {"t": str(t), "t_to_fourth": str(value)}
            for t, value in zip(WITNESS_T_VALUES, values)
        ],
        "constant_requirement": "The same nonzero right-hand-side constant must equal both 16 and 81.",
        "contradiction": True,
        "conclusion": "No fixed nonzero label-preserving diagonal J_c satisfies the declared all-h, all-t projective equality.",
    }


def run() -> dict[str, object]:
    source = source_ratio_audit()
    target = target_nonvanishing_audit()
    contradiction = fixed_diagonal_contradiction()
    assert source["all_h_ratio"] == "t^4"
    assert target["all_target_coordinates_finite_nonzero"]
    assert contradiction["contradiction"]
    return {
        "schema": "sic-stark-cycle-209-fixed-diagonal-projective-interface-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "No fixed nonzero label-preserving diagonal map realizes the declared all-h, all-t projective equality between the complete Cycle-206 source family and the fixed C198 point. This does not reject parameter-dependent, non-diagonal, nonlinear, selected-source-point, or other source-authorized interfaces, and proves no target minor identity, AFK, fusion, Stark, or TCC statement.",
        "source_ratio_audit": source,
        "target_nonvanishing_audit": target,
        "fixed_diagonal_contradiction": contradiction,
        "gate_outcome": {
            "fixed_diagonal_all_source_family_interface": "FALSIFIED",
            "remaining_design_problem": "Construct or falsify a parameter-dependent, non-diagonal, nonlinear, or differently sourced interface without endpoint fitting.",
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    text = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    print(text, end="") if args.output is None else args.output.write_text(text, encoding="utf-8")
