#!/usr/bin/env python3
"""Seal Cycle 123 joint radial/alias saddle and normalized operator."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-123-joint-radial-alias-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-123-joint-radial-alias-preregistration-v1.md", "f5590c50be3f7c5422eb339a54e0d0385590892ecd6c789ab74616ed63a10885"),
    "document": (ROOT / "docs/cycle-123-joint-radial-alias-v1.md", "cb17a7208fb10524c7aab1eb74ec590065d9cbabfb1dd6ce5eff70c5df09de77"),
    "conventions": (ROOT / "conventions/joint_radial_alias_v1.py", "c23de73a82ee7e4d26c96b1db33b3770fa9f144638c0138a7d1dfac7be642972"),
    "tests": (ROOT / "tests/test_cycle_123_joint_radial_alias_v1.py", "049e1cb6f7b7490029ed92e663c650e333678efff158a0f5a4428eccd4e5b24f"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle122": (ROOT / "artifacts/cycle-122-radial-mean-alias-v1.json", "c419446735481e49ceef40c66296ad0ae6d0efe5bdef90cf4b3e173711a86a95"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle122"][0], "SEALED_RADIAL_ZERO_MODE_REMOVED_K_ALIAS_OPERATOR_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="joint_radial_alias_v1")
    require("det=-(c/n)^2" in theorem["hessian"], "joint Hessian")
    require("signature zero" in theorem["hessian"], "joint signature")
    require("(q0/p0)g^(u+v)" in theorem["total_amplitude"], "amplitude collapse")
    require("-(u+v)/D" in theorem["cutoffs"], "cutoff evaluation")
    require("e(-ell n'g^u)" in theorem["factorization"], "phase factorization")
    require("no bilinear estimate" in theorem["boundary"], "claim boundary")
    return {
        "artifact_id": "cycle-123-joint-radial-alias-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_JOINT_ALIAS_AMPLITUDE_PHASE_FACTORIZATION_BILINEAR_OPEN",
        "claim_boundary": (
            "This artifact derives the fully normalized joint-saddle leading "
            "operator and fixed-chart remainder scale. It proves no bilinear "
            "estimate, simple-root closure, complete moment, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 123"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "joint_alias_theorem": {"epistemic_status": "PROVED", **theorem},
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "prove the required weighted bilinear estimate for the separable "
                "ell~K phase or extract a phase-aware additive-energy inverse"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_123_joint_radial_alias_v1.py --write",
            "check_command": "python3 proof/build_cycle_123_joint_radial_alias_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_123_joint_radial_alias_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 123 sealer", output=OUTPUT, payload_factory=seal))
