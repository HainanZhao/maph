#!/usr/bin/env python3
"""Seal Cycle 60 coordinate-ANOVA identity."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-60-coordinate-anova-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-60-coordinate-anova-preregistration-v1.md", "2d98193c39074a0dc992ecee612b82f448514c8f1c7491fe7973b9b5f0b9977d"),
    "document": (ROOT / "docs/cycle-60-coordinate-anova-v1.md", "b42b4ff6286aaaf6aea4fcda743d5943e564baf932e7c0d4ab2c559a859eb7a0"),
    "conventions": (ROOT / "conventions/coordinate_anova_v1.py", "b0779f7cc64ea8dc03991599482fbfd6155956c5f28c20ad52a114da20cddf2f"),
    "tests": (ROOT / "tests/test_cycle_60_coordinate_anova_v1.py", "d87b97214a3d6dd39b58cd0662331dd7d1bdcd0b32267bf35aa5dcf304accc66"),
    "cycle57": (ROOT / "artifacts/cycle-57-cumulant-support-collapse-v1.json", "c2af9b4aa7c467c6e9d795eb0c7665b9769aa9e4c6187b3c0e9a7d5d94174e8d"),
    "cycle59": (ROOT / "artifacts/cycle-59-trigger-to-recurrence-v1.json", "f01cc7fa5fdf066f3c461b6db6227cfe7c4050ab6230fe58bd9ade8a45ad96fa"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_runtime() -> dict[str, Any]:
    runtime = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
    }
    require(runtime == EXPECTED_RUNTIME, "Cycle 60 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("coordinate_anova_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 60 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["s3"]["subset_component_count"] == 16, "s3 component count")
    require(rows["s4"]["subset_component_count"] == 32, "s4 component count")
    require("C_m(h_e,h_f)" in rows["s4"]["full_interaction_quadratic_norm"], "full interaction kernel")
    return rows


def validate_priors() -> dict[str, str]:
    cycle57 = json.loads(INPUTS["cycle57"][0].read_text(encoding="utf-8"))
    cycle59 = json.loads(INPUTS["cycle59"][0].read_text(encoding="utf-8"))
    require(cycle57.get("status") == "SEALED_HILBERT_EDGE_CUMULANT_RESTRICTION_3_50_OPEN", "Cycle 57 status mismatch")
    require(cycle59.get("status") == "SEALED_DIRECT_RESTRICTION_OR_GRAPH_AMPLIFICATION_OPEN", "Cycle 59 status mismatch")
    return {"cycle57_role": "Hilbert support representation", "cycle59_role": "complete-quadratic-form requirement"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-60-coordinate-anova-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_ANOVA_COMPONENT_RESTRICTION_OR_FLAT_ENERGY_INVERSE_OPEN",
        "claim_boundary": "This artifact proves an exact finite coordinate-ANOVA identity only. It does not force component variance or prove restriction, AMPR, density, or interval gains.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_priors()},
        "anova_identity": {
            "epistemic_status": "PROVED",
            "statement": "The phase-aligned tuple-energy density decomposes orthogonally by centered coordinate subsets; the full interaction is exactly the Cycle 56/57 Hilbert edge-cumulant quadratic form.",
        },
        "analytic_dichotomy": {
            "epistemic_status": "CONJECTURED",
            "statement": "Bound all nonconstant ANOVA components at coordinate-cardinality scale or classify the flat-energy branch using actual prime logarithms or detector surgery.",
        },
        "exact_replay": rows,
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_60_coordinate_anova_v1.py --write",
            "check_command": "python3 proof/build_cycle_60_coordinate_anova_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_60_coordinate_anova_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 60 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 60 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 60 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
