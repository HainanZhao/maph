#!/usr/bin/env python3
"""Seal Cycle 131 order-three denominator bridge."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-131-order-three-denominator-bridge-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-131-order-three-bridge-preregistration-v1.md", "b35cd3f9dcb0119f4aed086e50ba83e121800e9056f6345960cc1c089ddefc31"),
    "document": (ROOT / "docs/cycle-131-order-three-denominator-bridge-v1.md", "6e2ce62a4e2e8fb50f537579f4b04a0b88b9d975cb89c3b54eb5d75c5246e8d5"),
    "conventions": (ROOT / "conventions/order_three_denominator_bridge_v1.py", "9fdcbade003c3d1e8c5e0e85123f9705a8b2e6f3dc6f74dbc1976c6e1e7a90d2"),
    "tests": (ROOT / "tests/test_cycle_131_order_three_denominator_bridge_v1.py", "1db2a07bb973d28477d8cf3d47e56c6db24d07dcec448eedb3ad78b85c08609f"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle127": (ROOT / "artifacts/cycle-127-low-multiplicity-log-saddle-v1.json", "0dc33bc38ac1e3edf85b98abeffcdcf162fe6c6f6f335c3cc0f9bf268d78955a"),
    "cycle130": (ROOT / "artifacts/cycle-130-broad-cf-cylinder-v1.json", "07cbb17383fbc224b3a122540ce2c70ea15a01e0413a63f0b7018c2f882860ab"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle127"][0], "SEALED_LOW_MULTIPLICITY_VOLUME_MARGIN_MELLIN_DIAGONAL_OPEN")
    validate_prior(INPUTS["cycle130"][0], "SEALED_BROAD_CF_CYLINDERS_VOLUME_CLOSED_NARROW_ENDPOINT_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="order_three_denominator_bridge_v1")
    module = __import__("conventions.order_three_denominator_bridge_v1", fromlist=["range_ledger"])
    left = module.range_ledger(Fraction(16, 25), Fraction(0))
    require(left["extension_beyond_broad"] == Fraction(2, 225), "minimum extension")
    require(left["remaining_endpoint_width"] == Fraction(8, 45), "left endpoint width")
    require("all four terms are <=1/3" in theorem["closure_ceiling"], "four-term closure")
    require(">=133/900" in theorem["remaining_width"], "remaining width")
    require("no endpoint-denominator" in theorem["boundary"], "claim boundary")
    return {
        "artifact_id": "cycle-131-order-three-denominator-bridge-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_DENOMINATORS_TO_7_45_MINUS_2MU_3_ENDPOINT_OPEN",
        "claim_boundary": (
            "This artifact closes denominator blocks only through "
            "rho<=7/45-2mu/3. It proves no endpoint-denominator, full low-"
            "multiplicity or simple-root closure, complete moment, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 131"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "order_three_bridge_theorem": {"epistemic_status": "PROVED", **theorem},
        "lower_endpoint_ledger": {
            "epistemic_status": "PROVED",
            "hs_ceiling": str(left["hs_ceiling"]),
            "extension_beyond_broad": str(left["extension_beyond_broad"]),
            "remaining_endpoint_width": str(left["remaining_endpoint_width"]),
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "control 7/45-2mu/3<rho<=1/3-mu by joint endpoint discrepancy "
                "or extract a narrow-cylinder relation graph"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_131_order_three_denominator_bridge_v1.py --write",
            "check_command": "python3 proof/build_cycle_131_order_three_denominator_bridge_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_131_order_three_denominator_bridge_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 131 sealer", output=OUTPUT, payload_factory=seal))
