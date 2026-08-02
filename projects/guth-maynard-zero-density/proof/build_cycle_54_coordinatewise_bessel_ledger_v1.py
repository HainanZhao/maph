#!/usr/bin/env python3
"""Seal Cycle 54 conditional coordinatewise-Bessel design ledger."""
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
OUTPUT = ROOT / "artifacts/cycle-54-coordinatewise-bessel-ledger-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-54-coordinatewise-bessel-preregistration-v1.md", "1022ec13babf7ae1a2f44b3c938db3524d311bc9badd2dbdbcb119a4b40e57fa"),
    "document": (ROOT / "docs/cycle-54-coordinatewise-bessel-v1.md", "f68b46b18fcf7649f531126cb926af8ea3be8efdcda65e1630ba0f7b842db706"),
    "conventions": (ROOT / "conventions/coordinatewise_bessel_ledger_v1.py", "59d1e0a0fd15927073ab032a49e1c3583e68601d563455202217822ee8a1b398"),
    "tests": (ROOT / "tests/test_cycle_54_coordinatewise_bessel_ledger_v1.py", "1f76cd0354d6a415cb78fd4eac4c370207ec4f5d3de152d95aaf81bb909adb18"),
    "cycle53": (ROOT / "artifacts/cycle-53-self-duality-trigger-v1.json", "fefe66bf2b3d65835d0b187afc4fc7ea3e53f9953d701f7dcd29943ed921484e"),
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
    if isinstance(value, list):
        return [exact_json(item) for item in value]
    return value


def check_runtime() -> dict[str, Any]:
    runtime = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
    }
    require(runtime == EXPECTED_RUNTIME, "Cycle 54 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("coordinatewise_bessel_ledger_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 54 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    for key in ("s3", "s4"):
        data = rows[key]
        s = data["s"]
        require(data["with_q_saving"][s - 1]["signed_gap_trigger_minus_selected"] == Fraction(3, 50), "penultimate gap")
        require(data["with_q_saving"][s]["signed_gap_trigger_minus_selected"] == -Fraction(47, 50), "full margin")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle53"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_ONE_SHOT_TRIGGER_INSUFFICIENT_MULTILINEAR_TRIGGER_OPEN", "Cycle 53 status mismatch")
    return {"prior_role": "quantify the coordinatewise redesign required by the one-shot trigger gap"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-54-coordinatewise-bessel-ledger-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_FULL_ORDINARY_EXPOSURE_OR_THREE_FIFTIETHS_HYBRID_REQUIRED",
        "claim_boundary": "This artifact proves an exact conditional design ledger. It does not prove the coordinatewise Bessel contract, transplant the Cycle 48 saving analytically, or prove AMPR, density, or interval gains.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "design_theorem": {
            "epistemic_status": "PROVED",
            "statement": "Under the frozen coordinatewise contract, s-1 ordinary contractions plus 7/50 miss by 3/50, while all s contractions trigger with margin 47/50 for s=3,4.",
        },
        "analytic_contract": {
            "epistemic_status": "CONJECTURED",
            "statement": "A source-valid sequential Bessel inequality removes one support power for every exposed ordinary prime and retains the powered-coordinate 7/50 saving.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_54_coordinatewise_bessel_ledger_v1.py --write",
            "check_command": "python3 proof/build_cycle_54_coordinatewise_bessel_ledger_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_54_coordinatewise_bessel_ledger_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 54 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 54 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 54 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
