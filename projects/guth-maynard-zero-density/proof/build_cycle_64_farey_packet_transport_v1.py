#!/usr/bin/env python3
"""Seal Cycle 64 primitive Farey-packet reduction."""
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
OUTPUT = ROOT / "artifacts/cycle-64-farey-packet-transport-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-64-farey-packet-preregistration-v1.md", "7ddbda60349a2f46cc1c853da47d47b6b2827b58b31bd2e4405d920bba104e5f"),
    "document": (ROOT / "docs/cycle-64-farey-packet-v1.md", "afaad92a12b6aed8d53bad95d4ad7a5a0ef66532dee26285b51e490cf2d242ff"),
    "conventions": (ROOT / "conventions/farey_packet_transport_v1.py", "d9ecdc6a21904b85cc72694421b6b7aec408efaca9419f6f73ecf173faf38f80"),
    "tests": (ROOT / "tests/test_cycle_64_farey_packet_transport_v1.py", "1fdf9161e62033c07ad90074a6b78278a60e2f19fd5546950eaa810774a4e6db"),
    "cycle63": (ROOT / "artifacts/cycle-63-log-transport-census-v1.json", "d5dc9dd9ff3f5636c98980d35f6f973d72f9e62c04644fe510b4f0de06d4f153"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 64 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("farey_packet_transport_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 64 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    data = rows["packet"]
    require(data["unique_reduced_approximant_per_ell"], "fraction uniqueness")
    require(data["unique_ell_per_reduced_approximant"], "curve-point uniqueness")
    require(data["harmonic_packet_mass_target_open"] == -Fraction(1, 5), "packet target")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle63"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_LOG_TRANSPORT_PAIR_CENSUS_LT_17_25_OPEN", "Cycle 63 status mismatch")
    return {"prior_role": "compress the beta-free weighted pair census by reduced rational packets"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-64-farey-packet-transport-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_LOG_FAREY_PACKET_MASS_OR_LOW_DENOMINATOR_RECURRENCE_OPEN",
        "claim_boundary": "This artifact proves packet uniqueness and a weighted reduction only. It does not bound packet mass or prove pair, powered, LCAM, density, or interval gains.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "packet_reduction": {
            "epistemic_status": "PROVED",
            "statement": "Every beta-free resonance belongs to one injective reduced Farey packet; its weighted multiples cost at most H^2/(2q), reducing pair exponent <17/25 to harmonic packet mass <X^-1/5.",
        },
        "structured_exception": {
            "epistemic_status": "CONJECTURED",
            "statement": "Either the packet mass has a strict X^-1/5 bound or a heavy low-denominator packet is extracted and routed to recurrence/detector surgery; uniform small mass without exceptions is not asserted.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_64_farey_packet_transport_v1.py --write",
            "check_command": "python3 proof/build_cycle_64_farey_packet_transport_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_64_farey_packet_transport_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 64 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 64 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 64 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
