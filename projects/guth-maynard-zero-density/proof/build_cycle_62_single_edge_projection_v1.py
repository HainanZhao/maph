#!/usr/bin/env python3
"""Seal Cycle 62 single-edge projection boundary."""
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
OUTPUT = ROOT / "artifacts/cycle-62-single-edge-projection-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-62-single-edge-projection-preregistration-v1.md", "2ba2f881cdce721eea9641749b488e0c068655258eb29972ca5ce4403ccaed19"),
    "document": (ROOT / "docs/cycle-62-single-edge-projection-v1.md", "845435ce3813b86758b03810b2d332f69c48be2c2a682c393dd19093f76e9fb8"),
    "conventions": (ROOT / "conventions/single_edge_projection_v1.py", "0e2b384f69b61991e6f37ee7a8643f127153cfd939fa55ef422fab9317fd27d1"),
    "tests": (ROOT / "tests/test_cycle_62_single_edge_projection_v1.py", "aab377017b2439d5e1800fb535b30561267861fe7502db2a458c41dcd1749567"),
    "cycle61": (ROOT / "artifacts/cycle-61-coefficient-projection-inverse-v1.json", "d44a5144f06d51336c0be81e89bf24d4007939d1cacdaab498251adc708164ff"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 62 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("single_edge_projection_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 62 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["zero_kernel_endpoint"]["retained_fraction"] == 1, "zero-kernel saturation")
    require(rows["s4"]["union_bound_verified"], "s4 union bound")
    require(rows["s4"]["genuine_edge_nonnegative"], "genuine convolution positivity")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle61"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_PRIME_COORDINATE_MARGINAL_CAPTURE_OR_ANNIHILATOR_INVERSE_OPEN", "Cycle 61 status mismatch")
    return {"prior_role": "stress-test universal marginal capture on one Fourier edge"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-62-single-edge-projection-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_NONNEGATIVE_AUTOCORRELATION_ANOVA_OR_RECURRENCE_OPEN",
        "claim_boundary": "This artifact proves a pointwise projection boundary only. It does not obstruct estimates using nonnegative multi-edge autocorrelation vectors and proves no AMPR, density, or interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "single_edge_boundary": {
            "epistemic_status": "PROVED",
            "statement": "Full coordinate centering retains fraction (1-|k(mh)|^2)(1-|k(h)|^2)^s of one Fourier edge, hence 1-o(1) when normalized kernels are polynomially small.",
        },
        "valid_vector_structure": {
            "epistemic_status": "PROVED",
            "statement": "Phase-aligned edge vectors satisfy beta_n=|sum_t z_t n^(-it)|^2>=0 and couple all row differences; this structure is absent from the single-edge stress model.",
        },
        "analytic_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Use nonnegative rank-one autocorrelation and a target-violating separated row set to prove ANOVA restriction or extract recurrence.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_62_single_edge_projection_v1.py --write",
            "check_command": "python3 proof/build_cycle_62_single_edge_projection_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_62_single_edge_projection_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 62 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 62 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 62 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
