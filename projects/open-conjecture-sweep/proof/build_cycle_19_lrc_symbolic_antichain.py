"""Seal Cycle 19's corrected symbolic-antichain performance boundary."""

from __future__ import annotations

import csv
from pathlib import Path

from check_cycle_19_symbolic_antichain import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle19-symbolic-antichain-optimized"
OUTPUT = ROOT / "artifacts/cycle-19-b019-lrc-symbolic-antichain-v1.json"
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-19-b019-lrc-symbolic-antichain-preregistration-v1.md", "56eab6a6107c0048194206763d59dcb6e18e3b7e3f322c8317ee1b6477c46ef1"),
    "prior_artifact": (ROOT / "artifacts/cycle-18-b018-lrc-pair-choice-v1.json", "fdf45cf4e3814d4ebe7d86a5149914f86ac4f1d21d7e5df2088397935e0988e0"),
    "soundness": (ROOT / "proof/cycle_19_symbolic_antichain_soundness.md", "4087f8425de584d9544e756615043a5ede3a2768fc30a95c913a3265b6b8f28f"),
    "executed_source": (ROOT / "discovery/lrc_symbolic_antichain.cpp", "5bc734ee42d0a23b3e019c000f98e7b9296845e0ef724370cbc3b40da2c608da"),
    "executed_binary": (ROOT / "discovery/out/cycle19-symbolic-antichain/lrc_symbolic_antichain_optimized", "6cc9724993d80a2db80e33b8dab4d61c8d2ab96f798e06330f36901231f01a27"),
    "normalizer": (ROOT / "discovery/normalize_cycle_19_results.py", "2d5a824a8f4803eab3dbb0e5bbd23f9a1a53458d953f04dcc584f1e6f733cdab"),
    "audit": (ROOT / "proof/check_cycle_19_symbolic_antichain.py", "0f320e3b51ceb2af6e96b1142b9740e8382b03b34f4dd63bc5e6cf092a786fd7"),
    "test": (ROOT / "tests/test_cycle_19_symbolic_antichain.py", "49b63d882c190ddde1e391cb47651921fb9ed1daafd0c70fa69ecfa16e37b3a0"),
    "raw_results": (OUT / "results.tsv", "6f589562167b67ff3295e6fe5602b6f7b055d9773685915af3fb119035bbc0a1"),
    "corrected_results": (OUT / "results-corrected.tsv", "d51825b2d0f7a66394810b7600878fdcc3f72da8acbc41b47c924c6cb6a0b678"),
    "raw_summary": (OUT / "result.txt", "c7bf7d195836c507e5d433e8478a6cf17c3a0765aa346c2ad18beb0247f55062"),
    "corrected_summary": (OUT / "result-corrected.txt", "5ec64a24b51faf97cdcce2e14693ab759650d5e422e8b2affe6e6e4c21ecdc32"),
    "timing": (OUT / "run.time", "3198669a6b602c4b9b4f3fa7445451f058183c2a5e1139e1d56418af5cc1f667"),
    "cycle18_results": (ROOT / "discovery/out/cycle18-pair-choice/results.tsv", "7317d2285b0db951e8fffda50aab031c4c80a24c2ffdf863bd2052705057507c"),
    "cycle17_lp": (ROOT / "discovery/out/cycle17-time-deficit/lp-results.tsv", "da5f5f926d317e07e662002ac722e2422f22beb47f15e4b55815be98540f935e"),
    "base4_cnf": (ROOT / "discovery/out/cycle11-certified-sat/p199/004.cnf", "ea4356bd1ff5cdf06fb5504411d0ca57ddc8b3056dc8281c8025d1d24ef60648"),
    "base3_cnf": (ROOT / "discovery/out/cycle11-certified-sat/p199/003.cnf", "e07cde8b14f19bf2094e2643ac43c6aad6c6d62ade399db270968a479d0ee6c4"),
    "sample_bases": (ROOT / "discovery/out/cycle8-p199-strata.txt", "327334cf85b821a77b254420d0617c8771a9f272cf38b2512ab79c937de4299b"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
}


def corrected_rows() -> list[dict[str, str]]:
    with (OUT / "results-corrected.tsv").open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def payload() -> dict:
    runtime = check_runtime("Cycle 19 symbolic antichain")
    frozen = freeze_inputs(ROOT, INPUTS)
    summary = audit()
    rows = corrected_rows()
    partial = [row for row in rows if int(row["generated_children"]) > 0]
    return {
        "artifact_id": "cycle-19-b019-lrc-symbolic-antichain-v1",
        "budget_ordinal": "B019",
        "cycle": 19,
        "record_type": "METHOD_PERFORMANCE_BOUNDARY",
        "recorded_at_utc": "2026-08-03T23:28:40Z",
        "status": "SEALED",
        "epistemic_status": "OBSERVED",
        "outcome": "The exact symbolic-antichain theorem is proved, but the frozen optimized experiment certified no leaf and produced no full-cover candidate. All 76 rows are aggregate-wall CAP: three rows partially executed before the 3,500-second internal deadline and 73 were then retained without execution. This is a performance boundary only.",
        "claim_boundary": "The run provides no mathematical efficacy or no-go claim for symbolic antichains, no leaf exclusion, no full-cover witness, no complete base, and no implication for F_1, J, or LRC(13). The partial frontiers are OBSERVED implementation traces. The three raw 'frontier-state cap' labels were deadline-sentinel bookkeeping errors and are superseded by the corrected table.",
        "antichain_theorem": {
            "epistemic_status": "PROVED",
            "statement": "Replacing a coverage-mask family by its inclusion-maximal antichain preserves existence of a full-covering completion; exact left/right complement containment is equivalent to a 13-coordinate full cover.",
        },
        "corrected_run": {
            "epistemic_status": "OBSERVED",
            "rows": summary["rows"],
            "aggregate_wall_caps": summary["aggregate_wall_caps"],
            "partially_executed_rows": summary["partially_executed_rows"],
            "unstarted_after_deadline": 73,
            "certified_no_cover": summary["certified"],
            "full_cover_candidates": summary["candidates"],
            "persistent_frontier_bytes": 0,
            "partial_rows": [
                {
                    "base_index": int(row["base_index"]),
                    "leaf_ordinal": int(row["leaf_ordinal"]),
                    "left_counts": row["left_counts"],
                    "right_counts": row["right_counts"],
                    "generated_children": int(row["generated_children"]),
                    "seconds": float(row["seconds"]),
                    "corrected_detail": row["detail"],
                }
                for row in partial
            ],
        },
        "correction": {
            "epistemic_status": "PROVED",
            "affected_rows": summary["sentinel_label_corrections"],
            "cause": "The in-loop deadline returned a vector of size STATE_CAP+1 as a sentinel; the caller labeled every oversize return as a frontier-state cap.",
            "scope": "Only three cap-detail labels; counts, hashes, elapsed times, target rows, and all mathematical boundaries are unchanged.",
            "resolution": "Preserve raw output and deterministically derive results-corrected.tsv; the audit requires the three elapsed times to exceed 3,500 seconds.",
        },
        "binary_reproduction": {
            "epistemic_status": "PROVED",
            "compiler": "g++ 13.3.0 -O3 -march=native -std=c++20 -pthread",
            "result": "A fresh compile of executed_source was byte-identical to executed_binary.",
            "sha256": "6cc9724993d80a2db80e33b8dab4d61c8d2ab96f798e06330f36901231f01a27",
        },
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "scope_review": "The theorem is proved, but the experiment is only an aggregate-wall failure; 73 rows never started and no efficacy/no-go conclusion is available.",
            "recommendation": "Correct and seal Cycle 19, then open a distinct narrow CRT interface test rather than expand this resource shape.",
            "strongest_flaw": "The run does not distinguish an intrinsically weak representation from avoidable scheduling or implementation cost.",
            "falsifier": "Any mismatch in corrected timestamps/counters, antichain theorem counterexample, or branch-state reconstruction error invalidates the affected statement.",
            "independent_ideas": ["exact CRT bad-time-interface equivalence test", "fractional-primal integrality-gap conflict invariant", "later Problem-1 saturation decision"],
            "next_action": "Open Cycle 20: exact CRT interface test on complete controls and one frozen p199 leaf; one disagreement kills the factorized state space.",
        },
        "resources": {
            "canonical_wall_seconds": 3509.99,
            "aggregate_wall_cap_seconds": 3600,
            "peak_rss_kib": 3866092,
            "output_corpus_bytes": 23641,
            "persistent_frontier_bytes": 0,
            "temporary_disk_cap_bytes": 21474836480,
            "optimized_worker_threads": 3,
            "optimized_worker_cpus": [0, 1],
            "superseded_tranche_cpu": 2,
            "reserved_cpu": 3,
        },
        "runtime": runtime,
        "frozen_hashes": frozen,
        "replay": {
            "compile_command": "g++ -O3 -march=native -std=c++20 -pthread discovery/lrc_symbolic_antichain.cpp -o discovery/out/cycle19-symbolic-antichain/lrc_symbolic_antichain_optimized",
            "run_command": "taskset -c 0-2 /usr/bin/time -v -o discovery/out/cycle19-symbolic-antichain-optimized/run.time discovery/out/cycle19-symbolic-antichain/lrc_symbolic_antichain_optimized discovery/out/cycle8-p199-strata.txt discovery/out/cycle11-certified-sat/p199/004.cnf discovery/out/cycle11-certified-sat/p199/003.cnf discovery/out/cycle18-pair-choice/results.tsv discovery/out/cycle17-time-deficit/lp-results.tsv discovery/out/cycle19-symbolic-antichain-optimized",
            "normalize_command": "python3 discovery/normalize_cycle_19_results.py",
            "audit_command": "python3 proof/check_cycle_19_symbolic_antichain.py",
            "check_command": "python3 proof/build_cycle_19_lrc_symbolic_antichain.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_19_symbolic_antichain.py -v",
        },
        "sealer": {"path": "proof/build_cycle_19_lrc_symbolic_antichain.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
