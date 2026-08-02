#!/usr/bin/env python3
"""Seal Cycle 83 Fejer--van der Corput resonance band."""
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
OUTPUT = ROOT / "artifacts/cycle-83-fejer-vdc-resonance-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "discovery_candidate": (ROOT / "discovery/cycle-83-fejer-vdc-candidate-v1.md", "2f2c655ec6dc611b7c8c4be45da8f4b8a797b7a9029d0c85e486cde5c54f0742"),
    "preregistration": (ROOT / "docs/cycle-83-fejer-vdc-preregistration-v1.md", "42924d6ea6ac024527da2878fcdfa49056d66027c1f7807bab3c031de05e0716"),
    "document": (ROOT / "docs/cycle-83-fejer-vdc-resonance-v1.md", "04081ef7f814c1b7c1afee90625139f2a42f2b61283d2aee3f2ffeef7806988d"),
    "conventions": (ROOT / "conventions/fejer_vdc_resonance_v1.py", "113b5d99c56e42825c995d9f93be170c502956fb5cd0634fc6666b27c7d3490b"),
    "tests": (ROOT / "tests/test_cycle_83_fejer_vdc_resonance_v1.py", "de2c3215e12cd9abd78576807888338f18e945b50caf32462d776c027116cacd"),
    "cycle81": (ROOT / "artifacts/cycle-81-exact-q-transform-v1.json", "0753d455a2e9428b28f1b9dac59b04fd57008db562370202a300a38a818631a4"),
    "cycle82": (ROOT / "artifacts/cycle-82-smooth-phase-projector-v1.json", "5faff9b1b6a94da3df33e0b68423d0b9a0663a62c480d5713e2cea8a21ec4b11"),
    "gm_primary_source": (ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex", "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 83 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("fejer_vdc_resonance_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 83 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["new_cutoff"] == "37/75", "new cutoff")
    require(rows["band_width"] == "17/225", "band width")
    require(rows["derivative_ceiling_at_endpoint"] == "-28/75", "derivative range")
    return rows


def validate_priors() -> dict[str, str]:
    cycle81 = json.loads(INPUTS["cycle81"][0].read_text(encoding="utf-8"))
    cycle82 = json.loads(INPUTS["cycle82"][0].read_text(encoding="utf-8"))
    require(cycle81.get("status") == "SEALED_EXACT_Q_TRANSFORM_LOG_RESONANCE_PROJECTOR_OPEN", "Cycle 81 status mismatch")
    require(cycle82.get("status") == "SEALED_SMOOTH_PROJECTOR_BAND_FIXED_CENTER_RESONANCE_OPEN", "Cycle 82 status mismatch")
    return {
        "cycle81_role": "supply the exact smooth transform and sign convention",
        "cycle82_role": "supply the projector-to-resonance reduction and prior cutoff",
        "source_role": "record primary Guth--Maynard use of the classical first/second derivative bounds",
    }


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-83-fejer-vdc-resonance-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_FEJER_VDC_BAND_HIGH_FREQUENCY_EXPONENT_PAIR_OPEN",
        "claim_boundary": "This artifact proves the fixed-center Fejer--second-derivative resonance estimate and closes only 94/225<=xi<37/75. The endpoint, higher frequencies, packet closure, density gain, and interval gain remain open.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_priors()},
        "resonance_bound": {
            "epistemic_status": "PROVED",
            "statement": "Fejer plus the second-derivative test gives R_k<<D/Q+sqrt(kQ)+D/sqrt(kQ), with the sqrt(kQ) term dominant on the active range.",
        },
        "annular_extension": {
            "epistemic_status": "PROVED",
            "statement": "Bandwidth Q/L at radius L/Q and fixed Schwartz decay preserve the central resonance exponent.",
        },
        "new_band": {
            "epistemic_status": "PROVED",
            "statement": "The Fourier block exponent is 3xi/2+1/2, closing 94/225<=xi<37/75; width 17/225. The endpoint ties.",
        },
        "analytic_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Beat the square-root derivative term using an exponent pair, k-average, or an inverse theorem on 37/75<=xi<=83/75.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_83_fejer_vdc_resonance_v1.py --write",
            "check_command": "python3 proof/build_cycle_83_fejer_vdc_resonance_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_83_fejer_vdc_resonance_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 83 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 83 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 83 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

