#!/usr/bin/env python3
"""Seal a read-only hostile audit of the G1 route-decision v1 package."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = {
    "adjudicator": (ROOT / "proof/adjudicate_g1_route_selection_v1.py", "5879cadd61bf23015cbc27ed00d049f3a8792dc75dd09e835dd7321aa307d355"),
    "artifact": (ROOT / "artifacts/cycle-3-g1-route-decision-v1.json", "a54115024a6dd1eae5cff7653b1488d9cde05d8063f4769e27eeda7aec702d6b"),
    "document": (ROOT / "docs/cycle-3-g1-route-decision-v1.md", "8eddc8d1dc7624937e81ad89d7bd933ea815c9c7a2a0e9982fd98a6cb105ea7c"),
    "tests": (ROOT / "tests/test_g1_route_selection_v1.py", "4e24bb3524c31c81a92b4fcb148c9c6aecb6fb3643fcd0a3c998338730bc6435"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_checked(command: list[str]) -> dict[str, Any]:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    return {"command": command, "returncode": result.returncode, "stderr": result.stderr}


def audit() -> dict[str, Any]:
    require(platform.python_implementation() == "CPython", "hostile audit requires CPython")
    require(platform.python_version() == "3.12.3", "hostile audit requires CPython 3.12.3")
    require(sys.flags.optimize == 0, "hostile audit requires non-optimized mode")
    hashes: dict[str, str] = {}
    for label, (path, expected) in PACKAGE.items():
        require(path.is_file(), f"sealed package member missing: {label}")
        actual = sha256(path)
        require(actual == expected, f"sealed package member hash mismatch: {label}")
        hashes[label] = actual

    script = PACKAGE["adjudicator"][0]
    script_text = script.read_text(encoding="utf-8")
    artifact = json.loads(PACKAGE["artifact"][0].read_text(encoding="utf-8"))
    normal = run_checked([sys.executable, str(script), "--check", str(PACKAGE["artifact"][0])])
    optimized = run_checked([sys.executable, "-O", str(script), "--check", str(PACKAGE["artifact"][0])])
    optimized_twice = run_checked([sys.executable, "-OO", str(script), "--check", str(PACKAGE["artifact"][0])])
    require(normal["returncode"] == 0, "sealed normal-mode replay failed")
    require(optimized["returncode"] != 0, "-O did not fail closed")
    require(optimized_twice["returncode"] != 0, "-OO did not fail closed")

    predicate_defect = all(fragment in script_text for fragment in (
        "p2a_selected = retained_rows > 0",
        "p2b_selected = retained_rows > 0 and energy[\"summary\"][\"energy_retention_eligible_rows\"] > 0",
        "p2c_selected = retained_rows > 0 and transfer[\"B_minus_source_term\"][\"LV3\"] == \"0/1\"",
        "combination_selected = sum((p2a_selected, p2b_selected, p2c_selected)) >= 2",
    ))
    identity_defect = "\"adjudicator\"" not in artifact
    require(predicate_defect, "expected route-predicate defect was not found in sealed v1")
    require(identity_defect, "expected executable-identity defect was not found in sealed v1")

    return {
        "artifact_id": "g1-route-decision-v1-hostile-audit-v1",
        "epistemic_status": "OBSERVED",
        "status": "FAIL_ROUTE_PREDICATE_COMPLETENESS",
        "claim_boundary": "Read-only audit of the sealed G1 route-decision v1 package. This records a program-decision defect, not a mathematical result or route selection.",
        "audited_package_hashes": hashes,
        "replay": {"normal": normal, "optimized": optimized, "optimized_twice": optimized_twice},
        "findings": {
            "normal_replay": "PASS",
            "optimized_mode": "PASS_FAIL_CLOSED",
            "frozen_input_hashes": "PASS",
            "route_predicates": {
                "status": "FAIL",
                "detail": "The v1 code equates any retained row with P2A evidence and combines that proxy with fixed LV3/energy booleans for P2B/P2C/COMBINATION. The frozen clauses require distinct trace, energy/affine, named decomposition/branch, and separate labeled-evidence predicates; a retained row alone does not establish them.",
            },
            "adjudicator_identity": {
                "status": "FAIL",
                "detail": "The v1 artifact pins only its inputs. It does not record the adjudicator path/SHA-256, so the artifact cannot bind the executable which purportedly made the decision.",
            },
        },
        "containment": "Do not promote G1_CLOSED_NO_SELECTION from v1. The empirical 0-retained observation remains valid, but a v2 adjudicator must fail on any retained row unless separately sealed evidence proves each frozen route predicate.",
        "required_correction": [
            "Make the v2 no-selection adjudicator explicitly no-selection-only: require zero retained rows and set every route predicate false; a nonzero retained count must fail closed rather than auto-select any route.",
            "For any future affirmative route decision, require separately versioned, labeled evidence for the exact frozen P2A/P2B/P2C predicates and for a combination.",
            "Record the v2 adjudicator path and SHA-256 in its decision artifact and have --check recompute that identity.",
            "Add normal, -O, -OO, frozen-input-tamper, and retained-row counterfactual regressions.",
        ],
    }


def render(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    require(args.check.is_file(), "hostile-audit artifact is absent")
    require(args.check.read_bytes() == render(result), "hostile-audit artifact mismatch")
    print(json.dumps({"status": result["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
