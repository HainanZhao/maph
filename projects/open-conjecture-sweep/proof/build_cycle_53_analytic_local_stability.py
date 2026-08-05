#!/usr/bin/env python3
"""Seal Cycle 53's directional-local-stability theorem."""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from proof.check_cycle_53_analytic_local_stability import audit
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


def timing(path: Path):
    seconds, kib = path.read_text().strip().split("\t")
    return float(seconds), int(kib)


INPUTS = {
    "cycle52_artifact": (ROOT / "artifacts/cycle-52-b052-sidorenko-local-variation-v1.json", "3961dfa1b0fcc16db535ee59b031b7b4ae683ea9ecf6e5060199175257019b45"),
    "idea_selection": (ROOT / "discovery/cycle53_analytic_local_stability_idea_selection.md", "74578cf98e0e188a54c14ef07f22baa0c347aab7885ad8e23dd0d2e2503dee40"),
    "preregistration": (ROOT / "docs/cycle-53-b053-analytic-local-stability-preregistration-v1.md", "a93efc741ef5df1be58f1808777c054f901057770f666c656bb0fcb6a1d0dd9a"),
    "preregistration_validator": (ROOT / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
    "principal_enumerator": (ROOT / "proof/cycle53_subset_audit.py", "c4349c7aa920ad783ad693241110b67f6a70e54f0652d2fcb8a5c0576878c615"),
    "independent_enumerator": (ROOT / "proof/replay_cycle_53_subset_independent.py", "1ebdf4a2b04b2a519ab59cb0a4de24cf2d7af27a6f00bcbe6ee17a8ddcfe8834"),
    "audit": (ROOT / "proof/check_cycle_53_analytic_local_stability.py", "5ff4396f9a9790436c345cf35a1a88a4fd111e9a0147901edf89baff39f81cd6"),
    "soundness": (ROOT / "proof/cycle_53_analytic_local_stability_soundness.md", "6d1e3b26c5dd3df991e40f3f8fb37844e2427440a583901b112e6b5de1b07d22"),
    "test": (ROOT / "tests/test_cycle_53_analytic_local_stability.py", "c9b56af4772eabf7ed274b9c0722aca2fcddcf5b0555279996c436279725b512"),
    "principal_summary": (ROOT / "discovery/out/cycle53-analytic-local-stability/principal-summary.json", "1aaa7cd24444a5fa124934aa61a9e717323daaa59c72393c448cf85797e77a47"),
    "independent_summary": (ROOT / "discovery/out/cycle53-analytic-local-stability/independent-summary.json", "36a1417dbfc1c9ec9480435ed3ae35fc148bb5587d1d60d3261cbec98ecaa159"),
    "principal_timing": (ROOT / "discovery/out/cycle53-analytic-local-stability/run-principal.time", "e0531534a80db5c9c1517767b54928ead3ac19c295be375cd06fab8f2a090db2"),
    "independent_timing": (ROOT / "discovery/out/cycle53-analytic-local-stability/run-independent.time", "be93ae5efc4cd86e14985b1ab10ae173d0c77ac5a41dd1c9543f9106e959c378"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
}


def payload():
    checked = audit()
    principal_seconds, principal_kib = timing(ROOT / "discovery/out/cycle53-analytic-local-stability/run-principal.time")
    independent_seconds, independent_kib = timing(ROOT / "discovery/out/cycle53-analytic-local-stability/run-independent.time")
    require(principal_seconds + independent_seconds < 600, "wall cap exceeded")
    require(max(principal_kib, independent_kib) < 512 * 1024, "memory cap exceeded")
    return {
        "artifact_id": "cycle-53-b053-analytic-local-stability-v1", "budget_ordinal": "B053", "cycle": 53,
        "record_type": "PROVED_DIRECTIONAL_LOCAL_STABILITY_THEOREM", "recorded_at_utc": "2026-08-05T08:41:00Z",
        "status": "SEALED", "epistemic_status": "PROVED",
        "outcome": "For every nonzero bounded symmetric zero-mean kernel U, the Möbius graph density t_H(1/2+epsilon U) exceeds 2^-15 for all sufficiently small positive epsilon. The exact leading coefficient is quadratic unless d_U=0; on that kernel it is the positive five-four-cycle quartic trace term.",
        "claim_boundary": checked["claim_boundary"], "audit": checked,
        "cycle_decision": {
            "companion_identity": "/root/darwin_cycle25_short",
            "companion_advice": "Seal the symmetric directional theorem. Open a distinct C54 for nonsymmetric bipartite zero-mean kernels, where the quartic C4 term is tr((T_U T_U*)^2)=sum s_i^4; do not infer a uniform neighborhood or global inequality.",
            "next_question": "Does the p=1/2 directional local theorem extend to arbitrary bounded rectangular bipartite kernels after separately removing their left and right degree functions?",
            "falsifier": "An exact degree-zero nonzero rectangular kernel with a nonpositive C4 term, an omitted leafless 3/4-edge subgraph with an indefinite contribution, or a demonstrated failure of the theorem's frozen hypotheses."
        },
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "resources": {"worker_cpus": [0, 1, 2], "reserved_cpu": 3, "principal_wall_seconds": principal_seconds, "independent_wall_seconds": independent_seconds, "principal_peak_rss_kib": principal_kib, "independent_peak_rss_kib": independent_kib, "temporary_disk_bytes": sum(p.stat().st_size for p in (ROOT / "discovery/out/cycle53-analytic-local-stability").iterdir() if p.is_file())},
        "runtime": check_runtime("cycle 53 sealer"), "sealer": {"path": "proof/build_cycle_53_analytic_local_stability.py", "sha256": sha256(Path(__file__))},
        "replay": {"principal_command": ".venv/bin/python proof/cycle53_subset_audit.py", "independent_command": ".venv/bin/python proof/replay_cycle_53_subset_independent.py", "audit_command": ".venv/bin/python proof/check_cycle_53_analytic_local_stability.py", "test_command": ".venv/bin/python -m unittest tests.test_cycle_53_analytic_local_stability -v", "check_command": ".venv/bin/python proof/build_cycle_53_analytic_local_stability.py --check"},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=ROOT / "artifacts/cycle-53-b053-analytic-local-stability-v1.json", payload_factory=payload))
