#!/usr/bin/env python3
"""Seal the Cycle-2 frozen-barrier seed-dependence obstruction."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


OUTPUT = ROOT / "artifacts/cycle-2-b003-frozen-seed-dependence-v1.json"
INPUTS = {
    "mathematical_record": (
        "proof/frozen_barrier_seed_dependence.md",
        "d12e34fe008480eb5306fb246d431ce3bdc3fc6c59b2f940f48238751040fede",
    ),
    "exact_witness_audit": (
        "proof/verify_frozen_seed_dependence.py",
        "3dba1b65df3375d29b6e199fd3a5f836efed237b1c65f8867ba0c32be7b7520c",
    ),
    "prior_theorem": (
        "artifacts/cycle-2-b002-frozen-ballistic-transmission-v1.json",
        "721b2c0d8c3e582a787c2af827da483495780c6d304bde222010ee2461286781",
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
    exact = run_json("proof/verify_frozen_seed_dependence.py")
    scaffold = run_json("proof/test_cycle_seal_v1.py")
    require(exact.get("status") == "PASS", "seed-dependence audit failed")
    require(exact.get("critical_phase_separation") == 2, "phase mismatch")
    require(scaffold.get("status") == "PASS", "scaffold self-test failed")
    return {
        "artifact_id": "cycle-2-b003-frozen-seed-dependence-v1",
        "budget_ordinal": "B003",
        "cycle": 2,
        "record_type": "METHOD_OBSTRUCTION",
        "recorded_at_utc": "2026-08-08T13:46:04Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": (
            "Even with the competition barrier frozen exactly, critical front "
            "phase depends on J_C(q_0)=integral exp(y)H_C(y)q_0(y)dy. A "
            "previous-hump-only event state is not universal over incoming seeds."
        ),
        "claim_boundary": (
            "This is a theorem for the frozen linear leading-edge problem. It "
            "does not exclude nonlinear seed universality, select a wavelength, "
            "justify freezing K*u, or prove P1/P2."
        ),
        "uniform_corollary": (
            "For |s|<=A log(t), q(t,2t+s)=(4*pi*t)^(-1/2) "
            "exp(-s)(J_C(q_0)+o(1))."
        ),
        "exact_witness": {
            "barrier": "C(x)=3 for x<0 and C(x)=0 for x>=0",
            "seeds": "equal-mass translates q_-2 and q_-3 of one bump",
            "critical_phase_separation": 2,
        },
        "cycle_decision": {
            "killed_state": "frozen previous competition profile C alone",
            "minimal_surviving_linear_state": "(C, J_C(q_0))",
            "next_gate": (
                "Determine whether nonlinear top-hat evolution makes J_C(q_0) "
                "a universal function of the established hump profile."
            ),
        },
        "audit": {"exact_step_translation": exact, "scaffold": scaffold},
        "frozen_hashes": freeze_inputs(
            ROOT,
            {label: (ROOT / path, digest) for label, (path, digest) in INPUTS.items()},
        ),
        "runtime": check_runtime("cycle-2 frozen seed dependence"),
        "sealer": {
            "path": "proof/build_cycle2_frozen_seed_dependence.py",
            "sha256": sha256(Path(__file__)),
        },
        "replay": {
            "exact_witness_audit": "python3 proof/verify_frozen_seed_dependence.py",
            "scaffold_test": "python3 proof/test_cycle_seal_v1.py",
            "artifact_check": (
                "python3 proof/build_cycle2_frozen_seed_dependence.py --check"
            ),
        },
    }


if __name__ == "__main__":
    raise SystemExit(
        run_cli(description=__doc__, output=OUTPUT, payload_factory=payload)
    )
