#!/usr/bin/env python3
"""Seal Cycle 81 exact q-transform and uniform remainder."""
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
OUTPUT = ROOT / "artifacts/cycle-81-exact-q-transform-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "discovery_candidate": (ROOT / "discovery/cycle-81-exact-q-transform-candidate-v1.md", "6244e79c9ae3072ac3b3d7ee49d3e23e1b8f688d3575f0cb569bf70adfc5ef37"),
    "preregistration": (ROOT / "docs/cycle-81-exact-q-transform-preregistration-v1.md", "e1dfaf723b69b1357efc179c32d5d3de844d5183635b7d378118a6243ec2abd1"),
    "document": (ROOT / "docs/cycle-81-exact-q-transform-v1.md", "736441b06acc044219c9370f188858100e2f2e39be9d4fe3d509c6e0dc622559"),
    "conventions": (ROOT / "conventions/exact_q_transform_v1.py", "f15b75902d4830511139944b88ff4e18642ab630a3f4dc85e17e4a2583c57499"),
    "tests": (ROOT / "tests/test_cycle_81_exact_q_transform_v1.py", "d0b8dba21798fac9722130c123cbbf6ec81f13d7496206ac5d0b78a37fa59242"),
    "cycle79": (ROOT / "artifacts/cycle-79-double-b-process-v1.json", "855bd15a08f78433e09edf2b3e66ef67abea109d69d55a763132ef3a8c084eb2"),
    "cycle80": (ROOT / "artifacts/cycle-80-phase-occupancy-v1.json", "751e8edde6469dabe637a17d8bc2cad491a9ed2caa49f099ce60020ef0a069d7"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 81 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("exact_q_transform_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 81 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["strict_margin"] == "2/15", "remainder margin")
    require(rows["per_k_error_exponent"] == "0", "per-k error")
    require("V(a)" in rows["leading_term"], "Fourier inversion sign")
    return rows


def validate_priors() -> dict[str, str]:
    cycle79 = json.loads(INPUTS["cycle79"][0].read_text(encoding="utf-8"))
    cycle80 = json.loads(INPUTS["cycle80"][0].read_text(encoding="utf-8"))
    require(cycle79.get("status") == "SEALED_DOUBLE_B_HIGH_FREQUENCY_LOG_SADDLE_OPEN", "Cycle 79 status mismatch")
    require(cycle80.get("status") == "SEALED_PRIMAL_OCCUPANCY_BAND_CLOSED_DUAL_HIGH_FREQUENCY_OPEN", "Cycle 80 status mismatch")
    return {
        "cycle79_role": "supply the raw Fourier target and formal logarithmic saddle",
        "cycle80_role": "restrict the active dual range to xi>=163/450",
    }


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-81-exact-q-transform-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_EXACT_Q_TRANSFORM_LOG_RESONANCE_PROJECTOR_OPEN",
        "claim_boundary": "This artifact proves the exact smooth q-transform, its central O(D/(Qr^2)) error, O(1) per-k summed remainder, negligible nonstationary tails, and 2/15 global error margin. It proves no dual cancellation, remaining-band closure, packet closure, density gain, or interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_priors()},
        "exact_transform": {
            "epistemic_status": "PROVED",
            "statement": "Linearity in q gives an exact one-variable Fourier kernel whose leading term is the Cycle-79 logarithmic saddle with weight V(hD/(beta Qr)).",
        },
        "uniform_remainder": {
            "epistemic_status": "PROVED",
            "statement": "The central error is O_(W,V)(D/(Qr^2)), summing to X^o(1) per k; smooth nonstationary tails are O_A(X^-A).",
        },
        "global_margin": {
            "epistemic_status": "PROVED",
            "statement": "Accumulating the error through k<=X^(83/75+o(1)) costs exponent 83/75, margin 2/15 to 31/25.",
        },
        "analytic_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Treat the inner smooth h-sum as a logarithmic resonance projector and bound the resulting (k,r) resonant set on 163/450<=xi<=83/75.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_81_exact_q_transform_v1.py --write",
            "check_command": "python3 proof/build_cycle_81_exact_q_transform_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_81_exact_q_transform_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 81 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 81 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 81 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

