#!/usr/bin/env python3
"""Seal Cycle 161's phase-aligned four-cycle or labelled-star dichotomy."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-161-high-cell-refinement-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-161-high-cell-refinement-preregistration-v1.md", "04d9e001cbd48aab66e8e99260ad4974c0e2ad39f2fb6f4660016ce1c5c8e510"),
    "document": (ROOT / "docs/cycle-161-high-cell-refinement-v1.md", "70cd0f7190475addc97f6021843c03cc6b2c725f2ffbf951213c26deebafff07"),
    "conventions": (ROOT / "conventions/high_cell_refinement_v1.py", "aa004bb414f573bb42e7a60a33f40f4f83ab56513d962f2d6034be05b6454983"),
    "tests": (ROOT / "tests/test_cycle_161_high_cell_refinement_v1.py", "c5b4c0afdc1aa88aa99ab80fb3c3e58ee8a6ae618c975ee6743a9092143e10d6"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle160": (ROOT / "artifacts/cycle-160-colored-four-cycle-condenser-v1.json", "4a24ed36bc62ef718d33cf1bb5ac3eeaf744f45bbb29d94ee0670313dbcbe83b"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle160"][0], "SEALED_COEFFICIENT_WEIGHTED_OFF_DIAGONAL_CONDENSER_HIGH_CODEGREE_PAIR_CELL_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="high_cell_refinement_v1")
    module = __import__(
        "conventions.high_cell_refinement_v1",
        fromlist=["disjoint_pair_mass_lower_bound", "hub_effective_neighbor_lower_bound", "refined_class_witness"],
    )
    refinement = module.refined_class_witness(((Fraction(1), Fraction(1)), (Fraction(1), Fraction(1))))
    disjoint = module.disjoint_pair_mass_lower_bound(Fraction(5), Fraction(1))
    hub = module.hub_effective_neighbor_lower_bound(hub_incidence=Fraction(3), total_square_mass=Fraction(8))
    require(refinement["best_refined_effective_multiplicity"] >= refinement["retained_lower_bound"], "refinement retention")
    require(disjoint == 15, "disjoint-pair lower ledger")
    require(hub == Fraction(9, 8), "hub effective-neighbor ledger")
    require("does not prove" in theorem["boundary"], "claim boundary")
    return {
        "artifact_id": "cycle-161-high-cell-refinement-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_PHASE_ALIGNED_FOUR_CYCLE_OR_LABELLED_STAR_DEGENERACY_BANKED",
        "claim_boundary": (
            "This artifact conditionally refines a Cycle-160 high effective-codegree cell into coefficient-weighted positive-real four-distinct-atom mass or a labelled effective-degree star. "
            "It does not prove Cycle-89 excess, a rational web, a transport seed, a fourth-moment estimate, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 161"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "high_cell_refinement": {"epistemic_status": "PROVED", **theorem},
        "sample": {
            "epistemic_status": "PROVED",
            "refinement": {key: str(value) for key, value in refinement.items()},
            "disjoint_pair_mass_lower_bound": str(disjoint),
            "hub_effective_neighbor_lower_bound": str(hub),
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "compile the actual labelled positive-real four-cycle population to a moment gain, or classify the labelled star as a rational web or admissible obstruction"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_161_high_cell_refinement_v1.py --write",
            "check_command": "python3 proof/build_cycle_161_high_cell_refinement_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_161_high_cell_refinement_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 161 sealer", output=OUTPUT, payload_factory=seal))
