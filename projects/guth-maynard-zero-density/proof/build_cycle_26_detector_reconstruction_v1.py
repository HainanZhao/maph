#!/usr/bin/env python3
"""Seal Cycle 26 detector-reconstruction duality."""
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
OUTPUT = ROOT / "artifacts/cycle-26-detector-reconstruction-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-26-detector-reconstruction-preregistration-v1.md", "08d43d84ce7f76af4a32a33bebe69af4f9889647ccce66b3d0e54b65b0346a62"),
    "document": (ROOT / "docs/cycle-26-detector-reconstruction-v1.md", "569b0da894d90f2c03a0a2fb8fd035d6b98769b9f98b7265bc9f44c2aa8d6bbb"),
    "conventions": (ROOT / "conventions/detector_reconstruction_v1.py", "f597325cfd6e124c4bfb0572a8ca362efd67e0afcc26c4577f194dbf3c8bb638"),
    "tests": (ROOT / "tests/test_cycle_26_detector_reconstruction_v1.py", "3b6e247b8a87a8c9013db6fdcabfcc0d548ad6e09250102c83bdc5a4b97f1b53"),
    "cycle23": (ROOT / "artifacts/cycle-23-residual-spectral-shift-v1.json", "605e7a3eb5ac5b4e342b512e4465762d43b1b919051e4dafd01058e7ae14121b"),
    "cycle24": (ROOT / "artifacts/cycle-24-leverage-pruning-v1.json", "939b0d39d4976be5b3dfbbef4e5797b3130504945825eb43cc9b5ed7516f5531"),
    "cycle25": (ROOT / "artifacts/cycle-25-near-cauchy-exclusion-v1.json", "a550a56484243f2e3b3cc4b237d41f91e794618a79630afdaac21c6426fa4392"),
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
    runtime = {"implementation": platform.python_implementation(), "python": platform.python_version(), "optimization_level": sys.flags.optimize}
    require(runtime == EXPECTED_RUNTIME, "Cycle 26 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("detector_reconstruction_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 26 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["critical_exponents"]["k_rho"] == Fraction(6, 25), "critical scale mismatch")
    require(rows["critical_exponents"]["reconstruction_error_exponent_fraction"] == Fraction(1, 8), "reconstruction scale mismatch")
    require(rows["positive_definite_check"]["c_star_s"] == rows["positive_definite_check"]["L"], "dual identity mismatch")
    return rows


def validate_prior() -> dict[str, str]:
    cycle23 = json.loads(INPUTS["cycle23"][0].read_text(encoding="utf-8"))
    cycle24 = json.loads(INPUTS["cycle24"][0].read_text(encoding="utf-8"))
    cycle25 = json.loads(INPUTS["cycle25"][0].read_text(encoding="utf-8"))
    require(cycle23.get("status") == "SEALED_RESIDUAL_SPECTRAL_SHIFT_INVERSE_LEVERAGE_DICHOTOMY_PRIME_GATE_OPEN", "Cycle 23 status mismatch")
    require(cycle24.get("status") == "SEALED_NEAR_CAUCHY_OR_RESIDUAL_ILL_CONDITIONING_TRICHOTOMY_PRIME_EXCLUSION_OPEN", "Cycle 24 status mismatch")
    require(cycle25.get("status") == "SEALED_NEAR_CAUCHY_PRIME_RECURRENCE_EXCLUDED_RESIDUAL_DEPENDENCE_OPEN", "Cycle 25 status mismatch")
    return {"prior_role": "large leverage and singular residual reinterpreted after near-Cauchy exclusion"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-26-detector-reconstruction-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_INVERSE_LEVERAGE_DETECTOR_RECONSTRUCTION_EXACT_DEPENDENCE_OPEN",
        "claim_boundary": "This artifact reinterprets large inverse leverage as detector reconstruction and splits a singular residual into exact reconstruction or exact row dependence. It does not construct a source-valid complementary detector, exclude exact row dependence, prove the skeleton target, improve zero density, or improve intervals.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "positive_definite_duality": {
            "epistemic_status": "PROVED",
            "statement": "For c=B^(-1)s and L=s*B^(-1)s, the scaled-row combination (c*/L)D^(-1)X reconstructs b* with exact error L^(-1/2).",
            "critical_error": "sqrt(2) exp(-k rho/8)=exp(-X^(6/25-o(1))/8+O(1))",
        },
        "singular_split": {
            "epistemic_status": "PROVED",
            "statement": "A residual null vector either reconstructs b* exactly or is an exact dependence among the scaled prime rows.",
        },
        "remaining_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Use approximate/exact detector reconstruction to build a source-valid complementary detector, and treat exact prime-row dependence via E8 or E9.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_json(rows),
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_26_detector_reconstruction_v1.py --write",
            "check_command": "python3 proof/build_cycle_26_detector_reconstruction_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_26_detector_reconstruction_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 26 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 26 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 26 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
