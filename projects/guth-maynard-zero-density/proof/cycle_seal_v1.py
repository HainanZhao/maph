"""Shared immutable sealing scaffold for proof cycles.

Breaking changes must create ``cycle_seal_v2.py`` so artifacts frozen against
this module remain replayable.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
from typing import Any, Callable


EXPECTED_RUNTIME = {
    "implementation": "CPython",
    "python": "3.12.3",
    "optimization_level": 0,
}
FrozenInputs = dict[str, tuple[Path, str]]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_runtime(label: str) -> dict[str, Any]:
    runtime = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
    }
    require(runtime == EXPECTED_RUNTIME, f"{label} runtime mismatch")
    return runtime


def freeze_inputs(root: Path, inputs: FrozenInputs) -> dict[str, dict[str, str]]:
    result = {}
    for label, (path, expected) in inputs.items():
        require(path.is_file(), f"missing frozen input: {label}")
        actual = sha256(path)
        require(actual == expected, f"frozen input hash mismatch: {label}")
        result[label] = {"path": str(path.relative_to(root)), "sha256": actual}
    return result


def load_record(
    *, root: Path, path: Path, module_name: str, factory: str = "theorem_record"
) -> dict[str, object]:
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    spec = importlib.util.spec_from_file_location(module_name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {module_name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    producer = getattr(module, factory, None)
    require(callable(producer), f"missing callable {factory} in {module_name}")
    record = producer()
    require(isinstance(record, dict), f"{module_name}.{factory} did not return a dict")
    return record


def validate_prior(path: Path, expected_status: str) -> dict[str, Any]:
    prior = json.loads(path.read_text(encoding="utf-8"))
    require(prior.get("status") == expected_status, "prior artifact status mismatch")
    return prior


def render(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def run_cli(
    *, description: str, output: Path, payload_factory: Callable[[], dict[str, Any]]
) -> int:
    parser = argparse.ArgumentParser(description=description)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = payload_factory()
    encoded = render(payload)
    if args.write:
        require(not output.exists(), f"refusing to overwrite {output.name}")
        with output.open("xb") as handle:
            handle.write(encoded)
    else:
        require(output.is_file(), f"{output.name} is absent")
        require(output.read_bytes() == encoded, f"{output.name} mismatch")
    print(json.dumps({"artifact": output.name, "status": payload["status"]}, sort_keys=True))
    return 0
