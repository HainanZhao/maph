#!/usr/bin/env python3
"""Seal Cycle 55 abstract centered-trace boundary."""
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
OUTPUT = ROOT / "artifacts/cycle-55-centered-trace-boundary-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-55-centered-trace-preregistration-v1.md", "ad904f4ba907562c96ffa9b200a01d1ee9b8b2e7195c57f8ed5a32d39145da6e"),
    "document": (ROOT / "docs/cycle-55-centered-trace-v1.md", "179a7722a3cd1d5159c798c3372ed2fc0943e63d1cc1934790003b49fa015c9d"),
    "conventions": (ROOT / "conventions/centered_trace_boundary_v1.py", "45cdfe4816feb1e8f8e2724777e33743da4dc0302db4f7cabe8cc316e571372b"),
    "tests": (ROOT / "tests/test_cycle_55_centered_trace_boundary_v1.py", "945ff0745115183c04cacd4bc023d5b5d5d91b6a8be48aaeb18fb25020efe20b"),
    "cycle54": (ROOT / "artifacts/cycle-54-coordinatewise-bessel-ledger-v1.json", "566e0c651c7fc95cf91719094702fe35a7156821fedac688cb96a6cf1f6362e0"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 55 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("centered_trace_boundary_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 55 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["penultimate_exponent"]["R_rho_exponent"] == -Fraction(3, 50), "penultimate exponent")
    require(rows["endpoint_example"]["all_even_centered_traces"] == 0, "endpoint centered trace")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle54"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_FULL_ORDINARY_EXPOSURE_OR_THREE_FIFTIETHS_HYBRID_REQUIRED", "Cycle 54 status mismatch")
    return {"prior_role": "test whether scalar diagonal centering can supply Cycle 54's missing 3/50"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-55-centered-trace-boundary-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_SCALAR_CENTERED_TRACES_SHARP_PRIME_CUMULANT_OPEN",
        "claim_boundary": "This artifact proves an abstract common-projection/PSD boundary only. It does not obstruct prime-coordinate cumulants or prove an analytic, density, or interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "centered_trace_boundary": {
            "epistemic_status": "PROVED",
            "statement": "For every R rho<=1 there are unit rows with common projection rho and Gram I_R, so every scalar-diagonal-centered even trace vanishes; Cycle 54 has R rho exponent -3/50.",
        },
        "prime_cumulant_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Insert actual prime-coordinate edge covariances or Cycle-51 partition cumulants before taking the trace and seek the missing 3/50.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_55_centered_trace_boundary_v1.py --write",
            "check_command": "python3 proof/build_cycle_55_centered_trace_boundary_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_55_centered_trace_boundary_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 55 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 55 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 55 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
