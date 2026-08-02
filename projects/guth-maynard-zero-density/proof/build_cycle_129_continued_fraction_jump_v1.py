#!/usr/bin/env python3
"""Seal Cycle 129 continued-fraction jump compiler."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-129-continued-fraction-jump-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-129-continued-fraction-jump-preregistration-v1.md", "46b0a6bc17fe235bd1aaafa5e86d1cea3f017bad1640073fa2508e398478edfe"),
    "document": (ROOT / "docs/cycle-129-continued-fraction-jump-v1.md", "e8fe7d790e9250d1c014c970193f97ec389554d884376c562f8f3def480bfebf"),
    "conventions": (ROOT / "conventions/continued_fraction_jump_v1.py", "7c5d853e13d0e7c74798337e155117eda6ab34ebdacb142db219c53e9f0c7765"),
    "tests": (ROOT / "tests/test_cycle_129_continued_fraction_jump_v1.py", "9f705afe8ed98d127a9cfe428ef71fd2aa590be78f1dc14416d1860ba2242ecf"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle92": (ROOT / "artifacts/cycle-92-collision-ray-inverse-v1.json", "e4d20db8df77672cd8622abd891b0bc97cbb0914c538e95682c19cf98e48f43e"),
    "cycle128": (ROOT / "artifacts/cycle-128-sampled-mellin-profiler-v1.json", "ade56d2370748ecc7e0365e7134f11ec6775840a799f4b3e280b7d7a3ef01136"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle92"][0], "SEALED_EQUAL_HEIGHT_ANALYTIC_BOUND_OR_INJECTIVE_RAY_WEB_TO_E16_OPEN")
    validate_prior(INPUTS["cycle128"][0], "SEALED_DISCOVERY_MELLIN_ALIASES_PRIMITIVE_CONVERGENT_MINOR_MAJOR_SPLIT_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="continued_fraction_jump_v1")
    module = __import__("conventions.continued_fraction_jump_v1", fromlist=["jump_ledger"])
    left = module.jump_ledger(Fraction(16, 25), Fraction(0))
    require(left["legendre_margin"] == Fraction(23, 75), "minimum margin")
    require("Legendre's criterion" in theorem["legendre"], "convergent compiler")
    require(">>KM" in theorem["next_denominator"], "next denominator")
    require(">>KM^2/Q" in theorem["partial_quotient"], "partial quotient")
    require("O((Q/M)X^epsilon)" in theorem["averaged_target"], "averaged target")
    require("no averaged" in theorem["boundary"], "claim boundary")
    return {
        "artifact_id": "cycle-129-continued-fraction-jump-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_COLLISIONS_FORCE_POWER_PARTIAL_QUOTIENT_AVERAGE_OPEN",
        "claim_boundary": (
            "This artifact proves that every collision forces a continued-"
            "fraction convergent and a fixed-power next partial quotient. It "
            "proves no averaged jump theorem, collision or simple-root closure, "
            "complete moment, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 129"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "continued_fraction_jump_theorem": {"epistemic_status": "PROVED", **theorem},
        "minimum_jump_margin": {
            "epistemic_status": "PROVED",
            "exponent": str(left["legendre_margin"]),
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "bound the number of exponential modes with a convergent followed "
                "by a partial quotient >>KM^2/Q, or classify their common structure"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_129_continued_fraction_jump_v1.py --write",
            "check_command": "python3 proof/build_cycle_129_continued_fraction_jump_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_129_continued_fraction_jump_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 129 sealer", output=OUTPUT, payload_factory=seal))
