#!/usr/bin/env python3
"""Reconcile two independent exact G1 envelope-sensitivity routes."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ROUTE_A = ROOT / "artifacts/g1-envelope-sensitivity-route-a-v1.json"
ROUTE_B = ROOT / "artifacts/g1-envelope-sensitivity-route-b-v1.json"
SCRIPT_A = ROOT / "proof/derive_g1_envelope_sensitivity_route_a_v1.py"
SCRIPT_B = ROOT / "proof/derive_g1_envelope_sensitivity_route_b_v1.py"
ATLAS = ROOT / "artifacts/cycle-3-g1-exact-structural-atlas-v2.json"
OUTPUT = ROOT / "artifacts/g1-envelope-sensitivity-reconciliation-v1.json"

PINS = {
    "route_a_artifact": (ROUTE_A, "40ea902852d319e0c6a2562e1bde07bd925cf46827c7ecb167e9bc16556c3cda"),
    "route_b_artifact": (ROUTE_B, "8f2649be1e543e321972a994471b5a147f9d6fd5df9a0245d94f2c18b72ad2a0"),
    "route_a_script": (SCRIPT_A, "014e36f1c9e942a5e298a6c893a3be921f22a3f9b29424ad40e5814b00c30404"),
    "route_b_script": (SCRIPT_B, "af65b7d1da0737e74e2f9d183034211ee458cae90e3c0a190caaa448637fbf1e"),
    "atlas_v2": (ATLAS, "fd66d17664ca921795617c6bfca76c3be49246ea9351644848a2aadf9e680b08"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def certificate() -> dict[str, Any]:
    require(sys.flags.optimize == 0, "G1 sensitivity reconciliation forbids -O/-OO")
    require(platform.python_implementation() == "CPython" and platform.python_version() == "3.12.3", "G1 sensitivity reconciliation requires CPython 3.12.3")
    hashes = {}
    for label, (path, expected) in PINS.items():
        observed = digest(path)
        require(observed == expected, "frozen dependency hash mismatch: " + str(path))
        hashes[label] = observed
    a, b = json.loads(ROUTE_A.read_text()), json.loads(ROUTE_B.read_text())
    require(a["epistemic_status"] == b["epistemic_status"] == "PROVED", "route status mismatch")
    require(a["frozen_inputs"]["hashes"]["atlas_v2"] == b["frozen_inputs"]["hashes"]["atlas_v2"] == hashes["atlas_v2"], "atlas pin disagreement")
    require(a["activity_counts"]["A_max_tie_counts"] == b["activity_count_replay"]["A_max_tie_counts"], "A activity count disagreement")
    require(a["activity_counts"]["C_outer_inner_tie_counts"] == b["activity_count_replay"]["C_outer_inner_tie_counts"], "C activity count disagreement")
    require(a["activity_counts"]["E_max_tie_counts_on_diagonal"] == b["activity_count_replay"]["E_max_tie_counts_on_diagonal"], "E activity count disagreement")
    a_zeroes = a["zero_B_residual_transfer_rows"]
    b_zeroes = b["zero_B_residuals"]["rows"]
    require([(row["id"], row["s"], row["zero_terms"], row["q"]) for row in a_zeroes] == [(row["id"], row["s"], [row["term"]], row["q"]) for row in b_zeroes], "zero-residual row disagreement")
    critical = a["critical_transfer"]
    barrier = b["critical_barrier"]
    require(critical["bottleneck"] == "LV3" and barrier["required_term"].startswith("Theorem 1.1 third term"), "named bottleneck disagreement")
    require(critical["B_minus_term"] == {"LV1": "3/13", "LV2": "1/13", "LV3": "0/1"}, "critical residual identity mismatch")
    a_formal = a["counterfactual_sensitivity"]
    b_formal = b["endpoint_and_conditional_propagation"]
    require(a_formal["published_range_no_effect"]["identity"] == "30/13-3/(2-s)=30*(7/10-s)/(13*(2-s))", "Route A endpoint identity changed")
    require(b_formal["published_endpoint_no_effect"]["identity"] == "30/13-3/(2-(7/10-h))=300h/(169+130h)", "Route B endpoint identity changed")
    require(a_formal["conditional_left_extension"]["crossing_equation"] == "300*h^2+(90-50*mu)*h-65*mu=0", "Route A crossing polynomial changed")
    require(b_formal["formal_mu_model"]["junction_polynomial"] == "300h^2+(90-50mu)h-65mu=0", "Route B crossing polynomial changed")
    return {
        "artifact_id": "g1-envelope-sensitivity-reconciliation-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "PROVED exact reconciliation of two independently written rational-identity routes, conditional on pinned published formulas and the finite G1 structural atlas. It does not assert any new large-values, zero-density, or short-interval inequality, and it makes no G1 route selection.",
        "frozen_hashes": hashes,
        "independence": {"route_a": "direct term evaluation then exact atlas-label comparison", "route_b": "cleared pairwise and transfer residual factorizations then atlas-label comparison", "shared_inputs_only": ["sealed G1 preregistration", "G1 exact structural atlas v2", "pinned Guth--Maynard TeX/tar"]},
        "reconciled_map": {"active_count_maps": "identical across A/C/E labels", "zero_B_residual_rows": len(a_zeroes), "zero_residual_term": "LV3 only", "zero_residual_characterization": "q=ell(s), n0=ell(s)/2, k=2 for every one of the 11 frozen s values", "critical_cell": {"local": "(s,n,v,w)=(7/10,5/6,7/10,2/3)", "A_active": ["A2", "A3"], "C_active": ["min(C2,C3) via C2"], "E_active": ["E1", "E2", "E3"], "transfer": "(s,n0,k,q)=(7/10,5/13,2,10/13)", "residuals": {"LV1": "3/13", "LV2": "1/13", "LV3": "0/1"}}, "required_improvement_target": "Only the source's named third Theorem 1.1 term T*N^(12/5)*V^(-4) can create first-order slack at the critical transfer; the first two have positive residuals."},
        "contained_no_effect": {"epistemic_status": "PROVED", "statement": "Within the existing split (Ingham only for s<7/10 and Guth--Maynard only for s>=7/10), a critical-point or right-side-only gain cannot lower the strict uniform 30/13 envelope because the Ingham left limit is 30/13.", "falsifier": "A proposed global gain must provide a valid bound on a left neighborhood of 7/10, or improve/replace the Ingham side; otherwise it fails this exact implication gate."},
        "formal_conditional_margin": {"premise_tag": "CONJECTURED", "premise": "A decrease mu>0 in the N exponent of LV3, with a separately valid left-neighborhood zero-detection propagation.", "critical_local": "delta=10mu/13; LV3 remains the active local term only through mu=1/10, after which LV2 is the local barrier.", "left_extension_crossing": "300h^2+(90-50mu)h-65mu=0", "first_order_global_density": "30/13-50mu/39+O(mu^2)", "formal_threshold_only": "17/30-13mu/54+O(mu^2); no short-interval result follows without a full replay."},
        "falsifier": "Any hash mismatch, route-label/count disagreement, non-LV3 zero residual, changed critical residual, or attempted endpoint-only propagation invalidates this reconciliation or the scoped conclusion it supports.",
        "replay": {"script_sha256": digest(Path(__file__)), "write_command": "python3 projects/guth-maynard-zero-density/proof/reconcile_g1_envelope_sensitivity_v1.py --write", "check_command": "python3 projects/guth-maynard-zero-density/proof/reconcile_g1_envelope_sensitivity_v1.py --check"},
    }


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = render(certificate())
    if args.write:
        OUTPUT.write_text(payload)
    else:
        require(OUTPUT.is_file() and OUTPUT.read_text() == payload, "G1 sensitivity reconciliation artifact mismatch")
        print(json.dumps({"artifact": OUTPUT.name, "verified": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
