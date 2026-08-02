#!/usr/bin/env python3
"""Seal Cycle 135 tail-coupled transition operator."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-135-tail-coupled-transition-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-135-tail-coupled-transition-preregistration-v1.md", "adc3b14a3ccdc54c77135c53305169ad1062183e65ab6b8c565d3b0041eef3dd"),
    "document": (ROOT / "docs/cycle-135-tail-coupled-transition-v1.md", "029232eff6347070355a3377f090b45321899029dccff2fec333dce360f99a14"),
    "conventions": (ROOT / "conventions/tail_coupled_transition_v1.py", "be48a9104a056f9dd062c59051cc6bdc70e3b604e4f4641ee3b2cc58bdb90200"),
    "tests": (ROOT / "tests/test_cycle_135_tail_coupled_transition_v1.py", "a15c0bb9a2fcf0d9102608a693807dcde6cc19ebd31c91ee2e7a22501d596dd2"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle132": (ROOT / "artifacts/cycle-132-unimodular-endpoint-lift-v1.json", "aeab0475962728918ab08c2b78e87dcef4bed7840c57e376557bcdcdfb434cee"),
    "cycle134": (ROOT / "artifacts/cycle-134-transition-entropy-v1.json", "02141cd02825052f2de39cb1edff0499f9d073c1f7c00e748eaa7d3f98722202"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle132"][0], "SEALED_ENDPOINT_VOLUME_CLOSED_DETERMINANT_CLUSTER_NORM_OPEN")
    validate_prior(INPUTS["cycle134"][0], "SEALED_DETERMINANT_ONLY_SHEAR_ENTROPY_TAIL_PHASE_REQUIRED")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="tail_coupled_transition_v1")
    module = __import__("conventions.tail_coupled_transition_v1", fromlist=["frequency_ledger"])
    edge = module.frequency_ledger(Fraction(16, 25), Fraction(0), Fraction(1, 3), Fraction(16, 25))
    require(edge["tail_frequency"] == Fraction(23, 75), "full-endpoint tail frequency")
    require(edge["raw_residual_frequency"] == Fraction(32, 25), "raw residual frequency")
    require("reproduces the Cycle-132" in theorem["marginal_no_gain"], "marginal no-gain scope")
    require("not proved" in theorem["boundary"], "paired norm remains open")
    return {
        "artifact_id": "cycle-135-tail-coupled-transition-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_TAIL_MARGINAL_SELF_DUAL_PAIRED_EDGE_NORM_OPEN",
        "claim_boundary": (
            "This artifact proves only that tail-only projection telescopes to "
            "the Cycle-132 discrepancy and derives the exact paired-edge target. "
            "It proves no paired-tail bound, transition concentration, seed, "
            "endpoint, moment, density, or prime intervals."
        ),
        "runtime": check_runtime("Cycle 135"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "tail_coupled_transition_theorem": {"epistemic_status": "PROVED", **theorem},
        "full_endpoint_frequency_ledger": {
            "epistemic_status": "PROVED",
            "tail_frequency": str(edge["tail_frequency"]),
            "raw_residual_frequency": str(edge["raw_residual_frequency"]),
            "normalized_residual_scale": str(edge["normalized_residual_scale"]),
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "prove the fixed-difference paired-tail diagonal second moment "
                "at L=S/N or invert its excess into a phase-anchored chain"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_135_tail_coupled_transition_v1.py --write",
            "check_command": "python3 proof/build_cycle_135_tail_coupled_transition_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_135_tail_coupled_transition_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 135 sealer", output=OUTPUT, payload_factory=seal))
