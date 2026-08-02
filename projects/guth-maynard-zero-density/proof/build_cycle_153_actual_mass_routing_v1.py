#!/usr/bin/env python3
"""Seal Cycle 153 actual negative-mass routing compiler."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-153-actual-mass-routing-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-153-actual-mass-routing-preregistration-v1.md", "a15f414c3c2702b36578880c8c4e848a0be6bb2b86500a046dc0de9f2bcd72cb"),
    "document": (ROOT / "docs/cycle-153-actual-mass-routing-v1.md", "cc450221b115a6915de9fab7de3a67842944f79db1243447bb70e0aeb6be1694"),
    "conventions": (ROOT / "conventions/actual_mass_routing_v1.py", "a0b61b0db798eacb4e3e0c97203e088706b05ac60194daa4eacb6089c3e5094c"),
    "tests": (ROOT / "tests/test_cycle_153_actual_mass_routing_v1.py", "798c265722b306d54ad2240052800b2c741738b861f94a528a2e531dcca334e2"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle152_correction": (ROOT / "artifacts/cycle-152-bounded-multiplier-divisor-fan-v1-scope-correction.json", "fb602a39858838f62eee16e119747a7922baf6cf054129c1777a021a122ee2f8"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle152_correction"][0], "SEALED_CONDITIONAL_BOUNDED_MULTIPLIER_DIVISOR_FAN_INVERSE")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="actual_mass_routing_v1")
    module = __import__("conventions.actual_mass_routing_v1", fromlist=["routing_dichotomy", "validate_partition"])
    strict = module.routing_dichotomy(
        post_error_negative_mass=Fraction(1), strict_real_correlations=[Fraction(-3, 5), Fraction(1, 7)]
    )
    escape = module.routing_dichotomy(
        post_error_negative_mass=Fraction(1), strict_real_correlations=[Fraction(-1, 3), Fraction(1, 9)]
    )
    module.validate_partition(
        strict_ids=["s1", "s2"],
        escape_rows=[("e1", "boundary_denominator"), ("e2", "unbounded_tau")],
    )
    require(strict["route"] == "STRICT_LABELLED_MASS", "strict route")
    require(escape["route"] == "LABELLED_ESCAPE_OBLIGATION", "escape route")
    require(escape["escape_correlation_lower_bound"] >= escape["threshold"], "escape threshold")
    require("Cycle 152" in theorem["cycle152_interface"], "Cycle 152 interface")
    return {
        "artifact_id": "cycle-153-actual-mass-routing-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_ACTUAL_MASS_ROUTING_TO_STRICT_BRANCH_OR_LABELLED_ESCAPE",
        "claim_boundary": (
            "This artifact proves an exact post-error mass-routing dichotomy. It does not prove the strict "
            "branch's weight normalization or uniform per-mode bound, bound either routed class, or prove a "
            "full moment, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 153"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "actual_mass_routing_theorem": {"epistemic_status": "PROVED", **theorem},
        "sample_strict_route": {"epistemic_status": "PROVED", **{key: str(value) for key, value in strict.items()}},
        "sample_escape_route": {"epistemic_status": "PROVED", **{key: str(value) for key, value in escape.items()}},
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "prove the actual strict branch has normalized positive weights and a uniform complete per-mode "
                "bound so Cycle 152 yields an actual bounded-multiplier fan, or analyze the quantitative labelled escape obligation"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_153_actual_mass_routing_v1.py --write",
            "check_command": "python3 proof/build_cycle_153_actual_mass_routing_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_153_actual_mass_routing_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 153 sealer", output=OUTPUT, payload_factory=seal))
