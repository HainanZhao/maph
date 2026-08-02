#!/usr/bin/env python3
"""Seal Cycle 167 reduced-rational scope correction."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-167-affine-fibre-transport-v1-scope-correction.json"
INPUTS = {
    "original": (ROOT / "artifacts/cycle-167-affine-fibre-transport-v1.json", "7ba12c9d0534c0d0d151bce753fa24191c4e174af839ca12b86d65911779ed1b"),
    "correction_document": (ROOT / "docs/cycle-167-affine-fibre-transport-scope-correction-v1.md", "7f70fd3890febf939639db6c11dbb37b13e9869dbbd4fb998b91025017e263da"),
    "tests": (ROOT / "tests/test_cycle_167_affine_fibre_transport_scope_correction_v1.py", "2ba73b86d51c2f0fd677f13d7bda72bf8607078461f43b7124f542edf08415be"),
    "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
}


def seal() -> dict[str, Any]:
    frozen = freeze_inputs(ROOT, INPUTS)
    document = INPUTS["correction_document"][0].read_text(encoding="utf-8")
    require("reduced-rational affine multiplicative" in document, "missing narrowed scope")
    require("No identity, convention, finite test, parent-count result" in document, "wrong correction type")
    return {
        "artifact_id": "cycle-167-affine-fibre-transport-v1-scope-correction",
        "epistemic_status": "PROVED",
        "status": "SEALED_REDUCED_RATIONAL_SCOPE_CORRECTION",
        "claim_boundary": "This correction narrows the Cycle-167 top-level boundary to the reduced-rational approximant ansatz. It changes no mathematical identity or result and proves no transport recurrence, skeleton, density, or interval gain.",
        "runtime": check_runtime("Cycle 167 scope correction"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen,
        "corrects": {
            "artifact": "artifacts/cycle-167-affine-fibre-transport-v1.json",
            "artifact_sha256": INPUTS["original"][1],
            "cause": "top-level scope wording was broader than the frozen reduced-rational theorem",
            "error": "The original claim boundary omitted the qualifier 'reduced-rational' although the theorem record and proof document include it.",
            "mathematical_content_changed": False,
            "replacement_boundary": "Within the one-step reduced-rational affine multiplicative architecture, this classifies beta-preserving cross-label edges.",
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Join an eligible cross-label edge to a retained target-local packet, or construct a labelled closed loop yielding an equivalent local relation.",
        },
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_167_affine_fibre_transport_scope_correction_v1.py --write",
            "check_command": "python3 proof/build_cycle_167_affine_fibre_transport_scope_correction_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_167_affine_fibre_transport_scope_correction_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 167 correction", output=OUTPUT, payload_factory=seal))
