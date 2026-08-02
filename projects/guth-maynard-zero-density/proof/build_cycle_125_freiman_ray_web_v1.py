#!/usr/bin/env python3
"""Seal Cycle 125 high-multiplicity Freiman ray-web compiler."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-125-freiman-ray-web-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-125-freiman-ray-web-preregistration-v1.md", "42c6d46c0c72de27c9eeabf1aaa2eb2520397a5131d02d85379d2f3658d30fdf"),
    "document": (ROOT / "docs/cycle-125-freiman-ray-web-v1.md", "51823d9950a4f6d15a848b9d556589cd7524cfd8731730efafe873ccaeed8c43"),
    "conventions": (ROOT / "conventions/freiman_ray_web_v1.py", "b8693f7e1ef08f4bd63be075cb973c25a030151b056ab7b5c7fa37875245a368"),
    "tests": (ROOT / "tests/test_cycle_125_freiman_ray_web_v1.py", "7c74cef57d17f93a190dfdd9e2cb616397857c147e73ef8d99a7a38c352e70ea"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle92": (ROOT / "artifacts/cycle-92-collision-ray-inverse-v1.json", "e4d20db8df77672cd8622abd891b0bc97cbb0914c538e95682c19cf98e48f43e"),
    "cycle124": (ROOT / "artifacts/cycle-124-bilinear-self-duality-v1.json", "d057acb6807a58be37e42a5bb1869de62e33e873dd0aebdb6033aad6b2e1f2b8"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle92"][0], "SEALED_EQUAL_HEIGHT_ANALYTIC_BOUND_OR_INJECTIVE_RAY_WEB_TO_E16_OPEN")
    validate_prior(INPUTS["cycle124"][0], "SEALED_TENSOR_CAUCHY_NORM_SELF_DUAL_COLLISION_INVERSE_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="freiman_ray_web_v1")
    module = __import__("conventions.freiman_ray_web_v1", fromlist=["threshold_ledger"])
    left = module.threshold_ledger(Fraction(16, 25), Fraction(1, 10))
    require(left["high_multiplicity_threshold"] == Fraction(9, 100), "left threshold")
    require("M^4K>>Q^3" in theorem["integer_forcing"], "integer forcing")
    require("R^4/(2D-1)" in theorem["energy"], "energy lower bound")
    require("Freiman 2-homomorphism" in theorem["valuation_web"], "valuation web")
    require("does not give" in theorem["seed_gate"], "seed boundary")
    return {
        "artifact_id": "cycle-125-freiman-ray-web-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_HIGH_MULTIPLICITY_FREIMAN_WEB_LOW_MULTIPLICITY_SEED_GATE_OPEN",
        "claim_boundary": (
            "This artifact compiles high-multiplicity collision rays into an exact "
            "valuation-labelled Freiman web. It proves no low-multiplicity bound, "
            "seed realization, simple-root closure, complete moment, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 125"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "freiman_ray_web_theorem": {"epistemic_status": "PROVED", **theorem},
        "lower_endpoint_threshold": {
            "epistemic_status": "PROVED",
            "multiplicity_exponent": str(left["high_multiplicity_threshold"]),
            "condition": "strictly greater, with frozen constant buffer",
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "control the complementary low-multiplicity rays or extract a "
                "popular-difference anchored seed from the Freiman web"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_125_freiman_ray_web_v1.py --write",
            "check_command": "python3 proof/build_cycle_125_freiman_ray_web_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_125_freiman_ray_web_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 125 sealer", output=OUTPUT, payload_factory=seal))
