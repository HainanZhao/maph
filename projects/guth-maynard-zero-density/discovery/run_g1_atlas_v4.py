#!/usr/bin/env python3
"""Fresh-production wrapper for two-run empirical reconciliation at G1.

Every v4 production starts from a nonexistent checkpoint and emits an
``UNVERIFIED_PENDING_SECOND_FRESH_RUN`` observation artifact.  No resume or
cached assembly mode exists here.  A separate adjudicator is the only program
authorized to emit an empirical-reconciliation artifact after two complete,
byte-identical timing-independent observations.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from discovery import run_g1_atlas_v3 as v3  # noqa: E402


V3_ENGINE = ROOT / "discovery/run_g1_atlas_v3.py"
V3_ENGINE_SHA256 = "921f25ae3f6d535899b439b04f310bc91b4278046976b7ad7947c04b6166f06f"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def driver_identity() -> dict[str, str]:
    return {"path": str(Path(__file__).relative_to(ROOT)), "sha256": sha256(Path(__file__))}


def check_runtime() -> dict[str, Any]:
    require(sha256(V3_ENGINE) == V3_ENGINE_SHA256, "G1 v3 engine hash mismatch")
    return v3.check_runtime()


def prepare_fresh_checkpoint(path: Path, run_label: str) -> None:
    runtime = check_runtime()
    require(not path.exists(), "v4 production checkpoint must be a new path")
    checkpoint = v3.v2.new_checkpoint(runtime)
    checkpoint["driver_v3"] = v3.driver_identity()
    checkpoint["driver_v4"] = driver_identity()
    checkpoint["production_origin_v4"] = {
        "run_label": run_label,
        "started_from_empty_checkpoint": True,
        "resume_allowed": False,
        "promotion_status": "UNVERIFIED_PENDING_SECOND_FRESH_RUN",
    }
    v3.v2.atomic_replace(path, checkpoint)


def decorate_observations(observations_v3: dict[str, Any]) -> dict[str, Any]:
    observations = json.loads(json.dumps(observations_v3))
    observations["artifact_id"] = "cycle-3-g1-atlas-observations-v4"
    observations["correction"]["engine_v4_sha256"] = sha256(Path(__file__))
    observations["correction"]["engine_v3_sha256"] = V3_ENGINE_SHA256
    observations["promotion_boundary"] = {
        "epistemic_status": "OBSERVED",
        "status": "UNVERIFIED_PENDING_SECOND_FRESH_RUN",
        "promotion_allowed": False,
        "required_evidence": "A separate adjudicator must reconcile two fresh, complete, distinct-checkpoint v4 executions with byte-identical timing-independent observations.",
        "cached_assembly_is_not_promotion_evidence": True,
    }
    return observations


def decorate_performance(performance_v3: dict[str, Any]) -> dict[str, Any]:
    performance = json.loads(json.dumps(performance_v3))
    performance["artifact_id"] = "cycle-3-g1-atlas-performance-v4"
    performance["engine_v4_sha256"] = sha256(Path(__file__))
    performance["engine_v3_sha256"] = V3_ENGINE_SHA256
    return performance


def run_fresh(checkpoint_path: Path, observations_path: Path, performance_path: Path, run_label: str) -> None:
    require(run_label in {"A", "B"}, "v4 run label must be A or B")
    require(not observations_path.exists(), "v4 observations path must be new")
    require(not performance_path.exists(), "v4 performance path must be new")
    prepare_fresh_checkpoint(checkpoint_path, run_label)
    observations_v2, performance_v2, checkpoint = v3.v2.run_or_resume(checkpoint_path, resume=True)
    observations = decorate_observations(v3.decorate_observations(observations_v2))
    performance = decorate_performance(v3.decorate_performance(performance_v2))
    v3.v2.atomic_write_or_verify(performance_path, performance)
    v3.v2.atomic_write_or_verify(observations_path, observations)
    checkpoint["phase"] = "COMPLETE"
    checkpoint["fresh_full_completion_v4"] = {
        "status": "COMPLETE_UNVERIFIED",
        "run_label": run_label,
        "observations": str(observations_path),
        "observations_sha256": hashlib.sha256(v3.v2.json_bytes(observations)).hexdigest(),
        "performance": str(performance_path),
        "performance_sha256": hashlib.sha256(v3.v2.json_bytes(performance)).hexdigest(),
        "driver_v4_sha256": sha256(Path(__file__)),
    }
    v3.v2.atomic_replace(checkpoint_path, checkpoint)


def integrity_report() -> dict[str, Any]:
    runtime = check_runtime()
    return {
        "epistemic_status": "OBSERVED",
        "claim_boundary": "Promotion-boundary integrity only; no finite screen row evaluated.",
        "engine_v4_sha256": sha256(Path(__file__)),
        "engine_v3_sha256": V3_ENGINE_SHA256,
        "runtime": runtime,
        "production_mode": "fresh checkpoint only; no resume",
        "per_run_status": "UNVERIFIED_PENDING_SECOND_FRESH_RUN",
        "promotion_gate": "separate two-fresh-run empirical adjudicator",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check-integrity", action="store_true")
    action.add_argument("--run-fresh", action="store_true")
    parser.add_argument("--run-label", choices=("A", "B"))
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--observations", type=Path)
    parser.add_argument("--performance", type=Path)
    args = parser.parse_args()
    if args.check_integrity:
        require(args.run_label is None and args.checkpoint is None and args.observations is None and args.performance is None, "integrity check accepts no run arguments")
        print(json.dumps(integrity_report(), sort_keys=True))
        return 0
    require(args.run_label is not None and args.checkpoint is not None and args.observations is not None and args.performance is not None, "fresh run requires label, checkpoint, observations, and performance paths")
    run_fresh(args.checkpoint, args.observations, args.performance, args.run_label)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
