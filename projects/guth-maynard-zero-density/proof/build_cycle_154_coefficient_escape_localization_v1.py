#!/usr/bin/env python3
"""Seal Cycle 154 finite labelled coefficient-escape localization."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-154-coefficient-escape-localization-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-154-coefficient-transport-preregistration-v1.md", "ddc37e517a93fd34bb56b4dee8ebf8dc3825342df6db85076b4ba44fcaa7eac5"),
    "document": (ROOT / "docs/cycle-154-coefficient-escape-localization-v1.md", "8b872b4c38f065403fae90accb8f3ddde2041f6e870f27cc1b7a40b1e86172c8"),
    "conventions": (ROOT / "conventions/coefficient_escape_localization_v1.py", "c5790ac5ec34850415b64a1dbce79874c6e206f42018151f72b7cfb8b6181c91"),
    "tests": (ROOT / "tests/test_cycle_154_coefficient_escape_localization_v1.py", "b4268bd06b2b82c51bcb96229f1cd51d392713f8c68bc6b46f300351915d2cd5"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle153": (ROOT / "artifacts/cycle-153-actual-mass-routing-v1.json", "aed7046d0019dbf13178aee549da8abcec23bbb747b101a88b846ff56a6769e9"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle153"][0], "SEALED_ACTUAL_MASS_ROUTING_TO_STRICT_BRANCH_OR_LABELLED_ESCAPE")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="coefficient_escape_localization_v1")
    module = __import__("conventions.coefficient_escape_localization_v1", fromlist=["localized_escape"])
    row = module.localized_escape(
        total_negative_projection=Fraction(1),
        class_real_projections=(Fraction(-1, 10), Fraction(2, 5), Fraction(-9, 10)),
        witness_norm_squared_over_scale=Fraction(2),
    )
    require(row["class_count"] == 3, "finite partition count")
    require(row["chosen_class_negative_projection"] >= row["per_class_lower_bound"], "pigeonhole threshold")
    require(row["one_ray_l2_squared_over_scale_lower_bound"] == Fraction(1, 18), "Cauchy scale")
    require("does not prove" in theorem["boundary"], "claim boundary")
    return {
        "artifact_id": "cycle-154-coefficient-escape-localization-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_CONDITIONAL_FINITE_LABELLED_ESCAPE_LOCALIZATION",
        "claim_boundary": (
            "This artifact proves only the conditional finite labelled escape localization lemma. It does not "
            "establish an actual coefficient partition, a comb-norm majorant, positive transport, a bounded fan, "
            "a moment, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 154"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "finite_labelled_escape_localization": {"epistemic_status": "PROVED", **theorem},
        "sample": {"epistemic_status": "PROVED", **{key: str(value) for key, value in row.items()}},
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "derive or reject the actual finite coefficient-escape partition and fixed comb-norm majorant; "
                "then analyze the selected class or prove O_kappa(1) positive fixed-phase transport"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_154_coefficient_escape_localization_v1.py --write",
            "check_command": "python3 proof/build_cycle_154_coefficient_escape_localization_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_154_coefficient_escape_localization_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 154 sealer", output=OUTPUT, payload_factory=seal))
