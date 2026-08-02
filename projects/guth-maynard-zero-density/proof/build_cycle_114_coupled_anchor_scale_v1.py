#!/usr/bin/env python3
"""Seal Cycle 114 coupled anchor-scale-label aggregation."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-114-coupled-anchor-scale-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-114-coupled-anchor-scale-preregistration-v1.md", "5f644a3043d206975dd807b2f48d22d8f1c9fdd1c98907351c72df11ffdf8d10"),
    "document": (ROOT / "docs/cycle-114-coupled-anchor-scale-v1.md", "686c4ddb63d03246c4004cd17f43aa3f1b8cdee28f63c505cfc8dd058589cd73"),
    "conventions": (ROOT / "conventions/coupled_anchor_scale_v1.py", "b92c6723700f9302c286144cb9aa4fcf63b423878a3af042cbac23ad46caf1ac"),
    "tests": (ROOT / "tests/test_cycle_114_coupled_anchor_scale_v1.py", "ef1acc9d764a4f3c3d9e657880b846ad6026afd6aad30858a087875f1683e298"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle99": (ROOT / "artifacts/cycle-99-critical-rational-ray-v1.json", "69e453fea12a404c17078169ac605c17b05109b99c74e0dd82f830e1ecdf2ee6"),
    "cycle112": (ROOT / "artifacts/cycle-112-full-triple-b-symbol-v1.json", "e6f890eaae72a99c53dbd07cea7bd69d050f4df5c93d40e27245f71503f6954c"),
    "cycle113": (ROOT / "artifacts/cycle-113-irrational-weighted-split-v1.json", "2d29b2600e9b123ded335a2be83c656361c6ba46e3d74117d00bdf9253ebe393"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle99"][0], "SEALED_STRONG_NEAR_DOUBLE_CRITICAL_RAYS_WEAK_AND_FIBER_OPEN")
    validate_prior(INPUTS["cycle112"][0], "SEALED_SMOOTH_PERFECT_POWER_STRONG_BRANCH_X3_5_ARITHMETIC_MULTIPLICITY")
    validate_prior(INPUTS["cycle113"][0], "SEALED_GENERAL_STRONG_SPLIT_SUBPOWER_ANCHOR_SCALE_AGGREGATE_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="coupled_anchor_scale_v1")
    require("p0,q0<=1/a" in theorem["anchor_bound"], "anchor bound")
    require("d*Z" in theorem["gcd_bound"], "weighted gcd sum")
    require("X^(13/30" in theorem["aggregate"], "aggregate exponent")
    return {
        "artifact_id": "cycle-114-coupled-anchor-scale-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_ALL_SMOOTH_STRONG_CORES_WEIGHTED_X13_30_WEAK_SIMPLE_OPEN",
        "claim_boundary": (
            "This artifact couples coefficient bounds, stationary support, scale windows, "
            "and cross-gcd sums to bound all registered smooth strong near-double cores by "
            "the arithmetic factor X^(13/30+o(1)) after the common chart factor. Weak, "
            "simple-root, nonsmooth, moment, density, and interval branches remain open."
        ),
        "runtime": check_runtime("Cycle 114"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "coupled_theorem": {"epistemic_status": "PROVED", **theorem},
        "correction_resolution": {
            "epistemic_status": "PROVED",
            "statement": "Cycle 113's anchor-scale warning is resolved by using B,C<=Q jointly with n',m~Q; Cycle 112's X3/5 route is superseded by the X13/30 coupled route",
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "control weak localization and simple-root averages, then assemble the full signed moment",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_114_coupled_anchor_scale_v1.py --write",
            "check_command": "python3 proof/build_cycle_114_coupled_anchor_scale_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_114_coupled_anchor_scale_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 114 sealer", output=OUTPUT, payload_factory=seal))
