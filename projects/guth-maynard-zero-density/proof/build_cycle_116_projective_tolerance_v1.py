#!/usr/bin/env python3
"""Seal Cycle 116 projective tolerance and weak-mode cap."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-116-projective-tolerance-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-116-projective-tolerance-preregistration-v1.md", "22a131857efb6633e33146ec9672523f1a3fc65fb1c3ab1a6ce82f1195ae1b10"),
    "document": (ROOT / "docs/cycle-116-projective-tolerance-v1.md", "0f2814d46a8287cb5d171df18347f271ef0f661ceebc273d9dbfea3a1ac84d17"),
    "conventions": (ROOT / "conventions/projective_tolerance_v1.py", "581333b60590140e7e4163bd5add60adfadebbf7c514d8d4d05990a013591936"),
    "tests": (ROOT / "tests/test_cycle_116_projective_tolerance_v1.py", "1cee340a541d5da13bbe186db00098b55836fda22173662ff0c5625158e8c1c8"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle95": (ROOT / "artifacts/cycle-95-projective-entropy-modes-v1.json", "73c1a220bd5bbacd2c813a7cbb36611c88bcc4e9e0e84bc8de97c95d6364128f"),
    "cycle115": (ROOT / "artifacts/cycle-115-local-turnover-v1.json", "cfc45ce92d0a986fca7d5708f1fd6a71befe47e07c1d6c95fe2a1059a72f029d"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle95"][0], "SEALED_EXACT_ALIASES_CENTRAL_NEAR_PROJECTIVE_MODES_QUANTITATIVE_OPEN")
    validate_prior(INPUTS["cycle115"][0], "SEALED_LOCAL_SIMPLE_OR_CRITICAL_BELOW_S2_D2_TOLERANCE_COMPARISON_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="projective_tolerance_v1")
    require("1/K" in theorem["laurent_tolerance"], "Laurent tolerance")
    require("D^2/K" in theorem["transition_energy"], "weak energy cap")
    require("7/25" in theorem["worst_exponent"], "mode exponent")
    return {
        "artifact_id": "cycle-116-projective-tolerance-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_WEAK_TRANSITION_ENERGY_CAP_MODE_EXPONENT_7_25_AGGREGATE_OPEN",
        "claim_boundary": (
            "This artifact reconstructs the projective Laurent tolerance as O(1/K) and "
            "confines every weak turnover to S2<<D^2/K, hence mode exponent at most 7/25. "
            "The reduced sector is not yet summed."
        ),
        "runtime": check_runtime("Cycle 116"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "tolerance_theorem": {"epistemic_status": "PROVED", **theorem},
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "sum the low-energy weak sector with coefficient weights and aggregate simple roots",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_116_projective_tolerance_v1.py --write",
            "check_command": "python3 proof/build_cycle_116_projective_tolerance_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_116_projective_tolerance_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 116 sealer", output=OUTPUT, payload_factory=seal))
