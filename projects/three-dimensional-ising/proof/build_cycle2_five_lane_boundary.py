#!/usr/bin/env python3
"""Seal the five-lane Stage 2 screen and post-test selection boundary."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.cycle_seal_v1 import (  # noqa: E402
    check_runtime,
    freeze_inputs,
    run_cli,
    sha256,
)
from proof.verify_cycle2_five_lanes import build_report  # noqa: E402


OUTPUT = ROOT / "artifacts/cycle-2-b2-five-lane-boundary-v1.json"
HASHES = {
    "prior": (
        "artifacts/cycle-1-b1-stage1-obstruction-v1.json",
        "9125472b04a263222a62d2e23b573c400f839c5c795e1929de117605a3a5a198",
    ),
    "candidate_report": (
        "docs/cycle2-candidate-report.md",
        "021ee0d7f46ce58686c6220f1bb5a4874fd2b550d55118696e1a509013c9b013",
    ),
    "selection": (
        "discovery/cycle-2-five-lane-selection.md",
        "05d821d464aa8172037cfec1736a1d61f9a3ce2f1132110ab6c2cf1344bc2645",
    ),
    "source_audit": (
        "discovery/cycle2-source-audit.md",
        "3e3e5b5e8948efbe96add2817e2ae86311cb7d532a7be951f46f7f48de0f4614",
    ),
    "failure_ledger": (
        "discovery/failure-ledger-cycle2.md",
        "d7896743d4139ad0e323b9109959311e5f3e68053127b10bd3b5fb608cf37484",
    ),
    "conventions": (
        "src/conventions.py",
        "b6b328f6b7b1725c39f4e4ba4084c275a141189b7efe32e9727c75488d705bb3",
    ),
    "embedding": (
        "src/embeddings.py",
        "ebc9f3839f74d4590bcd853913b69ca4effc5a5a44e415203bfffca30092dada",
    ),
    "verifier": (
        "proof/verify_cycle2_five_lanes.py",
        "b5f1db0718b9b1677083545af66ebc88e5ebae390a67a203c5da899e77bdc038",
    ),
    "tests": (
        "tests/test_cycle2_five_lanes.py",
        "f19e2723e1f3a273502d0078c0c4d372274d6ce4b0198a7d9f9e6892c1162f1e",
    ),
    "requirements": (
        "requirements.txt",
        "8347daed02ebf7b3c3cfa494e97049b7e0ab15b9af00a5addd843ed44381a64a",
    ),
    "scaffold": (
        "proof/cycle_seal_v1.py",
        "c4a09e7baa8a5588d4c6855a533eb933c85791707ed9653437644c1e1ad6c163",
    ),
}


def payload() -> dict[str, object]:
    report = build_report()
    if report["status"] != "PASS" or report["sympy_version"] != "1.12":
        raise RuntimeError("Cycle 2 exact report or pinned SymPy version failed")
    selected = report["selection_after_all_tests"]["selected_lane"]
    if selected != "B_spin_structure_compression":
        raise RuntimeError("post-test selection drift")
    return {
        "artifact_id": "cycle-2-b2-five-lane-boundary-v1",
        "author": "Hainan Zhao",
        "budget_ordinal": "B2",
        "cycle": 2,
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "record_type": "FIVE_LANE_DECISIVE_SCREEN_AND_SELECTION",
        "outcome": (
            "All five Stage 2 lanes received an exact first falsification test. Lane A is "
            "a restricted no-go for the direct vertex tetrahedron tensor and invariant "
            "D<=4 extensions; Lane B survives only through growing-genus TT rank or an "
            "exact L-recurrence; Lane C's direct known-bosonization substitution is killed "
            "by the Gauss-law mismatch; Lane D is a restricted crossing-selector no-go; "
            "and Lane E is a restricted pairwise-closure no-go. Lane B was selected only "
            "after all tests as the next exact experiment."
        ),
        "claim_boundary": (
            "No lane yet supplies a successful reduction, controlled thermodynamic limit, "
            "critical datum, or exact solution. Every no-go is limited to its stated ansatz."
        ),
        "falsifier": (
            "Any replay mismatch, invalid minimum-genus rotation system, vanishing declared "
            "residual, or source theorem whose exact hypotheses contradict the recorded use."
        ),
        "exact_replay": report,
        "frozen_hashes": freeze_inputs(
            ROOT, {label: (ROOT / path, digest) for label, (path, digest) in HASHES.items()}
        ),
        "runtime": check_runtime("cycle-2-five-lane"),
        "sealer": {
            "path": "proof/build_cycle2_five_lane_boundary.py",
            "sha256": sha256(Path(__file__)),
        },
        "replay": {
            "five_lanes": "python3 proof/verify_cycle2_five_lanes.py",
            "tests": "python3 -m unittest discover -s tests -v",
            "artifact_check": "python3 proof/build_cycle2_five_lane_boundary.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
