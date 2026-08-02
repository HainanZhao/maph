#!/usr/bin/env python3
"""Seal Cycle 80 primal phase-occupancy high-frequency band."""
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
OUTPUT = ROOT / "artifacts/cycle-80-phase-occupancy-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-80-phase-occupancy-preregistration-v1.md", "9e0d8dec43aa7d6525b68f569f1f7d1f0eecff2c056706258bbd014c0c16b75c"),
    "document": (ROOT / "docs/cycle-80-phase-occupancy-v1.md", "a237f3448790170564e686500367dc9d8ee7da95c639c58fbc0a52245e2305d2"),
    "conventions": (ROOT / "conventions/phase_occupancy_v1.py", "60735184c0675692695034660bb7728f06732c35d78369a3db429d8534a15924"),
    "tests": (ROOT / "tests/test_cycle_80_phase_occupancy_v1.py", "515bd401403a1c6b1869f7a167478386e8bf003d6bf4e3d4e32474fa8b3b1d1e"),
    "cycle79": (ROOT / "artifacts/cycle-79-double-b-process-v1.json", "855bd15a08f78433e09edf2b3e66ef67abea109d69d55a763132ef3a8c084eb2"),
    "cycle47_source_ledger": (ROOT / "artifacts/cycle-47-near-curve-gap-v1.json", "209dd38186cefbfad2f286b1fbc6400745425fb6fc8555bd8e06ac5547174a55"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 80 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("phase_occupancy_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 80 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["closed_band"] == "4/15<=xi<163/450", "closed band")
    require(rows["band_width"] == "43/450", "band width")
    return rows


def validate_priors() -> dict[str, str]:
    cycle79 = json.loads(INPUTS["cycle79"][0].read_text(encoding="utf-8"))
    source = json.loads(INPUTS["cycle47_source_ledger"][0].read_text(encoding="utf-8"))
    require(cycle79.get("status") == "SEALED_DOUBLE_B_HIGH_FREQUENCY_LOG_SADDLE_OPEN", "Cycle 79 status mismatch")
    require(source.get("epistemic_status") == "PROVED", "Cycle 47 source ledger status mismatch")
    return {
        "cycle79_role": "supply the Fourier target and initial low-frequency cutoff",
        "cycle47_role": "supply the checked order-three near-integer theorem and source chain",
    }


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-80-phase-occupancy-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_PRIMAL_OCCUPANCY_BAND_CLOSED_DUAL_HIGH_FREQUENCY_OPEN",
        "claim_boundary": "This artifact closes only the Fourier band 4/15<=xi<163/450 by primal phase occupancy and a clustered large sieve. The remaining high frequencies, ACSI, packet closure, powered saving, density gain, and interval gain remain open.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_priors()},
        "occupancy": {
            "epistemic_status": "PROVED",
            "statement": "Every length-1/Q phase interval contains at most X^(22/45+o(1)) primal d-phases, uniformly through the Fourier support.",
        },
        "large_sieve": {
            "epistemic_status": "PROVED",
            "statement": "The clustered circle large sieve gives |S_k|<=X^(79/90+o(1)).",
        },
        "new_band": {
            "epistemic_status": "PROVED",
            "statement": "All 4/15<=xi<163/450 blocks are strictly below 31/25; width 43/450. The endpoint ties.",
        },
        "analytic_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Use the double B-process and valuation-web split only on 163/450<=xi<=83/75.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_80_phase_occupancy_v1.py --write",
            "check_command": "python3 proof/build_cycle_80_phase_occupancy_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_80_phase_occupancy_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 80 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 80 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 80 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
