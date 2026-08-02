#!/usr/bin/env python3
"""Seal Cycle 94 triple-B entropy and anchor-difference atlas."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
from typing import Any

import sympy


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-94-triple-b-entropy-v1.json"
EXPECTED_RUNTIME = {
    "implementation": "CPython",
    "python": "3.12.3",
    "optimization_level": 0,
    "sympy": "1.12",
}
INPUTS: dict[str, tuple[Path, str]] = {
    "discovery_candidate": (ROOT / "discovery/cycle-94-triple-b-entropy-candidate-v1.md", "a06cd061cc6850245a3aee5df3fbe2573e72f7dfcc047127225f810f1cd78477"),
    "preregistration": (ROOT / "docs/cycle-94-triple-b-entropy-preregistration-v1.md", "71bdcbd85195c0faa70cf1468077e5cbb5ddf0e5b91810104fc9ad68f07d4126"),
    "document": (ROOT / "docs/cycle-94-triple-b-entropy-v1.md", "4b2a022c9bb4a11851ff7c8e5078e17685235988e91c22e0befa39ed4b3583a3"),
    "conventions": (ROOT / "conventions/triple_b_entropy_v1.py", "e39d9ab1dc977f1fa343ed115cd6ee5ae4cbed7cc7aff81def7c19b5b94e22f8"),
    "tests": (ROOT / "tests/test_cycle_94_triple_b_entropy_v1.py", "f03327b3dc98b57361fa6c4d82e32be8966b96695555e3a901cba11b704b9cb6"),
    "cycle90": (ROOT / "artifacts/cycle-90-equal-height-bprocess-v1.json", "a24a63110e26fff4672c8b8e2cca27569a00885dec7b8c934f8ca3971967c3de"),
    "cycle93": (ROOT / "artifacts/cycle-93-nonstationary-mellin-branch-v1.json", "5dd299f0a0c67774f65b30cffd1e2ee48aace17b07eb6c3c6e1700b1e306cd3d"),
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
        "sympy": sympy.__version__,
    }
    require(runtime == EXPECTED_RUNTIME, "Cycle 94 runtime mismatch")
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
    spec = importlib.util.spec_from_file_location("triple_b_entropy_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 94 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["central_anchor_difference"] == "m=c0*(n-n')", "anchor difference")
    require(rows["hessian_determinant"] == "0 identically", "Hessian degeneracy")
    require("not covered" in rows["open_modes"], "open modes")
    return rows


def validate_priors() -> dict[str, str]:
    cycle90 = json.loads(INPUTS["cycle90"][0].read_text(encoding="utf-8"))
    cycle93 = json.loads(INPUTS["cycle93"][0].read_text(encoding="utf-8"))
    require(cycle90.get("status") == "SEALED_EQUAL_HEIGHT_BPROCESS_SADDLE_DISCREPANCY_OR_WEB_OPEN", "Cycle 90 status mismatch")
    require(cycle93.get("status") == "SEALED_STRICT_SUB_ALIAS_POWER_NEGLIGIBLE_TRANSITION_AND_ALIASES_OPEN", "Cycle 93 status mismatch")
    return {
        "cycle90_role": "supply the logarithmic r and r' B-process signs",
        "cycle93_role": "leave only transition and stationary integer aliases after strict nonstationary closure",
    }


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-94-triple-b-entropy-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_CENTRAL_ANCHOR_DIFFERENCE_WEB_PROJECTIVE_ENTROPY_ALIASES_OPEN",
        "claim_boundary": "This artifact proves the triple-B entropy phase, central stationary anchor-difference relation, and projective Hessian degeneracy. It proves no full stationary-alias bound, moment theorem, density gain, or interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_priors()},
        "central_web": {
            "epistemic_status": "PROVED",
            "statement": "Central stationarity forces h'/h=n'/n and m=c0(n-n'); for rational c0=p0/q0 this is q0 m=p0(n-n').",
        },
        "projective_boundary": {
            "epistemic_status": "PROVED",
            "statement": "The entropy phase is degree-one homogeneous in (h,Delta) and its Hessian determinant vanishes identically.",
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Bound nonzero projective entropy aliases or show that each produces a translated anchor-difference web.",
        },
        "exact_replay": rows,
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_94_triple_b_entropy_v1.py --write",
            "check_command": "python3 proof/build_cycle_94_triple_b_entropy_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_94_triple_b_entropy_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 94 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 94 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 94 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

