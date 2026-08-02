#!/usr/bin/env python3
"""Seal Cycle 33 v2 anchor-scope correction."""
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
OUTPUT = ROOT / "artifacts/cycle-33-anchor-aware-scope-correction-v2.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-33-anchor-aware-correction-preregistration-v2.md", "b9536c1e886ad82e3959cc942e2fd4f5fa877c515f299f31b9873921248e9b60"),
    "document": (ROOT / "docs/cycle-33-anchor-aware-scope-correction-v2.md", "64310900af26b85fa848fe9be2348621fc4a0f55f91e606aaa79074395833e18"),
    "conventions": (ROOT / "conventions/anchor_aware_scope_correction_v2.py", "da0c0dcd903e14b75559357f3d23fe70ae1ba09000012886b145d50ecd7932b0"),
    "tests": (ROOT / "tests/test_cycle_33_anchor_aware_scope_correction_v2.py", "52ef19bc5614329a1730f399a8f4aa860256a897c433418451110d3faf093642"),
    "cycle33_v1": (ROOT / "artifacts/cycle-33-anchor-aware-correction-v1.json", "6594393b00ff39f98b85d8eb1027dbf85187c6772ef97d9616d14a3a580b654d"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 33 v2 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("anchor_aware_scope_correction_v2", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 33 v2 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["one_anchor"]["kernel_lower"] == rows["one_anchor"]["evaluation_floor"] - rows["one_anchor"]["approximation_error"], "evaluation-floor inequality mismatch")
    require(rows["multi_anchor"]["l1_norm"] == 200, "multi-anchor instability mismatch")
    return rows


def validate_prior() -> dict[str, str]:
    v1 = json.loads(INPUTS["cycle33_v1"][0].read_text(encoding="utf-8"))
    cycle26 = json.loads(INPUTS["cycle26"][0].read_text(encoding="utf-8"))
    require(v1.get("status") == "SEALED_ANCHOR_WITNESS_UNIVERSAL_DISTANCE_GATE_FALSE", "Cycle 33 v1 status mismatch")
    require(cycle26.get("status") == "SEALED_INVERSE_LEVERAGE_DETECTOR_RECONSTRUCTION_EXACT_DEPENDENCE_OPEN", "Cycle 26 status mismatch")
    return {"v1_effect": "actual-prime witness retained; recurrence scope restricted to directions with an evaluation floor and stable anchor coefficients"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-33-anchor-aware-scope-correction-v2",
        "epistemic_status": "PROVED",
        "status": "SEALED_ANCHOR_RECURRENCE_EVALUATION_STABILITY_CORRECTION",
        "correction": "Anchor-span closeness yields useful recurrence only for a direction with a registered evaluation floor; multiple anchors additionally require coefficient stability.",
        "claim_effect": "The original rank-one detector b has the required floor sqrt(rho), so its one-anchor route remains valid. Adaptive rank-J directions require an additional overlap theorem.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "exact_replay": exact_json(rows),
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_33_anchor_aware_scope_correction_v2.py --write",
            "check_command": "python3 proof/build_cycle_33_anchor_aware_scope_correction_v2.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_33_anchor_aware_scope_correction_v2.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 33 v2 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 33 v2 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 33 v2 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
