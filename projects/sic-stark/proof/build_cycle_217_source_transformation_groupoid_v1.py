#!/usr/bin/env python3
"""Seal Cycle 217/B054's raw source-transformation groupoid audit."""
from __future__ import annotations

from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_217_source_transformation_groupoid import run as groupoid_run


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-217-b054-source-transformation-groupoid-v1.json"
INPUTS = {
    "prior_direct_e_obstruction": (ROOT / "artifacts/cycle-215-b052-equation66-e-transport-v1.json", "900f167c92c68c292d846694f5f2afa280b26c30ea5e27cfd732f271e8f1efbe"),
    "prior_rotating_path_obstruction": (ROOT / "artifacts/cycle-216-b053-rotating-period-cone-v1.json", "223667885a6507615ba6a73af823e03364f15dfe7127b0c473c3f3b7a5c288e6"),
    "preregistration": (ROOT / "docs/cycle-217-b054-source-transformation-groupoid-preregistration-v1.md", "0d1b6774d8baf1796fe8c24a253fc0b0b7bab7862e1fff283ee429e07d9758c1"),
    "replay": (ROOT / "proof/verify_cycle_217_source_transformation_groupoid.py", "e038ffb0d9ab95d4eb6edfbf99eaf8ddbb046ba52fa46b8cb84b4c2bdeb3b465"),
    "regression_test": (ROOT / "tests/test_cycle_217_source_transformation_groupoid.py", "38e932b19dbcee430434451fadb8c32b6ced8f4534c196bcaf24ff26fd142729"),
    "prototype": (ROOT / "discovery/cycle-217-b054-source-transformation-groupoid-prototype-v1.json", "9dea9b279909d5b799157aeae620cb103bcea7362aa9425e3c0ca1a05aab15e1"),
    "equation66_audit": (ROOT / "scripts/dimension_six_ss_evaluation_audit.py", "24c9258e46a1233c552017f3b58de0d45acd0197c8c807579f090ca1332f626f"),
    "prior_reflection_audit": (ROOT / "proof/verify_cycle_190_balanced_helical_reflection.py", "69da849d11c00ec30a5bca1a1220e1616d3d31beb75c8b906e8a67a9b0c98469"),
    "source_paper": (ROOT / "paper/sic-stark-dimension-six-boundary-fusion.tex", "347228e05a87946ca41bb31c118aae069b7fb6002fff4933d030a153cef21cb7"),
    "preregistration_validator": (ROOT / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 217 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = groupoid_run()
    raw = result["raw_orbit_audit"]
    canonical = result["candidate_canonical_orbit_audit"]
    affine = result["affine_period_argument_audit"]
    packet = result["packet_boundary_audit"]
    require(raw["raw_orbit_size"] == 4, "raw-orbit size drift")
    require(raw["two_step_matrix_is_minus_M_E"], "projective target drift")
    require(canonical["epistemic_status"] == "OBSERVED", "canonicalization scope drift")
    require(not affine["raw_two_step_periods_match_E_target"], "period mismatch drift")
    require(not packet["source_arrow_to_packet_t_a_b_map_available"], "packet-map scope drift")
    return {
        "artifact_id": "cycle-217-b054-source-transformation-groupoid-v1",
        "cycle": 217,
        "budget_ordinal": "B054",
        "epistemic_status": "PROVED",
        "status": "SEALED_RAW_SOURCE_TRANSFORMATION_GROUPOID_AFFINE_MISMATCH",
        "claim_boundary": result["claim_boundary"],
        "outcome": {"epistemic_status": "PROVED", "statement": "The raw cited F2/F3 matrix orbit has a projective -M_E hit, but its full affine period/argument/discrete state misses the E target; the k>0 M_E hit is quarantined as OBSERVED matrix algebra."},
        "raw_orbit_audit": raw,
        "candidate_canonical_orbit_audit": canonical,
        "affine_period_argument_audit": affine,
        "packet_boundary_audit": packet,
        "gate_outcome": result["gate_outcome"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "evidence_scope_review": "C217 proves the complete four-state raw F2/F3 matrix orbit, its projective hit on -M_E, and the decisive affine mismatch: periods 576*(omega2,omega1), argument 576*(mu+m*omega2), and discrete label zero. The k>0 M_E hit remains OBSERVED.",
            "recommendation": "Seal C217 as the completed raw-groupoid audit and open a new cycle; adding a signed/scaled period cover changes the state space and transformation family.",
            "known_flaw": "The result does not exclude a source-derived sign, swap, or multiplication formula that lifts projective canonicalization and reconciles the factor 576, discrete label, branches, and residual ordinary-gamma factors.",
            "falsifier": "Any F2/F3 parameter map, four-state closure, period composition, affine argument, discrete-label, residual-factor, M_E comparison, or replay discrepancy invalidates the seal.",
            "next_action": "Open a signed-period-cover cycle whose states include oriented/scaled periods, affine arguments, discrete labels, and residual factors; derive sign/swap/576-scaling laws from Gamma_M's product definition before testing whether C2 becomes an admissible arrow.",
            "adopted": True,
            "reason": "The raw groupoid frozen here is complete and exactly contained; the proposed period cover adds a different state representation and source-law requirement."
        },
        "preregistration_preflight": {"cycle": 217, "manifest_sha256": sha256(ROOT / "docs/cycle-217-b054-source-transformation-groupoid-preregistration-v1.md"), "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"}},
        "frozen_hashes": frozen,
        "replay": {"preflight_command": "research prereg check docs/cycle-217-b054-source-transformation-groupoid-preregistration-v1.md --expected-cycle 217 --allow-head-drift", "prototype_command": "python3 proof/verify_cycle_217_source_transformation_groupoid.py --output discovery/cycle-217-b054-source-transformation-groupoid-prototype-v1.json", "test_command": "python3 -m unittest tests/test_cycle_217_source_transformation_groupoid.py", "write_command": "python3 proof/build_cycle_217_source_transformation_groupoid_v1.py --write", "check_command": "python3 proof/build_cycle_217_source_transformation_groupoid_v1.py --check"},
        "runtime": runtime,
        "sealer": {"path": "proof/build_cycle_217_source_transformation_groupoid_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
