#!/usr/bin/env python3
"""Seal Cycle 103 critical-scale algebraic alias inverse."""
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
OUTPUT = ROOT / "artifacts/cycle-103-critical-scale-alias-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "discovery_candidate": (ROOT / "discovery/cycle-103-critical-scale-alias-candidate-v1.md", "934e11dece50f61d92416ae313b7d840654c4a76df72a34c755b3b1fbc335a65"),
    "preregistration": (ROOT / "docs/cycle-103-critical-scale-alias-preregistration-v1.md", "1859399f4bd966154b129e793917fcaf313911769d0f440298ac3bf11a257277"),
    "document": (ROOT / "docs/cycle-103-critical-scale-alias-v1.md", "91b76391d55a2c1339f63afe9d31a420a3abdbe78b9a2c7231dad9f76546e97b"),
    "conventions": (ROOT / "conventions/critical_scale_alias_v1.py", "db35d90f9cf24336caf1a2fd9c7467324901fa918f29bbc391e0cbf6cff90b39"),
    "tests": (ROOT / "tests/test_cycle_103_critical_scale_alias_v1.py", "e42c2eceb6d3694806cce8a4fdb0b4d68c663c189a288cae88002118017d6532"),
    "cycle102": (ROOT / "artifacts/cycle-102-cross-valuation-inverse-v1.json", "1f4d27e5e1c269b04d3779634d6deaaa5ae21eb3f9352de781bc33b396c002ff"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 103 runtime mismatch")
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
    spec = importlib.util.spec_from_file_location("critical_scale_alias_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 103 conventions")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    record = module.theorem_record()
    require("f(t*)=A-lambda*K" in record["homogeneity"], "critical homogeneity")
    require("||qK||<=2epsilon" in record["inverse"], "scale alias inverse")
    require("no useful irrationality measure" in record["boundary"], "claim boundary")
    return record


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle102"][0].read_text(encoding="utf-8"))
    require(
        prior.get("status") == "SEALED_EXACT_CROSS_VALUATION_CORE_CONDITIONAL_COLOUR_CONCENTRATION",
        "Cycle 102 status mismatch",
    )
    return {"cycle102_role": "supply exact primitive cross cores and lambda ranges"}


def seal() -> dict[str, Any]:
    theorem = load_theorem()
    return {
        "artifact_id": "cycle-103-critical-scale-alias-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_CRITICAL_SCALE_ONE_HIT_OR_SHORT_ALGEBRAIC_ALIAS",
        "claim_boundary": (
            "This artifact proves critical-value homogeneity, algebraicity of K, and "
            "the one-hit-or-short-alias inverse. It proves no irrationality measure, "
            "aggregate exceptional-web bound, phase cancellation, weak/simple-root "
            "estimate, complete moment, density gain, or interval gain."
        ),
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "scale_alias_theorem": {"epistemic_status": "PROVED", **theorem},
        "e16_interface": {
            "epistemic_status": "PROVED",
            "statement": (
                "J critical-value hits produce q<=floor((Lambda-1)/(J-1)) "
                "with ||qK||<=2epsilon, retaining the full cross core"
            ),
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "separate K quantitatively, count short-alias cores, or exploit the "
                "actual stationary phases before aggregating splits"
            ),
        },
        "containment": {
            "epistemic_status": "OBSERVED",
            "statement": (
                "two initial test expectations were arithmetically wrong; corrected "
                "fixtures leave theorem formulas unchanged"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_103_critical_scale_alias_v1.py --write",
            "check_command": "python3 proof/build_cycle_103_critical_scale_alias_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_103_critical_scale_alias_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 103 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 103 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 103 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
