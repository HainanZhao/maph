#!/usr/bin/env python3
"""Seal Cycle 18 coherent-cluster skeleton reduction."""
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
OUTPUT = ROOT / "artifacts/cycle-18-coherent-cluster-skeleton-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-18-coherent-cluster-skeleton-preregistration-v1.md", "ae6b429a8c3981c1c4b2ca1799d048e5d335f16cb36f82ec180e756313cb894a"),
    "document": (ROOT / "docs/cycle-18-coherent-cluster-skeleton-v1.md", "726d4a5c0dccde95c7a48947661fa8c1b16380877a5ac20a9eae7657dd2127a7"),
    "conventions": (ROOT / "conventions/coherent_cluster_skeleton_v1.py", "da415df6b9377c9a1187ab2b4e2de33335b74fd43f8ba243e9b17dea63644366"),
    "tests": (ROOT / "tests/test_cycle_18_coherent_cluster_skeleton_v1.py", "4e8e0c815df94d62270e50f0cd5dfbd87581d0341031ffae66d6f93ebb0cf98f"),
    "gm_source": (ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex", "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"),
    "cycle17_result": (ROOT / "artifacts/cycle-17-prime-phase-separable-search-v1.json", "8ce4a5592b1ce895b62c659b4568e10992f84f92574db9f2b3f799d1189b89f6"),
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
    runtime = {"implementation": platform.python_implementation(), "python": platform.python_version(), "optimization_level": sys.flags.optimize}
    require(runtime == EXPECTED_RUNTIME, "Cycle 18 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("coherent_cluster_skeleton_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 18 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["local_large_values"]["cluster_exponent"] == Fraction(3, 5), "cluster exponent mismatch")
    require(rows["skeleton_translation"]["target_skeleton"] == Fraction(21, 25), "skeleton target mismatch")
    return rows


def validate_source() -> dict[str, str]:
    source = INPUTS["gm_source"][0].read_text(encoding="utf-8")
    require("N^2V^{-2}+T\\min(NV^{-2},N^4 V^{-6})" in source, "classical large-values source anchor missing")
    cycle17 = json.loads(INPUTS["cycle17_result"][0].read_text(encoding="utf-8"))
    require(cycle17.get("status") == "BASELINE_APPROACHED", "Cycle 17 adverse status mismatch")
    return {"classical_large_values": "GM equation ClassicalLargeValue, TeX lines 84--87", "cycle17_role": "finite clustered adverse evidence only"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-18-coherent-cluster-skeleton-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_COHERENT_CLUSTER_COST_SEPARATED_RECURRENCE_SKELETON_OPEN",
        "claim_boundary": "This artifact proves a covering reduction using the checked classical large-values estimate. It does not bound the separated skeleton, prove a rank-one semiprime saving, select a prime component on zero rows, improve density, or improve intervals.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "source_context": {"epistemic_status": "PROVED", **validate_source()},
        "local_cluster": {
            "epistemic_status": "PROVED",
            "statement": "Every interval of length 2X^(3/5) contains at most X^(3/5+o(1)) one-separated rows with |P|>=X^(7/10).",
        },
        "skeleton_reduction": {
            "epistemic_status": "PROVED",
            "statement": "A maximal X^(3/5)-separated subset C covers W by radius-X^(3/5) intervals and |W|<=X^(3/5+o(1))|C|.",
            "target": "It suffices to prove |C|<=X^(21/25+o(1)).",
            "required_saving_in_X": "4/25",
        },
        "recurrence_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Bound the number of X^(3/5)-separated recurrences of one common prime coefficient vector at threshold X^(7/10) by X^(21/25+o(1)).",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_json(rows),
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_18_coherent_cluster_skeleton_v1.py --write",
            "check_command": "python3 proof/build_cycle_18_coherent_cluster_skeleton_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_18_coherent_cluster_skeleton_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 18 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 18 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 18 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
