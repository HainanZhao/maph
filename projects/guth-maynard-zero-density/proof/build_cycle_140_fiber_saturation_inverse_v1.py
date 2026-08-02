#!/usr/bin/env python3
"""Seal Cycle 140 multiplier-fiber saturation inverse."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-140-fiber-saturation-inverse-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-140-fiber-saturation-preregistration-v1.md", "1562d3dbe9eec857ffc4b51de30e4a8ae359d0c02d7b13b5a2023c441103f61b"),
    "document": (ROOT / "docs/cycle-140-fiber-saturation-inverse-v1.md", "940110fbb61981ce42cb0d665c492359c6a43f3d776c15d98a69709cbd818a7d"),
    "conventions": (ROOT / "conventions/fiber_saturation_inverse_v1.py", "7ff444ecb2eb460a467e85b75df6e3de4ffd8ad1dfd10298ffab9274a53b780a"),
    "tests": (ROOT / "tests/test_cycle_140_fiber_saturation_inverse_v1.py", "6d04e8d7aa30555eee3abe92454f97cb60387777e219407eea0abf8af2d7e87b"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle138": (ROOT / "artifacts/cycle-138-multiplier-fiber-height-v1.json", "d1eacac468da23239faa829ec6fb509dbba083dafbd2855ee55b84f8174029a6"),
    "cycle139": (ROOT / "artifacts/cycle-139-multiplier-curvature-v1.json", "7f78a648ef0126918ab4487c9947d84fc04c51bdd7fe459d9b04ef7ab55776ca"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle138"][0], "SEALED_ALL_EDGE_MULTIPLICITIES_TO_1_6_MINUS_MU_2_UPPER_FAREY_RANGE_OPEN")
    validate_prior(INPUTS["cycle139"][0], "SEALED_LOW_EDGE_CURVATURE_TO_17_90_MINUS_2MU_3_HIGH_EDGE_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="fiber_saturation_inverse_v1")
    module = __import__("conventions.fiber_saturation_inverse_v1", fromlist=["saturation_ledger"])
    tied = module.saturation_ledger(
        Fraction(16, 25), Fraction(0), Fraction(1, 5), Fraction(4, 5), Fraction(1, 20), Fraction(1, 15)
    )
    require(tied["slack_threshold"] == Fraction(1, 15), "registered slack threshold")
    require(tied["discretization_margin"] == 0, "threshold tie")
    require("J X^{-epsilon}" in theorem["divisor_seed"], "divisor-class seed")
    require("no theorem forces" in theorem["boundary"], "saturation boundary")
    return {
        "artifact_id": "cycle-140-fiber-saturation-inverse-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_HEIGHT_SLACK_CLOSED_DIVISOR_FIBER_SEED_RECURRENCE_OPEN",
        "claim_boundary": (
            "This artifact closes sufficiently large height slack and extracts a "
            "divisor-class seed from survivors. It does not force subpower slack "
            "and proves no recurrence, full paired norm, endpoint, moment, density, "
            "or prime intervals."
        ),
        "runtime": check_runtime("Cycle 140"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "fiber_saturation_theorem": {"epistemic_status": "PROVED", **theorem},
        "sample_threshold_ledger": {
            "epistemic_status": "PROVED",
            "xi": "16/25",
            "mu": "0",
            "rho": "1/5",
            "tau": "4/5",
            "edge": "1/20",
            "slack_threshold": str(tied["slack_threshold"]),
            "next_partial_quotient_floor": str(tied["next_partial_quotient_floor"]),
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "couple the common divisor class and signed tails across popular "
                "differences to force a Cycle-126 recurrence seed"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_140_fiber_saturation_inverse_v1.py --write",
            "check_command": "python3 proof/build_cycle_140_fiber_saturation_inverse_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_140_fiber_saturation_inverse_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 140 sealer", output=OUTPUT, payload_factory=seal))
