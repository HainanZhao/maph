#!/usr/bin/env python3
"""Seal Cycle 119 simple-root zeroth-mode limitation."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-119-simple-root-volume-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-119-simple-root-volume-preregistration-v1.md", "e1c8c49a8b7f7dab63fa2848dc65b07cd69bafb05b080222d0f9050f16d2e489"),
    "document": (ROOT / "docs/cycle-119-simple-root-volume-v1.md", "2a6b773925932aff63364508e2c4f030bbcdc4abd4d26769cb48cf3b9033bd9f"),
    "conventions": (ROOT / "conventions/simple_root_volume_v1.py", "abc7df41b20c4b637d4571194df72c889573042d03ae03545a0ded7d681cf9fb"),
    "tests": (ROOT / "tests/test_cycle_119_simple_root_volume_v1.py", "f720a078dbb60349e90373165335953c876fe7065033ddcb014679e211171629"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle117": (ROOT / "artifacts/cycle-117-weighted-weak-sector-v1.json", "2594773d6768fd46aa46da2e424cb2c06ab49fada984fd9b3c7315ff521b56ea"),
    "cycle118": (ROOT / "artifacts/cycle-118-simple-root-profiler-v1.json", "5862998cc7811f79fee31301ae65ddcf55c93fb5455c38fa6627cb6f70b4065c"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle117"][0], "SEALED_SMOOTH_WEAK_SECTOR_X59_150_SIMPLE_ROOT_OPEN")
    validate_prior(INPUTS["cycle118"][0], "SEALED_DISCOVERY_SIMPLE_ROOT_JET_COLLAPSE_FALSIFIED_DISCREPANCY_ENGINE_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="simple_root_volume_v1")
    module = __import__("conventions.simple_root_volume_v1", fromlist=["exponent_ledger"])
    left = module.exponent_ledger(Fraction(16, 25))
    near_right = module.exponent_ledger(Fraction(58, 75) - Fraction(1, 7500))
    require(left["weighted_volume"] == Fraction(109, 150), "left volume exponent")
    require(left["required_saving"] == Fraction(22, 75), "left saving")
    require(near_right["required_saving"] == Fraction(4, 25) + Fraction(1, 7500), "right saving limit")
    require("termwise in absolute value" in theorem["limitation"], "scoped limitation")
    require("does not exclude" in theorem["boundary"], "claim boundary")
    return {
        "artifact_id": "cycle-119-simple-root-volume-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_SIMPLE_UNSIGNED_ABSOLUTE_VOLUME_LIMIT_SIGNED_DISCREPANCY_OPEN",
        "claim_boundary": (
            "This artifact proves only that a Selberg-majorant argument taking "
            "termwise absolute values cannot beat its zeroth mode. It does not "
            "exclude cancellation against the mean, and proves no signed moment, "
            "density coefficient, or prime-interval improvement."
        ),
        "runtime": check_runtime("Cycle 119"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "simple_root_volume_theorem": {"epistemic_status": "PROVED", **theorem},
        "endpoint_ledger": {
            "epistemic_status": "PROVED",
            "left_weighted_exponent": str(left["weighted_volume"]),
            "left_required_saving": str(left["required_saving"]),
            "upper_edge_required_saving_limit": "4/25",
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "retain the sign-sector Fourier products or the original stationary "
                "phase and save X^(14/15-xi) in the simple-root contribution"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_119_simple_root_volume_v1.py --write",
            "check_command": "python3 proof/build_cycle_119_simple_root_volume_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_119_simple_root_volume_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 119 sealer", output=OUTPUT, payload_factory=seal))
