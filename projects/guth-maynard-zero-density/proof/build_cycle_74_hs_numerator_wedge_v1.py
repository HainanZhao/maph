#!/usr/bin/env python3
"""Seal Cycle 74 Huxley--Sargos numerator wedge."""
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
OUTPUT = ROOT / "artifacts/cycle-74-hs-numerator-wedge-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-74-hs-numerator-preregistration-v1.md", "e9cb862efdbd4e9f57ffc8558277340533cb17313ae1807279456dc0794dbdc1"),
    "document": (ROOT / "docs/cycle-74-hs-numerator-v1.md", "0def9a7ba3435000b5639c31650a951fb55708dd36bc9850f3467df5013a1c41"),
    "conventions": (ROOT / "conventions/hs_numerator_wedge_v1.py", "b4dfe2db110c0a79dc067ce3202e066b561328f07353dcfec429e46041708d64"),
    "tests": (ROOT / "tests/test_cycle_74_hs_numerator_wedge_v1.py", "8d8deeb86da4e33764656bc73dd15250f52dbdab40857b3a9d4b4bd2c22d91a9"),
    "cycle73": (ROOT / "artifacts/cycle-73-numerator-resolved-atlas-v1.json", "fdad9eae285d61f8782b8e6e18809d559fee87ffcf2fddeca53a002b807b6685"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 74 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("hs_numerator_wedge_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 74 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["summed_bound"] == "theta+w", "summed bound")
    require(rows["transition"] == "theta=1/5", "transition")
    return rows


def validate_priors() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle73"][0].read_text(encoding="utf-8"))
    source = json.loads(INPUTS["cycle47_source_ledger"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_NUMERATOR_WEDGE_CLOSED_RESIDUAL_CURVATURE_OPEN", "Cycle 73 status mismatch")
    require(source.get("epistemic_status") == "PROVED", "Cycle 47 source ledger status mismatch")
    return {
        "cycle73_role": "supply the numerator-resolved atlas and raw fraction budget",
        "cycle47_role": "supply the checked order-three near-integer theorem and primary-source chain",
    }


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-74-hs-numerator-wedge-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_HS_NUMERATOR_WEDGE_CLOSED_Q_AVERAGE_RESIDUAL_OPEN",
        "claim_boundary": "This artifact closes only a strict band of numerator-resolved cells by a fixed-denominator order-three estimate. The q-average residual, powered saving, density gain, and interval gain remain open.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_priors()},
        "fixed_denominator_bound": {
            "epistemic_status": "PROVED",
            "statement": "w(theta,alpha)=min(alpha,max(0,alpha+1/10-theta/2)); summing q gives exponent theta+w.",
        },
        "new_wedge": {
            "epistemic_status": "PROVED",
            "statement": "For theta>1/5, the lower piece closes when theta+kappa<6/25 and the upper piece closes when alpha+theta/2+kappa<7/50.",
            "witness": "(theta,kappa,alpha)=(11/50,0,1/50) improves a raw tie at 6/25 to 23/100.",
        },
        "analytic_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Exploit cancellation across q, preferably through the nonzero two-variable curvature or the shifted Dirichlet-correlation form, on the remaining cells.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_74_hs_numerator_wedge_v1.py --write",
            "check_command": "python3 proof/build_cycle_74_hs_numerator_wedge_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_74_hs_numerator_wedge_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 74 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 74 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 74 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
