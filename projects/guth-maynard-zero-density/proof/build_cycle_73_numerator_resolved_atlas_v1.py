#!/usr/bin/env python3
"""Seal Cycle 73 numerator-resolved packet atlas."""
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
OUTPUT = ROOT / "artifacts/cycle-73-numerator-resolved-atlas-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-73-numerator-atlas-preregistration-v1.md", "a2ebb7420254f56d09515b2895fffc665f20a0e9fb4027272bb84dac6e744a56"),
    "document": (ROOT / "docs/cycle-73-numerator-atlas-v1.md", "0c6087cac2de107226cb94ac37222ce9c5c9d6b440dcc24d8437c3a1771ea50a"),
    "conventions": (ROOT / "conventions/numerator_resolved_atlas_v1.py", "39b5703cea6c9509aeb383f547c63ae793f200de305722afba32f164fc4651f4"),
    "tests": (ROOT / "tests/test_cycle_73_numerator_resolved_atlas_v1.py", "eb4c8c45fb1dc72c5c4cb30a62e25019dd7736794aca681f123175c17ad43074"),
    "cycle72": (ROOT / "artifacts/cycle-72-positive-numerator-cutoff-v1.json", "547bb719c76df324c2dfda63f12c6a2a3c83ace3bbfd4d8eb5b941895296a7ef"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 73 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("numerator_resolved_atlas_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 73 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["closed_region"] == "theta+alpha+kappa<6/25", "closed region")
    require(rows["hessian_loss"] == "theta-alpha", "Hessian loss")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle72"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_FACTORED_CURVATURE_LOSS_XTHETA_ON_RESIDUAL_ATLAS_OPEN", "Cycle 72 status mismatch")
    return {"prior_role": "resolve the positive numerator to close more cells and sharpen curvature cellwise"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-73-numerator-resolved-atlas-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_NUMERATOR_WEDGE_CLOSED_RESIDUAL_CURVATURE_OPEN",
        "claim_boundary": "This artifact closes only strict numerator-resolved cells and sharpens their curvature ledger. The boundary and residual atlas remain open; no powered, density, or interval gain is proved.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "numerator_wedge": {
            "epistemic_status": "PROVED",
            "statement": "The cell count X^(theta+alpha) closes packet and pair targets whenever theta+alpha+kappa<6/25.",
        },
        "cellwise_curvature": {
            "epistemic_status": "PROVED",
            "statement": "The curve-index relation alpha=theta+lambda-3/5 makes the factored Hessian loss exactly theta-alpha.",
        },
        "analytic_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Prove the factored two-variable estimate only on theta+alpha+kappa>=6/25 with the cellwise determinant loss.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_73_numerator_resolved_atlas_v1.py --write",
            "check_command": "python3 proof/build_cycle_73_numerator_resolved_atlas_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_73_numerator_resolved_atlas_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 73 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 73 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 73 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
