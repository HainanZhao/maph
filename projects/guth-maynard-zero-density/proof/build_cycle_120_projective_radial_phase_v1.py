#!/usr/bin/env python3
"""Seal Cycle 120 exact projective/radial phase normal form."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-120-projective-radial-phase-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-120-projective-radial-phase-preregistration-v1.md", "7ebaba8f1b001e6be54da745bc0400b20959ad6344982d3e254895c04129ca18"),
    "document": (ROOT / "docs/cycle-120-projective-radial-phase-v1.md", "26314b4a1ae2b995d061df31fcd6b480ae311347cf7415b1148f9658ad2888cc"),
    "conventions": (ROOT / "conventions/projective_radial_phase_v1.py", "68832b9d53f67e055f325136414b94fc3a303c8bdf32da67d559820eea47026d"),
    "tests": (ROOT / "tests/test_cycle_120_projective_radial_phase_v1.py", "b6df06a870669158147aea90af166ced520e34173517d9ff2179c2c356ab8b7b"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle119": (ROOT / "artifacts/cycle-119-simple-root-volume-v1.json", "d101504a18724dc79c143a0d485790584478e282c9544cfab8be2349212d50e9"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle119"][0], "SEALED_SIMPLE_UNSIGNED_ABSOLUTE_VOLUME_LIMIT_SIGNED_DISCREPANCY_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="projective_radial_phase_v1")
    require("H P_(u,v)(z)" in theorem["normal_form"], "homogeneous normal form")
    require("P(z_v)=c log" in theorem["radial_frequency"], "radial frequency")
    require("sign(P(z_v))=sign(R)" in theorem["residual_orientation"], "orientation")
    require("|R|=O(1/K)" in theorem["coherence"], "tolerance recovery")
    require("no cancellation estimate" in theorem["boundary"], "claim boundary")
    return {
        "artifact_id": "cycle-120-projective-radial-phase-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_PROJECTIVE_CURVATURE_RADIAL_SIGNED_KERNEL_OPEN",
        "claim_boundary": (
            "This artifact derives the exact projective saddle and signed radial "
            "frequency. It proves no cancellation estimate, simple-root sum, "
            "complete moment, density coefficient, or prime-interval improvement."
        ),
        "runtime": check_runtime("Cycle 120"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "projective_radial_theorem": {"epistemic_status": "PROVED", **theorem},
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "bound the phase-aware sum of radial Fourier profiles with saving "
                "X^(14/15-xi), retaining sign sectors and projective amplitudes"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_120_projective_radial_phase_v1.py --write",
            "check_command": "python3 proof/build_cycle_120_projective_radial_phase_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_120_projective_radial_phase_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 120 sealer", output=OUTPUT, payload_factory=seal))
