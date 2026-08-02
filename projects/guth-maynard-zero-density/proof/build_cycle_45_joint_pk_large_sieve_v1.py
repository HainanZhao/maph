#!/usr/bin/env python3
"""Seal Cycle 45 joint p-k large-sieve and wrap de-aliasing ledger."""
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
OUTPUT = ROOT / "artifacts/cycle-45-joint-pk-large-sieve-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-45-joint-pk-large-sieve-preregistration-v1.md", "df573b2e354a9f38452a5431f873e8a5534f6b8f13f9e8b6a02a42f36155fc98"),
    "document": (ROOT / "docs/cycle-45-joint-pk-large-sieve-v1.md", "06cffe446a900c3a34b55f7bb86f56b591475e423f8eb9b5534945e140a648ce"),
    "conventions": (ROOT / "conventions/joint_pk_large_sieve_v1.py", "2098713c55c534e970566282d408ff1adc67c0cc3ca932f0355c86812cd43a1d"),
    "tests": (ROOT / "tests/test_cycle_45_joint_pk_large_sieve_v1.py", "79d479ba2b0d8a36da4f143f906934f753085e16809b71c037cde5bbc7c90e6a"),
    "cycle44": (ROOT / "artifacts/cycle-44-beatty-derivative-v1.json", "8271c9f5a84cc576a3ab088247697d341de67795f2bf04d7665e40e3b55177a7"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 45 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("joint_pk_large_sieve_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 45 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["naive_wrap_coloring"]["saving"] == Fraction(2, 25), "naive saving")
    require(rows["alias_threshold_for_4_25"] == Fraction(7, 11), "alias threshold")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle44"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_FIXED_BEATTY_AND_DERIVATIVE_TEST_INSUFFICIENT_JOINT_PK_OPEN", "Cycle 44 status mismatch")
    return {"prior_role": "replace one-variable derivative estimates by a joint prime-resonance large sieve"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-45-joint-pk-large-sieve-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_JOINT_PK_SAVING_2_25_WRAP_DEALIASING_OPEN",
        "claim_boundary": "This artifact proves wrap coloring, the checked classical large-sieve application, and the de-aliasing exponent ledger. It does not prove the de-aliasing target, a prime-pair bound, LCAM_s, density, or interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "joint_gain": {
            "epistemic_status": "PROVED",
            "statement": "At Fourier resolution 11/25, O(h) wrap coloring plus the separated-frequency large sieve gives joint-sum saving 2/25.",
        },
        "dealiasing_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Reduce effective wrap multiplicity from h to h^(7/11+o(1)) or better to recover saving 4/25.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_45_joint_pk_large_sieve_v1.py --write",
            "check_command": "python3 proof/build_cycle_45_joint_pk_large_sieve_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_45_joint_pk_large_sieve_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 45 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 45 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 45 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
