"""Seal Cycle 7's direct-feasibility performance-gate failure."""

from __future__ import annotations

import re
from pathlib import Path
import subprocess

from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-7-b007-lrc-direct-feasibility-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-7-b007-lrc-direct-feasibility-preregistration-v1.md", "dff01abbba6520215a1790388dde7474d5d18ca8a820f9a30ca9c4869c723b89"),
    "soundness_argument": (ROOT / "proof/cycle_7_direct_feasibility_soundness.md", "ad5e04b3977e5663c33fb1338c143568ead127f7039621f892204ff579fb0498"),
    "strata_builder": (ROOT / "discovery/make_cycle_7_strata.py", "3555a37145dcc66d26dd1bb73ce8d8806bfbea4c6e0e6eae7f32dd5784e112f2"),
    "strata": (ROOT / "discovery/out/cycle7-stratified-p199.txt", "2d44632aad9e39293f55f0cad25142a2ee6c9efc55e9e2541ddcb58b3ab6f8a6"),
    "benchmark": (ROOT / "discovery/lrc_direct_feasibility_benchmark.cpp", "5cf912b6cef4112418b460465bdde8cba306f7d5d7f54ad3f3dd5663533a1a4c"),
    "benchmark_first": (ROOT / "discovery/out/cycle7-direct-strata.txt", "ba19cc7f0f51ef0a1bffe0a57254105fe6a16651d6ccbf7fd15698bec9f065ce"),
    "benchmark_replay": (ROOT / "discovery/out/cycle7-direct-strata-replay.txt", "6cc1294122191b069839c76b431599dc1fc6bec2288934b689e64c817cb9ceec"),
    "partition_engine": (ROOT / "discovery/lrc_direct_partitioned.cpp", "02e39ded3a2d164ea6b1e820a9e878450d4f4e9efce08de7ce45abc3b7fdf6c5"),
    "k6_result": (ROOT / "discovery/out/cycle7-k6.result", "fa5a86535f8ed9fb88349e10d69758696c4846aec5f0c41c41cd6a8db907132e"),
    "k6_tuples": (ROOT / "discovery/out/cycle7-k6.txt", "3282243c9bd46b7cf0cb2f57a60fcf75d01df5f3ffdd11fe0ad91f8713170e03"),
    "k7_result": (ROOT / "discovery/out/cycle7-k7.result", "4e877a82a5ac5c13203ac692b87f98b85d06da72a28be255efddac2870fce705"),
    "k7_tuples": (ROOT / "discovery/out/cycle7-k7.txt", "8687bd7725b570baeb72d4d666a52c6b9fcf20204a6c4a036c21c672c9338a4d"),
    "h11_direct_oracle": (ROOT / "proof/check_cycle_6_direct_oracle.py", "25390dfab957f38544d98575391ebceba8b2495d934d6cc114f6d0f170725f1b"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "regression_test": (ROOT / "tests/test_cycle_7_lrc_direct_feasibility.py", "031ec2bbe172033a97cd364e1667ab69afd67d23b27dead3f206e7dcf43517b2"),
}


def summary(path: str) -> dict[str, int]:
    return {key: int(value) for key, value in re.findall(r"(\w+)=(\d+)", (ROOT / path).read_text())}


def payload() -> dict:
    runtime = check_runtime("Cycle 7 direct feasibility")
    frozen = freeze_inputs(ROOT, INPUTS)
    first = summary("discovery/out/cycle7-direct-strata.txt")
    replay = summary("discovery/out/cycle7-direct-strata-replay.txt")
    k6 = summary("discovery/out/cycle7-k6.result")
    k7 = summary("discovery/out/cycle7-k7.result")
    compiler = subprocess.run(["g++", "--version"], check=True, capture_output=True, text=True).stdout.splitlines()[0]
    return {
        "artifact_id": "cycle-7-b007-lrc-direct-feasibility-v1", "budget_ordinal": "B007", "cycle": 7,
        "record_type": "PERFORMANCE_GATE", "recorded_at_utc": "2026-08-03T16:22:00Z", "status": "SEALED", "epistemic_status": "OBSERVED",
        "outcome": "The exact direct FEAS implementation is sound on frozen controls but fails the preregistered full-frontier performance gate; no full frontier was run.",
        "claim_boundary": "This is a host-specific bounded benchmark of one implementation. It does not prove a lower bound for direct feasibility, rule out another representation or batching strategy, or make any LRC claim.",
        "controls": {"h11_direct_oracle_rows": 96, "k6_tuples": k6["canonical_solutions"], "k7_tuples": k7["canonical_solutions"], "k6_direct_prunes": k6["direct_prunes"], "k7_direct_prunes": k7["direct_prunes"], "tuple_comparison": "BYTE_IDENTICAL_TO_CYCLE_4"},
        "performance_gate": {"epistemic_status": "OBSERVED", "stratified_rows": replay["rows"], "feasible": replay["feasible"], "infeasible": replay["infeasible"], "caps": replay["cap"], "p99_nanoseconds_first": first["p99_nanoseconds"], "p99_nanoseconds_replay": replay["p99_nanoseconds"], "required_p99_nanoseconds": 100_000, "peak_rss_kib": 1_018_424, "outcome": "FAILED"},
        "companion_decision": {"identity": "/root/decision_companion_2", "adopted": True, "recommendation": "Seal Cycle 7 as a performance-gate failure; open distinct Cycle 8 for fused cover/lifting.", "flaw": "Single-host sample cannot rule out a different exact representation or batching strategy.", "falsifier": "A reproducible bounded exact implementation meeting the frozen p99 gate, or any cache/certificate/tuple defect.", "next_action": "Freeze a lift-compatible fused state space and retained-path invariant."},
        "runtime": {**runtime, "compiler": compiler}, "frozen_hashes": frozen,
        "replay": {"direct_oracle_command": "python3 proof/check_cycle_6_direct_oracle.py", "check_command": "python3 proof/build_cycle_7_lrc_direct_feasibility.py --check", "test_command": "python3 -m unittest tests/test_cycle_7_lrc_direct_feasibility.py -v"},
        "sealer": {"path": "proof/build_cycle_7_lrc_direct_feasibility.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
