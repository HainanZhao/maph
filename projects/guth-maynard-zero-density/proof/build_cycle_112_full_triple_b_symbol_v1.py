#!/usr/bin/env python3
"""Seal Cycle 112 corrected full triple-B symbol and anchor absorption."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-112-full-triple-b-symbol-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-112-full-symbol-preregistration-v1.md", "bf4eda703e03560fb63a3b9e0bc04143fc9818f85d1531afa343fe41d9cb99f9"),
    "document": (ROOT / "docs/cycle-112-full-triple-b-symbol-v1.md", "d50064bd8e46ff445b3d3300d505d5abce0696bcfc04f823755bb71acf423e82"),
    "conventions": (ROOT / "conventions/full_triple_b_symbol_v1.py", "3ccdf397660c6f5f9ee16101aac4e465fd7574d7cb94ebc961012452815a2246"),
    "tests": (ROOT / "tests/test_cycle_112_full_triple_b_symbol_v1.py", "81fbbc5d737743923af9490d4312d45f7989d5a46c79a253c5b2b669cd6fb370"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle81": (ROOT / "artifacts/cycle-81-exact-q-transform-v1.json", "0753d455a2e9428b28f1b9dac59b04fd57008db562370202a300a38a818631a4"),
    "cycle90": (ROOT / "artifacts/cycle-90-equal-height-bprocess-v1.json", "a24a63110e26fff4672c8b8e2cca27569a00885dec7b8c934f8ca3971967c3de"),
    "cycle110": (ROOT / "artifacts/cycle-110-perfect-power-split-sum-v1.json", "cfcedf8145cf6ef70fb88b1a722067460236dfb7a04061d75db325e093746c42"),
    "cycle111": (ROOT / "artifacts/cycle-111-k-stationary-correction-v1.json", "22bb8d5a5d9eb581f66776b3fe9a88f9677e15173422c323ba4108138e7ae5c1"),
}


def seal() -> dict[str, Any]:
    expected = {
        "cycle81": "SEALED_EXACT_Q_TRANSFORM_LOG_RESONANCE_PROJECTOR_OPEN",
        "cycle90": "SEALED_EQUAL_HEIGHT_BPROCESS_SADDLE_DISCREPANCY_OR_WEB_OPEN",
        "cycle110": "SEALED_PERFECT_POWER_SPLIT_WEIGHT_UNIFORMLY_SUMMABLE",
        "cycle111": "SEALED_CORRECTION_K_LOCATION_ENTROPY_AND_SCALE_LAWS_SURVIVE",
    }
    for label, status in expected.items():
        validate_prior(INPUTS[label][0], status)
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="full_triple_b_symbol_v1")
    require("not a size prefactor" in theorem["anchor_role"], "anchor translation")
    require("lambda>=a" in theorem["anchor_absorption"], "anchor absorption")
    require("1/30" in theorem["aggregate"], "strict arithmetic margin")
    return {
        "artifact_id": "cycle-112-full-triple-b-symbol-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_SMOOTH_PERFECT_POWER_STRONG_BRANCH_X3_5_ARITHMETIC_MULTIPLICITY",
        "claim_boundary": (
            "This artifact restores the paired Cycle-81 outer amplitude at the corrected "
            "stationary points, proves uniform smooth-symbol anchor dependence, and combines "
            "support absorption with Cycle 110 to bound the strong smooth perfect-power "
            "arithmetic multiplicity by X^(3/5+o(1)). Other root and payload branches remain open."
        ),
        "runtime": check_runtime("Cycle 112"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "full_symbol_theorem": {"epistemic_status": "PROVED", **theorem},
        "closed_branch": {
            "epistemic_status": "PROVED",
            "statement": "registered smooth strong perfect-power arithmetic multiplicity is X^(3/5+o(1)), below X^(19/30+o(1)) by 1/30",
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "control irrational large-degree cores and weak/simple-root branches, then assemble the signed moment",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_112_full_triple_b_symbol_v1.py --write",
            "check_command": "python3 proof/build_cycle_112_full_triple_b_symbol_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_112_full_triple_b_symbol_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 112 sealer", output=OUTPUT, payload_factory=seal))
