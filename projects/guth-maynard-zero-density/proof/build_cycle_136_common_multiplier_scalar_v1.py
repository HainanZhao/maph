#!/usr/bin/env python3
"""Seal Cycle 136 common-multiplier scalar dichotomy."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-136-common-multiplier-scalar-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-136-common-multiplier-preregistration-v1.md", "53b29de2ed32b30758fa286ca1cc796cbdec142e252fe81cee7c2da9828baa70"),
    "document": (ROOT / "docs/cycle-136-common-multiplier-scalar-v1.md", "baf74ed31cac4cfe9123d41e40344246ba27388c7cfc6c0df920872c4c27830f"),
    "conventions": (ROOT / "conventions/common_multiplier_scalar_v1.py", "f376f8c8e723fcd623a421bf7c03a6f30e21ffa2363d8b2195ef65d5f0cd71a6"),
    "tests": (ROOT / "tests/test_cycle_136_common_multiplier_scalar_v1.py", "d75ff1e0b4b32602786079946c9d2be0c758bb94176f276da38717fb2e6a1aac"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle133": (ROOT / "artifacts/cycle-133-determinant-cluster-energy-v1.json", "c837c041cc796ec2553a97074d66707ad6fb339bcc6530beddc242eb06d56427"),
    "cycle135": (ROOT / "artifacts/cycle-135-tail-coupled-transition-v1.json", "fa5dcd292a3076e865ffaf7b40f7bef595b803688c37bcc6df7d65be83a76464"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle133"][0], "SEALED_EXACT_DETERMINANT_FREIMAN_SUBRANGE_TRANSITION_CONCENTRATION_OPEN")
    validate_prior(INPUTS["cycle135"][0], "SEALED_TAIL_MARGINAL_SELF_DUAL_PAIRED_EDGE_NORM_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="common_multiplier_scalar_v1")
    module = __import__("conventions.common_multiplier_scalar_v1", fromlist=["scalar_ledger"])
    sample = module.scalar_ledger(Fraction(7, 10), Fraction(0), Fraction(1, 5), Fraction(13, 20))
    require(sample["legendre_margin"] == Fraction(1, 10), "strict Legendre margin")
    require(sample["next_partial_quotient_floor"] == Fraction(1, 10), "jump exponent")
    require("N^3/S" in theorem["scalar_dichotomy"], "scalar threshold")
    require("no averaged exclusion" in theorem["boundary"], "exception average open")
    return {
        "artifact_id": "cycle-136-common-multiplier-scalar-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_PAIRED_NORM_SCALAR_DICHOTOMY_EXCEPTIONAL_MULTIPLIER_AVERAGE_OPEN",
        "claim_boundary": (
            "This artifact proves the paired diagonal bound only away from one "
            "scalar exception and compiles exceptions to continued-fraction jumps "
            "only in the strict S>>N^3 region. It proves no averaged exclusion, "
            "full paired norm, endpoint, moment, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 136"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "common_multiplier_scalar_theorem": {"epistemic_status": "PROVED", **theorem},
        "sample_strict_ledger": {
            "epistemic_status": "PROVED",
            "xi": "7/10",
            "mu": "0",
            "rho": "1/5",
            "tau": "13/20",
            "legendre_margin": str(sample["legendre_margin"]),
            "next_denominator_floor": str(sample["next_denominator_floor"]),
            "next_partial_quotient_floor": str(sample["next_partial_quotient_floor"]),
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "average the exceptional convergent jumps of g^d over popular "
                "differences d, retaining r_d and the original phase anchor"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_136_common_multiplier_scalar_v1.py --write",
            "check_command": "python3 proof/build_cycle_136_common_multiplier_scalar_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_136_common_multiplier_scalar_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 136 sealer", output=OUTPUT, payload_factory=seal))
