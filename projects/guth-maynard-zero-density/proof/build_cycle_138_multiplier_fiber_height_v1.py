#!/usr/bin/env python3
"""Seal Cycle 138 multiplier-fiber height descent."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-138-multiplier-fiber-height-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-138-multiplier-fiber-preregistration-v1.md", "615c9d80e8199d94a9f091681e204859be5d24b7d2d9c9b1fdc9f13e53e2131a"),
    "document": (ROOT / "docs/cycle-138-multiplier-fiber-height-v1.md", "fb7b216164b86511fc9be967c38305af656d7987eb38e2d0a07291f2d012cf69"),
    "conventions": (ROOT / "conventions/multiplier_fiber_height_v1.py", "827c0ed58bf931f8d74d2feff2794fcf3ccc4e37da3540df6fbf873b37d6bcbf"),
    "tests": (ROOT / "tests/test_cycle_138_multiplier_fiber_height_v1.py", "d0079582ed19cef776a1611d05c37a6310ba981fe33afa11a6339949e5a58819"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle137": (ROOT / "artifacts/cycle-137-exceptional-multiplier-average-v1.json", "305d9dfe39e0f3c2b18d7969eecc2e6b8f898aefe8565f03bcd7925cf4cf4359"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle137"][0], "SEALED_LOW_EDGE_EXCEPTION_AVERAGE_CLOSED_FAREY_DISCRETIZATION_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="multiplier_fiber_height_v1")
    module = __import__("conventions.multiplier_fiber_height_v1", fromlist=["closure_ledger"])
    cell = module.closure_ledger(Fraction(16, 25), Fraction(0), Fraction(29, 180), Fraction(4, 5))
    require(cell["rho_ceiling"] == Fraction(1, 6), "rho ceiling")
    require(cell["extension_beyond_hs"] == Fraction(1, 90), "minimum extension")
    require(cell["discretization_margin"] > 0 and cell["volume_margin"] > 0, "strict sample closure")
    require("cancels exactly" in theorem["weighted_count"], "J^2 cancellation")
    require("no full paired norm" in theorem["boundary"], "regional claim boundary")
    return {
        "artifact_id": "cycle-138-multiplier-fiber-height-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_ALL_EDGE_MULTIPLICITIES_TO_1_6_MINUS_MU_2_UPPER_FAREY_RANGE_OPEN",
        "claim_boundary": (
            "This artifact closes the exceptional-multiplier weighted average "
            "for every edge multiplicity only under the two strict regional "
            "conditions. It proves no full paired norm, endpoint, moment, density, "
            "or prime intervals."
        ),
        "runtime": check_runtime("Cycle 138"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "multiplier_fiber_height_theorem": {"epistemic_status": "PROVED", **theorem},
        "registered_cell": {
            "epistemic_status": "PROVED",
            "xi": "16/25",
            "mu": "0",
            "rho": "29/180",
            "tau": "4/5",
            "rho_ceiling": str(cell["rho_ceiling"]),
            "extension_beyond_hs": str(cell["extension_beyond_hs"]),
            "discretization_margin": str(cell["discretization_margin"]),
            "volume_margin": str(cell["volume_margin"]),
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "control rho>=1/6-mu/2 by curvature across multiplier "
                "denominators or compile the surviving high-height ratio graph"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_138_multiplier_fiber_height_v1.py --write",
            "check_command": "python3 proof/build_cycle_138_multiplier_fiber_height_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_138_multiplier_fiber_height_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 138 sealer", output=OUTPUT, payload_factory=seal))
