#!/usr/bin/env python3
"""Minimal read-only G0 replay successor ending at the hardened authority v3.

The v3 harness remains the complete fixed operational inventory.  This v4
successor first enforces runtime convention v2 without bare assertions, then
replays v3 and appends the optimization-robust authoritative v3 certificate.
It is an OBSERVED replay, not a new mathematical result or a new G0 decision.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from typing import Any, Final


ROOT: Final = Path(__file__).resolve().parents[1]
FROZEN: Final[dict[str, tuple[str, str]]] = {
    "runtime_v2": ("conventions/proof_runtime_v2.py", "d921965e2815f8fefa7877ba149f6147398e996cb889446d31e13383f9df4bd1"),
    "v3_harness": ("proof/run_g0_replay_v3.py", "4a8f54412264d5687fc847a6b08585286a9f55366445a7fdaf6d05366e7923c0"),
    "v3_reconciliation": ("proof/reconcile_g0_full_v3.py", "aac94af746f19cd34688633bf1998f82eb3ff092856d21d8f45d2ac3556a4ffa"),
    "v3_artifact": ("artifacts/g0-full-reconstruction-v3.json", "5a3ec153c843d0c89d9a987ad043cdf9513a171d581f98447a9c12930d26cc4f"),
}
# Direct v4 commands are deliberately tiny: v3 owns its sealed full inventory.
CHECKS: Final[tuple[tuple[str, tuple[str, ...]], ...]] = (
    ("g0-read-only-replay-harness-v3", ("proof/run_g0_replay_v3.py",)),
    ("g0-authoritative-full-reconstruction-v3", ("proof/reconcile_g0_full_v3.py", "--check")),
)
TIMING_MUTABLE_RAW_ARTIFACTS: Final[tuple[str, ...]] = (
    "artifacts/cycle-2-g0-per-route-resource-gate-performance-v1.json",
    "artifacts/g0-six-route-resource-gate-performance-v2.json",
)


def fail(message: str) -> None:
    raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    if spec is None or spec.loader is None:
        fail(f"cannot load pinned module: {relative}")
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def runtime_preflight() -> dict[str, object]:
    """Use v2's explicit RuntimeError checks before any legacy invocation."""
    relative, expected = FROZEN["runtime_v2"]
    if sha256(ROOT / relative) != expected:
        fail("G0 replay v4 runtime-v2 hash mismatch")
    runtime = load_module("g0_runtime_v2", relative).require_pinned_runtime()
    if runtime != {
        "implementation": "CPython", "version": "3.12.3", "optimize": 0,
        "json_policy": "stdlib json sort_keys=True; UTF-8; LF; trailing newline",
    }:
        fail("G0 replay v4 runtime-v2 convention returned unexpected values")
    return {**runtime, "runtime_convention_sha256": expected, "epistemic_status": "OBSERVED"}


def validate_static_configuration() -> None:
    identifiers = [identifier for identifier, _ in CHECKS]
    if identifiers != ["g0-read-only-replay-harness-v3", "g0-authoritative-full-reconstruction-v3"]:
        fail("v4 direct inventory is not the minimal v3 successor")
    arguments = tuple(argument for _, command in CHECKS for argument in command)
    if any(argument == "--write" or argument.startswith("--write-") for argument in arguments):
        fail("G0 replay v4 configuration contains a writer")
    if any(path in arguments for path in TIMING_MUTABLE_RAW_ARTIFACTS):
        fail("G0 replay v4 names a timing-mutable raw artifact")
    for label, (relative, expected) in FROZEN.items():
        if sha256(ROOT / relative) != expected:
            fail(f"G0 replay v4 frozen dependency changed: {label}")


def run() -> dict[str, Any]:
    runtime = runtime_preflight()
    validate_static_configuration()
    checks: list[dict[str, object]] = []
    for identifier, command in CHECKS:
        completed = subprocess.run((sys.executable, *command), cwd=ROOT,
                                   capture_output=True, text=True)
        if completed.returncode != 0:
            fail(json.dumps({"failed_check": identifier, "command": [sys.executable, *command], "stdout": completed.stdout, "stderr": completed.stderr}, sort_keys=True))
        checks.append({"id": identifier, "command": list(command), "epistemic_status": "OBSERVED"})
    return {
        "artifact_id": "g0-read-only-replay-harness-v4",
        "supersedes": "g0-read-only-replay-harness-v3 operationally; v1-v3 remain immutable historical harnesses",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "OBSERVED operational replay only: runtime-v2 explicitly enforced non-optimized CPython 3.12.3, the complete v3 inventory exited zero, and authoritative g0-full-v3 checked byte-for-byte. This adds no theorem and does not itself adjudicate G0.",
        "status": "PASS",
        "runtime_preflight": runtime,
        "checks": checks,
        "preserved_containment": "The v2 optimization-mode bypass remains in the sealed v2 hostile audit. V4 does not erase it; runtime v2 rejects -O/-OO before v3 or g0-full-v3 can run.",
        "excluded_timing_mutable_raw_artifacts": list(TIMING_MUTABLE_RAW_ARTIFACTS),
        "non_promotion": "Host-specific resource measurements remain OBSERVED operational evidence, and the published Guth--Maynard consequences remain reconstructed rather than newly proved.",
    }


def main() -> int:
    try:
        print(json.dumps(run(), sort_keys=True))
        return 0
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
