#!/usr/bin/env python3
"""Seal Cycle 82 smooth-projector Fourier band."""
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
OUTPUT = ROOT / "artifacts/cycle-82-smooth-phase-projector-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "discovery_candidate": (ROOT / "discovery/cycle-82-smooth-projector-candidate-v1.md", "67dc0276044241d6bc034945d015d85356bacf10e80cf756c14d5321f65ea57f"),
    "preregistration": (ROOT / "docs/cycle-82-smooth-projector-preregistration-v1.md", "a086501de5d2ce2c4082e32c93208c2713a5c1cf50971e2fa149b399e8a623c2"),
    "document": (ROOT / "docs/cycle-82-smooth-phase-projector-v1.md", "9ccf8b8c17b976f5b2e40170c41178dca42f008e5477f13b1613266496428afa"),
    "conventions": (ROOT / "conventions/smooth_phase_projector_v1.py", "0ddfcb60bc4812045f00724efe0aaec00e020af493c3f6f7eb0c6c1b2da963f3"),
    "tests": (ROOT / "tests/test_cycle_82_smooth_phase_projector_v1.py", "bf5792789798ff9c81a5914e6ada3de44233740654300092c14679b9115e6900"),
    "cycle80": (ROOT / "artifacts/cycle-80-phase-occupancy-v1.json", "751e8edde6469dabe637a17d8bc2cad491a9ed2caa49f099ce60020ef0a069d7"),
    "cycle81": (ROOT / "artifacts/cycle-81-exact-q-transform-v1.json", "0753d455a2e9428b28f1b9dac59b04fd57008db562370202a300a38a818631a4"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 82 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("smooth_phase_projector_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 82 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["per_k_exponent"] == "37/45", "per-k projector exponent")
    require(rows["new_cutoff"] == "94/225", "new cutoff")
    require(rows["band_width"] == "1/18", "band width")
    return rows


def validate_priors() -> dict[str, str]:
    cycle80 = json.loads(INPUTS["cycle80"][0].read_text(encoding="utf-8"))
    cycle81 = json.loads(INPUTS["cycle81"][0].read_text(encoding="utf-8"))
    require(cycle80.get("status") == "SEALED_PRIMAL_OCCUPANCY_BAND_CLOSED_DUAL_HIGH_FREQUENCY_OPEN", "Cycle 80 status mismatch")
    require(cycle81.get("status") == "SEALED_EXACT_Q_TRANSFORM_LOG_RESONANCE_PROJECTOR_OPEN", "Cycle 81 status mismatch")
    return {
        "cycle80_role": "supply A_k<=X^(22/45+o(1)) uniformly in interval center",
        "cycle81_role": "supply the smooth q-projector and frozen Fourier sign",
    }


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-82-smooth-phase-projector-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_SMOOTH_PROJECTOR_BAND_FIXED_CENTER_RESONANCE_OPEN",
        "claim_boundary": "This artifact proves |S_k|<=X^(37/45+o(1)) and closes only 163/450<=xi<94/225 beyond Cycle 80. The endpoint, higher frequencies, packet closure, density gain, and interval gain remain open.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_priors()},
        "smooth_projector": {
            "epistemic_status": "PROVED",
            "statement": "Smooth Poisson summation gives |Theta_Q(x)|<<Q(1+Q||x||)^(-A), and occupancy annuli give |S_k|<<Q A_k without Cauchy-Schwarz.",
        },
        "new_band": {
            "epistemic_status": "PROVED",
            "statement": "The per-k exponent is 37/45, so all xi<94/225 close strictly; the new width beyond 163/450 is 1/18 and the endpoint ties.",
        },
        "analytic_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Improve the fixed-center integer-resonance count, rather than worst-interval occupancy, on 94/225<=xi<=83/75.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_82_smooth_phase_projector_v1.py --write",
            "check_command": "python3 proof/build_cycle_82_smooth_phase_projector_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_82_smooth_phase_projector_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 82 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 82 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 82 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

