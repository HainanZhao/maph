#!/usr/bin/env python3
"""Seal the Cycle-2 critical exponential-moment dissipation theorem."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


OUTPUT = ROOT / "artifacts/cycle-2-b004-critical-exponential-moment-v1.json"
INPUTS = {
    "mathematical_record": (
        "proof/critical_exponential_moment.md",
        "f8fca6a2d40f43696dbd495a5e17c9da0e0124b2175522bd6df0240758bb01ec",
    ),
    "exact_coefficient_audit": (
        "proof/verify_critical_exponential_moment.py",
        "8585c0093a9eb85f3c469913aad5207ae4c1229243e422b78f5318ba4a016af2",
    ),
    "sealing_scaffold": (
        "proof/cycle_seal_v1.py",
        "2061713b05a9c2a64677a7fd504d6c987ecae7ef9cf46da218b803d92b0816d6",
    ),
    "scaffold_test": (
        "proof/test_cycle_seal_v1.py",
        "13b7c93eaadba30e33a39aa0ad3e31431af5ec47296aa30e0d6df0639e55be04",
    ),
}


def run_json(relative: str) -> dict[str, object]:
    output = subprocess.check_output(
        [sys.executable, str(ROOT / relative)], cwd=ROOT, text=True
    )
    return json.loads(output)


def payload() -> dict[str, object]:
    exact = run_json("proof/verify_critical_exponential_moment.py")
    scaffold = run_json("proof/test_cycle_seal_v1.py")
    require(exact.get("status") == "PASS", "critical-moment audit failed")
    require(exact.get("total_exact_checks") == 11, "audit coverage mismatch")
    require(scaffold.get("status") == "PASS", "scaffold self-test failed")
    return {
        "artifact_id": "cycle-2-b004-critical-exponential-moment-v1",
        "budget_ordinal": "B004",
        "cycle": 2,
        "record_type": "THEOREM_AND_METHOD_OBSTRUCTION",
        "recorded_at_utc": "2026-08-08T13:51:06Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": (
            "For the full nonlinear top-hat equation, exp(-2t) integral "
            "exp(plus_or_minus x/sqrt(D))u is strictly decreasing, with an "
            "explicit positive top-hat pair-interaction dissipation."
        ),
        "translation_delay": (
            "If u(t+T,x)=u(t,x-lambda), then lambda/sqrt(D)=2T-" 
            "integral_0^T tilted_average(K*u)dt, hence lambda/T<2sqrt(D)."
        ),
        "claim_boundary": (
            "Requires a nonzero nonnegative classical solution with finite "
            "critical exponential moments. It rules out an exact localized "
            "repeating packet at pulled speed, not a front with divergent "
            "critical moment, a stationary deposited wake, P1/P2, or any "
            "specific wake wavelength."
        ),
        "published_dependency": {
            "source": "Hamel and Ryzhik, On the nonlocal Fisher-KPP equation",
            "doi": "10.1088/0951-7715/27/11/2735",
            "result": "Theorem 1.2",
            "use": "global bounded classical solution for bounded nonnegative data",
            "hypothesis_check": (
                "The radius-one top-hat kernel is nonnegative, has unit mass, "
                "and has positive essential infimum on an interval."
            ),
        },
        "cycle_decision": {
            "killed_state": (
                "An exact finite-moment shedding packet that repeats at or "
                "above the pulled speed."
            ),
            "required_new_ingredient": (
                "Separate the critical leading tail from the localized wake "
                "and retain the tilted competition-delay integral."
            ),
            "next_gate": (
                "Bound the tilted competition delay over one actual nonlinear "
                "hump-formation cycle."
            ),
        },
        "audit": {"exact_coefficients": exact, "scaffold": scaffold},
        "frozen_hashes": freeze_inputs(
            ROOT,
            {label: (ROOT / path, digest) for label, (path, digest) in INPUTS.items()},
        ),
        "runtime": check_runtime("cycle-2 critical exponential moment"),
        "sealer": {
            "path": "proof/build_cycle2_critical_exponential_moment.py",
            "sha256": sha256(Path(__file__)),
        },
        "replay": {
            "exact_coefficient_audit": (
                "python3 proof/verify_critical_exponential_moment.py"
            ),
            "scaffold_test": "python3 proof/test_cycle_seal_v1.py",
            "artifact_check": (
                "python3 proof/build_cycle2_critical_exponential_moment.py --check"
            ),
        },
    }


if __name__ == "__main__":
    raise SystemExit(
        run_cli(description=__doc__, output=OUTPUT, payload_factory=payload)
    )
