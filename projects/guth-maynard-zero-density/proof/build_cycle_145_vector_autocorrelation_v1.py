#!/usr/bin/env python3
"""Seal Cycle 145 vector-valued autocorrelation compiler."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-145-vector-autocorrelation-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-145-vector-autocorrelation-preregistration-v1.md", "3773ba1a82e607bb64bfb8cf939a8f9bb630e04e79672a48e722b7c68cdf84bd"),
    "document": (ROOT / "docs/cycle-145-vector-autocorrelation-v1.md", "911c4d7b5144ff234a8a154cba941470a940ba22d74020df28c9619186ad0acc"),
    "conventions": (ROOT / "conventions/vector_autocorrelation_v1.py", "7f510a3029cd922728df835ce9d3c9fe30ff2d5ef87cad7ae2b8eb72bcb6b6da"),
    "tests": (ROOT / "tests/test_cycle_145_vector_autocorrelation_v1.py", "b58b064f501c76fb5aac9e9913c9816fd1dcb85d0c6cdf17c3362ac8df38b654"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle144": (ROOT / "artifacts/cycle-144-actual-edge-coefficient-v1.json", "c8260b7152a02b9d2b61ee1f60340b79c4eea40542311c64057af88c7a5ebf3c"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle144"][0], "SEALED_COEFFICIENT_PRESERVING_WEIGHTED_COLLISION_INVERSE_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="vector_autocorrelation_v1")
    module = __import__("conventions.vector_autocorrelation_v1", fromlist=["autocorrelation"])
    sequence = (1 + 1j, 2 - 1j, -1 + 2j)
    total = sum((module.autocorrelation(sequence, d) for d in range(-2, 3)), 0j)
    require(total == sum(sequence, 0j) * sum(sequence, 0j).conjugate(), "autocorrelation identity")
    require("ell^m" in theorem["vector_moments"], "frequency multipliers retained")
    require("mask" in theorem["selection_mask"], "arithmetic selection mask")
    require("no bound" in theorem["boundary"], "claim boundary")
    return {
        "artifact_id": "cycle-145-vector-autocorrelation-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_ARITHMETIC_SELECTION_MASK_AUTOCORRELATION_OPEN",
        "claim_boundary": (
            "This artifact proves an exact vector-valued Taylor compiler and "
            "the complete-difference autocorrelation identity. It proves no "
            "saving for the selected arithmetic mask, paired norm, endpoint, "
            "complete moment, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 145"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "vector_autocorrelation_theorem": {"epistemic_status": "PROVED", **theorem},
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "bound the vector-valued selected autocorrelation for the actual "
                "continued-fraction/tail mask, or factor that mask as a controlled Gram kernel"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_145_vector_autocorrelation_v1.py --write",
            "check_command": "python3 proof/build_cycle_145_vector_autocorrelation_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_145_vector_autocorrelation_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 145 sealer", output=OUTPUT, payload_factory=seal))
