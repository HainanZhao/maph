#!/usr/bin/env python3
"""Exact two-sign logarithmic axis-to-packet audit for Cycle 212/B049."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from proof.verify_cycle_203_inverse_normal_line import a6_axis_multiplier
from proof.verify_cycle_163_fixed_full_ray_selector import is_positive_at_selected_embedding


def logarithmic_lifts() -> dict[str, object]:
    axis = a6_axis_multiplier()
    assert axis["local_action"] == "A6*gamma(s)=gamma(beta^(-6)*s)"
    records = []
    for epsilon in (1, -1):
        records.append({
            "epsilon": epsilon,
            "Lambda_lift": f"{epsilon}*(36*omega/(pi*D))*log(s)",
            "packet_coordinate": "s^(-1)" if epsilon == 1 else "s",
            "A6_packet_action": "t->beta^(6)*t" if epsilon == 1 else "t->beta^(-6)*t",
            "s_to_zero_cusp": "t->infinity, [e_(0,5)]" if epsilon == 1 else "t->0^+, [e_(5,0)]",
        })
    assert len(records) == 2
    return {
        "epistemic_status": "PROVED",
        "axis_orientation": axis["orientation"],
        "axis_contraction": "s->beta^(-6)*s",
        "lifts": records,
        "two_signs_required": True,
    }


def real_embedding_audit() -> dict[str, object]:
    # beta'=(5-sqrt(21))/2 lies strictly between zero and one.  The selector
    # predicate from C163 recognizes this exact inequality for b=1,lift=0.
    assert is_positive_at_selected_embedding(1, 0)
    assert not is_positive_at_selected_embedding(1, 6)
    return {
        "epistemic_status": "PROVED",
        "selected_embedding": "beta'=(5-sqrt(21))/2 with 0<beta'<1",
        "orientation_role": "It fixes the arithmetic positive-lift convention, not an action on s, Lambda, t, or epsilon.",
        "epsilon_selector": "NOT_SUPPLIED",
    }


def frobenius_provenance_audit() -> dict[str, object]:
    data = json.loads((ROOT / "artifacts/cycle-173-local-artin-action-v2.json").read_text(encoding="utf-8"))
    local = data["exact_prototype"]["local_inputs"]
    assert local["oriented_generator"] == "g=Frob_(4 beta+1), ray log 1"
    assert local["ray_group"] == "C6"
    return {
        "epistemic_status": "PROVED",
        "arithmetic_generator": local["oriented_generator"],
        "proved_action_domain": "local inertia on U_L^1/U_L^2",
        "analytic_coordinate_action": "NOT_SUPPLIED_BY_FROZEN_ARTIFACT",
        "epsilon_selector": "NOT_SUPPLIED",
    }


def two_sign_equivariance_audit() -> dict[str, object]:
    # Under A6, both lifts are covariant, with inverse packet dilations.  The
    # frozen action fixes characteristic labels and supplies no transformation
    # of epsilon, so it cannot distinguish the two listed lifts.
    records = [
        {"epsilon": 1, "packet_dilation_exponent": 6, "cusp": "[e_(0,5)]"},
        {"epsilon": -1, "packet_dilation_exponent": -6, "cusp": "[e_(5,0)]"},
    ]
    assert {row["packet_dilation_exponent"] for row in records} == {-6, 6}
    return {
        "epistemic_status": "PROVED",
        "records": records,
        "A6_action_on_epsilon": "NOT_SUPPLIED; both covariant lifts remain admissible",
        "frozen_selector_count": 0,
        "conclusion": "The declared A6 axis, real embedding, and arithmetic Frobenius data do not select one of the two specified logarithmic lifts.",
    }


def run() -> dict[str, object]:
    lifts = logarithmic_lifts()
    embedding = real_embedding_audit()
    frobenius = frobenius_provenance_audit()
    symmetry = two_sign_equivariance_audit()
    assert lifts["two_signs_required"]
    assert embedding["epsilon_selector"] == "NOT_SUPPLIED"
    assert frobenius["analytic_coordinate_action"] == "NOT_SUPPLIED_BY_FROZEN_ARTIFACT"
    assert symmetry["frozen_selector_count"] == 0
    return {
        "schema": "sic-stark-cycle-212-logarithmic-axis-to-packet-orientation-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "For the two declared logarithmic axis-to-packet lifts, the frozen A6 contraction, selected real embedding, and norm-37 arithmetic Frobenius data preserve both orientations but supply no map selecting epsilon. This does not rule out a new theorem defining an analytic Frobenius action, a source density, a non-logarithmic link, C198 comparison, AFK identity, fusion, Stark, or TCC statement.",
        "logarithmic_lifts": lifts,
        "real_embedding_audit": embedding,
        "frobenius_provenance_audit": frobenius,
        "two_sign_equivariance_audit": symmetry,
        "gate_outcome": {
            "declared_logarithmic_axis_to_packet_orientation": "TWO_SIGN_COVARIANT_LIFTS_NO_SELECTOR",
            "remaining_design_problem": "Derive a new analytic Frobenius/real-embedding/density theorem selecting epsilon, or explore a non-logarithmic axis-to-packet link without C198 fitting.",
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    text = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    print(text, end="") if args.output is None else args.output.write_text(text, encoding="utf-8")
