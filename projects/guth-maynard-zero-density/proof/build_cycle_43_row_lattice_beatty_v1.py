#!/usr/bin/env python3
"""Seal Cycle 43 row-lattice resonance and curved Beatty-strip reduction."""
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
OUTPUT = ROOT / "artifacts/cycle-43-row-lattice-beatty-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-43-row-lattice-beatty-preregistration-v1.md", "43d52637fe8fb4436e9b942f88f85402c8c2b5aaf65112c4a4f17e9908659b17"),
    "document": (ROOT / "docs/cycle-43-row-lattice-beatty-v1.md", "33edc59324b365a8a730f4634858d44f77a2ba80cdcbc41643330ef2c8cd0b4f"),
    "conventions": (ROOT / "conventions/row_lattice_beatty_v1.py", "6b70274cbdc244784f2eae9923dd7ca86351c63ec758ccfd88fcf64dd252744a"),
    "tests": (ROOT / "tests/test_cycle_43_row_lattice_beatty_v1.py", "153668efc28c2ff1bf10eb2507a784f880785b30904d977066c41415b2f350d0"),
    "cycle42": (ROOT / "artifacts/cycle-42-localized-comb-v1.json", "c109b790a235080fc0b6130a78e4f647fc54951217fe37c7f84e0b8b94090369"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 43 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("row_lattice_beatty_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 43 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["target"]["integer_shift_window"] == Fraction(-11, 25), "target shift window")
    require(rows["target"]["linearization_error"] == Fraction(-1, 5), "linearization error")
    return rows


def validate_prior() -> dict[str, str]:
    prior = json.loads(INPUTS["cycle42"][0].read_text(encoding="utf-8"))
    require(prior.get("status") == "SEALED_LOCALIZED_COMB_DIAGONAL_SHARP_ROW_RESONANCE_OPEN", "Cycle 42 status mismatch")
    return {"prior_role": "stress-test the row Fourier factor on the sharp arithmetic-progression resonance model"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-43-row-lattice-beatty-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_AP_ROW_RESONANCE_CURVED_BEATTY_PRIME_PAIR_OPEN",
        "claim_boundary": "This artifact proves the AP-row resonance formula and its curved Beatty-strip translation. It does not reduce arbitrary rows to APs, prove the prime-pair estimate, close LCAM_s, or improve density or intervals.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_prior()},
        "stress_reduction": {
            "epistemic_status": "PROVED",
            "statement": "At target row exponent 21/25, full AP-row resonance for log((p+r)/p) confines r to a curved Beatty strip of width X^(-11/25).",
        },
        "linearization_boundary": {
            "epistemic_status": "PROVED",
            "statement": "For fixed small k the shift scale is X^(2/5), but the first-order center has error X^(-1/5), larger than the admissible X^(-11/25) strip width.",
        },
        "analytic_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "Control weighted curved Beatty prime pairs on lattice-like rows, or prove nonlattice row Fourier decay on enough prime-monomial ratios.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_43_row_lattice_beatty_v1.py --write",
            "check_command": "python3 proof/build_cycle_43_row_lattice_beatty_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_43_row_lattice_beatty_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 43 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 43 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 43 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
