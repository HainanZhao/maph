#!/usr/bin/env python3
"""Seal Cycle 171 eligibility-weighted projective-content divisor web."""
from __future__ import annotations

from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-171-eligibility-weighted-projective-content-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-171-eligibility-weighted-projective-content-preregistration-v1.md", "1b5eafa9e682156c316c19840d36721af27ccd4326758dc922c6606f4c6abd22"),
    "document": (ROOT / "docs/cycle-171-eligibility-weighted-projective-content-v1.md", "9d4ea4afa8a1a6c09588750bec0be1cd05c39ba30f85b61842465efa3a8673bb"),
    "conventions": (ROOT / "conventions/eligibility_weighted_projective_content_v1.py", "1bb331586861ff8cb62a0f136381fa83ad27dd84f3abcc02912f473133c3ccc9"),
    "tests": (ROOT / "tests/test_cycle_171_eligibility_weighted_projective_content_v1.py", "dede22063d585fae082f90a665a754c6ae59fe8a3775f2cb09d6d64265a1b06d"),
    "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "cycle170": (ROOT / "artifacts/cycle-170-projective-packet-lift-v1.json", "7d0769218a734d80cd80bfcdb962656f918a7df5156efbc44042cfd50a2491b9"),
    "cycle169": (ROOT / "artifacts/cycle-169-source-coupled-label-energy-v1.json", "b79f6a8800bcb5dd6a2d58f9f71e6e89fb783bf1a562054196767a2f5ea7c008"),
}


def exact_checks() -> dict[str, object]:
    module = __import__("conventions.eligibility_weighted_projective_content_v1", fromlist=["verify_all"])
    checked = module.verify_all()
    require("conditional moment transfer" in checked["boundary"], "claim boundary")
    data = module.factor_content(d=6, b=9, q=10, a=21)
    require(data == {"D": 60, "N": 255, "g": 15, "c": 3, "u": 1, "v": 5}, "canonical factorization")
    required = module.required_content(load=Q(17, 6), D=60, critical_depth=5, height_cap=20)
    require(required == 15 and module.is_deep(content=15, load=Q(17, 6), D=60, critical_depth=5, height_cap=20), "joint threshold")
    require(module.low_content_reason(c=3, u=1, v=1, required=15) == "numerator_absorption", "obstruction refinement")
    ledger = module.verify_weighted_transfer(rows=[(Q(1, 2), Q(99, 100)), (Q(1, 2), Q(4))], cap=Q(4))
    require(ledger["deep_mass"] >= ledger["lower_bound"], "labelled moment transfer")
    return checked


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle170"][0], "SEALED_PROJECTIVE_LIFT_SEEDED_TARGET_PACKET_OR_ERROR_CONTENT_ADMISSIBILITY_CLASSIFIER")
    validate_prior(INPUTS["cycle169"][0], "SEALED_COMMON_SOURCE_MARGINALS_DO_NOT_FORCE_TARGET_LABEL_ENERGY")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="eligibility_weighted_projective_content_v1")
    return {
        "artifact_id": "cycle-171-eligibility-weighted-projective-content-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_ELIGIBILITY_WEIGHTED_PROJECTIVE_CONTENT_DIVISOR_WEB_AND_SHARP_TRANSFER",
        "claim_boundary": "This proves a finite eligibility-weighted projective-content divisor classifier and a conditional sharp moment-to-deep-population transfer. It proves no actual compatible mass or moment lower bound, recurrence, skeleton, density, or interval gain.",
        "runtime": check_runtime("Cycle 171"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "prior_context": {
            "epistemic_status": "PROVED",
            "cycle169_role": "rules out total-marginal forcing, so the moment is explicitly conditioned on complete eligible labelled pairs",
            "cycle170_role": "supplies the exact seed/range, error, and capacity gates compressed by the required-content threshold",
        },
        "eligibility_weighted_content": {"epistemic_status": "PROVED", **theorem},
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_checks(),
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "Prove an actual lower bound for the complete labelled eligible divisor-content moment, or quantitatively bank seed/range, error, capacity, source-core, numerator-absorption, or denominator-absorption mass."},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_171_eligibility_weighted_projective_content_v1.py --write",
            "check_command": "python3 proof/build_cycle_171_eligibility_weighted_projective_content_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_171_eligibility_weighted_projective_content_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 171", output=OUTPUT, payload_factory=seal))
