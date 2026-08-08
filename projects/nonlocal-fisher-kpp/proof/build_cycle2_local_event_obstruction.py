#!/usr/bin/env python3
"""Seal the Cycle-2 exact local-event closure obstruction."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))

from cycle_seal_v1 import (
    check_runtime,
    freeze_inputs,
    require,
    run_cli,
    sha256,
)


OUTPUT = ROOT / "artifacts/cycle-2-b001-local-event-closure-obstruction-v1.json"
INPUTS = {
    "mathematical_record": (
        "proof/cycle2_local_event_obstruction.md",
        "7b4b949275f955758461656b07eaf5780d945811d7222cb447a5766160240f35",
    ),
    "exact_replay": (
        "proof/verify_local_event_obstruction.py",
        "621df28273abd81a1b9e71e36a5bb7b66f9f8151185d1acd5b428763033a767f",
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
        [sys.executable, str(ROOT / relative)],
        cwd=ROOT,
        text=True,
    )
    return json.loads(output)


def payload() -> dict[str, object]:
    exact = run_json("proof/verify_local_event_obstruction.py")
    scaffold = run_json("proof/test_cycle_seal_v1.py")
    require(exact.get("status") == "PASS", "exact obstruction replay failed")
    require(exact.get("bump_mass") == "1/17920", "bump mass mismatch")
    require(exact.get("level_speed_delta") == "-1/125440", "speed mismatch")
    require(exact.get("critical_ray_checks") == 54, "ray coverage mismatch")
    require(scaffold.get("status") == "PASS", "scaffold self-test failed")
    return {
        "artifact_id": "cycle-2-b001-local-event-closure-obstruction-v1",
        "budget_ordinal": "B001",
        "cycle": 2,
        "record_type": "METHOD_OBSTRUCTION",
        "recorded_at_utc": "2026-08-08T13:08:52Z",
        "status": "SEALED",
        "epistemic_status": "CONJECTURED",
        "outcome": (
            "Equal complete local germs at a regular density level can have "
            "different exact level velocities because the top-hat competition "
            "trace is not locally determined."
        ),
        "claim_boundary": (
            "Kills exact local-germ-only hump-event closure for arbitrary "
            "positive data. It does not rule out an asymptotic map carrying a "
            "window profile and proves no wake-selection or P1/P2 statement."
        ),
        "cycle_decision": {
            "decision": (
                "Abandon exact Markov closure on hump positions/local edge "
                "shape; continue Cycle 2 with a nonlocal boundary-layer trace."
            ),
            "falsifier": (
                "Two positive profiles identical near the level point have "
                "level-speed difference -epsilon/17920."
            ),
            "surviving_state": "Competition trace K*u or a controlled window profile.",
        },
        "audit": {
            "exact_arithmetic": exact,
            "scaffold": scaffold,
        },
        "frozen_hashes": freeze_inputs(
            ROOT,
            {label: (ROOT / path, digest) for label, (path, digest) in INPUTS.items()},
        ),
        "runtime": check_runtime("cycle-2 local-event obstruction"),
        "sealer": {
            "path": "proof/build_cycle2_local_event_obstruction.py",
            "sha256": sha256(Path(__file__)),
        },
        "replay": {
            "audit": "python3 proof/verify_local_event_obstruction.py",
            "scaffold_test": "python3 proof/test_cycle_seal_v1.py",
            "artifact_check": (
                "python3 proof/build_cycle2_local_event_obstruction.py --check"
            ),
        },
    }


if __name__ == "__main__":
    raise SystemExit(
        run_cli(description=__doc__, output=OUTPUT, payload_factory=payload)
    )
