#!/usr/bin/env python3
"""Seal Cycle 128 sampled-Mellin discovery profiler."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-128-sampled-mellin-profiler-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-128-sampled-mellin-profiler-preregistration-v1.md", "b29205c2e6a9c4dc29df1a874bcc6a520512f0482f0c0bd5c232bd0643c4ee80"),
    "document": (ROOT / "docs/cycle-128-sampled-mellin-profiler-v1.md", "3f94acb22b792c34f95faa8e689aab904f69644b1cd5a7067cf2d413edde8473"),
    "discovery_script": (ROOT / "discovery/run_cycle_128_sampled_mellin_profiler_v1.py", "121f1a239fe0a0919ce70eca18a4334cad082870084ec42602c8797ae963cfbf"),
    "discovery_output": (ROOT / "discovery/cycle-128-sampled-mellin-profiler-v1.json", "5aaf8f962329d29fd395bf358b40655c132790e31246c4d2415c63549f11aa34"),
    "tests": (ROOT / "tests/test_cycle_128_sampled_mellin_profiler_v1.py", "72b660b864421d992ba3b36ed67b9e4aabac808b7777cba6b786d8ee651898c1"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle127": (ROOT / "artifacts/cycle-127-low-multiplicity-log-saddle-v1.json", "0dc33bc38ac1e3edf85b98abeffcdcf162fe6c6f6f335c3cc0f9bf268d78955a"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle127"][0], "SEALED_LOW_MULTIPLICITY_VOLUME_MARGIN_MELLIN_DIAGONAL_OPEN")
    profiler = json.loads(INPUTS["discovery_output"][0].read_text(encoding="utf-8"))
    rows = profiler["rows"]
    radius_one = [row for row in rows if row["radius"] == 1]
    radius_four = [row for row in rows if row["radius"] == 4]
    require(len(rows) == 18, "frozen row count")
    require(sum(row["total_hits"] for row in radius_one) == 16, "radius-one hits")
    require(sum(row["total_hits"] for row in radius_four) == 48, "radius-four hits")
    require(max(row["max_ray_multiplicity"] for row in rows) == 1, "ray multiplicity")
    require(sum(row["nonconvergent_rays"] for row in rows) == 0, "continued-fraction rows")
    require(sum(row["rays_above_cycle125_threshold"] for row in rows) == 0, "high branch")
    return {
        "artifact_id": "cycle-128-sampled-mellin-profiler-v1",
        "epistemic_status": "OBSERVED",
        "status": "SEALED_DISCOVERY_MELLIN_ALIASES_PRIMITIVE_CONVERGENT_MINOR_MAJOR_SPLIT_OPEN",
        "claim_boundary": (
            "This artifact records a finite 80-decimal profiler. It proves no "
            "asymptotic sparsity, continued-fraction classification, sampled-"
            "Mellin estimate, collision bound, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 128"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "profiler": profiler,
        "finding": {
            "epistemic_status": "OBSERVED",
            "statement": (
                "all frozen aliases have ray multiplicity one and are continued-"
                "fraction convergents; every grid remains below target Q"
            ),
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "prove a convergent-minor-arc count with the Freiman compiler as "
                "the structured high-multiplicity output"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "discovery_command": "python3 discovery/run_cycle_128_sampled_mellin_profiler_v1.py",
            "check_command": "python3 proof/build_cycle_128_sampled_mellin_profiler_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_128_sampled_mellin_profiler_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 128 sealer", output=OUTPUT, payload_factory=seal))
