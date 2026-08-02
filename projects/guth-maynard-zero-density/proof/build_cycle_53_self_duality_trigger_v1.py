#!/usr/bin/env python3
"""Seal Cycle 53 one-shot self-duality trigger ledger."""
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
OUTPUT = ROOT / "artifacts/cycle-53-self-duality-trigger-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-53-self-duality-trigger-preregistration-v1.md", "bbb756668134df98fc6172c3949ba34c8413914fb3eb2b1543855eefa205818a"),
    "document": (ROOT / "docs/cycle-53-self-duality-trigger-v1.md", "ea81409dd2d99c16b2b71b3809e8f4e109048d658b8b5b47c618de429cc8f616"),
    "conventions": (ROOT / "conventions/self_duality_trigger_v1.py", "3b992431a3a3c290a868c298c4b5d9d47fda270d7a1e8360b4f0a8000b84a458"),
    "tests": (ROOT / "tests/test_cycle_53_self_duality_trigger_v1.py", "289692e84650a2a7415566ba59ad34a7d3d1c11d0b86cddc8c11c9f3c2b9901a"),
    "cycle52": (ROOT / "artifacts/cycle-52-support-kernel-self-duality-v1.json", "bec97f88a9d9602d28cb5ee528dab803c854022c35f8c3fd9187c302bc793cc6"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 53 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("self_duality_trigger_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 53 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["s3"]["trigger_gap"] == Fraction(11, 5), "s3 gap")
    require(rows["s4"]["trigger_gap"] == Fraction(16, 5), "s4 gap")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle52"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_TWO_SCALE_SELF_DUALITY_POPULAR_DIFFERENCE_STRUCTURE_OPEN", "Cycle 52 status mismatch")
    return {"prior_role": "check whether AMPR failure reaches the one-shot support-correlation trigger"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-53-self-duality-trigger-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_ONE_SHOT_TRIGGER_INSUFFICIENT_MULTILINEAR_TRIGGER_OPEN",
        "claim_boundary": "This artifact proves the one-shot trigger gaps only. It does not obstruct multilinear or centered-trace uses of self-duality and proves no analytic or density gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "trigger_boundary": {
            "epistemic_status": "PROVED",
            "statement": "After harmonic selection, AMPR failure lies below the one-shot Halasz--Montgomery off-diagonal trigger by 11/5 for s=3 and 16/5 for s=4.",
        },
        "analytic_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Expose prime coordinates successively or use a centered higher trace, then apply the Cycle 52 inverse recurrence.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_53_self_duality_trigger_v1.py --write",
            "check_command": "python3 proof/build_cycle_53_self_duality_trigger_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_53_self_duality_trigger_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 53 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 53 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 53 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
