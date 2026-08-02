#!/usr/bin/env python3
"""Seal Cycle 99 critical rational-ray compiler."""
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
OUTPUT = ROOT / "artifacts/cycle-99-critical-rational-ray-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "discovery_candidate": (ROOT / "discovery/cycle-99-critical-ray-candidate-v1.md", "29cbbf8ca2b81f4b324ad7f77729b966660a00692b4c00d9033cb86692895b59"),
    "preregistration": (ROOT / "docs/cycle-99-critical-ray-preregistration-v1.md", "f9007b616fe4d14fb65842d01209a3a8965227a11df0f2389c0bf68fa2fc395a"),
    "document": (ROOT / "docs/cycle-99-critical-rational-ray-v1.md", "3b961dfcabae0ae4164b3f9de5fb5fef84b837088d9d2a2e1c6152b69b114f24"),
    "conventions": (ROOT / "conventions/critical_rational_ray_v1.py", "5b0b52da864c3d508b0d50bc269d8d66d357afe03f7fe75253e8bd0be6d77693"),
    "tests": (ROOT / "tests/test_cycle_99_critical_rational_ray_v1.py", "6d4450385d00f2cb86cfa065e43231b296d8717d9898278b17705bcb79961369"),
    "cycle97": (ROOT / "artifacts/cycle-97-projective-algebraic-root-v1.json", "5af4394e8a8f48b70cff4f1b32e9a213640df499f273f701bc0ffe5ffd0d2644"),
    "cycle98": (ROOT / "artifacts/cycle-98-gaudron-direct-ledger-v1.json", "9ac5bba45e11798b592b94250ee52d3b89d632125f116754188580ff8f55c160"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 99 runtime mismatch")
    return runtime


def frozen_inputs() -> dict[str, dict[str, str]]:
    result = {}
    for label, (path, expected) in INPUTS.items():
        require(path.is_file(), f"missing frozen input: {label}")
        actual = sha256(path)
        require(actual == expected, f"frozen input hash mismatch: {label}")
        result[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual}
    return result


def load_theorem() -> dict[str, object]:
    path = INPUTS["conventions"][0]
    spec = importlib.util.spec_from_file_location("critical_rational_ray_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 99 conventions")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    record = module.theorem_record()
    require("H=Q*M" in record["height"], "height contract")
    require("1/(2*H^2)" in record["fixed_w_uniqueness"], "Farey threshold")
    require("orientation retained" in record["fiber"], "fiber orientation")
    require("no bound" in record["boundary"], "claim boundary")
    return record


def validate_priors() -> dict[str, str]:
    cycle97 = json.loads(INPUTS["cycle97"][0].read_text(encoding="utf-8"))
    cycle98 = json.loads(INPUTS["cycle98"][0].read_text(encoding="utf-8"))
    require("NEAR_DOUBLE" in cycle97.get("status", ""), "Cycle 97 status mismatch")
    require("POINTWISE_TRANSCENDENCE_TOO_WEAK" in cycle98.get("status", ""), "Cycle 98 status mismatch")
    return {
        "cycle97_role": "supply the critical point and distance rho<=2eta/ell",
        "cycle98_role": "force a sparse/averaged/critical alternative to generic pointwise bounds",
    }


def seal() -> dict[str, Any]:
    theorem = load_theorem()
    return {
        "artifact_id": "cycle-99-critical-rational-ray-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_STRONG_NEAR_DOUBLE_CRITICAL_RAYS_WEAK_AND_FIBER_OPEN",
        "claim_boundary": (
            "This artifact compiles strongly localized near-double rows into unique injective "
            "critical rational rays. It proves no fiber bound, weak-row estimate, complete alias "
            "moment, density gain, or interval gain."
        ),
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_priors()},
        "critical_ray_theorem": {"epistemic_status": "PROVED", **theorem},
        "inverse_output": {
            "epistemic_status": "PROVED",
            "statement": (
                "At the registered strong threshold, labels (w,N,R) are unique and injective; "
                "all multiplicity lies in C|b|R=B|a|N with orientation retained."
            ),
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Bound the factorization fiber with signed/Mobius weights and treat weak near-double rows.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_99_critical_rational_ray_v1.py --write",
            "check_command": "python3 proof/build_cycle_99_critical_rational_ray_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_99_critical_rational_ray_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 99 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 99 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 99 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
