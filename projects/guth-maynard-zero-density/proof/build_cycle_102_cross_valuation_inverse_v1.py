#!/usr/bin/env python3
"""Seal Cycle 102 exact cross-valuation inverse atlas."""
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
OUTPUT = ROOT / "artifacts/cycle-102-cross-valuation-inverse-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "discovery_candidate": (ROOT / "discovery/cycle-102-cross-valuation-candidate-v1.md", "cfafb207998e9d66962ef9c2510c85fe69ed511bcb853201c991bced2df4094e"),
    "preregistration": (ROOT / "docs/cycle-102-cross-valuation-preregistration-v1.md", "a2060fdbf763c3c14bb7dacc7aca20b3cd1b9ea96eecb6f2b889e5f5c0fb3e2c"),
    "document": (ROOT / "docs/cycle-102-cross-valuation-inverse-v1.md", "c3646c142dd6ab3a1bc668ca8b91cb039e12a69ac6ca5fa5f63cb2f99386f6cb"),
    "conventions": (ROOT / "conventions/cross_valuation_inverse_v1.py", "4d29bc48686c062422547a88902ee0d27104e37ca88103cab275bc7b697d13db"),
    "tests": (ROOT / "tests/test_cycle_102_cross_valuation_inverse_v1.py", "60245b9b7eaffc9cd2193a782793af9d6e366515905f7bd866b6a552bb65313a"),
    "cycle101": (ROOT / "artifacts/cycle-101-generic-critical-packing-v1.json", "3c4e6a34b839df06028233e127a01001e094dc16665c833f43ec370642d3c4d1"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 102 runtime mismatch")
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
    spec = importlib.util.spec_from_file_location("cross_valuation_inverse_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 102 conventions")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    record = module.theorem_record()
    require("B0=t2*R2" in record["core"], "exact core formula")
    require("E/(2*P(2M)*A)" in record["unrefined_concentration"], "colour threshold")
    require("per-w cap A" in record["boundary"], "claim boundary")
    return record


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle101"][0].read_text(encoding="utf-8"))
    require(
        prior.get("status") == "SEALED_GENERIC_STRONG_CRITICAL_AGGREGATE_X19_30_EXCEPTIONAL_OPEN",
        "Cycle 101 status mismatch",
    )
    return {"cycle101_role": "supply the generic aggregate and isolate cross-valuation exceptions"}


def seal() -> dict[str, Any]:
    theorem = load_theorem()
    return {
        "artifact_id": "cycle-102-cross-valuation-inverse-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_EXACT_CROSS_VALUATION_CORE_CONDITIONAL_COLOUR_CONCENTRATION",
        "claim_boundary": (
            "This artifact proves an exact coprime-core parametrization and a weighted "
            "side/prime-power concentration threshold. It proves no exceptional-mass "
            "bound, phase cancellation, common anchor, weak/simple-root estimate, alias "
            "moment, density gain, or interval gain."
        ),
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "inverse_atlas": {"epistemic_status": "PROVED", **theorem},
        "e16_interface": {
            "epistemic_status": "PROVED",
            "statement": (
                "each exceptional split retains side, full prime powers, both dyadic "
                "cross-gcd scales, distinct w, and an unchanged stationary/anchor payload"
            ),
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "obtain a strong per-w mass cap or phase cancellation, then compile any "
                "threshold-exceeding colour class into a genuine anchored seed"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_102_cross_valuation_inverse_v1.py --write",
            "check_command": "python3 proof/build_cycle_102_cross_valuation_inverse_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_102_cross_valuation_inverse_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 102 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 102 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 102 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
