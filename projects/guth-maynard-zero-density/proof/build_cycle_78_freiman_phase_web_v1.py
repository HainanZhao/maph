#!/usr/bin/env python3
"""Seal Cycle 78 exact Freiman phase-web rigidity."""
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
OUTPUT = ROOT / "artifacts/cycle-78-freiman-phase-web-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-78-freiman-phase-web-preregistration-v1.md", "87188e407b4877f1700ccdb06d5ae7b952daa8dfc83c8440721203e9d0b77556"),
    "document": (ROOT / "docs/cycle-78-freiman-phase-web-v1.md", "15be85dcea0d252aa52e317a84b4f82cc82e90665c9c9e034d8e9fbd4b849256"),
    "conventions": (ROOT / "conventions/freiman_phase_web_v1.py", "ad3c228b6b283786afd3589b3664035c7b526a52617e4ae91d3cd71b4e79ba3f"),
    "tests": (ROOT / "tests/test_cycle_78_freiman_phase_web_v1.py", "ec4294a1bca2804b0e1905b16b0e8705e0cb9505cecee706ca441512b2aa70ee"),
    "cycle77": (ROOT / "artifacts/cycle-77-critical-saddle-v1.json", "c68cc89eb163d81d85374a61986c62c4004f1b5c195a5088a7063fb9ed670dbd"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 78 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("freiman_phase_web_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 78 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require("-8/75" in rows["cross_error"], "integer-forcing margin")
    require("O(log Q)" in rows["progression_length"], "progression length")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle77"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_CRITICAL_ANCHORED_SADDLE_ACSI_OR_PHASE_WEB_OPEN", "Cycle 77 status mismatch")
    return {"cycle77_role": "supply the critical packet scales, anchored form, and ratio error"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-78-freiman-phase-web-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_EXACT_FREIMAN_WEB_OR_SPARSE_ACSI_OPEN",
        "claim_boundary": "This artifact proves exact additive-to-multiplicative relation transfer and logarithmic length for complete arithmetic progressions of critical hits. It does not force relations in a sparse packet set and proves no ACSI, packet closure, powered saving, density gain, or interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "freiman_transfer": {
            "epistemic_status": "PROVED",
            "statement": "Every additive quadruple of hit indices yields exact multiplicative equality of reduced rational labels, with integer-forcing margin X^(-8/75+o(1)).",
        },
        "progression_rigidity": {
            "epistemic_status": "PROVED",
            "statement": "A complete arithmetic progression maps to r_j=r_0*g^j and has length O(log Q).",
        },
        "scope_boundary": {
            "epistemic_status": "PROVED",
            "statement": "At target cardinality X^(2/15), additive-energy pigeonholing need not produce any nontrivial relation; sparse Sidon-type sets remain an analytic branch.",
        },
        "analytic_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Route relation-rich ACSI failures into valuation webs, and prove ACSI on the relation-poor branch.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_78_freiman_phase_web_v1.py --write",
            "check_command": "python3 proof/build_cycle_78_freiman_phase_web_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_78_freiman_phase_web_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 78 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 78 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 78 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
