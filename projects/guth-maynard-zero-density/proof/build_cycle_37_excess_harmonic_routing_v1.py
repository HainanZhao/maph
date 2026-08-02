#!/usr/bin/env python3
"""Seal Cycle 37 entropy-excess harmonic-routing boundary."""
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
OUTPUT = ROOT / "artifacts/cycle-37-excess-harmonic-routing-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-37-excess-harmonic-routing-preregistration-v1.md", "204c65893c3ed469f1e457a97cea4100b22978259fd9c295fd05975a13b4a6b7"),
    "document": (ROOT / "docs/cycle-37-excess-harmonic-routing-v1.md", "8846c97bca418cadc4e3cdf70cbe3159b91f674da262747f89036f582b71aa69"),
    "conventions": (ROOT / "conventions/excess_harmonic_routing_v1.py", "e10e6ab2bfc46879cc5b0d1be02b5c3f3e340d69819067c6937b455e8a4607b2"),
    "tests": (ROOT / "tests/test_cycle_37_excess_harmonic_routing_v1.py", "c636eff0da0d34fbb4eb81fdc78b13513f4f6f4874259e2f3cb89adde6942715"),
    "cycle36": (ROOT / "artifacts/cycle-36-information-projection-v1.json", "a80600191a8dd58642b6bf9bc72a40c6946c4503b36db213cdee5ec0037b027d"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 37 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("excess_harmonic_routing_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 37 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["registered_scales"]["r4_excess"]["kernel_harmonic"] == Fraction(1, 4), "r4 route")
    require(rows["registered_scales"]["r2_excess"]["kernel_harmonic"] == Fraction(11, 20), "r2 route")
    require(rows["registered_scales"]["r2_excess"]["harmonic_color_loss"] == Fraction(3, 10), "color loss")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle36"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_FIRST_HARMONIC_ENTROPY_DETERMINANT_EQUIVALENCE_EXCESS_OPEN", "Cycle 36 status mismatch")
    return {"prior_role": "route the only new Cycle 36 statistic, entropy excess, into harmonic information"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-37-excess-harmonic-routing-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_ENTROPY_EXCESS_ARBITRARY_HARMONIC_HIDING_VECTOR_ROUTE_OPEN",
        "claim_boundary": "This artifact proves a scoped abstract histogram no-go and exact routing ledger. It does not construct actual prime rows, control the full harmonic vector, prove the kernel count, improve density, or improve intervals.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "harmonic_hiding": {
            "epistemic_status": "PROVED",
            "statement": "Positive cyclic histograms can preserve mass and first Fourier coefficient while placing KL-comparable new mass at any order 2<=m<=L-2.",
            "scope": "ABSTRACT_HISTOGRAM_NOT_ACTUAL_PRIME_PHASES",
        },
        "routing_loss": {
            "epistemic_status": "PROVED",
            "statement": "At L=X^(3/10), scalar Fourier pigeonholing costs X^(3/10), exceeding the missing 4/25; r^4 and r^2 excess route only to kernel exponents 1/4 and 11/20.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_json(rows),
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_37_excess_harmonic_routing_v1.py --write",
            "check_command": "python3 proof/build_cycle_37_excess_harmonic_routing_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_37_excess_harmonic_routing_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 37 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 37 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 37 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
