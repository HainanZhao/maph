#!/usr/bin/env python3
"""Seal Cycle 56 actual-prime edge cumulant algebra."""
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
OUTPUT = ROOT / "artifacts/cycle-56-prime-edge-cumulant-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-56-prime-edge-cumulant-preregistration-v1.md", "2236ec31ea62c6f8e4a422687a803d3ccaeb98cb878b78909bdd1e12545df1f7"),
    "document": (ROOT / "docs/cycle-56-prime-edge-cumulant-v1.md", "af9298d5eccea6997825e7699db9456a8d67e8ee78cbec2d19ea646bf33df55a"),
    "conventions": (ROOT / "conventions/prime_edge_cumulant_v1.py", "626276ba56a8238973d232ca344dae3318e5e9aa014f3ec5af470f30923c6f97"),
    "tests": (ROOT / "tests/test_cycle_56_prime_edge_cumulant_v1.py", "e28767a3662b3e60c8f89705bb581bb132cf80a353b1b2d5b48379e0d701a5d1"),
    "cycle55": (ROOT / "artifacts/cycle-55-centered-trace-boundary-v1.json", "50a66a5d1aea0e9173e4c23bc8bf262e0c937b162a86942e957065635c6c53ab"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 56 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("prime_edge_cumulant_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 56 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["s3"]["coefficient_l1"] == 16, "s3 coefficient norm")
    require(rows["s4"]["coefficient_l1"] == 32, "s4 coefficient norm")
    require(rows["s4"]["positive_semidefinite"], "edge kernel positivity")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle55"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_SCALAR_CENTERED_TRACES_SHARP_PRIME_CUMULANT_OPEN", "Cycle 55 status mismatch")
    return {"prior_role": "replace scalar post-collapse centering by actual prime-coordinate centering"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-56-prime-edge-cumulant-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_EDGE_CUMULANT_SUPPORT_COLLAPSE_3_50_OPEN",
        "claim_boundary": "This artifact proves ordered-coordinate edge-cumulant algebra and positivity. It does not prove support-collapse control, an analytic saving, AMPR, density, or interval gains.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "edge_cumulant": {
            "epistemic_status": "PROVED",
            "statement": "Coordinatewise centering gives PSD kernel C_m(h,g)C(h,g)^s, annihilates diagonal edges, and has constant-cost signed expansions for s=3,4.",
        },
        "analytic_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Push the cumulant through integer-frequency support partitions, then gain 3/50 or extract simultaneous approximate multiplicativity at scales 1,m.",
        },
        "exact_replay": rows,
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_56_prime_edge_cumulant_v1.py --write",
            "check_command": "python3 proof/build_cycle_56_prime_edge_cumulant_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_56_prime_edge_cumulant_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 56 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 56 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 56 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
