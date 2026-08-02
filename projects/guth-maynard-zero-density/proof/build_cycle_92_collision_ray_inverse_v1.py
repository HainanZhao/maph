#!/usr/bin/env python3
"""Seal Cycle 92 equal-height collision-ray inverse lemma."""
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
OUTPUT = ROOT / "artifacts/cycle-92-collision-ray-inverse-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "discovery_candidate": (ROOT / "discovery/cycle-92-collision-ray-candidate-v1.md", "4a5e532c728007b1564f5e234d033347290076bbc88898a1eaf100242f8ba183"),
    "preregistration": (ROOT / "docs/cycle-92-collision-ray-preregistration-v1.md", "5dcddb85e5b74fc224fb9724a5337a20648430dfa85579b703519bce2a4014a1"),
    "document": (ROOT / "docs/cycle-92-collision-ray-inverse-v1.md", "ddc415c929318dec64040803ec83bafc7a31f865f522db7842266ee63036d6f7"),
    "conventions": (ROOT / "conventions/collision_ray_inverse_v1.py", "d79b735744abada4dfcb725c366e53dbdb7216df4a0cd7969a9a0a43df1df7fd"),
    "tests": (ROOT / "tests/test_cycle_92_collision_ray_inverse_v1.py", "b453cff66bdb549736566ded426273d01d5f6bb2a872df6aade4bdf237b5daea"),
    "cycle90": (ROOT / "artifacts/cycle-90-equal-height-bprocess-v1.json", "a24a63110e26fff4672c8b8e2cca27569a00885dec7b8c934f8ca3971967c3de"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 92 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("collision_ray_inverse_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 92 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["minimum_same_a_margin"] == "23/75", "same-a margin")
    require(rows["minimum_cross_a_margin"] == "28/75", "cross-a margin")
    require("q<<Q/M" in rows["multiplicity_contract"], "multiplicity contract")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle90"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_EQUAL_HEIGHT_BPROCESS_SADDLE_DISCREPANCY_OR_WEB_OPEN", "Cycle 90 status mismatch")
    return {"cycle90_role": "supply the saddle collision relation and lower-band parameter margins"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-92-collision-ray-inverse-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_EQUAL_HEIGHT_ANALYTIC_BOUND_OR_INJECTIVE_RAY_WEB_TO_E16_OPEN",
        "claim_boundary": "This artifact proves fixed-a ray uniqueness, cross-a injectivity, multiplicity versus primitive denominator, and dyadic web extraction. It proves no collision bound, transport seed, equal-height closure, full moment, density gain, or interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "ray_rigidity": {
            "epistemic_status": "PROVED",
            "statement": "All collisions at fixed a are multiples of one primitive rational ray, and distinct a values have distinct primitive labels.",
        },
        "inverse_output": {
            "epistemic_status": "PROVED",
            "statement": "C_tot collisions yield a dyadic multiplicity M, at least a constant times C_tot/(M log Q) distinct a values, and injective primitive labels of denominator O(Q/M).",
        },
        "analytic_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Prove C_tot<=Q X^epsilon, or compile the exported injective ray web into an original transport seed.",
        },
        "exact_replay": rows,
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_92_collision_ray_inverse_v1.py --write",
            "check_command": "python3 proof/build_cycle_92_collision_ray_inverse_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_92_collision_ray_inverse_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 92 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 92 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 92 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

