"""Correct Cycle 4 to include its 128-GiB continuation and final edge gate."""

from __future__ import annotations
import re
from pathlib import Path
import subprocess
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-4-b004-lrc-partitioned-v2.json"
INPUTS = {
    "superseded_v1": (ROOT / "artifacts/cycle-4-b004-lrc-partitioned-v1.json", "685b8d82f4c25ca969d9a7f1ccf42ee4249cb08b6e9a8f3de25e896d9d54c444"),
    "continuation_execution_freeze": (ROOT / "discovery/cycle4-128g-execution-freeze.md", "226c997933f2daf44b4424ad04425116bab5c19393d355cf1016f3eaba7291b8"),
    "continuation_runner": (ROOT / "proof/run_cycle_4_frontier_128g.sh", "e2e83ffeb5ee687ea1646901b24a414ef58b5ccc0daa928a5969c85454ce62e3"),
    "continuation_result": (ROOT / "discovery/out/partitioned-k13-p199-128g.result", "946a6f060e2285ef90b6d3919fc7f24917df0b25fa5cbbe8695d2ad099580493"),
    "continuation_timing": (ROOT / "discovery/out/partitioned-k13-p199-128g.time", "104a0d7ee1c334f9cabe28c6bccc9098ecc4f2ab5dcf30bffb7f3cb1c82b0a26"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "regression_test": (ROOT / "tests/test_cycle_4_lrc_partitioned_v2.py", "e91c9ddda906077d27680692048d531b7dbd7d1247bb66d93aab351480fc5589"),
}

def metric(pattern: str, text: str, cast=int):
    match = re.search(pattern, text)
    if not match:
        raise RuntimeError(f"missing metric: {pattern}")
    return cast(match.group(1))

def payload() -> dict:
    runtime = check_runtime("Cycle 4 correction")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = (ROOT / "discovery/out/partitioned-k13-p199-128g.result").read_text()
    timing = (ROOT / "discovery/out/partitioned-k13-p199-128g.time").read_text()
    compiler = subprocess.run(["g++", "--version"], check=True, capture_output=True, text=True).stdout.splitlines()[0]
    return {
        "artifact_id": "cycle-4-b004-lrc-partitioned-v2", "budget_ordinal": "B004", "cycle": 4,
        "record_type": "CORRECTION", "recorded_at_utc": "2026-08-03T14:56:54Z", "status": "SEALED", "epistemic_status": "OBSERVED",
        "supersedes": "cycle-4-b004-lrc-partitioned-v1",
        "correction": {
            "error": "Cycle 4 was sealed after its intermediate 64-GiB tranche and the identical 128-GiB continuation was initially misnumbered as a new cycle.",
            "cause": "A resource-cap continuation was mistaken for a new research question despite the unchanged engine and decision block.",
            "affected_claim": "The v1 logical-disk-cap outcome is valid for its tranche but is not the final Cycle-4 strategic boundary.",
            "resolution": "Preserve v1 immutably, count no B005 cycle, and supersede the intermediate conclusion with the combined-tranche edge-cap outcome.",
        },
        "claim_boundary": "The exact 64-partition coverage engine passed the 64-GiB intermediate tranche, completed depth 9 under the 128-GiB continuation, and then breached the unchanged generated-edge cap before reaching a leaf. This is an algorithmic performance boundary only; it proves no J-empty claim, LRC(13), or asymptotic obstruction.",
        "frontier_gate": {
            "epistemic_status": "OBSERVED", "outcome": "FAILED_EDGE_CAP",
            "completed_depth": metric(r"completed_depth=(\d+)", result),
            "depth_9_states": metric(r"level=9 states=(\d+)", timing),
            "expanded_states": metric(r"expanded_states=(\d+)", result),
            "generated_edges": metric(r"generated_edges=(\d+)", result),
            "edge_cap": 5_869_850_724, "bounded_parallel_overshoot": metric(r"generated_edges=(\d+)", result) - 5_869_850_724,
            "leaf_states": metric(r"leaf_states=(\d+)", result),
            "peak_logical_disk_bytes": metric(r"peak_disk_bytes=(\d+)", result),
            "peak_rss_kib": metric(r"Maximum resident set size \(kbytes\): (\d+)", timing),
            "wall_seconds_internal": metric(r"wall_seconds=([0-9.]+)", result, float),
            "wall_seconds_external": 24 * 60 + 3.56,
            "filesystem_before_available_bytes": metric(r"filesystem_before_bytes=\d+ \d+ (\d+)", timing),
            "filesystem_after_cleanup_available_bytes": metric(r"filesystem_after_cleanup_bytes=\d+ \d+ (\d+)", timing),
            "cleanup_removed_entries": metric(r"cleanup_removed_entries=(\d+)", result),
        },
        "companion_decision": {
            "identity": "/root/decision_companion_2", "adopted": True,
            "recommendation": "Close the combined Cycle-4 storage-engine block at the edge cap; the next distinct cycle tests a pre-emission invariant.",
            "falsifier": "A baseline tuple/level mismatch, partition-integrity failure, non-edge-counter stop, or materially different strict-cap frontier.",
            "next_action": "Open the next cycle only for the distinct question of a proved orbit-invariant dominance/completion cut; keep fused cover/lifting as fallback.",
        },
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "A sound pre-emission dominance/completion invariant might avoid generating most of the depth-10 frontier while retaining every cover orbit."},
        "runtime": {**runtime, "compiler": compiler}, "frozen_hashes": frozen,
        "replay": {"check_command": "python3 proof/build_cycle_4_lrc_partitioned_v2.py --check", "test_command": "python3 -m unittest tests/test_cycle_4_lrc_partitioned_v2.py -v", "frontier_command": "/usr/bin/time -v sh proof/run_cycle_4_frontier_128g.sh > discovery/out/partitioned-k13-p199-128g.result 2> discovery/out/partitioned-k13-p199-128g.time"},
        "sealer": {"path": "proof/build_cycle_4_lrc_partitioned_v2.py", "sha256": sha256(Path(__file__))},
    }

if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
