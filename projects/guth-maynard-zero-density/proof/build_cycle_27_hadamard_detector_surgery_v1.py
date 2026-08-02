#!/usr/bin/env python3
"""Seal Cycle 27 Hadamard detector-surgery dichotomy."""
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
OUTPUT = ROOT / "artifacts/cycle-27-hadamard-detector-surgery-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-27-hadamard-detector-surgery-preregistration-v1.md", "f4204657fada5c738f4f41137d63de35197c83e6a5f4fcd3245031c0dfd83ce3"),
    "document": (ROOT / "docs/cycle-27-hadamard-detector-surgery-v1.md", "2b400f80a28cfa650250064101121449e1cc4113716f69471d22d38793423aeb"),
    "conventions": (ROOT / "conventions/hadamard_detector_surgery_v1.py", "196f7ff2b0861aa2b3e895e5fc8b24738d6fbbab0dd07731e8e8ae37c9f30a52"),
    "tests": (ROOT / "tests/test_cycle_27_hadamard_detector_surgery_v1.py", "fca7a6659e49825de2263b5f2ca2b24187b0baf3f2890a500becb89f52ee5d98"),
    "cycle11": (ROOT / "artifacts/cycle-11-e1-e2-block-variance-v1.json", "fa6264fc8d040f0e0164b1256ec97f07a6637c7688b94f794096cb6bdef04a8a"),
    "cycle26": (ROOT / "artifacts/cycle-26-detector-reconstruction-v1.json", "6082d255ea07383913f30ceb5d9835e5f902245972d208af66b95acd27dcc64e"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_json(value: Any) -> Any:
    if isinstance(value, Fraction):
        return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    if isinstance(value, tuple):
        return [exact_json(item) for item in value]
    if isinstance(value, dict):
        return {str(key): exact_json(item) for key, item in value.items()}
    return value


def check_runtime() -> dict[str, Any]:
    runtime = {"implementation": platform.python_implementation(), "python": platform.python_version(), "optimization_level": sys.flags.optimize}
    require(runtime == EXPECTED_RUNTIME, "Cycle 27 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("hadamard_detector_surgery_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 27 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["hadamard"]["row_gram"][0][0] == 4, "Hadamard check mismatch")
    require(rows["parseval"]["complement_energy"] == rows["parseval"]["variance_energy"], "complement identity mismatch")
    require(rows["branches"]["high_variance"]["max_nontrivial_squared"] >= rows["branches"]["high_variance"]["forced_max_squared"], "surgery branch mismatch")
    return rows


def validate_prior() -> dict[str, str]:
    cycle11 = json.loads(INPUTS["cycle11"][0].read_text(encoding="utf-8"))
    cycle26 = json.loads(INPUTS["cycle26"][0].read_text(encoding="utf-8"))
    require(cycle11.get("status") == "SEALED_BLOCK_VARIANCE_DECOMPOSITION_RANK_ONE_COHERENT_SATURATION_RANDOM_COLOUR_EXPECTATION", "Cycle 11 status mismatch")
    require(cycle26.get("status") == "SEALED_INVERSE_LEVERAGE_DETECTOR_RECONSTRUCTION_EXACT_DEPENDENCE_OPEN", "Cycle 26 status mismatch")
    return {"prior_role": "block variance converted into an orthogonal signed-detector or multiblock-synchronization dichotomy"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-27-hadamard-detector-surgery-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_ORTHOGONAL_SIGNED_DETECTOR_OR_MULTIBLOCK_SYNCHRONIZATION",
        "claim_boundary": "This artifact proves an algebraic detector-surgery dichotomy for equal-mass prime blocks. It does not bound the synchronized branch, close the full large-values argument, prove the skeleton target, improve zero density, or improve intervals.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "orthogonal_surgery": {
            "epistemic_status": "PROVED",
            "statement": "Hadamard signings of equal-mass blocks are orthogonal equal-norm detector vectors; block variance forces a non-original detector value at least V/(4J).",
        },
        "synchronized_branch": {
            "epistemic_status": "PROVED",
            "statement": "Failure of complementary energy forces every aligned block contribution to have real part greater than 3V/(4J).",
            "analytic_status": "MULTIBLOCK_PRIME_LOG_BOUND_OPEN",
        },
        "remaining_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Bound separated rows simultaneously large and phase-aligned on every one of J=X^o(1) multiplicatively independent prime blocks.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_json(rows),
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_27_hadamard_detector_surgery_v1.py --write",
            "check_command": "python3 proof/build_cycle_27_hadamard_detector_surgery_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_27_hadamard_detector_surgery_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 27 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 27 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 27 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
