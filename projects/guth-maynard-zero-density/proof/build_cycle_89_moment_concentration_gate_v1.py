#!/usr/bin/env python3
"""Seal Cycle 89 moment-concentration inverse gate."""
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
OUTPUT = ROOT / "artifacts/cycle-89-moment-concentration-gate-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-89-moment-concentration-preregistration-v1.md", "cae9f500858d2ededd96171b6fa25f8e39dfe478b73c1220045ba36902cd9e24"),
    "document": (ROOT / "docs/cycle-89-moment-concentration-gate-v1.md", "e0e7804db6648de42910626b166b38c81e152c4e0431535c9af96ed3fdd60ee0"),
    "conventions": (ROOT / "conventions/moment_concentration_gate_v1.py", "5df7b73affba0aecd5820d3afd2968759c97188268aea0a50988b8e6605496b6"),
    "tests": (ROOT / "tests/test_cycle_89_moment_concentration_gate_v1.py", "a11dfcbee47b0364f9b018247cbf33ac18f6698808a0345ff8fceb36b4cc9a37"),
    "cycle86": (ROOT / "artifacts/cycle-86-signed-regime-split-v1.json", "4d6f78f433b052c6d3497d46d67b015d6963fe67f862e0d6c52124c6d26a3dd4"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 89 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("moment_concentration_gate_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 89 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["forced_excess"] == "2xi-116/75+2delta", "forced excess mismatch")
    require(rows["ceiling_excess"] == "2/3", "ceiling excess mismatch")
    return rows


def validate_priors() -> dict[str, str]:
    cycle86 = json.loads(INPUTS["cycle86"][0].read_text(encoding="utf-8"))
    cycle87 = json.loads(INPUTS["cycle87"][0].read_text(encoding="utf-8"))
    require(cycle86.get("status") == "SEALED_SIGNED_REGIME_SPLIT_MOMENT_AND_LARGE_VALUES_OPEN", "Cycle 86 status mismatch")
    require(cycle87.get("status") == "SEALED_MELLIN_ALIAS_TRICHOTOMY_BOUND_OR_WEB_OPEN", "Cycle 87 status mismatch")
    return {
        "cycle86_role": "supply atom exponent, raw target, split, and ceiling",
        "cycle87_role": "supply explicit alias coordinates for a future inverse theorem",
    }


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-89-moment-concentration-gate-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_MOMENT_CONCENTRATION_OR_SATURATION_INVERSE_OPEN",
        "claim_boundary": "This artifact proves an exact Holder reduction and exponent gate. It proves no second- or fourth-moment estimate, large-value theorem, Fourier-band closure, density gain, or interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_priors()},
        "reduction": {
            "epistemic_status": "PROVED",
            "statement": "M2<=L1^(2/3)M4^(1/3), so conditional diagonal-size M2 and the raw L1 target force M4 exponent at least 3xi+8/25 and excess 2xi-116/75 above K(DQ)^2.",
        },
        "inverse_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Classify the forced fourth-moment excess through the Cycle-87 Mellin alias atlas, or prove it arithmetically impossible.",
        },
        "exact_replay": rows,
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_89_moment_concentration_gate_v1.py --write",
            "check_command": "python3 proof/build_cycle_89_moment_concentration_gate_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_89_moment_concentration_gate_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 89 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 89 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 89 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

