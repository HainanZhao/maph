#!/usr/bin/env python3
"""Seal Cycle 95 exact projective entropy mode classification."""
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
OUTPUT = ROOT / "artifacts/cycle-95-projective-entropy-modes-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "discovery_candidate": (ROOT / "discovery/cycle-95-projective-mode-candidate-v1.md", "678a753e14c8f6960d27cbdfc53ff1f7731dd083e131fc7d71ed9f9dbf00e82c"),
    "source_ledger": (ROOT / "docs/cycle-95-gelfond-schneider-source-v1.md", "de9a7a5e0b42a105e63f1c4ba09f9c9bd728af23df84b6cdc8ec51ba74ece142"),
    "preregistration": (ROOT / "docs/cycle-95-projective-mode-preregistration-v1.md", "d7cd4fa07e1e2a67769a7f3b0a661548a18daf5a1a1c7b86f4f72f0bf7655417"),
    "document": (ROOT / "docs/cycle-95-projective-entropy-modes-v1.md", "b59e02901ec20fabed2a75add7134314e0cbf9e9fd0b4907b6a8c689d9717b8d"),
    "conventions": (ROOT / "conventions/projective_entropy_modes_v1.py", "5af2f8787333270a03fa2cef6292c1b083fb8b3b560700e77990057f4fc52bfb"),
    "tests": (ROOT / "tests/test_cycle_95_projective_entropy_modes_v1.py", "71c80e4074bd5de640089968f84e6bd660578781696cd2b170553a5d63b23757"),
    "cycle94": (ROOT / "artifacts/cycle-94-triple-b-entropy-v1.json", "9b6fc5021af3622821729f72966fcb15a4c9b74d0ef668d14ccc6f32349266a5"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 95 runtime mismatch")
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
    spec = importlib.util.spec_from_file_location("projective_entropy_modes_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 95 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require("iff u=v=0" in rows["exact_mode_classification"], "mode classification")
    require("Gelfond-Schneider" in rows["transcendence"], "transcendence input")
    require("no uniform lower bound" in rows["noncentral_boundary"], "quantitative boundary")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle94"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_CENTRAL_ANCHOR_DIFFERENCE_WEB_PROJECTIVE_ENTROPY_ALIASES_OPEN", "Cycle 94 status mismatch")
    return {"cycle94_role": "supply the entropy phase and its Poisson-mode stationary derivatives"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-95-projective-entropy-modes-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_EXACT_ALIASES_CENTRAL_NEAR_PROJECTIVE_MODES_QUANTITATIVE_OPEN",
        "claim_boundary": "This artifact proves the exact projective entropy mode classification using Gelfond-Schneider. It proves no quantitative near-mode lower bound, alias estimate, moment theorem, density gain, or interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "transcendence_input": {
            "epistemic_status": "PROVED",
            "statement": "Gelfond-Schneider applied to (-1)^(-2i/D) proves exp(2pi/D) transcendental for every positive integer D.",
        },
        "exact_classification": {
            "epistemic_status": "PROVED",
            "statement": "The Laurent stationary equation has a solution exactly only for u=v=0 and p0(n-n')=q0m.",
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Obtain a uniform lower bound or inverse theorem for near-zero noncentral Laurent trinomials as D and the modes grow.",
        },
        "exact_replay": rows,
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_95_projective_entropy_modes_v1.py --write",
            "check_command": "python3 proof/build_cycle_95_projective_entropy_modes_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_95_projective_entropy_modes_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 95 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 95 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 95 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

