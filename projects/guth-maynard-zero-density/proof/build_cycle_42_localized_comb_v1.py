#!/usr/bin/env python3
"""Seal Cycle 42 localized-comb row-resonance reduction."""
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
OUTPUT = ROOT / "artifacts/cycle-42-localized-comb-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-42-localized-comb-preregistration-v1.md", "a5edb486916bdea0a6867a725ece0d6d6e0c3d51be6975084d8391dda343f246"),
    "document": (ROOT / "docs/cycle-42-localized-comb-v1.md", "caa9f4bce6e57ec94054d8ad495abe722e416914333dbdc7af8b3e70ababc5d7"),
    "conventions": (ROOT / "conventions/localized_comb_v1.py", "ba534f803cb178c3751d4f7fab83eaf2283aa0506fc010e76b9554875ca987c1"),
    "tests": (ROOT / "tests/test_cycle_42_localized_comb_v1.py", "342df25915e075ec54467dabaf3a63fb00a7e5472f62041cb19e37b2aee2160b"),
    "cycle41": (ROOT / "artifacts/cycle-41-annular-sampling-v1.json", "b10715ee78b090b432b0b2f928eb20153967b162ace7c9323df9e42e290de343"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 42 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("localized_comb_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 42 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["s3"]["full_annulus_relaxation_loss"] == Fraction(9, 10), "relaxation loss")
    require(rows["s3"]["localized_diagonal_vector"] == Fraction(61, 10), "s3 diagonal")
    require(rows["s4"]["localized_diagonal_vector"] == Fraction(71, 10), "s4 diagonal")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle41"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_SMOOTH_ANNULAR_SAMPLING_SIGNED_COLLISION_OPEN", "Cycle 41 status mismatch")
    return {"prior_role": "retain the exact localized sampling weight rather than spend the full-annulus relaxation loss"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-42-localized-comb-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_LOCALIZED_COMB_DIAGONAL_SHARP_ROW_RESONANCE_OPEN",
        "claim_boundary": "This artifact proves the localized-comb identities, Fourier factorization, relaxation loss, and diagonal ledger. It does not prove LCAM_s, a kernel count, a density gain, or an interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "comb_correction": {
            "epistemic_status": "PROVED",
            "statement": "Replacing the localized comb by B times the full annulus loses exponent 9/10, exceeding both closure margins.",
        },
        "row_resonance": {
            "epistemic_status": "PROVED",
            "statement": "The localized form factors into prime-monomial coefficient pairs, a smooth frequency cutoff, and the row Fourier sum R_C(log(n/n')).",
        },
        "analytic_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Bound LCAM_3 or LCAM_4 at the diagonal exponent s+31/10 without replacing R_C by its cardinality.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_42_localized_comb_v1.py --write",
            "check_command": "python3 proof/build_cycle_42_localized_comb_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_42_localized_comb_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 42 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 42 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 42 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
