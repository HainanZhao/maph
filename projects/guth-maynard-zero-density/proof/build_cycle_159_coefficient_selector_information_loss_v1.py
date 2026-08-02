#!/usr/bin/env python3
"""Seal Cycle 159 primitive-ray coefficient-selector information loss."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-159-coefficient-selector-information-loss-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-159-coefficient-selector-reconstruction-preregistration-v1.md", "98c303800cb4b338cd993ee9c11675c18a8560a87e06078358b30f0e54d78df1"),
    "document": (ROOT / "docs/cycle-159-coefficient-selector-information-loss-v1.md", "3d5d57cd0614d6cd3e35905718918d987663f84c9469d3afecb20c42f948c1ad"),
    "conventions": (ROOT / "conventions/coefficient_selector_information_loss_v1.py", "e0ff742263a72243f9929cab178b97b856d1671a58cdeb71c34b944a1dc61721"),
    "tests": (ROOT / "tests/test_cycle_159_coefficient_selector_information_loss_v1.py", "00ff48fc8f110dfa7331417fa599c0c5ce766cf3de0d40527d70db6a555ad32e"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle92": (ROOT / "artifacts/cycle-92-collision-ray-inverse-v1.json", "e4d20db8df77672cd8622abd891b0bc97cbb0914c538e95682c19cf98e48f43e"),
    "cycle124": (ROOT / "artifacts/cycle-124-bilinear-self-duality-v1.json", "d057acb6807a58be37e42a5bb1869de62e33e873dd0aebdb6033aad6b2e1f2b8"),
    "cycle144": (ROOT / "artifacts/cycle-144-actual-edge-coefficient-v1.json", "c8260b7152a02b9d2b61ee1f60340b79c4eea40542311c64057af88c7a5ebf3c"),
    "cycle157": (ROOT / "artifacts/cycle-157-selection-mask-negative-spectral-v1.json", "f76f0e349593ab3b8c327f7c140e8c4aa85b8e8f6156774549c90a6054280aed"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle92"][0], "SEALED_EQUAL_HEIGHT_ANALYTIC_BOUND_OR_INJECTIVE_RAY_WEB_TO_E16_OPEN")
    validate_prior(INPUTS["cycle124"][0], "SEALED_TENSOR_CAUCHY_NORM_SELF_DUAL_COLLISION_INVERSE_OPEN")
    validate_prior(INPUTS["cycle144"][0], "SEALED_COEFFICIENT_PRESERVING_WEIGHTED_COLLISION_INVERSE_OPEN")
    validate_prior(INPUTS["cycle157"][0], "SEALED_RAW_ZERO_DIAGONAL_GRAM_OBSTRUCTION_COEFFICIENT_NEGATIVE_SPECTRAL_ALIGNMENT_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="coefficient_selector_information_loss_v1")
    module = __import__("conventions.coefficient_selector_information_loss_v1", fromlist=["multiplier_loss_witness"])
    row = module.multiplier_loss_witness(
        numerator=3, denominator=2, first_multiplier=3, second_multiplier=4,
        first_oriented_product=Fraction(1), second_oriented_product=Fraction(2),
    )
    require(row["first_ordered_atoms"] != row["second_ordered_atoms"], "distinct coefficient atoms")
    require(row["first_oriented_product"] != row["second_oriented_product"], "nonreconstructible products")
    require("multiplier t" in theorem["minimal_missing_label"], "minimal multiplier repair")
    return {
        "artifact_id": "cycle-159-coefficient-selector-information-loss-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_PRIMITIVE_RAY_MULTIPLIER_INFORMATION_LOSS_COEFFICIENT_PRESERVING_SELECTOR_OPEN",
        "claim_boundary": (
            "This artifact proves a coefficient-interface information-loss theorem for nonconstant ray fibres with two admissible multipliers. "
            "It does not show target mass in such a fibre, construct the actual selector, prove spectral concentration, a moment, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 159"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "coefficient_selector_information_loss": {"epistemic_status": "PROVED", **theorem},
        "sample": {"epistemic_status": "PROVED", **{key: str(value) for key, value in row.items()}},
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "construct a multiplier-resolved coefficient-preserving collision measure with target mass, or timebox E14D-L and activate E14D-H"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_159_coefficient_selector_information_loss_v1.py --write",
            "check_command": "python3 proof/build_cycle_159_coefficient_selector_information_loss_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_159_coefficient_selector_information_loss_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 159 sealer", output=OUTPUT, payload_factory=seal))
