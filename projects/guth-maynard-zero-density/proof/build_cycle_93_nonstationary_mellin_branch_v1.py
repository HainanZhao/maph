#!/usr/bin/env python3
"""Seal Cycle 93 strict sub-alias nonstationary branch closure."""
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
OUTPUT = ROOT / "artifacts/cycle-93-nonstationary-mellin-branch-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "discovery_candidate": (ROOT / "discovery/cycle-93-nonstationary-branch-candidate-v1.md", "bb6a2c7e26981edf1b68ba00a4bee10dad10f48bf8fdd3e40fa107ec2e17ec8e"),
    "preregistration": (ROOT / "docs/cycle-93-nonstationary-branch-preregistration-v1.md", "b121c55f2fe4da8b840f8658f8dd75298a4f39a5d9f2abb2324b979f31a073a1"),
    "document": (ROOT / "docs/cycle-93-nonstationary-mellin-branch-v1.md", "26e906cbe3b8350355c6fb20bf561c17f52179fcb9e694f8bfb641cc3fb7b887"),
    "conventions": (ROOT / "conventions/nonstationary_mellin_branch_v1.py", "f306904bb79b2256a8a16af47d0a6e861d9776d8f12bbd3b34a8bc5266528d30"),
    "tests": (ROOT / "tests/test_cycle_93_nonstationary_mellin_branch_v1.py", "3f0f425934871ff5c08ad44aff4f9f758005332e9b3448837c420b5ba956ac12"),
    "cycle87": (ROOT / "artifacts/cycle-87-mellin-alias-atlas-v1.json", "68b88ccd4ce3e5371906e3b0da3c254056b79bad9504880ebbff04b9cebce8ca"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_runtime() -> dict[str, Any]:
    runtime = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
    }
    require(runtime == EXPECTED_RUNTIME, "Cycle 93 requires non-optimized CPython 3.12.3")
    return runtime


def frozen_inputs() -> dict[str, dict[str, str]]:
    result = {}
    for label, (path, expected) in INPUTS.items():
        require(path.is_file(), f"missing frozen input: {label}")
        actual = sha256(path)
        require(actual == expected, f"frozen input hash mismatch: {label}")
        result[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual}
    return result


def load_rows() -> dict[str, object]:
    path = INPUTS["conventions"][0]
    spec = importlib.util.spec_from_file_location("nonstationary_mellin_branch_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 93 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["kernel_decay"] == "for every A, O_A(K*D^-A)", "kernel decay")
    require("O_B(X^-B)" in rows["full_branch"], "full branch")
    require("remain open" in rows["open_transition"], "open transition")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle87"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_MELLIN_ALIAS_TRICHOTOMY_BOUND_OR_WEB_OPEN", "Cycle 87 status mismatch")
    return {"cycle87_role": "supply the sub-alias height range and crossed Mellin phase"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-93-nonstationary-mellin-branch-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_STRICT_SUB_ALIAS_POWER_NEGLIGIBLE_TRANSITION_AND_ALIASES_OPEN",
        "claim_boundary": "This artifact proves arbitrary power decay only on the strict buffered sub-alias branch. The transition, stationary aliases, equal-height analytic bound, full moment, density gain, and interval gain remain open.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "nonstationary_closure": {
            "epistemic_status": "PROVED",
            "statement": "For every fixed B, the complete strict branch 0<|Delta h|<=c_*K/D contributes O_B(X^-B) after all support sums.",
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Handle the transition |Delta h|~K/D and all stationary integer aliases, while routing equal-height excess through the Cycle-92 ray web.",
        },
        "exact_replay": rows,
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_93_nonstationary_mellin_branch_v1.py --write",
            "check_command": "python3 proof/build_cycle_93_nonstationary_mellin_branch_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_93_nonstationary_mellin_branch_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 93 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 93 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 93 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

