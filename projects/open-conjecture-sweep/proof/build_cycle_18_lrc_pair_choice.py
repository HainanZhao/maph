"""Seal Cycle 18's exact pair-choice Hall certificates."""

from __future__ import annotations

from pathlib import Path

from check_cycle_18_pair_choice import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle18-pair-choice"
OUTPUT = ROOT / "artifacts/cycle-18-b018-lrc-pair-choice-v1.json"
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-18-b018-lrc-pair-choice-preregistration-v1.md", "b0dc79f6d20f70ba5b4a9545bd46136ab9bf895ea68455b45d238b05d70e01c9"),
    "prior_artifact": (ROOT / "artifacts/cycle-17-b017-lrc-time-deficit-v1.json", "71460c48d17b58b366bf0ef415b7b16f5636bb6bc8381b28608b6ebaf318fb35"),
    "soundness": (ROOT / "proof/cycle_18_pair_choice_soundness.md", "265c758036f95b292bbf099b2ff64e9db1f47b1f0d09b9b02b24b9818a96b4f1"),
    "engine": (ROOT / "discovery/lrc_pair_choice.py", "f3faa9c3152467243ec1acfe27310c857cadbbe40b565c7cf51fb6e47318d55a"),
    "audit": (ROOT / "proof/check_cycle_18_pair_choice.py", "a3ca7288745b316df2fcbf75f9f0b560dd8de03a4207e78fe12efef41ed4ba4b"),
    "test": (ROOT / "tests/test_cycle_18_pair_choice.py", "7a20e2d702b13dd828e0a0966d815758431b8e24e142fc0743f7fcf7b16d9903"),
    "results": (OUT / "results.tsv", "7317d2285b0db951e8fffda50aab031c4c80a24c2ffdf863bd2052705057507c"),
    "result": (OUT / "result.txt", "0f21c224f0bd4a659336a1f9653aa54ec22ef054b1c07056a8c5018fd5ffec54"),
    "run_timing": (OUT / "run.time", "e54784df887af49ed0c041336b942491274981656bcc6d2777acf3d38387ebd7"),
    "audit_timing": (OUT / "audit.time", "0d27c7148fc322fd5414a5594e6cc3a735a8b869ed19fc8e6beb44867c57f488"),
    "cycle17_bounded": (ROOT / "discovery/out/cycle17-time-deficit/results.tsv", "0e3fcf08b7c168b1abef2307574e0f2896853f6691a924f1b14ef64c0c41f06e"),
    "cycle17_lp": (ROOT / "discovery/out/cycle17-time-deficit/lp-results.tsv", "da5f5f926d317e07e662002ac722e2422f22beb47f15e4b55815be98540f935e"),
    "base4_cnf": (ROOT / "discovery/out/cycle11-certified-sat/p199/004.cnf", "ea4356bd1ff5cdf06fb5504411d0ca57ddc8b3056dc8281c8025d1d24ef60648"),
    "base3_cnf": (ROOT / "discovery/out/cycle11-certified-sat/p199/003.cnf", "e07cde8b14f19bf2094e2643ac43c6aad6c6d62ade399db270968a479d0ee6c4"),
    "sample_bases": (ROOT / "discovery/out/cycle8-p199-strata.txt", "327334cf85b821a77b254420d0617c8771a9f272cf38b2512ab79c937de4299b"),
    "requirements": (ROOT / "requirements-cycle17.txt", "ff5d0c36b5024e0b76b1eb815d52ff00cee3ab78523f3419b5006f728b02b7a4"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
}


def payload() -> dict:
    runtime = check_runtime("Cycle 18 pair choice")
    frozen = freeze_inputs(ROOT, INPUTS)
    summary = audit()
    return {
        "artifact_id": "cycle-18-b018-lrc-pair-choice-v1",
        "budget_ordinal": "B018",
        "cycle": 18,
        "record_type": "CERTIFIED_FINITE_RESULT",
        "recorded_at_utc": "2026-08-03T21:55:52Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "The pair-choice Hall inequality is exact, and independent reconstruction validates four strict integer deficits for frozen base-3 leaf ordinals 83, 121, 952, and 979. Combined with Cycle 17, this raises base 3 to 6,048 of 6,084 certified canonical leaves while base 4 remains at 6,044. No base is complete.",
        "claim_boundary": "Only the four stored base-3 pair-choice inequalities are newly PROVED. The frozen engine reported no candidate on 76 other rows, but this bounded numerical search outcome is OBSERVED and does not rule out other partitions, weights, larger blocks, symbolic cases, CRT, complete base exclusion, F_1, J, or LRC(13).",
        "certificate_theorem": {
            "epistemic_status": "PROVED",
            "statement": "For a disjoint singleton/pair partition, count each weighted time once per block; any full cover has W<=U_P, so U_P<W is a contradiction.",
        },
        "exact_result": {
            "epistemic_status": "PROVED",
            "target_rows": summary["rows"],
            "base4_new_certificates": summary["base4_certified"],
            "base3_new_certificates": summary["base3_certified"],
            "base3_leaf_ordinals": [83, 121, 952, 979],
            "strict_margins": [13, 21, 13, 21],
            "combined_base4_certified": 6044,
            "combined_base3_certified": 6048,
            "complete_bases": 0,
        },
        "bounded_search": {
            "epistemic_status": "OBSERVED",
            "unresolved_rows": summary["unresolved"],
            "base4_candidates": 0,
            "base3_candidates": 4,
            "interpretation": "The small gain makes broader enumeration of the same frozen pair family lower value, but proves no general no-go.",
        },
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "scope_review": "After independent reconstruction, only four named base-3 leaves are new exact eliminations; 76 target rows remain unresolved.",
            "recommendation": "Seal Cycle 18 after audit and open a distinct symbolic cycle; do not expand pair partitions.",
            "strongest_flaw": "Four asymmetric hits give weak evidence about pair coupling, and the frozen partitions may miss the relevant interaction.",
            "falsifier": "Any leaf/base/partition mismatch or reconstructed inequality with U_P>=W invalidates the affected certificate.",
            "independent_ideas": ["first-seven-coordinate symbolic case split", "exact fractional primal/integrality-gap witnesses", "CRT after a coverage-equivalence test"],
            "next_action": "Open Cycle 19: freeze a symbolic first-seven-coordinate grammar guided by exact fractional structure; every closed branch ends in an exact Hall or DRAT certificate.",
        },
        "resources": {
            "aggregate_wall_seconds": 380.85,
            "aggregate_wall_cap_seconds": 3600,
            "peak_rss_kib": 176048,
            "output_corpus_bytes": 14691,
            "dependency_environment_bytes": 235737075,
            "temporary_disk_cap_bytes": 21474836480,
            "worker_cpus": [0, 1, 2],
            "reserved_cpu": 3,
            "runtime": "CPython 3.12.3, numpy 2.2.6, scipy 1.14.1",
        },
        "runtime": runtime,
        "frozen_hashes": frozen,
        "replay": {
            "run_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_pair_choice.py",
            "audit_command": "python3 proof/check_cycle_18_pair_choice.py",
            "check_command": "python3 proof/build_cycle_18_lrc_pair_choice.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_18_pair_choice.py -v",
        },
        "sealer": {"path": "proof/build_cycle_18_lrc_pair_choice.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
