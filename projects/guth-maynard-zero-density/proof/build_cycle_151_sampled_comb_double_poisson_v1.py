#!/usr/bin/env python3
"""Seal Cycle 151 sampled-comb lcm/tail-transform theorem."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-151-sampled-comb-double-poisson-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-151-sampled-comb-double-poisson-preregistration-v1.md", "684feff0d41e5c423991bcd8d211ff82098294362636aeb191dc12561166280f"),
    "document": (ROOT / "docs/cycle-151-sampled-comb-double-poisson-v1.md", "6dca9b595141bc4a47c8fbc7974fe18b8f28d1ec236194d42ef55896310d3e5c"),
    "conventions": (ROOT / "conventions/sampled_comb_double_poisson_v1.py", "9fe253b4f9654025e23e0f38a641be6d67b18d17c54ff9a3f849252070ba17e5"),
    "tests": (ROOT / "tests/test_cycle_151_sampled_comb_double_poisson_v1.py", "35e95a77518b724facc3f01fc416832cc44ba6016944d2d0dd18fb4dea460782"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle150": (ROOT / "artifacts/cycle-150-divisor-comb-sign-test-v1.json", "1039725acb7e764e1d352a7506756f5c6b620b232bfddeaf6c0cb1b0e73f1269"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle150"][0], "SEALED_HALO_BOUNDARY_DIVISOR_COMB_ESTIMATE_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="sampled_comb_double_poisson_v1")
    module = __import__("conventions.sampled_comb_double_poisson_v1", fromlist=["exponent_ledger"])
    ledger = module.exponent_ledger(
        xi=Fraction(7, 10),
        rho=Fraction(1, 5),
        rho_b=Fraction(1, 4),
        gamma=Fraction(1, 10),
    )
    require(ledger["lcm"] == Fraction(7, 20), "lcm exponent")
    require(ledger["relative_to_witness"] == Fraction(-3, 20), "gcd capacity")
    require("lcm" in theorem["structural_implication"], "lcm lock")
    require("negative" in theorem["negative_lobe"], "tail-sign lock")
    require("not bounded" in theorem["boundary"], "claim boundary")
    return {
        "artifact_id": "cycle-151-sampled-comb-double-poisson-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_GCD_WEIGHTED_NEGATIVE_TAIL_LOBE_OR_BOUNDARY_OPEN",
        "claim_boundary": (
            "This artifact proves the lcm resonance lattice and fixed-chart "
            "tail-transform formula for smooth halo denominators a fixed power "
            "below Q. It does not bound the gcd-weighted negative-lobe population "
            "or boundary denominators and proves no full moment, endpoint, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 151"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "sampled_comb_double_poisson_theorem": {"epistemic_status": "PROVED", **theorem},
        "sample_exponent_ledger": {
            "epistemic_status": "PROVED",
            **{key: str(value) for key, value in ledger.items()},
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "bound the gcd-weighted population of endpoint tails in negative "
                "transform lobes and treat denominators within a fixed power of Q"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_151_sampled_comb_double_poisson_v1.py --write",
            "check_command": "python3 proof/build_cycle_151_sampled_comb_double_poisson_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_151_sampled_comb_double_poisson_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 151 sealer", output=OUTPUT, payload_factory=seal))
