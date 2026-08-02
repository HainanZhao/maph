#!/usr/bin/env python3
"""Seal Cycle 97 projective algebraic-root inverse atlas."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-97-projective-algebraic-root-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "discovery_candidate": (ROOT / "discovery/cycle-97-algebraic-root-candidate-v1.md", "bf279f0fc3fa1908ad4572fa31efe3dda26a74fab1e513e29eb04b1eca4fa027"),
    "preregistration": (ROOT / "docs/cycle-97-algebraic-root-preregistration-v1.md", "23fcb8ca2fa987eec53da39a80f6ed7e191ccc6ac735b3f3ac0c76d623b4df7e"),
    "document": (ROOT / "docs/cycle-97-projective-algebraic-root-v1.md", "62aee801e3ee2a4da37acdd085425d15793396844d489588d97c2961e8b09f72"),
    "conventions": (ROOT / "conventions/projective_algebraic_root_v1.py", "495191976af5fd9e14445b3b92aec16382432844d6c5732e97d1a6048c0ba588"),
    "tests": (ROOT / "tests/test_cycle_97_projective_algebraic_root_v1.py", "aa377f29f1b11b56d47abb9d3ecfcddcbba4aa1379eb2ee6c89ed8eba55d1af7"),
    "cycle96": (ROOT / "artifacts/cycle-96-projective-integer-jet-v1.json", "4ab624c4d2edd837ca4c70ce7ae6067982e5c846798a855f89931340d3485683"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_runtime() -> dict[str, Any]:
    runtime = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
    }
    require(runtime == EXPECTED_RUNTIME, "Cycle 97 runtime mismatch")
    return runtime


def frozen_inputs() -> dict[str, dict[str, str]]:
    result = {}
    for label, (path, expected) in INPUTS.items():
        require(path.is_file(), f"missing frozen input: {label}")
        actual = sha256(path)
        require(actual == expected, f"frozen input hash mismatch: {label}")
        result[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual}
    return result


def load_theorem() -> dict[str, object]:
    path = INPUTS["conventions"][0]
    spec = importlib.util.spec_from_file_location("projective_algebraic_root_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 97 conventions")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    record = module.theorem_record()
    require("deg(P)<=2*M" == record["polynomial_contract"]["degree"], "degree contract")
    require("at most two" in record["shape"]["root_count"], "root count")
    require("2*delta/eta" in record["inverse"]["simple"], "Newton radius")
    require("no effective lower bound" in record["boundary"], "claim boundary")
    return record


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle96"][0].read_text(encoding="utf-8"))
    require(
        prior.get("status")
        == "SEALED_INTEGER_JET_SMALL_MODE_SEPARATION_TURNOVER_SECTORS_OPEN",
        "Cycle 96 status mismatch",
    )
    return {"cycle96_role": "supply the integer jets and identify the turnover sectors"}


def seal() -> dict[str, Any]:
    theorem = load_theorem()
    return {
        "artifact_id": "cycle-97-projective-algebraic-root-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_ALGEBRAIC_ROOT_OR_NEAR_DOUBLE_INVERSE_EFFECTIVE_SEPARATION_OPEN",
        "claim_boundary": (
            "This artifact proves the algebraic-root encoding and local simple-root/near-double-root "
            "inverse. It proves no effective entropy linear-form lower bound, support exhaustion, "
            "complete alias estimate, moment theorem, density gain, or interval gain."
        ),
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "inverse_theorem": {"epistemic_status": "PROVED", **theorem},
        "actual_entropy_effect": {
            "epistemic_status": "PROVED",
            "statement": (
                "Every sufficiently small residual is routed either to an algebraic alpha with "
                "|D log(alpha)-2pi|<=2D delta/eta or to an explicit near-double-root certificate."
            ),
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "Determine whether an effective linear-form estimate closes the simple-root rows "
                "on actual support and count the explicit critical-point rows."
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_97_projective_algebraic_root_v1.py --write",
            "check_command": "python3 proof/build_cycle_97_projective_algebraic_root_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_97_projective_algebraic_root_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 97 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 97 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 97 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
