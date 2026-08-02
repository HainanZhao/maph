#!/usr/bin/env python3
"""Seal Cycle 61 coefficient-projection inverse formulation."""
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
OUTPUT = ROOT / "artifacts/cycle-61-coefficient-projection-inverse-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-61-coefficient-projection-preregistration-v1.md", "ee4fe79d438bf161ca256aa66a88c17e09c7ba9b44e5d548c50a91824c3b6c99"),
    "document": (ROOT / "docs/cycle-61-coefficient-projection-v1.md", "9b4fe5cd439c6816d1ec4e3e27fd8a38ccad631390880c00b361839fc4f022c4"),
    "conventions": (ROOT / "conventions/coefficient_projection_inverse_v1.py", "8dbe534c6c35fd4226fb9934db08019f284cd40fe643e7689ad17eff32c174e5"),
    "tests": (ROOT / "tests/test_cycle_61_coefficient_projection_inverse_v1.py", "8c66bd6941bf3ca979c1f8f6b21f16fb5eddcc9f3930325ab16e65f3eedcdc61"),
    "cycle39": (ROOT / "artifacts/cycle-39-moment-amplified-prime-monomial-v1.json", "3b83385d1d7e7ed447cafe0f7e42be1badb1bb26ba42cc458cf3fa3b8f204826"),
    "cycle60": (ROOT / "artifacts/cycle-60-coordinate-anova-v1.json", "69f032ddd9d6d22fdca9c55a2078f274baca900a98b281046d694ba77c1c2d8a"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 61 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("coefficient_projection_inverse_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 61 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["s3"]["bessel_operator_bound"] == 12, "s3 Bessel bound")
    require(rows["s4"]["bessel_operator_bound"] == 72, "s4 Bessel bound")
    require(rows["s4"]["hilbert_synthesis"] == "A=C B", "operator factorization")
    return rows


def validate_priors() -> dict[str, str]:
    cycle39 = json.loads(INPUTS["cycle39"][0].read_text(encoding="utf-8"))
    cycle60 = json.loads(INPUTS["cycle60"][0].read_text(encoding="utf-8"))
    require(cycle39.get("status") == "SEALED_MOMENT_AMPLIFIED_PRIME_MONOMIAL_RESTRICTION_OPEN", "Cycle 39 status mismatch")
    require(cycle60.get("status") == "SEALED_ANOVA_COMPONENT_RESTRICTION_OR_FLAT_ENERGY_INVERSE_OPEN", "Cycle 60 status mismatch")
    return {"cycle39_role": "fiber multiplicity", "cycle60_role": "coordinate ANOVA routing"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-61-coefficient-projection-inverse-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_PRIME_COORDINATE_MARGINAL_CAPTURE_OR_ANNIHILATOR_INVERSE_OPEN",
        "claim_boundary": "This artifact proves operator factorization, Bessel bounds, and a scoped inverse condition. It does not exclude annihilators or prove a power saving, AMPR, density, or interval gains.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_priors()},
        "projection_theorem": {
            "epistemic_status": "PROVED",
            "statement": "Hilbert synthesis factors as A=C B with C the full coordinate-centering projection; A*A<=D_s I, and near-saturation forces every prime-coordinate marginal of the lifted Fourier vector small.",
        },
        "analytic_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Prove fixed-power marginal capture for actual edge Fourier vectors or turn simultaneous small marginals into a prime-log annihilator/recurrence/detector-surgery theorem.",
        },
        "exact_replay": rows,
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_61_coefficient_projection_inverse_v1.py --write",
            "check_command": "python3 proof/build_cycle_61_coefficient_projection_inverse_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_61_coefficient_projection_inverse_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 61 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 61 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 61 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
