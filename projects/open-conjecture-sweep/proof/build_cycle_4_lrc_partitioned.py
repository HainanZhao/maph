"""Build the immutable Cycle-4 partitioned-search boundary record."""

from __future__ import annotations
import re
from pathlib import Path
import subprocess
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-4-b004-lrc-partitioned-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-4-b004-lrc-disk-partition-preregistration-v1.md", "692e2d5bb11d2f82cab4b72225a4e011c00e135d24764302a61ce491ef1437f1"),
    "partition_argument": (ROOT / "proof/cycle_4_partition_exactness_argument.md", "cde68555f2847c6b1b60da27170bc92d7ef84607ea4d735209c34bb44bf31479"),
    "partition_engine": (ROOT / "discovery/lrc_coverage_partitioned.cpp", "2e2ccebba549ec194df2f6d2c63dc3815701077645fd46cb3dc5034bc3b7736b"),
    "tiny_tuples": (ROOT / "discovery/out/partitioned-tiny.txt", "1def07dbe06eeb097aafec8a40329937cd20c93a83634b8221ea2b41a894310c"),
    "tiny_result": (ROOT / "discovery/out/partitioned-tiny.result", "48fb8baa585446179d1a9734315df299f49e4360c473d5fba748530173bad4fa"),
    "k6_tuples": (ROOT / "discovery/out/partitioned-k6.txt", "3282243c9bd46b7cf0cb2f57a60fcf75d01df5f3ffdd11fe0ad91f8713170e03"),
    "k6_result": (ROOT / "discovery/out/partitioned-k6.result", "a3d71226e0e7d7369f44063a6f277ec7008a0d419a07ecd136890f87700b4e7b"),
    "k6_levels": (ROOT / "discovery/out/partitioned-k6.levels", "2639fb05c967da8f12741dfdccdd0d7f48867f853c076c7daedbd5e9aa36609b"),
    "k7_tuples": (ROOT / "discovery/out/partitioned-k7.txt", "8687bd7725b570baeb72d4d666a52c6b9fcf20204a6c4a036c21c672c9338a4d"),
    "k7_result": (ROOT / "discovery/out/partitioned-k7.result", "4f22517cfcb74f57a476d4f6885669159d9aa8d7f87b5f86d8ed7a4f66a1e391"),
    "k7_levels": (ROOT / "discovery/out/partitioned-k7.levels", "1895b2c652873a07556553f0c21039685b01642e0b8981f91d885f858caf6c5f"),
    "frontier_runner": (ROOT / "proof/run_cycle_4_frontier.sh", "116aebf6aad5d04e00d8d56386101063aa02138965018e4ecc6c8bc227591dac"),
    "frontier_result": (ROOT / "discovery/out/partitioned-k13-p199.result", "33009bbf7aba733a0c4e01a431e9a45e027fb1ccb2a7e430ce3b29204532b28e"),
    "frontier_timing": (ROOT / "discovery/out/partitioned-k13-p199.time", "6efc8ec5b717ac4ab56faf51a2a0d1dd4992c30eef5ca3e66b33c970b910f185"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "regression_test": (ROOT / "tests/test_cycle_4_lrc_partitioned.py", "d7f9ba1621265c7e9d2aee872f193e42b86c16c86f3984dbecd9f58364a0d469"),
    "validator": (ROOT / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}

def metric(pattern: str, text: str, cast=int):
    match = re.search(pattern, text)
    if not match:
        raise RuntimeError(f"missing metric: {pattern}")
    return cast(match.group(1))

def payload() -> dict:
    runtime = check_runtime("Cycle 4")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = (ROOT / "discovery/out/partitioned-k13-p199.result").read_text()
    timing = (ROOT / "discovery/out/partitioned-k13-p199.time").read_text()
    k6 = (ROOT / "discovery/out/partitioned-k6.result").read_text()
    k7 = (ROOT / "discovery/out/partitioned-k7.result").read_text()
    tiny = subprocess.run(["python3", "discovery/check_lrc_ansatz.py", "--k", "3", "--p", "11", "--tuples", "discovery/out/partitioned-tiny.txt", "--brute-force"], cwd=ROOT, check=True, capture_output=True, text=True)
    compiler = subprocess.run(["g++", "--version"], check=True, capture_output=True, text=True).stdout.splitlines()[0]
    return {
        "artifact_id": "cycle-4-b004-lrc-partitioned-v1", "budget_ordinal": "B004", "cycle": 4,
        "recorded_at_utc": "2026-08-03T14:28:37Z", "status": "SEALED", "epistemic_status": "OBSERVED",
        "claim_boundary": "The 64-partition external engine exactly reproduced the tiny oracle, both frozen p=47 tuple sets, and their level sequences. At k=13,p=199 it passed the prior memory barrier and then stopped at its configured 64-GiB logical serialized-live-byte cap while expanding depth 9. This is an algorithmic storage result, not a physical-filesystem exhaustion claim or an LRC/J-empty result.",
        "baseline_validation": {"epistemic_status": "OBSERVED", "tiny_oracle": tiny.stdout.strip().splitlines(), "counts": {"k6_p47": metric(r"canonical_solutions=(\d+)", k6), "k7_p47": metric(r"canonical_solutions=(\d+)", k7)}, "tuple_and_level_equality": True},
        "frontier_gate": {"epistemic_status": "OBSERVED", "outcome": "FAILED_LOGICAL_DISK_CAP", "completed_depth": metric(r"completed_depth=(\d+)", result), "expanded_states": metric(r"expanded_states=(\d+)", result), "generated_edges": metric(r"generated_edges=(\d+)", result), "leaf_states": metric(r"leaf_states=(\d+)", result), "peak_logical_disk_bytes": metric(r"peak_disk_bytes=(\d+)", result), "wall_seconds": metric(r"wall_seconds=([0-9.]+)", result, float), "peak_rss_kib": metric(r"Maximum resident set size \(kbytes\): (\d+)", timing), "cleanup_removed_entries": metric(r"cleanup_removed_entries=(\d+)", result)},
        "companion_decision": {"identity": "/root/decision_companion_2", "adopted": True, "recommendation": "Seal Cycle 4 and open Cycle 5 changing only the disk tranche to 128 GiB.", "next_action": "Retain engine, serialization, 64 partitions, and all non-disk caps; log logical and filesystem storage observations."},
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "The same exact engine may progress farther under the user-authorized 128-GiB disk tranche."},
        "runtime": {**runtime, "compiler": compiler}, "frozen_hashes": frozen,
        "replay": {"check_command": "python3 proof/build_cycle_4_lrc_partitioned.py --check", "test_command": "python3 -m unittest tests/test_cycle_4_lrc_partitioned.py -v", "frontier_command": "/usr/bin/time -v sh proof/run_cycle_4_frontier.sh > discovery/out/partitioned-k13-p199.result 2> discovery/out/partitioned-k13-p199.time"},
        "sealer": {"path": "proof/build_cycle_4_lrc_partitioned.py", "sha256": sha256(Path(__file__))},
    }

if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
