#!/usr/bin/env python3
"""Seal Cycle 69 stationary transport-dual boundary."""
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
OUTPUT = ROOT / "artifacts/cycle-69-stationary-transport-dual-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-69-stationary-dual-preregistration-v1.md", "2e7c52d6940c204f22bf4aba4d4f2298ee164cfe9a895680e9cef0d9f06219fc"),
    "document": (ROOT / "docs/cycle-69-stationary-dual-v1.md", "b82cb1033ea2381540251239cf2526a727ba5bda44a5901e2cbc2e98e85fdbb2"),
    "conventions": (ROOT / "conventions/stationary_transport_dual_v1.py", "ca21d80c230ef9ebc86813074a7b7a0678364dfe5858eb66a75addaf26e9ebc3"),
    "tests": (ROOT / "tests/test_cycle_69_stationary_transport_dual_v1.py", "29ac05b65edbe72861cf6e0105fbe8911581664ccd6f1b2a3ac50624b65fe2e6"),
    "cycle68": (ROOT / "artifacts/cycle-68-folded-frequency-baseline-v1.json", "4c179b10dfb15ec20a9189001ca2c2b81dd3aac09ab56c0b1da9d224ae85d4b8"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 69 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("stationary_transport_dual_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 69 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["hessian_determinant"] == Fraction(0), "Hessian determinant")
    require(rows["dual_index_ceiling"] == Fraction(21, 25), "dual index")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle68"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_FOLDED_LARGE_SIEVE_GAP_3_50_PLUS_THETA_KAPPA", "Cycle 68 status mismatch")
    return {"prior_role": "test whether stationary curvature can recover the folded large-sieve deficit"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-69-stationary-transport-dual-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_STATIONARY_HESSIAN_DEGENERATE_PROJECTIVE_X21_25_OPEN",
        "claim_boundary": "This artifact proves the stationary phase, its homogeneous Hessian degeneracy, and the dual-index exponent only. It proves no primitive Poisson, packet, recurrence, powered, density, or interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "stationary_dual": {
            "epistemic_status": "PROVED",
            "statement": "The Legendre phase is homogeneous of degree one and has identically zero Hessian determinant in (m,k).",
        },
        "scale_interface": {
            "epistemic_status": "PROVED",
            "statement": "The maximum stationary dual-index exponent is 21/25, exactly the critical skeleton cardinality exponent; no identification of the two objects is claimed.",
        },
        "analytic_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Exploit projective ratio curvature or an unfurled variable, or route stationary aliases into the skeleton/seeded-recurrence engine.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_69_stationary_transport_dual_v1.py --write",
            "check_command": "python3 proof/build_cycle_69_stationary_transport_dual_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_69_stationary_transport_dual_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 69 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 69 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 69 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
