#!/usr/bin/env python3
"""Seal Cycle 21 v2 weighted-continuum correction."""
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
OUTPUT = ROOT / "artifacts/cycle-21-continuum-volume-correction-v2.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-21-continuum-volume-correction-preregistration-v2.md", "c9b8b197d016a6d44bb3c53e957e52f984238dae7a15f05062e1e37bb5fb135c"),
    "document": (ROOT / "docs/cycle-21-continuum-volume-correction-v2.md", "d56db8a1768d654138232fa835be19d602326ea739be6ef44664aa7c46a6ae45"),
    "conventions": (ROOT / "conventions/weighted_continuum_volume_v2.py", "eba4b266607d5921182421444647d7cf2052ac59c7f0eacaf4d207640b3a4f61"),
    "tests": (ROOT / "tests/test_cycle_21_continuum_volume_correction_v2.py", "5aa77132ca43e842105778a358b01338173f71312088c1cec1618b2b57636eac"),
    "superseded_v1_artifact": (ROOT / "artifacts/cycle-21-continuum-volume-v1.json", "ed5f391adb5d767ec5c769043ea884633d09d65192057af8995104032dfdd391"),
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
    runtime = {"implementation": platform.python_implementation(), "python": platform.python_version(), "optimization_level": sys.flags.optimize}
    require(runtime == EXPECTED_RUNTIME, "Cycle 21 v2 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("weighted_continuum_volume_v2", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 21 v2 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["critical_exponents"]["volume_collapse_scale"] == Fraction(6, 25), "volume exponent changed")
    require(rows["finite_weighted_check"]["weighted_row_sum"] == Fraction(1, 8), "weighted constant mismatch")
    return rows


def validate_v1() -> dict[str, str]:
    prior = json.loads(INPUTS["superseded_v1_artifact"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_CONTINUUM_VOLUME_THEOREM_PRIME_OPERATOR_QUADRATURE_OPEN", "v1 status mismatch")
    return {
        "affected_claim": "uniform log measure was used as the strategic prime reference frame",
        "unaffected_claim": "the v1 uniform continuous-frame theorem and its explicit conditional implication remain valid",
        "correction": "replace uniform dy by e^y dy on [0,log 2]",
    }


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-21-continuum-volume-correction-v2",
        "epistemic_status": "PROVED",
        "status": "SEALED_WEIGHTED_CONTINUUM_CORRECTION_PRIME_OPERATOR_QUADRATURE_OPEN",
        "claim_boundary": "This correction supplies the natural weighted prime continuum reference and preserves the exponent bridge. It does not prove the prime operator discrepancy, the skeleton target, a density improvement, or an interval result.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "correction_record": {"epistemic_status": "OBSERVED", **validate_v1()},
        "weighted_continuum": {
            "epistemic_status": "PROVED",
            "reference_measure": "e^y dy on [0,log 2]",
            "kernel": "(2^(1-ih)-1)/(1-ih)",
            "row_sum_bound": "6H_(k-1)/Delta",
        },
        "prime_perturbation": {
            "epistemic_status": "PROVED",
            "conditional_statement": "If ||H_P-H_nu||_op=o(X^(-3/5)) after log-squared coloring, the weighted determinant lower bound contradicts Cycle 20.",
            "analytic_input_status": "CONJECTURED_OPEN",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_json(rows),
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_21_continuum_volume_correction_v2.py --write",
            "check_command": "python3 proof/build_cycle_21_continuum_volume_correction_v2.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_21_continuum_volume_correction_v2.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 21 v2 correction artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 21 v2 correction artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 21 v2 correction artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
