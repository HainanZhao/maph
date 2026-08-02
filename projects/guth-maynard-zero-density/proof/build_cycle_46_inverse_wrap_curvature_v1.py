#!/usr/bin/env python3
"""Seal Cycle 46 inverse-wrap near-lattice curvature reduction."""
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
OUTPUT = ROOT / "artifacts/cycle-46-inverse-wrap-curvature-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-46-inverse-wrap-curvature-preregistration-v1.md", "57d1bdbdb6f7f558b31b9410c72a36a5ef8e1e9252275158add879d8ea5c7de6"),
    "document": (ROOT / "docs/cycle-46-inverse-wrap-curvature-v1.md", "24feac3eaf8d66f9f1ac291d613b014d327b8a6a88317f817fce72b639f5c8db"),
    "conventions": (ROOT / "conventions/inverse_wrap_curvature_v1.py", "cd85b91416d0605819012c42db84afc3c20efa6bc8abb838328ac137b064906c"),
    "tests": (ROOT / "tests/test_cycle_46_inverse_wrap_curvature_v1.py", "bb526482bc28ee114f5395d353ce22c95431a0ceea35a4d95a4eacdbbb515017"),
    "cycle45": (ROOT / "artifacts/cycle-45-joint-pk-large-sieve-v1.json", "7927eab818a98871417d94ef595310de4cb0c3ef1eb9eea5293328a1f5edeabf"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 46 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("inverse_wrap_curvature_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 46 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    row = rows["critical_inverse_curve"]
    require(row["curvature"] == Fraction(-7, 25), "curvature")
    require(row["tube_width"] == Fraction(-21, 25), "tube width")
    require(row["target_count"] == Fraction(7, 25), "target count")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle45"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_JOINT_PK_SAVING_2_25_WRAP_DEALIASING_OPEN", "Cycle 45 status mismatch")
    return {"prior_role": "translate the h^(7/11) wrap de-aliasing gate into an exact near-lattice curve count"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-46-inverse-wrap-curvature-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_INVERSE_LOG_CURVE_RECIPROCAL_CURVATURE_OPEN",
        "claim_boundary": "This artifact proves the inverse-wrap equivalence and exact curvature/tube/count ledger. It does not prove ILC, de-aliasing, LCAM_s, density, or interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "inverse_wrap": {
            "epistemic_status": "PROVED",
            "statement": "Frequency clustering in a 1/X arc is equivalent up to absolute window constants to near-integer points on (Delta/2pi)log(1+(j+beta)/h).",
        },
        "critical_transition": {
            "epistemic_status": "PROVED",
            "statement": "At h=X^(11/25), curvature is X^(-7/25), tube width X^(-21/25), and the required count X^(7/25) equals reciprocal curvature scale.",
        },
        "analytic_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Prove the uniform inverse-log near-lattice count ILC at h^(7/11+o(1)), or use nonlattice row decay.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_46_inverse_wrap_curvature_v1.py --write",
            "check_command": "python3 proof/build_cycle_46_inverse_wrap_curvature_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_46_inverse_wrap_curvature_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 46 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 46 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 46 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
