#!/usr/bin/env python3
"""Seal Cycle 150 divisor-comb sign test and escape inverse."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-150-divisor-comb-sign-test-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-150-divisor-comb-sign-test-preregistration-v1.md", "3435448be32780993a9b81b94afda02ca106fb545fc966043c1b78a7b30f7144"),
    "document": (ROOT / "docs/cycle-150-divisor-comb-sign-test-v1.md", "0779438399729435bd8bb86114c75bf1775d3f334971b938d19a419f9305034a"),
    "conventions": (ROOT / "conventions/divisor_comb_sign_test_v1.py", "07695886b7643ef972fceb334d148b8962bdd4d971ba83b666320f27fd8bb575"),
    "tests": (ROOT / "tests/test_cycle_150_divisor_comb_sign_test_v1.py", "2e9c27d4e60f9fc3f50ebfc73216f76fa248afe2da4e9500aad83630e987ab1a"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle148": (ROOT / "artifacts/cycle-148-endpoint-major-arc-comb-v1.json", "9549454a2cefd60d37673ecd9b7f012bb8d18bcb24ff7f439c99005e99604cbb"),
    "cycle149": (ROOT / "artifacts/cycle-149-target-mass-comb-inverse-v1.json", "2e7b318892e5ee0807d30a2d548b515a837a54757a3596223df5097c86564a48"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle148"][0], "SEALED_CROSS_ENDPOINT_COMB_CANCELLATION_OR_INVERSE_OPEN")
    validate_prior(INPUTS["cycle149"][0], "SEALED_DIVISOR_COMB_ANTIALIGNMENT_EXCLUSION_OR_MODEL_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="divisor_comb_sign_test_v1")
    module = __import__("conventions.divisor_comb_sign_test_v1", fromlist=["one_ray_escape_ledger"])
    ledger = module.one_ray_escape_ledger(
        xi=Fraction(7, 10),
        rho=Fraction(1, 5),
    )
    require(ledger["excess"] == Fraction(2, 15), "one-ray escape excess")
    require("reinforce" in theorem["no_strict_antialignment"], "strict sign exclusion")
    require("endpoint error" in theorem["escape_split"], "escape classes")
    require("not bounded" in theorem["boundary"], "claim boundary")
    return {
        "artifact_id": "cycle-150-divisor-comb-sign-test-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_HALO_BOUNDARY_DIVISOR_COMB_ESTIMATE_OPEN",
        "claim_boundary": (
            "This artifact proves that strict positive endpoint modes cannot "
            "supply the Cycle-149 negative divisor-comb correlation and forces a "
            "quantified escape-class norm. It does not bound or exclude the "
            "escape class and proves no full second moment, endpoint, complete "
            "moment, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 150"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "divisor_comb_sign_test_theorem": {"epistemic_status": "PROVED", **theorem},
        "sample_exponent_ledger": {
            "epistemic_status": "PROVED",
            **{key: str(value) for key, value in ledger.items()},
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "bound the halo and boundary-denominator negative divisor-comb "
                "projection, retaining phase-changing and nonsmooth payload separately"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_150_divisor_comb_sign_test_v1.py --write",
            "check_command": "python3 proof/build_cycle_150_divisor_comb_sign_test_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_150_divisor_comb_sign_test_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 150 sealer", output=OUTPUT, payload_factory=seal))
