#!/usr/bin/env python3
"""Seal Cycle 65 depth-refined logarithmic packet ledger."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-65-depth-packet-ledger-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-65-depth-packet-preregistration-v1.md", "8ac12435ed50fd894126764b1580d5c53a87354e139d2b34ce493a22db799327"),
    "document": (ROOT / "docs/cycle-65-depth-packet-v1.md", "a6c8d3356417b140f72c1edfd9607d8b807efd47a71e4a2e6d7b619c03a32b6d"),
    "conventions": (ROOT / "conventions/depth_packet_ledger_v1.py", "bb13f7c1a325cba90bef813873da459d149d6b1c203cd40d0b2af33fc00dac9e"),
    "tests": (ROOT / "tests/test_cycle_65_depth_packet_ledger_v1.py", "5d4f11d5bb21c5d4c128763cef95f06fa2cc4b03f3103a2b2b132296b0ed5b61"),
    "cycle64": (ROOT / "artifacts/cycle-64-farey-packet-transport-v1.json", "60a78bc81f2916e594221a1258a35024b96e67ecf5d2af6bc9a53731d1cdc76f"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_json(value: Any) -> Any:
    if isinstance(value, Fraction):
        return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    if isinstance(value, dict):
        return {str(key): exact_json(item) for key, item in value.items()}
    return value


def check_runtime() -> dict[str, Any]:
    runtime = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
    }
    require(runtime == EXPECTED_RUNTIME, "Cycle 65 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("depth_packet_ledger_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 65 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    constants = rows["constants"]
    require(constants["dangerous_depth_threshold"] == Fraction(6, 25), "depth threshold")
    require(constants["deep_packet_denominator_threshold"] == Fraction(1, 5), "denominator threshold")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle64"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_LOG_FAREY_PACKET_MASS_OR_LOW_DENOMINATOR_RECURRENCE_OPEN", "Cycle 64 status mismatch")
    return {"prior_role": "refine the harmonic packet envelope by retaining multiplicative depth"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-65-depth-packet-ledger-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_LOG_DEPTH_PACKET_DISCREPANCY_OR_X6_25_AP_RECURRENCE_OPEN",
        "claim_boundary": "This artifact proves an exact depth-weighted exponent ledger. It does not prove packet discrepancy, recurrence, powered, LCAM, density, or interval gains.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "depth_reduction": {
            "epistemic_status": "PROVED",
            "statement": "At q=X^theta and depth K=X^kappa, packet weight has exponent 11/25+kappa and sufficient packet count is strictly below X^(6/25-kappa).",
        },
        "threshold_interface": {
            "epistemic_status": "PROVED",
            "statement": "One packet reaches the pair target only at depth at least X^(6/25), possible only for denominator at most X^(1/5); strict versions require strict margins.",
        },
        "analytic_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Prove depth-packet discrepancy on shallow scales or route an X^(6/25)-deep low-denominator packet to arithmetic-progression recurrence with approximation error retained.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_65_depth_packet_ledger_v1.py --write",
            "check_command": "python3 proof/build_cycle_65_depth_packet_ledger_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_65_depth_packet_ledger_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 65 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 65 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 65 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
