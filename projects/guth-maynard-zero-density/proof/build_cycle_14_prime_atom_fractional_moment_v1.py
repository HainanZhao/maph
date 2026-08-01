#!/usr/bin/env python3
"""Seal Cycle 14 prime-atom fractional-moment envelope."""
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
OUTPUT = ROOT / "artifacts/cycle-14-prime-atom-fractional-moment-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-14-prime-atom-fractional-moment-preregistration-v1.md", "e90d3342510efc01e45d72d2e119a4570fd618a0f04b9456be4c92153f70ba63"),
    "document": (ROOT / "docs/cycle-14-prime-atom-fractional-moment-v1.md", "0795a8b430990b8ae749fd852e46b3bf5f34358178362c0e8272f15c8ca9c1e3"),
    "conventions": (ROOT / "conventions/prime_atom_fractional_moment_v1.py", "771ddf116423d62c8919d5e09f5d599c3e0b9ebe252ad52bba8f71cc58f6ccaf"),
    "tests": (ROOT / "tests/test_cycle_14_prime_atom_fractional_moment_v1.py", "3d886d1b4cefc7e8d3006ee8bb6f4659ffbe903df2db30919e96b5b15d83c471"),
    "gm_source": (ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex", "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"),
    "mp_source": (ROOT / "artifacts/sources/maynard-pratt-2206.11729/HalfIsolatedv2.tex", "ec22dfdb8394b8ab4b228d0f438d19858015fc74330e247d08f36e5830782426"),
    "cycle13_artifact": (ROOT / "artifacts/cycle-13-source-obstruction-weighted-tensor-v1.json", "c1c057b089ed8626d3d049520eeb1a5ec1709bc55e24db1b0374f09a05588ecf"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_json(value: Any) -> Any:
    if isinstance(value, Fraction):
        return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    if isinstance(value, list):
        return [exact_json(item) for item in value]
    if isinstance(value, dict):
        return {str(key): exact_json(item) for key, item in value.items()}
    return value


def check_runtime() -> dict[str, Any]:
    runtime = {"implementation": platform.python_implementation(), "python": platform.python_version(), "optimization_level": sys.flags.optimize}
    require(runtime == EXPECTED_RUNTIME, "Cycle 14 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("prime_atom_fractional_moment_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 14 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["integer_census"]["optimum_local_rows"] == 8, "integer optimum mismatch")
    require(rows["continuous_optimum"]["local_rows"] == Fraction(36, 5), "continuous optimum mismatch")
    return rows


def validate_sources() -> dict[str, str]:
    gm = INPUTS["gm_source"][0].read_text(encoding="utf-8")
    require("$N=T^{5/13}$" in gm and "$T_1=T^{12/13}$" in gm, "GM critical source anchors missing")
    mp = INPUTS["mp_source"][0].read_text(encoding="utf-8")
    for needle in ("label{def:YHalfIsolated}", "label{prp:HalfIsolated}", "T^{2(1-\\sigma)+o(1)}"):
        require(needle in mp, f"Maynard--Pratt source anchor missing: {needle}")
    return {
        "gm_critical_configuration": "TeX line 2398",
        "mp_half_isolated_definition": "TeX lines 380--405",
        "mp_lambda_detector": "Proposition HalfIsolated, TeX lines 721--729",
        "mp_existing_count": "stated theorem near TeX lines 201--208",
    }


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-14-prime-atom-fractional-moment-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_INTEGER_MOMENT_QUANTIZATION_FRACTIONAL_PRIME_TARGET_OPEN",
        "claim_boundary": "This artifact proves an exact exponent-model barrier and identifies a conjectural prime-specific fractional target. It does not prove that target, a zero-density gain, an interval improvement, or applicability of a half-isolated detector to arbitrary zeros.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "source_context": {"epistemic_status": "PROVED", **validate_sources()},
        "integer_moment_barrier": {
            "epistemic_status": "PROVED",
            "envelope": "E(k)=max(12-2k,3k)",
            "integer_optimum": "E(2)=8",
            "continuous_optimum": "E(12/5)=36/5",
            "integer_penalty": "4/5",
            "ordinary_interpolation": "At order 24/5 it gives 42/5, not 36/5.",
        },
        "half_isolated_scope": {
            "epistemic_status": "PROVED",
            "statement": "The source-checked Lambda detector applies to Y-half-isolated zeros, a class already bounded by T^(2(1-sigma)+o(1)); it cannot be substituted for the all-zero Type-I detector.",
        },
        "fractional_prime_restriction": {
            "epistemic_status": "CONJECTURED",
            "target": "integral_H |P|^(24/5) <= v^(24+o(1)), or a restricted weak-type analogue",
            "implication": "Conditional local exponent 36/5 and gain 4/5 for the prime atom.",
            "falsifier": "A source-scale prime-supported family with 24/5 moment v^(24+kappa-o(1)) for fixed kappa>0.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_json(rows),
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_14_prime_atom_fractional_moment_v1.py --write",
            "check_command": "python3 proof/build_cycle_14_prime_atom_fractional_moment_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_14_prime_atom_fractional_moment_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 14 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 14 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 14 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
