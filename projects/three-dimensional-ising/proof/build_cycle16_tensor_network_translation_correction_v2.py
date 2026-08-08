#!/usr/bin/env python3
"""Correct the tensor-network record to depend on authoritative Cycle 14 v2."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256  # noqa: E402

OUTPUT = ROOT / "artifacts/cycle-16-b16-tensor-network-translation-v2.json"
HASHES = {
    "translation": ("proof/tensor_network_translation_note.md", "547458b822e05f619fe118177a49e80b1fc40d5221866a2854b48af96148ef90"),
    "separator_theorem": ("proof/abstract_spin_structure_separator_theorem.md", "5baa6fa7038133c498c34719f25ccf8de311cce2e2920d6c07ffa0511ed82c9c"),
    "polynomial_tt": ("proof/polynomial_tt_telescoping_proof.md", "c55df74246996d493579d0bfca300e993b54fe596316212d6e87e31d9d26b399"),
    "marginals": ("proof/lane_b_all_q_marginal_algorithm.md", "2db827bb258786ba4672a33bd8fc101f6faecc25ef859a2a86cb62491884c378"),
    "phase0_artifact": ("artifacts/cycle-13-b13-polynomial-tt-grid-cores-v1.json", "741e1f910177542255157d041cc3dc70998002dca23c2a7040f06d32ab3e6fa4"),
    "homogeneous_artifact_v2": ("artifacts/cycle-14-b14-homogeneous-w3-v2.json", "372e887252210e8084d122c100c0293c28f34ff2efbbc71ff51b9e98d9f831bb"),
    "correction": ("discovery/cycle16-translation-dependency-correction.md", "e5fbe81e0c256b34d671b0b9f47874093f020662bc0fb1c874b08d903ad82d0b"),
    "v1_artifact": ("artifacts/cycle-16-b16-tensor-network-translation-v1.json", "63b2c1117c07d8500b186edd9b609fcbc6cf6d49e97b8d35752b7dc6d2b81710"),
    "v1_builder": ("proof/build_cycle16_tensor_network_translation.py", "ebd5b2656ac205fd772381211e2dae1f32fd173d40eec20924200d54512fc452"),
    "scaffold": ("proof/cycle_seal_v1.py", "c4a09e7baa8a5588d4c6855a533eb933c85791707ed9653437644c1e1ad6c163"),
}


def payload():
    return {
        "artifact_id": "cycle-16-b16-tensor-network-translation-v2",
        "author": "Hainan Zhao",
        "budget_ordinal": "B16",
        "cycle": 16,
        "status": "SEALED",
        "supersedes": "cycle-16-b16-tensor-network-translation-v1",
        "correction": {"error": "v1 depended on corrected Cycle 14 v1", "affected_claims": "none", "mathematical_fields_changed": False},
        "epistemic_status": "PROVED_TRANSLATION_ONLY",
        "record_type": "TENSOR_NETWORK_DICTIONARY_CORRECTION",
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
        "runtime": check_runtime("cycle-16-tensor-network-translation-v2"),
        "sealer": {"path": "proof/build_cycle16_tensor_network_translation_correction_v2.py", "sha256": sha256(Path(__file__))},
        "replay": {"artifact_check": "python3 proof/build_cycle16_tensor_network_translation_correction_v2.py --check"}
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
