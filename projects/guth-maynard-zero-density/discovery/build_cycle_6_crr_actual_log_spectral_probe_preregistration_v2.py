#!/usr/bin/env python3
"""Seal the runner-hash correction for the actual-log spectral probe."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-6-crr-actual-log-spectral-probe-preregistration-v2.json"
V1_ARTIFACT = ROOT / "artifacts/cycle-6-crr-actual-log-spectral-probe-preregistration-v1.json"
V1_BUILDER = ROOT / "discovery/build_cycle_6_crr_actual_log_spectral_probe_preregistration_v1.py"
RUNNER = ROOT / "discovery/run_cycle_6_crr_actual_log_spectral_probe_v1.py"
CONVENTIONS = ROOT / "conventions/crr_actual_log_spectral_probe_v1.py"
DOCUMENT = ROOT / "docs/cycle-6-crr-actual-log-spectral-probe-preregistration-v2-correction.md"
V1_HASH = "7fa06dee91982d1c74cf29c40093f6eb21cf243a2f985a30f5df45a2627ba512"
RUNNER_HASH = "9591e287e7ff879449bf7091615520f406d56fc01bdbcd1884a57019ef26661f"
CONVENTIONS_HASH = "d15cb5a290236823a657227d28e43c7d530fdd3a92a7c38f6a584e0c5db92bca"
EXPECTED_RUNTIME = {
    "implementation": "CPython",
    "python": "3.12.3",
    "numpy": "1.26.4",
    "optimization_level": 0,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(path: Path, label: str):
    spec = importlib.util.spec_from_file_location(label, path)
    require(spec is not None and spec.loader is not None, f"cannot load module: {label}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def runtime_metadata() -> dict[str, Any]:
    import numpy as np

    result = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "optimization_level": sys.flags.optimize,
    }
    require(result == EXPECTED_RUNTIME, "actual-log spectral preregistration v2 requires non-optimized CPython 3.12.3 and NumPy 1.26.4")
    return result


def validate_v1() -> dict[str, Any]:
    require(V1_ARTIFACT.is_file() and sha256(V1_ARTIFACT) == V1_HASH, "v1 preregistration hash mismatch")
    builder = load_module(V1_BUILDER, "crr_actual_log_spectral_prereg_v1")
    require(V1_ARTIFACT.read_bytes() == builder.render(builder.seal()), "v1 preregistration byte replay mismatch")
    v1 = json.loads(V1_ARTIFACT.read_text(encoding="utf-8"))
    require(v1["status"] == "SEALED_DISCOVERY_PREREGISTRATION_EXECUTABLE", "v1 preregistration status mismatch")
    return v1


def frozen_inputs() -> dict[str, dict[str, str]]:
    inputs = {
        "v1_preregistration": (V1_ARTIFACT, V1_HASH),
        "v1_builder": (V1_BUILDER, ""),
        "runner": (RUNNER, RUNNER_HASH),
        "conventions": (CONVENTIONS, CONVENTIONS_HASH),
        "document": (DOCUMENT, ""),
    }
    result: dict[str, dict[str, str]] = {}
    for label, (path, expected) in inputs.items():
        require(path.is_file(), f"missing frozen input: {label}")
        actual = sha256(path)
        if expected:
            require(actual == expected, f"frozen input hash mismatch: {label}")
        result[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual}
    return result


def seal() -> dict[str, Any]:
    v1 = validate_v1()
    frozen = frozen_inputs()
    return {
        "artifact_id": "cycle-6-crr-actual-log-spectral-probe-preregistration-v2",
        "epistemic_status": "CONJECTURED",
        "status": "SEALED_DISCOVERY_PREREGISTRATION_EXECUTABLE",
        "claim_boundary": "V2 is a runner-hash correction to a three-row bounded actual-log discovery protocol. It proves no continuous CRR compatibility/incompatibility statement, AFARI/FARI result, extremizer, saturation theorem, density theorem, or short-interval consequence. A hit is OBSERVED and a miss is not a universal negative.",
        "runtime": runtime_metadata(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen,
        "correction": {
            "preserves_v1": True,
            "v1_sha256": V1_HASH,
            "v1_status": "CONTAINED_PRE_RUNNER_HASH",
            "defect": "v1 was sealed before the executable runner path/hash was frozen",
            "repair": "v2 freezes the runner path/hash and resource-cap control flow before any row execution",
            "result_consulted": False,
            "scientific_parameters_changed": False,
        },
        "research_stage_review_policy": v1["research_stage_review_policy"],
        "context": v1["context"],
        "frozen_rows": v1["frozen_rows"],
        "row_schedule": v1["row_schedule"],
        "common_object_rule": v1["common_object_rule"],
        "actual_labels": v1["actual_labels"],
        "iteration": v1["iteration"],
        "retention": v1["retention"],
        "resources": v1["resources"],
        "numerics": v1["numerics"],
        "runner_control": {
            "path": str(RUNNER.relative_to(ROOT)),
            "sha256": RUNNER_HASH,
            "write_rule": "The runner verifies this v2 artifact, its own hash, and the conventions hash before executing; it refuses to overwrite a result artifact.",
            "check_rule": "The runner recomputes semantic fields and excludes only observed wall/RSS fields from byte comparison.",
        },
        "replay": {
            "write_command": "python3 discovery/build_cycle_6_crr_actual_log_spectral_probe_preregistration_v2.py --write",
            "check_command": "python3 discovery/build_cycle_6_crr_actual_log_spectral_probe_preregistration_v2.py --check",
            "runner_write_command": "python3 discovery/run_cycle_6_crr_actual_log_spectral_probe_v1.py --write",
            "runner_check_command": "python3 discovery/run_cycle_6_crr_actual_log_spectral_probe_v1.py --check",
        },
    }


def render(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = seal()
    if args.write:
        require(not OUTPUT.exists(), "refusing to overwrite actual-log spectral preregistration v2")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "actual-log spectral preregistration v2 is absent")
        require(OUTPUT.read_bytes() == render(payload), "actual-log spectral preregistration v2 mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
