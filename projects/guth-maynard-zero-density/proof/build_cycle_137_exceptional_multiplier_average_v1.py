#!/usr/bin/env python3
"""Seal Cycle 137 exceptional-multiplier weighted average."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-137-exceptional-multiplier-average-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-137-exceptional-multiplier-average-preregistration-v1.md", "5d00764977cd28467f497ac369eb00f6ce48a629a68450505c84be8a9b1d90d0"),
    "document": (ROOT / "docs/cycle-137-exceptional-multiplier-average-v1.md", "4244aeeef8f10042ac24709f3836fb2309519314e863813b0a78c4468f2619ff"),
    "conventions": (ROOT / "conventions/exceptional_multiplier_average_v1.py", "14d4f2a9821e0f27e35e50d856ab20dd6d3ea4b84e449dd5f0d43dacf2926144"),
    "tests": (ROOT / "tests/test_cycle_137_exceptional_multiplier_average_v1.py", "aad823510abef4ba53c1a7a4331b13ac6d53368477452a7522a73011e44e8168"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle136": (ROOT / "artifacts/cycle-136-common-multiplier-scalar-v1.json", "d3af0383df6754f59fb0515c0f0811e116c772b441868d1ad41c13360cfcf52f"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle136"][0], "SEALED_PAIRED_NORM_SCALAR_DICHOTOMY_EXCEPTIONAL_MULTIPLIER_AVERAGE_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="exceptional_multiplier_average_v1")
    module = __import__("conventions.exceptional_multiplier_average_v1", fromlist=["average_ledger"])
    cell = module.average_ledger(Fraction(16, 25), Fraction(0), Fraction(7, 45), Fraction(184, 225), Fraction(0))
    require(cell["edge_ceiling"] == Fraction(1, 45), "registered edge ceiling")
    require(cell["edge_ceiling_volume"] == Fraction(173, 450), "volume ceiling")
    require("B_exc J^2" in theorem["weighted_target"], "edge-weight target")
    require("no high-edge" in theorem["boundary"], "high-edge boundary")
    return {
        "artifact_id": "cycle-137-exceptional-multiplier-average-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_LOW_EDGE_EXCEPTION_AVERAGE_CLOSED_FAREY_DISCRETIZATION_OPEN",
        "claim_boundary": (
            "This artifact closes only edge-multiplicity cells satisfying the "
            "two strict Cycle-137 inequalities. It proves no high-edge or full "
            "exception average, paired norm, endpoint, moment, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 137"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "exceptional_multiplier_average_theorem": {"epistemic_status": "PROVED", **theorem},
        "registered_cell": {
            "epistemic_status": "PROVED",
            "xi": "16/25",
            "mu": "0",
            "rho": "7/45",
            "tau": "184/225",
            "edge_ceiling": str(cell["edge_ceiling"]),
            "volume_ceiling": str(cell["edge_ceiling_volume"]),
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "remove the N^4 Farey discretization term using edge multiplicity, "
                "or compile its weighted rational multipliers into a seed"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_137_exceptional_multiplier_average_v1.py --write",
            "check_command": "python3 proof/build_cycle_137_exceptional_multiplier_average_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_137_exceptional_multiplier_average_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 137 sealer", output=OUTPUT, payload_factory=seal))
