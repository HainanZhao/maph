#!/usr/bin/env python3
"""Seal Cycle 90 equal-height B-process and saddle-collision contract."""
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
OUTPUT = ROOT / "artifacts/cycle-90-equal-height-bprocess-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "discovery_candidate": (ROOT / "discovery/cycle-90-equal-height-bprocess-candidate-v1.md", "7e45e6e5cb000b6cdf9f91c19bb9f7b750e90e998198da2dce0551c69023dadf"),
    "preregistration": (ROOT / "docs/cycle-90-equal-height-bprocess-preregistration-v1.md", "603e22f484c648eae533f2a81d452d444417e50c3cc625ceff2efcf83e2ca233"),
    "document": (ROOT / "docs/cycle-90-equal-height-bprocess-v1.md", "77eef98dcd888e306ed9f952f34d70567bcf4e071b9c3db9f98726e93e6b3588"),
    "conventions": (ROOT / "conventions/equal_height_bprocess_v1.py", "4b9cb36d00feafb445ca64761b8b714829a0e239e0dedea0ec36ba4165603853"),
    "tests": (ROOT / "tests/test_cycle_90_equal_height_bprocess_v1.py", "1ffde005c542a42438ca8cb3bebda38b7f9fdba43aef53bd589b8600fa5c916c"),
    "cycle69": (ROOT / "artifacts/cycle-69-stationary-transport-dual-v1.json", "4f868a07381d89ccfafe72f80553a63b9457447a848408d22cb4493d4726a04c"),
    "cycle81": (ROOT / "artifacts/cycle-81-exact-q-transform-v1.json", "0753d455a2e9428b28f1b9dac59b04fd57008db562370202a300a38a818631a4"),
    "cycle87": (ROOT / "artifacts/cycle-87-mellin-alias-atlas-v1.json", "68b88ccd4ce3e5371906e3b0da3c254056b79bad9504880ebbff04b9cebce8ca"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 90 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("equal_height_bprocess_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 90 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["dual_length_exponent"] == "1/3", "dual length")
    require(rows["minimum_sample_surplus"] == "1/25", "sample surplus")
    require(rows["bprocess_remainder_margin"] == "1/3", "remainder margin")
    require("exp(2*beta*a/D)" in rows["surface_determinant"], "saddle determinant")
    return rows


def validate_priors() -> dict[str, str]:
    cycle69 = json.loads(INPUTS["cycle69"][0].read_text(encoding="utf-8"))
    cycle81 = json.loads(INPUTS["cycle81"][0].read_text(encoding="utf-8"))
    cycle87 = json.loads(INPUTS["cycle87"][0].read_text(encoding="utf-8"))
    require(cycle69.get("status") == "SEALED_STATIONARY_HESSIAN_DEGENERATE_PROJECTIVE_X21_25_OPEN", "Cycle 69 status mismatch")
    require(cycle81.get("status") == "SEALED_EXACT_Q_TRANSFORM_LOG_RESONANCE_PROJECTOR_OPEN", "Cycle 81 status mismatch")
    require(cycle87.get("status") == "SEALED_MELLIN_ALIAS_TRICHOTOMY_BOUND_OR_WEB_OPEN", "Cycle 87 status mismatch")
    return {
        "cycle69_role": "supply the registered smooth one-dimensional B-process convention",
        "cycle81_role": "supply the exact dual leading amplitude and support",
        "cycle87_role": "identify equal height as a separate second-moment branch",
    }


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-90-equal-height-bprocess-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_EQUAL_HEIGHT_BPROCESS_SADDLE_DISCREPANCY_OR_WEB_OPEN",
        "claim_boundary": "This artifact proves the equal-height quadratic form, smooth B-process map, exponent ledger, and nondegenerate saddle-collision target. It proves no saddle collision bound, full equal-height bound, diagonal second moment, Fourier-band closure, density gain, or interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_priors()},
        "bprocess_reduction": {
            "epistemic_status": "PROVED",
            "statement": "The equal-height length-K Mellin polynomial B-transforms to length Q; its diagonal has exponent xi+14/15 and the smooth B-process remainder has margin 1/3.",
        },
        "saddle_contract": {
            "epistemic_status": "PROVED",
            "statement": "The dual off-diagonal localizes to |n'-n exp(2pi a/D)|<<1/K. Its volume-to-target margin is xi-3/5>=1/25 and its affine Hessian determinant is nonzero.",
        },
        "analytic_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Bound every Schwartz-weighted saddle-collision annulus by X^(1/3+o(1)), or export an explicit anchored collision web.",
        },
        "exact_replay": rows,
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_90_equal_height_bprocess_v1.py --write",
            "check_command": "python3 proof/build_cycle_90_equal_height_bprocess_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_90_equal_height_bprocess_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 90 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 90 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 90 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

