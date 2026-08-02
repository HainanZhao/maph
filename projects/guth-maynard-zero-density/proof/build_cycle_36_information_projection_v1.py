#!/usr/bin/env python3
"""Seal Cycle 36 first-harmonic information-projection saturation."""
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
OUTPUT = ROOT / "artifacts/cycle-36-information-projection-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-36-information-projection-preregistration-v1.md", "3cd926401f4bfb69a1140e0419d2de876723ecf6f94e4cef6387807be62a074b"),
    "document": (ROOT / "docs/cycle-36-information-projection-v1.md", "d88cff80b85a2e45eb9b3675fd3978e62c506904369c1a4fcadd6f517b4e5f21"),
    "conventions": (ROOT / "conventions/information_projection_v1.py", "bffc26fb3a7a394d4c4b4469497aa935c1204e8151a71595710d63a8cf5fee4c"),
    "tests": (ROOT / "tests/test_cycle_36_information_projection_v1.py", "c907f715240f6888d8c300ccf46b36327bb1e045d463691d3d84cd8b361120e1"),
    "cycle19": (ROOT / "artifacts/cycle-19-synchronization-graph-v1.json", "3c68ee97a31f7a7cb2612769f58c2645b4a58332aeceaa856d7082de635aeb63"),
    "cycle20": (ROOT / "artifacts/cycle-20-exterior-volume-v1.json", "5d647c7ccd850cdae77cb04bb5287d175cb210f1d546ab5f5341b50c4f185b5c"),
    "cycle35": (ROOT / "artifacts/cycle-35-kernel-engine-ledger-v1.json", "cedc4cce7699fa02db9cabe2346286aac3eabd4f82e4559d4f0263c268cdce3e"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 36 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("information_projection_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 36 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["bessel_series"]["rate_r_2_4_6"][0] == 1, "information leading constant")
    require(rows["exponent_match"]["information_leading"] == Fraction(6, 25), "information scale")
    require(rows["exponent_match"]["von_mises_second_harmonic_kernel"] == Fraction(2, 5), "second harmonic scale")
    return rows


def validate_prior() -> dict[str, str]:
    expected = {
        "cycle19": "SEALED_SYNCHRONIZATION_GRAPH_ABSTRACT_BOUNDARY_PRIME_LOG_CLOSURE_OPEN",
        "cycle20": "SEALED_SHARP_EXTERIOR_VOLUME_COLLAPSE_PRIME_DETERMINANT_LOWER_BOUND_OPEN",
        "cycle35": "SEALED_THREE_KERNEL_REDUCTIONS_ENTROPY_VOLUME_MATCH",
    }
    for label, status in expected.items():
        prior = json.loads(INPUTS[label][0].read_text(encoding="utf-8"))
        require(prior.get("status") == status, f"{label} status mismatch")
    return {"prior_role": "compare the Cycle 35 entropy budget with sharp Cycle 20 volume and Cycle 19 second-harmonic scales"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-36-information-projection-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_FIRST_HARMONIC_ENTROPY_DETERMINANT_EQUIVALENCE_EXCESS_OPEN",
        "claim_boundary": "This artifact proves an exact information-projection decomposition and scoped first-harmonic saturation. It does not control entropy excess or joint von Mises rigidity on prime rows, prove the kernel count, improve density, or improve intervals.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "information_projection": {
            "epistemic_status": "PROVED",
            "statement": "D(q||u)=J(r)+E(q), with E(q)=D(q||qstar)>=0 and J(r)=r^2+r^4/4+5r^6/36+O(r^8).",
        },
        "scoped_saturation": {
            "epistemic_status": "PROVED",
            "statement": "At k=X^(21/25), r^2=X^(-3/5), kJ(r) and the sharp common-projection negative log determinant both have leading constant one at scale X^(6/25).",
        },
        "rigidity_boundary": {
            "epistemic_status": "PROVED",
            "statement": "Quadratically tiny excess returns the von Mises second harmonic at unnormalized scale X^(2/5), exactly the Cycle 19 popular-kernel scale; only excess entropy or joint rigidity is new.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_json(rows),
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_36_information_projection_v1.py --write",
            "check_command": "python3 proof/build_cycle_36_information_projection_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_36_information_projection_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 36 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 36 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 36 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
