#!/usr/bin/env python3
"""Seal Cycle 51's finite conjugacy-averaging census."""
from __future__ import annotations

from pathlib import Path

from check_cycle_51_conjugacy_averaging import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle51-conjugacy-averaging"
OUTPUT = ROOT / "artifacts/cycle-51-b051-sidorenko-conjugacy-averaging-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-51-b051-sidorenko-conjugacy-averaging-preregistration-v1.md", "a07005e4845afca4d8e0c9fccdb6c767ed67687398ea18b3f83f215fa5fbc5b0"),
    "cycle50_artifact": (ROOT / "artifacts/cycle-50-b050-lrc-deletion-aware-packet-v1.json", "c29fb94c0e7eea145157ea3e71deb71c5352da6ebc53c96e908a93576047f3e9"),
    "eligibility": (ROOT / "discovery/problem2_eligibility_audit.md", "196c30a07951a091fefd10d1d2550e111d614664f3aea7fc70eebe9b70fc3250"),
    "idea_selection": (ROOT / "discovery/cycle51_conjugacy_averaging_idea_selection.md", "10bec560c1210973f9acad49f7120053a27cee378c4a24410c8cdb725ae0afc8"),
    "principal_engine": (ROOT / "discovery/sidorenko_conjugacy_census.cpp", "1f34232506d8e06e5d60f1ea723abfa0347c9197317aa8ec6e398d86287b074f"),
    "principal_summary": (OUT / "summary.json", "0419a726a51586e6370d8484eb0f89e0b4ee27cdd9a8121053e273bef5f30218"),
    "principal_rows": (OUT / "comparison-rows.tsv", "2d4c7840746a78fd01ba75762a8fc4a622c65d2e4a6fde3d8123fb8689cdcc57"),
    "direct_controls": (OUT / "direct-s3-controls.tsv", "75a7dcc6c553f02a3786fea6a9bccef3ecd17a0218942a6866cf2c56a7061a6e"),
    "independent_engine": (ROOT / "proof/replay_cycle_51_conjugacy_independent.cpp", "ee277384f516affc2dff9b7efe89b6a0da9f1dfe3b65563413cf8b5423f83bf2"),
    "independent_summary": (OUT / "independent-summary.json", "2daffa13e46f98cdd463371cedd9438faf310db237a625485c4bf7025c0a2b74"),
    "independent_rows": (OUT / "independent-comparison-rows.tsv", "29182bfb6b9e48f0d837391d81ef3a2060f812dc9e9926da082aedf7c0c38f16"),
    "audit": (ROOT / "proof/check_cycle_51_conjugacy_averaging.py", "74dbc7cfecca847b2ba92df98cad84afedcc730072c0097aa202bebf9a9b03ee"),
    "soundness": (ROOT / "proof/cycle_51_conjugacy_averaging_soundness.md", "6c7baed4510940f5800c53d019a2bf82f08212e820abc199220d5dbfb949d3f5"),
    "test": (ROOT / "tests/test_cycle_51_conjugacy_averaging.py", "cea0ee6ca1581538c22dd7a10e6d83c92e4bd8bfcb84750a455204c53fae1a97"),
    "principal_timing": (OUT / "run-principal.time", "feb1c44299eb5db9cfce8b92910eac59d348bc1a655e2997f805e564ff10508c"),
    "independent_timing": (OUT / "run-independent.time", "5b036c250641e674f8db19e0603f601bbfb83574f18833419732674d43c7a04c"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "preregistration_validator": (ROOT / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def payload():
    checked = audit()
    return {
        "artifact_id": "cycle-51-b051-sidorenko-conjugacy-averaging-v1", "budget_ordinal": "B051", "cycle": 51,
        "record_type": "PROVED_FINITE_CONJUGACY_AVERAGING_CORPUS", "recorded_at_utc": "2026-08-05T08:20:00Z",
        "status": "SEALED", "epistemic_status": "PROVED",
        "outcome": "The exact Zhao conjugacy-averaging comparison has no countermodel in the frozen 840-row corpus: every indicator on S3, D8, Q8 and every distinct subgroup-product indicator in S3,S4 is nondecreasing under conjugacy averaging for the 15-edge Möbius graph.",
        "claim_boundary": "This exact finite pass neither proves Zhao's all-finite-group/all-nonnegative-function hypothesis, strong Sidorenko, Sidorenko, nor a graphon extremizer reduction.",
        "cycle_decision": {
            "companion_identity": "/root/darwin_cycle25_short",
            "companion_advice": "Seal the finite corpus; do not enlarge the structured-group census. Open a distinct fixed-density local graphon-variation block.",
            "next_question": "Does an exact finite-rank zero-mean graphon perturbation have a negative first nonzero coefficient in t(H,p+epsilon U)-p^15?",
            "falsifier": "One exact negative coefficient realized by a bounded rational step graphon gives a Sidorenko counterexample; nonnegative local forms are only a local boundary.",
        },
        "audit": checked,
        "resources": {"worker_cpus": [0, 1, 2], "reserved_cpu": 3, "principal_wall_seconds": 15.28, "independent_wall_seconds": 14.73, "principal_peak_rss_kib": 3840, "independent_peak_rss_kib": 3840, "temporary_disk_bytes": sum(path.stat().st_size for path in OUT.iterdir() if path.is_file())},
        "runtime": check_runtime("Cycle 51 conjugacy averaging"), "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "replay": {
            "principal_command": "g++ -O3 -std=c++20 discovery/sidorenko_conjugacy_census.cpp -o /tmp/c51-principal && taskset -c 0-2 /tmp/c51-principal discovery/out/cycle51-conjugacy-averaging",
            "independent_command": "g++ -O3 -std=c++20 proof/replay_cycle_51_conjugacy_independent.cpp -o /tmp/c51-independent && taskset -c 0-2 /tmp/c51-independent discovery/out/cycle51-conjugacy-averaging",
            "audit_command": ".venv/bin/python proof/check_cycle_51_conjugacy_averaging.py", "test_command": ".venv/bin/python -m unittest tests.test_cycle_51_conjugacy_averaging -v", "check_command": ".venv/bin/python proof/build_cycle_51_sidorenko_conjugacy.py --check",
        },
        "sealer": {"path": "proof/build_cycle_51_sidorenko_conjugacy.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
