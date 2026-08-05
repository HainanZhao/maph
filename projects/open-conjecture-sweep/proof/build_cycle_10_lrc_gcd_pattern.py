"""Seal Cycle 10's exact controls and bounded gcd-pattern performance gate."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
import subprocess

from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-10-b010-lrc-gcd-pattern-v1.json"
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-10-b010-lrc-gcd-pattern-preregistration-v1.md", "28347486a89f246b5b59d4ad9a4a3358ce319a6a5bdcd221f2df0f980fdaf140"),
    "soundness": (ROOT / "proof/cycle_10_gcd_pattern_soundness.md", "e88c7a7a7e9284a35a66e07022dd5fadf909be1fef05e12ae7f47553fc91e7db"),
    "pattern_engine": (ROOT / "discovery/lrc_gcd_pattern_lift.cpp", "7b46322c5832ce5b0ef80097235aa254584603364f21926bb6ba0d90487b440f"),
    "sealed_control_engine": (ROOT / "discovery/lrc_p199_multichoice_lift.cpp", "3478bc9b0723292f4b380dcf887935206219b3100d56eb1e9c6a0a34784facf8"),
    "control_result": (ROOT / "discovery/out/cycle10-controls.result", "593c165c64f4960167ef85b81bc99aac7d13648c31ecee117758dcf6313718c5"),
    "p199_result": (ROOT / "discovery/out/cycle10-p199-pattern.txt", "023218dafca5aeda4593262df25772df7b6b066a0afb4445578ffc966c364500"),
    "p199_timing": (ROOT / "discovery/out/cycle10-p199-pattern.time", "da1de2e1651773eb10e15685f70a4f29a4c888d12628a8d6f05d09d2157ee570"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "regression_test": (ROOT / "tests/test_cycle_10_lrc_gcd_pattern.py", "0508234e83a3ae515b6ce8773368735bc62f130d9405aa1c313f266bca41f50c"),
}


def elapsed_seconds(path: Path) -> float:
    match = re.search(r"Elapsed \(wall clock\).*?: (\d+):(\d+\.\d+)", path.read_text())
    if not match:
        raise RuntimeError("missing elapsed time")
    return int(match.group(1)) * 60 + float(match.group(2))


def peak_rss_kib(path: Path) -> int:
    match = re.search(r"Maximum resident set size \(kbytes\): (\d+)", path.read_text())
    if not match:
        raise RuntimeError("missing peak RSS")
    return int(match.group(1))


def payload() -> dict:
    runtime = check_runtime("Cycle 10 gcd pattern")
    frozen = freeze_inputs(ROOT, INPUTS)
    control = (ROOT / "discovery/out/cycle10-controls.result").read_text().strip()
    if control != "PASS h11_retained=0 p47_retained=0 p47_eliminated=53":
        raise RuntimeError("unexpected control result")
    rows = [line.split() for line in (ROOT / "discovery/out/cycle10-p199-pattern.txt").read_text().splitlines() if line.strip()]
    if len(rows) != 100 or [int(row[0]) for row in rows] != list(range(100)):
        raise RuntimeError("unexpected p199 sample indices")
    statuses = Counter(row[1] for row in rows)
    counters = [int(row[2]) for row in rows]
    if statuses != Counter({"CAP": 100}) or set(counters) != {2_000_001}:
        raise RuntimeError("unexpected p199 classifications or counters")
    timing = ROOT / "discovery/out/cycle10-p199-pattern.time"
    return {
        "artifact_id": "cycle-10-b010-lrc-gcd-pattern-v1",
        "budget_ordinal": "B010",
        "cycle": 10,
        "record_type": "CONTROL_AND_PERFORMANCE_GATE",
        "recorded_at_utc": "2026-08-03T17:28:44Z",
        "status": "SEALED",
        "epistemic_status": "OBSERVED",
        "outcome": "The exact gcd-pattern engine passed the complete H11 and p47 controls. Every row of the fixed 100-orbit p199 sample reached its two-million-node cap without SAT or UNSAT, so the engine did not discriminate the sample.",
        "claim_boundary": "The controls verify the exact gcd-admissibility predicate on the frozen finite instances. The p199 result is a bounded implementation-performance failure only: it proves no p199 lift feasible or infeasible and says nothing about F_1(13,199,14), J(13,199), or LRC(13).",
        "proved_controls": {
            "epistemic_status": "PROVED",
            "h11_retained": 0,
            "p47_retained": 0,
            "p47_eliminated": 53,
            "result": control,
        },
        "p199_performance": {
            "epistemic_status": "OBSERVED",
            "sample_orbits": 100,
            "status_counts": dict(statuses),
            "node_counter_total": sum(counters),
            "node_counter_per_row": 2_000_001,
            "explored_node_cap_per_row": 2_000_000,
            "cap_interpretation": "The counter includes the deterministic cap-plus-one sentinel. CAP is neither SAT nor UNSAT.",
            "wall_seconds": elapsed_seconds(timing),
            "peak_rss_kib": peak_rss_kib(timing),
            "worker_cpus": [0, 1, 2],
        },
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "adopted": True,
            "recommendation": "Seal Cycle 10 and open Cycle 11 for a proof-producing CDCL/PB encoding.",
            "primary_ideas": ["proof-producing CDCL", "CRT decomposition", "custom learned cores", "stop Problem 1"],
            "companion_independent_ideas": ["proof-producing CDCL", "certified PB/MaxSAT", "small exact CRT preflight"],
            "flaw": "The all-CAP result cannot distinguish intrinsic feasibility from weak bounds or repeated partial assignments.",
            "falsifier": "A directly checked SAT assignment is an improper first lift; a checked DRAT/LRAT or certified PB proof establishes finite UNSAT for its encoded base.",
            "next_action": "New Cycle 11: exact CNF/PB encoding with direct SAT-witness checking and independently checked proof output for UNSAT.",
        },
        "runtime": {**runtime, "compiler": subprocess.run(["g++", "--version"], check=True, capture_output=True, text=True).stdout.splitlines()[0]},
        "frozen_hashes": frozen,
        "replay": {
            "check_command": "python3 proof/build_cycle_10_lrc_gcd_pattern.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_10_lrc_gcd_pattern.py -v",
        },
        "sealer": {"path": "proof/build_cycle_10_lrc_gcd_pattern.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
