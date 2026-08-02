#!/usr/bin/env python3
"""Seal Cycle 27 v2 prime-count remainder correction."""
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
OUTPUT = ROOT / "artifacts/cycle-27-hadamard-detector-surgery-correction-v2.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-27-hadamard-detector-surgery-correction-preregistration-v2.md", "82d05ead85aa9e929f9bf00be1836e3e9f23482b3e652f8c77280b0bc595e5cd"),
    "document": (ROOT / "docs/cycle-27-hadamard-detector-surgery-correction-v2.md", "23948482c0beb5af85a5ef56d216a72d4322afb84ccf30e53e885efe6e0ce0c3"),
    "conventions": (ROOT / "conventions/hadamard_detector_surgery_correction_v2.py", "5614d0d19a9501699dd13f2c78c4848f587f0b96b34f5de580496611d1083689"),
    "tests": (ROOT / "tests/test_cycle_27_hadamard_detector_surgery_correction_v2.py", "83027a322cadab6096bbb3930bf03578eae7f52b404d2b3cc8a1ed06d9ab02a8"),
    "cycle27_v1": (ROOT / "artifacts/cycle-27-hadamard-detector-surgery-v1.json", "4a62765a22c0a2ca7a70d5917925859029faad155827a031efee90918c703c53"),
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
    runtime = {"implementation": platform.python_implementation(), "python": platform.python_version(), "optimization_level": sys.flags.optimize}
    require(runtime == EXPECTED_RUNTIME, "Cycle 27 v2 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("hadamard_detector_surgery_correction_v2", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 27 v2 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["finite_remainder"]["discarded"] < rows["finite_remainder"]["blocks"], "remainder cap mismatch")
    require(rows["exponents"]["detector_relative_loss_exponent"] == Fraction(-7, 10), "detector loss mismatch")
    return rows


def validate_v1() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle27_v1"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_ORTHOGONAL_SIGNED_DETECTOR_OR_MULTIBLOCK_SYNCHRONIZATION", "Cycle 27 v1 status mismatch")
    return {"v1_effect": "conditional equal-mass theorem unchanged; arbitrary prime-count application repaired"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-27-hadamard-detector-surgery-correction-v2",
        "epistemic_status": "PROVED",
        "status": "SEALED_PRIME_COUNT_REMAINDER_CORRECTION_V1_THEOREM_UNCHANGED",
        "correction": "The v1 exposition omitted that the dyadic prime count need not be divisible by J. Retain J floor(M/J) coordinates and discard fewer than J.",
        "claim_effect": "For J=X^o(1), the detector-value and mass losses are o(1) relatively at the critical scales, so the v1 fixed-power conclusions survive with V replaced by V-O(J).",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_v1()},
        "exact_replay": exact_json(rows),
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_27_hadamard_detector_surgery_correction_v2.py --write",
            "check_command": "python3 proof/build_cycle_27_hadamard_detector_surgery_correction_v2.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_27_hadamard_detector_surgery_correction_v2.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 27 v2 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 27 v2 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 27 v2 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
