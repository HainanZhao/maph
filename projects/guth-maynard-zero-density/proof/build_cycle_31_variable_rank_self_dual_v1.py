#!/usr/bin/env python3
"""Seal Cycle 31 variable-rank self-dual block reduction."""
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
OUTPUT = ROOT / "artifacts/cycle-31-variable-rank-self-dual-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-31-variable-rank-self-dual-preregistration-v1.md", "9a9dda25dae5d0218648fccd59e0cab9dd3aa5a028fe9acb7fd6432b9b2d86b2"),
    "document": (ROOT / "docs/cycle-31-variable-rank-self-dual-v1.md", "5816e78e00d0abe5a74c7d65b2d9f035a2f56b7c0548ca06d490d2bb43d05dd0"),
    "conventions": (ROOT / "conventions/variable_rank_self_dual_v1.py", "6d1db56753089bd1e727e57d03d7c3a28819e2717e18bb2aee2d1966aaca5fbd"),
    "tests": (ROOT / "tests/test_cycle_31_variable_rank_self_dual_v1.py", "8751660ef4421e77860f3acd9e652e034858d6927061f66ba5c8caad0f2bf7e9"),
    "g0": (ROOT / "artifacts/g0-theorem-dependency-graph-v1.json", "14f80b35774a3994c93e1a08de34afb2aefff7023e1797932e6fb4d78af1281b"),
    "cycle25": (ROOT / "artifacts/cycle-25-near-cauchy-exclusion-v1.json", "a550a56484243f2e3b3cc4b237d41f91e794618a79630afdaac21c6426fa4392"),
    "cycle28": (ROOT / "artifacts/cycle-28-rank-j-spectral-shift-v1.json", "53d2c7eca302b3fd02ff499578657c533a1747077f4e21439587ecc56614a576"),
    "cycle29": (ROOT / "artifacts/cycle-29-polynomial-block-subspace-v1.json", "bec07567ef2855c27f67bcb05f21268873fdaa7b1f87a540e38047820029aed8"),
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
    if isinstance(value, list):
        return [exact_json(item) for item in value]
    if isinstance(value, dict):
        return {str(key): exact_json(item) for key, item in value.items()}
    return value


def check_runtime() -> dict[str, Any]:
    runtime = {"implementation": platform.python_implementation(), "python": platform.python_version(), "optimization_level": sys.flags.optimize}
    require(runtime == EXPECTED_RUNTIME, "Cycle 31 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("variable_rank_self_dual_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 31 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(len(rows["tradeoff_table"]) == 5, "tradeoff table size mismatch")
    require(rows["self_dual"]["block_count"] == Fraction(4, 25), "self-dual block count mismatch")
    require(rows["self_dual"]["block_size"] == Fraction(21, 25), "self-dual block size mismatch")
    require(rows["self_dual"]["reconstruction"] == Fraction(2, 25), "self-dual reconstruction mismatch")
    return rows


def validate_prior() -> dict[str, str]:
    expected = {
        "cycle25": "SEALED_NEAR_CAUCHY_PRIME_RECURRENCE_EXCLUDED_RESIDUAL_DEPENDENCE_OPEN",
        "cycle28": "SEALED_RANK_J_SHIFT_OR_ADAPTIVE_DETECTOR_RECONSTRUCTION",
        "cycle29": "SEALED_POLYNOMIAL_BLOCK_SUBSPACE_NEAR_PACKET_EXCLUDED",
    }
    for label, status in expected.items():
        prior = json.loads(INPUTS[label][0].read_text(encoding="utf-8"))
        require(prior.get("status") == status, f"{label} status mismatch")
    g0 = json.loads(INPUTS["g0"][0].read_text(encoding="utf-8"))
    require(g0.get("status") == "source dependency map; no new theorem", "G0 status mismatch")
    return {"prior_role": "Cycle 29 proof generalized across the full positive reconstruction-exponent range"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-31-variable-rank-self-dual-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_VARIABLE_RANK_SELF_DUAL_BLOCK_REDUCTION",
        "claim_boundary": "This artifact generalizes the block-subspace theorem to fixed 0<kappa<6/25 and identifies the self-dual kappa=4/25 scale. It does not prove a prime determinant bound, close the skeleton target, improve zero density, or improve intervals.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "variable_rank": {
            "epistemic_status": "PROVED",
            "statement": "For every fixed 0<kappa<6/25, near-subspace packets are excluded and the regular reconstruction error is exp(-X^(6/25-kappa-o(1))).",
        },
        "self_dual": {
            "epistemic_status": "PROVED",
            "statement": "At kappa=4/25, block count has exponent 4/25, primes per block and target rows both have exponent 21/25, and reconstruction error has exponent 2/25.",
        },
        "remaining_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Flatten the reconstructed modulation by amplitude profile and prove a generalized prime-Vandermonde or multiplicative-energy bound at the self-dual scale.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_json(rows),
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_31_variable_rank_self_dual_v1.py --write",
            "check_command": "python3 proof/build_cycle_31_variable_rank_self_dual_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_31_variable_rank_self_dual_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 31 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 31 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 31 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
