#!/usr/bin/env python3
"""Seal Cycle 130 broad continued-fraction cylinder closure."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-130-broad-cf-cylinder-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-130-broad-cylinder-preregistration-v1.md", "376db1015de56f89816b7ffae18388ed78feab5c3c9e3a48ebbf73fb3d33bea2"),
    "document": (ROOT / "docs/cycle-130-broad-cf-cylinder-v1.md", "decebd4469ab8dca709924b301ed8724017a8bf3d0c7959a275c845b728c2a06"),
    "conventions": (ROOT / "conventions/broad_cf_cylinder_v1.py", "a17f2dfe6d854b236227af89e89b4a5a3b18dc7e32a87b3eaaa3be75ec1132eb"),
    "tests": (ROOT / "tests/test_cycle_130_broad_cf_cylinder_v1.py", "7d79e1878a90ce487b9fa61f85622096651f34c385eb3209d393e87345ed9eb4"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle129": (ROOT / "artifacts/cycle-129-continued-fraction-jump-v1.json", "8be0a48187028ba3ca4ddf46a2c80d4e682207855cc86a1756b25c607de861bf"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle129"][0], "SEALED_COLLISIONS_FORCE_POWER_PARTIAL_QUOTIENT_AVERAGE_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="broad_cf_cylinder_v1")
    module = __import__("conventions.broad_cf_cylinder_v1", fromlist=["cylinder_ledger"])
    left = module.cylinder_ledger(Fraction(16, 25), Fraction(0))
    require(left["target_margin"] == Fraction(1, 25), "target margin")
    require(left["narrow_range_width"] == Fraction(14, 75), "narrow width")
    require("O(1+D|J|)" in theorem["grid_spacing"], "grid count")
    require("D/A0" in theorem["broad_count"], "broad count")
    require("narrow cylinders" in theorem["remaining_range"], "remaining range")
    require("no narrow-cylinder" in theorem["boundary"], "claim boundary")
    return {
        "artifact_id": "cycle-130-broad-cf-cylinder-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_BROAD_CF_CYLINDERS_VOLUME_CLOSED_NARROW_ENDPOINT_OPEN",
        "claim_boundary": (
            "This artifact closes only convergent cylinders with "
            "q<=sqrt(DQ/(KM^2)). It proves no narrow-cylinder, full low-"
            "multiplicity or simple-root closure, complete moment, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 130"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "broad_cylinder_theorem": {"epistemic_status": "PROVED", **theorem},
        "lower_endpoint_ledger": {
            "epistemic_status": "PROVED",
            "broad_denominator_ceiling": str(left["broad_denominator_ceiling"]),
            "narrow_range_width": str(left["narrow_range_width"]),
            "target_margin": str(left["target_margin"]),
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "control narrow cylinders sqrt(DQ/(KM^2))<q<<Q/M by endpoint "
                "discrepancy or compile their relation graph"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_130_broad_cf_cylinder_v1.py --write",
            "check_command": "python3 proof/build_cycle_130_broad_cf_cylinder_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_130_broad_cf_cylinder_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 130 sealer", output=OUTPUT, payload_factory=seal))
