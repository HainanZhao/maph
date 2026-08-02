#!/usr/bin/env python3
"""Seal Cycle 47 near-curve comparison and geometric correction."""
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
OUTPUT = ROOT / "artifacts/cycle-47-near-curve-gap-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-47-near-curve-gap-preregistration-v1.md", "df50cbc94f934ce5dbe4a3d02a82555ab820e9deecd3b4bd14e86ba4dde867a0"),
    "document": (ROOT / "docs/cycle-47-near-curve-gap-v1.md", "172f58979533941ae9ce77b67f97cd3cb67475309ae6cacd84d4dcf05fbaeced"),
    "conventions": (ROOT / "conventions/near_curve_gap_v1.py", "c7c46473b81ff274c3af2ab1a8ee8cd900a55b3ed1fef8b34f46e2558b329f8d"),
    "tests": (ROOT / "tests/test_cycle_47_near_curve_gap_v1.py", "8fc923f27c0bbe55ac524502819521d2e04c3e7f82b23172526b78668df7c822"),
    "cycle46": (ROOT / "artifacts/cycle-46-inverse-wrap-curvature-v1.json", "1917dc4886fc65333e4a7933b582a80344c208a8e7ff13b34493f98d9d512d64"),
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
    if isinstance(value, list):
        return [exact_json(item) for item in value]
    return value


def check_runtime() -> dict[str, Any]:
    runtime = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
    }
    require(runtime == EXPECTED_RUNTIME, "Cycle 47 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("near_curve_gap_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 47 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["best_huxley_sargos"]["bound"] == Fraction(8, 25), "best exponent")
    require(rows["huxley_sargos_gap"] == Fraction(1, 25), "gap")
    require(rows["geometry"]["euclidean_curvature"] == Fraction(-19, 25), "curvature")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle46"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_INVERSE_LOG_CURVE_RECIPROCAL_CURVATURE_OPEN", "Cycle 46 status mismatch")
    return {"prior_role": "correct the geometric terminology and compare ILC with checked near-curve theorems"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-47-near-curve-gap-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_HUXLEY_SARGOS_8_25_LOG_MAJOR_ARC_GAP_1_25",
        "claim_boundary": "This artifact proves the checked near-curve exponent comparison and geometric correction. It does not prove LMAS, LCAM_s, density, or interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "near_curve_input": {
            "epistemic_status": "PROVED",
            "statement": "The checked Huxley--Sargos theorem gives X^(8/25+o(1)) at order three, missing the X^(7/25+o(1)) alias target by X^(1/25).",
        },
        "correction": {
            "epistemic_status": "PROVED",
            "statement": "Cycle 46's X^(-7/25) is graph second derivative; Euclidean curvature is X^(-19/25), normal tube width is X^(-1), and the generic curvature count is X^(26/75+o(1)).",
        },
        "analytic_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Save X^(1/25) in the logarithmic order-three major-arc term, or prove nonlattice row decay.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_47_near_curve_gap_v1.py --write",
            "check_command": "python3 proof/build_cycle_47_near_curve_gap_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_47_near_curve_gap_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 47 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 47 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 47 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
