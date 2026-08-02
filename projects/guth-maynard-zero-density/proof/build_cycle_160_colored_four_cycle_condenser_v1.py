#!/usr/bin/env python3
"""Seal Cycle 160 coefficient-weighted off-diagonal condenser."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-160-colored-four-cycle-condenser-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-160-colored-four-cycle-condenser-preregistration-v1.md", "ec681027c027074cdffb411456f00c2688f35a11b696cb74c80a6790a7d75b25"),
    "document": (ROOT / "docs/cycle-160-colored-four-cycle-condenser-v1.md", "72046d3fc6d18271b36c85ad1c2052a666e11a7ab8f201bb2343adec0e3e6c3b"),
    "conventions": (ROOT / "conventions/colored_four_cycle_condenser_v1.py", "31143d357be67b92e5969e72b8a97aadecbc3d3023ff4dd4ce3f7827dcc4b03f"),
    "tests": (ROOT / "tests/test_cycle_160_colored_four_cycle_condenser_v1.py", "6144c5dbe80aab17eab724ed3432a795f386761d7afb917725cba0e738878b02"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle87": (ROOT / "artifacts/cycle-87-mellin-alias-atlas-v1.json", "68b88ccd4ce3e5371906e3b0da3c254056b79bad9504880ebbff04b9cebce8ca"),
    "cycle89": (ROOT / "artifacts/cycle-89-moment-concentration-gate-v1.json", "93e22952845f8e5b21ad841d79604a09eccc26ca9ca083bf1f65ac0a60de5dc8"),
    "cycle159": (ROOT / "artifacts/cycle-159-coefficient-selector-information-loss-v1.json", "4891fc7ba34340a4ff76cd6cdf26d76ac45ca65ad3042e460e0ef1681a0c52ea"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle87"][0], "SEALED_MELLIN_ALIAS_TRICHOTOMY_BOUND_OR_WEB_OPEN")
    validate_prior(INPUTS["cycle89"][0], "SEALED_MOMENT_CONCENTRATION_OR_SATURATION_INVERSE_OPEN")
    validate_prior(INPUTS["cycle159"][0], "SEALED_PRIMITIVE_RAY_MULTIPLIER_INFORMATION_LOSS_COEFFICIENT_PRESERVING_SELECTOR_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="colored_four_cycle_condenser_v1")
    module = __import__("conventions.colored_four_cycle_condenser_v1", fromlist=["effective_codegree", "condenser_ledger"])
    codegree = module.effective_codegree((Fraction(1), Fraction(1)))
    row = module.condenser_ledger(
        atom_l2_mass=Fraction(3), off_pair_l2_mass=Fraction(8), maximum_effective_codegree=codegree,
        cutoff_mass_over_k=Fraction(1), kernel_schur_constant=Fraction(1),
    )
    require(codegree == 2, "effective codegree")
    require(row["fourth_moment_bound_over_k"] == 50, "diagonal plus off-diagonal ledger")
    require("not yet a phase-aligned" in theorem["colored_configuration"], "four-cycle boundary")
    return {
        "artifact_id": "cycle-160-colored-four-cycle-condenser-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_COEFFICIENT_WEIGHTED_OFF_DIAGONAL_CONDENSER_HIGH_CODEGREE_PAIR_CELL_OPEN",
        "claim_boundary": (
            "This artifact proves a coefficient-weighted off-diagonal fourth-moment condenser and conditional high-codegree pair-cell inverse. "
            "It does not prove Cycle-89 excess, a phase-aligned colored four-cycle, a fourth-moment estimate, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 160"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "colored_four_cycle_condenser": {"epistemic_status": "PROVED", **theorem},
        "sample": {"epistemic_status": "PROVED", "effective_codegree": str(codegree), **{key: str(value) for key, value in row.items()}},
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "turn a labelled high effective-codegree pair-difference cell into a phase-aligned colored four-cycle or rational web, "
                "or exhibit an admissible condenser falsifier"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_160_colored_four_cycle_condenser_v1.py --write",
            "check_command": "python3 proof/build_cycle_160_colored_four_cycle_condenser_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_160_colored_four_cycle_condenser_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 160 sealer", output=OUTPUT, payload_factory=seal))
