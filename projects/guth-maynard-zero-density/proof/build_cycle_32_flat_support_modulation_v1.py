#!/usr/bin/env python3
"""Seal Cycle 32 flat-support modulation reduction."""
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
OUTPUT = ROOT / "artifacts/cycle-32-flat-support-modulation-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-32-flat-support-modulation-preregistration-v1.md", "d30bf3e596e15e5854d97ab62c218f22ecdcfa71b2fd655be5a250c51dc03303"),
    "document": (ROOT / "docs/cycle-32-flat-support-modulation-v1.md", "b40d91a45ca4318970d8ac7aaad22905067d4beadeeebbd2c1c6d8ae22a8dc45"),
    "conventions": (ROOT / "conventions/flat_support_modulation_v1.py", "39bbc928ee4ca6268dfca96d05b2e64b7a93f7347b1bf5fceb1f82b33f7e35ed"),
    "tests": (ROOT / "tests/test_cycle_32_flat_support_modulation_v1.py", "33949e8a6667392e1ceaa4249a1fa6d47df62973bfd0610187c213e6c0b2eda0"),
    "cycle29": (ROOT / "artifacts/cycle-29-polynomial-block-subspace-v1.json", "bec07567ef2855c27f67bcb05f21268873fdaa7b1f87a540e38047820029aed8"),
    "cycle31": (ROOT / "artifacts/cycle-31-variable-rank-self-dual-v1.json", "7c6f3a75cbe0d16ebe729260cbc7ac42fee4b86e00b80fb832926317e8f11784"),
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
    if isinstance(value, list):
        return [exact_json(item) for item in value]
    if isinstance(value, dict):
        return {str(key): exact_json(item) for key, item in value.items()}
    return value


def check_runtime() -> dict[str, Any]:
    runtime = {"implementation": platform.python_implementation(), "python": platform.python_version(), "optimization_level": sys.flags.optimize}
    require(runtime == EXPECTED_RUNTIME, "Cycle 32 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("flat_support_modulation_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 32 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["finite_dyadic"]["selected_mass"] == Fraction(3, 4), "selected mass mismatch")
    require(rows["finite_dyadic"]["error_amplification_squared"] == Fraction(4, 3), "error amplification mismatch")
    require(rows["support_ladder"][0]["prime_coordinate_support"] == Fraction(21, 25), "square endpoint mismatch")
    require(rows["support_ladder"][-1]["prime_coordinate_support"] == 1, "full endpoint mismatch")
    return rows


def validate_prior() -> dict[str, str]:
    expected = {
        "cycle29": "SEALED_POLYNOMIAL_BLOCK_SUBSPACE_NEAR_PACKET_EXCLUDED",
        "cycle31": "SEALED_VARIABLE_RANK_SELF_DUAL_BLOCK_REDUCTION",
    }
    for label, status in expected.items():
        prior = json.loads(INPUTS[label][0].read_text(encoding="utf-8"))
        require(prior.get("status") == status, f"{label} status mismatch")
    return {"prior_role": "adaptive block modulation flattened at the self-dual scale"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-32-flat-support-modulation-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_FLAT_SUPPORT_MODULATION_LADDER",
        "claim_boundary": "This artifact reduces arbitrary reconstructed modulation to a near-flat dyadic support and quantifies its support ladder. It does not exclude any rung, prove a prime-Vandermonde bound, close the skeleton target, improve zero density, or improve intervals.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "dyadic_flattening": {
            "epistemic_status": "PROVED",
            "statement": "A dyadic level carries squared mass at least 3/(4L), has normalized block amplitudes between 1/(2sqrt(s)) and 2/sqrt(s), and preserves reconstruction error exp(-X^(2/25-o(1))).",
        },
        "support_ladder": {
            "epistemic_status": "PROVED",
            "statement": "For s=X^(lambda+o(1)), 0<=lambda<=4/25, prime-coordinate exponent is 21/25+lambda while row exponent is 21/25.",
            "square_rung": "lambda=0",
        },
        "remaining_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Prove a generalized prime-Vandermonde lower bound on the lambda=0 square rung and multiplicative-energy/support-pruning bounds for lambda>0.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_json(rows),
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_32_flat_support_modulation_v1.py --write",
            "check_command": "python3 proof/build_cycle_32_flat_support_modulation_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_32_flat_support_modulation_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 32 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 32 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 32 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
