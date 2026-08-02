#!/usr/bin/env python3
"""Seal Cycle 85 logarithmic crossing occupancy to the volume limit."""
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
OUTPUT = ROOT / "artifacts/cycle-85-log-crossing-occupancy-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "discovery_candidate": (ROOT / "discovery/cycle-85-log-crossing-candidate-v1.md", "a77f1dc1e9bc7181eba551a1289d8d197b3693f72e344cc4aa23f90fe3e5e95d"),
    "preregistration": (ROOT / "docs/cycle-85-log-crossing-preregistration-v1.md", "9db940d9bfa08acf7ddc90ef51e090937b0dad8f1e303bf2320456a04a173e9f"),
    "document": (ROOT / "docs/cycle-85-log-crossing-occupancy-v1.md", "310c60cb7278c15aa537f83c69402df31faab8f193bf93480fba0ba6481e1b92"),
    "conventions": (ROOT / "conventions/log_crossing_occupancy_v1.py", "6c31a3b80a256c7bba469216070502977dce6bd63339ed0062d8ba82414b319c"),
    "tests": (ROOT / "tests/test_cycle_85_log_crossing_occupancy_v1.py", "9d66ca11df8ee8ca832902de2a3ba265406d347a5e6fbe96ec619850cbde0c4f"),
    "cycle47_source_ledger": (ROOT / "artifacts/cycle-47-near-curve-gap-v1.json", "209dd38186cefbfad2f286b1fbc6400745425fb6fc8555bd8e06ac5547174a55"),
    "cycle84": (ROOT / "artifacts/cycle-84-averaged-resonance-v1.json", "b7f67aa9613891c0de006711fc07475085aab0114fd44808a701cf57fe79ca9b"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 85 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("log_crossing_occupancy_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 85 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["new_cutoff"] == "16/25", "new cutoff")
    require(rows["band_width"] == "1/15", "band width")
    require(rows["minimum_derivative_over_tube_margin"] == "8/225", "dominance margin")
    return rows


def validate_priors() -> dict[str, str]:
    source = json.loads(INPUTS["cycle47_source_ledger"][0].read_text(encoding="utf-8"))
    cycle84 = json.loads(INPUTS["cycle84"][0].read_text(encoding="utf-8"))
    require(source.get("epistemic_status") == "PROVED", "Cycle 47 source ledger status mismatch")
    require(cycle84.get("status") == "SEALED_AVERAGED_RESONANCE_BAND_CROSSING_INVERSE_OPEN", "Cycle 84 status mismatch")
    return {
        "cycle47_role": "supply the checked order-three near-integer theorem and hypotheses",
        "cycle84_role": "supply the occupied-crossing reduction and prior cutoff",
    }


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-85-log-crossing-occupancy-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_UNSIGNED_INCIDENCE_VOLUME_LIMIT_SIGNED_RESONANCE_OPEN",
        "claim_boundary": "This artifact proves logarithmic crossing occupancy and closes only 43/75<=xi<16/25. The endpoint, all higher frequencies, signed cancellation, packet closure, density gain, and interval gain remain open.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_priors()},
        "crossing_occupancy": {
            "epistemic_status": "PROVED",
            "statement": "Order-three Huxley--Sargos on g_j(r)=D/(2pi)log(r/(jc0)) gives crossing exponent min(nu,1/10+nu/2), with derivative-over-tube margin at least 8/225.",
        },
        "new_band": {
            "epistemic_status": "PROVED",
            "statement": "The block exponent is xi+3/5, closing 43/75<=xi<16/25; width 1/15. The endpoint ties.",
        },
        "structural_boundary": {
            "epistemic_status": "PROVED",
            "statement": "Unsigned smooth incidence has reached its volume limit at xi=16/25; higher frequencies require signed cancellation or structured inverse output.",
        },
        "analytic_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Construct signed high-frequency cancellation on 16/25<=xi<=83/75 using the exact logarithmic projector, routing valuation webs to E16.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_85_log_crossing_occupancy_v1.py --write",
            "check_command": "python3 proof/build_cycle_85_log_crossing_occupancy_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_85_log_crossing_occupancy_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 85 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 85 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 85 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

