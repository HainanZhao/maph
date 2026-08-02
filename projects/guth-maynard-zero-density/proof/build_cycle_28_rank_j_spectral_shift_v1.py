#!/usr/bin/env python3
"""Seal Cycle 28 rank-J spectral shift and reconstruction."""
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
OUTPUT = ROOT / "artifacts/cycle-28-rank-j-spectral-shift-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-28-rank-j-spectral-shift-preregistration-v1.md", "c145e8bf7a727b8de721cb8d7d0547893a71859fb5a4957cd0e1c7f482550851"),
    "document": (ROOT / "docs/cycle-28-rank-j-spectral-shift-v1.md", "95ffeb060bbbf4aeb4df35913ef3c8a66cc8e888c7dcc9832fdca53e464ffbe9"),
    "conventions": (ROOT / "conventions/rank_j_spectral_shift_v1.py", "effe89932b669122a4014c363f09f2665bc02b865cef1bb5f1808d1a5ea2552a"),
    "tests": (ROOT / "tests/test_cycle_28_rank_j_spectral_shift_v1.py", "6acaac4faa73911f75f1ee84111f4f12a9f58248cbd24be6d875e719010c5907"),
    "cycle23": (ROOT / "artifacts/cycle-23-residual-spectral-shift-v1.json", "605e7a3eb5ac5b4e342b512e4465762d43b1b919051e4dafd01058e7ae14121b"),
    "cycle26": (ROOT / "artifacts/cycle-26-detector-reconstruction-v1.json", "6082d255ea07383913f30ceb5d9835e5f902245972d208af66b95acd27dcc64e"),
    "cycle27_v1": (ROOT / "artifacts/cycle-27-hadamard-detector-surgery-v1.json", "4a62765a22c0a2ca7a70d5917925859029faad155827a031efee90918c703c53"),
    "cycle27_v2": (ROOT / "artifacts/cycle-27-hadamard-detector-surgery-correction-v2.json", "3010bb6b8f32fad2d10630c8ce9fc15682393ecc54d0567bfa82597582d7c4e5"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 28 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("rank_j_spectral_shift_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 28 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    determinant = rows["determinant_example"]
    require(determinant["H_det"] / determinant["B_det"] == determinant["D_product"] * determinant["det_I_plus_L"], "determinant identity mismatch")
    require(rows["critical_ledger"]["k_rho"] == Fraction(6, 25), "critical scale mismatch")
    require(rows["critical_ledger"]["reconstruction_constant"] == Fraction(1, 64), "reconstruction constant mismatch")
    return rows


def validate_prior() -> dict[str, str]:
    expected = {
        "cycle23": "SEALED_RESIDUAL_SPECTRAL_SHIFT_INVERSE_LEVERAGE_DICHOTOMY_PRIME_GATE_OPEN",
        "cycle26": "SEALED_INVERSE_LEVERAGE_DETECTOR_RECONSTRUCTION_EXACT_DEPENDENCE_OPEN",
        "cycle27_v1": "SEALED_ORTHOGONAL_SIGNED_DETECTOR_OR_MULTIBLOCK_SYNCHRONIZATION",
        "cycle27_v2": "SEALED_PRIME_COUNT_REMAINDER_CORRECTION_V1_THEOREM_UNCHANGED",
    }
    for label, status in expected.items():
        prior = json.loads(INPUTS[label][0].read_text(encoding="utf-8"))
        require(prior.get("status") == status, f"{label} status mismatch")
    return {"prior_role": "rank-one shift/reconstruction upgraded to the corrected Hadamard detector subspace"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-28-rank-j-spectral-shift-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_RANK_J_SHIFT_OR_ADAPTIVE_DETECTOR_RECONSTRUCTION",
        "claim_boundary": "This artifact extends residual shift and reconstruction to an orthonormal detector subspace and verifies the Hadamard exponent ledger. It does not bound multiblock synchronization or exact row dependence, prove the skeleton target, improve zero density, or improve intervals.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "rank_j_identity": {
            "epistemic_status": "PROVED",
            "statement": "det(XX*)/det(B)=product_t(1-rho_t) det(I_J+S*B^(-1)S).",
        },
        "adaptive_reconstruction": {
            "epistemic_status": "PROVED",
            "statement": "Avoiding shift -K/2 reconstructs a top-leverage direction in the detector subspace with error at most sqrt(2)exp(-K/(4J)).",
        },
        "hadamard_ledger": {
            "epistemic_status": "PROVED",
            "statement": "With surgery threshold V/(4J), either shift magnitude is at least k rho/(32J^2) or reconstruction error is at most sqrt(2)exp(-k rho/(64J^3)).",
            "scale_for_subpower_J": "X^(6/25-o(1))",
        },
        "singular_split": {
            "epistemic_status": "PROVED",
            "statement": "Residual singularity gives exact detector-subspace reconstruction or exact scaled-row dependence.",
        },
        "remaining_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Iterate adaptive detector-subspace reconstruction or prove prime arithmetic for multiblock synchronization and exact row dependence.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_json(rows),
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_28_rank_j_spectral_shift_v1.py --write",
            "check_command": "python3 proof/build_cycle_28_rank_j_spectral_shift_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_28_rank_j_spectral_shift_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 28 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 28 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 28 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
