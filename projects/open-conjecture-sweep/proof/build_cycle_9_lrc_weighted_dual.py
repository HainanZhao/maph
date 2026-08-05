"""Seal Cycle 9's exact H11 weighted-dual structural no-go."""

from __future__ import annotations

from pathlib import Path
import subprocess

from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-9-b009-lrc-weighted-dual-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-9-b009-lrc-weighted-dual-preregistration-v1.md", "d5a6dc7202c9cc73aca98edefd0d4fcf7bc0f7cbf07837e782005c7f972eaaca"),
    "soundness": (ROOT / "proof/cycle_9_weighted_dual_soundness.md", "5963cef2ecf9d7b636abcc85098e530d6a727e8559fb7bc0b0f45a3a71dccbf9"),
    "discovery_engine": (ROOT / "discovery/lrc_weighted_dual_h11.cpp", "cad543177a0f1e77ce71c817c02c4a7d538e399e1e3b89fe9970831d15ecd768"),
    "discovery_reference": (ROOT / "discovery/lrc_weighted_dual_h11.py", "5f2ca9ff6e74961300955a1e77aba2dd86f4b1dcf67a7b618864986c9c3822d1"),
    "discovery_output": (ROOT / "discovery/out/cycle9-h11-dual-discovery.txt", "59cbb3cf006b77af73b0b7667f3be472e852bc1fafb5a2cac820fc3360404b2f"),
    "discovery_result": (ROOT / "discovery/out/cycle9-h11-dual-discovery.result", "72cf11b790abdb9521a79492ece1c52274dd89f12ef9fde2378f37b830af8fb8"),
    "exact_falsifier": (ROOT / "proof/check_cycle_9_h11_mask_cover.py", "31e95700faa731711f7869e325cc1e8e1521240d56030e4d0e5a58008d3d4cf3"),
    "falsifier_output": (ROOT / "discovery/out/cycle9-h11-dual-falsifiers.txt", "868bc1fa4ef31dc0978f1deff59c2e8e947b7312b24402d3743b386fa8d8aba6"),
    "falsifier_result": (ROOT / "discovery/out/cycle9-h11-dual-falsifiers.result", "c6c3e29edb5eeb02c9a8956b016115d8718b96b9971c3f4f3dfae21cdfe81b2e"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "regression_test": (ROOT / "tests/test_cycle_9_lrc_weighted_dual.py", "0383c31048036ed6e7b1fab65d10d7a400e1af1dab0defccfde9af842c3c58b9"),
}


def payload() -> dict:
    runtime = check_runtime("Cycle 9 weighted dual")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = (ROOT / "discovery/out/cycle9-h11-dual-falsifiers.result").read_text().strip()
    if result != "h11_l1_improper_bases=240 mask_cover_falsifiers=240":
        raise RuntimeError("unexpected H11 dual-falsifier summary")
    rows = (ROOT / "discovery/out/cycle9-h11-dual-discovery.txt").read_text().splitlines()
    if len(rows) != 240 or any(row.split()[3] != "NO_CERTIFICATE" for row in rows):
        raise RuntimeError("unexpected dual discovery output")
    return {
        "artifact_id": "cycle-9-b009-lrc-weighted-dual-v1", "budget_ordinal": "B009", "cycle": 9,
        "record_type": "STRUCTURAL_NO_GO", "recorded_at_utc": "2026-08-03T17:02:00Z", "status": "SEALED", "epistemic_status": "PROVED",
        "outcome": "Every one of the 240 raw H11 l=1-improper bases has an explicit first-lift mask-cover selection. Therefore no nonnegative weighted-time dual of the frozen form can certify any of them, even though the gcd clause makes their F_1 survivors empty.",
        "claim_boundary": "This proves a structural no-go only for the nonnegative weighted-mask dual family on raw (3,11,4) base covers. It does not predict p199 behavior, refute gcd-aware certificates, construct an improper lift, or make a J/LRC claim.",
        "exact_falsifier": {"epistemic_status": "PROVED", "raw_h11_bases": 1000, "l1_improper_bases": 240, "mask_cover_falsifiers": 240, "dual_certificates_possible": 0},
        "discovery": {"epistemic_status": "OBSERVED", "deterministic_weight_search_rows": 240, "accepted_certificates": 0, "interpretation": "The search output is explanatory only; the explicit cover selections prove the no-go independently."},
        "companion_decision": {"identity": "/root/decision_companion_2", "adopted": True, "recommendation": "Seal Cycle 9 and open Cycle 10 for the gcd-pattern/cover engine.", "independent_ideas": ["gcd-pattern/cover", "CRT factorization", "pinned CDCL", "stop P1"], "flaw": "H11 may be atypical for p199 divisibility patterns.", "falsifier": "A directly rechecked p199 mask-cover assignment avoiding every 12-of-2/7 pattern gives an improper lift.", "next_action": "New Cycle 10: partition lift assignments by mod-2/mod-7 gcd patterns and test cover impossibility in gcd-admissible patterns."},
        "runtime": {**runtime, "compiler": subprocess.run(["g++", "--version"], check=True, capture_output=True, text=True).stdout.splitlines()[0]}, "frozen_hashes": frozen,
        "replay": {"falsifier_command": "python3 proof/check_cycle_9_h11_mask_cover.py", "check_command": "python3 proof/build_cycle_9_lrc_weighted_dual.py --check", "test_command": "python3 -m unittest tests/test_cycle_9_lrc_weighted_dual.py -v"},
        "sealer": {"path": "proof/build_cycle_9_lrc_weighted_dual.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
