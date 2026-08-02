#!/usr/bin/env python3
"""Seal Cycle 174 capacity-saturated bounded-slack transport classifier."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-174-adaptive-slack-transport-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-174-adaptive-slack-transport-preregistration-v1.md", "1547680fe66ccfd5a4b7a180f5382b776a895af30d787e1b829585bfc9f737b7"),
    "document": (ROOT / "docs/cycle-174-adaptive-slack-transport-v1.md", "08ea6ab22894a7b0aeaed21cb8b92ee81fc0ff8f56a005aa7f8002ca2a4ba01c"),
    "conventions": (ROOT / "conventions/adaptive_slack_transport_v1.py", "8aa296eace1d89c629370c13ed57d9af0da6c8e06b8e4752b9c595ad5184ee2d"),
    "tests": (ROOT / "tests/test_cycle_174_adaptive_slack_transport_v1.py", "541ecc0c8c31129cbdf173253d354db9d7d2ce98255ca47805a5039bae7bad53"),
    "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "cycle173": (ROOT / "artifacts/cycle-173-positive-forward-balance-v1.json", "f32a73c74ceecd4c7fae5794799e26fb4ffbfd79cf182d5fe7c71d1eff9010b8"),
    "cycle170": (ROOT / "artifacts/cycle-170-projective-packet-lift-v1.json", "7d0769218a734d80cd80bfcdb962656f918a7df5156efbc44042cfd50a2491b9"),
}


def exact_checks() -> dict[str, object]:
    module = __import__("conventions.adaptive_slack_transport_v1", fromlist=["verify_all"])
    checked = module.verify_all()
    require("adaptive-slack classifier" in checked["boundary"], "claim boundary")
    saturated = module.saturated_transport(h=20, h_plus=10, a=2, q=1, K=10, H=10, y=module.Q(6, 5), Y=module.Q(3, 2))
    require(saturated["rho"] <= saturated["slack"], "fixed saturated slack")
    deficit = module.deficit_lower_bound(h=40, h_plus=20, a=2, q=1, K=5, H=20, y=module.Q(6, 5))
    require(deficit["index"] == 2 and deficit["rho"] >= deficit["lower"], "labelled deficit")
    return checked


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle173"][0], "SEALED_POSITIVE_FORWARD_CONSERVATIVE_BALANCE_GATE_EMPTY")
    validate_prior(INPUTS["cycle170"][0], "SEALED_PROJECTIVE_LIFT_SEEDED_TARGET_PACKET_OR_ERROR_CONTENT_ADMISSIBILITY_CLASSIFIER")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="adaptive_slack_transport_v1")
    return {
        "artifact_id": "cycle-174-adaptive-slack-transport-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_CAPACITY_SATURATED_BOUNDED_SLACK_TRANSPORT_OR_LABELLED_DEFICIT_BANK",
        "claim_boundary": "This proves a finite adaptive-slack classifier: capacity-saturated forward edges transport at fixed constant C0+4Y*C1, and every other admissible edge has a labelled dyadic capacity-deficit class. It proves no actual population, target-local packet, recurrence, skeleton, density, or interval gain.",
        "runtime": check_runtime("Cycle 174"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "prior_context": {
            "epistemic_status": "PROVED",
            "cycle173_role": "closes the unit conservative forward budget, motivating exact fixed row-local slack",
            "cycle170_role": "accepts the saturated edge by replacing its edge error constant with 4Y*C1 in the projective lift ledger",
        },
        "adaptive_slack": {"epistemic_status": "PROVED", **theorem},
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_checks(),
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "Force mass of complete compatible pairs into the capacity-saturated bounded-slack branch, or quantitatively control the labelled dyadic capacity-deficit banks."},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_174_adaptive_slack_transport_v1.py --write",
            "check_command": "python3 proof/build_cycle_174_adaptive_slack_transport_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_174_adaptive_slack_transport_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 174", output=OUTPUT, payload_factory=seal))
