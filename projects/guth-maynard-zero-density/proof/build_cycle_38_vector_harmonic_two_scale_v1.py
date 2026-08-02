#!/usr/bin/env python3
"""Seal Cycle 38 vector-harmonic collision and two-scale lift."""
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
OUTPUT = ROOT / "artifacts/cycle-38-vector-harmonic-two-scale-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-38-vector-harmonic-two-scale-preregistration-v1.md", "17b17e2abbbe06658fe5f7bb1919d74762753f680577e6942926c5aaa54cde52"),
    "document": (ROOT / "docs/cycle-38-vector-harmonic-two-scale-v1.md", "5ad47bd90c2cc67f275818362f3ee1c2b8ee4245d83530b143cae3cc9a782a59"),
    "conventions": (ROOT / "conventions/vector_harmonic_two_scale_v1.py", "f064e52a7dd405c182692834f500a820bbc36f4ad222c11bef5a8fe38021809b"),
    "tests": (ROOT / "tests/test_cycle_38_vector_harmonic_two_scale_v1.py", "d3167e64d25a56b5564a72382a2175f427d907e0a46c7a3e01110d9b32f30b49"),
    "cycle37": (ROOT / "artifacts/cycle-37-excess-harmonic-routing-v1.json", "4877fa4480dd6834253be58be82f981f2600002f9c385079acbccd288fc7dd43"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_json(value: Any) -> Any:
    if isinstance(value, Fraction):
        return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    if isinstance(value, tuple):
        return [exact_json(item) for item in value]
    if isinstance(value, dict):
        return {str(key): exact_json(item) for key, item in value.items()}
    return value


def check_runtime() -> dict[str, Any]:
    runtime = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
    }
    require(runtime == EXPECTED_RUNTIME, "Cycle 38 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("vector_harmonic_two_scale_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 38 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["registered_scales"]["geometry"]["collision_multiplicity"] == Fraction(3, 10), "collision exponent")
    require(rows["registered_scales"]["r2_energy"]["target_vector_bound"] == Fraction(91, 25), "r2 target")
    require(rows["prime_monomial"]["coefficient_square_norm"] == "M^2", "monomial norm")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle37"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_ENTROPY_EXCESS_ARBITRARY_HARMONIC_HIDING_VECTOR_ROUTE_OPEN", "Cycle 37 status mismatch")
    return {"prior_role": "retain the Cycle 37 full harmonic vector without scalar colour selection"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-38-vector-harmonic-two-scale-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_VECTOR_RESCALING_COLLISION_TWO_SCALE_PRIME_MONOMIAL_OPEN",
        "claim_boundary": "This artifact proves exact collision, injectivity, norm, and conditional vector-energy ledgers. It does not prove the required vector mean value, transfer all entropy excess to actual harmonic energy, close the kernel count, improve density, or improve intervals.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "collision_boundary": {
            "epistemic_status": "PROVED",
            "statement": "A Delta-separated rescaling fan has A pairs (t_m,m) with one common mt; at A=X^(3/10) flattening loses more than 4/25.",
        },
        "two_scale_lift": {
            "epistemic_status": "PROVED",
            "statement": "For m>=2, K(t)K(mt) has M^2 injectively labelled coefficients p*q^m and exact coefficient-square norm M^2.",
        },
        "analytic_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Bound the vector sum of |K(t)K(mt)|^2 at X^(91/25+o(1)) or X^(76/25+o(1)) under the corresponding actual harmonic-energy branch without using ambient X^(m+1).",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_json(rows),
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_38_vector_harmonic_two_scale_v1.py --write",
            "check_command": "python3 proof/build_cycle_38_vector_harmonic_two_scale_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_38_vector_harmonic_two_scale_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 38 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 38 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 38 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
