#!/usr/bin/env python3
"""Seal Cycle 49 row-Fourier exceptional-set and absolute-pairing ledger."""
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
OUTPUT = ROOT / "artifacts/cycle-49-row-fourier-exceptional-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-49-row-fourier-exceptional-preregistration-v1.md", "c58609e10b2fb227f48fd5211da00ef51db413564dd4620f0ac341eff4902f82"),
    "document": (ROOT / "docs/cycle-49-row-fourier-exceptional-v1.md", "3e319b269e14c7b593b1f21edc5b5638f4b623e83c420ced0c2cc446e360651a"),
    "conventions": (ROOT / "conventions/row_fourier_exceptional_v1.py", "083c8520ab9abe71b5099ca07bad71439029d7b01a1e8715b0102a310bc313fa"),
    "tests": (ROOT / "tests/test_cycle_49_row_fourier_exceptional_v1.py", "72cc0b3b9723c0f510adb4d38d628be943a4e6bd5cdff28b11b49745e6907be6"),
    "cycle48": (ROOT / "artifacts/cycle-48-hs-joint-sieve-v1.json", "2c0522bee7f7d287dbadfc3d6268316a5f87a0c67725379ea399cfa1583d580f"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 49 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("row_fourier_exceptional_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 49 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["exceptional_measure_exponents"]["s4_margin"] == Fraction(-13, 50), "s4 exceptional measure")
    require(rows["absolute_lcam_gaps"]["s4_at_7_50"] == Fraction(39, 10), "absolute gap")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle48"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_AUXILIARY_S4_MARGIN_7_50_LCAM4_BRIDGE_OPEN", "Cycle 48 status mismatch")
    return {"prior_role": "separate the nonlattice row-Fourier budget from the structured Huxley--Sargos branch"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-49-row-fourier-exceptional-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_EXCEPTIONAL_MEASURE_SMALL_ABSOLUTE_PAIRING_FAILS_RRD_OPEN",
        "claim_boundary": "This artifact proves a scalar row-Fourier exceptional-set bound and an absolute-pairing obstruction. It does not prove RRD_s, LCAM_s, density, or interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "row_fourier_theorem": {
            "epistemic_status": "PROVED",
            "statement": "At target row size, the set where |R_C| exceeds R X^(-7/50) has measure at most X^(-13/50+o(1)).",
        },
        "scope_boundary": {
            "epistemic_status": "PROVED",
            "statement": "Absolute pairing with prime-monomial coefficient mass exceeds LCAM_4 by X^(39/10); a signed or L2 row--ratio discrepancy theorem is mandatory.",
        },
        "analytic_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Prove RRD_4 at coefficient-energy scale and combine it with the Cycle 48 structured exceptional branch.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_49_row_fourier_exceptional_v1.py --write",
            "check_command": "python3 proof/build_cycle_49_row_fourier_exceptional_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_49_row_fourier_exceptional_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 49 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 49 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 49 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
