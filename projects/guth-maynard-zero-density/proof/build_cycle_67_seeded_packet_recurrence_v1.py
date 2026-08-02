#!/usr/bin/env python3
"""Seal Cycle 67 seeded deep-packet recurrence lemma."""
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
OUTPUT = ROOT / "artifacts/cycle-67-seeded-packet-recurrence-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-67-seeded-packet-preregistration-v1.md", "77b1c67d6c8e5ade56f5fc5cc814dc926e0d84f988420feace4562631dea9bc8"),
    "document": (ROOT / "docs/cycle-67-seeded-packet-v1.md", "31e24bf4334ac55d60317bbce4e52e47d500547f35f5d6ce1b85a2eb069a5142"),
    "conventions": (ROOT / "conventions/seeded_packet_recurrence_v1.py", "f5cfece042014c29dd1be3634e323bc98fac47beb4b348903c209bc00554f411"),
    "tests": (ROOT / "tests/test_cycle_67_seeded_packet_recurrence_v1.py", "d04b2ff83dadb2f148730b07ac02ae2d901aa2fee1aa51416787acbb633960af"),
    "cycle66": (ROOT / "artifacts/cycle-66-primitive-poisson-contract-v1.json", "5d096b9f64a2dc82657d798d7fcd911812d8a6b8a7a326368330b532e16ef5bd"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 67 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("seeded_packet_recurrence_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 67 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require("X^(6/25)" in rows["critical_interface"], "critical depth")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle66"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_PRIMITIVE_POISSON_X31_25_OR_DEEP_PACKET_RECURRENCE_OPEN", "Cycle 66 status mismatch")
    return {"prior_role": "make the deep-packet structured branch a realized rather than beta-free recurrence statement"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-67-seeded-packet-recurrence-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_SEEDED_X6_25_AP_RECURRENCE_OPEN",
        "claim_boundary": "This artifact proves seed propagation along one approximate rational packet. It does not count seeds or packets and proves no large-value, powered, density, or interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "seeded_recurrence": {
            "epistemic_status": "PROVED",
            "statement": "One genuine strip hit plus packet depth K yields at least 1+floor(K/2) realized q-progression hits at enlarged constant C0+C1.",
        },
        "scope_correction": {
            "epistemic_status": "PROVED",
            "statement": "Without a genuine beta-dependent seed, a beta-free packet supplies allowable differences only and is not yet an E7/E9/E10 recurrence handoff.",
        },
        "analytic_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Show every major-arc obstruction to the X^(31/25) primitive Poisson bound supplies a seeded deep packet, then control or exploit its realized AP rows.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_67_seeded_packet_recurrence_v1.py --write",
            "check_command": "python3 proof/build_cycle_67_seeded_packet_recurrence_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_67_seeded_packet_recurrence_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 67 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 67 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 67 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
