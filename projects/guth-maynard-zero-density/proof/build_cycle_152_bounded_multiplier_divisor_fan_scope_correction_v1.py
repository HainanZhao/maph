#!/usr/bin/env python3
"""Seal the Cycle 152 scope-status correction without mutating v1."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-152-bounded-multiplier-divisor-fan-v1-scope-correction.json"
INPUTS = {
    "correction_document": (ROOT / "docs/cycle-152-bounded-multiplier-divisor-fan-scope-correction-v1.md", "3113ba6ea8cbf25a336be01865b89968da83c72c80b339ed1b650128bdd46e3b"),
    "tests": (ROOT / "tests/test_cycle_152_bounded_multiplier_divisor_fan_scope_correction_v1.py", "b6cf5be90814958fb54d6c85b4b35b7afb6a73010fe6f1afb365e848e02ff490"),
    "original": (ROOT / "artifacts/cycle-152-bounded-multiplier-divisor-fan-v1.json", "a5100588231e9bb551965096b5c13f3ba05e11e68603204fa56cf685acfc86d6"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["original"][0], "SEALED_BOUNDED_MULTIPLIER_DIVISOR_FAN_TAIL_INCIDENCE_OR_FAN_ANALYSIS_OPEN")
    require(INPUTS["original"][1] == sha256(INPUTS["original"][0]), "original immutable hash")
    return {
        "artifact_id": "cycle-152-bounded-multiplier-divisor-fan-v1-scope-correction",
        "epistemic_status": "PROVED",
        "status": "SEALED_CONDITIONAL_BOUNDED_MULTIPLIER_DIVISOR_FAN_INVERSE",
        "claim_boundary": (
            "This correction narrows Cycle 152's status to its conditional strict smooth-halo inverse. "
            "It does not prove that the actual complement supplies the normalized mass and uniform-bound "
            "hypotheses, and it proves no incidence bound, full moment, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 152 scope correction"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "corrects": {
            "epistemic_status": "PROVED",
            "artifact": "artifacts/cycle-152-bounded-multiplier-divisor-fan-v1.json",
            "artifact_sha256": INPUTS["original"][1],
            "error": "The original status could be read as an actual E14D-L advance although its theorem is conditional.",
            "cause": "status scope was broader than the frozen claim boundary",
            "mathematical_content_changed": False,
            "replacement_status": "SEALED_CONDITIONAL_BOUNDED_MULTIPLIER_DIVISOR_FAN_INVERSE",
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "route the actual Cycle-149--151 negative correlation into normalized strict-halo mass "
                "meeting the Cycle-152 hypotheses, or quantify the residual boundary, phase-changing, nonsmooth, or unbounded-tail escape mass"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_152_bounded_multiplier_divisor_fan_scope_correction_v1.py --write",
            "check_command": "python3 proof/build_cycle_152_bounded_multiplier_divisor_fan_scope_correction_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_152_bounded_multiplier_divisor_fan_scope_correction_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 152 scope correction", output=OUTPUT, payload_factory=seal))
