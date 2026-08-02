#!/usr/bin/env python3
"""Seal Cycle 146 balanced high-pass mask compiler."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-146-balanced-highpass-mask-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-146-balanced-mask-preregistration-v1.md", "333112a863094a625c39a9639617b1ff7a5f258980749f3e674542b9b697074d"),
    "document": (ROOT / "docs/cycle-146-balanced-mask-v1.md", "189d39c42b28ccb8901e48b18733bfeb156f819691e57ba41af9b4c4cb35c385"),
    "conventions": (ROOT / "conventions/balanced_highpass_mask_v1.py", "ae4244ca2061823523987cd5b32f6214b77115bf214393e5c378caa4b5c7051c"),
    "tests": (ROOT / "tests/test_cycle_146_balanced_highpass_mask_v1.py", "86225c97b3bf7bff4003bce3523a56611d93856c0034ce94c338b7ac8d6b0a1e"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle87": (ROOT / "artifacts/cycle-87-mellin-alias-atlas-v1.json", "68b88ccd4ce3e5371906e3b0da3c254056b79bad9504880ebbff04b9cebce8ca"),
    "cycle145": (ROOT / "artifacts/cycle-145-vector-autocorrelation-v1.json", "5989739fe7de6e80782e98d38b60226b0eb5aa95e630a10587427dc12a77d41a"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle87"][0], "SEALED_MELLIN_ALIAS_TRICHOTOMY_BOUND_OR_WEB_OPEN")
    validate_prior(INPUTS["cycle145"][0], "SEALED_ARITHMETIC_SELECTION_MASK_AUTOCORRELATION_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="balanced_highpass_mask_v1")
    module = __import__("conventions.balanced_highpass_mask_v1", fromlist=["signed_cell_witness"])
    _, witness = module.signed_cell_witness((-4.0, 7.0, 3.0, 2.0))
    require(witness >= 8.0 / 4.0, "signed cell averaging")
    require(module.circle_mean({-1: 2, 1: 2}) == 0j, "zero Fourier mode")
    require("E/P" in theorem["signed_partition"], "cell entropy charged")
    require("no arithmetic cell" in theorem["boundary"], "claim boundary")
    return {
        "artifact_id": "cycle-146-balanced-highpass-mask-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_SIGNED_HIGH_PASS_CELL_ENTROPY_OPEN",
        "claim_boundary": (
            "This artifact proves the exact high-pass mean-zero identity, the "
            "conditional Gram representation for a nonnegative dyadic cutoff, "
            "the zero-mode cost of positive majorants, and a signed cell averaging "
            "interface. It proves no arithmetic-cell estimate, paired norm, "
            "endpoint, complete moment, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 146"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "balanced_highpass_theorem": {"epistemic_status": "PROVED", **theorem},
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "build an affordable hierarchical arithmetic partition retaining "
                "the signed high-pass feature and estimate or invert its terminal cell"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_146_balanced_highpass_mask_v1.py --write",
            "check_command": "python3 proof/build_cycle_146_balanced_highpass_mask_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_146_balanced_highpass_mask_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 146 sealer", output=OUTPUT, payload_factory=seal))
