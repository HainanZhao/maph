#!/usr/bin/env python3
"""Seal Cycle 16 separable tensor gate."""
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
OUTPUT = ROOT / "artifacts/cycle-16-separable-tensor-gate-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-16-separable-tensor-gate-preregistration-v1.md", "6668d76d52affefa5dc4685c398d76292e0ca375450b93ee3c670302946778c6"),
    "document": (ROOT / "docs/cycle-16-separable-tensor-gate-v1.md", "0e5e42af55cfd3e6c866a54e32e0d14304d2816a733f1b26ad0e14e2d1bb94b4"),
    "conventions": (ROOT / "conventions/separable_tensor_gate_v1.py", "3065f011b116df1c5b95fc2e48c856cc7adbd1be56ee5d84eaef1fbc1dae09cf"),
    "tests": (ROOT / "tests/test_cycle_16_separable_tensor_gate_v1.py", "0ef7f7ea8530ef66b8d6ef509d80cf9438239033eb702c4803f76b3773bcb7ab"),
    "cycle15_artifact": (ROOT / "artifacts/cycle-15-prime-phase-transition-rank-one-v1.json", "49a5a573b00f3d56e75b7537dee36792751b877b63bef8d5bfee667fb42b51d1"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_json(value: Any) -> Any:
    if isinstance(value, Fraction):
        return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    if isinstance(value, list):
        return [exact_json(item) for item in value]
    if isinstance(value, dict):
        return {str(key): exact_json(item) for key, item in value.items()}
    return value


def check_runtime() -> dict[str, Any]:
    runtime = {"implementation": platform.python_implementation(), "python": platform.python_version(), "optimization_level": sys.flags.optimize}
    require(runtime == EXPECTED_RUNTIME, "Cycle 16 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("separable_tensor_gate_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 16 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["exponents"]["required_sep"] == Fraction(56, 25), "separable exponent mismatch")
    require(all(row["lambda_max"] == row["separable_witness"] for row in rows["identical_row_countermodels"]), "countermodel mismatch")
    return rows


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-16-separable-tensor-gate-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_SEPARABLE_TENSOR_GATE_PRIME_ARITHMETIC_OVERLAP_OPEN",
        "claim_boundary": "This artifact proves exact tensor, separable-norm, and spectral-overlap reductions plus an abstract sharp countermodel. It does not bound the actual prime-phase operator, prove a rank-one semiprime saving, select a prime detector component, improve density, or improve prime intervals.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "tensor_identity": {
            "epistemic_status": "PROVED",
            "statement": "For S with rows u_t tensor u_t, S(a tensor a)=(Ua)^2 and <a tensor a,S*S(a tensor a)>=sum_t |(Ua)_t|^4.",
            "row_gram": "SS*=(UU*) circle (UU*) with complex-square entries.",
        },
        "separable_gate": {
            "epistemic_status": "PROVED",
            "definition": "Sep(H_2) is the Rayleigh supremum over a tensor a.",
            "large_value_bound": "|W|V^4<=Sep(H_2)||a||_2^4.",
            "target_exponent_in_X": "56/25",
            "generic_exponent_in_X": "12/5",
            "required_saving_in_X": "4/25",
        },
        "overlap_certificate": {
            "epistemic_status": "PROVED",
            "statement": "If a unit rank-one tensor has Rayleigh quotient A>L, its squared overlap with the spectrum above L is at least (A-L)/(lambda_max-L).",
            "scope": "Exact exhaustiveness only inside the separable tensor architecture.",
        },
        "abstract_countermodel": {
            "epistemic_status": "PROVED",
            "statement": "Identical sampling rows satisfy Sep(H_2)=lambda_max(H_2)=R||u||_2^4; rank-one coefficients alone force no saving.",
        },
        "prime_arithmetic_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "For separated prime-phase rows, prove either high-spectrum loss or fixed-power distance of high eigentensors from the Veronese cone.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_json(rows),
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_16_separable_tensor_gate_v1.py --write",
            "check_command": "python3 proof/build_cycle_16_separable_tensor_gate_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_16_separable_tensor_gate_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 16 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 16 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 16 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
