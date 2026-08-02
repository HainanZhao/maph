#!/usr/bin/env python3
"""Seal Cycle 84 averaged-resonance Fourier band."""
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
OUTPUT = ROOT / "artifacts/cycle-84-averaged-resonance-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "discovery_candidate": (ROOT / "discovery/cycle-84-averaged-resonance-candidate-v1.md", "6f94f04e143d51abe2296ad339d44886183955de61177f3e7c87c020a9d7ab10"),
    "preregistration": (ROOT / "docs/cycle-84-averaged-resonance-preregistration-v1.md", "acbd72c66872e1c4fc3a7fd4f31fc0166a810082746677471ba083093b7058b6"),
    "document": (ROOT / "docs/cycle-84-averaged-resonance-v1.md", "9ae5f0c0bf6370c1e97ac4b3cc4643689bf4e7d799f65ada277bcddb5cf69177"),
    "conventions": (ROOT / "conventions/averaged_resonance_v1.py", "03ee059552c97e9acd69b9963c868459ac865dfad1fab144d9cabfefd3dfc3c9"),
    "tests": (ROOT / "tests/test_cycle_84_averaged_resonance_v1.py", "cce46be019eef4dfc23ef0f185baf0483b79f5546e73543aa2420af96abeeb12"),
    "cycle81": (ROOT / "artifacts/cycle-81-exact-q-transform-v1.json", "0753d455a2e9428b28f1b9dac59b04fd57008db562370202a300a38a818631a4"),
    "cycle82": (ROOT / "artifacts/cycle-82-smooth-phase-projector-v1.json", "5faff9b1b6a94da3df33e0b68423d0b9a0663a62c480d5713e2cea8a21ec4b11"),
    "cycle83": (ROOT / "artifacts/cycle-83-fejer-vdc-resonance-v1.json", "e946bcc64e4601a0822e81dfc6c0e5ee8296f46187af743716b8bd2cfde8fafe"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 84 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("averaged_resonance_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 84 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["new_cutoff"] == "43/75", "new cutoff")
    require(rows["band_width"] == "2/25", "band width")
    require(rows["crossing_gap_to_volume"] == "1/15", "crossing gap")
    return rows


def validate_priors() -> dict[str, str]:
    statuses = {
        "cycle81": "SEALED_EXACT_Q_TRANSFORM_LOG_RESONANCE_PROJECTOR_OPEN",
        "cycle82": "SEALED_SMOOTH_PROJECTOR_BAND_FIXED_CENTER_RESONANCE_OPEN",
        "cycle83": "SEALED_FEJER_VDC_BAND_HIGH_FREQUENCY_EXPONENT_PAIR_OPEN",
    }
    for label, status in statuses.items():
        payload = json.loads(INPUTS[label][0].read_text(encoding="utf-8"))
        require(payload.get("status") == status, f"{label} status mismatch")
    return {
        "cycle81_role": "supply exact smooth Fourier conventions",
        "cycle82_role": "supply the projector and annular decomposition",
        "cycle83_role": "supply the prior cutoff and fixed-center comparison",
    }


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-84-averaged-resonance-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_AVERAGED_RESONANCE_BAND_CROSSING_INVERSE_OPEN",
        "claim_boundary": "This artifact proves the joint (k,d) resonance incidence bound and closes only 37/75<=xi<43/75. The endpoint, higher frequencies, packet closure, density gain, and interval gain remain open.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_priors()},
        "crossing_lemma": {
            "epistemic_status": "PROVED",
            "statement": "Smooth k-projection and monotonicity give |B_j|<<D+jK, including rational-anchor multiples.",
        },
        "incidence_bound": {
            "epistemic_status": "PROVED",
            "statement": "At projector radius L/Q, I_L<<KDL/Q+D+KQ/L; fixed Schwartz decay preserves the L=1 exponents.",
        },
        "new_band": {
            "epistemic_status": "PROVED",
            "statement": "The block exponent is max(xi+3/5,14/15,xi+2/3), closing 37/75<=xi<43/75; width 2/25. The endpoint ties.",
        },
        "structural_lock": {
            "epistemic_status": "PROVED",
            "statement": "The crossing-discretization term stops unsigned incidence at 43/75, exactly 1/15 before its volume-only cutoff 16/25.",
        },
        "analytic_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Show a power-saving fraction of integer crossings are occupied or classify saturation as an anchor/valuation web; use signed cancellation beyond xi=16/25.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_84_averaged_resonance_v1.py --write",
            "check_command": "python3 proof/build_cycle_84_averaged_resonance_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_84_averaged_resonance_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 84 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 84 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 84 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

