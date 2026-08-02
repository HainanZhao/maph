#!/usr/bin/env python3
"""Seal Cycle 98 direct Gaudron exponent ledger."""
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
OUTPUT = ROOT / "artifacts/cycle-98-gaudron-direct-ledger-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "discovery_candidate": (ROOT / "discovery/cycle-98-linear-form-ledger-candidate-v1.md", "7cd569fedf1640c38b785b9ec5f251624345c6f4c967ff52a47026591c294419"),
    "source_ledger": (ROOT / "docs/cycle-98-gaudron-source-v1.md", "2fc5ff268d74bcc2e57736ec02bec696ceaada1a3ccd15dcbf084223b243fd47"),
    "preregistration": (ROOT / "docs/cycle-98-linear-form-ledger-preregistration-v1.md", "09b8e2b64768e1572c41f75517fcc05e4a922bc5d176026024e9e1d718ca8d5e"),
    "document": (ROOT / "docs/cycle-98-gaudron-direct-ledger-v1.md", "b24e38304b4271e47a17fcad682cc5d58fff8055bd3bba58beca8c12caef39df"),
    "conventions": (ROOT / "conventions/gaudron_direct_ledger_v1.py", "ffb186bb2cfb23f97bef9a6d227b4a84a2b82330680186343c236b5b880ef3d4"),
    "tests": (ROOT / "tests/test_cycle_98_gaudron_direct_ledger_v1.py", "acb73229cb08c2180a82231ad47b223dc68ae53e91a6fef769f95deb00afccac"),
    "cycle97": (ROOT / "artifacts/cycle-97-projective-algebraic-root-v1.json", "5af4394e8a8f48b70cff4f1b32e9a213640df499f273f701bc0ffe5ffd0d2644"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 98 runtime mismatch")
    return runtime


def frozen_inputs() -> dict[str, dict[str, str]]:
    result = {}
    for label, (path, expected) in INPUTS.items():
        require(path.is_file(), f"missing frozen input: {label}")
        actual = sha256(path)
        require(actual == expected, f"frozen input hash mismatch: {label}")
        result[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual}
    return result


def load_ledgers() -> dict[str, object]:
    path = INPUTS["conventions"][0]
    spec = importlib.util.spec_from_file_location("gaudron_direct_ledger_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 98 conventions")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    cost = module.cost_ledger()
    support = module.support_ledger()
    require(cost["negative_log_exponent"] == "12/5", "cost exponent mismatch")
    require("TOO_WEAK" in cost["comparison"], "comparison mismatch")
    require("<=4M" in support["field_degree"], "field-degree ledger mismatch")
    return {"cost": cost, "support": support}


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle97"][0].read_text(encoding="utf-8"))
    require(
        prior.get("status")
        == "SEALED_ALGEBRAIC_ROOT_OR_NEAR_DOUBLE_INVERSE_EFFECTIVE_SEPARATION_OPEN",
        "Cycle 97 status mismatch",
    )
    return {"cycle97_role": "supply algebraic roots, degree/height envelope, and linear-form target"}


def seal() -> dict[str, Any]:
    ledgers = load_ledgers()
    return {
        "artifact_id": "cycle-98-gaudron-direct-ledger-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_DIRECT_POINTWISE_TRANSCENDENCE_TOO_WEAK_SPARSE_AVERAGED_CRITICAL_OPEN",
        "claim_boundary": (
            "This artifact proves only that direct worst-case insertion into Gaudron Theorem 1.1 "
            "gives exp(-X^(12/5+o(1))), too weak for a power separation. It proves no saturation "
            "for sparse, averaged, low-degree, or critical-point methods and no moment, density, "
            "or interval theorem."
        ),
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "source_input": {
            "epistemic_status": "PROVED",
            "statement": "Gaudron arXiv:1004.3652, Theorem 1.1, specialized with n=2,t=1 and k=Q(i,alpha).",
        },
        "direct_insertion": {"epistemic_status": "PROVED", **ledgers},
        "structural_no_go": {
            "epistemic_status": "PROVED",
            "scope": "direct generic-degree pointwise use of Gaudron Theorem 1.1 only",
            "implication": "retain sparse trinomial structure, average modes, or count critical relations",
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Build an averaged sparse-trinomial/critical-point counting theorem on actual support.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_98_gaudron_direct_ledger_v1.py --write",
            "check_command": "python3 proof/build_cycle_98_gaudron_direct_ledger_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_98_gaudron_direct_ledger_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 98 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 98 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 98 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
