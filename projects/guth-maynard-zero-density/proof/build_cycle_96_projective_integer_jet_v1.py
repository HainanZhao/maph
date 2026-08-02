#!/usr/bin/env python3
"""Seal Cycle 96 quantitative projective integer-jet separation."""
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
OUTPUT = ROOT / "artifacts/cycle-96-projective-integer-jet-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "discovery_candidate": (ROOT / "discovery/cycle-96-integer-jet-candidate-v1.md", "450e5679ccc69556438f7f99af5520a27d088c5201066d001a961ab29f6f96a5"),
    "preregistration": (ROOT / "docs/cycle-96-integer-jet-preregistration-v1.md", "d034e8bc25187cca83076d67a888d0c9c991012eeb2b9edd61529c087f12867d"),
    "document": (ROOT / "docs/cycle-96-projective-integer-jet-v1.md", "ea2543fbf4b1d53c232cd1128baf112302ae0d361f2e359aac185c296ebf8cf6"),
    "conventions": (ROOT / "conventions/projective_integer_jet_v1.py", "0d35b0d628f4f6bcc674077fe79e646d50493eb68c707a4056ac4f3b992fbdc9"),
    "tests": (ROOT / "tests/test_cycle_96_projective_integer_jet_v1.py", "e1eb92220f90f92ea0297f1bc68dfe4806a34e4e253ffee8546e52ff2a51de9b"),
    "cycle95": (ROOT / "artifacts/cycle-95-projective-entropy-modes-v1.json", "73c1a220bd5bbacd2c813a7cbb36611c88bcc4e9e0e84bc8de97c95d6364128f"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 96 runtime mismatch")
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
    spec = importlib.util.spec_from_file_location("projective_integer_jet_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 96 conventions")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    record = module.theorem_record()
    require("J0=A-B-C" in record["integer_jets"], "constant jet mismatch")
    require("J1=B*a+C*b" in record["integer_jets"], "linear jet mismatch")
    require("x^2*S2/2" in record["cases"]["both_jets_zero"], "quadratic gap mismatch")
    require("no claim" in record["boundary"], "claim boundary mismatch")
    return record


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle95"][0].read_text(encoding="utf-8"))
    require(
        prior.get("status")
        == "SEALED_EXACT_ALIASES_CENTRAL_NEAR_PROJECTIVE_MODES_QUANTITATIVE_OPEN",
        "Cycle 95 status mismatch",
    )
    return {"cycle95_role": "supply the exact Laurent residual and central/noncentral split"}


def seal() -> dict[str, Any]:
    theorem = load_theorem()
    return {
        "artifact_id": "cycle-96-projective-integer-jet-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_INTEGER_JET_SMALL_MODE_SEPARATION_TURNOVER_SECTORS_OPEN",
        "claim_boundary": (
            "This artifact proves explicit lower bounds in four integer-jet sectors. "
            "It does not prove that they exhaust the Poisson support, a complete alias estimate, "
            "a moment theorem, a density gain, or an interval gain."
        ),
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "integer_jet_theorem": {"epistemic_status": "PROVED", **theorem},
        "actual_entropy_effect": {
            "epistemic_status": "PROVED",
            "statement": (
                "Under (A,B,C,a,b,x)=(p0n,p0n',q0m,u,u+v,2pi/D), "
                "the registered jet inequalities quantitatively separate noncentral modes."
            ),
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "Control the constant-jet large-displacement and negative-linear-jet "
                "turnover sectors, then reinsert all jet lower bounds into the oscillatory integral."
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_96_projective_integer_jet_v1.py --write",
            "check_command": "python3 proof/build_cycle_96_projective_integer_jet_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_96_projective_integer_jet_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 96 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 96 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 96 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
