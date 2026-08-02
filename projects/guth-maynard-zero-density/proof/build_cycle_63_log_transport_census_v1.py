#!/usr/bin/env python3
"""Seal Cycle 63 logarithmic transport census reduction."""
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
OUTPUT = ROOT / "artifacts/cycle-63-log-transport-census-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-63-log-transport-preregistration-v1.md", "65df49241db40aeff0d703b8bf252b32fd6982006ef96a6e902e1e77b0dfbdf9"),
    "document": (ROOT / "docs/cycle-63-log-transport-v1.md", "02e8e988b026f6fcee3b985a6388552fc222c214f461bfcf7602122bcd8feb8b"),
    "conventions": (ROOT / "conventions/log_transport_census_v1.py", "f98ce11b67ae05928ab827c1d06f238789f9bd22e231d024232c3280ea90f2ff"),
    "tests": (ROOT / "tests/test_cycle_63_log_transport_census_v1.py", "5e72ebd15bd86769389b193841b33d72943e6aa18cf572e223e7cce73d44fda6"),
    "cycle48": (ROOT / "artifacts/cycle-48-hs-joint-sieve-v1.json", "2c0522bee7f7d287dbadfc3d6268316a5f87a0c67725379ea399cfa1583d580f"),
    "cycle58": (ROOT / "artifacts/cycle-58-strict-hybrid-margin-correction-v1.json", "0bde0caa82cda62b8a61af9902e6eecc00d89442d41779826bb52a59e6a3dcef"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 63 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("log_transport_census_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 63 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    data = rows["transport"]
    require(data["desired_total_census_open_endpoint"] == Fraction(16, 25), "triple target")
    require(data["desired_pair_census_open_endpoint"] == Fraction(17, 25), "pair target")
    require(data["hessian_determinant_exponent"] == -Fraction(6, 5), "surface determinant")
    return rows


def validate_priors() -> dict[str, str]:
    cycle48 = json.loads(INPUTS["cycle48"][0].read_text(encoding="utf-8"))
    cycle58 = json.loads(INPUTS["cycle58"][0].read_text(encoding="utf-8"))
    require(cycle48.get("status") == "SEALED_AUXILIARY_S4_MARGIN_7_50_LCAM4_BRIDGE_OPEN", "Cycle 48 status mismatch")
    require(cycle58.get("status") == "SEALED_STRICT_GT_3_50_OR_ENDPOINT_MARGIN_REQUIRED", "Cycle 58 status mismatch")
    return {"cycle48_role": "pointwise 7/50 saving", "cycle58_role": "strict powered target above 1/5"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-63-log-transport-census-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_LOG_TRANSPORT_PAIR_CENSUS_LT_17_25_OPEN",
        "claim_boundary": "This artifact proves a two-dimensional transport reduction and exponent targets only. It does not prove the pair/triple census, a powered saving, LCAM, density, or interval gains.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_priors()},
        "transport_reduction": {
            "epistemic_status": "PROVED",
            "statement": "Averaged wrap multiplicity is a triple strip census on a saddle surface; h-differencing removes beta and reduces the desired total exponent <16/25 to a sufficient weighted pair exponent <17/25.",
        },
        "analytic_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Use two-dimensional spacing, determinant, or bilinear-sieve structure to beat the beta-free pair census exponent 17/25 with strict margin, or prove the triple census directly.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_63_log_transport_census_v1.py --write",
            "check_command": "python3 proof/build_cycle_63_log_transport_census_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_63_log_transport_census_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 63 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 63 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 63 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
