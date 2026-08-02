#!/usr/bin/env python3
"""Seal Cycle 44 Beatty-literature and derivative-test boundary."""
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
OUTPUT = ROOT / "artifacts/cycle-44-beatty-derivative-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-44-beatty-derivative-preregistration-v1.md", "752ac573a947e2102ad9c1b2667d1bc4931219da6d6e4ef5ab6ff623fb74e163"),
    "document": (ROOT / "docs/cycle-44-beatty-derivative-v1.md", "00ffc665b4683d80defe31dc2acd337b172cb82f0ebf3d2f1057dee5bf83f080"),
    "conventions": (ROOT / "conventions/beatty_derivative_v1.py", "cf6fb6fa82ce8bddb24a4c2096f90cfd3cd123935ccb6850102c6aa20ce52ab8"),
    "tests": (ROOT / "tests/test_cycle_44_beatty_derivative_v1.py", "381bb0e4851ea3f510adf7b3a6777f954760e09eb31c51f1b82a5ea818bdefa5"),
    "cycle43": (ROOT / "artifacts/cycle-43-row-lattice-beatty-v1.json", "96af26c677f43d4998cd25190456202d6c61d1297c9a493259048337ab7144b9"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 44 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("beatty_derivative_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 44 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["best_registered_saving"] == Fraction(12, 175), "best derivative saving")
    require(rows["best_registered_saving"] < rows["cycle39_margin_r4"], "margin comparison")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle43"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_AP_ROW_RESONANCE_CURVED_BEATTY_PRIME_PAIR_OPEN", "Cycle 43 status mismatch")
    return {"prior_role": "test fixed-slope Beatty theorems and one-variable derivative estimates against the curved strip"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-44-beatty-derivative-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_FIXED_BEATTY_AND_DERIVATIVE_TEST_INSUFFICIENT_JOINT_PK_OPEN",
        "claim_boundary": "This artifact checks the cited fixed-slope Beatty hypotheses and exact derivative-test exponent ledger. It does not delimit all Beatty, exponent-pair, sieve, or joint p-k methods and proves no density or interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "source_boundary": {
            "epistemic_status": "PROVED",
            "statement": "Banks-Shparlinski fixes an irrational finite-type slope with slope-dependent constants; Banks-Guo prime pairs additionally assume strong Hardy-Littlewood. Neither supplies the shrinking-slope unconditional input.",
            "sources": ["https://arxiv.org/abs/0708.1015", "https://arxiv.org/abs/1612.01468", "https://arxiv.org/abs/2407.02094"],
        },
        "derivative_boundary": {
            "epistemic_status": "PROVED",
            "statement": "At Fourier resolution 11/25, the best saving from the checked explicit d-th derivative theorem is 12/175 at d=4, below both closure margins.",
        },
        "analytic_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Use joint p-k curvature/sieve averaging or prove nonlattice row decay; one-variable derivative tests are not allocated as the closing engine.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_44_beatty_derivative_v1.py --write",
            "check_command": "python3 proof/build_cycle_44_beatty_derivative_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_44_beatty_derivative_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 44 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 44 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 44 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
