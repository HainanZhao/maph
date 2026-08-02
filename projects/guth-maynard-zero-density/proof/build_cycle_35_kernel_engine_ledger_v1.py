#!/usr/bin/env python3
"""Seal Cycle 35 kernel-engine ledger and entropy--volume match."""
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
OUTPUT = ROOT / "artifacts/cycle-35-kernel-engine-ledger-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-35-kernel-engine-ledger-preregistration-v1.md", "9cd11dcfa8c0275c8066a85e30977f9036593aa52a769b6fc81c92e3f3333b1f"),
    "document": (ROOT / "docs/cycle-35-kernel-engine-ledger-v1.md", "0a2411dc15faf13ab0cef6c68da8530eeab5cda0891e11b67dc22a3e0d5afe46"),
    "conventions": (ROOT / "conventions/kernel_engine_ledger_v1.py", "2b6cae8144aea03c6602d2357031023c7f9c66f2047c11a0950a626b14f81a34"),
    "tests": (ROOT / "tests/test_cycle_35_kernel_engine_ledger_v1.py", "7e884e41a0e2334ae560b2bfeb3877a83c762340effc89cfa9bd97367a4c0f0e"),
    "cycle20": (ROOT / "artifacts/cycle-20-exterior-volume-v1.json", "5d647c7ccd850cdae77cb04bb5287d175cb210f1d546ab5f5341b50c4f185b5c"),
    "cycle23": (ROOT / "artifacts/cycle-23-residual-spectral-shift-v1.json", "605e7a3eb5ac5b4e342b512e4465762d43b1b919051e4dafd01058e7ae14121b"),
    "cycle34": (ROOT / "artifacts/cycle-34-stable-anchor-kernel-v1.json", "0390c0f9ce57deccfee89e2fa3632c9a0e217818f9d7b94ddbe5960ead63c4a1"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_json(value: Any) -> Any:
    if isinstance(value, Fraction):
        return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    if isinstance(value, tuple):
        return [exact_json(item) for item in value]
    if isinstance(value, dict):
        return {str(key): exact_json(item) for key, item in value.items()}
    return value


def check_runtime() -> dict[str, Any]:
    runtime = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
    }
    require(runtime == EXPECTED_RUNTIME, "Cycle 35 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("kernel_engine_ledger_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 35 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["hollow_fractional"]["target_bound"] == Fraction(21, 5), "hollow target mismatch")
    require(rows["hollow_fractional"]["required_saving"] == Fraction(3, 5), "spacing saving mismatch")
    require(rows["phase_entropy"]["target_accumulation_budget"] == Fraction(6, 25), "entropy budget mismatch")
    return rows


def validate_prior() -> dict[str, str]:
    expected = {
        "cycle20": "SEALED_SHARP_EXTERIOR_VOLUME_COLLAPSE_PRIME_DETERMINANT_LOWER_BOUND_OPEN",
        "cycle23": "SEALED_RESIDUAL_SPECTRAL_SHIFT_INVERSE_LEVERAGE_DICHOTOMY_PRIME_GATE_OPEN",
        "cycle34": "SEALED_STABLE_ANCHOR_TO_UNWEIGHTED_PRIME_KERNEL_REDUCTION",
    }
    for label, status in expected.items():
        prior = json.loads(INPUTS[label][0].read_text(encoding="utf-8"))
        require(prior.get("status") == status, f"{label} status mismatch")
    return {"prior_role": "unweighted kernel target plus independently sealed 6/25 volume and shift scales"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-35-kernel-engine-ledger-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_THREE_KERNEL_REDUCTIONS_ENTROPY_VOLUME_MATCH",
        "claim_boundary": "This artifact proves exact sufficient ledgers and a finite phase-histogram entropy lemma. It does not prove hollow fractional restriction, sifted curvature, entropy accumulation, the kernel count, a density gain, or an interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "hollow_fractional": {
            "epistemic_status": "PROVED",
            "statement": "An off-origin separated 24/5 moment bound X^(21/5+o(1)) implies the target; it saves exactly the spacing exponent 3/5 over the global scale.",
        },
        "sieve_curvature": {
            "epistemic_status": "PROVED",
            "statement": "The aggregate shifted-prime correlation bound X^(2+o(1))/|t| implies a pointwise power saving above X^(3/5+eta); the analogous unrestricted integer estimate follows from first derivatives only at low time.",
            "prime_input": "CONJECTURED",
        },
        "phase_entropy": {
            "epistemic_status": "PROVED",
            "statement": "Each threshold row has coarse histogram divergence at least delta^2/8; the target total exponent is 6/25, exactly matching the sealed residual volume/shift scale.",
            "accumulation_input": "CONJECTURED",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_json(rows),
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_35_kernel_engine_ledger_v1.py --write",
            "check_command": "python3 proof/build_cycle_35_kernel_engine_ledger_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_35_kernel_engine_ledger_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 35 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 35 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 35 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
