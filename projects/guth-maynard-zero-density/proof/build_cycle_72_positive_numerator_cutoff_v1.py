#!/usr/bin/env python3
"""Seal Cycle 72 primitive positive-numerator cutoff."""
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
OUTPUT = ROOT / "artifacts/cycle-72-positive-numerator-cutoff-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-72-positive-numerator-preregistration-v1.md", "7c855f3b4080212623ddbeee769c55611dcba43ce5eea9b98b50928e9a646ca8"),
    "document": (ROOT / "docs/cycle-72-positive-numerator-v1.md", "a63580381ce82e6dc9d33ad9fee15d984dccb3e588f6d1de9abd89247c3bb9fe"),
    "conventions": (ROOT / "conventions/positive_numerator_cutoff_v1.py", "ae5a68f3d5e2e7868e28a4978fb58397f3571ecd568b33ca9aedc496371241db"),
    "tests": (ROOT / "tests/test_cycle_72_positive_numerator_cutoff_v1.py", "9d3249120a1c9f7fae7191bdbe5c9c41f0bdf54af6272847d01fa77da77a8d1f"),
    "cycle71": (ROOT / "artifacts/cycle-71-fraction-budget-wedge-v1.json", "f6711801f4f6b521a801933d6cfe596f2953821a56daa6baab206cb27557ef35"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 72 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("positive_numerator_cutoff_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 72 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["hessian_lower"] == "exp(4pi*x)-1>>X^(-theta-o(1))", "Hessian lower bound")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle71"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_FRACTION_WEDGE_2THETA_PLUS_KAPPA_LT_6_25_CLOSED", "Cycle 71 status mismatch")
    return {"prior_role": "sharpen the curvature loss on the residual fraction-budget atlas"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-72-positive-numerator-cutoff-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_FACTORED_CURVATURE_LOSS_XTHETA_ON_RESIDUAL_ATLAS_OPEN",
        "claim_boundary": "This artifact sharpens the primitive endpoint and Hessian loss only. It proves no two-variable sum, full packet, recurrence, powered, density, or interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "positive_numerator": {
            "epistemic_status": "PROVED",
            "statement": "For q>1, primitivity excludes a=0; packet accuracy then forces ell>>Delta/q.",
        },
        "curvature_improvement": {
            "epistemic_status": "PROVED",
            "statement": "The factored stationary Hessian is at least X^(-theta-o(1)), superseding the nonsharp Cycle-70 loss X^(-9/25-kappa).",
        },
        "analytic_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Apply a two-variable oscillatory estimate on the residual atlas with only X^theta determinant loss.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_72_positive_numerator_cutoff_v1.py --write",
            "check_command": "python3 proof/build_cycle_72_positive_numerator_cutoff_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_72_positive_numerator_cutoff_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 72 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 72 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 72 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
