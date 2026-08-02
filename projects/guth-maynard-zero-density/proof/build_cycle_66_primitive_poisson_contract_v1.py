#!/usr/bin/env python3
"""Seal Cycle 66 primitive Möbius--Poisson contract."""
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
OUTPUT = ROOT / "artifacts/cycle-66-primitive-poisson-contract-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-66-primitive-poisson-preregistration-v1.md", "39f4b33a7e856bc95aa58f022c3706345515db96d2d4cbd1f0e49a9c842713a4"),
    "document": (ROOT / "docs/cycle-66-primitive-poisson-v1.md", "41ec4fee394832df59a2f9f4ae8b83e867b08b79ade981398bd597cf11cec49c"),
    "conventions": (ROOT / "conventions/primitive_poisson_contract_v1.py", "705c7280d5e4334115c2d1de0561a17db3616210ae4062c44d40a431c7c571a9"),
    "tests": (ROOT / "tests/test_cycle_66_primitive_poisson_contract_v1.py", "fbc300cb4811b529dfb54b423961e9ec55a2957773c3b260fb66a300a37e7e52"),
    "cycle65": (ROOT / "artifacts/cycle-65-depth-packet-ledger-v1.json", "f86cecfa996a7583990a24a6060167a700fa8cca54c199ec92cdf2f3c8637a2d"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 66 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("primitive_poisson_contract_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 66 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["exponents"]["raw_off_diagonal_target"] == "31/25 independent of theta,kappa", "raw target")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle65"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_LOG_DEPTH_PACKET_DISCREPANCY_OR_X6_25_AP_RECURRENCE_OPEN", "Cycle 65 status mismatch")
    return {"prior_role": "dualize the depth-refined primitive packet count without losing coprimality"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-66-primitive-poisson-contract-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_PRIMITIVE_POISSON_X31_25_OR_DEEP_PACKET_RECURRENCE_OPEN",
        "claim_boundary": "This artifact proves a primitive Möbius--Poisson identity and exponent contract only. It does not bound the off-diagonal or prove packet, recurrence, powered, density, or interval gains.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "primitive_dual": {
            "epistemic_status": "PROVED",
            "statement": "Möbius inversion before Poisson summation preserves primitive numerator-denominator labels and separates a diagonal from a signed exponential form.",
        },
        "scale_invariant_target": {
            "epistemic_status": "PROVED",
            "statement": "The diagonal has at least 1/5 exponent margin; after the (KX)^-1 prefactor, the raw off-diagonal target is strictly below X^(31/25) on every admissible scale, with frequencies at most X^(36/25+o(1)).",
        },
        "analytic_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Bound the signed primitive Möbius--Poisson form below X^(31/25), or extract its structured major arcs into the deep-packet recurrence branch.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_66_primitive_poisson_contract_v1.py --write",
            "check_command": "python3 proof/build_cycle_66_primitive_poisson_contract_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_66_primitive_poisson_contract_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 66 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 66 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 66 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
