#!/usr/bin/env python3
"""Seal Cycle 141 divisor-seed recurrence compiler."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-141-divisor-seed-recurrence-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-141-divisor-seed-recurrence-preregistration-v1.md", "1af93560528884cbb9b304a37dcc47a433de5d579af5ff9806d01f41ab937aca"),
    "document": (ROOT / "docs/cycle-141-divisor-seed-recurrence-v1.md", "bf5acfda464d555cba7199dc5a1d72dc2b5eb8487cc3f1d95d1e4c3c142c2f1a"),
    "conventions": (ROOT / "conventions/divisor_seed_recurrence_v1.py", "d9d8e2e1c6173db12a26be8cc199d95403487c3a899a7e6dbd4b8a1e9098ba7a"),
    "tests": (ROOT / "tests/test_cycle_141_divisor_seed_recurrence_v1.py", "cbe56126e8f533958fc39ebb740798807893fecec98e4a37fb86c1b3a1ef3f10"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle126": (ROOT / "artifacts/cycle-126-freiman-recurrence-v1.json", "c228988b1549f129522a68f5b10698768ae3581b367166a9253048b67aeb92e5"),
    "cycle140": (ROOT / "artifacts/cycle-140-fiber-saturation-inverse-v1.json", "a02aa56b0a79c95baff74e0088b08caaf5ad4d9c5e956eec4dd1da62c140f5d8"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle126"][0], "SEALED_COMMON_RATIONAL_MULTIPLIER_CHAIN_DEPTH_ANCHOR_OPEN")
    validate_prior(INPUTS["cycle140"][0], "SEALED_HEIGHT_SLACK_CLOSED_DIVISOR_FIBER_SEED_RECURRENCE_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="divisor_seed_recurrence_v1")
    module = __import__("conventions.divisor_seed_recurrence_v1", fromlist=["continuation_ledger"])
    sample = module.continuation_ledger(100, 75, 3)
    require(sample["longest_chain_edges"] == 3, "path-forest chain bound")
    require(sample["length_two_starts"] == 50, "continuation count")
    require("at most one edge" in theorem["unimodular_no_go"], "transition no-go")
    require("must not be used" in theorem["replacement_invariant"], "replacement invariant")
    return {
        "artifact_id": "cycle-141-divisor-seed-recurrence-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_TRANSITION_REPETITION_IMPOSSIBLE_CONTINUATION_PROFILE_OPEN",
        "claim_boundary": (
            "This artifact excludes repeated GL_2(Z) transitions as the recurrence "
            "mechanism and identifies class-colored continuation density as the "
            "replacement invariant. It proves no positive continuation density, "
            "recurrence, full paired norm, endpoint, moment, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 141"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "divisor_seed_recurrence_theorem": {"epistemic_status": "PROVED", **theorem},
        "sample_continuation_ledger": {
            "epistemic_status": "PROVED",
            "vertices": 100,
            "colored_edges": 75,
            "depth": 3,
            **sample,
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "prove or invert class-colored continuation intersections while "
                "retaining signed tails and the original packet anchor"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_141_divisor_seed_recurrence_v1.py --write",
            "check_command": "python3 proof/build_cycle_141_divisor_seed_recurrence_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_141_divisor_seed_recurrence_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 141 sealer", output=OUTPUT, payload_factory=seal))
