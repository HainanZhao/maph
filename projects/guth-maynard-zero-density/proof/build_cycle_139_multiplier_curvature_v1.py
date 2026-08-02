#!/usr/bin/env python3
"""Seal Cycle 139 multiplier-denominator curvature."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-139-multiplier-curvature-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-139-multiplier-curvature-preregistration-v1.md", "f5140ac973139a83946cf4b95fe757f04c3ca5b61405d81a0dcc798da69cb145"),
    "document": (ROOT / "docs/cycle-139-multiplier-curvature-v1.md", "ee4ea568ad5db65bbb919b9df9c7161dbe9da60bac6ea3c98e43aef5ccc3dffb"),
    "conventions": (ROOT / "conventions/multiplier_curvature_v1.py", "a7e9ce507bd086bc59a1e7c60c50ec915ea4f2c7680deac018c4f24028fc1188"),
    "tests": (ROOT / "tests/test_cycle_139_multiplier_curvature_v1.py", "216a4ed66263ac967ad9081c8b8fa5ee7e827f1159efe2869bb0de9b5b1ecb9e"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle131": (ROOT / "artifacts/cycle-131-order-three-denominator-bridge-v1.json", "1fa3645c6cf6c59abc35604de076412cf413593ea49d5e5a214f9dee0aa99e55"),
    "cycle138": (ROOT / "artifacts/cycle-138-multiplier-fiber-height-v1.json", "d1eacac468da23239faa829ec6fb509dbba083dafbd2855ee55b84f8174029a6"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle131"][0], "SEALED_DENOMINATORS_TO_7_45_MINUS_2MU_3_ENDPOINT_OPEN")
    validate_prior(INPUTS["cycle138"][0], "SEALED_ALL_EDGE_MULTIPLICITIES_TO_1_6_MINUS_MU_2_UPPER_FAREY_RANGE_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="multiplier_curvature_v1")
    module = __import__("conventions.multiplier_curvature_v1", fromlist=["range_ledger"])
    worst = module.range_ledger(Fraction(16, 25), Fraction(9, 100))
    require(worst["extension"] == Fraction(13, 1800), "minimum low-edge extension")
    require(all(worst[key] > 0 for key in (
        "tube_margin_at_new_ceiling", "ratio_margin_at_new_ceiling", "constant_margin_at_new_ceiling"
    )), "secondary margins")
    require("does not extend" in theorem["high_edge_limit"], "high-edge limitation")
    require("no high-edge" in theorem["boundary"], "claim boundary")
    return {
        "artifact_id": "cycle-139-multiplier-curvature-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_LOW_EDGE_CURVATURE_TO_17_90_MINUS_2MU_3_HIGH_EDGE_OPEN",
        "claim_boundary": (
            "This artifact extends only low-edge exceptional-average cells through "
            "rho<17/90-2mu/3. It proves no high-edge or all-multiplicity extension, "
            "full paired norm, endpoint, moment, density, or prime intervals."
        ),
        "runtime": check_runtime("Cycle 139"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "multiplier_curvature_theorem": {"epistemic_status": "PROVED", **theorem},
        "worst_extension_ledger": {
            "epistemic_status": "PROVED",
            "xi": "16/25",
            "mu": "9/100",
            "new_low_edge_ceiling": str(worst["new_low_edge_ceiling"]),
            "extension": str(worst["extension"]),
            "tube_margin": str(worst["tube_margin_at_new_ceiling"]),
            "ratio_margin": str(worst["ratio_margin_at_new_ceiling"]),
            "constant_margin": str(worst["constant_margin_at_new_ceiling"]),
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "control high-edge classes beyond rho=1/6-mu/2 using a "
                "multiplicative-energy inverse or a phase-anchored recurrence"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_139_multiplier_curvature_v1.py --write",
            "check_command": "python3 proof/build_cycle_139_multiplier_curvature_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_139_multiplier_curvature_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 139 sealer", output=OUTPUT, payload_factory=seal))
