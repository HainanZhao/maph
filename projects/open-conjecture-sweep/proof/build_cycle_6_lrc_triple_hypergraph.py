"""Seal Cycle 6's triple-hypergraph discovery and direct-oracle boundary."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess

from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-6-b006-lrc-triple-hypergraph-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-6-b006-lrc-triple-hypergraph-preregistration-v1.md", "1d1693fa6cf8fc6f57264e7bbd3ded11aefb9e7e9b9cfdda2fae3c98b0a045c9"),
    "soundness_argument": (ROOT / "proof/cycle_6_triple_hypergraph_soundness.md", "b5d0333e2a031ba255eeee433a6a9b23b00d019a1a4c06dd00124599fb4704a4"),
    "triple_checker": (ROOT / "discovery/check_lrc_triple_hypergraph.py", "01015c8f2fd1001fcb349a76e583a8674decccd16c213022f912083a5719f04f"),
    "h11_oracle": (ROOT / "discovery/out/triple-h11-oracle.json", "a5c25d683fb41c4e54e713d9e5d8700fa153e97caab93573cca885f48865874c"),
    "global_relation": (ROOT / "discovery/out/triple-global-2.json", "08dc73c654b8e731f9af93c44899c3d00732d4fc15436852962bd4fc547bca9a"),
    "sample_generator": (ROOT / "discovery/lrc_triple_sample.cpp", "f04944c25c58311f9c97c86adec0322affa61fe029c66969eaebd838fc5f122c"),
    "sample_result": (ROOT / "discovery/out/triple-sample-p199.result", "15ca7827fd6344c41ede98bb7e24e43953e872407052c2a1949f9322e8dcabf8"),
    "sample_timing": (ROOT / "discovery/out/triple-sample-p199.time", "e91093dbdecd1398d7c67d2bd42308ea9c12dcca5a1a72095882254886aee495"),
    "sample_states": (ROOT / "discovery/out/triple-sample-p199.txt", "cc003c483ae18513b630ea152d7479d4e014b8845dd60886f0eef1b7766b9712"),
    "evaluator": (ROOT / "discovery/lrc_triple_sample_evaluate.cpp", "3345242912f040191916709af239857b65a3f0d74eeb28ead444e6f01a257e9d"),
    "triple_prefix_result": (ROOT / "discovery/out/triple-eval-1000-fast.txt", "a8f5f4b2172a9d9f1a9e9e52229c61e92f0e0e9ecddd5890938707e37be550fe"),
    "direct_prefix_result": (ROOT / "discovery/out/triple-eval-1000-direct-fast.txt", "f09c9c9ab72ebfc2e4e88d918831c444aa7e1d991e63e6e62b61110af2631f38"),
    "direct_part_0": (ROOT / "discovery/out/triple-direct-final-part-0.txt", "8802bf1f3c0987716afb6b87405bb8c062f86c087108d26eea3470176c6d61b9"),
    "direct_part_1": (ROOT / "discovery/out/triple-direct-final-part-1.txt", "71924225779763d3754229009e963f76ad826686a9b6ac5bffc6b45d2785066f"),
    "direct_part_2": (ROOT / "discovery/out/triple-direct-final-part-2.txt", "4375fe2408ab3224be98837d5f51ddd09241fa7d54162af5a413988bdad5a217"),
    "direct_oracle_check": (ROOT / "proof/check_cycle_6_direct_oracle.py", "25390dfab957f38544d98575391ebceba8b2495d934d6cc114f6d0f170725f1b"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "regression_test": (ROOT / "tests/test_cycle_6_lrc_triple_hypergraph.py", "adc4330b067dc114be2812ad75ea37a335af525b1037ffb108dfe8a64453cb14"),
}


def payload() -> dict:
    runtime = check_runtime("Cycle 6 triple hypergraph")
    frozen = freeze_inputs(ROOT, INPUTS)
    h11 = json.loads((ROOT / "discovery/out/triple-h11-oracle.json").read_text())
    global_relation = json.loads((ROOT / "discovery/out/triple-global-2.json").read_text())
    compiler = subprocess.run(["g++", "--version"], check=True, capture_output=True, text=True).stdout.splitlines()[0]
    return {
        "artifact_id": "cycle-6-b006-lrc-triple-hypergraph-v1",
        "budget_ordinal": "B006",
        "cycle": 6,
        "record_type": "STRUCTURAL_REDUCTION",
        "recorded_at_utc": "2026-08-03T16:16:00Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "Forbidden triples give a sound non-completability relation that is nontrivial at (13,199); its direct exact-translate comparator rejects 85.594% of the frozen depth-8 sample, motivating a distinct direct-feasibility engine.",
        "claim_boundary": "The proved lemma is only the necessary weak-colorability condition for the frozen triple hypergraph. The observed sample rejection rate does not prove full-frontier performance, equivalence of triple colorability and translate feasibility, J(13,199)=empty, LRC(13), or any higher-arity result.",
        "h11_oracle": {"epistemic_status": "PROVED", **h11},
        "global_relation": {"epistemic_status": "PROVED", **global_relation},
        "sample_generation": {
            "epistemic_status": "OBSERVED", "depth": 8, "total_canonical_states": 33_193_860,
            "lexicographic_prefix_states": 100_000, "peak_disk_bytes": 733_747_312,
            "wall_seconds": 13.9197,
        },
        "sample_comparison": {
            "epistemic_status": "OBSERVED", "states": 1_000,
            "triple_unsat": 994, "triple_sat": 6,
            "direct_unsat": 994, "direct_sat": 6,
            "agreement": "EXACT_ON_FROZEN_PREFIX_1000",
        },
        "sample_direct_feasibility": {
            "epistemic_status": "OBSERVED", "states": 100_000,
            "rejected_states": 85_594, "retained_states": 14_406,
            "rejection_fraction": 0.85594, "resource_workers": 3,
            "independent_h11_direct_oracle_rows": 96,
        },
        "cycle_decision": {
            "outcome": "SEALED_FOR_DISTINCT_DIRECT_ENGINE",
            "companion_identity": "/root/decision_companion_2",
            "recommendation": "Seal Cycle 6; direct exact r-translate feasibility is a stronger method family and opens a distinct Cycle 7.",
            "flaw": "The 1000-state agreement does not establish equivalence, and direct feasibility is not an independent validation of the triple encoding.",
            "falsifier": "A fixed state where direct feasibility and declared triple weak-colorability disagree, or a reproducible direct-witness validation failure.",
            "next_action": "Preregister Cycle 7 for direct exact r-translate feasibility with stratified triple comparisons and frontier caps.",
        },
        "runtime": {**runtime, "compiler": compiler},
        "frozen_hashes": frozen,
        "replay": {
            "triple_oracle_command": "python3 discovery/check_lrc_triple_hypergraph.py --h11-oracle",
            "direct_oracle_command": "python3 proof/check_cycle_6_direct_oracle.py",
            "check_command": "python3 proof/build_cycle_6_lrc_triple_hypergraph.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_6_lrc_triple_hypergraph.py -v",
        },
        "sealer": {"path": "proof/build_cycle_6_lrc_triple_hypergraph.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
