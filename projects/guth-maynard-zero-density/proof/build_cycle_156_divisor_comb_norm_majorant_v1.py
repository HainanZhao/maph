#!/usr/bin/env python3
"""Seal Cycle 156 exact divisor-comb norm majorant."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-156-divisor-comb-norm-majorant-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-156-divisor-comb-norm-preregistration-v1.md", "e18503890a96f7fa78451068ed0d33b29d88ea5093d40d24bf255a3ff768f90d"),
    "document": (ROOT / "docs/cycle-156-divisor-comb-norm-v1.md", "01002a20685abfd681d440960f3b413049f046c7b1b179265a55df15e457ac25"),
    "conventions": (ROOT / "conventions/divisor_comb_norm_majorant_v1.py", "b8bbd8bb173b843cca728b9052684e3119273db00b01ef493297624b4ff21765"),
    "tests": (ROOT / "tests/test_cycle_156_divisor_comb_norm_majorant_v1.py", "30c6bc1a97bd2a7fd34d2a666f88d064fff16d2cb9821204102040e17cffaf61"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle150": (ROOT / "artifacts/cycle-150-divisor-comb-sign-test-v1.json", "1039725acb7e764e1d352a7506756f5c6b620b232bfddeaf6c0cb1b0e73f1269"),
    "cycle154": (ROOT / "artifacts/cycle-154-coefficient-escape-localization-v1.json", "3d17a6773aa714d83c12bc7beddbde5bfefc499f82ba7848f79cdf3cd7f28184"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle150"][0], "SEALED_HALO_BOUNDARY_DIVISOR_COMB_ESTIMATE_OPEN")
    validate_prior(INPUTS["cycle154"][0], "SEALED_CONDITIONAL_FINITE_LABELLED_ESCAPE_LOCALIZATION")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="divisor_comb_norm_majorant_v1")
    module = __import__("conventions.divisor_comb_norm_majorant_v1", fromlist=["divisor_comb_norm_majorant"])
    special = module.divisor_comb_norm_majorant(
        frequency_length=10, modulus=4, anchor_ratio=Fraction(1)
    )
    general = module.divisor_comb_norm_majorant(
        frequency_length=10, modulus=15, anchor_ratio=Fraction(3, 2)
    )
    require(special["multiple_count"] == 3, "exact special count")
    require(special["norm_squared_majorant_constant"] == 2, "A equals two")
    require(general["norm_squared_majorant_constant"] == Fraction(5, 2), "frozen general A")
    require("Cycle 154" in theorem["cycle154_interface"], "Cycle 154 interface")
    return {
        "artifact_id": "cycle-156-divisor-comb-norm-majorant-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_EXACT_DIVISOR_COMB_NORM_MAJORANT_ACTUAL_FINITE_PARTITION_OPEN",
        "claim_boundary": (
            "This artifact proves an exact fixed-constant norm majorant for the selected divisor comb only. "
            "It does not establish an actual finite coefficient partition, escape projection, positive transport, "
            "bounded fan, moment, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 156"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "divisor_comb_norm_majorant": {"epistemic_status": "PROVED", **theorem},
        "samples": {
            "epistemic_status": "PROVED",
            "h_at_most_k": {key: str(value) for key, value in special.items()},
            "fixed_anchor_ratio": {key: str(value) for key, value in general.items()},
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "construct or reject Cycle 155's actual exact fixed finite reason-labelled coefficient-escape partition; "
                "then Cycle 154 localizes a class with this now-fixed norm constant"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_156_divisor_comb_norm_majorant_v1.py --write",
            "check_command": "python3 proof/build_cycle_156_divisor_comb_norm_majorant_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_156_divisor_comb_norm_majorant_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 156 sealer", output=OUTPUT, payload_factory=seal))
