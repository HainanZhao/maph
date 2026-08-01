#!/usr/bin/env python3
"""Seal Cycle 13 source obstruction and weighted fractional-tensor results."""
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
OUTPUT = ROOT / "artifacts/cycle-13-source-obstruction-weighted-tensor-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-13-source-obstruction-weighted-tensor-preregistration-v1.md", "da127f1d34088bae8217079409f9db2b0fe6f8a7525d220ca1a21934424e5e9b"),
    "document": (ROOT / "docs/cycle-13-source-obstruction-weighted-tensor-v1.md", "bc28eb1bd8007ce7625b1e81ab1aacbb2ba4a505da181ec36c19eb0fe8f44cb8"),
    "conventions": (ROOT / "conventions/weighted_fractional_tensor_v1.py", "61d2ad19f57e3fe3a53da5dc1f19fd845e423ff8a2805e4d2c74b7ca793e6fef"),
    "tests": (ROOT / "tests/test_cycle_13_source_obstruction_weighted_tensor_v1.py", "194e6da8840faebc4bdb278d4ad7a47d215f2d871151031681ffe7e08add5526"),
    "gm_source": (ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex", "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"),
    "heath_brown_source": (ROOT / "artifacts/sources/heath-brown-1982-generalized-vaughan-identity.pdf", "b32e586d26dac73cb36a4f6dc7c6a7bf08ea5fa88e8ef8b18a8df2d5e849a807"),
    "cycle12_artifact": (ROOT / "artifacts/cycle-12-balanced-five-factor-v1.json", "2c57bd1f621d7474cea68fd07cd8719c0f8f64c4766cf2cd7fbfcd765921d24d"),
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
    if isinstance(value, list):
        return [exact_json(item) for item in value]
    if isinstance(value, dict):
        return {str(key): exact_json(item) for key, item in value.items()}
    return value


def check_runtime() -> dict[str, Any]:
    runtime = {"implementation": platform.python_implementation(), "python": platform.python_version(), "optimization_level": sys.flags.optimize}
    require(runtime == EXPECTED_RUNTIME, "Cycle 13 requires non-optimized CPython 3.12.3")
    return runtime


def frozen_inputs() -> dict[str, dict[str, str]]:
    frozen = {}
    for label, (path, expected) in INPUTS.items():
        require(path.is_file(), f"missing frozen input: {label}")
        actual = sha256(path)
        require(actual == expected, f"frozen input hash mismatch: {label}")
        frozen[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual}
    return frozen


def load_conventions():
    path = INPUTS["conventions"][0]
    spec = importlib.util.spec_from_file_location("weighted_fractional_tensor_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 13 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_sources() -> dict[str, str]:
    source = INPUTS["gm_source"][0].read_text(encoding="utf-8")
    for needle in (
        "d|n\\\\ d\\le 2T^{1/100}",
        "\\mu(d)",
        "\\exp\\Bigl(-\\frac{n}{T^{1/2}}\\Bigr)",
        "\\tilde{b}_n:=\\Bigl(\\frac{N}{n}\\Bigr)^\\sigma b_n",
    ):
        require(needle in source, f"missing Guth--Maynard source anchor: {needle}")
    cycle12 = json.loads(INPUTS["cycle12_artifact"][0].read_text(encoding="utf-8"))
    require(cycle12.get("artifact_id") == "cycle-12-balanced-five-factor-v1", "Cycle 12 artifact mismatch")
    return {
        "gm_detector": "TeX lines 2309--2315",
        "gm_normalization": "TeX lines 2328--2330",
        "heath_brown_scope": "Pinned primary PDF is reconnaissance for a later detector identity; no theorem is imported here.",
    }


def seal() -> dict[str, Any]:
    module = load_conventions()
    rows = module.verify_all()
    grid = rows["grid"]
    require(grid["checked"] == 1442, "grid count mismatch")
    require(grid["strict_gain"] == 927, "strict-gain count mismatch")
    require(rows["registered_unbalanced"]["tau"] == Fraction(1, 3), "registered unbalanced tau mismatch")
    return {
        "artifact_id": "cycle-13-source-obstruction-weighted-tensor-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_SOURCE_OBSTRUCTION_CELLWISE_WEIGHTED_GAIN_ROUGH_REMAINDER_OPEN",
        "claim_boundary": "This artifact disproves exact full-detector decomposition into fivefold convolutions supported above one and proves a conditional cellwise weighted-moment theorem. It does not prove a zeta density gain, a prime-interval improvement, a source-valid replacement detector, transformed coefficient norms, or a complete envelope.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "source_context": {"epistemic_status": "PROVED", **validate_sources()},
        "source_obstruction": {
            "epistemic_status": "PROVED",
            "statement": "Above the truncation cutoff the current detector has nonzero prime coefficients, while every sum of fivefold convolutions with all factors supported on integers >=2 vanishes at primes.",
            "scope": "Exact full-coefficient equality only; no large-value assertion about the prime remainder.",
        },
        "weighted_fractional_tensor": {
            "epistemic_status": "PROVED",
            "conditional_on": "For every selected transformed moment, coefficient-square norm <=v^(12+o(1)) and the standard length-v^12 discrete mean-value input.",
            "design": "A probability distribution on integer increments k with y dot k<=2 and E(k_i)=tau for every i.",
            "pointwise_identity": "weighted geometric mean |B_k|=|A|^(2+tau)",
            "local_row_exponent": "10-7tau",
            "strict_gain_criterion": "tau>2/7",
            "universal_upper_bound": "tau<=2/5",
        },
        "singleton_design": {
            "epistemic_status": "PROVED",
            "statement": "For max y_i<=2, q_i=floor(2/y_i) and weights proportional to 1/q_i give tau=1/sum_i(1/q_i).",
            "registered_unbalanced": "(1/2,1/2,1,3/2,3/2) gives tau=1/3, local exponent 23/3, and gain 1/3.",
            "optimality": "NOT_CLAIMED",
        },
        "grid_census": {"epistemic_status": "PROVED", **exact_json(grid)},
        "source_redesign": {
            "epistemic_status": "CONJECTURED",
            "next_gate": "Derive a source-valid product-cell identity for a prime-weighted or logarithmic-derivative detector, prove transformed coefficient norms cell by cell, and control cells with tau<=2/7 or y_i>2.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_json(rows),
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_13_source_obstruction_weighted_tensor_v1.py --write",
            "check_command": "python3 proof/build_cycle_13_source_obstruction_weighted_tensor_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_13_source_obstruction_weighted_tensor_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 13 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 13 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 13 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
