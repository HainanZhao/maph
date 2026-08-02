#!/usr/bin/env python3
"""Correct Cycle 173 replay by excluding mutable PLAN.md from frozen inputs."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-173-local-artin-action-v2.json"
INPUTS = {
    "superseded_artifact": (ROOT / "artifacts/cycle-173-local-artin-action-v1.json", "86560fe8b673671020a2e5a86a9d0a0c616eb4bd830d28ae92621248192b6a08"),
    "correction": (ROOT / "docs/cycle-173-local-artin-action-correction-v2.md", "50390e08784b5598ea7b5184825b33a416d8addae24a3398458a0697d539a0ed"),
    "prior": (ROOT / "artifacts/cycle-172-local-filtration-v1.json", "b6775274f7e069ff765341eb1c0553a831864f3ad5d1e90727a1dcf22ee77adb"),
    "prereg": (ROOT / "docs/cycle-173-local-artin-action-preregistration-v1.md", "b2b76dccd70dc3bf1c1f0840e9963c434994b697e608e2fd5f7a76e0462f2d39"),
    "replay": (ROOT / "proof/verify_cycle_173_local_artin_action.py", "c445f484464191168da217ace66316f2e04e3390687a1c58fca02b427bed97d9"),
    "output": (ROOT / "discovery/cycle-173-local-artin-action-prototype-v1.json", "c352118fb8360f3a9dc4527482989ea31be18364590657e31693386142d6f813"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 173 v2 correction")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = json.loads((ROOT / "discovery/cycle-173-local-artin-action-prototype-v1.json").read_text())
    local = result["local_inertia_derivation"]
    require(local["all_artin_powers"] == [1, 2, 1, 2, 1, 2], "Artin power action drift")
    require(local["wild_action_on_gr1"] == 1, "wild action drift")
    require(result["orientation_test"]["rho_g_equals_rho_g_inverse"], "orientation-loss witness absent")
    return {
        "artifact_id": "cycle-173-local-artin-action-v2",
        "cycle": 173,
        "budget_ordinal": "B011",
        "epistemic_status": "PROVED",
        "status": "SEALED_FIRST_GRADED_ARTIN_ACTION_ORIENTATION_LOSS_CORRECTED_REPLAY",
        "supersedes": "cycle-173-local-artin-action-v1",
        "correction": {
            "epistemic_status": "PROVED",
            "statement": "v1 froze mutable PLAN.md; v2 removes that replay-only input without changing the mathematical result.",
            "affected_claims": "v1 replay and evidence-drift status only; no mathematical claim is affected.",
        },
        "claim_boundary": result["claim_boundary"],
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": "The oriented generator acts by -1 on U_L^1/U_L^2, its wild square acts trivially, and this quotient identifies g with g^-1.",
        },
        "exact_prototype": {
            "source_output": "discovery/cycle-173-local-artin-action-prototype-v1.json",
            "local_inputs": result["exact_inputs"],
            "action": local,
            "orientation_test": result["orientation_test"],
        },
        "gate_outcome": {
            "d6_interface": "FIRST_GRADED_ACTION_ORIENTATION_BLIND_DEEPER_ENGINE_REQUIRED",
            "remaining_bottleneck": "Derive a minimal deeper unit quotient or non-graded local invariant with an oriented Artin/Hilbert pairing before selecting a coefficient module.",
            "disallowed_pseudo_progress": ["using U_L^1/U_L^2 as an oriented coefficient module", "fitting a deeper action from the convolution defect", "calling first-graded orientation loss a regulator, interface, fusion, or TCC no-go"],
        },
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "Cycle 174/B012: preregister the minimal deeper local quotient and refined Artin/Hilbert-pairing invariant that could distinguish g from g^-1, then derive it exactly or contain that engine."},
        "preregistration_preflight": {"cycle": 173, "manifest_sha256": sha256(ROOT / "docs/cycle-173-local-artin-action-preregistration-v1.md"), "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"}},
        "frozen_hashes": frozen,
        "replay": {"preflight_command": "research prereg check docs/cycle-173-local-artin-action-preregistration-v1.md --expected-cycle 173 --allow-head-drift", "prototype_command": "python3 proof/verify_cycle_173_local_artin_action.py --output discovery/cycle-173-local-artin-action-prototype-v1.json", "write_command": "python3 proof/build_cycle_173_local_artin_action_v2.py --write", "check_command": "python3 proof/build_cycle_173_local_artin_action_v2.py --check"},
        "runtime": runtime,
        "sealer": {"path": "proof/build_cycle_173_local_artin_action_v2.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
