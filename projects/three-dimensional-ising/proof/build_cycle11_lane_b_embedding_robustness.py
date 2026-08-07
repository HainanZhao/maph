#!/usr/bin/env python3
"""Seal the embedding-robustness theorem and K3,3 rotation obstruction."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256  # noqa: E402
from proof.verify_lane_b_embedding_robustness import verify  # noqa: E402


OUTPUT = ROOT / "artifacts/cycle-11-b10-lane-b-embedding-robustness-v1.json"
HASHES: dict[str, tuple[str, str]] = {
    "prior": ("artifacts/cycle-10-b9-abstract-separator-k33-sharpness-v1.json", "c85caf6df8bf59c77b5ff5b38d772e69ac39b43bc9147c3886880f4a76ec27c8"),
    "selection": ("discovery/cycle-11-embedding-robustness-selection.md", "1818cc35aa856d9224feeb3f53310a987fcc2aeb0c7d8ee61287fc5fd1585c60"),
    "failure_ledger": ("discovery/failure-ledger-cycle11.md", "7640e8f1972922a4e89813aec295e3ac63c3d4f9a7519f49b347022f0e67492d"),
    "report": ("docs/cycle11-lane-b-embedding-robustness.md", "92ddc1da1fbc0024221aaeabc830f59fdefe745cd643cdad4aea19a68ea0fffe"),
    "proof": ("proof/lane_b_embedding_robustness.md", "403784d0679692ce21bd32541b0a835cb3be25b2bfc512d5457c03a849728fa7"),
    "verifier": ("proof/verify_lane_b_embedding_robustness.py", "0f7617765e280bdc1ea6b95ffd00c96cf8bd0bc1f19aa73cd772bf12fba59dd3"),
    "tests": ("tests/test_lane_b_embedding_robustness.py", "68312d1cef177e98b7fd59b413baf4a1d70592a784584b85e44b60e1459f6689"),
    "frontier_dependency": ("proof/verify_lane_b_arbitrary_width_frontier.py", "f98f80b203eb93bd0c18deb37e80dbf7cdcbb58237129cba60c42cff3fa73615"),
    "homology_dependency": ("proof/verify_lane_b_genus3.py", "1f5a944a1249525ff75b4a471da73e55709de169f0e53d0540ede14b1bb298a4"),
    "intersection_dependency": ("proof/verify_lane_b_intersection.py", "1b6b59d188dfdc033b1c37c0059ee3e068181c458a9da028d0a8e0f1a273abd9"),
    "conventions": ("src/conventions.py", "b6b328f6b7b1725c39f4e4ba4084c275a141189b7efe32e9727c75488d705bb3"),
    "requirements": ("requirements.txt", "8347daed02ebf7b3c3cfa494e97049b7e0ab15b9af00a5addd843ed44381a64a"),
    "scaffold": ("proof/cycle_seal_v1.py", "c4a09e7baa8a5588d4c6855a533eb933c85791707ed9653437644c1e1ad6c163"),
}


def payload() -> dict[str, object]:
    replay = verify()
    by_rotation = {}
    for row in replay["rows"]:
        by_rotation.setdefault(row["rotation"], set()).add(
            (row["genus"], row["spin_structure_count"])
        )
        if not row["physical_values_agree"]:
            raise RuntimeError("embedding-invariant physical contraction regressed")
    if by_rotation != {
        "minimum_genus_one": {(1, 4)},
        "maximum_genus_two": {(2, 16)},
    }:
        raise RuntimeError("rotation-system obstruction regressed")
    return {
        "artifact_id": "cycle-11-b10-lane-b-embedding-robustness-v1",
        "author": "Hainan Zhao",
        "budget_ordinal": "B10",
        "cycle": 11,
        "status": "SEALED",
        "epistemic_status": "MIXED_PROVED_AND_CERTIFIED_NUMERICAL",
        "record_type": "LANE_B_EMBEDDING_ROBUSTNESS_CLASSIFICATION",
        "outcome": (
            "The separator bound is invariant under filtration-compatible homeomorphisms, "
            "gauge/completion changes, and cut-local coordinate changes. Gauge-redundant "
            "stabilization is rank one but noncellular; arbitrary rotation changes can alter "
            "genus and the dimension of the complete pre-Arf tensor."
        ),
        "gate_outcome": "UPGRADE_4_COMPLETE",
        "claim_boundary": (
            "No invariance under arbitrary embeddings or cross-cut symplectic mixing is claimed. "
            "The normalized physical Arf contraction remains the same Ising polynomial."
        ),
        "theorem": {
            "positive_class": "filtration-compatible embedded separator data satisfying H1-H3",
            "stabilization": "rank-one if disjoint from graph; necessarily noncellular",
            "cellular_obstruction": "H_1(graph)->H_1(surface) is surjective",
            "rotation_counterexample": "K3,3 genus 1 versus genus 2; 4 versus 16 spin structures",
        },
        "exact_replay": replay,
        "frozen_hashes": freeze_inputs(
            ROOT, {label: (ROOT / path, digest) for label, (path, digest) in HASHES.items()}
        ),
        "runtime": check_runtime("cycle-11-lane-b-embedding-robustness"),
        "sealer": {
            "path": "proof/build_cycle11_lane_b_embedding_robustness.py",
            "sha256": sha256(Path(__file__)),
        },
        "replay": {
            "verification": "python3 proof/verify_lane_b_embedding_robustness.py",
            "tests": "python3 -m unittest tests/test_lane_b_embedding_robustness.py -v",
            "artifact_check": "python3 proof/build_cycle11_lane_b_embedding_robustness.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
