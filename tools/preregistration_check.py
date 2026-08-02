#!/usr/bin/env python3
"""Validate the machine-readable freeze embedded in a cycle preregistration."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


SCHEMA = "research-preregistration-freeze-v1"
MARKER = re.compile(r"<!--\s*research-freeze-v1\s*\n(.*?)\n\s*-->", re.DOTALL)
CYCLE = re.compile(r"cycle-(\d+)(?:-|$)")
TYPED_KINDS = {"integer", "rational", "symbolic", "expression", "text", "not_applicable"}


class PreflightError(ValueError):
    """A preregistration is incomplete or not operationally frozen."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PreflightError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_state(root: Path) -> dict[str, str]:
    head_process = subprocess.run(["git", "rev-parse", "--verify", "HEAD"], cwd=root, check=False, capture_output=True, text=True)
    head = head_process.stdout.strip() if head_process.returncode == 0 else "UNBORN"
    status = subprocess.run(["git", "status", "--short"], cwd=root, check=True, capture_output=True, text=True).stdout.strip()
    return {"head": head, "status": status or "CLEAN"}


def extract_manifest(path: Path) -> dict[str, Any]:
    matches = MARKER.findall(path.read_text(encoding="utf-8"))
    require(len(matches) == 1, f"{path}: expected exactly one research-freeze-v1 manifest")
    try:
        manifest = json.loads(matches[0])
    except json.JSONDecodeError as exc:
        raise PreflightError(f"{path}: malformed freeze JSON: {exc.msg}") from exc
    require(isinstance(manifest, dict), f"{path}: freeze manifest must be an object")
    return manifest


def typed_entries(value: Any, label: str) -> None:
    require(isinstance(value, dict) and value, f"{label}: expected nonempty object")
    for name, entry in value.items():
        require(isinstance(name, str) and name.strip(), f"{label}: blank name")
        require(isinstance(entry, dict), f"{label}.{name}: expected object")
        kind = entry.get("kind")
        require(kind in TYPED_KINDS, f"{label}.{name}: invalid kind")
        if kind == "not_applicable":
            require(isinstance(entry.get("justification"), str) and entry["justification"].strip(), f"{label}.{name}: missing not_applicable justification")
        else:
            require("value" in entry and entry["value"] not in ("", None, [], {}), f"{label}.{name}: missing value")
        require(isinstance(entry.get("rationale"), str) and entry["rationale"].strip(), f"{label}.{name}: missing rationale")


def nonempty_text_list(value: Any, label: str) -> None:
    require(isinstance(value, list) and value, f"{label}: expected nonempty list")
    for index, item in enumerate(value):
        require(isinstance(item, str) and item.strip(), f"{label}[{index}]: expected nonempty text")


def validate_preregistration(
    path: Path, *, expected_cycle: int | None = None, enforce_manifest_head: bool = True
) -> dict[str, Any]:
    """Return a checked manifest; never writes to the preregistration."""
    path = path.resolve()
    manifest = extract_manifest(path)
    require(manifest.get("schema") == SCHEMA, f"{path}: unsupported freeze schema")
    match = CYCLE.search(path.name)
    require(match is not None, f"{path}: cycle number absent from filename")
    cycle = int(match.group(1))
    require(manifest.get("cycle") == cycle, f"{path}: manifest cycle does not match filename")
    if expected_cycle is not None:
        require(cycle == expected_cycle, f"{path}: expected Cycle {expected_cycle}")
    typed_entries(manifest.get("parameters"), "parameters")
    typed_entries(manifest.get("resource_caps"), "resource_caps")
    nonempty_text_list(manifest.get("formula_families"), "formula_families")
    nonempty_text_list(manifest.get("selection_rule"), "selection_rule")
    nonempty_text_list(manifest.get("failure_rule"), "failure_rule")
    preexecution = manifest.get("pre_execution")
    require(isinstance(preexecution, dict), "pre_execution: expected object")
    require(isinstance(preexecution.get("timestamp_utc"), str) and preexecution["timestamp_utc"].endswith("Z"), "pre_execution.timestamp_utc: require UTC timestamp")
    require(isinstance(preexecution.get("git_head"), str) and preexecution["git_head"].strip(), "pre_execution.git_head: missing head declaration")
    require(isinstance(preexecution.get("git_state"), str) and preexecution["git_state"].strip(), "pre_execution.git_state: missing state declaration")
    inputs = manifest.get("input_paths")
    require(isinstance(inputs, list) and inputs, "input_paths: expected nonempty list")
    project_root = path.parents[1]
    checked_inputs = []
    for item in inputs:
        require(isinstance(item, str) and item.strip(), "input_paths: invalid path")
        resolved = project_root / item
        require(resolved.is_file(), f"input_paths: missing {item}")
        checked_inputs.append({"path": item, "sha256": sha256(resolved)})
    current_git = git_state(project_root)
    if enforce_manifest_head:
        require(preexecution["git_head"] == current_git["head"], "pre_execution.git_head: current head drift")
    return {
        "schema": SCHEMA,
        "cycle": cycle,
        "path": str(path),
        "manifest_sha256": sha256(path),
        "input_hashes": checked_inputs,
        "git_now": current_git,
        "parameters": manifest["parameters"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("preregistration", type=Path)
    parser.add_argument("--expected-cycle", type=int)
    parser.add_argument("--json", action="store_true", help="emit the checked freeze record as JSON")
    parser.add_argument("--allow-head-drift", action="store_true", help="replay a frozen manifest after a later commit")
    args = parser.parse_args()
    try:
        result = validate_preregistration(
            args.preregistration, expected_cycle=args.expected_cycle,
            enforce_manifest_head=not args.allow_head_drift,
        )
    except (OSError, subprocess.CalledProcessError, PreflightError) as exc:
        print(f"preflight: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"OK: Cycle {result['cycle']} preregistration freeze; manifest {result['manifest_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
