#!/usr/bin/env python3
"""Seal Cycle 21 continuum-volume theorem and prime discrepancy gate."""
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
OUTPUT = ROOT / "artifacts/cycle-21-continuum-volume-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-21-continuum-volume-preregistration-v1.md", "301a4ed42e7528ab19821085d493d92c74ac58c81524f4eee95b124118e6f82e"),
    "document": (ROOT / "docs/cycle-21-continuum-volume-v1.md", "f276d1b2c9c6eb272815eb4204f34ca80fff660b72761052d96a90d009c50d42"),
    "conventions": (ROOT / "conventions/continuum_volume_v1.py", "0c1adb0d678d6bdc7a9f3c5bb2c04ff73c56d5d1b6e9f338494c12d74df57520"),
    "tests": (ROOT / "tests/test_cycle_21_continuum_volume_v1.py", "45b3e3cac09b80f06a6aac6178d59fd139db061ed9c5f642e9736faaf543c90e"),
    "cycle20": (ROOT / "artifacts/cycle-20-exterior-volume-v1.json", "5d647c7ccd850cdae77cb04bb5287d175cb210f1d546ab5f5341b50c4f185b5c"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 21 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("continuum_volume_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 21 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    critical = rows["critical_exponents"]
    finite = rows["finite_frame_check"]
    require(critical["volume_collapse_scale"] == Fraction(6, 25), "volume scale mismatch")
    require(critical["required_prime_operator_discrepancy"] == "o(X^(-3/5))", "prime discrepancy mismatch")
    require(finite["total_error"] == Fraction(1, 6), "finite perturbation mismatch")
    return rows


def validate_cycle20() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle20"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_SHARP_EXTERIOR_VOLUME_COLLAPSE_PRIME_DETERMINANT_LOWER_BOUND_OPEN", "Cycle 20 status mismatch")
    require(prior["exterior_volume"]["critical_log_collapse_scale"] == "-X^(6/25+o(1))", "Cycle 20 collapse mismatch")
    return {"cycle20_role": "sharp determinant upper bound to contradict"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-21-continuum-volume-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_CONTINUUM_VOLUME_THEOREM_PRIME_OPERATOR_QUADRATURE_OPEN",
        "claim_boundary": "This artifact proves a continuous-frame determinant lower bound and a conditional prime operator-discrepancy bridge. It does not prove that discrepancy for primes, the skeleton target, a density improvement, or an interval result.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_cycle20()},
        "continuum_frame": {
            "epistemic_status": "PROVED",
            "statement": "For Delta-separated log-frequency rows, det(H_0)>=(1-4H_(k-1)/(B Delta))^k whenever the bracket is positive.",
        },
        "prime_perturbation": {
            "epistemic_status": "PROVED",
            "conditional_statement": "If eta_C=||H_P-H_0||_op=o(X^(-3/5)) after log-squared coloring, the prime determinant lower bound contradicts Cycle 20 and yields the target skeleton bound.",
            "analytic_input_status": "CONJECTURED_OPEN",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_json(rows),
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_21_continuum_volume_v1.py --write",
            "check_command": "python3 proof/build_cycle_21_continuum_volume_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_21_continuum_volume_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 21 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 21 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 21 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
