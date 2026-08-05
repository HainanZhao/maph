"""Build the immutable Cycle-2 orbit-quotient performance-boundary record."""

from __future__ import annotations

import re
from pathlib import Path
import subprocess

from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-2-b002-lrc-orbit-quotient-v1.json"
INPUTS = {
    "preregistration": (
        ROOT / "docs/cycle-2-b002-lrc-orbit-quotient-preregistration-v1.md",
        "10e47b26145f578e46e5bf3867a14a31132f5f7630d41d7ac76364447ccdc896",
    ),
    "canonical_augmentation_argument": (
        ROOT / "proof/cycle_2_canonical_augmentation_argument.md",
        "58873cdeda9e3f86c0934f467f354230b149be2d46ee6315289e65b61acbb336",
    ),
    "exact_quotient_search": (
        ROOT / "discovery/lrc_orbit_quotient.cpp",
        "37ae1fc9eeb63089fe66467bd0c81f7b4d39c6da593f66359399dc98d5de76de",
    ),
    "baseline_k6_tuples": (
        ROOT / "discovery/out/orbit-k6-p47-dynamic.txt",
        "3282243c9bd46b7cf0cb2f57a60fcf75d01df5f3ffdd11fe0ad91f8713170e03",
    ),
    "baseline_k6_result": (
        ROOT / "discovery/out/orbit-k6-p47-dynamic.result",
        "975113ffadbb7aba24993618c05147c0827906532e4ae95bd66421ab77c82121",
    ),
    "baseline_k7_tuples": (
        ROOT / "discovery/out/orbit-k7-p47-dynamic.txt",
        "8687bd7725b570baeb72d4d666a52c6b9fcf20204a6c4a036c21c672c9338a4d",
    ),
    "baseline_k7_result": (
        ROOT / "discovery/out/orbit-k7-p47-dynamic.result",
        "d5c9bdde39b1ffee30e1d9e4c9a55fc24ff45dc8334106691cd77ef130596303",
    ),
    "frontier_result": (
        ROOT / "discovery/out/orbit-k13-p199-dynamic.result",
        "a667907434fd63bf0979d924d97713e8c359fbd2dd7a3ab80cdaad9f2b1f5d7e",
    ),
    "frontier_timing": (
        ROOT / "discovery/out/orbit-k13-p199-dynamic.time",
        "e8919497ba72bf52543174a56e340f177029a7bfc33ff81e7495de12f4c745d7",
    ),
    "scaffold": (
        ROOT / "proof/cycle_seal_v1.py",
        "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7",
    ),
    "regression_test": (
        ROOT / "tests/test_cycle_2_lrc_orbit_quotient.py",
        "feea0afad2d66add17313bef90c1de7690fc4b02bbe5d309b46c48c7279bbc55",
    ),
    "preregistration_validator": (
        ROOT / "../../tools/preregistration_check.py",
        "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
    ),
}


def metric(pattern: str, text: str, cast=int):
    match = re.search(pattern, text)
    if not match:
        raise RuntimeError(f"missing frozen metric: {pattern}")
    return cast(match.group(1))


def payload() -> dict:
    runtime = check_runtime("Cycle 2")
    frozen = freeze_inputs(ROOT, INPUTS)
    k6 = (ROOT / "discovery/out/orbit-k6-p47-dynamic.result").read_text()
    k7 = (ROOT / "discovery/out/orbit-k7-p47-dynamic.result").read_text()
    frontier = (ROOT / "discovery/out/orbit-k13-p199-dynamic.result").read_text()
    timing = (ROOT / "discovery/out/orbit-k13-p199-dynamic.time").read_text()
    compiler = subprocess.run(
        ["g++", "--version"], check=True, capture_output=True, text=True
    ).stdout.splitlines()[0]
    return {
        "artifact_id": "cycle-2-b002-lrc-orbit-quotient-v1",
        "budget_ordinal": "B002",
        "cycle": 2,
        "recorded_at_utc": "2026-08-03T13:53:26Z",
        "status": "SEALED",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "The declared largest-entry canonical-parent quotient has a written completeness argument and reproduces the frozen p=47 tuple sets exactly. At k=13,p=199 it breached the preregistered aggregate node cap before completing any depth-13 leaf, so it is strategically insufficient at this frontier. This is an algorithmic performance result only: it proves neither a mathematical obstruction, J(13,199)=empty, nor LRC(13).",
        "baseline_validation": {
            "epistemic_status": "OBSERVED",
            "statement": "Three-thread dynamic scheduling reproduced both Cycle-1 baseline tuple files byte-for-byte and preserved the unsharded node and leaf counts.",
            "counts": {
                "k6_p47": metric(r"canonical_solutions=(\d+)", k6),
                "k7_p47": metric(r"canonical_solutions=(\d+)", k7),
            },
            "nodes": {"k6_p47": metric(r"nodes=(\d+)", k6), "k7_p47": metric(r"nodes=(\d+)", k7)},
            "leaves": {"k6_p47": metric(r"leaves=(\d+)", k6), "k7_p47": metric(r"leaves=(\d+)", k7)},
        },
        "frontier_gate": {
            "epistemic_status": "OBSERVED",
            "outcome": "FAILED_NODE_CAP",
            "k": metric(r"k=(\d+)", frontier),
            "p": metric(r"p=(\d+)", frontier),
            "threads": metric(r"threads=(\d+)", frontier),
            "task_depth": metric(r"task_depth=(\d+)", frontier),
            "frontier_tasks": metric(r"frontier_tasks=(\d+)", frontier),
            "assigned_tasks": metric(r"assigned_tasks=(\d+)", frontier),
            "nodes": metric(r"nodes=(\d+)", frontier),
            "leaves": metric(r"leaves=(\d+)", frontier),
            "canonical_solutions_seen": metric(r"canonical_solutions=(\d+)", frontier),
            "wall_seconds": metric(r"wall_seconds=([0-9.]+)", frontier, float),
            "peak_rss_kib": metric(r"rss_kb=(\d+)", timing),
            "statement": "The shared three-worker search crossed the frozen 586,985,072-node limit by the single detecting node; only three of 42,925 depth-four tasks began and no leaf was reached.",
        },
        "structural_diagnosis": {
            "epistemic_status": "CONJECTURED",
            "statement": "Largest-entry deletion preserves an orbit tree but appears to destroy the uncovered-time choice that makes exact-cover branching effective.",
            "falsifier": "A reproducible complete k=13,p=199 run using the frozen parent and pruning rules that meets both tenfold node and leaf caps.",
        },
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "adopted": True,
            "recommendation": "Seal Cycle 2 as exact quotient, strategically insufficient at the frozen frontier, and open a distinct Cycle 3.",
            "next_action": "Open Cycle 3 for a coverage-aware invariant parent with a canonical uncovered class and compatible add/delete rules; require the same baseline tuple equality before any frontier claim.",
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Construct a coverage-directed orbit quotient that retains one construction path for every cover orbit while avoiding the largest-entry prefix explosion.",
        },
        "runtime": {**runtime, "compiler": compiler, "compile_flags": "-std=c++20 -O3 -march=native -flto -DNDEBUG -pthread"},
        "frozen_hashes": frozen,
        "replay": {
            "check_command": "python3 proof/build_cycle_2_lrc_orbit_quotient.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_2_lrc_orbit_quotient.py -v",
            "write_command": "python3 proof/build_cycle_2_lrc_orbit_quotient.py --write",
            "compile_command": "g++ -std=c++20 -O3 -march=native -flto -DNDEBUG -pthread discovery/lrc_orbit_quotient.cpp -o discovery/out/lrc_orbit_quotient_opt",
            "frontier_command": "taskset -c 0-2 discovery/out/lrc_orbit_quotient_opt --k 13 --p 199 --node-cap 586985072 --max-seconds 3600 --threads 3 --task-depth 4 --output discovery/out/orbit-k13-p199-dynamic.txt",
        },
        "sealer": {"path": "proof/build_cycle_2_lrc_orbit_quotient.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
