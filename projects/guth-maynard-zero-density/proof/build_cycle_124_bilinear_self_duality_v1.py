#!/usr/bin/env python3
"""Seal Cycle 124 scoped bilinear norm-self-duality theorem."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-124-bilinear-self-duality-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-124-bilinear-self-duality-preregistration-v1.md", "b3d88f76413cf1992b4858c0fdb7ce184d4ea6fb425e99edf394c92164d0cb9c"),
    "document": (ROOT / "docs/cycle-124-bilinear-self-duality-v1.md", "34088c4a5aa2638afdc7ea850730581396437b8006805333c16808f323d5cecc"),
    "conventions": (ROOT / "conventions/bilinear_self_duality_v1.py", "106756438c7c88fb75c4f5a6f40ab58f659ec0910324661de7c3e0f043fdb04d"),
    "tests": (ROOT / "tests/test_cycle_124_bilinear_self_duality_v1.py", "5b41b61abf94aedaf56e24567de9dd46802cc7d9e47cd853479a2040bb75a5a3"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle123": (ROOT / "artifacts/cycle-123-joint-radial-alias-v1.json", "e700c21a422413abb6f35882d8d5a67b4ae4095b23c157da6397417b08f4da79"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle123"][0], "SEALED_JOINT_ALIAS_AMPLITUDE_PHASE_FACTORIZATION_BILINEAR_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="bilinear_self_duality_v1")
    module = __import__("conventions.bilinear_self_duality_v1", fromlist=["exponent_ledger"])
    left = module.exponent_ledger(Fraction(16, 25))
    require(left["alias_target"] == left["diagonal_second_moment"], "target identity")
    require("rank O(X^epsilon)" in theorem["tensor_separation"], "tensor rank")
    require("exactly the Cycle-87 target" in theorem["cauchy_target"], "target match")
    require("norm-neutral" in theorem["self_duality"], "scoped self-duality")
    require("does not exclude" in theorem["boundary"], "claim boundary")
    return {
        "artifact_id": "cycle-124-bilinear-self-duality-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_TENSOR_CAUCHY_NORM_SELF_DUAL_COLLISION_INVERSE_OPEN",
        "claim_boundary": (
            "This artifact proves norm-level self-duality only after smooth tensor "
            "separation, Cauchy, and separate diagonal second moments. It does not "
            "exclude correlated bilinear cancellation or prove simple-root closure, "
            "a complete moment, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 124"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "bilinear_self_duality_theorem": {"epistemic_status": "PROVED", **theorem},
        "left_endpoint_ledger": {
            "epistemic_status": "PROVED",
            "alias_target": str(left["alias_target"]),
            "diagonal_second_moment": str(left["diagonal_second_moment"]),
            "required_trivial_saving": str(left["required_trivial_saving"]),
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "exploit correlated bilinear structure beyond separate Cauchy, or "
                "compile a labelled excess second moment into the collision-web inverse"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_124_bilinear_self_duality_v1.py --write",
            "check_command": "python3 proof/build_cycle_124_bilinear_self_duality_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_124_bilinear_self_duality_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 124 sealer", output=OUTPUT, payload_factory=seal))
