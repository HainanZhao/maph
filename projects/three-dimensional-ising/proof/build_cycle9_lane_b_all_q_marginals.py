#!/usr/bin/env python3
"""Seal the exact all-spin-structure Walsh-marginal algorithm."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256  # noqa: E402
from proof.verify_lane_b_all_q_marginals import verify  # noqa: E402


OUTPUT = ROOT / "artifacts/cycle-9-b8-lane-b-all-q-marginals-v1.json"
HASHES: dict[str, tuple[str, str]] = {
    "prior": ("artifacts/cycle-7-b7-lane-b-arbitrary-width-closure-v1.json", "3caa6e9e2a170b6de7660a158719c762d733dcc9f022707143d6ff2aaa80320c"),
    "selection": ("discovery/cycle-9-all-q-marginal-selection.md", "d9783df1f3d7cd1040df62be4e27a6b3997e9d393d7974cb0bc487beb126fb8a"),
    "report": ("docs/cycle9-lane-b-all-q-marginals.md", "2b4878a3d3742d02ba11b32a66fd58c2d30c8a9ea08604096f23040bf4fd1fe9"),
    "proof": ("proof/lane_b_all_q_marginal_algorithm.md", "2db827bb258786ba4672a33bd8fc101f6faecc25ef859a2a86cb62491884c378"),
    "verifier": ("proof/verify_lane_b_all_q_marginals.py", "ad582ba38c3628024d0e160578d1d04b3798eef66718c158f4d5feb86e03ddcb"),
    "tests": ("tests/test_lane_b_all_q_marginals.py", "5d4ce771c82f1e41a895798221ba0e40a3de02fee9e6ac2abe2eb17fbc07b65f"),
    "canonical_dependency": ("proof/verify_lane_b_universal_canonical_ranks.py", "d631149c9429d921359a6a67042b0e476cb681b9bc8aa63de42bcac6503662b0"),
    "frontier_dependency": ("proof/verify_lane_b_arbitrary_width_frontier.py", "f98f80b203eb93bd0c18deb37e80dbf7cdcbb58237129cba60c42cff3fa73615"),
    "width_dependency": ("proof/verify_lane_b_width_scaling.py", "2cb86284481e69b26bea8d9f7a52e91664a7b2b7869cdf1915795bef18926ae4"),
    "transfer_engine": ("proof/lane_b_width4_character_transfer.cpp", "dd7f5f3e381ae3759eaa8d86a930d968ab3ac75773646ba69c52d59f77e1d940"),
    "conventions": ("src/conventions.py", "b6b328f6b7b1725c39f4e4ba4084c275a141189b7efe32e9727c75488d705bb3"),
    "embedding": ("src/lane_b_universal_embedding.py", "62e57075103f4f2f252f30f9bd1e01c63820656455900b6db0b875e5294ab430"),
    "requirements": ("requirements.txt", "8347daed02ebf7b3c3cfa494e97049b7e0ab15b9af00a5addd843ed44381a64a"),
    "scaffold": ("proof/cycle_seal_v1.py", "c4a09e7baa8a5588d4c6855a533eb933c85791707ed9653437644c1e1ad6c163"),
}


def payload() -> dict[str, object]:
    replay = verify()
    replay.pop("wall_seconds", None)
    if len(replay["rows"]) != 4 or not all(row["direct_enumeration_agrees"] for row in replay["rows"]):
        raise RuntimeError("all-q two-prime validation regression")
    return {
        "artifact_id": "cycle-9-b8-lane-b-all-q-marginals-v1",
        "author": "Hainan Zhao",
        "budget_ordinal": "B8",
        "cycle": 9,
        "status": "SEALED",
        "epistemic_status": "MIXED_PROVED_AND_CERTIFIED_NUMERICAL",
        "record_type": "LANE_B_ALL_Q_ALGORITHMIC_APPLICATION",
        "outcome": (
            "All four single-handle Walsh marginals at every canonical handle, under arbitrary "
            "product-form sector weights, are obtained by two TT environment sweeps in "
            "O(g*4*d_w^2) dense ring operations."
        ),
        "gate_outcome": "UPGRADE_3_COMPLETE",
        "claim_boundary": (
            "The advantage is over explicit all-sector evaluation for these 4g family "
            "observables. It is not an advantage over ordinary transfer for one physical Z, "
            "and it gives no thermodynamic or critical-temperature result."
        ),
        "theorem": {
            "input": "exact four-state all-q TT with bond at most d_w",
            "output": "4g product-weighted single-handle Walsh marginals",
            "dense_ring_operations": "O(g*4*d_w^2)",
            "explicit_sector_baseline": "Omega(4^g) tensor entries",
        },
        "exact_replay": replay,
        "frozen_hashes": freeze_inputs(
            ROOT, {label: (ROOT / path, digest) for label, (path, digest) in HASHES.items()}
        ),
        "runtime": check_runtime("cycle-9-lane-b-all-q-marginals"),
        "sealer": {
            "path": "proof/build_cycle9_lane_b_all_q_marginals.py",
            "sha256": sha256(Path(__file__)),
        },
        "replay": {
            "verification": "python3 proof/verify_lane_b_all_q_marginals.py",
            "tests": "python3 -m unittest tests/test_lane_b_all_q_marginals.py -v",
            "artifact_check": "python3 proof/build_cycle9_lane_b_all_q_marginals.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
