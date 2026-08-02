#!/usr/bin/env python3
"""Seal Cycle 121 projective stationary-amplitude collapse."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-121-projective-amplitude-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-121-projective-amplitude-preregistration-v1.md", "431898ba32a2e253a10503ad37bf1695f465db551fd0cca56948534cd3a9a8a6"),
    "document": (ROOT / "docs/cycle-121-projective-amplitude-v1.md", "9951408ba077e33b710a7f03b0df762d772e9cb07a64f421f87907602da6f785"),
    "conventions": (ROOT / "conventions/projective_amplitude_v1.py", "fcc554f213fb2beab747c690b281b6704444368921d8f0a0c811a34ba21efe95"),
    "tests": (ROOT / "tests/test_cycle_121_projective_amplitude_v1.py", "c345154a9b40ff1ec1d9e614e1dbe66ae12ce69c8dc4a3c6bee824e58a05a0fa"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle120": (ROOT / "artifacts/cycle-120-projective-radial-phase-v1.json", "cd584128c1624c8ced2d91c71ff7cb370a7bab7a57f8441b7a8e7b994b5c66cd"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle120"][0], "SEALED_PROJECTIVE_CURVATURE_RADIAL_SIGNED_KERNEL_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="projective_amplitude_v1")
    require("c z_v/m" in theorem["amplitude_collapse"], "amplitude collapse")
    require("no remaining power of H" in theorem["amplitude_collapse"], "radial-height cancellation")
    require("hat(U)(-H0 P(z_v))" in theorem["radial_profile"], "radial profile")
    require("O(1/m)" in theorem["remainder"], "summed remainder")
    require("no arithmetic cancellation" in theorem["boundary"], "claim boundary")
    return {
        "artifact_id": "cycle-121-projective-amplitude-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_PROJECTIVE_AMPLITUDE_COLLAPSE_RADIAL_OPERATOR_BOUND_OPEN",
        "claim_boundary": (
            "This artifact derives the projective leading amplitude and a fixed-chart "
            "summed stationary remainder. It proves no cancellation across arithmetic "
            "labels, simple-root closure, complete moment, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 121"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "projective_amplitude_theorem": {"epistemic_status": "PROVED", **theorem},
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "prove the X^(14/15-xi) saving for the explicit weighted radial "
                "Fourier-profile operator, or extract a phase-aware inverse"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_121_projective_amplitude_v1.py --write",
            "check_command": "python3 proof/build_cycle_121_projective_amplitude_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_121_projective_amplitude_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 121 sealer", output=OUTPUT, payload_factory=seal))
