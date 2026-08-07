#!/usr/bin/env python3
"""Seal the Stage 1 exact baseline and scoped obstruction boundary."""

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
from proof.verify_stage1_baseline import build_report  # noqa: E402


OUTPUT = ROOT / "artifacts/cycle-1-b1-stage1-obstruction-v1.json"
HASHES = {
    "obstruction_note": (
        "docs/stage1-obstruction.md",
        "332bc682750dc17c58f96793ada46a0cd9ff2419b01a843eab6f960f241965ac",
    ),
    "source_audit": (
        "discovery/stage1-source-audit.md",
        "62b0fea3ff23edcf39b8fb070f8c54df6e22fcbc79b862e1bbd3d9ade732f129",
    ),
    "selection": (
        "discovery/cycle-1-selection.md",
        "c1b6d04051d9b923bf0d7868d8181e20454242369fdedcba5f7a7936a1d0cfd2",
    ),
    "failure_ledger": (
        "discovery/failure-ledger.md",
        "e248a739fe76128d4d9f7c69d582c8d738dda8e57deb8491914ff714a501f6b8",
    ),
    "conventions": (
        "src/conventions.py",
        "b6b328f6b7b1725c39f4e4ba4084c275a141189b7efe32e9727c75488d705bb3",
    ),
    "verifier": (
        "proof/verify_stage1_baseline.py",
        "c9532a798f89eba96e0b26135f7c8dd807607a771a0dedd286050cf6cd93b7ab",
    ),
    "baseline_tests": (
        "tests/test_stage1_baseline.py",
        "423411f15c5ab9c1feaf40c4a94776fe3610364ddbcdcda81d2075ec1bf84e69",
    ),
    "scaffold": (
        "proof/cycle_seal_v1.py",
        "c4a09e7baa8a5588d4c6855a533eb933c85791707ed9653437644c1e1ad6c163",
    ),
    "scaffold_tests": (
        "tests/test_cycle_seal_v1.py",
        "43650aea32eaf3d9f3ff69083830db71c4be0da31fefd313f024f504eb52432d",
    ),
}


def payload() -> dict[str, object]:
    report = build_report()
    if report["status"] != "PASS":
        raise RuntimeError("Stage 1 exact baseline did not pass")
    return {
        "artifact_id": "cycle-1-b1-stage1-obstruction-v1",
        "author": "Hainan Zhao",
        "budget_ordinal": "B1",
        "cycle": 1,
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "record_type": "BASELINE_AND_SCOPED_METHOD_OBSTRUCTION",
        "outcome": (
            "The graph-independent high- and low-temperature identities are fixed and "
            "exactly replayed. The uncompressed surface Kac-Ward/Pfaffian route has "
            "2^(2g) terms, while the free L-cube has orientable genus at least "
            "ceil(1+(L^3-3L^2)/4); hence that standard route has a volume-exponential "
            "spin-structure sum. Ordinary Jordan-Wigner locality and scalar self-duality "
            "also fail in their stated scopes."
        ),
        "claim_boundary": (
            "This is not a universal lower bound on all exact representations, not a "
            "thermodynamic-limit result, and not an exact solution or critical-point claim."
        ),
        "falsifier": (
            "A valid counterexample to the Euler/girth genus bound or Cimasoni theorem "
            "instantiation, or any exact mismatch in a declared finite replay case."
        ),
        "exact_replay": report,
        "frozen_hashes": freeze_inputs(
            ROOT, {label: (ROOT / path, digest) for label, (path, digest) in HASHES.items()}
        ),
        "runtime": check_runtime("cycle-1-stage1"),
        "sealer": {
            "path": "proof/build_cycle1_stage1_obstruction.py",
            "sha256": sha256(Path(__file__)),
        },
        "replay": {
            "baseline": "python3 proof/verify_stage1_baseline.py",
            "tests": "python3 -m unittest discover -s tests -v",
            "artifact_check": "python3 proof/build_cycle1_stage1_obstruction.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
