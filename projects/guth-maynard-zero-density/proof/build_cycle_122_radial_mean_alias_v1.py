#!/usr/bin/env python3
"""Seal Cycle 122 radial zero-mode cancellation and alias map."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-122-radial-mean-alias-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-122-radial-mean-alias-preregistration-v1.md", "95d16b2d50fe98c54368fc99fe60192c19acaa26af91f0cfd3393f744259ca46"),
    "document": (ROOT / "docs/cycle-122-radial-mean-alias-v1.md", "c0b307139f1e5513336791d8717156fe7fad32bbb6a6e14e54d7767c89447094"),
    "conventions": (ROOT / "conventions/radial_mean_alias_v1.py", "54ed6e7daebfd45c872729cc0ac4c6c8f0c22359dc1ab89a206799f256ef8661"),
    "tests": (ROOT / "tests/test_cycle_122_radial_mean_alias_v1.py", "d1a8dd59ac250081e9d118b373e3074bb9714df1be4a002b0f8a871aec95cbe7"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle121": (ROOT / "artifacts/cycle-121-projective-amplitude-v1.json", "5c003a1ce44fc5a87d7997fa80d71c18729ad3c89d857f09955a7baf0110317f"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle121"][0], "SEALED_PROJECTIVE_AMPLITUDE_COLLAPSE_RADIAL_OPERATOR_BOUND_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="radial_mean_alias_v1")
    module = __import__("conventions.radial_mean_alias_v1", fromlist=["alias_exponent_ledger"])
    left = module.alias_exponent_ledger(Fraction(16, 25))
    require("U^(j)(0)=0" in theorem["vanishing_moments"], "moment cancellation")
    require("(cH0)^(-N)" in theorem["zero_mode"], "rapid zero-mode decay")
    require("n*=Hc/ell" in theorem["nonzero_saddle"], "alias saddle")
    require("ell~K" in theorem["alias_support"], "alias order")
    require(left["n_stationary_amplitude"] == Fraction(-23, 150), "left amplitude exponent")
    require("no bound" in theorem["boundary"], "claim boundary")
    return {
        "artifact_id": "cycle-122-radial-mean-alias-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_RADIAL_ZERO_MODE_REMOVED_K_ALIAS_OPERATOR_OPEN",
        "claim_boundary": (
            "This artifact removes the continuous n-Poisson mode and derives the "
            "nonzero ell~K saddle map. It proves no bound for those aliases, "
            "simple-root closure, complete moment, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 122"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "radial_mean_alias_theorem": {"epistemic_status": "PROVED", **theorem},
        "left_endpoint_ledger": {
            "epistemic_status": "PROVED",
            "alias_order": str(left["alias_order"]),
            "stationary_amplitude": str(left["n_stationary_amplitude"]),
            "Hc_scale": str(left["Hc_scale"]),
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "bound the ell~K entropy aliases with the Cycle-121 arithmetic "
                "weight or extract a phase-aware inverse"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_122_radial_mean_alias_v1.py --write",
            "check_command": "python3 proof/build_cycle_122_radial_mean_alias_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_122_radial_mean_alias_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 122 sealer", output=OUTPUT, payload_factory=seal))
