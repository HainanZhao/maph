#!/usr/bin/env python3
"""Seal Cycle 59 trigger-surplus to recurrence ledger."""
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
OUTPUT = ROOT / "artifacts/cycle-59-trigger-to-recurrence-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-59-trigger-to-recurrence-preregistration-v1.md", "a04a68b7d4c69d9645672535f05c736c55246f4d43f6d507b49301348d3e4b7e"),
    "document": (ROOT / "docs/cycle-59-trigger-to-recurrence-v1.md", "745290e96623e4952323c91c79fe9068317e3b4f5a1f2fd89384805c0580366f"),
    "conventions": (ROOT / "conventions/trigger_to_recurrence_v1.py", "4b722ed091ba71eca9397ff6f40fe4ac011ff17dc3edcc37e20d09572e97656d"),
    "tests": (ROOT / "tests/test_cycle_59_trigger_to_recurrence_v1.py", "2abddee6b01212db750f8ad6edb3c2eaabc2668db8a92bb64c229d9cc91a8f86"),
    "cycle58": (ROOT / "artifacts/cycle-58-strict-hybrid-margin-correction-v1.json", "0bde0caa82cda62b8a61af9902e6eecc00d89442d41779826bb52a59e6a3dcef"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 59 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("trigger_to_recurrence_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 59 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["target_rows"]["required_surplus_open_endpoint"] == Fraction(7, 10), "target surplus")
    require(rows["uniform_rows"]["required_surplus_open_endpoint"] == Fraction(43, 50), "uniform surplus")
    require(rows["hybrid_total_saving_for_target_7_50_open"] == Fraction(19, 25), "target total saving")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle58"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_STRICT_GT_3_50_OR_ENDPOINT_MARGIN_REQUIRED", "Cycle 58 status mismatch")
    return {"prior_role": "translate the strict trigger surplus into popular-correlation strength"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-59-trigger-to-recurrence-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_DIRECT_RESTRICTION_OR_GRAPH_AMPLIFICATION_OPEN",
        "claim_boundary": "This artifact proves a conditional exponent interface only. It does not prove a cumulant estimate, graph amplification, AMPR, density, or interval gains.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "trigger_recurrence_boundary": {
            "epistemic_status": "PROVED",
            "statement": "A trigger surplus mu generically forces correlation deficit eta only for eta>r-mu; eta=7/50 needs mu>7/10 at r=21/25 and mu>43/50 uniformly for r<=1.",
        },
        "analytic_fork": {
            "epistemic_status": "CONJECTURED",
            "statement": "Either prove the complete Hilbert edge-cumulant restriction directly or add a prime-specific graph amplification before Cycle 52 recurrence extraction.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_59_trigger_to_recurrence_v1.py --write",
            "check_command": "python3 proof/build_cycle_59_trigger_to_recurrence_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_59_trigger_to_recurrence_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 59 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 59 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 59 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
