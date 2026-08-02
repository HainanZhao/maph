#!/usr/bin/env python3
"""Seal Cycle 34 stable-anchor prime-kernel reduction."""
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
OUTPUT = ROOT / "artifacts/cycle-34-stable-anchor-kernel-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-34-stable-anchor-kernel-preregistration-v1.md", "1e3731212d268df0ea940b106f9c18df35490a8590605f2153a3c88effa7332a"),
    "document": (ROOT / "docs/cycle-34-stable-anchor-kernel-v1.md", "8a610ae65c25ac45a571cf7615586a4898cbd789dd5fe988a3308153ce2621ed"),
    "conventions": (ROOT / "conventions/stable_anchor_kernel_v1.py", "38749985ba07a728afc9b4c4de8155b45adb4d6ed6c5735f00f9c8ebc541b4a6"),
    "tests": (ROOT / "tests/test_cycle_34_stable_anchor_kernel_v1.py", "2c2e15ddf4f8170d566881cbcbae8d617e0c0560e3b8d22ec2f60b5ee15cf6ca"),
    "cycle18": (ROOT / "artifacts/cycle-18-coherent-cluster-skeleton-v1.json", "2aab1890a1e68efc58dcc9ad45dc636766760a610de8299a7f52afb605138936"),
    "cycle26": (ROOT / "artifacts/cycle-26-detector-reconstruction-v1.json", "6082d255ea07383913f30ceb5d9835e5f902245972d208af66b95acd27dcc64e"),
    "cycle33_v2": (ROOT / "artifacts/cycle-33-anchor-aware-scope-correction-v2.json", "dbe25f01bdf8a49aa4f6cace91dcce773a8c76ebc2f9a3879ca185028274ef75"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 34 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("stable_anchor_kernel_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 34 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["one_anchor"]["kernel_lower"] >= rows["one_anchor"]["coarse_lower"], "one-anchor bound mismatch")
    require(rows["multi_anchor"]["l1_norm"] == 1, "multi-anchor stability mismatch")
    require(rows["exponents"]["unnormalized_kernel"] == Fraction(7, 10), "kernel exponent mismatch")
    require(rows["exponents"]["missing_saving"] == Fraction(4, 25), "saving mismatch")
    return rows


def validate_prior() -> dict[str, str]:
    expected = {
        "cycle18": "SEALED_COHERENT_CLUSTER_COST_SEPARATED_RECURRENCE_SKELETON_OPEN",
        "cycle26": "SEALED_INVERSE_LEVERAGE_DETECTOR_RECONSTRUCTION_EXACT_DEPENDENCE_OPEN",
        "cycle33_v2": "SEALED_ANCHOR_RECURRENCE_EVALUATION_STABILITY_CORRECTION",
    }
    for label, status in expected.items():
        prior = json.loads(INPUTS[label][0].read_text(encoding="utf-8"))
        require(prior.get("status") == status, f"{label} status mismatch")
    return {"prior_role": "valid original-detector anchor branch reduced to an unweighted prime-kernel skeleton"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-34-stable-anchor-kernel-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_STABLE_ANCHOR_TO_UNWEIGHTED_PRIME_KERNEL_REDUCTION",
        "claim_boundary": "This artifact reduces stable anchor reconstruction of the original detector to an unweighted prime-kernel large-values theorem. It does not prove that theorem, handle unstable/transverse reconstruction, close the skeleton target, improve zero density, or improve intervals.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "one_anchor": {
            "epistemic_status": "PROVED",
            "statement": "If b is o(sqrt(rho))-close to one anchor row, every translated skeleton row has unweighted prime-kernel value at least X^(7/10-o(1)).",
        },
        "stable_multi_anchor": {
            "epistemic_status": "PROVED",
            "statement": "X^o(1) anchors with X^o(1) l1 coefficient norm reduce by coloring to one anchor without fixed-power loss.",
        },
        "remaining_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Bound X^(3/5)-separated h with |K(h)|>=X^(7/10-o(1)) by X^(21/25+o(1)); the generic skeleton exponent is 1 and the missing saving is 4/25.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_json(rows),
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_34_stable_anchor_kernel_v1.py --write",
            "check_command": "python3 proof/build_cycle_34_stable_anchor_kernel_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_34_stable_anchor_kernel_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 34 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 34 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 34 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
