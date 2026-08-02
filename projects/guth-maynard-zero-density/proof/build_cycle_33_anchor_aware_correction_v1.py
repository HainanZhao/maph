#!/usr/bin/env python3
"""Seal Cycle 33 anchor-aware correction."""
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
OUTPUT = ROOT / "artifacts/cycle-33-anchor-aware-correction-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-33-anchor-aware-correction-preregistration-v1.md", "2d123d641c15c90e308334c167735ce16e329b881ca7ab6414d6029d82b8a8f6"),
    "document": (ROOT / "docs/cycle-33-anchor-aware-correction-v1.md", "43eb1e5211a7feee7530870db67be95d685e2e17b3d984adfc26a1045c6e81f6"),
    "conventions": (ROOT / "conventions/anchor_aware_correction_v1.py", "b04d6745bc5b3af40f72f8f5988080b6b497b383873446967829091e496c6090"),
    "tests": (ROOT / "tests/test_cycle_33_anchor_aware_correction_v1.py", "92df161a1d403d2d201d97398634377262e0facde56bfaff552f6a966839f28a"),
    "cycle31": (ROOT / "artifacts/cycle-31-variable-rank-self-dual-v1.json", "7c6f3a75cbe0d16ebe729260cbc7ac42fee4b86e00b80fb832926317e8f11784"),
    "cycle32": (ROOT / "artifacts/cycle-32-flat-support-modulation-v1.json", "be844d4e3967573eb7e00464e6be3a85a10d37c943c3a6e3e8607734b04bfa22"),
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
    runtime = {"implementation": platform.python_implementation(), "python": platform.python_version(), "optimization_level": sys.flags.optimize}
    require(runtime == EXPECTED_RUNTIME, "Cycle 33 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("anchor_aware_correction_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 33 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["flat_phase_row"]["augmented_determinant"] == 0, "actual-prime witness determinant mismatch")
    require(rows["flat_phase_row"]["distance_to_row_span_squared"] == 0, "actual-prime witness distance mismatch")
    require(rows["full_column_rank"]["reconstruction"] == rows["full_column_rank"]["detector"], "dimension witness mismatch")
    return rows


def validate_prior() -> dict[str, str]:
    expected = {
        "cycle31": "SEALED_VARIABLE_RANK_SELF_DUAL_BLOCK_REDUCTION",
        "cycle32": "SEALED_FLAT_SUPPORT_MODULATION_LADDER",
    }
    for label, status in expected.items():
        prior = json.loads(INPUTS[label][0].read_text(encoding="utf-8"))
        require(prior.get("status") == status, f"{label} status mismatch")
    return {"prior_role": "flat-support ladder retained; universal square-rung distance gate corrected"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-33-anchor-aware-correction-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_ANCHOR_WITNESS_UNIVERSAL_DISTANCE_GATE_FALSE",
        "claim_boundary": "This artifact disproves only universal flat-vector distance or augmented-determinant lower bounds and replaces them by an anchor-aware alternative. It does not bound either anchor or transverse branch, close the skeleton target, improve zero density, or improve intervals.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "actual_prime_witness": {
            "epistemic_status": "PROVED",
            "statement": "A normalized restricted row p^(-it0) is exactly flat and lies exactly in any row span containing t0; its augmented Gram determinant is zero.",
        },
        "dimension_boundary": {
            "epistemic_status": "PROVED",
            "statement": "For full column rank with k>=N, every detector lies in the row span; invertibility confirms rather than excludes reconstruction.",
        },
        "replacement_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Few-anchor reconstruction must yield a weighted restricted-prime-kernel recurrence bound; reconstruction transverse to every X^o(1)-anchor span must yield a many-row arithmetic exterior-volume bound.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_json(rows),
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_33_anchor_aware_correction_v1.py --write",
            "check_command": "python3 proof/build_cycle_33_anchor_aware_correction_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_33_anchor_aware_correction_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 33 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 33 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 33 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
