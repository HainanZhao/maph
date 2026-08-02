#!/usr/bin/env python3
"""Seal Cycle 39 moment-amplified prime-monomial reduction."""
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
OUTPUT = ROOT / "artifacts/cycle-39-moment-amplified-prime-monomial-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-39-moment-amplified-prime-monomial-preregistration-v1.md", "1dcd275102049dee34c5c5325eeb0468978326cedd9c4c311c7813fa45e2063b"),
    "document": (ROOT / "docs/cycle-39-moment-amplified-prime-monomial-v1.md", "59ac1d3864e713ac998c037cd3d3973c3af9063ec12c212da42871e9f5879080"),
    "conventions": (ROOT / "conventions/moment_amplified_prime_monomial_v1.py", "6932c2ebae9f1b210e3ffd468827c443ebbdae26668d9f7516f31eb28f758bb2"),
    "tests": (ROOT / "tests/test_cycle_39_moment_amplified_prime_monomial_v1.py", "1c44a189808d9edfe4705bed6d8d5d830e5b583ce22c3eab63a9facba9eccfbe"),
    "cycle38": (ROOT / "artifacts/cycle-38-vector-harmonic-two-scale-v1.json", "0da5a1791b7228a19651db15ecf3bce1909bbc2c57b985bee107e8787010de52"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 39 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("moment_amplified_prime_monomial_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 39 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["closing_r2"]["conditional_count_bound"] == Fraction(1, 2), "r2 count")
    require(rows["closing_r2"]["closing_margin"] == Fraction(17, 50), "r2 margin")
    require(rows["closing_r4"]["conditional_count_bound"] == Fraction(7, 10), "r4 count")
    require(rows["closing_r4"]["closing_margin"] == Fraction(7, 50), "r4 margin")
    require(rows["coefficients_s4"]["coefficient_bound"] == 72, "coefficient multiplicity")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle38"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_VECTOR_RESCALING_COLLISION_TWO_SCALE_PRIME_MONOMIAL_OPEN", "Cycle 38 status mismatch")
    return {"prior_role": "amplify the two-scale prime-monomial lift instead of applying an unamplified vector mean square"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-39-moment-amplified-prime-monomial-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_MOMENT_AMPLIFIED_PRIME_MONOMIAL_RESTRICTION_OPEN",
        "claim_boundary": "This artifact proves fixed-s coefficient multiplicity and the conditional closure ledger. It does not prove AMPR_s, a kernel-count gain, a density gain, or an interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "coefficient_theorem": {
            "epistemic_status": "PROVED",
            "statement": "For fixed s and every m>=2, coefficients of K(t)^s K(mt) are at most C_s=(1+floor(s/2))*s!, and their square norm lies between M^(s+1) and C_s*M^(s+1).",
        },
        "conditional_reduction": {
            "epistemic_status": "PROVED",
            "statement": "AMPR_3 gives count exponent 1/2 with margin 17/50 on the e=3/5 branch; AMPR_4 gives 7/10 with margin 7/50 on the e=6/5 branch.",
        },
        "analytic_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "For hollow Delta-separated rows, prove sum_t sum_m |K(t)^s K(mt)|^2 <= X^(s+31/10+o(1)) for s=3,4, uniformly over 2<=m<=X^(3/10).",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_json(rows),
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_39_moment_amplified_prime_monomial_v1.py --write",
            "check_command": "python3 proof/build_cycle_39_moment_amplified_prime_monomial_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_39_moment_amplified_prime_monomial_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 39 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 39 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 39 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
