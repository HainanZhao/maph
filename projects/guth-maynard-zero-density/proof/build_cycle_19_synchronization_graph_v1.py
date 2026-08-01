#!/usr/bin/env python3
"""Seal Cycle 19 synchronization-graph reduction and abstract obstruction."""
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
OUTPUT = ROOT / "artifacts/cycle-19-synchronization-graph-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-19-synchronization-graph-preregistration-v1.md", "cdbd9d196f714325c14e6e9aa2ae79d5b41b0d193b1defaa8817935ef7134e4d"),
    "document": (ROOT / "docs/cycle-19-synchronization-graph-v1.md", "395d98a35d49ad868ec0ba7a10aa053d548e21c3d2064addc38ef9bf33478b0d"),
    "conventions": (ROOT / "conventions/synchronization_graph_v1.py", "1f9698b3a1bf62f727ed995e3369546a2eeec9dcecc68dbebd69757cfcec52b7"),
    "tests": (ROOT / "tests/test_cycle_19_synchronization_graph_v1.py", "6e620489cb346fbc6346940b8ab6419ba247de4ebe1fd3734aecda3b03a2f977"),
    "cycle18": (ROOT / "artifacts/cycle-18-coherent-cluster-skeleton-v1.json", "2aab1890a1e68efc58dcc9ad45dc636766760a610de8299a7f52afb605138936"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 19 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("synchronization_graph_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 19 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    critical = rows["critical_exponents"]
    finite = rows["finite_common_component_simplex"]
    require(critical["popular_ordered_pairs"] == Fraction(27, 25), "pair exponent mismatch")
    require(critical["ordered_two_step_paths"] == Fraction(33, 25), "path exponent mismatch")
    require(finite["phase_code_entropy"] == 0, "entropy obstruction mismatch")
    return rows


def validate_cycle18() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle18"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_COHERENT_CLUSTER_COST_SEPARATED_RECURRENCE_SKELETON_OPEN", "Cycle 18 status mismatch")
    require(prior["skeleton_reduction"]["target"] == "It suffices to prove |C|<=X^(21/25+o(1)).", "Cycle 18 target mismatch")
    return {"cycle18_role": "source of the separated skeleton target only"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-19-synchronization-graph-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_SYNCHRONIZATION_GRAPH_ABSTRACT_BOUNDARY_PRIME_LOG_CLOSURE_OPEN",
        "claim_boundary": "This artifact proves abstract synchronization, popular-pair, two-step path, and common-component countermodel statements. It does not prove a prime-log closure lemma, the separated skeleton bound, a density improvement, or an interval result.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_cycle18()},
        "synchronization_graph": {
            "epistemic_status": "PROVED",
            "statement": "Common V-large projections force phase-aligned Gram mass at least R^2V^2/A; if Rw>=2M, at least R^2w/(4M) ordered pairs have aligned real kernel at least w/4.",
            "critical_edge_exponent": "27/25",
            "critical_average_degree_exponent": "6/25",
            "critical_two_step_path_exponent": "33/25",
        },
        "abstract_boundary": {
            "epistemic_status": "PROVED",
            "statement": "A positive-definite common-component simplex has every off-diagonal kernel exactly w for arbitrary R and may have zero block entropy; scalar coherence and separation labels alone cannot bound the skeleton.",
        },
        "prime_log_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Use the actual prime phase curve to forbid the two-step graph, close endpoint differences, or force multiblock structure usable by detector surgery.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_json(rows),
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_19_synchronization_graph_v1.py --write",
            "check_command": "python3 proof/build_cycle_19_synchronization_graph_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_19_synchronization_graph_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 19 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 19 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 19 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
