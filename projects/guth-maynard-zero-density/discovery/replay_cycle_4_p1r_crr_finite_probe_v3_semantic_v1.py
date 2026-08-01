#!/usr/bin/env python3
"""Full deterministic semantic replay of the immutable CRR finite probe v3.

This recomputes the frozen 160-row calculation but never overwrites its result
artifact. Variable wall time and peak RSS are excluded from equality; every
other result field, including every row field/status, is compared exactly.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import time
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
RESULT = ROOT / "discovery/cycle-4-p1r-crr-finite-probe-v3.json"
RUNNER = ROOT / "discovery/run_cycle_4_p1r_crr_finite_probe_v3.py"
OUTPUT = ROOT / "discovery/cycle-4-p1r-crr-finite-probe-v3-semantic-replay-v1.json"
EXPECTED_RESULT_SHA256 = "41576b9ad21d44435d251a8fefad1cc64bb038384644ce93c1d1a4314c38a0cb"
EXPECTED_RUNNER_SHA256 = "667207f0f690aaf36f33fa498a5b90594e2ac500173c44db64388e2958b4d90f"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_runner():
    spec = importlib.util.spec_from_file_location("crr_probe_v3_semantic_replay_runner", RUNNER)
    require(spec is not None and spec.loader is not None, "cannot load immutable v3 runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def deterministic_projection(payload: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(payload)
    result["resources"].pop("wall_seconds", None)
    result["resources"].pop("peak_rss_bytes", None)
    return result


def first_difference(expected: Any, actual: Any, path: str = "$") -> dict[str, str] | None:
    if type(expected) is not type(actual):
        return {"path": path, "expected": repr(expected)[:1000], "actual": repr(actual)[:1000]}
    if isinstance(expected, dict):
        if set(expected) != set(actual):
            return {"path": path, "expected_keys": repr(sorted(expected))[:1000], "actual_keys": repr(sorted(actual))[:1000]}
        for key in sorted(expected):
            difference = first_difference(expected[key], actual[key], f"{path}.{key}")
            if difference is not None:
                return difference
        return None
    if isinstance(expected, list):
        if len(expected) != len(actual):
            return {"path": path, "expected_length": str(len(expected)), "actual_length": str(len(actual))}
        for index, (left, right) in enumerate(zip(expected, actual, strict=True)):
            difference = first_difference(left, right, f"{path}[{index}]")
            if difference is not None:
                return difference
        return None
    if expected != actual:
        return {"path": path, "expected": repr(expected)[:1000], "actual": repr(actual)[:1000]}
    return None


def execute() -> dict[str, Any]:
    require(sha256(RESULT) == EXPECTED_RESULT_SHA256, "immutable v3 result hash mismatch")
    require(sha256(RUNNER) == EXPECTED_RUNNER_SHA256, "immutable v3 runner hash mismatch")
    expected = json.loads(RESULT.read_text(encoding="utf-8"))
    runner = load_runner()
    started = time.monotonic()
    actual = runner.execute()
    elapsed = time.monotonic() - started
    difference = first_difference(deterministic_projection(expected), deterministic_projection(actual))
    status = "SEMANTIC_REPLAY_MATCH" if difference is None else "SEMANTIC_REPLAY_MISMATCH"
    return {
        "artifact_id": "cycle-4-p1r-crr-finite-probe-v3-semantic-replay-v1",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "Deterministic replay only. It neither changes nor reruns the immutable result artifact and makes no continuous CRR claim.",
        "status": status,
        "immutable_inputs": {
            "result": {"path": str(RESULT.relative_to(ROOT)), "sha256": sha256(RESULT)},
            "runner": {"path": str(RUNNER.relative_to(ROOT)), "sha256": sha256(RUNNER)},
        },
        "comparison": {
            "excluded_variable_fields": ["resources.wall_seconds", "resources.peak_rss_bytes"],
            "all_other_fields_compared_exactly": True,
            "row_count": len(actual["rows"]),
            "unique_row_ids": len({row["id"] for row in actual["rows"]}),
            "status_counts": actual["status_counts"],
            "first_difference": difference,
        },
        "replay_resources": {"wall_seconds": elapsed, "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024},
        "harness": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "replay": {"check_command": "python3 discovery/replay_cycle_4_p1r_crr_finite_probe_v3_semantic_v1.py --check", "write_command": "python3 discovery/replay_cycle_4_p1r_crr_finite_probe_v3_semantic_v1.py --write"},
    }


def render(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def check() -> None:
    require(OUTPUT.is_file(), "semantic replay artifact is absent")
    data = json.loads(OUTPUT.read_text(encoding="utf-8"))
    require(data["immutable_inputs"]["result"]["sha256"] == sha256(RESULT), "semantic replay result pin mismatch")
    require(data["immutable_inputs"]["runner"]["sha256"] == sha256(RUNNER), "semantic replay runner pin mismatch")
    require(data["harness"]["sha256"] == sha256(SELF), "semantic replay harness pin mismatch")
    require(data["comparison"]["row_count"] == 160 and data["comparison"]["unique_row_ids"] == 160, "semantic replay row invariant mismatch")
    require(data["status"] in {"SEMANTIC_REPLAY_MATCH", "SEMANTIC_REPLAY_MISMATCH"}, "unknown semantic replay status")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write:
        require(not OUTPUT.exists(), "refusing to overwrite semantic replay artifact")
        payload = execute()
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
        print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
        return 0 if payload["status"] == "SEMANTIC_REPLAY_MATCH" else 2
    check()
    print(json.dumps({"artifact": OUTPUT.name, "check": "ok"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
