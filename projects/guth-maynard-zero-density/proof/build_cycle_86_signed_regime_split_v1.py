#!/usr/bin/env python3
"""Seal Cycle 86 zero-mode identity and signed-regime contracts."""
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
OUTPUT = ROOT / "artifacts/cycle-86-signed-regime-split-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "discovery_candidate": (ROOT / "discovery/cycle-86-signed-regime-candidate-v1.md", "8df135dbd2a4b07260c81fbedf5f5ea4327d4b2303225a21fe25692455a106ef"),
    "preregistration": (ROOT / "docs/cycle-86-signed-regime-preregistration-v1.md", "7eb35b66522850c4e7aa285fcf95772dd91b206ad60a4035300de00669698c05"),
    "document": (ROOT / "docs/cycle-86-signed-regime-split-v1.md", "bfa77256c12c10ebd226b085b851cb8fa27de4bd357974716d6efff8cf611fab"),
    "conventions": (ROOT / "conventions/signed_regime_split_v1.py", "2c16c4a9618a8a947243ad40501ae39ea9fdc6f78edf5d1f64792c9e5d7f522f"),
    "tests": (ROOT / "tests/test_cycle_86_signed_regime_split_v1.py", "d904d66cdcf5f4f271eac28de73dc40a8daf9e0c58817069d7eec513a2ca76a9"),
    "cycle81": (ROOT / "artifacts/cycle-81-exact-q-transform-v1.json", "0753d455a2e9428b28f1b9dac59b04fd57008db562370202a300a38a818631a4"),
    "cycle85": (ROOT / "artifacts/cycle-85-log-crossing-occupancy-v1.json", "c35f1fb2425f9e54497225907e66b69d0176fdc4f4030c8c721bf82d66d3c2e9"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 86 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("signed_regime_split_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 86 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["moment_boundary"] == "58/75", "moment boundary")
    require(rows["ceiling_average_allowance"] == "2/15", "ceiling allowance")
    require("V(0)=0" in rows["projector_zero_mode"], "zero mode")
    return rows


def validate_priors() -> dict[str, str]:
    cycle81 = json.loads(INPUTS["cycle81"][0].read_text(encoding="utf-8"))
    cycle85 = json.loads(INPUTS["cycle85"][0].read_text(encoding="utf-8"))
    require(cycle81.get("status") == "SEALED_EXACT_Q_TRANSFORM_LOG_RESONANCE_PROJECTOR_OPEN", "Cycle 81 status mismatch")
    require(cycle85.get("status") == "SEALED_UNSIGNED_INCIDENCE_VOLUME_LIMIT_SIGNED_RESONANCE_OPEN", "Cycle 85 status mismatch")
    return {
        "cycle81_role": "supply exact projector convention and dual transform",
        "cycle85_role": "supply the unsigned volume boundary 16/25",
    }


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-86-signed-regime-split-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_SIGNED_REGIME_SPLIT_MOMENT_AND_LARGE_VALUES_OPEN",
        "claim_boundary": "This artifact proves the signed projector zero mode and exact moment/large-value target split. It proves no second moment, large-value estimate, new Fourier-band closure, packet closure, density gain, or interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_priors()},
        "zero_mode": {
            "epistemic_status": "PROVED",
            "statement": "The smooth q-projector has circle mean V(0)=0 because its dyadic weight is supported in (0,infinity).",
        },
        "moment_contract": {
            "epistemic_status": "PROVED",
            "statement": "A diagonal-strength second moment gives block exponent xi+7/15 and would close 16/25<=xi<58/75; the endpoint ties.",
        },
        "large_value_contract": {
            "epistemic_status": "PROVED",
            "statement": "For 58/75<=xi<=83/75 pointwise square-root size is insufficient; dyadic large values must satisfy s+log_X M_xi(s)<31/25. The ceiling average allowance is 2/15.",
        },
        "analytic_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Prove the diagonal-strength signed moment below 58/75 and a sparse-large-value/inverse theorem above it.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_86_signed_regime_split_v1.py --write",
            "check_command": "python3 proof/build_cycle_86_signed_regime_split_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_86_signed_regime_split_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 86 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 86 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 86 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

