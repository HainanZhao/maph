#!/usr/bin/env python3
"""Seal Cycle 149 target-mass comb anti-alignment inverse."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-149-target-mass-comb-inverse-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-149-target-mass-comb-inverse-preregistration-v1.md", "a3b099d71c4331f88d60c1da51b735d4a5d01a4ca168e217ab993081cad4939f"),
    "document": (ROOT / "docs/cycle-149-target-mass-comb-inverse-v1.md", "80952c11f36eb6062b5915b34fbea6bde10d13d4cbd7febcac367f6e425c15f4"),
    "conventions": (ROOT / "conventions/target_mass_comb_inverse_v1.py", "aaf8e1193cd4b4788ee32cc9a71427086911a16dd49bfb3794ca352428c1f38c"),
    "tests": (ROOT / "tests/test_cycle_149_target_mass_comb_inverse_v1.py", "7c43bbc5f3fc5268efef19797b4339c7d311875536eae0beefe85aa75e5d63c6"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle148": (ROOT / "artifacts/cycle-148-endpoint-major-arc-comb-v1.json", "9549454a2cefd60d37673ecd9b7f012bb8d18bcb24ff7f439c99005e99604cbb"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle148"][0], "SEALED_CROSS_ENDPOINT_COMB_CANCELLATION_OR_INVERSE_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="target_mass_comb_inverse_v1")
    module = __import__("conventions.target_mass_comb_inverse_v1", fromlist=["exponent_ledger"])
    ledger = module.exponent_ledger(
        rho=Fraction(1, 5),
        endpoint_mode_exponent=Fraction(1, 2),
    )
    require(ledger["threshold_exponent"] == Fraction(7, 15), "endpoint threshold")
    require(ledger["relative_antialignment_exponent"] == Fraction(-1, 60), "half-power inverse")
    require("R_C/D=N/Q" in theorem["occupancy_threshold"], "critical occupancy")
    require("denominator h" in theorem["modulus_witness"], "modulus witness")
    require("not excluded" in theorem["boundary"], "claim boundary")
    return {
        "artifact_id": "cycle-149-target-mass-comb-inverse-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_DIVISOR_COMB_ANTIALIGNMENT_EXCLUSION_OR_MODEL_OPEN",
        "claim_boundary": (
            "This artifact proves the exact endpoint occupancy threshold and a "
            "coefficient-sensitive Hilbert anti-alignment inverse, including one "
            "retained denominator witness. It does not exclude anti-alignment and "
            "proves no full second moment, endpoint, complete moment, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 149"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "target_mass_comb_inverse_theorem": {"epistemic_status": "PROVED", **theorem},
        "sample_exponent_ledger": {
            "epistemic_status": "PROVED",
            **{key: str(value) for key, value in ledger.items()},
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "exclude the retained negative divisor-comb correlation using the "
                "complement phase geometry, or construct an explicit actual model"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_149_target_mass_comb_inverse_v1.py --write",
            "check_command": "python3 proof/build_cycle_149_target_mass_comb_inverse_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_149_target_mass_comb_inverse_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 149 sealer", output=OUTPUT, payload_factory=seal))
