"""Build the immutable Cycle-3 coverage-level resource-boundary record."""

from __future__ import annotations

import re
from pathlib import Path
import subprocess

from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-3-b003-lrc-coverage-levels-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-3-b003-lrc-coverage-directed-orbits-preregistration-v1.md", "3191dcdff14a84cce2ea94f9afc29681b69fec3db936eab865a567aae4a4dfd2"),
    "retained_path_argument": (ROOT / "proof/cycle_3_coverage_directed_argument.md", "e1091ef0bb6336be4340f30c161f6e2549a0304c4a26ad054de42f077eb3fe52"),
    "exact_level_search": (ROOT / "discovery/lrc_coverage_levels.cpp", "e94f2e62273cb8a23bc18b00345a32c95c0778499b83077bd05579845d86ff2d"),
    "tiny_tuples": (ROOT / "discovery/out/coverage-tiny.txt", "1def07dbe06eeb097aafec8a40329937cd20c93a83634b8221ea2b41a894310c"),
    "tiny_result": (ROOT / "discovery/out/coverage-tiny.result", "a07249709fd5be7bcad645c13f3fa94c41ddff9ee3ffa00ac5e1f1993e3f701c"),
    "baseline_k6_tuples": (ROOT / "discovery/out/coverage-k6.txt", "3282243c9bd46b7cf0cb2f57a60fcf75d01df5f3ffdd11fe0ad91f8713170e03"),
    "baseline_k6_result": (ROOT / "discovery/out/coverage-k6.result", "fc3f409cb3719c157b50a1d387d01071adb24fbf08665663487f11fc701cf26c"),
    "baseline_k7_tuples": (ROOT / "discovery/out/coverage-k7.txt", "8687bd7725b570baeb72d4d666a52c6b9fcf20204a6c4a036c21c672c9338a4d"),
    "baseline_k7_result": (ROOT / "discovery/out/coverage-k7.result", "31acac65bb8416117eccb83c5d5809325677ab872af9baa2cd42dee54a7fb3c3"),
    "frontier_runner": (ROOT / "proof/run_cycle_3_frontier.sh", "ce5b5f1262cdb91302a34f2e8f12c7c6fe4a5bb0d2183c3a8ad12e371ec6ae91"),
    "frontier_timing": (ROOT / "discovery/out/coverage-k13-p199.time", "94c89ac54d805376106083ddbe478f24fabca71ce768a58357c8d2478d927955"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "regression_test": (ROOT / "tests/test_cycle_3_lrc_coverage_levels.py", "1caf5a7f2ad8626558cb64c7034c666061d9c8680c3e68d4ce6e55e123403665"),
    "preregistration_validator": (ROOT / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def metric(pattern: str, text: str, cast=int):
    match = re.search(pattern, text)
    if not match:
        raise RuntimeError(f"missing frozen metric: {pattern}")
    return cast(match.group(1))


def payload() -> dict:
    runtime = check_runtime("Cycle 3")
    frozen = freeze_inputs(ROOT, INPUTS)
    tiny_check = subprocess.run(
        ["python3", "discovery/check_lrc_ansatz.py", "--k", "3", "--p", "11", "--tuples", "discovery/out/coverage-tiny.txt", "--brute-force"],
        cwd=ROOT, check=True, capture_output=True, text=True,
    )
    k6 = (ROOT / "discovery/out/coverage-k6.result").read_text()
    k7 = (ROOT / "discovery/out/coverage-k7.result").read_text()
    timing = (ROOT / "discovery/out/coverage-k13-p199.time").read_text()
    if "std::bad_alloc" not in timing or "Command terminated by signal 6" not in timing:
        raise RuntimeError("frozen frontier log does not record the allocation failure")
    compiler = subprocess.run(["g++", "--version"], check=True, capture_output=True, text=True).stdout.splitlines()[0]
    return {
        "artifact_id": "cycle-3-b003-lrc-coverage-levels-v1",
        "budget_ordinal": "B003",
        "cycle": 3,
        "recorded_at_utc": "2026-08-03T14:06:22Z",
        "status": "SEALED",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "The coverage-directed canonical-level construction has a written retained-path argument and exactly reproduces a naive tiny oracle plus both frozen p=47 tuple sets. Its in-memory k=13,p=199 implementation failed while constructing depth 8 under the logged 8 GiB virtual-memory limit. This is a storage/resource result only; it proves no mathematical obstruction, J-empty claim, or LRC(13).",
        "baseline_validation": {
            "epistemic_status": "OBSERVED",
            "tiny_oracle": tiny_check.stdout.strip().splitlines(),
            "counts": {"k6_p47": metric(r"canonical_solutions=(\d+)", k6), "k7_p47": metric(r"canonical_solutions=(\d+)", k7)},
            "expanded_states": {"k6_p47": metric(r"expanded_states=(\d+)", k6), "k7_p47": metric(r"expanded_states=(\d+)", k7)},
            "tuple_equality": "The frozen output hashes are byte-identical to the Cycle-1 baseline tuple hashes.",
        },
        "frontier_gate": {
            "epistemic_status": "OBSERVED",
            "outcome": "FAILED_MEMORY_CAP",
            "last_completed_depth": metric(r"level=(\d+) states=2982862", timing),
            "depth_7_states": metric(r"level=7 states=(\d+)", timing),
            "expanded_states_through_depth_7": metric(r"level=7 states=\d+ expanded=(\d+)", timing),
            "generated_edges_through_depth_7": metric(r"level=7 states=\d+ expanded=\d+ edges=(\d+)", timing),
            "virtual_memory_limit_kib": metric(r"virtual_memory_limit_kib=(\d+)", timing),
            "peak_rss_kib": metric(r"Maximum resident set size \(kbytes\): (\d+)", timing),
            "wall_seconds": metric(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): 0:([0-9.]+)", timing, float),
            "statement": "Depth 7 completed exactly; allocation failed while materializing/deduplicating the next level under the logged RLIMIT_AS.",
        },
        "structural_diagnosis": {
            "epistemic_status": "OBSERVED",
            "statement": "The in-memory implementation requires simultaneous storage for the current level, worker child buffers, and the merged next level; that representation exceeded the frozen memory budget before depth 8 completed.",
            "falsifier": "A reproducible complete in-memory run of the frozen construction within every Cycle-3 resource cap.",
        },
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "adopted": True,
            "recommendation": "Seal Cycle 3 as an in-memory resource failure and open a distinct storage-engine cycle.",
            "next_action": "Open Cycle 4 for deterministic disk/radix-partitioned canonical deduplication; freeze serialization, partition and merge proof, disk/wall caps, and baseline equality.",
        },
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "External partitioning may preserve the retained-path engine while bounding RAM independently of the next-level frontier width."},
        "runtime": {**runtime, "compiler": compiler, "compile_flags": "-std=c++20 -O3 -march=native -flto -DNDEBUG -pthread"},
        "frozen_hashes": frozen,
        "replay": {
            "check_command": "python3 proof/build_cycle_3_lrc_coverage_levels.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_3_lrc_coverage_levels.py -v",
            "write_command": "python3 proof/build_cycle_3_lrc_coverage_levels.py --write",
            "compile_command": "g++ -std=c++20 -O3 -march=native -flto -DNDEBUG -pthread discovery/lrc_coverage_levels.cpp -o discovery/out/lrc_coverage_levels",
            "frontier_command": "/usr/bin/time -v sh proof/run_cycle_3_frontier.sh > discovery/out/coverage-k13-p199.result 2> discovery/out/coverage-k13-p199.time",
        },
        "sealer": {"path": "proof/build_cycle_3_lrc_coverage_levels.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
