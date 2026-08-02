#!/usr/bin/env python3
"""Seal Cycle 126 Freiman-web recurrence-chain compiler."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-126-freiman-recurrence-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-126-freiman-recurrence-preregistration-v1.md", "7311b26d1df61dfcb912f7669130684ad7cce3be1f00e70930b77193ae129ff8"),
    "document": (ROOT / "docs/cycle-126-freiman-recurrence-v1.md", "9ee2302837ee197a223029b0fd24cd7bd33ee9ad74339ad04f8dbb47ebc7be25"),
    "conventions": (ROOT / "conventions/freiman_recurrence_v1.py", "b7c82f5bfac0da4b760dc6d2a9f677e31b4dea60c7cb9b3e01037074799ea840"),
    "tests": (ROOT / "tests/test_cycle_126_freiman_recurrence_v1.py", "52980f330989ec4e81811a892ae106c0c7c91fb99d67f91d43496f39ab50443b"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle125": (ROOT / "artifacts/cycle-125-freiman-ray-web-v1.json", "28112cb9c4e676719d1637b5ca650c49917b28ddcd2f43f04f93b54288802785"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle125"][0], "SEALED_HIGH_MULTIPLICITY_FREIMAN_WEB_LOW_MULTIPLICITY_SEED_GATE_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="freiman_recurrence_v1")
    module = __import__("conventions.freiman_recurrence_v1", fromlist=["error_margin"])
    require(module.error_margin(Fraction(16, 25)) == Fraction(28, 75), "error margin")
    require("independent of a" in theorem["difference_multiplier"], "common multiplier")
    require("ceil(L_d/(R-L_d))" in theorem["chain_bound"], "chain bound")
    require("J/(KQ)" in theorem["approximation"], "chain error")
    require("still tie" in theorem["anchor_gate"], "anchor gate")
    require("no long chain" in theorem["boundary"], "claim boundary")
    return {
        "artifact_id": "cycle-126-freiman-recurrence-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_COMMON_RATIONAL_MULTIPLIER_CHAIN_DEPTH_ANCHOR_OPEN",
        "claim_boundary": (
            "This artifact compiles each represented difference into a common "
            "rational multiplier and quantifies chain depth and phase error. It "
            "proves no long chain from energy alone, seed realization, low-"
            "multiplicity bound, simple-root closure, complete moment, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 126"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "freiman_recurrence_theorem": {"epistemic_status": "PROVED", **theorem},
        "minimum_chain_error_margin": {
            "epistemic_status": "PROVED",
            "exponent": "28/75",
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "force near-unit edge density for a represented difference or "
                "obtain the required E16 anchor/depth by a different graph extraction"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_126_freiman_recurrence_v1.py --write",
            "check_command": "python3 proof/build_cycle_126_freiman_recurrence_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_126_freiman_recurrence_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 126 sealer", output=OUTPUT, payload_factory=seal))
