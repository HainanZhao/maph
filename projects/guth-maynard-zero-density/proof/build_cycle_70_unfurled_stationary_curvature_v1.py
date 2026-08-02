#!/usr/bin/env python3
"""Seal Cycle 70 unfurled stationary-curvature identity."""
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
OUTPUT = ROOT / "artifacts/cycle-70-unfurled-stationary-curvature-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-70-unfurled-curvature-preregistration-v1.md", "22ed400d762fdf7f3688628e8bbee23e525efc9693ee7245c59c8ad84c7898b7"),
    "document": (ROOT / "docs/cycle-70-unfurled-curvature-v1.md", "ef1d9f477d36922f2eddef1d5f799777a98c25ba7878b5617f696c205d4cdb20"),
    "conventions": (ROOT / "conventions/unfurled_stationary_curvature_v1.py", "1e8afc97f2becf439d7da8c6be141813c0bf8049b5907ecc04060a84251ccf08"),
    "tests": (ROOT / "tests/test_cycle_70_unfurled_stationary_curvature_v1.py", "2f6b03497baa24d7f819a057f93dcdcf90be03744b1078ca3e955f25f4ad1d53"),
    "cycle69": (ROOT / "artifacts/cycle-69-stationary-transport-dual-v1.json", "4f868a07381d89ccfafe72f80553a63b9457447a848408d22cb4493d4726a04c"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 70 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("unfurled_stationary_curvature_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 70 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require("(u/m)^2-1" in rows["derivative_identity"]["product_hessian"], "factored Hessian")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle69"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_STATIONARY_HESSIAN_DEGENERATE_PROJECTIVE_X21_25_OPEN", "Cycle 69 status mismatch")
    return {"prior_role": "restore a product variable projected away by complete frequency folding"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-70-unfurled-stationary-curvature-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_FACTORED_R_QPRIME_CURVATURE_WITH_ENDPOINT_LOSS_OPEN",
        "claim_boundary": "This artifact proves the factored Hessian and trivial small-endpoint split only. It proves no two-variable sum, full packet, recurrence, powered, density, or interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "curvature_restoration": {
            "epistemic_status": "PROVED",
            "statement": "For fixed stationary k, det Hess_(r,q') Psi(rq',k)=exp(4pi x)-1, positive off the ell=0 endpoint.",
        },
        "endpoint_split": {
            "epistemic_status": "PROVED",
            "statement": "Packet uniqueness makes ell blocks below exponent 6/25-kappa subcritical; the weakest surviving determinant exponent is -9/25-kappa.",
        },
        "analytic_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Prove a two-variable oscillatory estimate on the unbalanced (r,q') box that absorbs the quantified determinant loss.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_70_unfurled_stationary_curvature_v1.py --write",
            "check_command": "python3 proof/build_cycle_70_unfurled_stationary_curvature_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_70_unfurled_stationary_curvature_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 70 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 70 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 70 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
