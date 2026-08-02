#!/usr/bin/env python3
"""Seal Cycle 48 Huxley--Sargos joint-sieve threshold ledger."""
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
OUTPUT = ROOT / "artifacts/cycle-48-hs-joint-sieve-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-48-hs-joint-sieve-preregistration-v1.md", "649d0e2d3f8abb927f5d7b1a537282aee672f51ac23f4a0148a895051bc42230"),
    "document": (ROOT / "docs/cycle-48-hs-joint-sieve-v1.md", "592a930c156aaaf3fcc10b8133a38585e2955af12cbb3b5bb7968810ec1c5f2d"),
    "conventions": (ROOT / "conventions/hs_joint_sieve_v1.py", "294bf8cd626511791273a0efa037cfdfc5f9d6e28c8bc75755f2edc08ff77c0c"),
    "tests": (ROOT / "tests/test_cycle_48_hs_joint_sieve_v1.py", "43a431e82ef991dd3638105d66a85173f6c2093629d2ace2b482fb0da245f31c"),
    "cycle47": (ROOT / "artifacts/cycle-47-near-curve-gap-v1.json", "209dd38186cefbfad2f286b1fbc6400745425fb6fc8555bd8e06ac5547174a55"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 48 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("hs_joint_sieve_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 48 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["endpoint"]["saving"] == Fraction(7, 50), "endpoint saving")
    require(rows["comparisons"]["gap_to_full_missing"] == Fraction(1, 50), "full gap")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle47"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_HUXLEY_SARGOS_8_25_LOG_MAJOR_ARC_GAP_1_25", "Cycle 47 status mismatch")
    return {"prior_role": "insert the proved X^(8/25) wrap count into the full two-term joint large-sieve ledger"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-48-hs-joint-sieve-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_AUXILIARY_S4_MARGIN_7_50_LCAM4_BRIDGE_OPEN",
        "claim_boundary": "This artifact proves auxiliary joint-sum saving 7/50. It does not prove LCAM_4, a density estimate, or an interval theorem.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "threshold_event": {
            "epistemic_status": "PROVED",
            "statement": "The checked near-curve wrap count improves the joint saving from 2/25 to exactly 7/50, matching the Cycle 39 s=4 auxiliary margin and remaining 1/50 below 4/25.",
        },
        "bridge_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Restore the complete LCAM_4 off-diagonal expansion with only subpower loss, or save the residual power in logarithmic major arcs/nonlattice rows.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_48_hs_joint_sieve_v1.py --write",
            "check_command": "python3 proof/build_cycle_48_hs_joint_sieve_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_48_hs_joint_sieve_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 48 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 48 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 48 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
