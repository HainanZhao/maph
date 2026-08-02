#!/usr/bin/env python3
"""Seal Cycle 175's frozen local leading-residue pairing."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-175-leading-residue-pairing-v1.json"
INPUTS = {
    "instructions": (ROOT / "AGENTS.md", "363495f0dbbe93e244b460c8eafb13247a8fb1f41be24f94c037ae9f6400c6f2"),
    "prior": (ROOT / "artifacts/cycle-174-deeper-local-action-v1.json", "25f19eb3e6a54f3d3ee2cb1cf4d45a274c0a06a1d747811bbb3e01365816d691"),
    "prereg": (ROOT / "docs/cycle-175-leading-residue-pairing-preregistration-v1.md", "f50f57226fa01883f2a7cb18578d3dcb3a49f0dfca5eac9df91bff7e2c25e948"),
    "replay": (ROOT / "proof/verify_cycle_175_leading_residue_pairing.py", "a70988256ed7102640550bb234192510d7c5735af95ac081928be0735168cf91"),
    "output": (ROOT / "discovery/cycle-175-leading-residue-pairing-prototype-v1.json", "6a470b1c8e4a9fa0241adebc41e9eeb054b1303492d3a7d7e74c549e44b21344"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 175 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = json.loads((ROOT / "discovery/cycle-175-leading-residue-pairing-prototype-v1.json").read_text())
    residue, pairing = result["leading_residue"], result["pairing"]
    require((residue["c_h"], residue["c_h_squared"], residue["oriented_difference_delta"]) == (2, 1, 1), "leading residue drift")
    require(pairing["matrix_a_rows_b_columns"] == [[0, 0, 0], [0, 2, 1], [0, 1, 2]], "pairing matrix drift")
    require(pairing["anchors_distinct_nonzero"], "anchor distinction absent")
    return {
        "artifact_id": "cycle-175-leading-residue-pairing-v1", "cycle": 175, "budget_ordinal": "B013", "epistemic_status": "PROVED", "status": "SEALED_ORIENTATION_SENSITIVE_LOCAL_ANCHOR_PAIRING", "claim_boundary": result["claim_boundary"],
        "outcome": {"epistemic_status": "PROVED", "statement": "The frozen wild leading-residue pairing is F3-bilinear and gives the two labelled anchors distinct nonzero values 2 and 1."},
        "exact_prototype": {"source_output": "discovery/cycle-175-leading-residue-pairing-prototype-v1.json", "leading_residue": residue, "pairing": pairing},
        "gate_outcome": {"d6_interface": "LOCAL_ANCHOR_PAIRING_CONSTRUCTED_36_ROW_TRANSPORT_TEST_REQUIRED", "remaining_bottleneck": "Define an outcome-blind map from all 36 multiplier rows to the two pairing inputs, then test totality, T-transport compatibility, and both labelled anchors.", "disallowed_pseudo_progress": ["changing the uniformizer or pairing normalization", "fitting row assignments from transport outcomes", "calling the local pairing an AFK or coefficient interface"]},
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "Cycle 176/B014: preregister an outcome-blind all-36-row map into the frozen local pairing inputs and test exact totality, T-transport compatibility, and the two anchors."},
        "preregistration_preflight": {"cycle": 175, "manifest_sha256": sha256(ROOT / "docs/cycle-175-leading-residue-pairing-preregistration-v1.md"), "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"}},
        "frozen_hashes": frozen,
        "replay": {"preflight_command": "research prereg check docs/cycle-175-leading-residue-pairing-preregistration-v1.md --expected-cycle 175 --allow-head-drift", "prototype_command": "python3 proof/verify_cycle_175_leading_residue_pairing.py --output discovery/cycle-175-leading-residue-pairing-prototype-v1.json", "write_command": "python3 proof/build_cycle_175_leading_residue_pairing_v1.py --write", "check_command": "python3 proof/build_cycle_175_leading_residue_pairing_v1.py --check"},
        "runtime": runtime, "sealer": {"path": "proof/build_cycle_175_leading_residue_pairing_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
