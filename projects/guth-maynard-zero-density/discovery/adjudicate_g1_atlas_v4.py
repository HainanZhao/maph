#!/usr/bin/env python3
"""Independently reconcile two complete fresh G1 v4 production runs.

This standard-library adjudicator imports none of the probe engines.  It emits
an immutable empirical-reconciliation artifact only after checking both exact
driver chains, complete row/validation coverage, per-run unverified status,
distinct fresh checkpoints, checkpoint-to-observation bindings, and
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
V4_ENGINE = ROOT / "discovery/run_g1_atlas_v4.py"
V4_ENGINE_SHA256 = "e7171c7b4720797b5a9bb87246c10a1e7f26569c9f240f69923de782f262dbd5"
V3_ENGINE_SHA256 = "921f25ae3f6d535899b439b04f310bc91b4278046976b7ad7947c04b6166f06f"
V2_ENGINE_SHA256 = "62d3b565f4b80f7a7d17d19e779eec5107a1b2df11990cb30db1dc1d07830941"
V1_ENGINE_SHA256 = "78f5088cbe615237d565854428511cda03e22fc04838d192c64d3215748c28ee"
PREREG_SHA256 = "227ec1c66b2e109653354b6c3245b4e809fe52692c01514ac10064c23db2b6f8"
VALIDATION_SCALES = ("2^15", "2^18")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"required reconciliation input is absent: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"reconciliation input is not a JSON object: {path}")
    return value


def expected_screen_ids() -> list[str]:
    return [f"G1-S{index:03d}" for index in range(588)]


def validate_screen_rows(rows: list[dict[str, Any]], label: str) -> None:
    require(len(rows) == 588, f"run {label} does not contain 588 screen rows")
    require([row.get("row_id") for row in rows] == expected_screen_ids(), f"run {label} screen row IDs/order mismatch")
    require([row.get("screen_index") for row in rows] == list(range(588)), f"run {label} screen indexes mismatch")
    require(all(row.get("status") in {"COMPLETED", "FAILED"} for row in rows), f"run {label} has invalid screen status")


def validate_validation_rows(rows: list[dict[str, Any]], selected: list[str], label: str) -> None:
    expected = [(row_id, scale) for row_id in selected for scale in VALIDATION_SCALES]
    actual = [(row.get("validation_of"), row.get("validation_scale")) for row in rows]
    require(actual == expected, f"run {label} validation coverage/order mismatch")
    require(len(rows) <= 72, f"run {label} validation-row cap exceeded")
    require(all("validation_comparison" in row for row in rows), f"run {label} validation comparison missing")


def validate_observations(observations: dict[str, Any], label: str) -> None:
    require(observations.get("artifact_id") == "cycle-3-g1-atlas-observations-v4", f"run {label} observation ID mismatch")
    boundary = observations.get("promotion_boundary", {})
    require(boundary.get("status") == "UNVERIFIED_PENDING_SECOND_FRESH_RUN", f"run {label} lacks unverified promotion status")
    require(boundary.get("promotion_allowed") is False, f"run {label} improperly permits promotion")
    require(boundary.get("cached_assembly_is_not_promotion_evidence") is True, f"run {label} cached-assembly firewall missing")
    require(observations.get("correction", {}).get("engine_v4_sha256") == V4_ENGINE_SHA256, f"run {label} v4 observation engine mismatch")
    require(observations.get("preregistration", {}).get("sha256") == PREREG_SHA256, f"run {label} preregistration identity mismatch")
    local_rows = observations.get("structural", {}).get("local_rows", [])
    transfer_rows = observations.get("structural", {}).get("transfer_rows", [])
    require(len(local_rows) == 7744, f"run {label} local structural coverage mismatch")
    require(len(transfer_rows) == 560, f"run {label} transfer structural coverage mismatch")
    validate_screen_rows(observations.get("screen_rows", []), label)
    selected = observations.get("retained_screen_row_ids", [])
    require(len(selected) <= 36 and len(set(selected)) == len(selected), f"run {label} retained-row bound/uniqueness mismatch")
    validate_validation_rows(observations.get("validation", {}).get("rows", []), selected, label)
    summary = observations.get("screen_outcome_summary", {})
    require(summary.get("scheduled_rows") == 588, f"run {label} screen summary count mismatch")
    require(summary.get("retained_row_ids") == selected, f"run {label} retained summary mismatch")
    require(summary.get("validation_rows") == 2 * len(selected), f"run {label} validation summary mismatch")


def validate_checkpoint(checkpoint: dict[str, Any], observations: dict[str, Any], observations_path: Path, label: str) -> None:
    require(checkpoint.get("phase") == "COMPLETE", f"run {label} checkpoint is not COMPLETE")
    require(checkpoint.get("driver_v4", {}).get("sha256") == V4_ENGINE_SHA256, f"run {label} checkpoint v4 identity mismatch")
    require(checkpoint.get("driver_v3", {}).get("sha256") == V3_ENGINE_SHA256, f"run {label} checkpoint v3 identity mismatch")
    require(checkpoint.get("engine", {}).get("v2_sha256") == V2_ENGINE_SHA256, f"run {label} checkpoint v2 identity mismatch")
    require(checkpoint.get("engine", {}).get("v1_sha256") == V1_ENGINE_SHA256, f"run {label} checkpoint v1 identity mismatch")
    origin = checkpoint.get("production_origin_v4", {})
    require(origin.get("run_label") == label, f"run {label} origin label mismatch")
    require(origin.get("started_from_empty_checkpoint") is True, f"run {label} was not declared fresh")
    require(origin.get("resume_allowed") is False, f"run {label} improperly permits resume")
    completion = checkpoint.get("fresh_full_completion_v4", {})
    require(completion.get("status") == "COMPLETE_UNVERIFIED", f"run {label} completion status mismatch")
    require(completion.get("run_label") == label, f"run {label} completion label mismatch")
    require(completion.get("driver_v4_sha256") == V4_ENGINE_SHA256, f"run {label} completion engine mismatch")
    require(completion.get("observations_sha256") == sha256(observations_path), f"run {label} checkpoint/observation hash mismatch")
    require(Path(completion.get("observations", "")).resolve() == observations_path.resolve(), f"run {label} checkpoint/observation path mismatch")
    validate_screen_rows(checkpoint.get("screen_rows", []), label)
    require(checkpoint.get("screen_rows") == observations.get("screen_rows"), f"run {label} checkpoint/observation screen payload mismatch")
    selected = checkpoint.get("selected_screen_row_ids", [])
    require(selected == observations.get("retained_screen_row_ids"), f"run {label} checkpoint/observation retained set mismatch")
    validation = checkpoint.get("validation_rows", [])
    validate_validation_rows(validation, selected, label)
    require(validation == observations.get("validation", {}).get("rows", []), f"run {label} checkpoint/observation validation payload mismatch")
    require(checkpoint.get("finite_rows_started", 0) <= 660, f"run {label} finite-row cap exceeded")
    require(checkpoint.get("aggregate_cpu_seconds", 0) < 128 * 3600, f"run {label} aggregate CPU cap reached or exceeded")
    require(len(checkpoint.get("performance_rows", [])) == 588 + len(validation), f"run {label} performance coverage mismatch")


def require_two_fresh_runs(records: list[dict[str, Any]]) -> None:
    """Promotion firewall independently testable without accepting cached assembly."""
    require(len(records) == 2, "empirical promotion requires exactly two fresh runs")
    require({record.get("label") for record in records} == {"A", "B"}, "fresh-run labels must be A and B")
    require(all(record.get("fresh") is True for record in records), "cached/resumed assembly cannot promote")
    require(records[0].get("checkpoint") != records[1].get("checkpoint"), "fresh runs require distinct checkpoint paths")
    require(records[0].get("observations") != records[1].get("observations"), "fresh runs require distinct observation paths")
    require(records[0].get("observations_sha256") == records[1].get("observations_sha256"), "fresh observations are not byte-identical")


def reconcile(checkpoint_a: Path, observations_a: Path, checkpoint_b: Path, observations_b: Path) -> dict[str, Any]:
    require(sha256(V4_ENGINE) == V4_ENGINE_SHA256, "G1 v4 production engine hash mismatch")
    require(checkpoint_a.resolve() != checkpoint_b.resolve(), "run checkpoints must be distinct paths")
    require(observations_a.resolve() != observations_b.resolve(), "run observations must be distinct paths")
    cp_a, cp_b = load_json(checkpoint_a), load_json(checkpoint_b)
    obs_a, obs_b = load_json(observations_a), load_json(observations_b)
    validate_observations(obs_a, "A")
    validate_observations(obs_b, "B")
    validate_checkpoint(cp_a, obs_a, observations_a, "A")
    validate_checkpoint(cp_b, obs_b, observations_b, "B")
    records = [
        {"label": "A", "fresh": cp_a["production_origin_v4"]["started_from_empty_checkpoint"], "checkpoint": str(checkpoint_a.resolve()), "observations": str(observations_a.resolve()), "observations_sha256": sha256(observations_a)},
        {"label": "B", "fresh": cp_b["production_origin_v4"]["started_from_empty_checkpoint"], "checkpoint": str(checkpoint_b.resolve()), "observations": str(observations_b.resolve()), "observations_sha256": sha256(observations_b)},
    ]
    require_two_fresh_runs(records)
    require(observations_a.read_bytes() == observations_b.read_bytes(), "fresh timing-independent observation bytes disagree")
    summary = obs_a["screen_outcome_summary"]
    return {
        "artifact_id": "cycle-3-g1-atlas-empirical-reconciliation-v1",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "Two-run deterministic finite empirical reconciliation only. It is not an independent mathematical proof, theorem, extremizer, saturation result, or density improvement.",
        "status": "EMPIRICALLY_RECONCILED",
        "promotion_scope": "G1 finite discovery evidence only",
        "adjudicator": {"path": str(Path(__file__).relative_to(ROOT)), "sha256": sha256(Path(__file__))},
        "engine_chain": {"v4": V4_ENGINE_SHA256, "v3": V3_ENGINE_SHA256, "v2": V2_ENGINE_SHA256, "v1": V1_ENGINE_SHA256, "preregistration": PREREG_SHA256},
        "runs": [
            {**record, "checkpoint_sha256": sha256(checkpoint_a if record["label"] == "A" else checkpoint_b)}
            for record in records
        ],
        "agreement": {
            "timing_independent_observations": "BYTE_IDENTICAL",
            "observations_sha256": sha256(observations_a),
            "screen_rows": 588,
            "local_structural_rows": 7744,
            "transfer_structural_rows": 560,
            "retained_rows": len(obs_a["retained_screen_row_ids"]),
            "validation_rows": len(obs_a["validation"]["rows"]),
        },
        "screen_outcome_summary": summary,
        "cached_assembly_alone_cannot_promote": true_value(),
    }


def true_value() -> bool:
    """Avoid an untagged magic literal in the reconciliation constructor."""
    return True


def render(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=2) + "\n").encode("utf-8")


def write_new(path: Path, value: dict[str, Any]) -> None:
    require(not path.exists(), "refusing to overwrite empirical reconciliation artifact")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(render(value))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint-a", type=Path, required=True)
    parser.add_argument("--observations-a", type=Path, required=True)
    parser.add_argument("--checkpoint-b", type=Path, required=True)
    parser.add_argument("--observations-b", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", type=Path)
    mode.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = reconcile(args.checkpoint_a, args.observations_a, args.checkpoint_b, args.observations_b)
    if args.write is not None:
        write_new(args.write, result)
    else:
        require(args.check.is_file() and args.check.read_bytes() == render(result), "empirical reconciliation mismatch")
    print(json.dumps({"status": result["status"], "observations_sha256": result["agreement"]["observations_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
