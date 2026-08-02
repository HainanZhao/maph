#!/usr/bin/env python3
"""Seal Cycle 25 near-Cauchy exclusion for dyadic prime rows."""
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
OUTPUT = ROOT / "artifacts/cycle-25-near-cauchy-exclusion-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-25-near-cauchy-exclusion-preregistration-v1.md", "d704ff883888fb7fada6ecb546a4bb7de73f7b861c4d33ca24165b41a3ea1bc4"),
    "document": (ROOT / "docs/cycle-25-near-cauchy-exclusion-v1.md", "70b576dc59c943ff8951e0cebf69304823e84141de4425f68d2d2e5d968b7c45"),
    "conventions": (ROOT / "conventions/near_cauchy_exclusion_v1.py", "7cba1fd7e48a50445b5520db86adcfdeb039e9c0ac74f2b64df4d423c7299620"),
    "tests": (ROOT / "tests/test_cycle_25_near_cauchy_exclusion_v1.py", "88a16784e678f4db2ad1ff005444d6c38e02b3350da3ace2e3222b636951d658"),
    "cycle24": (ROOT / "artifacts/cycle-24-leverage-pruning-v1.json", "939b0d39d4976be5b3dfbbef4e5797b3130504945825eb43cc9b5ed7516f5531"),
    "evertse_source": (ROOT / "artifacts/sources/evertse-linear-forms-logarithms-ch5.pdf", "1f7f41e3b3292e380651baf4b30ed8717c3411909202dc0409a0d41ed4f149f0"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 25 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("near_cauchy_exclusion_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 25 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["critical_exponents"]["k_rho"] == Fraction(6, 25), "critical scale mismatch")
    require(rows["critical_exponents"]["phase_error_exponent_fraction"] == Fraction(1, 16), "phase-error constant mismatch")
    require(rows["concentration_constants"]["ratio_distance_multiplier"] == 4, "concentration flow mismatch")
    require(rows["asymptotic_separation"]["contradiction_for_large_X"], "asymptotic contradiction absent")
    return rows


def validate_cycle24() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle24"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_NEAR_CAUCHY_OR_RESIDUAL_ILL_CONDITIONING_TRICHOTOMY_PRIME_EXCLUSION_OPEN", "Cycle 24 status mismatch")
    require(prior["regular_residual"]["critical_structure_scale"] == "X^(6/25)", "Cycle 24 scale mismatch")
    return {"cycle24_role": "near-Cauchy arm excluded; residual dependence arms retained"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-25-near-cauchy-exclusion-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_NEAR_CAUCHY_PRIME_RECURRENCE_EXCLUDED_RESIDUAL_DEPENDENCE_OPEN",
        "claim_boundary": "This artifact excludes Cycle 24's near-Cauchy alternative for full dyadic prime phase rows at polynomial height. It does not exclude residual singularity or stretched-exponential residual ill-conditioning, prove the skeleton target, improve zero density, or improve prime intervals.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_cycle24()},
        "source_scope": {
            "epistemic_status": "PROVED",
            "statement": "Theorem 5.4 of the pinned Evertse notes states the explicit rational Matveev bound used here; only its m=2 rational specialization is imported.",
            "derived_scale": "rational heights <=2X and B<=X^(12/5+o(1)) give exp(-O((log X)^3))",
        },
        "phase_concentration": {
            "epistemic_status": "PROVED",
            "statement": "Mean modulus at least 1-2delta forces every prime-ratio phase within 4 sqrt(M delta) of one.",
        },
        "three_prime_exclusion": {
            "epistemic_status": "PROVED",
            "statement": "Three primes in fixed separated proportional intervals produce a nonzero two-logarithm form with upper exp(-k rho/16+O(log X)), contradicting the Matveev lower exp(-O((log X)^3)).",
            "critical_scale": "k rho=X^(6/25-o(1))",
        },
        "remaining_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Detect the negative residual shift or exclude singular/stretched-exponentially ill-conditioned normalized prime residuals via a generalized Vandermonde principle.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_json(rows),
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_25_near_cauchy_exclusion_v1.py --write",
            "check_command": "python3 proof/build_cycle_25_near_cauchy_exclusion_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_25_near_cauchy_exclusion_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 25 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 25 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 25 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
