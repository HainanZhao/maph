#!/usr/bin/env python3
"""Seal Cycle 118 derivative-resolved simple-root profiler."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-118-simple-root-profiler-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-118-simple-root-profiler-preregistration-v1.md", "1fb10578f3b86b6860907e40b29a73ce14bd6f0a9cb6a61e070ce1a21ea45de2"),
    "document": (ROOT / "docs/cycle-118-simple-root-profiler-v1.md", "3dec0b18b4c1e0814b98c78bfebe658c8cd188eb73e433c3bc011a336194afb6"),
    "discovery_script": (ROOT / "discovery/run_cycle_118_simple_root_profiler_v1.py", "82f27e9b62973f0f33bcde085eb81c7db6044061b2c2442467f3810c2e82baf9"),
    "discovery_output": (ROOT / "discovery/cycle-118-simple-root-profiler-v1.json", "f4772a297acc8b15dd3f117b819cb5e4210fa3a79ef4873f052eb10ea3e1a1d6"),
    "tests": (ROOT / "tests/test_cycle_118_simple_root_profiler_v1.py", "9b9514be1ee03e99b3b64f76341eec5fc7b2706bae48333e9b078fa21342ee8a"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle97": (ROOT / "artifacts/cycle-97-projective-algebraic-root-v1.json", "5af4394e8a8f48b70cff4f1b32e9a213640df499f273f701bc0ffe5ffd0d2644"),
    "cycle117": (ROOT / "artifacts/cycle-117-weighted-weak-sector-v1.json", "2594773d6768fd46aa46da2e424cb2c06ab49fada984fd9b3c7315ff521b56ea"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle97"][0], "SEALED_ALGEBRAIC_ROOT_OR_NEAR_DOUBLE_INVERSE_EFFECTIVE_SEPARATION_OPEN")
    validate_prior(INPUTS["cycle117"][0], "SEALED_SMOOTH_WEAK_SECTOR_X59_150_SIMPLE_ROOT_OPEN")
    profiler = json.loads(INPUTS["discovery_output"][0].read_text(encoding="utf-8"))
    require([row["simple"] for row in profiler["rows"]] == [3461, 7400, 16128], "simple counts")
    require(profiler["rows"][-1]["signatures"]["J0_NONZERO/J1_NONZERO/OPPOSITE"] == 9184, "opposite signature")
    return {
        "artifact_id": "cycle-118-simple-root-profiler-v1",
        "epistemic_status": "OBSERVED",
        "status": "SEALED_DISCOVERY_SIMPLE_ROOT_JET_COLLAPSE_FALSIFIED_DISCREPANCY_ENGINE_OPEN",
        "claim_boundary": (
            "This artifact records a reproducible floating profiler which falsifies jet-collapse "
            "on the frozen grid. It proves no asymptotic simple-root count."
        ),
        "runtime": check_runtime("Cycle 118"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "profiler": profiler,
        "finding": {
            "epistemic_status": "OBSERVED",
            "statement": "dominant simple rows have J0 and J1 both nonzero in both sign sectors",
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "prove a derivative-weighted discrepancy/covering theorem for the sparse exponential surface",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_118_simple_root_profiler_v1.py --write",
            "check_command": "python3 proof/build_cycle_118_simple_root_profiler_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_118_simple_root_profiler_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 118 sealer", output=OUTPUT, payload_factory=seal))
