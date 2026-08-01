#!/usr/bin/env python3
"""Replay-boundary correction for the frozen Cycle-3 G1 finite atlas.

V3 preserves the v2 row engine byte-for-byte and separates three operations:

* a resumable production run;
* read-only assembly verification from an already sealed checkpoint; and
* a true full replay that must start from a new, explicit checkpoint.

No mode silently promotes cached rows to an independent replay.
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

from discovery import run_g1_atlas_v2 as v2  # noqa: E402


V2_ENGINE = ROOT / "discovery/run_g1_atlas_v2.py"
V2_ENGINE_SHA256 = "62d3b565f4b80f7a7d17d19e779eec5107a1b2df11990cb30db1dc1d07830941"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def check_runtime() -> dict[str, Any]:
    require(sha256(V2_ENGINE) == V2_ENGINE_SHA256, "G1 v2 row-engine hash mismatch")
    return v2.check_runtime()


def decorate_observations(observations: dict[str, Any]) -> dict[str, Any]:
    observations = json.loads(json.dumps(observations))
    observations["artifact_id"] = "cycle-3-g1-atlas-observations-v3"
    observations["correction"]["engine_v3_sha256"] = sha256(Path(__file__))
    observations["correction"]["engine_v2_row_core_sha256"] = V2_ENGINE_SHA256
    observations["correction"]["replay_boundary"] = (
        "Sealed-checkpoint assembly verification is read-only and explicitly "
        "not a replay; full replay requires a fresh explicit checkpoint."
    )
    return observations


def decorate_performance(performance: dict[str, Any]) -> dict[str, Any]:
    performance = json.loads(json.dumps(performance))
    performance["artifact_id"] = "cycle-3-g1-atlas-performance-v3"
    performance["engine_v3_sha256"] = sha256(Path(__file__))
    performance["engine_v2_row_core_sha256"] = V2_ENGINE_SHA256
    return performance


def expected_validation_plan(checkpoint: dict[str, Any]) -> list[tuple[str, int]]:
    return [
        (row_id, scale)
        for row_id in checkpoint["selected_screen_row_ids"]
        for scale in v2.base.VALIDATION_SCALES
    ]


def validate_sealed_checkpoint(checkpoint: dict[str, Any]) -> None:
    require(checkpoint["phase"] == "COMPLETE", "read-only assembly verification requires a COMPLETE checkpoint")
    require(len(checkpoint["screen_rows"]) == 588, "sealed checkpoint does not contain all 588 screen rows")
    selected = v2.base.retention_selection(checkpoint["screen_rows"])
    require(selected == checkpoint["selected_screen_row_ids"], "sealed checkpoint retained set mismatch")
    plan = expected_validation_plan(checkpoint)
    require(len(checkpoint["validation_rows"]) == len(plan), "sealed checkpoint validation coverage mismatch")
    for row, (row_id, scale) in zip(checkpoint["validation_rows"], plan):
        require(row.get("validation_of") == row_id, "sealed checkpoint validation row mismatch")
        require(row.get("validation_scale") == f"2^{scale.bit_length() - 1}", "sealed checkpoint validation scale mismatch")


def assemble_v3(checkpoint: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    return (
        decorate_observations(v2.assemble_observations(checkpoint)),
        decorate_performance(v2.assemble_performance(checkpoint)),
    )


def driver_identity() -> dict[str, str]:
    return {"path": str(Path(__file__).relative_to(ROOT)), "sha256": sha256(Path(__file__))}


def prepare_v3_checkpoint(checkpoint_path: Path, *, resume: bool) -> None:
    """Bind every persisted row checkpoint to this exact v3 driver."""
    runtime = check_runtime()
    if resume:
        require(checkpoint_path.is_file(), "--resume requires an existing checkpoint")
        checkpoint = v2.load_checkpoint(checkpoint_path, runtime)
        require(checkpoint.get("driver_v3") == driver_identity(), "G1 checkpoint v3 driver identity mismatch")
        return
    require(not checkpoint_path.exists(), "fresh production/replay checkpoint path already exists")
    checkpoint = v2.new_checkpoint(runtime)
    checkpoint["driver_v3"] = driver_identity()
    v2.atomic_replace(checkpoint_path, checkpoint)


def mark_complete(checkpoint_path: Path, checkpoint: dict[str, Any], observations_path: Path, performance_path: Path, observations: dict[str, Any], performance: dict[str, Any]) -> None:
    checkpoint["phase"] = "COMPLETE"
    checkpoint["final_artifacts_v3"] = {
        "observations": str(observations_path),
        "observations_sha256": hashlib.sha256(v2.json_bytes(observations)).hexdigest(),
        "performance": str(performance_path),
        "performance_sha256": hashlib.sha256(v2.json_bytes(performance)).hexdigest(),
        "engine_v3_sha256": sha256(Path(__file__)),
    }
    v2.atomic_replace(checkpoint_path, checkpoint)


def production_run(checkpoint_path: Path, observations_path: Path, performance_path: Path, *, resume: bool) -> None:
    prepare_v3_checkpoint(checkpoint_path, resume=resume)
    observations_v2, performance_v2, checkpoint = v2.run_or_resume(checkpoint_path, resume=True)
    observations = decorate_observations(observations_v2)
    performance = decorate_performance(performance_v2)
    # As in v2, performance commits first; observations is the final commit
    # marker. Existing byte-identical files are accepted for crash recovery.
    v2.atomic_write_or_verify(performance_path, performance)
    v2.atomic_write_or_verify(observations_path, observations)
    mark_complete(checkpoint_path, checkpoint, observations_path, performance_path, observations, performance)


def verify_sealed_assembly(checkpoint_path: Path, observations_path: Path, performance_path: Path | None) -> None:
    """Read cached rows, verify assembly bytes, and prove checkpoint immutability."""
    runtime = check_runtime()
    require(checkpoint_path.is_file(), "sealed checkpoint is absent")
    before_hash = sha256(checkpoint_path)
    checkpoint = v2.load_checkpoint(checkpoint_path, runtime)
    require(checkpoint.get("driver_v3") == driver_identity(), "sealed checkpoint v3 driver identity mismatch")
    validate_sealed_checkpoint(checkpoint)
    observations, performance = assemble_v3(checkpoint)
    require(observations_path.is_file(), "observations assembly target is absent")
    require(observations_path.read_bytes() == v2.json_bytes(observations), "sealed-checkpoint observations assembly mismatch")
    if performance_path is not None:
        require(performance_path.is_file(), "performance assembly target is absent")
        require(performance_path.read_bytes() == v2.json_bytes(performance), "sealed-checkpoint performance assembly mismatch")
    require(sha256(checkpoint_path) == before_hash, "read-only assembly verification mutated the sealed checkpoint")


def full_replay_fresh(checkpoint_path: Path, observations_target: Path) -> None:
    """Recompute every scheduled row into a new checkpoint, never cached rows."""
    require(not checkpoint_path.exists(), "full replay checkpoint must be a new path")
    prepare_v3_checkpoint(checkpoint_path, resume=False)
    observations_v2, _performance_v2, checkpoint = v2.run_or_resume(checkpoint_path, resume=True)
    observations = decorate_observations(observations_v2)
    require(observations_target.is_file(), "full replay observations target is absent")
    require(observations_target.read_bytes() == v2.json_bytes(observations), "fresh full replay observations mismatch")
    checkpoint["phase"] = "COMPLETE"
    checkpoint["fresh_full_replay"] = {
        "epistemic_status": "OBSERVED",
        "status": "MATCH",
        "target": str(observations_target),
        "target_sha256": hashlib.sha256(v2.json_bytes(observations)).hexdigest(),
        "claim_boundary": "Deterministic full recomputation agreement; not an independent mathematical route.",
    }
    v2.atomic_replace(checkpoint_path, checkpoint)


def integrity_report() -> dict[str, Any]:
    runtime = check_runtime()
    return {
        "epistemic_status": "OBSERVED",
        "claim_boundary": "Operational replay-boundary integrity only; no finite screen row evaluated.",
        "engine_v3_sha256": sha256(Path(__file__)),
        "engine_v2_row_core_sha256": V2_ENGINE_SHA256,
        "runtime": runtime,
        "production": "resumable explicit checkpoint",
        "assembly_verification": "read-only sealed checkpoint; cached rows; explicitly not replay",
        "full_replay": "fresh explicit checkpoint; recomputes all scheduled rows",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check-integrity", action="store_true")
    action.add_argument("--run-full", action="store_true")
    action.add_argument("--verify-sealed-assembly", action="store_true")
    action.add_argument("--full-replay-fresh", action="store_true")
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--observations", type=Path)
    parser.add_argument("--performance", type=Path)
    args = parser.parse_args()
    if args.check_integrity:
        require(args.checkpoint is None and not args.resume and args.observations is None and args.performance is None, "integrity check accepts no run arguments")
        print(json.dumps(integrity_report(), sort_keys=True))
        return 0
    require(args.checkpoint is not None and args.observations is not None, "selected mode requires --checkpoint and --observations")
    if args.run_full:
        require(args.performance is not None, "production run requires --performance")
        production_run(args.checkpoint, args.observations, args.performance, resume=args.resume)
    elif args.verify_sealed_assembly:
        require(not args.resume, "read-only assembly verification does not accept --resume")
        verify_sealed_assembly(args.checkpoint, args.observations, args.performance)
    else:
        require(not args.resume and args.performance is None, "fresh full replay accepts neither --resume nor --performance")
        full_replay_fresh(args.checkpoint, args.observations)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
