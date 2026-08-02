#!/usr/bin/env python3
"""Seal Cycle 170 signed projective packet-lift classifier."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-170-projective-packet-lift-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-170-projective-packet-lift-preregistration-v1.md", "c64020891722b63017fd0560d33324707771a862658171b4e27a007155d5b89f"),
    "document": (ROOT / "docs/cycle-170-projective-packet-lift-v1.md", "d5acc7e05b46c033cba9043a9fa27d98512bf27b7012b018d9ef8e9ddd28ede0"),
    "conventions": (ROOT / "conventions/projective_packet_lift_v1.py", "19ace16e5f0e0b62662860fdd41cbe2c4367a736a1a5d1ea29740a03cfd07852"),
    "tests": (ROOT / "tests/test_cycle_170_projective_packet_lift_v1.py", "850ecd9858f8e2621ee0ea0345f9bb0695f656ef5cacac3a48495014d7c07c5f"),
    "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "cycle169": (ROOT / "artifacts/cycle-169-source-coupled-label-energy-v1.json", "b79f6a8800bcb5dd6a2d58f9f71e6e89fb783bf1a562054196767a2f5ea7c008"),
    "cycle67": (ROOT / "artifacts/cycle-67-seeded-packet-recurrence-v1.json", "85bd999fca3e1d675c0b3096a6cd287866d9e1aef227239b42b94b39ff585d02"),
}


def exact_checks() -> dict[str, object]:
    module = __import__("conventions.projective_packet_lift_v1", fromlist=["verify_all"])
    checked = module.verify_all()
    require("finite projective-lift classifier" in checked["boundary"], "claim boundary")
    data = module.projective_data(d=2, b=1, q=2, a=3)
    require(data["Q"] == 4 and data["A"] == 5, "canonical reduction")
    depth = module.depth_ledger(content=17, load=module.Q(17, 6), h_cap=20, denominator=4)
    require(depth["target_depth"] == 5, "positive-load depth")
    require(module.certifies_reduced_packet(load=module.Q(17, 6), content=17, depth=5, denominator=4, h_cap=20), "positive-load certification")
    require(module.certifies_reduced_packet(load=module.Q(0), content=17, depth=5, denominator=4, h_cap=20), "zero-load certification")
    return checked


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle169"][0], "SEALED_COMMON_SOURCE_MARGINALS_DO_NOT_FORCE_TARGET_LABEL_ENERGY")
    validate_prior(INPUTS["cycle67"][0], "SEALED_SEEDED_X6_25_AP_RECURRENCE_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="projective_packet_lift_v1")
    return {
        "artifact_id": "cycle-170-projective-packet-lift-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_PROJECTIVE_LIFT_SEEDED_TARGET_PACKET_OR_ERROR_CONTENT_ADMISSIBILITY_CLASSIFIER",
        "claim_boundary": "This proves a finite signed projective packet-lift classifier for one compatible source packet/cross edge. It does not prove any compatible population, deep packet in the actual census, recurrence, skeleton, density, or interval gain.",
        "runtime": check_runtime("Cycle 170"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "prior_context": {
            "epistemic_status": "PROVED",
            "cycle169_role": "rules out marginal-only coupling, motivating the actual exponential projective identity",
            "cycle67_role": "provides recurrence after a deep target packet has a retained beta seed",
        },
        "projective_lift": {"epistemic_status": "PROVED", **theorem},
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_checks(),
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "Force a population of compatible source packet/cross-edge pairs into the seeded-deep branch, or bound/structure every low-content, error-load, and capacity obstruction bank."},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_170_projective_packet_lift_v1.py --write",
            "check_command": "python3 proof/build_cycle_170_projective_packet_lift_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_170_projective_packet_lift_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 170", output=OUTPUT, payload_factory=seal))
