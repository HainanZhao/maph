#!/usr/bin/env python3
"""Seal Cycle 71 primitive-fraction wedge closure."""
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
OUTPUT = ROOT / "artifacts/cycle-71-fraction-budget-wedge-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-71-fraction-budget-preregistration-v1.md", "ade0e8381312d252a8ff53b5ad27831511782df6ac62a54b0a0e405191462206"),
    "document": (ROOT / "docs/cycle-71-fraction-budget-v1.md", "9ffc93fc6d6890ee2965b0a91dbb3172f52d8979ec0a92acdafa5ee154cde303"),
    "conventions": (ROOT / "conventions/fraction_budget_wedge_v1.py", "38b5c7c6586a97aea17a913babe022ec1051062d9e2e82101cbfe940d86c9101"),
    "tests": (ROOT / "tests/test_cycle_71_fraction_budget_wedge_v1.py", "26e740c2e4f6ff403f15296002b9562d6cabc137a4658a0bd9ab1c91fd27967b"),
    "cycle70": (ROOT / "artifacts/cycle-70-unfurled-stationary-curvature-v1.json", "2218be784434352a97037a865a40acd43969562f3430df22944b23adbbde6acc"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 71 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("fraction_budget_wedge_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 71 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["closed_wedge"] == "2theta+kappa<6/25", "closed wedge")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle70"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_FACTORED_R_QPRIME_CURVATURE_WITH_ENDPOINT_LOSS_OPEN", "Cycle 70 status mismatch")
    return {"prior_role": "remove cells that close before the unfurled-curvature estimate is needed"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-71-fraction-budget-wedge-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_FRACTION_WEDGE_2THETA_PLUS_KAPPA_LT_6_25_CLOSED",
        "claim_boundary": "This artifact closes only the strict fraction-budget wedge. The boundary and residual packet atlas remain open; no powered, density, or interval gain is proved.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "fraction_wedge": {
            "epistemic_status": "PROVED",
            "statement": "Primitive packet injectivity and O(Q^2) available fractions close every cell with 2theta+kappa<6/25, both in packet count and weighted pair census.",
        },
        "boundary": {
            "epistemic_status": "PROVED",
            "statement": "The line 2theta+kappa=6/25 ties the strict target and is not closed without an additional margin.",
        },
        "literature_scope": {
            "epistemic_status": "OBSERVED",
            "statement": "Huang arXiv:1403.7388 definition (1.1) and Theorem 1 use a common denominator for both rational coordinates and do not directly cover the mixed grid-denominator packets here.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_71_fraction_budget_wedge_v1.py --write",
            "check_command": "python3 proof/build_cycle_71_fraction_budget_wedge_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_71_fraction_budget_wedge_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 71 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 71 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 71 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
