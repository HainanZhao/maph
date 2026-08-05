"""Immutable JSON sealing scaffold for the open-conjecture sweep."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path
import sys
from typing import Any, Callable


EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}


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


def freeze_inputs(root: Path, inputs: dict[str, tuple[Path, str]]) -> dict[str, dict[str, str]]:
    frozen = {}
    for label, (path, expected) in inputs.items():
        require(path.is_file(), f"missing frozen input: {label}")
        actual = sha256(path)
        require(actual == expected, f"frozen input hash mismatch: {label}")
        frozen[label] = {"path": str(path.relative_to(root)), "sha256": actual}
    return frozen


def render(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def run_cli(*, description: str, output: Path, payload_factory: Callable[[], dict[str, Any]]) -> int:
    parser = argparse.ArgumentParser(description=description)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = payload_factory()
    encoded = render(payload)
    if args.write:
        require(not output.exists(), f"refusing to overwrite {output.name}")
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("xb") as handle:
            handle.write(encoded)
    else:
        require(output.is_file(), f"{output.name} is absent")
        require(output.read_bytes() == encoded, f"{output.name} mismatch")
    print(json.dumps({"artifact": output.name, "status": payload["status"]}, sort_keys=True))
    return 0
