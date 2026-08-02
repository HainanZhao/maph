#!/usr/bin/env python3
"""Seal Cycle 40 global coherent-floor and hollow-notch reduction."""
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
OUTPUT = ROOT / "artifacts/cycle-40-hollow-notch-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-40-hollow-notch-preregistration-v1.md", "0a57c7d50b3260d13f9f4f9fb3f4ea2a8b8e7de7ffb6f651149b4d8abca5cdeb"),
    "document": (ROOT / "docs/cycle-40-hollow-notch-v1.md", "fad5f43c97ae75beb3b1208c8f923c4c566876141a07987b86f70fc69ea0b2e4"),
    "conventions": (ROOT / "conventions/hollow_notch_v1.py", "6cb017bb614ab855e19121710bc3568dd32038b2bec9ca9697e662a3992d57ae"),
    "tests": (ROOT / "tests/test_cycle_40_hollow_notch_v1.py", "308c792a7ce362c635097b4a8a903c4ec57252a81794a90e17e31b7cff8a5b9d"),
    "cycle39": (ROOT / "artifacts/cycle-39-moment-amplified-prime-monomial-v1.json", "3b83385d1d7e7ed447cafe0f7e42be1badb1bb26ba42cc458cf3fa3b8f204826"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 40 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("hollow_notch_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 40 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["s3"]["global_floor_excess_over_ampr"] == Fraction(19, 10), "s3 excess")
    require(rows["s4"]["global_floor_excess_over_ampr"] == Fraction(29, 10), "s4 excess")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle39"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_MOMENT_AMPLIFIED_PRIME_MONOMIAL_RESTRICTION_OPEN", "Cycle 39 status mismatch")
    return {"prior_role": "test whether raw global near-collision means can reach the hollow AMPR targets"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-40-hollow-notch-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_GLOBAL_COHERENT_FLOOR_HOLLOW_NOTCH_OPEN",
        "claim_boundary": "This artifact proves a global positive-kernel floor and a scoped route obstruction. It does not refute hollow AMPR_s or prove a kernel-count, density, or interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "coherent_floor": {
            "epistemic_status": "PROVED",
            "statement": "The triangular mean of F_(m,s) is at least M^(2s+2)/(12(s+m)); summed over m<=A its exponent is 2s+2.",
        },
        "route_obstruction": {
            "epistemic_status": "PROVED",
            "scope": "unmodified global positive-kernel mean-value proofs",
            "statement": "The coherent floor exceeds AMPR_3 by 19/10 and AMPR_4 by 29/10, so raw global near-collision counting is mis-scaled.",
        },
        "analytic_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Construct and bound a hollow/notched amplified restriction operator that removes the coherent zero packet before arithmetic collision analysis.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_40_hollow_notch_v1.py --write",
            "check_command": "python3 proof/build_cycle_40_hollow_notch_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_40_hollow_notch_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 40 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 40 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 40 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
