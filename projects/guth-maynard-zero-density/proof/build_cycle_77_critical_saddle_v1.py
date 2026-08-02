#!/usr/bin/env python3
"""Seal Cycle 77 critical anchored-saddle reduction."""
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
OUTPUT = ROOT / "artifacts/cycle-77-critical-saddle-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "discovery_candidate": (ROOT / "discovery/cycle-77-critical-saddle-candidate-v1.md", "bc1933db171327605021f943cb46e80300e6aede04131e37f3edf792e8a2f3d5"),
    "preregistration": (ROOT / "docs/cycle-77-critical-saddle-preregistration-v1.md", "41e620dfbcedca71b02549c4358ea1b99be35583691f79781ce6011f2959e496"),
    "document": (ROOT / "docs/cycle-77-critical-saddle-v1.md", "5e5d9d4f439dfa7e1fe197ce451089e6c97677bc9fcf255be736a52d74751f05"),
    "conventions": (ROOT / "conventions/critical_saddle_v1.py", "59cbc753765509eedef3d338b117f69dc5a26d3d92c3f164a24dccb3fb8fc776"),
    "tests": (ROOT / "tests/test_cycle_77_critical_saddle_v1.py", "ee4d88231a4d521057dd575a0c41706144f58379d328cf4cd177914ff4830fdf"),
    "cycle76": (ROOT / "artifacts/cycle-76-hs-denominator-wedge-v1.json", "4f4c2c3a1829dd829f991147a41c22d8a75dc499c8c43e2d7ae0bed45b1a4219"),
    "cycle71_source_boundary": (ROOT / "artifacts/cycle-71-fraction-budget-wedge-v1.json", "f6711801f4f6b521a801933d6cfe596f2953821a56daa6baab206cb27557ef35"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 77 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("critical_saddle_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 77 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require("2/15" in rows["anchored_target"], "anchored target")
    require("17/75" in rows["ratio_loss"], "ratio loss")
    return rows


def validate_priors() -> dict[str, str]:
    cycle76 = json.loads(INPUTS["cycle76"][0].read_text(encoding="utf-8"))
    cycle71 = json.loads(INPUTS["cycle71_source_boundary"][0].read_text(encoding="utf-8"))
    require(cycle76.get("status") == "SEALED_DENOMINATOR_HS_WEDGE_CLOSED_TWOD_OR_SHIFTED_RESIDUAL_OPEN", "Cycle 76 status mismatch")
    require(cycle71.get("status") == "SEALED_FRACTION_WEDGE_2THETA_PLUS_KAPPA_LT_6_25_CLOSED", "Cycle 71 status mismatch")
    return {
        "cycle76_role": "supply the twice-compressed residual and unique surviving worst point",
        "cycle71_role": "supply the checked common-denominator source boundary",
    }


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-77-critical-saddle-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_CRITICAL_ANCHORED_SADDLE_ACSI_OR_PHASE_WEB_OPEN",
        "claim_boundary": "This artifact proves the anchored-saddle equivalence and exponent contracts at the unique worst cell. It proves no ACSI bound, full packet closure, seed extraction, powered saving, density gain, or interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_priors()},
        "discovery_quarantine": {
            "epistemic_status": "OBSERVED",
            "statement": "The exploratory candidate selected the anchored observable; all promoted identities and exponents were independently derived exactly.",
        },
        "anchored_reduction": {
            "epistemic_status": "PROVED",
            "statement": "Relative to one packet, the critical family is equivalent up to absolute tube constants to integer points within X^(-83/75) of n=c0*q*exp(2*pi*d/Delta), with target count X^(2/15).",
        },
        "ratio_boundary": {
            "epistemic_status": "PROVED",
            "statement": "The anchor-free ratio census has formal volume 37/75 against pair target 4/15, quantifying a 17/75 anchor loss.",
        },
        "source_boundary": {
            "epistemic_status": "OBSERVED",
            "statement": "Checked rational-point theorems use a common denominator; the direct embedding erases the anisotropic mesh and leaves a 4/5 exponent gap.",
        },
        "analytic_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Prove ACSI uniformly with exponent below 2/15, or turn every failure into a phase-bearing web for E16.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_77_critical_saddle_v1.py --write",
            "check_command": "python3 proof/build_cycle_77_critical_saddle_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_77_critical_saddle_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 77 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 77 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 77 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
