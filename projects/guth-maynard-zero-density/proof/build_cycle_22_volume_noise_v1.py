#!/usr/bin/env python3
"""Seal Cycle 22 square-root volume-noise obstruction."""
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
OUTPUT = ROOT / "artifacts/cycle-22-volume-noise-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-22-volume-noise-preregistration-v1.md", "d1fbf416acb698943f28a373ac14810bf122ef98a275d16de996c0622c698f09"),
    "document": (ROOT / "docs/cycle-22-volume-noise-v1.md", "6c60a626d445a53dff8dc7c7773e25fd11c26975cea48c8a206ce15f590c1936"),
    "conventions": (ROOT / "conventions/volume_noise_v1.py", "a06ec5339f50ac28317d656639b6b86b3d4b2eb32492f9232d0e9930d8d5945b"),
    "tests": (ROOT / "tests/test_cycle_22_volume_noise_v1.py", "65fd85311a9d9f76a68dcc76ea8ffdd43d15dcb9ab79fa9838905c5ac8ab1322"),
    "cycle21_correction": (ROOT / "artifacts/cycle-21-continuum-volume-correction-v2.json", "2d326ad019096f23c9a15c3bf1a9d4b1f860fe5d3241a1dbbc78b9bb8c462971"),
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
    runtime = {"implementation": platform.python_implementation(), "python": platform.python_version(), "optimization_level": sys.flags.optimize}
    require(runtime == EXPECTED_RUNTIME, "Cycle 22 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("volume_noise_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 22 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    critical = rows["critical_exponents"]
    finite = rows["finite_block_unitary"]
    require(critical["operator_power_gap"] == Fraction(13, 25), "operator gap mismatch")
    require(critical["bulk_minus_signal"] == Fraction(11, 25), "volume gap mismatch")
    require(finite["determinant"] == Fraction(3, 4) ** 4, "finite determinant mismatch")
    return rows


def validate_cycle21() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle21_correction"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_WEIGHTED_CONTINUUM_CORRECTION_PRIME_OPERATOR_QUADRATURE_OPEN", "Cycle 21 correction status mismatch")
    require(prior["prime_perturbation"]["analytic_input_status"] == "CONJECTURED_OPEN", "Cycle 21 gate status mismatch")
    return {"cycle21_role": "full operator-discrepancy target stress-tested by square-root noise"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-22-volume-noise-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_SQRT_NOISE_FULL_VOLUME_NO_GO_RENORMALIZED_SPECTRAL_SHIFT_OPEN",
        "claim_boundary": "This artifact proves an abstract square-root-noise obstruction to generic full-operator and absolute-volume formulations. It does not prove actual prime rows realize the model, refute every determinant method, prove the skeleton target, improve density, or improve intervals.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_cycle21()},
        "volume_noise": {
            "epistemic_status": "PROVED",
            "statement": "A flat block-unitary Gram perturbation has entry scale X^-1/2, operator scale X^-2/25, and negative log-volume scale X^17/25 at k=X^21/25.",
            "operator_gap_from_cycle21": "13/25",
            "bulk_volume_gap_over_common_vector": "11/25",
        },
        "route_effect": {
            "epistemic_status": "PROVED",
            "statement": "Square-root entry cancellation alone cannot deliver the Cycle-21 full operator gate or the Cycle-20 absolute determinant lower bound.",
            "next_gate": "Define and control a bulk-renormalized log-volume or spectral-shift statistic at common-vector scale X^(6/25).",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_json(rows),
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_22_volume_noise_v1.py --write",
            "check_command": "python3 proof/build_cycle_22_volume_noise_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_22_volume_noise_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 22 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 22 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 22 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
