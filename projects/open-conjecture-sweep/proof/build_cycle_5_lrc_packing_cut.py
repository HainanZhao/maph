"""Seal Cycle 5's exact pairwise-packing structural no-go and frontier replay."""

from __future__ import annotations

import json
import re
from pathlib import Path
import subprocess

from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-5-b005-lrc-packing-cut-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-5-b005-lrc-packing-cut-preregistration-v1.md", "54ba0f84e1595c4e95619e511a5f35fb51bf64dfe158b7fd1e2981773a84929c"),
    "soundness_argument": (ROOT / "proof/cycle_5_packing_soundness_argument.md", "85d609f69080ffeaf2fd8b9ec65b826c53b8e54aacd024a606942b5193baf2c9"),
    "engine": (ROOT / "discovery/lrc_coverage_packing.cpp", "77d82ab2dafd5dfb4c54749fd376b38ea04c7f3785e5422f7c18c91c8a57baef"),
    "small_oracle": (ROOT / "discovery/check_lrc_packing.py", "b0dd3d97964675b025f6c8393be62f268dedd2f28013e19845dda1243ba73eb0"),
    "small_oracle_table": (ROOT / "discovery/out/packing-h11.table", "ad42b05410f326420aee38b3e395ea69af98bf166a19e990b3485f914af60a34"),
    "tiny_result": (ROOT / "discovery/out/packing-tiny.result", "5f0705f279132f1273adb710f2a69d8d9c2b8f8f330d93c590cb4fbee579cb3c"),
    "packing_k6_tuples": (ROOT / "discovery/out/packing-k6.txt", "3282243c9bd46b7cf0cb2f57a60fcf75d01df5f3ffdd11fe0ad91f8713170e03"),
    "cycle4_k6_tuples": (ROOT / "discovery/out/partitioned-k6.txt", "3282243c9bd46b7cf0cb2f57a60fcf75d01df5f3ffdd11fe0ad91f8713170e03"),
    "packing_k7_tuples": (ROOT / "discovery/out/packing-k7.txt", "8687bd7725b570baeb72d4d666a52c6b9fcf20204a6c4a036c21c672c9338a4d"),
    "cycle4_k7_tuples": (ROOT / "discovery/out/partitioned-k7.txt", "8687bd7725b570baeb72d4d666a52c6b9fcf20204a6c4a036c21c672c9338a4d"),
    "relation_checker": (ROOT / "proof/check_cycle_5_packing_relation.py", "caa894a97405f8056f8b4b3032fa60169e0f1c3cc45ea2f6aa9f0e52d5cd485e"),
    "relation_result": (ROOT / "discovery/out/packing-relation-check.json", "56bab70904acefa0a815ac2a8dba5741ece70e22bca6439e9e5b64a410edaab3"),
    "frontier_runner": (ROOT / "proof/run_cycle_5_frontier.sh", "ba3dc6b4b5ab2b128d8834b9e6b5486fed7c01149488dc872ca1cf3630dff729"),
    "frontier_result": (ROOT / "discovery/out/packing-k13-p199.result", "d8c52250e9b6972902b2a6e5cc16f1f1535030c60c65656cfa45272ce7a07d21"),
    "frontier_timing": (ROOT / "discovery/out/packing-k13-p199.time", "70d964c2fc555dd6e8c8327dfc8502d443b22ee6d364c180bb0862a8b8754ea5"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "regression_test": (ROOT / "tests/test_cycle_5_lrc_packing_cut.py", "930ac7dbad1e9c91f661ce1faeac54eacf8ef1b4d2a360ca5760ae1753b5afa1"),
}


def metric(pattern: str, text: str, cast=int):
    match = re.search(pattern, text)
    if not match:
        raise RuntimeError(f"missing metric: {pattern}")
    return cast(match.group(1))


def payload() -> dict:
    runtime = check_runtime("Cycle 5 packing cut")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = (ROOT / "discovery/out/packing-k13-p199.result").read_text()
    timing = (ROOT / "discovery/out/packing-k13-p199.time").read_text()
    relation = json.loads((ROOT / "discovery/out/packing-relation-check.json").read_text())
    compiler = subprocess.run(
        ["g++", "--version"], check=True, capture_output=True, text=True
    ).stdout.splitlines()[0]
    return {
        "artifact_id": "cycle-5-b005-lrc-packing-cut-v1",
        "budget_ordinal": "B005",
        "cycle": 5,
        "record_type": "STRUCTURAL_NO_GO",
        "recorded_at_utc": "2026-08-03T15:32:50Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "The frozen pairwise incompatibility/clique cut is vacuous for (13,199): B-B equals all of H_199, so its incompatibility graph has no edges and it cannot prune any state.",
        "claim_boundary": "The no-go applies only to the frozen pairwise difference-set invariant for the specified bad set and quotient conventions. It does not constrain higher-order non-co-cover witnesses, fused cover/lifting, J(13,199), LRC(13), or any asymptotic statement.",
        "structural_no_go": {
            "epistemic_status": "PROVED",
            "dimension": relation["dimension"],
            "prime": relation["prime"],
            "group_order": relation["group_order"],
            "bad_exponents": relation["bad_exponents"],
            "bad_set_size": relation["bad_set_size"],
            "difference_set_size": relation["difference_set_size"],
            "incompatibility_edge_count": relation["incompatibility_edge_count"],
            "implication": "No pairwise incompatibility witness of size at least two exists for any uncovered subset.",
        },
        "controls": {
            "h11_exhaustive_rows": 96,
            "h11_oracle": "PASS",
            "tiny_canonical_solutions": 1,
            "p47_k6_tuple_count": 53,
            "p47_k7_tuple_count": 50,
            "p47_tuple_comparison": "BYTE_IDENTICAL_TO_CYCLE_4",
        },
        "frontier_gate": {
            "epistemic_status": "OBSERVED",
            "outcome": "FAILED_NO_REDUCTION_AND_EDGE_CAP",
            "completed_depth": metric(r"completed_depth=(\d+)", result),
            "depth_9_states": metric(r"level=9 states=(\d+)", timing),
            "expanded_states": metric(r"expanded_states=(\d+)", result),
            "generated_edges": metric(r"generated_edges=(\d+)", result),
            "edge_cap": 5_869_850_724,
            "bounded_parallel_overshoot": metric(r"generated_edges=(\d+)", result) - 5_869_850_724,
            "leaf_states": metric(r"leaf_states=(\d+)", result),
            "packing_checks": metric(r"packing_checks=(\d+)", result),
            "packing_prunes": metric(r"packing_prunes=(\d+)", result),
            "depth_9_edge_reduction_percent": 0.0,
            "peak_logical_disk_bytes": metric(r"peak_disk_bytes=(\d+)", result),
            "peak_rss_kib": metric(r"Maximum resident set size \(kbytes\): (\d+)", timing),
            "wall_seconds_internal": metric(r"wall_seconds=([0-9.]+)", result, float),
            "wall_seconds_external": 23 * 60 + 48.13,
            "runtime_disk_cap_bytes": metric(r"temporary_disk_limit_bytes=(\d+)", timing),
            "filesystem_reserve_bytes": metric(r"filesystem_reserve_bytes=(\d+)", timing),
            "cleanup_removed_entries": metric(r"cleanup_removed_entries=(\d+)", result),
        },
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "adopted": True,
            "recommendation": "Seal Cycle 5 as a structural no-go for the frozen pairwise incompatibility/clique-cut family.",
            "strongest_flaw": "The no-go does not extend to higher-order non-co-cover constraints or fused cover/lifting.",
            "falsifier": "A missing exact difference, a valid rejected pairwise witness, or any nonzero prune from the frozen cut.",
            "next_action": "Open distinct Cycle 6 for a minimally falsifiable three-way non-co-cover hypergraph invariant; if saturated, switch to fused initial-cover construction with lifting.",
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "A higher-order non-co-cover invariant may prune completions even though every pair of times is co-coverable.",
        },
        "runtime": {**runtime, "compiler": compiler},
        "frozen_hashes": frozen,
        "replay": {
            "relation_command": "python3 proof/check_cycle_5_packing_relation.py",
            "oracle_command": "python3 discovery/check_lrc_packing.py discovery/out/packing-h11.table",
            "check_command": "python3 proof/build_cycle_5_lrc_packing_cut.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_5_lrc_packing_cut.py -v",
            "frontier_command": "/usr/bin/time -v sh proof/run_cycle_5_frontier.sh > discovery/out/packing-k13-p199.result 2> discovery/out/packing-k13-p199.time",
        },
        "sealer": {"path": "proof/build_cycle_5_lrc_packing_cut.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
