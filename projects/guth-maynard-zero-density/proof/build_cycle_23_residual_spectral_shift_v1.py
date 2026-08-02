#!/usr/bin/env python3
"""Seal Cycle 23 residual spectral-shift and inverse-leverage dichotomy."""
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
OUTPUT = ROOT / "artifacts/cycle-23-residual-spectral-shift-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-23-residual-spectral-shift-preregistration-v1.md", "a0a58e9f030c233a82938de0392b69a06242eb0524be4d0b940d67b22f19e19c"),
    "document": (ROOT / "docs/cycle-23-residual-spectral-shift-v1.md", "dfebcc67148db74ca954095669a9f6ad55b3c87a8169dd48c91511b652d6e008"),
    "conventions": (ROOT / "conventions/residual_spectral_shift_v1.py", "a07efce513817a0da9878b7c58371990a1abd3026dc09d79ab85f43f737ee347"),
    "tests": (ROOT / "tests/test_cycle_23_residual_spectral_shift_v1.py", "b73082f8b7d7a5f56620b5c68ee5fed39e986fdff8b418176d56f2b196350a57"),
    "cycle22": (ROOT / "artifacts/cycle-22-volume-noise-v1.json", "e75e69e9d8b770de14aa4c567a598ae60779b31c790b5714745c03068ce8f9cc"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 23 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("residual_spectral_shift_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 23 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    critical = rows["critical_exponents"]
    finite = rows["finite_diagonal_residual"]
    require(critical["k_rho"] == Fraction(6, 25), "spectral-shift exponent mismatch")
    require(finite["determinant_ratio"] == finite["direct_determinant"], "determinant identity mismatch")
    return rows


def validate_cycle22() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle22"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_SQRT_NOISE_FULL_VOLUME_NO_GO_RENORMALIZED_SPECTRAL_SHIFT_OPEN", "Cycle 22 status mismatch")
    require(prior["route_effect"]["next_gate"].startswith("Define and control a bulk-renormalized"), "Cycle 22 next gate mismatch")
    return {"cycle22_role": "motivation and scale boundary for canonical residual subtraction"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-23-residual-spectral-shift-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_RESIDUAL_SPECTRAL_SHIFT_INVERSE_LEVERAGE_DICHOTOMY_PRIME_GATE_OPEN",
        "claim_boundary": "This artifact proves an exact common-direction residual factorization and shift/leverage dichotomy. It does not bound prime residual leverage, exclude the singular branch, prove the skeleton target, improve density, or improve intervals.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_cycle22()},
        "residual_factorization": {
            "epistemic_status": "PROVED",
            "statement": "With Z=H-qq*, D^2=diag(Z), B=D^-1ZD^-1, and s=D^-1q, det(H)/det(B)=product(1-rho_t)(1+s*B^-1s).",
        },
        "critical_dichotomy": {
            "epistemic_status": "PROVED",
            "small_leverage": "L<=exp(epsilon k rho) forces residual spectral shift <=-(1-epsilon)k rho+log 2.",
            "large_leverage": "Avoiding shift below -c k rho forces L>=exp((1-c)k rho)-1.",
            "critical_scale": "k rho=X^(6/25)",
            "singular_branch": "RESIDUAL_SINGULAR retained separately",
        },
        "prime_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Exclude exponentially large inverse leverage and the residual-singular branch for actual separated prime rows, or show their structure feeds E10 detector surgery.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_json(rows),
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_23_residual_spectral_shift_v1.py --write",
            "check_command": "python3 proof/build_cycle_23_residual_spectral_shift_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_23_residual_spectral_shift_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 23 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 23 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 23 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
