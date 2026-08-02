#!/usr/bin/env python3
"""Seal Cycle 30 block-subspace residual-shift extremizer."""
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
OUTPUT = ROOT / "artifacts/cycle-30-block-subspace-extremizer-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-30-block-subspace-extremizer-preregistration-v1.md", "7c5ed08ae64b47bf30dc3b54e95ab4a5daa2ab2643843fd3aa17bba63016e4fc"),
    "document": (ROOT / "docs/cycle-30-block-subspace-extremizer-v1.md", "177232a8b011c06dec04201d4d3d66fefa16b52d227272d9d5045a11f3fa1faa"),
    "conventions": (ROOT / "conventions/block_subspace_extremizer_v1.py", "cb1378643956b06fcd7771693a3a98ef01238be470fde8a7c29e7dca6a4c0839"),
    "tests": (ROOT / "tests/test_cycle_30_block_subspace_extremizer_v1.py", "d52c145c0d566248b9926e0003bb680eda798dc045ce4e5b52cf4c18966f39fd"),
    "cycle19": (ROOT / "artifacts/cycle-19-synchronization-graph-v1.json", "3c68ee97a31f7a7cb2612769f58c2645b4a58332aeceaa856d7082de635aeb63"),
    "cycle23": (ROOT / "artifacts/cycle-23-residual-spectral-shift-v1.json", "605e7a3eb5ac5b4e342b512e4465762d43b1b919051e4dafd01058e7ae14121b"),
    "cycle27": (ROOT / "artifacts/cycle-27-hadamard-detector-surgery-v1.json", "4a62765a22c0a2ca7a70d5917925859029faad155827a031efee90918c703c53"),
    "cycle28": (ROOT / "artifacts/cycle-28-rank-j-spectral-shift-v1.json", "53d2c7eca302b3fd02ff499578657c533a1747077f4e21439587ecc56614a576"),
    "cycle29": (ROOT / "artifacts/cycle-29-polynomial-block-subspace-v1.json", "bec07567ef2855c27f67bcb05f21268873fdaa7b1f87a540e38047820029aed8"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 30 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("block_subspace_extremizer_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 30 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    finite = rows["finite_extremizer"]
    require(finite["multiplicative_determinant_ratio"] == 1, "shift cancellation mismatch")
    require(finite["leverage"] == finite["L_target"], "leverage target mismatch")
    require(rows["block_synchronization"]["nontrivial_hadamard_values"] == (0, 0, 0), "block synchronization mismatch")
    require(rows["critical_exponents"]["k_rho"] == Fraction(6, 25), "critical scale mismatch")
    return rows


def validate_prior() -> dict[str, str]:
    expected = {
        "cycle19": "SEALED_SYNCHRONIZATION_GRAPH_ABSTRACT_BOUNDARY_PRIME_LOG_CLOSURE_OPEN",
        "cycle23": "SEALED_RESIDUAL_SPECTRAL_SHIFT_INVERSE_LEVERAGE_DICHOTOMY_PRIME_GATE_OPEN",
        "cycle27": "SEALED_ORTHOGONAL_SIGNED_DETECTOR_OR_MULTIBLOCK_SYNCHRONIZATION",
        "cycle28": "SEALED_RANK_J_SHIFT_OR_ADAPTIVE_DETECTOR_RECONSTRUCTION",
        "cycle29": "SEALED_POLYNOMIAL_BLOCK_SUBSPACE_NEAR_PACKET_EXCLUDED",
    }
    for label, status in expected.items():
        prior = json.loads(INPUTS[label][0].read_text(encoding="utf-8"))
        require(prior.get("status") == status, f"{label} status mismatch")
    return {"prior_role": "all abstract synchronization, shift, reconstruction, and block-subspace gates realized simultaneously"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-30-block-subspace-extremizer-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_ABSTRACT_BLOCK_SUBSPACE_RESIDUAL_SHIFT_SATURATION",
        "claim_boundary": "This artifact proves saturation only for arbitrary Hilbert rows with block-subspace projections and arbitrary separated labels. It does not assert an actual prime-phase extremizer, prove the skeleton target, improve zero density, or improve intervals.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "simultaneous_extremizer": {
            "epistemic_status": "PROVED",
            "statement": "A block-flat common detector plus a tuned simplex residual has perfect multiblock synchronization, zero nontrivial Hadamard values, exact determinant-shift cancellation, and detector reconstruction error L_target^(-1/2) for arbitrary k and J in the stated range.",
        },
        "critical_instance": {
            "epistemic_status": "PROVED",
            "statement": "At k=X^(21/25), rho=X^(-3/5), J=X^(1/25), the residual small eigenvalue and reconstruction error are stretched exponential on scale X^(6/25).",
        },
        "saturation_scope": {
            "epistemic_status": "PROVED",
            "architecture": "arbitrary Hilbert rows + separated labels + block-flat detector + Hadamard surgery + residual spectral shift/reconstruction",
            "missing_input": "actual prime phase curve, logarithmic curvature, unique factorization, or source identity",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_json(rows),
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_30_block_subspace_extremizer_v1.py --write",
            "check_command": "python3 proof/build_cycle_30_block_subspace_extremizer_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_30_block_subspace_extremizer_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 30 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 30 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 30 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
