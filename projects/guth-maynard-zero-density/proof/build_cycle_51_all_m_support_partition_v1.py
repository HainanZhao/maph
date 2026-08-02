#!/usr/bin/env python3
"""Seal Cycle 51 all-harmonic support-partition factorization."""
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
OUTPUT = ROOT / "artifacts/cycle-51-all-m-support-partition-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-51-all-m-support-partition-preregistration-v1.md", "1e5752f1a7e26035a4832dbd676eded8800c08dfe18fa29fc83c62d339bcd376"),
    "document": (ROOT / "docs/cycle-51-all-m-support-partition-v1.md", "9c9617658447ab364a32c9a0c2cf4dff9da220220d817386b78850ca64885260"),
    "conventions": (ROOT / "conventions/all_m_support_partition_v1.py", "adab258a9103cf81a9ade5a7c66c325f696ac90bc64d15094441736cff0f7348"),
    "tests": (ROOT / "tests/test_cycle_51_all_m_support_partition_v1.py", "91cbb0126aad646133c6f2b7d7da5e40947e3375d9b4fabd6d519050159f6455"),
    "cycle50": (ROOT / "artifacts/cycle-50-support-kernel-factorization-v1.json", "ed68a75b1e6d191e23528fb23b1e7e41e7919e1e16bbc09d178a2ed71c72aaab"),
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
    if isinstance(value, (list, tuple)):
        return [exact_json(item) for item in value]
    return value


def check_runtime() -> dict[str, Any]:
    runtime = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
    }
    require(runtime == EXPECTED_RUNTIME, "Cycle 51 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("all_m_support_partition_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 51 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["criterion"] == "lambda partitions s+m and max(lambda)>=m", "support criterion")
    require(len(rows["registered_small_m"]) == 5, "small-m registry")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle50"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_FACTORED_DIFFERENCE_KERNEL_DK4_PLUS_SMALL_M_OPEN", "Cycle 50 status mismatch")
    return {"prior_role": "close the finite small-harmonic collision exception by exponent-partition algebra"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-51-all-m-support-partition-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_ALL_HARMONIC_SUPPORT_KERNEL_ADK4_OPEN",
        "claim_boundary": "This artifact proves the all-m support criterion and its power-sum factorization. It does not prove ADK_s, AMPR_s, LCAM_s, density, or interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "support_classification": {
            "epistemic_status": "PROVED",
            "statement": "For every m>=2, the support is the sum of monomial symmetric functions indexed by partitions lambda of s+m with max(lambda)>=m.",
        },
        "power_sum_factorization": {
            "epistemic_status": "PROVED",
            "statement": "Set-partition Mobius inversion expresses every all-m support correlation as an explicit finite polynomial in K(jh), j<=s+m.",
        },
        "analytic_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Prove the all-harmonic factored difference-kernel estimate ADK_4 on hollow separated rows.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_51_all_m_support_partition_v1.py --write",
            "check_command": "python3 proof/build_cycle_51_all_m_support_partition_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_51_all_m_support_partition_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 51 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 51 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 51 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
