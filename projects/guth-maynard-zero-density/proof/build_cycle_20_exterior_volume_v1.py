#!/usr/bin/env python3
"""Seal Cycle 20 exterior-volume collapse and prime determinant target."""
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
OUTPUT = ROOT / "artifacts/cycle-20-exterior-volume-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-20-exterior-volume-preregistration-v1.md", "21845cb6e2c0eb7e3ebd29f8ef2fcc8582c55156bf96c17b8fe876d57ee1341e"),
    "document": (ROOT / "docs/cycle-20-exterior-volume-v1.md", "688b96ce3f5c161ce4b9ea48046ce3776a41985f9547575ea2a7b4ea14235963"),
    "conventions": (ROOT / "conventions/exterior_volume_v1.py", "1c6e653bcc8b7c13bc13b7a2485bfef89693fd92566518820701f990d802ab1f"),
    "tests": (ROOT / "tests/test_cycle_20_exterior_volume_v1.py", "b4f435e1431fcc050a38ee54b577722deab18f0adb59bc873bfd141ce4c1e1ae"),
    "cycle19": (ROOT / "artifacts/cycle-19-synchronization-graph-v1.json", "3c68ee97a31f7a7cb2612769f58c2645b4a58332aeceaa856d7082de635aeb63"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 20 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("exterior_volume_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 20 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    critical = rows["critical_exponents"]
    finite = rows["sharp_finite_model"]
    require(critical["k_rho"] == Fraction(6, 25), "collapse exponent mismatch")
    require(finite["normalized_determinant"] == finite["collapse_formula"], "sharpness mismatch")
    require(finite["minimum_witness_norm_squared"] == finite["A"], "witness mismatch")
    return rows


def validate_cycle19() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle19"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_SYNCHRONIZATION_GRAPH_ABSTRACT_BOUNDARY_PRIME_LOG_CLOSURE_OPEN", "Cycle 19 status mismatch")
    require(prior["synchronization_graph"]["critical_average_degree_exponent"] == "6/25", "Cycle 19 exponent mismatch")
    return {"cycle19_role": "common-projection synchronization input and abstract-coherence boundary"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-20-exterior-volume-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_SHARP_EXTERIOR_VOLUME_COLLAPSE_PRIME_DETERMINANT_LOWER_BOUND_OPEN",
        "claim_boundary": "This artifact proves a sharp abstract determinant upper bound forced by common large projections and its critical exponent translation. It does not prove a determinant lower bound for prime-phase rows, the skeleton target, a density improvement, or an interval result.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_cycle19()},
        "exterior_volume": {
            "epistemic_status": "PROVED",
            "statement": "If k equal-norm rows share a V-large coefficient vector and kw>=M, det(G)/M^k <= k rho [k(1-rho)/(k-1)]^(k-1).",
            "sharp_in_abstract_hilbert_architecture": True,
            "critical_log_collapse_scale": "-X^(6/25+o(1))",
        },
        "prime_determinant_gate": {
            "epistemic_status": "CONJECTURED",
            "sufficient_statement": "Uniformly lower-bound det(G_C/M) by exp(-X^(theta+o(1))) for some theta<6/25 on every target-sized X^(3/5)-separated prime-phase row set.",
            "equivalent_search_form": "Use Cauchy--Binet to lower-bound one generalized Vandermonde minor or the collective squared-minor sum.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_json(rows),
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_20_exterior_volume_v1.py --write",
            "check_command": "python3 proof/build_cycle_20_exterior_volume_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_20_exterior_volume_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 20 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 20 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 20 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
