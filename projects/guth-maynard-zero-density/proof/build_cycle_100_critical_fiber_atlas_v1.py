#!/usr/bin/env python3
"""Seal Cycle 100 exact critical-fiber atlas."""
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
OUTPUT = ROOT / "artifacts/cycle-100-critical-fiber-atlas-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "discovery_candidate": (ROOT / "discovery/cycle-100-critical-fiber-candidate-v1.md", "2a283fdb5af445b309d051ee5ceb9eb38fe6a6a4ef8d4cbabf6ddf6d1f8d2882"),
    "preregistration": (ROOT / "docs/cycle-100-critical-fiber-preregistration-v1.md", "63fa5b39e638ef95a7bc24bcbe059c2c2c65d59623d3b6e2ff01b158f5ba29ae"),
    "document": (ROOT / "docs/cycle-100-critical-fiber-atlas-v1.md", "96336e7a03ecfca1abce166a45e52b9d7c01971dc74316081a752f79a8065ba3"),
    "conventions": (ROOT / "conventions/critical_fiber_atlas_v1.py", "d432247621bd6c736496eadcf681d88b18936b36005b5d3d3855d1992e39eecf"),
    "tests": (ROOT / "tests/test_cycle_100_critical_fiber_atlas_v1.py", "00ae5a54357c5a35e97929cbcb71d814b78c9e1d2ee1594d50a838afb675a4b6"),
    "cycle99": (ROOT / "artifacts/cycle-99-critical-rational-ray-v1.json", "69e453fea12a404c17078169ac605c17b05109b99c74e0dd82f830e1ecdf2ee6"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 100 runtime mismatch")
    return runtime


def frozen_inputs() -> dict[str, dict[str, str]]:
    result = {}
    for label, (path, expected) in INPUTS.items():
        require(path.is_file(), f"missing frozen input: {label}")
        actual = sha256(path)
        require(actual == expected, f"frozen input hash mismatch: {label}")
        result[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual}
    return result


def load_theorem() -> dict[str, object]:
    path = INPUTS["conventions"][0]
    spec = importlib.util.spec_from_file_location("critical_fiber_atlas_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 100 conventions")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    record = module.theorem_record()
    require("lambda" in record["solutions"], "solution parametrization")
    require("gcd(s/g0,R)" in record["gcd_factorization"], "gcd factorization")
    require("tau(W)" in record["generic_bound"], "generic bound")
    require("no Mobius sign" in record["sign_boundary"], "sign boundary")
    return record


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle99"][0].read_text(encoding="utf-8"))
    require(
        prior.get("status") == "SEALED_STRONG_NEAR_DOUBLE_CRITICAL_RAYS_WEAK_AND_FIBER_OPEN",
        "Cycle 99 status mismatch",
    )
    return {"cycle99_role": "supply unique labels and the oriented factorization fiber"}


def seal() -> dict[str, Any]:
    theorem = load_theorem()
    return {
        "artifact_id": "cycle-100-critical-fiber-atlas-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_GENERIC_CRITICAL_FIBER_BOUND_CROSS_VALUATION_AND_LOW_HEIGHT_OPEN",
        "claim_boundary": (
            "This artifact proves the exact fiber formula, valuation factorization, and generic "
            "bound. It proves no exceptional-web bound, weak-row estimate, alias moment, density "
            "gain, or interval gain, and imports no unproved Mobius sign."
        ),
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "fiber_theorem": {"epistemic_status": "PROVED", **theorem},
        "generic_output": {
            "epistemic_status": "PROVED",
            "statement": "F_generic<=2Q tau(|w|)/min(N,R).",
        },
        "inverse_output": {
            "epistemic_status": "PROVED",
            "statement": "Every nongeneric split carries a side-labelled cross-valuation prime-power web.",
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Bound low-height labels and cross-valuation webs with actual stationary phases/amplitudes.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_100_critical_fiber_atlas_v1.py --write",
            "check_command": "python3 proof/build_cycle_100_critical_fiber_atlas_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_100_critical_fiber_atlas_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 100 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 100 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 100 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
