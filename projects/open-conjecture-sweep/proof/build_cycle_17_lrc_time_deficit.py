"""Seal Cycle 17's exact weighted time-deficit leaf exclusions."""

from __future__ import annotations

import csv
from pathlib import Path

from check_cycle_17_time_deficit import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle17-time-deficit"
OUTPUT = ROOT / "artifacts/cycle-17-b017-lrc-time-deficit-v1.json"
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-17-b017-lrc-time-deficit-preregistration-v1.md", "59f63187ac44572fb851d7d9c657b197d989df1d78187aa56e330e4bc4e98d36"),
    "prior_artifact": (ROOT / "artifacts/cycle-16-b016-lrc-gcd-witness-tree-v1.json", "3d283b68eda692a8dbf4c6efced493eacddab7109d7ae80c98ddf5e002628eb0"),
    "soundness": (ROOT / "proof/cycle_17_time_deficit_soundness.md", "1aeb54d9bbdc18487e95d19fbc29067a97d307b694cd5c5ba2392acfbc035d25"),
    "bounded_engine": (ROOT / "discovery/lrc_time_deficit.cpp", "e2d47f3a83ee4307c84137b5c03a4cd6b12014f1e605e5f9ae8b3ba7bebf30f8"),
    "lp_engine": (ROOT / "discovery/lrc_time_deficit_lp.py", "53076f50a40d8ba6bfc080725026ac8a09bbd08f6afe7bb5c6eee0ee75935a34"),
    "audit": (ROOT / "proof/check_cycle_17_time_deficit.py", "aa6971c671ccf3475242cd25bdbf5f867beb368aee0568836dce6872b0225161"),
    "test": (ROOT / "tests/test_cycle_17_time_deficit.py", "2e08a2f72bc75ffd86a82fbdc499afae61d64724f6793b22135d456440760fbd"),
    "requirements": (ROOT / "requirements-cycle17.txt", "ff5d0c36b5024e0b76b1eb815d52ff00cee3ab78523f3419b5006f728b02b7a4"),
    "base4_cnf": (ROOT / "discovery/out/cycle11-certified-sat/p199/004.cnf", "ea4356bd1ff5cdf06fb5504411d0ca57ddc8b3056dc8281c8025d1d24ef60648"),
    "base3_cnf": (ROOT / "discovery/out/cycle11-certified-sat/p199/003.cnf", "e07cde8b14f19bf2094e2643ac43c6aad6c6d62ade399db270968a479d0ee6c4"),
    "base7_cnf": (ROOT / "discovery/out/cycle11-certified-sat/p199/007.cnf", "cf88a2052e99b310304583294fb7d5db3f5a4fff9213f3f5428c18d60ef31ce9"),
    "sample_bases": (ROOT / "discovery/out/cycle8-p199-strata.txt", "327334cf85b821a77b254420d0617c8771a9f272cf38b2512ab79c937de4299b"),
    "bounded_results": (OUT / "results.tsv", "0e3fcf08b7c168b1abef2307574e0f2896853f6691a924f1b14ef64c0c41f06e"),
    "lp_results": (OUT / "lp-results.tsv", "da5f5f926d317e07e662002ac722e2422f22beb47f15e4b55815be98540f935e"),
    "lp_result": (OUT / "lp.result", "91694c7cac93297a35017817fd8238d5e3ad26dc8de1fd9cb7105fc9adf03ab5"),
    "bounded_timing": (OUT / "run.time", "380ba7b31347acf10755aa9d0076f343115c35e35324a9527944a79c1c177fc6"),
    "lp_timing": (OUT / "lp.time", "1f657f7a4d44e1a3a4b403e3b2a92dc02801b3d8cdbc962d0f768b78819f9ae4"),
    "audit_timing": (OUT / "audit-full.time", "0d29b0be1f34b8467526e2397aa8f7efa98f1551b1fc5c4c265c926d247a960f"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
}


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def payload() -> dict:
    runtime = check_runtime("Cycle 17 time deficit")
    frozen = freeze_inputs(ROOT, INPUTS)
    summary = audit()
    bounded = rows(OUT / "results.tsv")
    lp = rows(OUT / "lp-results.tsv")
    bounded_supports = {}
    for row in bounded:
        if row["status"] == "CERTIFIED_DEFICIT":
            key = f"base{row['base_index']}_support{len(row['source_clauses'].split(','))}"
            bounded_supports[key] = bounded_supports.get(key, 0) + 1
    lp_supports = [int(row["support"]) for row in lp if row["status"] == "CERTIFIED_DEFICIT"]
    return {
        "artifact_id": "cycle-17-b017-lrc-time-deficit-v1",
        "budget_ordinal": "B017",
        "cycle": 17,
        "record_type": "CERTIFIED_FINITE_RESULT",
        "recorded_at_utc": "2026-08-03T21:43:52Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "The weighted time-deficit inequality is exact. Independently reconstructed bounded-grammar certificates exclude 5,908 of 6,084 canonical leaves for frozen base 4 and 5,783 of 6,084 for frozen base 3. Full-signature LP proposals yielded 397 further integerized inequalities, all independently checked exactly. In total exactly 6,044 named leaves per base, 12,088 leaves total, are excluded. Forty leaves per base remain unresolved, so neither base is closed by this family.",
        "claim_boundary": "Only the 12,088 named base/leaf residuals with stored exact U<W certificates are proved UNSAT by this family. The 80 floating LP optima reported as one are OBSERVED and do not prove dual optimality or saturation. No complete new base, F_1 emptiness, J(13,199) emptiness, or LRC(13) follows.",
        "certificate_theorem": {
            "epistemic_status": "PROVED",
            "statement": "For nonnegative integer time weights, any full cover has W <= sum_i max_{allowed d} weighted_bad_count(i,d) = U; therefore U<W certifies the leaf UNSAT.",
            "positive_control": "PASS: base 7 leaf 74 has a singleton U=0<W=1 certificate",
        },
        "bounded_grammar": {
            "epistemic_status": "PROVED",
            "base4_certified": summary["base4_certified"],
            "base3_certified": summary["base3_certified"],
            "total_certified": summary["base4_certified"] + summary["base3_certified"],
            "support_distribution": bounded_supports,
        },
        "full_signature_lp_proposals": {
            "exact_promoted_epistemic_status": "PROVED",
            "floating_failure_epistemic_status": "OBSERVED",
            "rows": 477,
            "exact_integerized_certificates": summary["lp_certified"],
            "minimum_support": min(lp_supports),
            "maximum_support": max(lp_supports),
            "floating_no_deficit_rows": summary["no_lp_rows_observed"],
        },
        "combined_result": {
            "epistemic_status": "PROVED",
            "base4_certified": 6044,
            "base4_unresolved": summary["post_lp_base4_uncovered"],
            "base3_certified": 6044,
            "base3_unresolved": summary["post_lp_base3_uncovered"],
            "total_named_leaf_exclusions": 12088,
            "complete_bases": 0,
        },
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "scope_review": "The exact inequalities prove 6,044 named leaves per base; the forty survivors per base remain unresolved and numerical LP optima are not exact saturation certificates.",
            "recommendation": "Seal Cycle 17; a coupled pair-choice state space is materially new and belongs in Cycle 18.",
            "strongest_flaw": "The 38-ordinal overlap may be an indexing artifact rather than a shared semantic obstruction, and the two base-dependent exceptions matter.",
            "falsifier": "Any base/leaf mapping error or independently recomputed stored inequality with U>=W invalidates the affected exclusion.",
            "independent_ideas": ["conditional pair-choice Hall lift", "symbolic case split on the first seven coordinates", "CRT fallback"],
            "next_action": "Open Cycle 18: branch on the localized survivor pattern and use disjoint two-coordinate option groups with exact integer weights, explicitly covering the two exceptions.",
        },
        "resources": {
            "aggregate_wall_seconds": 15.92,
            "aggregate_wall_cap_seconds": 3600,
            "peak_rss_kib": 80388,
            "output_corpus_bytes": 971866,
            "dependency_environment_bytes": 235737075,
            "temporary_disk_cap_bytes": 21474836480,
            "worker_cpus": [0, 1, 2],
            "reserved_cpu": 3,
            "compiler": "g++ 13.3.0 -O3 -march=native -std=c++20 -pthread",
            "lp_runtime": "CPython 3.12.3, numpy 2.2.6, scipy 1.14.1",
        },
        "runtime": runtime,
        "frozen_hashes": frozen,
        "replay": {
            "compile_command": "g++ -O3 -march=native -std=c++20 -pthread discovery/lrc_time_deficit.cpp -o discovery/out/cycle17-time-deficit/lrc_time_deficit",
            "bounded_command": "taskset -c 0-2 discovery/out/cycle17-time-deficit/lrc_time_deficit discovery/out/cycle8-p199-strata.txt discovery/out/cycle11-certified-sat/p199/004.cnf discovery/out/cycle11-certified-sat/p199/003.cnf discovery/out/cycle11-certified-sat/p199/007.cnf discovery/out/cycle17-time-deficit/results.tsv",
            "lp_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_time_deficit_lp.py",
            "audit_command": "python3 proof/check_cycle_17_time_deficit.py",
            "check_command": "python3 proof/build_cycle_17_lrc_time_deficit.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_17_time_deficit.py -v",
        },
        "sealer": {"path": "proof/build_cycle_17_lrc_time_deficit.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
