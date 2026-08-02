#!/usr/bin/env python3
"""Seal Cycle 152 bounded-multiplier divisor-fan inverse."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-152-bounded-multiplier-divisor-fan-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-152-bounded-multiplier-divisor-fan-preregistration-v1.md", "4f603efdbdc7f8eec7bb7d26f4b9914a33e5d1c851ae6d8320c7728b7dfbd82a"),
    "document": (ROOT / "docs/cycle-152-bounded-multiplier-divisor-fan-v1.md", "bbd46f328a97d27fe6589e5a396a8312957b3ff3e244def9f021494bcb4d42b3"),
    "conventions": (ROOT / "conventions/bounded_multiplier_divisor_fan_v1.py", "48985ab3ab77bb8fd6c4fa0c4b2e3c05b426871dbc7127a42bb6485993ae51ba"),
    "tests": (ROOT / "tests/test_cycle_152_bounded_multiplier_divisor_fan_v1.py", "282a9caff8e074cc42ac7200657821a0c651f93f05e31cd0d67e4f153a5b60bd"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle151": (ROOT / "artifacts/cycle-151-sampled-comb-double-poisson-v1.json", "9a7cff91d70b5d7d9da91f7f718fd0e8ee68808b81f8e3ee89d9d5ecdda6245c"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle151"][0], "SEALED_GCD_WEIGHTED_NEGATIVE_TAIL_LOBE_OR_BOUNDARY_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="bounded_multiplier_divisor_fan_v1")
    module = __import__("conventions.bounded_multiplier_divisor_fan_v1", fromlist=["bounded_multiplier_inverse", "divisor_fan_row"])
    compiler = module.bounded_multiplier_inverse(
        contribution_bound=Fraction(2),
        target_mass=Fraction(1),
        rows=[(Fraction(1, 2), 1, Fraction(1)), (Fraction(1, 2), 2, Fraction(1, 2))],
    )
    fan = module.divisor_fan_row(witness_denominator=60, multiplier=4, divisor=20)
    require(compiler["multiplier_cap"] == 4, "bounded multiplier cap")
    require(compiler["chosen_multiplier_mass"] >= compiler["chosen_multiplier_lower_bound"], "pigeonhole mass")
    require(fan["mode_denominator"] == 80 and fan["gcd"] == 20, "exact divisor fan")
    require("conditional" in theorem["boundary"], "inverse claim boundary")
    return {
        "artifact_id": "cycle-152-bounded-multiplier-divisor-fan-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_BOUNDED_MULTIPLIER_DIVISOR_FAN_TAIL_INCIDENCE_OR_FAN_ANALYSIS_OPEN",
        "claim_boundary": (
            "This artifact proves a conditional bounded-multiplier divisor-fan inverse for the "
            "licensed smooth strict halo. It does not bound or exclude that fan, treat boundary "
            "denominators or other escape classes, or prove a full moment, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 152"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "bounded_multiplier_divisor_fan_theorem": {"epistemic_status": "PROVED", **theorem},
        "sample_compiler": {"epistemic_status": "PROVED", **{key: str(value) for key, value in compiler.items()}},
        "sample_fan_row": {"epistemic_status": "PROVED", **fan},
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "bound the labelled bounded-multiplier negative-tail divisor fan by spacing or "
                "order-three curvature, or classify a surviving fan with its actual coefficient and tail labels"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_152_bounded_multiplier_divisor_fan_v1.py --write",
            "check_command": "python3 proof/build_cycle_152_bounded_multiplier_divisor_fan_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_152_bounded_multiplier_divisor_fan_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 152 sealer", output=OUTPUT, payload_factory=seal))
