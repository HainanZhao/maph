#!/usr/bin/env python3
"""Seal Cycle 79 sublattice-aware double-B-process geometry."""
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
OUTPUT = ROOT / "artifacts/cycle-79-double-b-process-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "discovery_candidate": (ROOT / "discovery/cycle-79-double-b-process-candidate-v1.md", "aac672fb863a94482c94197f4bd55556c4587e45bd0d82039a4445b2fd0e5bbf"),
    "preregistration": (ROOT / "docs/cycle-79-double-b-process-preregistration-v1.md", "77919a944fb8082dbec44a6171a591496b46161ebe54b6602e1ba8f9785b4cac"),
    "document": (ROOT / "docs/cycle-79-double-b-process-v1.md", "626ca3ccb0c5606d291a6ea5a4f1e3f8160ac9242792ae8cae8f0e7904a6fa04"),
    "conventions": (ROOT / "conventions/double_b_process_v1.py", "4c5453c6c7babb19f1fa483a254ab20b1f160b4c68dd091127b94bc0c7cc0fec"),
    "tests": (ROOT / "tests/test_cycle_79_double_b_process_v1.py", "369b310e1a89a33f1aa41c6f50664f39263642c623a077ac906db217e9df2a81"),
    "cycle78": (ROOT / "artifacts/cycle-78-freiman-phase-web-v1.json", "bbff3b63005b7ef468ee23289e9e3f4b7d0f30cfe79374dcb3df0622aec23d5a"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 79 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("double_b_process_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 79 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require("31/25" in rows["fourier_contract"], "raw target")
    require("21/25" in rows["dual_support"], "dual ceiling")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle78"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_EXACT_FREIMAN_WEB_OR_SPARSE_ACSI_OPEN", "Cycle 78 status mismatch")
    return {"cycle78_role": "supply the relation-rich web branch and isolate sparse ACSI"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-79-double-b-process-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_DOUBLE_B_HIGH_FREQUENCY_LOG_SADDLE_OPEN",
        "claim_boundary": "This artifact proves the exact Fourier target, stationary maps, Hessians, support ledger, and trivial low-frequency closure. It proves no uniform stationary remainder, high-frequency dual bound, ACSI, packet closure, powered saving, density gain, or interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "discovery_quarantine": {
            "epistemic_status": "OBSERVED",
            "statement": "The exploratory note proposed the dual map; all promoted signs, determinants, and exponents were independently derived exactly.",
        },
        "double_b_geometry": {
            "epistemic_status": "PROVED",
            "statement": "The dual phase is (hDelta/(2pi))log(kc0/r), with r~k, h~kQ/Delta, amplitude Delta/(2pi r), and nonzero logarithmic-saddle determinant.",
        },
        "low_frequency_closure": {
            "epistemic_status": "PROVED",
            "statement": "All k<Delta/Q contribute at most X^(6/5+o(1)), margin 1/25 to the X^(31/25) raw target.",
        },
        "scale_match": {
            "epistemic_status": "PROVED",
            "statement": "The maximum dual h exponent is 21/25, matching the frozen prime-row skeleton scale.",
        },
        "analytic_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Control stationary remainders and prove cancellation in the high-frequency signed (k,h,r) logarithmic saddle, separating Cycle-78 valuation webs.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_79_double_b_process_v1.py --write",
            "check_command": "python3 proof/build_cycle_79_double_b_process_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_79_double_b_process_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 79 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 79 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 79 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
