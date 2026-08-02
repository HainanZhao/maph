#!/usr/bin/env python3
"""Seal Cycle 76 Huxley--Sargos denominator wedge."""
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
OUTPUT = ROOT / "artifacts/cycle-76-hs-denominator-wedge-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-76-hs-denominator-preregistration-v1.md", "8f17a6ef0bee1ede978978ba20b0e23008a0cec5085f55e23d1d7b16f1123f94"),
    "document": (ROOT / "docs/cycle-76-hs-denominator-v1.md", "8707a4635840ded15f30cbd659c4b8ec04efc449080578d7596b41bb17a449b7"),
    "conventions": (ROOT / "conventions/hs_denominator_wedge_v1.py", "b852de34d92d4af9afa864aaec3a82d800f603ad6eca670201a090de43750213"),
    "tests": (ROOT / "tests/test_cycle_76_hs_denominator_wedge_v1.py", "3b70f07594a245717c1727f03b15acc63db330e0699afea2ff74c2f581b48bd4"),
    "discovery_search": (ROOT / "discovery/search_cycle_76_hs_denominator_v1.py", "bec136c37b6dda43371a6b48f8b3f8906d9ee3940211f348fd26e8244cb42b78"),
    "cycle75": (ROOT / "artifacts/cycle-75-denominator-geometry-v1.json", "3dbe955aaea7dffece0b06e1e30fd9d46a7023d1d3ce438991a1dbd57c4576dd"),
    "cycle47_source_ledger": (ROOT / "artifacts/cycle-47-near-curve-gap-v1.json", "209dd38186cefbfad2f286b1fbc6400745425fb6fc8555bd8e06ac5547174a55"),
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
    runtime = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
    }
    require(runtime == EXPECTED_RUNTIME, "Cycle 76 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("hs_denominator_wedge_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 76 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["summed_bound"] == "alpha+u", "summed bound")
    require("9/50" in rows["new_witness"], "new witness")
    return rows


def validate_priors() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle75"][0].read_text(encoding="utf-8"))
    source = json.loads(INPUTS["cycle47_source_ledger"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_AFFINE_CURVATURE_CONTRACT_E14_E15_ANALYTIC_GAIN_OPEN", "Cycle 75 status mismatch")
    require(source.get("epistemic_status") == "PROVED", "Cycle 47 source ledger status mismatch")
    return {
        "cycle75_role": "supply the combined residual and affine denominator geometry",
        "cycle47_role": "supply the checked order-three near-integer theorem and source chain",
    }


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-76-hs-denominator-wedge-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_DENOMINATOR_HS_WEDGE_CLOSED_TWOD_OR_SHIFTED_RESIDUAL_OPEN",
        "claim_boundary": "This artifact closes only a strict denominator-curvature band of the Cycle-75 residual. The full two-dimensional/shifted residual, seed extraction, powered saving, density gain, and interval gain remain open.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_priors()},
        "discovery_quarantine": {
            "epistemic_status": "OBSERVED",
            "statement": "The bounded rational-grid search located a witness only; the promoted wedge follows from the exact symbolic inequalities.",
        },
        "denominator_bound": {
            "epistemic_status": "PROVED",
            "statement": "For fixed numerator, u=min(theta,1/10+alpha/6+theta/3); summing numerators gives alpha+u.",
        },
        "new_wedge": {
            "epistemic_status": "PROVED",
            "statement": "On theta>3/20 and alpha<4theta-3/5, strict closure holds when 7alpha/6+theta/3+kappa<7/50.",
            "witness": "(theta,kappa,alpha)=(6/25,0,0) improves a Cycle-75 tie at 6/25 to 9/50, margin 3/50.",
        },
        "analytic_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Use genuinely two-dimensional E14 or shifted multiplicative E15 structure on the twice-compressed residual, including the unchanged worst point.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_76_hs_denominator_wedge_v1.py --write",
            "check_command": "python3 proof/build_cycle_76_hs_denominator_wedge_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_76_hs_denominator_wedge_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 76 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 76 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 76 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
