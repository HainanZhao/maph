#!/usr/bin/env python3
"""Seal Cycle 68 folded-frequency generic large-sieve baseline."""
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
OUTPUT = ROOT / "artifacts/cycle-68-folded-frequency-baseline-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-68-frequency-folding-preregistration-v1.md", "6413e57cf9c803dae70ac2cea2290038d138a953257bc6cfae8de8d12db13ae2"),
    "document": (ROOT / "docs/cycle-68-frequency-folding-v1.md", "0aed3654b6401087b9e627512b8f3d39042e76a549589d00c23274b0f3bc6ed0"),
    "conventions": (ROOT / "conventions/folded_frequency_baseline_v1.py", "ece6a0c77348684797a82c7ffce7b421f09df687fdaf1b0b80d2a9d6bab72aca"),
    "tests": (ROOT / "tests/test_cycle_68_folded_frequency_baseline_v1.py", "269cda8613b35be82f1ef98a83864edbbc3b32712a26dfb6be24783fa540119b"),
    "cycle67": (ROOT / "artifacts/cycle-67-seeded-packet-recurrence-v1.json", "85bd999fca3e1d675c0b3096a6cd287866d9e1aef227239b42b94b39ff585d02"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 68 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("folded_frequency_baseline_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 68 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["required_saving"] == "3/50+theta+kappa", "required saving")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle67"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_SEEDED_X6_25_AP_RECURRENCE_OPEN", "Cycle 67 status mismatch")
    return {"prior_role": "measure the generic analytic baseline on the minor-arc primitive Poisson branch"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-68-folded-frequency-baseline-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_FOLDED_LARGE_SIEVE_GAP_3_50_PLUS_THETA_KAPPA",
        "claim_boundary": "This artifact proves a folded coefficient bound and generic large-sieve baseline only. It does not obstruct phase- or Möbius-sensitive estimates and proves no packet, recurrence, powered, density, or interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "coefficient_folding": {
            "epistemic_status": "PROVED",
            "statement": "The composite-frequency coefficient is divisor-bounded, supported through X^(1+theta+kappa), and has square norm of that exponent up to subpower factors.",
        },
        "generic_baseline": {
            "epistemic_status": "PROVED",
            "statement": "Cauchy plus fractional-part separation gives exponent 13/10+theta+kappa, missing 31/25 by 3/50+theta+kappa.",
        },
        "analytic_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Recover the deficit by retaining Möbius cancellation, the exponential transport phase, or a seeded major-arc extraction.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_68_folded_frequency_baseline_v1.py --write",
            "check_command": "python3 proof/build_cycle_68_folded_frequency_baseline_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_68_folded_frequency_baseline_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 68 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 68 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 68 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
