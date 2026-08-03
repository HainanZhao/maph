#!/usr/bin/env python3
"""Seal Cycle 212/B049's two-sign logarithmic orientation result."""
from __future__ import annotations

from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_212_logarithmic_axis_to_packet_orientation import run as orientation_run


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-212-b049-logarithmic-axis-to-packet-orientation-v1.json"
INPUTS = {
    "prior_two_cusp_sections": (ROOT / "artifacts/cycle-211-b048-cusp-asymptotic-flat-sections-v1.json", "62b4afdbdf4ad2f9aa11e648929c54aa66219088689231373c7ad16635f8936c"),
    "prior_normal_line": (ROOT / "artifacts/cycle-203-b040-inverse-normal-line-v1.json", "a8382ed299a8985f444510b5a18e2406692d2a82e1c5b428ba2f5440640f1f41"),
    "prior_packet": (ROOT / "artifacts/cycle-200-b037-regular-residue-jet-v1.json", "f5ca2891ed59bc82af8da8f8bfcfe7d35f834e205291ae640fd1c57009655cae"),
    "prior_frobenius_action": (ROOT / "artifacts/cycle-173-local-artin-action-v2.json", "ddf13a934fed3f7cc16d316cab6f4835b20f44f4fdd9814b87ede91cdfa102d6"),
    "prior_embedding_selector": (ROOT / "artifacts/cycle-163-spectral-ray-interface-v1.json", "165096dfab6f44c85c3d19bf1b1150d392a05310acd2b6c6da32686fd6b54240"),
    "preregistration": (ROOT / "docs/cycle-212-b049-logarithmic-axis-to-packet-orientation-preregistration-v1.md", "d87657d1eedaf4e626aa6748ed5489a53c599383156d65ffa6cdacc2fc87629e"),
    "replay": (ROOT / "proof/verify_cycle_212_logarithmic_axis_to_packet_orientation.py", "5bb6c2907e139626a458ce2ce114934b4f419df0602c6c8258b4ecee5c0a1fd7"),
    "regression_test": (ROOT / "tests/test_cycle_212_logarithmic_axis_to_packet_orientation.py", "b9ea96a3a058735be868e82f27cc96bf5363f9d33604db00330a3a9c3db4675d"),
    "prototype": (ROOT / "discovery/cycle-212-b049-logarithmic-axis-to-packet-orientation-prototype-v1.json", "9895bdae093abede04a4917dc94a9438607d5b482ebe50e6f1a4d5b3bea46036"),
    "cycle203_replay": (ROOT / "proof/verify_cycle_203_inverse_normal_line.py", "76a569b5812d64e13e3c0a2533442a5765c40fa2c0535026bdf60e1e9b0d9b71"),
    "cycle200_replay": (ROOT / "proof/verify_cycle_200_regular_residue_jet.py", "c93c8f6e9341e3c94714f558176a726ba30ac63c2a2e6056114e8a4328b0a2e9"),
    "cycle173_replay": (ROOT / "proof/verify_cycle_173_local_artin_action.py", "c445f484464191168da217ace66316f2e04e3390687a1c58fca02b427bed97d9"),
    "cycle163_replay": (ROOT / "proof/verify_cycle_163_fixed_full_ray_selector.py", "4a5f07439f7e47545fc3cb4f5b5d43228f8f045ab0a97bc321140d9143f30c3b"),
    "preregistration_validator": (ROOT / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 212 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = orientation_run()
    lifts = result["logarithmic_lifts"]
    embedding = result["real_embedding_audit"]
    frobenius = result["frobenius_provenance_audit"]
    symmetry = result["two_sign_equivariance_audit"]
    require(lifts["two_signs_required"] and len(lifts["lifts"]) == 2, "logarithmic lift census drift")
    require([row["packet_coordinate"] for row in lifts["lifts"]] == ["s^(-1)", "s"], "lift-coordinate drift")
    require(embedding["epsilon_selector"] == "NOT_SUPPLIED", "embedding scope drift")
    require(frobenius["analytic_coordinate_action"] == "NOT_SUPPLIED_BY_FROZEN_ARTIFACT", "Frobenius scope drift")
    require(symmetry["frozen_selector_count"] == 0, "A6 selector drift")
    return {
        "artifact_id": "cycle-212-b049-logarithmic-axis-to-packet-orientation-v1",
        "cycle": 212,
        "budget_ordinal": "B049",
        "epistemic_status": "PROVED",
        "status": "SEALED_TWO_SIGN_LOGARITHMIC_AXIS_PACKET_LIFTS_NO_SELECTOR",
        "claim_boundary": result["claim_boundary"],
        "outcome": {"epistemic_status": "PROVED", "statement": "The two source logarithmic lifts t=s^(-1) and t=s are equally A6-covariant and reach opposite packet cusps. The frozen real embedding and norm-37 ray action have no proved analytic epsilon action, so this method family contains no selector."},
        "logarithmic_lifts": lifts,
        "real_embedding_audit": embedding,
        "frobenius_provenance_audit": frobenius,
        "two_sign_equivariance_audit": symmetry,
        "gate_outcome": result["gate_outcome"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "evidence_scope_review": "C212 proves that the two frozen logarithmic lifts are equally A6-covariant, realize opposite C211 cusps, and are not distinguished by the pinned real embedding or presently proved norm-37 ray action.",
            "recommendation": "Seal C212 as a scoped two-sign logarithmic nonselection result, then open a new cycle rather than extending the same selector family.",
            "known_flaw": "The result excludes neither an analytic Frobenius action, source density/orientation theorem, nonlogarithmic coordinate, nor a construction that uses both ends without selecting one.",
            "falsifier": "Any logarithmic-lift, beta^+-6 covariance, t=s^(-/+1) identification, embedding convention, ray-action scope, cusp correspondence, or replay discrepancy invalidates the seal.",
            "next_action": "Build a sign-independent two-ended completion with the involution exchanging [e_(0,5)] and [e_(5,0)], then test whether an A6/multiplier-equivariant pairing or fusion invariant descends without choosing epsilon.",
            "adopted": True,
            "reason": "Both exact logarithmic orientations survive every frozen covariance and arithmetic-provenance check, while all possible selector mechanisms remain outside the claim boundary.",
        },
        "preregistration_preflight": {"cycle": 212, "manifest_sha256": sha256(ROOT / "docs/cycle-212-b049-logarithmic-axis-to-packet-orientation-preregistration-v1.md"), "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"}},
        "frozen_hashes": frozen,
        "replay": {"preflight_command": "research prereg check docs/cycle-212-b049-logarithmic-axis-to-packet-orientation-preregistration-v1.md --expected-cycle 212 --allow-head-drift", "prototype_command": "python3 proof/verify_cycle_212_logarithmic_axis_to_packet_orientation.py --output discovery/cycle-212-b049-logarithmic-axis-to-packet-orientation-prototype-v1.json", "test_command": "python3 -m unittest tests/test_cycle_212_logarithmic_axis_to_packet_orientation.py", "write_command": "python3 proof/build_cycle_212_logarithmic_axis_to_packet_orientation_v1.py --write", "check_command": "python3 proof/build_cycle_212_logarithmic_axis_to_packet_orientation_v1.py --check"},
        "runtime": runtime,
        "sealer": {"path": "proof/build_cycle_212_logarithmic_axis_to_packet_orientation_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
