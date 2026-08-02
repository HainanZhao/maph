#!/usr/bin/env python3
"""Seal Cycle 132 unimodular endpoint lift."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-132-unimodular-endpoint-lift-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-132-unimodular-endpoint-preregistration-v1.md", "fa954c04667d34c4ed6704b6a99ce9fa4281a7fd336a25f28f1ef5a7c8e61278"),
    "document": (ROOT / "docs/cycle-132-unimodular-endpoint-lift-v1.md", "9a17f63677c05a42fe37b0d856588ce3b55559a0e30f8dab1b800bd19c52cfbb"),
    "conventions": (ROOT / "conventions/unimodular_endpoint_lift_v1.py", "1a72c6e7205e16dd7e358aa37eb5f1c5f743d9c07e259759857107bf60f3c19f"),
    "tests": (ROOT / "tests/test_cycle_132_unimodular_endpoint_lift_v1.py", "1de156bf9f6c6d2282398583932a7c64557b7009ae1a404ce606622b6490d208"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle129": (ROOT / "artifacts/cycle-129-continued-fraction-jump-v1.json", "8be0a48187028ba3ca4ddf46a2c80d4e682207855cc86a1756b25c607de861bf"),
    "cycle131": (ROOT / "artifacts/cycle-131-order-three-denominator-bridge-v1.json", "1fa3645c6cf6c59abc35604de076412cf413593ea49d5e5a214f9dee0aa99e55"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle129"][0], "SEALED_COLLISIONS_FORCE_POWER_PARTIAL_QUOTIENT_AVERAGE_OPEN")
    validate_prior(INPUTS["cycle131"][0], "SEALED_DENOMINATORS_TO_7_45_MINUS_2MU_3_ENDPOINT_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="unimodular_endpoint_lift_v1")
    module = __import__("conventions.unimodular_endpoint_lift_v1", fromlist=["extremal_ledger"])
    left = module.extremal_ledger(Fraction(16, 25), Fraction(0))
    require(left["volume_margin"] == Fraction(1, 25), "minimum endpoint volume margin")
    require(left["fourier_bandwidth"] == Fraction(28, 75), "minimum natural bandwidth")
    require(left["cluster_allowance"] == 0, "full-endpoint cluster threshold")
    require("determinant s" in theorem["inverse_graph"], "determinant-labelled inverse")
    require("Fourier norm is not proved" in theorem["boundary"], "claim boundary")
    return {
        "artifact_id": "cycle-132-unimodular-endpoint-lift-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_ENDPOINT_VOLUME_CLOSED_DETERMINANT_CLUSTER_NORM_OPEN",
        "claim_boundary": (
            "This artifact closes only the endpoint zeroth-mode volume and proves "
            "a determinant-labelled cluster inverse. The nonzero Fourier norm, "
            "endpoint, low-multiplicity, simple-root, complete moment, density, "
            "and prime intervals remain open."
        ),
        "runtime": check_runtime("Cycle 132"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "unimodular_endpoint_theorem": {"epistemic_status": "PROVED", **theorem},
        "worst_endpoint_ledger": {
            "epistemic_status": "PROVED",
            "xi": "16/25",
            "mu": "0",
            "rho": str(left["rho"]),
            "tau": str(left["tau"]),
            "fourier_bandwidth": str(left["fourier_bandwidth"]),
            "restored_volume": str(left["restored_volume"]),
            "volume_margin": str(left["volume_margin"]),
            "cluster_allowance": str(left["cluster_allowance"]),
            "ray_tolerance": str(left["ray_tolerance"]),
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "prove the Cycle-132 logarithmic Fourier norm or feed its "
                "determinant-labelled cluster graph into the recurrence compiler"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_132_unimodular_endpoint_lift_v1.py --write",
            "check_command": "python3 proof/build_cycle_132_unimodular_endpoint_lift_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_132_unimodular_endpoint_lift_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 132 sealer", output=OUTPUT, payload_factory=seal))
