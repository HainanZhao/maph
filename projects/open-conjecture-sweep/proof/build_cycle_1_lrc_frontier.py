"""Build the immutable Cycle-1 Lonely Runner frontier census record."""

from __future__ import annotations

import re
from pathlib import Path
import subprocess

from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-1-b001-lrc-frontier-census-v1.json"
INPUTS = {
    "preregistration": (
        ROOT / "docs/cycle-1-b001-lrc-frontier-preregistration-v1.md",
        "40efa6087803a75169128bd1a48934c938469cf0ef2d42db16d244ad561b97c6",
    ),
    "exact_enumerator": (
        ROOT / "discovery/lrc_ansatz_exact.cpp",
        "6654f3d3ee8c662fdef19b1e07bba3703713afd43b04ba917c7242c885281e62",
    ),
    "independent_rechecker": (
        ROOT / "discovery/check_lrc_ansatz.py",
        "e08356377a8083d74929d061e0a24142b608720cf1bcfd13b26ec2fcbb769c8b",
    ),
    "baseline_k6_tuples": (
        ROOT / "discovery/out/k6-p47.txt",
        "3282243c9bd46b7cf0cb2f57a60fcf75d01df5f3ffdd11fe0ad91f8713170e03",
    ),
    "baseline_k7_tuples": (
        ROOT / "discovery/out/k7-p47.txt",
        "8687bd7725b570baeb72d4d666a52c6b9fcf20204a6c4a036c21c672c9338a4d",
    ),
    "frontier_result": (
        ROOT / "discovery/out/k13-p199.result",
        "9cb6375acf02546509c79eb7ff3d57676ba999b9b0275fd69444a344592d5b44",
    ),
    "frontier_timing": (
        ROOT / "discovery/out/k13-p199.time",
        "d9400663ed01dcc6695a20dfe3cfb5c105436a61d4aa552c2b383965cba049d9",
    ),
    "frontier_recheck_timing": (
        ROOT / "discovery/out/k13-p199-recheck.time",
        "37e3b74cdc470d7075963241ab9d1e057fef7769774312755f30446221ed0b51",
    ),
    "frontier_tuples_gzip": (
        ROOT / "discovery/out/k13-p199.txt.gz",
        "5e3c007e90f9bd6e6f0d87bab126f8eb59e3e021df0d3515893fd2f2747402de",
    ),
    "scaffold": (
        ROOT / "proof/cycle_seal_v1.py",
        "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7",
    ),
    "regression_test": (
        ROOT / "tests/test_cycle_1_lrc_frontier.py",
        "75294f03ffd8ef1f2f25f10315b536f6c30e04e21503b8fd7d46d888dae295bb",
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
    runtime = check_runtime("Cycle 1")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = (ROOT / "discovery/out/k13-p199.result").read_text()
    timing = (ROOT / "discovery/out/k13-p199.time").read_text()
    recheck = subprocess.run(
        [
            "python3", str(ROOT / "discovery/check_lrc_ansatz.py"),
            "--k", "13", "--p", "199",
            "--tuples", str(ROOT / "discovery/out/k13-p199.txt.gz"),
            "--stream-recheck", "--expected-count", "4748938",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    if recheck.stdout.strip() != "stream_rechecked=4748938":
        raise RuntimeError("frontier stream recheck mismatch")
    compiler = subprocess.run(["g++", "--version"], check=True, capture_output=True, text=True).stdout.splitlines()[0]
    return {
        "artifact_id": "cycle-1-b001-lrc-frontier-census-v1",
        "budget_ordinal": "B001",
        "cycle": 1,
        "recorded_at_utc": "2026-08-03T12:49:15Z",
        "status": "SEALED",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "The frozen exact set-cover DFS reproduced two published l=1 ansatz counts and completed a finite census of 4,748,938 emitted canonical representatives for I(13,199,1). Every emitted frontier row was independently checked for representative shape, strict ordering/uniqueness, and exact modular bad-time coverage. Completeness and full orbit minimality at p=199 still rely on the C++ branch partition and canonicalization proof; there is no second exhaustive frontier enumeration. This proves neither J(13,199)=empty nor LRC(13), and the bounded source audit is not a universal openness or novelty claim.",
        "eligibility": {
            "epistemic_status": "OBSERVED",
            "statement": "A primary-source and official-OpenAI bounded audit through 2026-08-03 identifies LRC(13), the 14-total-runner case, as the first eligible finite Lonely Runner target.",
            "primary_boundary": "Sungkawichai--Trakulthongchai, arXiv:2604.23906v1, Theorem 1.3 proves LRC(k) through k=12; Section 7 names I(13,p,1) computation as the next bottleneck.",
        },
        "published_baseline_reproduction": {
            "epistemic_status": "OBSERVED",
            "statement": "The exact DFS and an independent brute-force oracle agree tuple-for-tuple with the frozen published counts.",
            "instances": [
                {"k": 6, "p": 47, "canonical_count": 53},
                {"k": 7, "p": 47, "canonical_count": 50},
            ],
        },
        "frontier_census": {
            "epistemic_status": "OBSERVED",
            "statement": "The frozen Cycle-1 DFS completed its full branch traversal for k=13,p=199 and emitted 4,748,938 distinct sorted representatives, each satisfying the exact l=1 improper-tuple predicate.",
            "k": metric(r"k=(\d+)", result),
            "p": metric(r"p=(\d+)", result),
            "canonical_representatives": metric(r"canonical_solutions=(\d+)", result),
            "dfs_nodes": metric(r"nodes=(\d+)", result),
            "dfs_leaves": metric(r"leaves=(\d+)", result),
            "wall_seconds_internal": metric(r"wall_seconds=([0-9.]+)", result, float),
            "peak_rss_kib": metric(r"Maximum resident set size \(kbytes\): (\d+)", timing),
            "compressed_tuple_sha256": frozen["frontier_tuples_gzip"]["sha256"],
            "row_recheck": recheck.stdout.strip(),
        },
        "known_limitations": [
            "The independent stream pass validates emitted rows, not omitted branches.",
            "Full orbit-minimality for every p=199 row was not independently recomputed; the general canonicalization was independently exhausted only on the two p=47 baselines.",
            "I(13,199,1) is only an initial sieve. It does not establish eventual properness, J(13,199)=empty, a prime-product contradiction, or LRC(13).",
        ],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "adopted": True,
            "recommendation": "Seal Cycle 1/B001 as an OBSERVED frontier census and open a distinct Cycle 2 for an orbit-aware exact-cover quotient.",
            "known_flaw": "The p=199 completeness and orbit count still rest on one DFS/canonicalization implementation.",
            "falsifier": "A branch-partition counterexample, a noncanonical emitted orbit representative, or a baseline-count change under independently proved canonical augmentation.",
            "next_action": "Open Cycle 2; freeze the partial-cover group action, canonical-augmentation rule, and orbit-representative preservation proof before executable work.",
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Construct an orbit-aware exact-cover quotient that preserves every cover orbit, reproduces the 53/50 baselines, and materially reduces the certified node/leaf count at k=13,p=199; later lifting and the full LRC(13) bridge remain open.",
        },
        "runtime": {**runtime, "compiler": compiler},
        "frozen_hashes": frozen,
        "replay": {
            "check_command": "python3 proof/build_cycle_1_lrc_frontier.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_1_lrc_frontier.py -v",
            "write_command": "python3 proof/build_cycle_1_lrc_frontier.py --write",
            "frontier_row_recheck": "python3 discovery/check_lrc_ansatz.py --k 13 --p 199 --tuples discovery/out/k13-p199.txt.gz --stream-recheck --expected-count 4748938",
            "principal_replay": "g++ -std=c++20 -O3 -DNDEBUG -pthread discovery/lrc_ansatz_exact.cpp -o discovery/out/lrc_ansatz_exact && discovery/out/lrc_ansatz_exact --k 13 --p 199 --threads 8 --max-seconds 3600 --output discovery/out/k13-p199-replay.txt",
        },
        "sealer": {
            "path": "proof/build_cycle_1_lrc_frontier.py",
            "sha256": sha256(Path(__file__)),
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
