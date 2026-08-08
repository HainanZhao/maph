#!/usr/bin/env python3
"""Seal the theorem-preserving tensor-network translation."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256  # noqa: E402


OUTPUT = ROOT / "artifacts/cycle-16-b16-tensor-network-translation-v1.json"
HASHES = {
    "translation": ("proof/tensor_network_translation_note.md", "547458b822e05f619fe118177a49e80b1fc40d5221866a2854b48af96148ef90"),
    "separator_theorem": ("proof/abstract_spin_structure_separator_theorem.md", "5baa6fa7038133c498c34719f25ccf8de311cce2e2920d6c07ffa0511ed82c9c"),
    "polynomial_tt": ("proof/polynomial_tt_telescoping_proof.md", "c55df74246996d493579d0bfca300e993b54fe596316212d6e87e31d9d26b399"),
    "marginals": ("proof/lane_b_all_q_marginal_algorithm.md", "2db827bb258786ba4672a33bd8fc101f6faecc25ef859a2a86cb62491884c378"),
    "phase0_artifact": ("artifacts/cycle-13-b13-polynomial-tt-grid-cores-v1.json", "741e1f910177542255157d041cc3dc70998002dca23c2a7040f06d32ab3e6fa4"),
    "homogeneous_artifact": ("artifacts/cycle-14-b14-homogeneous-w3-v1.json", "62cf5108cb41ed46f8f4125723dc091729e03795f379387ee31ba43a5a393098"),
    "failure_ledger": ("discovery/failure-ledger-cycle16.md", "6619fab2738066e3f40096182fc5f2ee767015fcb7c8d4494ab28bc11a75301d"),
    "scaffold": ("proof/cycle_seal_v1.py", "c4a09e7baa8a5588d4c6855a533eb933c85791707ed9653437644c1e1ad6c163"),
}


def payload():
    return {
        "artifact_id": "cycle-16-b16-tensor-network-translation-v1",
        "author": "Hainan Zhao",
        "budget_ordinal": "B16",
        "cycle": 16,
        "status": "SEALED",
        "epistemic_status": "PROVED_TRANSLATION_ONLY",
        "record_type": "TENSOR_NETWORK_DICTIONARY",
        "outcome": "Existing separator, polynomial-TT, homogeneous-width-three, and marginal theorems are stated in exact MPS/MPO language without adding claims.",
        "gate_outcome": "T6_COMPLETE",
        "claim_boundary": "No new tensor-network theorem, asymptotic compression, or single-partition-function speedup is claimed.",
        "dictionary": {
            "handle": "four-state physical index",
            "separator_mask": "virtual index",
            "H1_H2_H3": "virtual gauge and phase-locality conditions",
            "marginals": "left/right environment sweep",
            "cubic_box_bond": "2^(L^2-1)"
        },
        "frozen_hashes": freeze_inputs(ROOT, {k: (ROOT / p, h) for k, (p, h) in HASHES.items()}),
        "runtime": check_runtime("cycle-16-tensor-network-translation"),
        "sealer": {"path": "proof/build_cycle16_tensor_network_translation.py", "sha256": sha256(Path(__file__))},
        "replay": {"artifact_check": "python3 proof/build_cycle16_tensor_network_translation.py --check"}
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
