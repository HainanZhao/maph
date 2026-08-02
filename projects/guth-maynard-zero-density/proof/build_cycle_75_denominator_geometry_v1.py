#!/usr/bin/env python3
"""Seal Cycle 75 affine-normalized denominator geometry."""
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
OUTPUT = ROOT / "artifacts/cycle-75-denominator-geometry-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "discovery_candidate": (ROOT / "discovery/cycle-75-denominator-geometry-candidate-v1.md", "0acda47404f42fbcf1a869bd168b00f4ae06be658876820c05ba186b5da6bf18"),
    "preregistration": (ROOT / "docs/cycle-75-denominator-geometry-preregistration-v1.md", "5374a5a7f0dd55f7296364112bff41754100fd9d152bc62c8c5f63d2f0815092"),
    "document": (ROOT / "docs/cycle-75-denominator-geometry-v1.md", "07f5969def52304aa71221b3526f0a39d514d9e2ca07f5f0d9c2252b65c74fb9"),
    "conventions": (ROOT / "conventions/denominator_geometry_v1.py", "9afea41088ad40544be198b48aaa9780009e2bf0aff19842ff84ccdebc7cbbc9"),
    "tests": (ROOT / "tests/test_cycle_75_denominator_geometry_v1.py", "ce0cdc04c4e4cd39b24319ab003e631cd7cfaf242a746a7fe8578923fe66bc2b"),
    "cycle70": (ROOT / "artifacts/cycle-70-unfurled-stationary-curvature-v1.json", "2218be784434352a97037a865a40acd43969562f3430df22944b23adbbde6acc"),
    "cycle74": (ROOT / "artifacts/cycle-74-hs-numerator-wedge-v1.json", "57869f9a6506076198b54bb877417eecaf96682ff8ada606ab8d39ab4cc9e1ae"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 75 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("denominator_geometry_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 75 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["banked_bound"] == "B=min(lambda,theta+w)", "banked bound")
    require("7/15" in rows["worst_required_saving"], "worst saving")
    return rows


def validate_priors() -> dict[str, str]:
    cycle70 = json.loads(INPUTS["cycle70"][0].read_text(encoding="utf-8"))
    cycle74 = json.loads(INPUTS["cycle74"][0].read_text(encoding="utf-8"))
    require(cycle70.get("status") == "SEALED_FACTORED_R_QPRIME_CURVATURE_WITH_ENDPOINT_LOSS_OPEN", "Cycle 70 status mismatch")
    require(cycle74.get("status") == "SEALED_HS_NUMERATOR_WEDGE_CLOSED_Q_AVERAGE_RESIDUAL_OPEN", "Cycle 74 status mismatch")
    return {
        "cycle70_role": "supply curve-index injectivity and the unfurled curvature identity",
        "cycle74_role": "supply the fixed-denominator Huxley--Sargos count",
    }


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-75-denominator-geometry-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_AFFINE_CURVATURE_CONTRACT_E14_E15_ANALYTIC_GAIN_OPEN",
        "claim_boundary": "This artifact proves the exact affine geometry, primitive-ray reduction, combined residual atlas, and additional-saving contract. It proves no denominator-average estimate, seed extraction, powered saving, density gain, or interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_priors()},
        "discovery_quarantine": {
            "epistemic_status": "OBSERVED",
            "statement": "The exploratory candidate selected identities for independent exact derivation; it is not used as proof.",
        },
        "affine_geometry": {
            "epistemic_status": "PROVED",
            "statement": "Both singular values of the unit-box Hessian are comparable to Delta*A/Q=X^(lambda+o(1)); relative tube width is X^(-1-alpha-kappa+o(1)).",
        },
        "primitive_shifted_form": {
            "epistemic_status": "PROVED",
            "statement": "gcd(a,q)=gcd(a+q,q), primitive pairs have unique exact rays, and e(kY)=((a+q)/q)^(i*k*Delta).",
        },
        "combined_atlas": {
            "epistemic_status": "PROVED",
            "statement": "The banked exponent is B=min(lambda,theta+w), the live residual is B+kappa>=6/25, and the maximal deficit is 7/15 at the unique point (1/3,1/3,8/75).",
        },
        "analytic_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Prove an affine-normalized E14 or shifted-strip E15 saving on the combined residual, routing structured failures to E16.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_75_denominator_geometry_v1.py --write",
            "check_command": "python3 proof/build_cycle_75_denominator_geometry_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_75_denominator_geometry_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 75 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 75 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 75 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
