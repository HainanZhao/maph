#!/usr/bin/env python3
"""Seal Cycle 52 support-kernel self-duality and inverse recurrence."""
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
OUTPUT = ROOT / "artifacts/cycle-52-support-kernel-self-duality-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-52-support-kernel-self-duality-preregistration-v1.md", "e1e0731696370f06987d61e939e6e2c9471ce5bc47db0e7ceaa315a846b4bd39"),
    "document": (ROOT / "docs/cycle-52-support-kernel-self-duality-v1.md", "bdaef9db6d9f224ab81bc3d32079de520b3080b355097eeb445a7919b4e6d1cd"),
    "conventions": (ROOT / "conventions/support_kernel_self_duality_v1.py", "b51a06f5f60e1cdf7a082e377ad54a3151dedbc15d929d2628e44b76a478b408"),
    "tests": (ROOT / "tests/test_cycle_52_support_kernel_self_duality_v1.py", "63d883baaf19a046d6a6dc888817852bdff609c5027c668ab978b9a6c62528d3"),
    "cycle51": (ROOT / "artifacts/cycle-51-all-m-support-partition-v1.json", "3608f1e6048d13dfbd8a8e619127518c4355bcc5dd80e578498014e8e0a20304"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 52 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("support_kernel_self_duality_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 52 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["collision_gap"] == Fraction(1), "collision gap")
    require(rows["inverse_s4_at_7_50"]["K_h_max_deficit"] == Fraction(7, 200), "inverse deficit")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle51"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_ALL_HARMONIC_SUPPORT_KERNEL_ADK4_OPEN", "Cycle 51 status mismatch")
    return {"prior_role": "extract the universal top distinct-prime stratum and derive its two-scale inverse recurrence"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-52-support-kernel-self-duality-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_TWO_SCALE_SELF_DUALITY_POPULAR_DIFFERENCE_STRUCTURE_OPEN",
        "claim_boundary": "This artifact proves the support-kernel leading term and inverse deficit implication. It does not prove popularity, additive structure, ADK_s, AMPR_s, LCAM_s, density, or interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "self_duality": {
            "epistemic_status": "PROVED",
            "statement": "Uniformly in m>=2, the support correlation is K(mh)K(h)^s/s! plus O_s(M^s), a full prime-coordinate power below the main scale.",
        },
        "inverse_recurrence": {
            "epistemic_status": "PROVED",
            "statement": "Correlation deficit eta<1 forces s alpha+beta<=eta+o(1); at s=4, eta=7/50 forces K(h) deficit at most 7/200 and K(mh) deficit at most 7/50.",
        },
        "analytic_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Convert a large off-diagonal into popular two-scale difference edges and then into progression-like structure or a nonlattice saving.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_52_support_kernel_self_duality_v1.py --write",
            "check_command": "python3 proof/build_cycle_52_support_kernel_self_duality_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_52_support_kernel_self_duality_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 52 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 52 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 52 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
