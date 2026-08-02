#!/usr/bin/env python3
"""Seal Cycle 134 transition entropy and tail anchor."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-134-transition-entropy-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-134-transition-entropy-preregistration-v1.md", "7eb143584173102c678301d950196855e91f4f69d8341451cd9c32e3537d2ce3"),
    "document": (ROOT / "docs/cycle-134-transition-entropy-v1.md", "27ee06d51a98ca4f5c142235b591d450acaa2119fe52d463d75137b4a7b48101"),
    "conventions": (ROOT / "conventions/transition_entropy_v1.py", "2d28244d1196e0ce9dd563fc67b4b4db4724eeb9d74b3678796591afd55b79eb"),
    "tests": (ROOT / "tests/test_cycle_134_transition_entropy_v1.py", "4feade2eff29c978adfc372151519ba8d175415228f65dc471afe2f37ea133b8"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle133": (ROOT / "artifacts/cycle-133-determinant-cluster-energy-v1.json", "c837c041cc796ec2553a97074d66707ad6fb339bcc6530beddc242eb06d56427"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle133"][0], "SEALED_EXACT_DETERMINANT_FREIMAN_SUBRANGE_TRANSITION_CONCENTRATION_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="transition_entropy_v1")
    module = __import__("conventions.transition_entropy_v1", fromlist=["entropy_ledger"])
    edge = module.entropy_ledger(Fraction(16, 25), Fraction(0), Fraction(1, 3), Fraction(16, 25))
    require(edge["shear_entropy"] == Fraction(23, 75), "minimum full-endpoint shear entropy")
    require("theta" in theorem["scoped_no_go"], "tail coordinate retained")
    require("not a no-go theorem" in theorem["boundary"], "scoped boundary")
    return {
        "artifact_id": "cycle-134-transition-entropy-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_DETERMINANT_ONLY_SHEAR_ENTROPY_TAIL_PHASE_REQUIRED",
        "claim_boundary": (
            "This artifact is a data-class no-go for determinant-only transition "
            "compilers. It is not a no-go for the phase-coupled operator and proves "
            "no transition concentration, seed, endpoint, moment, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 134"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "transition_entropy_theorem": {"epistemic_status": "PROVED", **theorem},
        "full_endpoint_ledger": {
            "epistemic_status": "PROVED",
            "xi": "16/25",
            "mu": "0",
            "rho": "1/3",
            "tau": "16/25",
            "shear_entropy": str(edge["shear_entropy"]),
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "retain theta or the signed collision residual in a repeated-difference "
                "transition operator and prove phase-coupled concentration or cancellation"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_134_transition_entropy_v1.py --write",
            "check_command": "python3 proof/build_cycle_134_transition_entropy_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_134_transition_entropy_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 134 sealer", output=OUTPUT, payload_factory=seal))
