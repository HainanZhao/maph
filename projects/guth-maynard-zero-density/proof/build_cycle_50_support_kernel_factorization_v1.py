#!/usr/bin/env python3
"""Seal Cycle 50 prime-monomial support-kernel factorization."""
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
OUTPUT = ROOT / "artifacts/cycle-50-support-kernel-factorization-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-50-support-kernel-factorization-preregistration-v1.md", "ef1ffec93751ff2d4c819f003d2ce2c0644a021c8a994fa1d82ed2af46f61d26"),
    "document": (ROOT / "docs/cycle-50-support-kernel-factorization-v1.md", "bf96bcb2f3d275e936a970cf7e559b82783186d5fe68ae5c7c3d52274e255396"),
    "conventions": (ROOT / "conventions/support_kernel_factorization_v1.py", "93591122ef31c36347505ba7be300e3690cc754f0b8bcfff776bcc22c4756d1e"),
    "tests": (ROOT / "tests/test_cycle_50_support_kernel_factorization_v1.py", "0d4570e0c01bafb64e7746be3dd5da4c2f134d1811695e6351a7bdebcd415579"),
    "cycle49": (ROOT / "artifacts/cycle-49-row-fourier-exceptional-v1.json", "ea00b6ff9791a4d389e9e2431e3bdec7cc185538e07ffd86f9873c7e90899f5a"),
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
    if isinstance(value, list):
        return [exact_json(item) for item in value]
    return value


def check_runtime() -> dict[str, Any]:
    runtime = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
    }
    require(runtime == EXPECTED_RUNTIME, "Cycle 50 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("support_kernel_factorization_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 50 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["injective_range"] == "m>s", "injective range")
    require(rows["identities"]["h4"].startswith("(P1^4"), "h4 identity")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle49"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_EXCEPTIONAL_MEASURE_SMALL_ABSOLUTE_PAIRING_FAILS_RRD_OPEN", "Cycle 49 status mismatch")
    return {"prior_role": "replace absolute coefficient-pair mass by an exact factored support-correlation kernel"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-50-support-kernel-factorization-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_FACTORED_DIFFERENCE_KERNEL_DK4_PLUS_SMALL_M_OPEN",
        "claim_boundary": "This artifact proves support injectivity, symmetric-polynomial factorization, and the large-value reduction for m>s. It does not prove DK_s, the small-m cases, AMPR_s, LCAM_s, density, or interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "factorization": {
            "epistemic_status": "PROVED",
            "statement": "For m>s, the distinct-support correlation is exactly K(mh) times the complete homogeneous degree-s symmetric polynomial in the prime phases.",
        },
        "large_value_reduction": {
            "epistemic_status": "PROVED",
            "statement": "Phase-aligned Halasz--Montgomery reduces large F_(m,s) values to row sums of K(m(t-u)) H_s(t-u), with coefficient norm and support both X^(s+1+o(1)).",
        },
        "analytic_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Prove the aggregate factored difference-kernel estimate DK_4 and treat m=2,3,4 separately.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_50_support_kernel_factorization_v1.py --write",
            "check_command": "python3 proof/build_cycle_50_support_kernel_factorization_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_50_support_kernel_factorization_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 50 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 50 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 50 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
