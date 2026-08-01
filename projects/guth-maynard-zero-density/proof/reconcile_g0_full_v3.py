#!/usr/bin/env python3
"""Optimization-robust authoritative successor to the corrected G0 v2."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/g0-full-reconstruction-v3.json"
FROZEN = {
    "v2_artifact": ("artifacts/g0-full-reconstruction-v2.json", "b6c9a8dbe3cff834f42dfa3afaed7650610211360a921a7731e894592cb1306f"),
    "v2_replay": ("proof/reconcile_g0_full_v2.py", "763f32a703abdf5ce19bc9dcfff4f169f4c5a63c9a611f0d775d7c10f62f4125"),
    "runtime_v2": ("conventions/proof_runtime_v2.py", "d921965e2815f8fefa7877ba149f6147398e996cb889446d31e13383f9df4bd1"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def runtime_module():
    spec = importlib.util.spec_from_file_location("g0_proof_runtime_v2", ROOT / FROZEN["runtime_v2"][0])
    require(spec is not None and spec.loader is not None, "cannot load pinned runtime module")
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def certificate() -> dict[str, Any]:
    runtime = runtime_module().require_pinned_runtime()
    hashes = {}
    for key, (relative, expected) in FROZEN.items():
        actual = sha256(ROOT / relative)
        require(actual == expected, f"G0 v3 frozen input changed: {relative}")
        hashes[key] = actual
    subprocess.run((sys.executable, "proof/reconcile_g0_full_v2.py", "--check"),
                   cwd=ROOT, check=True, capture_output=True, text=True)
    prior = json.loads((ROOT / FROZEN["v2_artifact"][0]).read_text())
    require(prior["decision"]["status"] == "PASS", "corrected G0 v2 is not PASS")
    require(prior["counts"]["resource_routes"] == 6, "corrected G0 v2 lacks six routes")
    require(prior["runtime"]["version"] == "3.12.3", "v2 runtime record changed")
    result = dict(prior)
    result.update({
        "artifact_id": "g0-full-reconstruction-v3",
        "certificate_version": 3,
        "supersedes": "g0-full-reconstruction-v2 as authoritative replay-hardening; v1-v2 remain preserved",
        "claim_boundary": "PROVED optimization-robust corrected adjudication that frozen G0 passes under the exact pinned runtime and cited published analytic inputs. This remains a reconstruction of published Guth--Maynard consequences, not a new theorem.",
        "runtime": runtime,
        "frozen_dependencies": hashes,
        "runtime_hardening_correction": {
            "status": "OBSERVED CORRECTION",
            "finding": "The v1 runtime convention and v2 reconciler used bare assertions, so an unauthorized standalone `python3 -O reconcile_g0_full_v2.py --check` could bypass their local assertions.",
            "containment": "V3 uses explicit RuntimeError checks and runtime v2 rejects optimization before invoking v2 under a fresh unoptimized CPython 3.12.3 subprocess. V2 remains valid only for its literal frozen `python3` command and is not the final authority.",
            "hostile_falsifier": "python3 -O proof/reconcile_g0_full_v3.py --check must exit nonzero with the optimization prohibition.",
        },
        "replay": {
            "script_sha256": sha256(Path(__file__)),
            "write_command": "python3 projects/guth-maynard-zero-density/proof/reconcile_g0_full_v3.py --write",
            "check_command": "python3 projects/guth-maynard-zero-density/proof/reconcile_g0_full_v3.py --check",
        },
    })
    return result


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = render(certificate())
    if args.write:
        OUTPUT.write_text(payload)
        return 0
    require(OUTPUT.is_file() and OUTPUT.read_text() == payload, "G0 v3 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "gate": "G0", "status": "PASS", "verified": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
