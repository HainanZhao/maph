#!/usr/bin/env python3
"""Seal the Cycle-2 general exponential-moment dissipation theorem."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


OUTPUT = ROOT / "artifacts/cycle-2-b005-general-exponential-moment-v1.json"
INPUTS = {
    "mathematical_record": (
        "proof/general_exponential_moment.md",
        "57fdbddb1e9acc494e87484916207cc0f3903deae529015e6d4ae9b8dc49b426",
    ),
    "exact_algebra_audit": (
        "proof/verify_general_exponential_moment.py",
        "331fc89cc1c3729c968125407c39887112692e9e3120037a73c2d841f32bee44",
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
    exact = run_json("proof/verify_general_exponential_moment.py")
    scaffold = run_json("proof/test_cycle_seal_v1.py")
    require(exact.get("status") == "PASS", "general moment audit failed")
    require(exact.get("total_exact_checks") == 11, "audit coverage mismatch")
    require(scaffold.get("status") == "PASS", "scaffold self-test failed")
    return {
        "artifact_id": "cycle-2-b005-general-exponential-moment-v1",
        "budget_ordinal": "B005",
        "cycle": 2,
        "record_type": "THEOREM_GENERALIZATION_FOR_REVIEW_NOTE",
        "recorded_at_utc": "2026-08-08T14:06:12Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": (
            "For every even nonnegative competition kernel and every finite "
            "exponential tilt a, exp(-(1+D*a^2)t) times the a-weighted mass "
            "has an exact nonnegative pair-interaction dissipation."
        ),
        "translation_delay": (
            "An exact translated finite-a-moment state has speed "
            "D*a+1/a minus its positive tilted competition delay; at the "
            "critical tilt this is strictly below 2sqrt(D)."
        ),
        "claim_boundary": (
            "Assumes a classical nonnegative solution and the weighted "
            "integrability and boundary decay needed for differentiation and "
            "integration by parts. It does not provide those hypotheses for "
            "every kernel, exclude fronts with divergent critical moment, "
            "select a wake wavelength, or prove asymptotic pattern formation."
        ),
        "relation_to_b004": (
            "B005 generalizes the sealed radius-one top-hat critical-tilt "
            "identity B004 to arbitrary even nonnegative kernels and arbitrary "
            "finite exponential tilts; it does not change the terminal gate."
        ),
        "audit": {"exact_algebra": exact, "scaffold": scaffold},
        "frozen_hashes": freeze_inputs(
            ROOT,
            {label: (ROOT / path, digest) for label, (path, digest) in INPUTS.items()},
        ),
        "runtime": check_runtime("cycle-2 general exponential moment"),
        "sealer": {
            "path": "proof/build_cycle2_general_exponential_moment.py",
            "sha256": sha256(Path(__file__)),
        },
        "replay": {
            "exact_algebra_audit": (
                "python3 proof/verify_general_exponential_moment.py"
            ),
            "scaffold_test": "python3 proof/test_cycle_seal_v1.py",
            "artifact_check": (
                "python3 proof/build_cycle2_general_exponential_moment.py --check"
            ),
        },
    }


if __name__ == "__main__":
    raise SystemExit(
        run_cli(description=__doc__, output=OUTPUT, payload_factory=payload)
    )
