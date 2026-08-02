#!/usr/bin/env python3
"""Seal Cycle 101 aggregate generic critical packing."""
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
OUTPUT = ROOT / "artifacts/cycle-101-generic-critical-packing-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "discovery_candidate": (ROOT / "discovery/cycle-101-generic-packing-candidate-v1.md", "a87d3d1ffec6ad5a4a8b23ffe08ca2b2ffce44662cc1145d5628fb929d2f1b0c"),
    "preregistration": (ROOT / "docs/cycle-101-generic-packing-preregistration-v1.md", "034ef56841580153c77b207a41683454747b65c5a0f3d90cb88a2fdc89a02396"),
    "document": (ROOT / "docs/cycle-101-generic-critical-packing-v1.md", "134decdfeb7c9bde54bb84ea421176c5b822e25c5b06ae11c106eec29ead7e13"),
    "conventions": (ROOT / "conventions/generic_critical_packing_v1.py", "d82b4d0f043774bca0301fcb1974682a7af34b0d73fe40a6df43d4dfa1e2be20"),
    "tests": (ROOT / "tests/test_cycle_101_generic_critical_packing_v1.py", "7f89cdd360b86e94bbe9b914f03d818e45ce64835fe3b67723b23fa9fa831b60"),
    "cycle100": (ROOT / "artifacts/cycle-100-critical-fiber-atlas-v1.json", "2b5de8802840ce6411ef9b1eef887d4619ecb04d1c71fe520491db4cb01b2da1"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 101 runtime mismatch")
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
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    spec = importlib.util.spec_from_file_location("generic_critical_packing_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 101 conventions")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    record = module.theorem_record()
    require("sqrt(J)" in record["reciprocal_sum"], "packing sum")
    require("8*K_L" in record["uniform"], "uniform constant")
    require("19/30" in record["actual_exponent"], "actual exponent")
    require("excluded" in record["boundary"], "claim boundary")
    return record


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle100"][0].read_text(encoding="utf-8"))
    require(
        prior.get("status")
        == "SEALED_GENERIC_CRITICAL_FIBER_BOUND_CROSS_VALUATION_AND_LOW_HEIGHT_OPEN",
        "Cycle 100 status mismatch",
    )
    return {"cycle100_role": "supply the labelwise generic fiber bound and exceptional split"}


def seal() -> dict[str, Any]:
    theorem = load_theorem()
    return {
        "artifact_id": "cycle-101-generic-critical-packing-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_GENERIC_STRONG_CRITICAL_AGGREGATE_X19_30_EXCEPTIONAL_OPEN",
        "claim_boundary": (
            "This artifact proves the aggregate generic strong-critical bound "
            "Q*M^(1/2+o(1))=X^(19/30+o(1)). It proves no cross-valuation, weak, "
            "simple-root, alias-moment, density, or interval bound."
        ),
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "packing_theorem": {"epistemic_status": "PROVED", **theorem},
        "aggregate_output": {
            "epistemic_status": "PROVED",
            "statement": "sum of all generic strong critical fibers is <=8 K_L Q T_M sqrt(M).",
            "actual_exponent": "19/30",
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Control cross-valuation webs, weak near-double rows, and simple-root averages.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_101_generic_critical_packing_v1.py --write",
            "check_command": "python3 proof/build_cycle_101_generic_critical_packing_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_101_generic_critical_packing_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 101 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 101 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 101 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
