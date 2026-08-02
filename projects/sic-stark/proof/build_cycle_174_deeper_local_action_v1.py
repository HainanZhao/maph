#!/usr/bin/env python3
"""Seal Cycle 174's oriented deeper-local quotient construction."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-174-deeper-local-action-v1.json"
INPUTS = {
    "instructions": (ROOT / "AGENTS.md", "363495f0dbbe93e244b460c8eafb13247a8fb1f41be24f94c037ae9f6400c6f2"),
    "prior": (ROOT / "artifacts/cycle-173-local-artin-action-v2.json", "ddf13a934fed3f7cc16d316cab6f4835b20f44f4fdd9814b87ede91cdfa102d6"),
    "prereg": (ROOT / "docs/cycle-174-deeper-local-action-preregistration-v1.md", "79333e3675f295db3955e8cf3b860e792296da8d4c6e4c7b3281dc5ccc759021"),
    "replay": (ROOT / "proof/verify_cycle_174_deeper_local_action.py", "165da8aaa15c350162e13d193fc8b8647f1a756f478d833651943a2496185c57"),
    "output": (ROOT / "discovery/cycle-174-deeper-local-action-prototype-v1.json", "b99f775a337e1b2b718b4a866b70a8697583ba32476b8c34eb014a8bdc7756b3"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 174 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = json.loads((ROOT / "discovery/cycle-174-deeper-local-action-prototype-v1.json").read_text())
    action = result["explicit_action"]
    quotient = result["orientation_sensitive_quotient"]
    require(result["conductor_crosscheck"]["p3_exponents_for_characters_0_to_5"] == [0, 2, 2, 1, 2, 2], "conductor census drift")
    require((action["vP_g2_minus_pi"], action["vP_g_minus_g_inverse"], quotient["first_distinguishing_depth"]) == (3, 3, 4), "orientation-depth drift")
    return {
        "artifact_id": "cycle-174-deeper-local-action-v1",
        "cycle": 174,
        "budget_ordinal": "B012",
        "epistemic_status": "PROVED",
        "status": "SEALED_ORIENTATION_SENSITIVE_DEEPER_LOCAL_QUOTIENT",
        "claim_boundary": result["claim_boundary"],
        "outcome": {"epistemic_status": "PROVED", "statement": "The first exact local quotient distinguishing the oriented Artin elements is O_L/P^4, with g(pi)-g^-1(pi) of valuation 3."},
        "exact_prototype": {"source_output": "discovery/cycle-174-deeper-local-action-prototype-v1.json", "conductor_crosscheck": result["conductor_crosscheck"], "explicit_action": action, "orientation_sensitive_quotient": quotient},
        "gate_outcome": {"d6_interface": "ORIENTATION_SENSITIVE_LOCAL_QUOTIENT_CONSTRUCTED_LEADING_RESIDUE_REQUIRED", "remaining_bottleneck": "Derive the normalized leading residue of (g(pi)-g^-1(pi))/pi^3 and test a frozen local pairing against both anchors before proposing finite transport.", "disallowed_pseudo_progress": ["calling O_L/P^4 a regulator equality", "fitting a transport from the convolution defect", "treating local orientation as the coefficient-to-ray map"]},
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "Cycle 175/B013: derive the normalized leading residue of (g(pi)-g^-1(pi))/pi^3 mod P, its generator behavior, and a frozen local pairing against the two anchors."},
        "preregistration_preflight": {"cycle": 174, "manifest_sha256": sha256(ROOT / "docs/cycle-174-deeper-local-action-preregistration-v1.md"), "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"}},
        "frozen_hashes": frozen,
        "replay": {"preflight_command": "research prereg check docs/cycle-174-deeper-local-action-preregistration-v1.md --expected-cycle 174 --allow-head-drift", "prototype_command": "python3 proof/verify_cycle_174_deeper_local_action.py --output discovery/cycle-174-deeper-local-action-prototype-v1.json", "write_command": "python3 proof/build_cycle_174_deeper_local_action_v1.py --write", "check_command": "python3 proof/build_cycle_174_deeper_local_action_v1.py --check"},
        "runtime": runtime,
        "sealer": {"path": "proof/build_cycle_174_deeper_local_action_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
