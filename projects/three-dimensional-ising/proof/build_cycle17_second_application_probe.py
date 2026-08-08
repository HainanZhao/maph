#!/usr/bin/env python3
"""Seal the bounded second-application prefilter outcome."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256  # noqa: E402

OUTPUT = ROOT / "artifacts/cycle-17-b17-second-application-probe-v1.json"
HASHES = {
    "preregistration": ("discovery/cycle-17-second-application-preregistration.md", "d1b5c86889c12b0706b2ea26ee7614d2c7c6a31122944054162cb671acf2b3a1"),
    "outcome": ("discovery/cycle-17-second-application-outcome.md", "2938f71d38bad7ad1eacb4e5e2cb1699e8e48e3a120e833ac9d71525f009607c"),
    "theorem": ("proof/abstract_spin_structure_separator_theorem.md", "5baa6fa7038133c498c34719f25ccf8de311cce2e2920d6c07ffa0511ed82c9c"),
    "scaffold": ("proof/cycle_seal_v1.py", "c4a09e7baa8a5588d4c6855a533eb933c85791707ed9653437644c1e1ad6c163"),
}


def payload():
    return {
        "artifact_id": "cycle-17-b17-second-application-probe-v1",
        "author": "Hainan Zhao",
        "budget_ordinal": "B17",
        "cycle": 17,
        "status": "SEALED",
        "epistemic_status": "PROVED_TOPOLOGICAL_PREFILTER_AND_BOUNDED_STOP",
        "record_type": "OPTIONAL_SECOND_APPLICATION_PROBE",
        "outcome": "Natural honeycomb/triangular strips are genus zero, or genus one after full periodic closure, and do not furnish the preregistered nontrivial second application.",
        "gate_outcome": "T7_STOP_RULE_FIRED_QUESTION_OPEN",
        "claim_boundary": "No no-go theorem for engineered honeycomb or triangular surface embeddings is claimed.",
        "frozen_hashes": freeze_inputs(ROOT, {k: (ROOT / p, h) for k, (p, h) in HASHES.items()}),
        "runtime": check_runtime("cycle-17-second-application"),
        "sealer": {"path": "proof/build_cycle17_second_application_probe.py", "sha256": sha256(Path(__file__))},
        "replay": {"artifact_check": "python3 proof/build_cycle17_second_application_probe.py --check"}
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
