#!/usr/bin/env python3
"""Crash-safe corrected driver for the frozen Cycle-3 G1 finite atlas.

This v2 driver preserves every v1 mathematical constructor and frozen screen
row.  It corrects only runtime enforcement, unexpected-exception retention,
larger-scale score-loss adjudication, and crash recovery.  All finite complex
outputs remain discovery-only ``RECOGNIZED``/``OBSERVED`` data.
"""
from __future__ import annotations

import argparse
from decimal import Decimal, localcontext
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import resource
import sys
import tempfile
import time
from typing import Any

import mpmath


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from discovery import run_g1_atlas_v1 as base  # noqa: E402


BASE_ENGINE = ROOT / "discovery/run_g1_atlas_v1.py"
BASE_ENGINE_SHA256 = "78f5088cbe615237d565854428511cda03e22fc04838d192c64d3215748c28ee"
EXPECTED_IMPLEMENTATION = "CPython"
EXPECTED_PYTHON = "3.12.3"
EXPECTED_MPMATH = "1.2.1"
EXPECTED_OPTIMIZE = 0
CHECKPOINT_SCHEMA = 2


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def runtime_record() -> dict[str, Any]:
    return {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "mpmath": mpmath.__version__,
        "optimization_level": sys.flags.optimize,
    }


def check_runtime() -> dict[str, Any]:
    """Fail closed on every frozen runtime or predecessor identity."""
    record = runtime_record()
    require(sha256(BASE_ENGINE) == BASE_ENGINE_SHA256, "G1 v1 predecessor engine hash mismatch")
    require(record["implementation"] == EXPECTED_IMPLEMENTATION, "G1 runtime implementation mismatch")
    require(record["python"] == EXPECTED_PYTHON, "G1 Python version mismatch")
    require(record["mpmath"] == EXPECTED_MPMATH, "G1 mpmath version mismatch")
    require(record["optimization_level"] == EXPECTED_OPTIMIZE, "G1 optimization mode must be CPython default (-O is prohibited)")
    # The predecessor's optimization-safe integrity function directly checks
    # preregistration, document, and both primary source hashes.
    report = base.integrity_report()
    require(report["screen_rows"] == 588 and report["structural_local_rows"] == 7744, "G1 predecessor integrity counts mismatch")
    return record


def sanitize_exception(exc: Exception) -> dict[str, str]:
    """Return a bounded deterministic exception identity, without addresses."""
    exception_type = type(exc).__name__
    message = " ".join(str(exc).split())
    message = message.replace(str(ROOT), "<PROJECT>")
    message = re.sub(r"0x[0-9a-fA-F]+", "<HEX>", message)
    message = re.sub(r"\b[Pp][Ii][Dd][=: ]+\d+\b", "pid=<PID>", message)
    message = message[:512]
    code_type = re.sub(r"[^A-Za-z0-9]+", "_", exception_type).upper().strip("_") or "UNKNOWN"
    return {
        "code": f"UNEXPECTED_EXCEPTION_{code_type}",
        "exception_type": exception_type,
        "message": message,
    }


def current_rss_bytes() -> int:
    return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) * 1024


def safe_run_row(spec: dict[str, Any], U: int, scale_label: str) -> tuple[dict[str, Any], dict[str, Any]]:
    """Retain unexpected Exceptions; intentionally propagate BaseException."""
    wall_started = time.monotonic()
    cpu_started = time.process_time()
    try:
        return base.run_screen_row(spec, U=U, scale_label=scale_label)
    except Exception as exc:
        identity = sanitize_exception(exc)
        detail = {
            "exception_type": identity["exception_type"],
            "sanitized_message": identity["message"],
            "policy": "Unexpected Exception retained once; no parameter-changing retry. KeyboardInterrupt and SystemExit are not caught.",
        }
        row = base.failed_screen_row(spec, U, identity["code"], detail, scale_label=scale_label)
        return row, {
            "wall_seconds": time.monotonic() - wall_started,
            "cpu_seconds": time.process_time() - cpu_started,
            "peak_rss_bytes": current_rss_bytes(),
        }


def decimal_score(value: str) -> Decimal:
    with localcontext() as context:
        context.prec = 128
        return +Decimal(value)


def validation_comparison(validation: dict[str, Any], screen: dict[str, Any]) -> dict[str, Any]:
    """Literal frozen falsifier: any strict larger-scale score decrease."""
    if validation["status"] != "COMPLETED":
        return {
            "epistemic_status": "OBSERVED",
            "status": "VALIDATION_EXECUTION_FAILURE",
            "claim_boundary": "Failed validation row only; not a score comparison or no-go result.",
            "screen_score": screen["retention"].get("score"),
            "validation_score": None,
            "difference_validation_minus_screen": None,
        }
    screen_score = decimal_score(screen["retention"]["score"])
    validation_score = decimal_score(validation["retention"]["score"])
    difference = validation_score - screen_score
    status = "SCORE_LOSS_FALSIFIER" if difference < 0 else "NO_SCORE_LOSS"
    return {
        "epistemic_status": "OBSERVED",
        "status": status,
        "claim_boundary": "Deterministic comparison of two finite 112-digit discovery scores; not a theorem or asymptotic claim.",
        "rule": "SCORE_LOSS_FALSIFIER iff validation_score < screen_score; equality is NO_SCORE_LOSS.",
        "screen_score": str(screen_score),
        "validation_score": str(validation_score),
        "difference_validation_minus_screen": str(difference),
        "validation_retention_eligible": validation["retention"]["eligible"],
    }


def json_bytes(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=2) + "\n").encode("utf-8")


def atomic_replace(path: Path, value: dict[str, Any]) -> None:
    """Durably replace a checkpoint using a same-directory temporary file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(json_bytes(value))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary.exists():
            temporary.unlink()


def atomic_write_or_verify(path: Path, value: dict[str, Any]) -> None:
    rendered = json_bytes(value)
    if path.exists():
        require(path.read_bytes() == rendered, f"refusing to replace mismatched final artifact: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(rendered)
            stream.flush()
            os.fsync(stream.fileno())
        # The new-only check is repeated immediately before the atomic rename.
        require(not path.exists(), f"final artifact appeared concurrently: {path}")
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def new_checkpoint(runtime: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_id": "cycle-3-g1-atlas-run-checkpoint-v2",
        "checkpoint_schema": CHECKPOINT_SCHEMA,
        "epistemic_status": "OBSERVED",
        "claim_boundary": "Crash-recovery state only. It is not a final discovery artifact or mathematical claim.",
        "engine": {
            "v2_path": str(Path(__file__).relative_to(ROOT)),
            "v2_sha256": sha256(Path(__file__)),
            "v1_path": str(BASE_ENGINE.relative_to(ROOT)),
            "v1_sha256": BASE_ENGINE_SHA256,
        },
        "runtime": runtime,
        "phase": "SCREEN",
        "screen_rows": [],
        "selected_screen_row_ids": [],
        "validation_rows": [],
        "performance_rows": [],
        "finite_rows_started": 0,
        "aggregate_cpu_seconds": 0.0,
    }


def load_checkpoint(path: Path, runtime: dict[str, Any]) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    require(data.get("checkpoint_schema") == CHECKPOINT_SCHEMA, "G1 checkpoint schema mismatch")
    require(data.get("engine", {}).get("v2_sha256") == sha256(Path(__file__)), "G1 checkpoint v2 engine hash mismatch")
    require(data.get("engine", {}).get("v1_sha256") == BASE_ENGINE_SHA256, "G1 checkpoint v1 engine hash mismatch")
    require(data.get("runtime") == runtime, "G1 checkpoint runtime mismatch")
    require(data.get("phase") in {"SCREEN", "VALIDATION", "ASSEMBLY", "COMPLETE"}, "G1 checkpoint phase invalid")
    specs = base.canonical_screen_specs()
    screen_rows = data.get("screen_rows", [])
    validation_rows = data.get("validation_rows", [])
    performance_rows = data.get("performance_rows", [])
    require(len(screen_rows) <= len(specs), "G1 checkpoint has too many screen rows")
    for index, row in enumerate(screen_rows):
        require(row.get("row_id") == specs[index]["row_id"], "G1 checkpoint screen prefix mismatch")
        require(row.get("screen_index") == index, "G1 checkpoint screen index mismatch")
        require(row.get("status") in {"COMPLETED", "FAILED"}, "G1 checkpoint screen status invalid")
    require(len(performance_rows) == len(screen_rows) + len(validation_rows), "G1 checkpoint performance/row accounting mismatch")
    recorded_cpu = sum(float(row["cpu_seconds"]) for row in performance_rows)
    require(recorded_cpu == float(data.get("aggregate_cpu_seconds", -1.0)), "G1 checkpoint aggregate CPU sum mismatch")
    require(data.get("finite_rows_started", 0) <= base.MAX_FINITE_ROWS, "G1 checkpoint finite-row cap exceeded")
    return data


def resource_cap_row(spec: dict[str, Any], U: int, scale_label: str, checkpoint: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    return base.aggregate_cap_failure(
        spec,
        U,
        scale_label=scale_label,
        cpu_seconds=float(checkpoint["aggregate_cpu_seconds"]),
        finite_rows=int(checkpoint["finite_rows_started"]),
    )


def update_accounting(checkpoint: dict[str, Any], performance: dict[str, Any], *, attempted: bool) -> None:
    if attempted:
        checkpoint["finite_rows_started"] += 1
    checkpoint["aggregate_cpu_seconds"] += float(performance["cpu_seconds"])
    require(checkpoint["finite_rows_started"] <= base.MAX_FINITE_ROWS, "G1 finite-row cap exceeded")


def may_attempt(checkpoint: dict[str, Any]) -> bool:
    return (
        checkpoint["finite_rows_started"] < base.MAX_FINITE_ROWS
        and checkpoint["aggregate_cpu_seconds"] < base.AGGREGATE_CPU_CAP_SECONDS
    )


def run_or_resume(checkpoint_path: Path, *, resume: bool) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    runtime = check_runtime()
    if resume:
        require(checkpoint_path.is_file(), "--resume requires an existing checkpoint")
        checkpoint = load_checkpoint(checkpoint_path, runtime)
    else:
        require(not checkpoint_path.exists(), "checkpoint already exists; use --resume explicitly")
        checkpoint = new_checkpoint(runtime)
        atomic_replace(checkpoint_path, checkpoint)

    specs = base.canonical_screen_specs()
    for spec in specs[len(checkpoint["screen_rows"]):]:
        if may_attempt(checkpoint):
            row, performance = safe_run_row(spec, base.SCREEN_SCALE, "2^12")
            attempted = True
        else:
            row, performance = resource_cap_row(spec, base.SCREEN_SCALE, "2^12", checkpoint)
            attempted = False
        checkpoint["screen_rows"].append(row)
        checkpoint["performance_rows"].append({"phase": "screen", "row_id": spec["row_id"], **performance})
        update_accounting(checkpoint, performance, attempted=attempted)
        atomic_replace(checkpoint_path, checkpoint)

    selected = base.retention_selection(checkpoint["screen_rows"])
    if checkpoint["selected_screen_row_ids"]:
        require(checkpoint["selected_screen_row_ids"] == selected, "G1 retained set changed across resume")
    else:
        checkpoint["selected_screen_row_ids"] = selected
    checkpoint["phase"] = "VALIDATION"
    atomic_replace(checkpoint_path, checkpoint)

    spec_by_id = {spec["row_id"]: spec for spec in specs}
    screen_by_id = {row["row_id"]: row for row in checkpoint["screen_rows"]}
    validation_plan = [(row_id, scale) for row_id in selected for scale in base.VALIDATION_SCALES]
    existing = checkpoint["validation_rows"]
    require(len(existing) <= len(validation_plan), "G1 checkpoint has too many validation rows")
    for index, row in enumerate(existing):
        expected_id, expected_scale = validation_plan[index]
        require(row.get("validation_of") == expected_id, "G1 checkpoint validation ID mismatch")
        require(row.get("validation_scale") == f"2^{expected_scale.bit_length() - 1}", "G1 checkpoint validation scale mismatch")

    for row_id, scale in validation_plan[len(existing):]:
        spec = spec_by_id[row_id]
        label = f"2^{scale.bit_length() - 1}"
        if may_attempt(checkpoint):
            row, performance = safe_run_row(spec, scale, label)
            attempted = True
        else:
            row, performance = resource_cap_row(spec, scale, label, checkpoint)
            attempted = False
        row["validation_of"] = row_id
        row["validation_scale"] = label
        row["validation_comparison"] = validation_comparison(row, screen_by_id[row_id])
        checkpoint["validation_rows"].append(row)
        checkpoint["performance_rows"].append({"phase": "validation", "row_id": row_id, "scale": label, **performance})
        update_accounting(checkpoint, performance, attempted=attempted)
        atomic_replace(checkpoint_path, checkpoint)

    checkpoint["phase"] = "ASSEMBLY"
    atomic_replace(checkpoint_path, checkpoint)
    observations = assemble_observations(checkpoint)
    performance = assemble_performance(checkpoint)
    return observations, performance, checkpoint


def validation_summary(checkpoint: dict[str, Any]) -> list[dict[str, Any]]:
    rows = checkpoint["validation_rows"]
    result = []
    for row_id in checkpoint["selected_screen_row_ids"]:
        comparisons = [row["validation_comparison"] for row in rows if row["validation_of"] == row_id]
        statuses = [item["status"] for item in comparisons]
        if "VALIDATION_EXECUTION_FAILURE" in statuses:
            outcome = "VALIDATION_EXECUTION_FAILURE"
        elif "SCORE_LOSS_FALSIFIER" in statuses:
            outcome = "SCORE_LOSS_FALSIFIER"
        else:
            outcome = "NO_SCORE_LOSS"
        result.append({
            "screen_row_id": row_id,
            "epistemic_status": "OBSERVED",
            "outcome": outcome,
            "scale_statuses": statuses,
            "claim_boundary": "Finite cross-scale discovery classification only; not an asymptotic conclusion.",
        })
    return result


def screen_outcome_summary(checkpoint: dict[str, Any]) -> dict[str, Any]:
    rows = checkpoint["screen_rows"]
    failures: dict[str, int] = {}
    feasible_by_regime = {"low": 0, "intermediate": 0, "high": 0}
    for row in rows:
        if row["status"] == "COMPLETED":
            feasible_by_regime[row["family"]["declared_energy_regime"]] += 1
        else:
            code = row["failure"]["code"]
            failures[code] = failures.get(code, 0) + 1
    retained = checkpoint["selected_screen_row_ids"]
    low_status = "NO_FEASIBLE_LOW_REGIME_ROWS" if feasible_by_regime["low"] == 0 else "FEASIBLE_LOW_REGIME_ROWS_PRESENT"
    return {
        "epistemic_status": "OBSERVED",
        "claim_boundary": "Complete finite frozen-screen accounting only; no universal construction or asymptotic claim.",
        "scheduled_rows": len(rows),
        "completed_rows": sum(row["status"] == "COMPLETED" for row in rows),
        "failed_rows": sum(row["status"] != "COMPLETED" for row in rows),
        "failure_code_counts": dict(sorted(failures.items())),
        "feasible_rows_by_declared_energy_regime": feasible_by_regime,
        "low_regime_status": low_status,
        "retained_rows": len(retained),
        "retained_row_ids": retained,
        "validation_rows": len(checkpoint["validation_rows"]),
        "retention_status": "NO_RETAINED" if not retained else "RETAINED_ROWS_PRESENT",
        "no_retuning": True,
    }


def assemble_observations(checkpoint: dict[str, Any]) -> dict[str, Any]:
    observations = base.build_observations(
        checkpoint["screen_rows"], checkpoint["validation_rows"],
        run_mode="FROZEN_588_SCREEN_AND_RETAINED_REPLAY_V2",
    )
    observations["artifact_id"] = "cycle-3-g1-atlas-observations-v2"
    observations["correction"] = {
        "supersedes_engine": "run_g1_atlas_v1.py operationally; v1 failed-launch evidence remains preserved",
        "failed_launch_artifact": "artifacts/cycle-3-g1-atlas-first-launch-failure-v1.json",
        "engine_v2_sha256": sha256(Path(__file__)),
        "engine_v1_sha256": BASE_ENGINE_SHA256,
    }
    observations["runtime"] = checkpoint["runtime"] | {"precisions_bits": list(base.PRECISIONS_BITS)}
    observations["validation"]["summary"] = validation_summary(checkpoint)
    observations["screen_outcome_summary"] = screen_outcome_summary(checkpoint)
    observations["resource_accounting"] = {
        "finite_rows_started": checkpoint["finite_rows_started"],
        "maximum_finite_rows": base.MAX_FINITE_ROWS,
        "aggregate_cpu_cap_seconds": base.AGGREGATE_CPU_CAP_SECONDS,
    }
    return observations


def assemble_performance(checkpoint: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_id": "cycle-3-g1-atlas-performance-v2",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "Host performance and crash-recovery accounting only; excluded from timing-independent mathematical observations.",
        "runtime": checkpoint["runtime"],
        "engine_v2_sha256": sha256(Path(__file__)),
        "row_count": len(checkpoint["performance_rows"]),
        "finite_rows_started": checkpoint["finite_rows_started"],
        "aggregate_cpu_seconds": checkpoint["aggregate_cpu_seconds"],
        "rows": checkpoint["performance_rows"],
        "resource_caps": {
            "seconds_per_finite_row": base.ROW_SECONDS_CAP,
            "max_rss_bytes": base.ROW_RSS_CAP,
            "maximum_finite_rows": base.MAX_FINITE_ROWS,
            "aggregate_cpu_hours": 128,
            "aggregate_cpu_cap_seconds": base.AGGREGATE_CPU_CAP_SECONDS,
        },
    }


def finalize(checkpoint_path: Path, observations_path: Path, performance_path: Path, *, resume: bool, check_path: Path | None = None) -> None:
    observations, performance, checkpoint = run_or_resume(checkpoint_path, resume=resume)
    if check_path is not None:
        require(check_path.is_file(), "observations check target is absent")
        require(check_path.read_bytes() == json_bytes(observations), "G1 v2 observations replay mismatch")
        checkpoint["phase"] = "COMPLETE"
        checkpoint["replay_check"] = {
            "observations": str(check_path),
            "observations_sha256": hashlib.sha256(json_bytes(observations)).hexdigest(),
            "status": "MATCH",
        }
    else:
        # Performance is written first; the authoritative observations artifact
        # is the commit marker for a complete assembly.
        atomic_write_or_verify(performance_path, performance)
        atomic_write_or_verify(observations_path, observations)
        checkpoint["phase"] = "COMPLETE"
        checkpoint["final_artifacts"] = {
            "observations": str(observations_path), "observations_sha256": hashlib.sha256(json_bytes(observations)).hexdigest(),
            "performance": str(performance_path), "performance_sha256": hashlib.sha256(json_bytes(performance)).hexdigest(),
        }
    atomic_replace(checkpoint_path, checkpoint)


def integrity_report() -> dict[str, Any]:
    runtime = check_runtime()
    return {
        "epistemic_status": "OBSERVED",
        "claim_boundary": "Operational integrity of corrected discovery driver only; no finite screen row evaluated.",
        "engine_v2_sha256": sha256(Path(__file__)),
        "engine_v1_sha256": BASE_ENGINE_SHA256,
        "runtime": runtime,
        "screen_rows": 588,
        "validation_row_cap": 72,
        "finite_row_cap": base.MAX_FINITE_ROWS,
        "unexpected_exception_policy": "retain sanitized distinct code; do not catch KeyboardInterrupt/SystemExit",
        "validation_score_loss_rule": "strict Decimal(validation_score) < Decimal(screen_score)",
        "checkpoint_schema": CHECKPOINT_SCHEMA,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check-integrity", action="store_true")
    action.add_argument("--run-full", action="store_true")
    action.add_argument("--check-observations", type=Path, metavar="PATH")
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--write-observations", type=Path)
    parser.add_argument("--write-performance", type=Path)
    args = parser.parse_args()
    if args.check_integrity:
        require(not args.resume and args.checkpoint is None and args.write_observations is None and args.write_performance is None, "integrity check accepts no run/write arguments")
        print(json.dumps(integrity_report(), sort_keys=True))
        return 0
    require(args.checkpoint is not None, "full run/replay requires --checkpoint PATH")
    if args.check_observations is not None:
        require(args.write_observations is None and args.write_performance is None, "check mode accepts no write paths")
        # Paths are schema placeholders only in check mode; no final files are written.
        finalize(args.checkpoint, args.check_observations, Path("<unused-performance>"), resume=args.resume, check_path=args.check_observations)
        print(json.dumps({"artifact": str(args.check_observations), "replayed": True}, sort_keys=True))
        return 0
    require(args.write_observations is not None and args.write_performance is not None, "--run-full requires both final write paths")
    finalize(args.checkpoint, args.write_observations, args.write_performance, resume=args.resume)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
