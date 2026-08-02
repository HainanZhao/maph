#!/usr/bin/env python3
"""Seal Cycle 58 strict hybrid-margin correction."""
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
OUTPUT = ROOT / "artifacts/cycle-58-strict-hybrid-margin-correction-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-58-strict-hybrid-margin-correction-preregistration-v1.md", "61d6794c7d79d35d216c19605ac340584b26c03a577f3e742796d38ba7929e6d"),
    "document": (ROOT / "docs/cycle-58-strict-hybrid-margin-correction-v1.md", "70d58388d1859a143eb6e77606db198f9b32dbe08359f6e0349bcef1eed084a4"),
    "conventions": (ROOT / "conventions/strict_hybrid_margin_correction_v1.py", "286a502f8d96f74b4c32e93e4571fae213a939d266616fb5c522a7c070914a7f"),
    "tests": (ROOT / "tests/test_cycle_58_strict_hybrid_margin_correction_v1.py", "b835e3c419531b3f902812bcc0bc96e4cf20c577bd0f242ea0eb131800096a5d"),
    "cycle54": (ROOT / "artifacts/cycle-54-coordinatewise-bessel-ledger-v1.json", "566e0c651c7fc95cf91719094702fe35a7156821fedac688cb96a6cf1f6362e0"),
    "cycle55": (ROOT / "artifacts/cycle-55-centered-trace-boundary-v1.json", "50a66a5d1aea0e9173e4c23bc8bf262e0c937b162a86942e957065635c6c53ab"),
    "cycle56": (ROOT / "artifacts/cycle-56-prime-edge-cumulant-v1.json", "3e38876a10cf4c5696b40eb69a77825569ec225566b6799f029f337cb4879d23"),
    "cycle57": (ROOT / "artifacts/cycle-57-cumulant-support-collapse-v1.json", "c2af9b4aa7c467c6e9d795eb0c7665b9769aa9e4c6187b3c0e9a7d5d94174e8d"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 58 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("strict_hybrid_margin_correction_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 58 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["tie"]["status"] == "TIES_NO_TRIGGER", "3/50 equality")
    require(rows["strict_surplus_example"]["adjusted_trigger_minus_selected"] == -Fraction(1, 1000), "strict surplus")
    require(rows["powered_tie"]["status"] == "TIES_NO_TRIGGER", "1/5 equality")
    return rows


def validate_priors() -> dict[str, str]:
    expected = {
        "cycle54": "SEALED_FULL_ORDINARY_EXPOSURE_OR_THREE_FIFTIETHS_HYBRID_REQUIRED",
        "cycle55": "SEALED_SCALAR_CENTERED_TRACES_SHARP_PRIME_CUMULANT_OPEN",
        "cycle56": "SEALED_EDGE_CUMULANT_SUPPORT_COLLAPSE_3_50_OPEN",
        "cycle57": "SEALED_HILBERT_EDGE_CUMULANT_RESTRICTION_3_50_OPEN",
    }
    for label, status in expected.items():
        prior = json.loads(INPUTS[label][0].read_text(encoding="utf-8"))
        require(prior.get("status") == status, f"{label} status mismatch")
    return {"affected_scope": "analytic target wording in Cycles 54--57; proved algebra unchanged"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-58-strict-hybrid-margin-correction-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_STRICT_GT_3_50_OR_ENDPOINT_MARGIN_REQUIRED",
        "claim_boundary": "This artifact corrects strict target wording only. It changes no proved Cycle 54--57 identity and proves no analytic, density, or interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "correction_scope": {"epistemic_status": "PROVED", **validate_priors()},
        "strictness_correction": {
            "epistemic_status": "PROVED",
            "statement": "A saving exactly 3/50 ties the strict trigger; closure needs >3/50 or an explicit endpoint margin. Standalone powered saving exactly 1/5 also ties.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_58_strict_hybrid_margin_correction_v1.py --write",
            "check_command": "python3 proof/build_cycle_58_strict_hybrid_margin_correction_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_58_strict_hybrid_margin_correction_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 58 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 58 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 58 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
