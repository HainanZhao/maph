#!/usr/bin/env python3
"""Seal Cycle 87 signed second-moment Mellin-alias atlas."""
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
OUTPUT = ROOT / "artifacts/cycle-87-mellin-alias-atlas-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "discovery_candidate": (ROOT / "discovery/cycle-87-mellin-alias-candidate-v1.md", "2880bf28dc4c2ece82afe991c29f204a3e2cc906f37a5c80fc36318ffa58135d"),
    "preregistration": (ROOT / "docs/cycle-87-mellin-alias-preregistration-v1.md", "44afc90487f23068722f499fa64f136204c21530d3a6b55620878372ace6acf0"),
    "document": (ROOT / "docs/cycle-87-mellin-alias-atlas-v1.md", "99bd3e0c9e72b9eb91df2ea9f40e5e1d9ec1a9ee96b45b3375deaba95811975a"),
    "conventions": (ROOT / "conventions/mellin_alias_atlas_v1.py", "4aea18e04382939105bd35cdab455e8f87720574ec4add520df02638c3f96934"),
    "tests": (ROOT / "tests/test_cycle_87_mellin_alias_atlas_v1.py", "6ccaef27642fe86a9512f18948c317b9e57ca33f52facb6a411561628ce60d23"),
    "cycle81": (ROOT / "artifacts/cycle-81-exact-q-transform-v1.json", "0753d455a2e9428b28f1b9dac59b04fd57008db562370202a300a38a818631a4"),
    "cycle86": (ROOT / "artifacts/cycle-86-signed-regime-split-v1.json", "4d6f78f433b052c6d3497d46d67b015d6963fe67f862e0d6c52124c6d26a3dd4"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 87 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("mellin_alias_atlas_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 87 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["atom_diagonal_exponent"] == "xi+14/15", "atom diagonal")
    require("1<<|m|<<Q" in rows["stationary_alias_branch"], "alias support")
    require("sqrt(K/|m|)" in rows["amplitude"], "stationary amplitude")
    return rows


def validate_priors() -> dict[str, str]:
    cycle81 = json.loads(INPUTS["cycle81"][0].read_text(encoding="utf-8"))
    cycle86 = json.loads(INPUTS["cycle86"][0].read_text(encoding="utf-8"))
    require(cycle81.get("status") == "SEALED_EXACT_Q_TRANSFORM_LOG_RESONANCE_PROJECTOR_OPEN", "Cycle 81 status mismatch")
    require(cycle86.get("status") == "SEALED_SIGNED_REGIME_SPLIT_MOMENT_AND_LARGE_VALUES_OPEN", "Cycle 86 status mismatch")
    return {
        "cycle81_role": "supply exact dual logarithmic columns and support",
        "cycle86_role": "supply the diagonal second-moment target and signed range",
    }


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-87-mellin-alias-atlas-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_MELLIN_ALIAS_TRICHOTOMY_BOUND_OR_WEB_OPEN",
        "claim_boundary": "This artifact proves the exact primal pair kernel, atom diagonal, and dual same-h/nonstationary/stationary-alias trichotomy. It proves no diagonal-strength second moment, new band, large-value theorem, packet closure, density gain, or interval gain.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "prior_context": {"epistemic_status": "PROVED", **validate_priors()},
        "pair_kernel": {
            "epistemic_status": "PROVED",
            "statement": "The primal pair kernel is K sum_m hatU(K(m-Delta z)); its atom diagonal has exponent xi+14/15 and its continuous zero mode is U(0)=0.",
        },
        "alias_atlas": {
            "epistemic_status": "PROVED",
            "statement": "Dual cross terms split into same h, nonstationary 0<|Delta h|<<K/D, and stationary aliases k=D Delta h/(2pi m) with 1<<|m|<<Q and amplitude sqrt(K/|m|).",
        },
        "analytic_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Bound the three branches jointly by X^(xi+14/15+o(1)) or export explicit alias data as a valuation/anchor web.",
        },
        "exact_replay": exact_json(rows),
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_87_mellin_alias_atlas_v1.py --write",
            "check_command": "python3 proof/build_cycle_87_mellin_alias_atlas_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_87_mellin_alias_atlas_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 87 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 87 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 87 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

