#!/usr/bin/env python3
"""Seal Cycle 24 leverage-pruning trichotomy."""
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
OUTPUT = ROOT / "artifacts/cycle-24-leverage-pruning-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-24-leverage-pruning-preregistration-v1.md", "605e026a9eefd43067266a2f496ce4cb49f2c71d444d5a7b539411c66c1cc2ec"),
    "document": (ROOT / "docs/cycle-24-leverage-pruning-v1.md", "7bfcc58effbb39ebf63da6a28973b925161034f443e7c5717778e328521350ec"),
    "conventions": (ROOT / "conventions/leverage_pruning_v1.py", "3bdf4977be9f2a83f84596516239d9c4f43e2d3b54f23129ab8ed3da5a9eea7a"),
    "tests": (ROOT / "tests/test_cycle_24_leverage_pruning_v1.py", "9763771faf870213589e9c99851e074972729f4476db269dec5c06e73e85f059"),
    "cycle23": (ROOT / "artifacts/cycle-23-residual-spectral-shift-v1.json", "605e7a3eb5ac5b4e342b512e4465762d43b1b919051e4dafd01058e7ae14121b"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 24 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("leverage_pruning_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 24 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["critical_exponents"]["k_rho"] == Fraction(6, 25), "structure exponent mismatch")
    require(rows["frozen_constants"]["small_eigenvalue_exponent_fraction"] == Fraction(1, 8), "eigenvalue constant mismatch")
    require(rows["finite_near_cauchy_check"]["kernel_lower"] == Fraction(3, 4), "near-Cauchy check mismatch")
    return rows


def validate_cycle23() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle23"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_RESIDUAL_SPECTRAL_SHIFT_INVERSE_LEVERAGE_DICHOTOMY_PRIME_GATE_OPEN", "Cycle 23 status mismatch")
    require(prior["critical_dichotomy"]["critical_scale"] == "k rho=X^(6/25)", "Cycle 23 scale mismatch")
    return {"cycle23_role": "exact shift/inverse-leverage dichotomy refined by amplitude pruning"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-24-leverage-pruning-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_NEAR_CAUCHY_OR_RESIDUAL_ILL_CONDITIONING_TRICHOTOMY_PRIME_EXCLUSION_OPEN",
        "claim_boundary": "This artifact refines inverse leverage into near-Cauchy recurrence, negative shift, residual singularity, or stretched-exponential residual ill-conditioning. It does not exclude any branch for primes, prove the skeleton target, improve density, or improve intervals.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_cycle23()},
        "near_cauchy": {
            "epistemic_status": "PROVED",
            "statement": "If at least half the rows have rho_t>=1-exp(-k rho/8), every pair in that subsystem has normalized kernel at least 1-2exp(-k rho/8).",
        },
        "regular_residual": {
            "epistemic_status": "PROVED",
            "statement": "On a half-sized regular subsystem, either shift<=-n rho/2, the residual is singular, or lambda_min(B)<=2k exp(-k rho/8).",
            "critical_structure_scale": "X^(6/25)",
        },
        "prime_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Exclude near-maximal prime-kernel recurrence and stretched-exponential residual dependence, or route either structure into E10 detector surgery.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_json(rows),
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_24_leverage_pruning_v1.py --write",
            "check_command": "python3 proof/build_cycle_24_leverage_pruning_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_24_leverage_pruning_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 24 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 24 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 24 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
