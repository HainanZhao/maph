#!/usr/bin/env python3
"""Seal Cycle 41 smooth annular sampling and signed-kernel reduction."""
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
OUTPUT = ROOT / "artifacts/cycle-41-annular-sampling-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-41-annular-sampling-preregistration-v1.md", "5998251a3429894921699e9abef65d5c57f8072f8d51098a8138cc6fb45eb3d7"),
    "document": (ROOT / "docs/cycle-41-annular-sampling-v1.md", "89d16d3ae1e1b3321887992e28efd798e1f243647abeee87662db33766aa9c02"),
    "conventions": (ROOT / "conventions/annular_sampling_v1.py", "b391baf436508211019b812425ea435033000819e864c92b4b574f3819dda111"),
    "tests": (ROOT / "tests/test_cycle_41_annular_sampling_v1.py", "80967c01dabdd19be26bae81012826c3246187abd108c59d2258c9f676fda1cb"),
    "cycle40": (ROOT / "artifacts/cycle-40-hollow-notch-v1.json", "d8a2c9cabc9834dc26ec7850e1f9268e136b2e2b13d1ddc6690195553b646254"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 41 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("annular_sampling_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 41 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["s3"]["leakage_margin"] == Fraction(7, 5), "s3 leakage margin")
    require(rows["s4"]["leakage_margin"] == Fraction(2, 5), "s4 leakage margin")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle40"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_GLOBAL_COHERENT_FLOOR_HOLLOW_NOTCH_OPEN", "Cycle 40 status mismatch")
    return {"prior_role": "construct the required notch instead of applying a raw positive global collision mean"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-41-annular-sampling-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_SMOOTH_ANNULAR_SAMPLING_SIGNED_COLLISION_OPEN",
        "claim_boundary": "This artifact proves smooth hollow sampling, leakage margins, and the exact signed annular kernel. It does not prove ASAM_s, a kernel count, a density gain, or an interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "sampling_reduction": {
            "epistemic_status": "PROVED",
            "statement": "A bandwidth-B exponential polynomial sampled on hollow Delta-separated rows is bounded by B times its enlarged-annulus mean square plus Schwartz leakage; N=9 makes total leakage power-negligible for s=3,4.",
        },
        "signed_kernel": {
            "epistemic_status": "PROVED",
            "statement": "The annular mean has kernel 2(sin(bu)-sin(au))/u, which changes sign and must not be replaced by its absolute value.",
        },
        "analytic_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Prove ASAM_3 or ASAM_4 by cancellation in the signed annular prime-monomial form.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_41_annular_sampling_v1.py --write",
            "check_command": "python3 proof/build_cycle_41_annular_sampling_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_41_annular_sampling_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 41 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 41 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 41 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
