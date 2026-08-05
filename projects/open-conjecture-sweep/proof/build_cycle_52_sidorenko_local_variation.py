#!/usr/bin/env python3
"""Seal the finite exact local-variation result for Cycle 52."""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.check_cycle_52_local_variation import audit
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


def timing(path: Path) -> tuple[float, int]:
    seconds, kib = path.read_text().strip().split("\t")
    return float(seconds), int(kib)


def payload():
    result = audit()
    principal_seconds, principal_kib = timing(ROOT / "discovery/out/cycle52-local-variation/run-principal.time")
    independent_seconds, independent_kib = timing(ROOT / "discovery/out/cycle52-local-variation/run-independent.time")
    require(principal_seconds + independent_seconds < 7200, "aggregate wall cap exceeded")
    require(max(principal_kib, independent_kib) < 4096 * 1024, "memory cap exceeded")
    inputs = {
        "cycle51_artifact": (ROOT / "artifacts/cycle-51-b051-sidorenko-conjugacy-averaging-v1.json", "f30ef5726bac1ab064f7d281efe48a8205ade1211c63dca58fa15c67fb2b599f"),
        "eligibility": (ROOT / "discovery/problem2_eligibility_audit.md", "196c30a07951a091fefd10d1d2550e111d614664f3aea7fc70eebe9b70fc3250"),
        "idea_selection": (ROOT / "discovery/cycle52_local_variation_idea_selection.md", "fdfe22e494abf57dbc38fc257ddbe63b19f3436de14aaaee8dd317be7bcf304d"),
        "preregistration": (ROOT / "docs/cycle-52-b052-sidorenko-local-variation-preregistration-v1.md", "146e5e567a1a1baf8bfe56886b59b1e4fd9a2c0a91a77a9ef6eeba2e2d4ecd23"),
        "preregistration_validator": (ROOT / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
        "principal_engine": (ROOT / "discovery/sidorenko_local_variation_census.cpp", "caafe606049c58447887d9bcbf77f01caacd3b328132e2aa351e23984d5e9147"),
        "independent_engine": (ROOT / "proof/replay_cycle_52_local_variation_independent.cpp", "17ba140eb30b62f7a013a16881fdfdef221046da5575484d3616ee66cd9432c9"),
        "audit": (ROOT / "proof/check_cycle_52_local_variation.py", "d1e96716de06a75ea5313142b65598b5a72ee9a0954e5419985f030c4f7f023e"),
        "soundness": (ROOT / "proof/cycle_52_local_variation_soundness.md", "d4963d4b4f54529f3240187559a49f3b6e48a51155bbbcaa6b10d7c986a73f2e"),
        "test": (ROOT / "tests/test_cycle_52_local_variation.py", "120b954cb8a7070283d491d3b4157d6c8d7ac06fce3398bcdc02d4e014f45876"),
        "principal_rows": (ROOT / "discovery/out/cycle52-local-variation/rows.tsv", "8ede164a970b41eacb7bb80f3705187fb005dfe5f53f4d8abff5ea240d556bab"),
        "independent_rows": (ROOT / "discovery/out/cycle52-local-variation/independent-rows.tsv", "d5bc195b4c07f13a0c315927cd8f4bcbcfd1377dc9a7a997f76419110799f127"),
        "principal_summary": (ROOT / "discovery/out/cycle52-local-variation/summary.json", "c31df84c0634d971de9683c2026ba3aa1a2a1e7e59c00e346df32790f1d71f57"),
        "independent_summary": (ROOT / "discovery/out/cycle52-local-variation/independent-summary.json", "84f4c46956a17af1cb35f7a0cea9cbee70f652a37de31b79500e4aab5dd087a4"),
        "principal_timing": (ROOT / "discovery/out/cycle52-local-variation/run-principal.time", "1d0e2eb1ce037bec8de0f71b57689912fbbfb6d804bb56fa84b48fd6e42d6d74"),
        "independent_timing": (ROOT / "discovery/out/cycle52-local-variation/run-independent.time", "f07471ed13c18208543b561e098cddcbf3b76c17c816c370ba5f0f84839fc3ec"),
        "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    }
    return {
        "artifact_id": "cycle-52-b052-sidorenko-local-variation-v1",
        "budget_ordinal": "B052", "cycle": 52, "record_type": "PROVED_FINITE_LOCAL_VARIATION_CENSUS", "recorded_at_utc": "2026-08-05T08:32:00Z",
        "status": "SEALED", "epistemic_status": "PROVED",
        "outcome": "Every one of the 512 frozen primitive symmetric zero-mean equal-block 2/3-step perturbation directions at p=1/2 has a positive first nonzero coefficient in t_H(1/2+epsilon B/2)-2^-15; no local counterexample candidate occurs in this family.",
        "claim_boundary": result["claim_boundary"],
        "audit": result,
        "cycle_decision": {
            "companion_identity": "/root/darwin_cycle25_short",
            "companion_advice": "Seal C52 and open a distinct analytic fixed-density local-stability engine: derive the arbitrary finite-rank bipartite quadratic form at p=1/2, decompose under D10, and analyze the quartic form on its Hessian kernel.",
            "strongest_scope_flaw": "The finite family excludes unequal block sizes, nonsymmetric bipartite perturbations, higher-rank directions, other densities, and large-amplitude/global competitors.",
            "next_question": "Is the exact p=1/2 quadratic form nonnegative on arbitrary finite-rank bipartite zero-mean perturbations, and is its first surviving higher form nonnegative on its kernel?",
            "falsifier": "An exact finite-rank perturbation with a negative quadratic form, or a Hessian-null perturbation with a negative first surviving coefficient, gives a rational graphon counterexample candidate after bounded scaling."
        },
        "frozen_hashes": freeze_inputs(ROOT, inputs),
        "resources": {
            "worker_cpus": [0, 1, 2], "reserved_cpu": 3,
            "principal_wall_seconds": principal_seconds, "independent_wall_seconds": independent_seconds,
            "principal_peak_rss_kib": principal_kib, "independent_peak_rss_kib": independent_kib,
            "temporary_disk_bytes": sum(path.stat().st_size for path in (ROOT / "discovery/out/cycle52-local-variation").iterdir() if path.is_file()),
        },
        "runtime": check_runtime("cycle 52 sealer"),
        "sealer": {"path": "proof/build_cycle_52_sidorenko_local_variation.py", "sha256": sha256(Path(__file__))},
        "replay": {
            "principal_command": "g++ -O3 -std=c++20 -fopenmp discovery/sidorenko_local_variation_census.cpp -o /tmp/c52-principal && taskset -c 0-2 /tmp/c52-principal discovery/out/cycle52-local-variation",
            "independent_command": "g++ -O3 -std=c++20 proof/replay_cycle_52_local_variation_independent.cpp -o /tmp/c52-independent && taskset -c 0-2 /tmp/c52-independent discovery/out/cycle52-local-variation",
            "audit_command": ".venv/bin/python proof/check_cycle_52_local_variation.py",
            "test_command": ".venv/bin/python -m unittest tests.test_cycle_52_local_variation -v",
            "check_command": ".venv/bin/python proof/build_cycle_52_sidorenko_local_variation.py --check",
        },
    }


if __name__ == "__main__":
    sys.exit(run_cli(description=__doc__, output=ROOT / "artifacts/cycle-52-b052-sidorenko-local-variation-v1.json", payload_factory=payload))
