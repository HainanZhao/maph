#!/usr/bin/env python3
"""Seal the same-cubic-grid rotation obstruction addendum to Cycle 11."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256  # noqa: E402
from proof.verify_lane_b_grid_rotation_robustness import verify  # noqa: E402


OUTPUT = ROOT / "artifacts/cycle-11-b10-lane-b-embedding-robustness-v2.json"
HASHES = {
    "prior_v1": ("artifacts/cycle-11-b10-lane-b-embedding-robustness-v1.json", "9dc1774c262c373e6ba5cea02bbe5055561071f73893100955d4abd95249e361"),
    "report": ("docs/cycle11-lane-b-grid-rotation-addendum-v2.md", "fc271f75bd6d59ee07fa8ddb7df5df86f5b10c355456b66ad361cf6853bbc7b0"),
    "proof": ("proof/lane_b_grid_rotation_addendum.md", "266664df79cc9d60e4110946507457c5b8093d17500c087d8480886cdaf4cc16"),
    "verifier": ("proof/verify_lane_b_grid_rotation_robustness.py", "4f6d04f1939855d0d4a593858029d49e0de401b364b602f5e79b2a62aa53e434"),
    "tests": ("tests/test_lane_b_grid_rotation_robustness.py", "f5414e136f82ed71a770aaa705a44423ab0346161a35696c57a6559d52d4ac1e"),
    "frontier_dependency": ("proof/verify_lane_b_arbitrary_width_frontier.py", "f98f80b203eb93bd0c18deb37e80dbf7cdcbb58237129cba60c42cff3fa73615"),
    "homology_dependency": ("proof/verify_lane_b_genus3.py", "1f5a944a1249525ff75b4a471da73e55709de169f0e53d0540ede14b1bb298a4"),
    "intersection_dependency": ("proof/verify_lane_b_intersection.py", "1b6b59d188dfdc033b1c37c0059ee3e068181c458a9da028d0a8e0f1a273abd9"),
    "conventions": ("src/conventions.py", "b6b328f6b7b1725c39f4e4ba4084c275a141189b7efe32e9727c75488d705bb3"),
    "requirements": ("requirements.txt", "8347daed02ebf7b3c3cfa494e97049b7e0ab15b9af00a5addd843ed44381a64a"),
    "scaffold": ("proof/cycle_seal_v1.py", "c4a09e7baa8a5588d4c6855a533eb933c85791707ed9653437644c1e1ad6c163"),
}


def payload() -> dict[str, object]:
    replay = verify()
    census = replay["rotation_census"]
    if census != {"0": 2, "1": 54, "2": 200}:
        raise RuntimeError("cube rotation census regressed")
    return {
        "artifact_id": "cycle-11-b10-lane-b-embedding-robustness-v2",
        "author": "Hainan Zhao",
        "budget_ordinal": "B10",
        "cycle": 11,
        "status": "SEALED_ADDENDUM",
        "epistemic_status": "MIXED_PROVED_AND_CERTIFIED_NUMERICAL",
        "record_type": "LANE_B_SAME_GRID_ROTATION_OBSTRUCTION_ADDENDUM",
        "extends": "cycle-11-b10-lane-b-embedding-robustness-v1",
        "outcome": (
            "The same cube grid graph has orientable cellular rotations of genera zero, one, "
            "and two; selected genus-zero and genus-two rotations have pre-Arf family sizes "
            "one and sixteen while preserving the physical Arf contraction."
        ),
        "gate_outcome": "UPGRADE_4_COMPLETE_WITH_EXPLICIT_SAME_GRID_ROTATIONS",
        "claim_boundary": (
            "This strengthens only the embedding-dependence obstruction. It does not alter "
            "the filtration-compatible robustness theorem or the physical Ising polynomial."
        ),
        "exact_replay": replay,
        "frozen_hashes": freeze_inputs(
            ROOT, {label: (ROOT / path, digest) for label, (path, digest) in HASHES.items()}
        ),
        "runtime": check_runtime("cycle-11-grid-rotation-addendum-v2"),
        "sealer": {
            "path": "proof/build_cycle11_lane_b_grid_rotation_addendum_v2.py",
            "sha256": sha256(Path(__file__)),
        },
        "replay": {
            "verification": "python3 proof/verify_lane_b_grid_rotation_robustness.py",
            "tests": "python3 -m unittest tests/test_lane_b_grid_rotation_robustness.py -v",
            "artifact_check": "python3 proof/build_cycle11_lane_b_grid_rotation_addendum_v2.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
