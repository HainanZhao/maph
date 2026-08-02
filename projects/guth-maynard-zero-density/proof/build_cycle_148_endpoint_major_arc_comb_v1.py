#!/usr/bin/env python3
"""Seal Cycle 148 endpoint major-arc comb theorem."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-148-endpoint-major-arc-comb-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-148-endpoint-major-arc-comb-preregistration-v1.md", "f288c07188fa6d4cf5aad278e323cb0cd7c01335f771224f871f84319e5fdf3b"),
    "document": (ROOT / "docs/cycle-148-endpoint-major-arc-comb-v1.md", "9427b81f88cde54d0341d7d521b39a0cc58c891df882216a1493e7ef81ad49e6"),
    "conventions": (ROOT / "conventions/endpoint_major_arc_comb_v1.py", "9fe4bbe25d463babb89dfded2bfaad694b03f34a1187479ead12429130fcba31"),
    "tests": (ROOT / "tests/test_cycle_148_endpoint_major_arc_comb_v1.py", "479263919dee61cecd23408cc159a27e061bd43bd82444f4bbc5598c2921abbb"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle132": (ROOT / "artifacts/cycle-132-unimodular-endpoint-lift-v1.json", "aeab0475962728918ab08c2b78e87dcef4bed7840c57e376557bcdcdfb434cee"),
    "cycle147": (ROOT / "artifacts/cycle-147-strict-core-signed-cell-v1.json", "95671bb99fb4f070b15e8c8210d7c69a6f9c4241d6ec5bd17434a3ab1e5116b8"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle132"][0], "SEALED_ENDPOINT_VOLUME_CLOSED_DETERMINANT_CLUSTER_NORM_OPEN")
    validate_prior(INPUTS["cycle147"][0], "SEALED_COEFFICIENT_FAITHFUL_CORE_HALO_BUNDLE_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="endpoint_major_arc_comb_v1")
    module = __import__("conventions.endpoint_major_arc_comb_v1", fromlist=["exponent_ledger"])
    ledger = module.exponent_ledger(
        xi=Fraction(7, 10),
        rho=Fraction(1, 5),
        mode_mass=Fraction(1, 4),
    )
    require(ledger["excess"] == Fraction(2, 15), "Q/N comb excess")
    require("Q/N" in theorem["diagonal_comparison"], "diagonal comparison")
    require("cannot reach" in theorem["structural_implication"], "endpoint norm obstruction")
    require("does not" in theorem["mass_boundary"], "cross-cell boundary")
    return {
        "artifact_id": "cycle-148-endpoint-major-arc-comb-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_CROSS_ENDPOINT_COMB_CANCELLATION_OR_INVERSE_OPEN",
        "claim_boundary": (
            "This artifact proves a Q/N super-diagonal lower bound for one "
            "strict positive endpoint operator in every fixed rho<1/3 band. "
            "It proves neither target mass for that operator nor absence of "
            "cross-cell cancellation, and proves no full second moment, endpoint, "
            "complete moment, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 148"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "endpoint_major_arc_comb_theorem": {"epistemic_status": "PROVED", **theorem},
        "sample_exponent_ledger": {
            "epistemic_status": "PROVED",
            **{key: str(value) for key, value in ledger.items()},
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "prove cancellation between rational endpoint combs using their "
                "common coefficient vector, or extract a target-mass comb obstruction"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_148_endpoint_major_arc_comb_v1.py --write",
            "check_command": "python3 proof/build_cycle_148_endpoint_major_arc_comb_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_148_endpoint_major_arc_comb_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 148 sealer", output=OUTPUT, payload_factory=seal))
