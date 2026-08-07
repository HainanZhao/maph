#!/usr/bin/env python3
"""Seal the Lane B genus-three physical rank-seven reduction."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.cycle_seal_v1 import (  # noqa: E402
    check_runtime,
    freeze_inputs,
    run_cli,
    sha256,
)
from proof.verify_lane_b_genus3 import verify as verify_genus3  # noqa: E402
from proof.verify_lane_b_intersection import verify as verify_intersection  # noqa: E402
from proof.verify_lane_b_physical_ranks import verify as verify_physical_ranks  # noqa: E402


OUTPUT = ROOT / "artifacts/cycle-3-b3-lane-b-rank-seven-v1.json"
HASHES = {
    "prior": (
        "artifacts/cycle-2-b2-five-lane-boundary-v1.json",
        "1b755981bc3be805b0316a0da2f9ca9b437b836b62413f5f6946cc5c3bec036b",
    ),
    "selection": (
        "discovery/cycle-3-lane-b-selection.md",
        "40f50bbaa85b6aea30ee942562f36fc1d6aaa0489dc3e6d08932de007402ac96",
    ),
    "failure_ledger": (
        "discovery/failure-ledger-cycle3.md",
        "348b38ad07137841dffa4ce30580cb964241e1279f0a813de7a658291ac28e60",
    ),
    "report": (
        "docs/cycle3-lane-b-report.md",
        "dad69b289f96db15e1d56ec2571edfc41c6ffd525b073ea1faea5a3c36b78fc8",
    ),
    "conventions": (
        "src/conventions.py",
        "b6b328f6b7b1725c39f4e4ba4084c275a141189b7efe32e9727c75488d705bb3",
    ),
    "prior_embedding": (
        "src/embeddings.py",
        "ebc9f3839f74d4590bcd853913b69ca4effc5a5a44e415203bfffca30092dada",
    ),
    "genus3_embedding": (
        "src/lane_b_genus3.py",
        "9129a873a842fceb4744fd41a6ebb2c2c83d0c62b8a1f9c673ba90d725bf265f",
    ),
    "stage1_dependency": (
        "proof/verify_stage1_baseline.py",
        "c9532a798f89eba96e0b26135f7c8dd807607a771a0dedd286050cf6cd93b7ab",
    ),
    "cycle2_dependency": (
        "proof/verify_cycle2_five_lanes.py",
        "b5f1db0718b9b1677083545af66ebc88e5ebae390a67a203c5da899e77bdc038",
    ),
    "genus3_verifier": (
        "proof/verify_lane_b_genus3.py",
        "1f5a944a1249525ff75b4a471da73e55709de169f0e53d0540ede14b1bb298a4",
    ),
    "intersection_verifier": (
        "proof/verify_lane_b_intersection.py",
        "1b6b59d188dfdc033b1c37c0059ee3e068181c458a9da028d0a8e0f1a273abd9",
    ),
    "rank_verifier": (
        "proof/verify_lane_b_physical_ranks.py",
        "a85a434b905babf15428869762a91f6a000329fb481c79793b992b121d8ffa47",
    ),
    "rank_search": (
        "proof/lane_b_symplectic_rank_search.cpp",
        "67f076167b3473c9246c99bcba0515b42f1a33a21e21fc851342568ca0f81ab8",
    ),
    "genus3_tests": (
        "tests/test_lane_b_genus3.py",
        "5c5bf345b37187e6e4c13bac569abf876b152562a1973e6a9a225c50fb1b04a3",
    ),
    "intersection_tests": (
        "tests/test_lane_b_intersection.py",
        "a7126ec309f77224fb85608bdf31d2293d2c02279f2bef69df2713cfc91ba422",
    ),
    "rank_tests": (
        "tests/test_lane_b_physical_ranks.py",
        "fac1b4b9602c81feebb6389680b6193dedc902eee88c5218dc2feab55cfe482a",
    ),
    "artifact_tests": (
        "tests/test_cycle3_lane_b_rank_reduction.py",
        "810f96b876adbbbf4f7d26d86ee38274365c29b44be8504b50d05219f928b1d7",
    ),
    "requirements": (
        "requirements.txt",
        "8347daed02ebf7b3c3cfa494e97049b7e0ab15b9af00a5addd843ed44381a64a",
    ),
    "scaffold": (
        "proof/cycle_seal_v1.py",
        "c4a09e7baa8a5588d4c6855a533eb933c85791707ed9653437644c1e1ad6c163",
    ),
}


def payload() -> dict[str, object]:
    genus3 = verify_genus3()
    intersection = verify_intersection()
    ranks = verify_physical_ranks()
    if genus3["minimum_genus_certificate"]["minimum_orientable_genus"] != 3:
        raise RuntimeError("minimum-genus certificate regression")
    box_intersection = intersection["genus_three_box"]
    if box_intersection["intersection_matrix_rows"] != [38, 25, 1, 2, 34, 17]:
        raise RuntimeError("physical intersection matrix regression")
    if not box_intersection["independent_routes_agree_with_labels"]:
        raise RuntimeError("intersection routes no longer agree")
    witness = ranks["exact_rank_seven_survivor"]
    if witness["generic_TT_rank_over_Q(t)"] != [2, 4, 7, 4, 2]:
        raise RuntimeError("rank-seven witness regression")
    if ranks["rank_reduction_symmetry_derivation"]["derived_flattening_identity"] != (
        "row_4 = row_6 for all eight columns"
    ):
        raise RuntimeError("symmetry derivation regression")
    for evaluation in ranks["evaluations"].values():
        search = evaluation["symplectic_search"]
        if search["symplectic_bases"] != 1_451_520:
            raise RuntimeError("incomplete Sp(6,2) enumeration")
        if search["profiles"] != {
            "2,4,7,4,2": 138_240,
            "2,4,8,4,2": 1_313_280,
        }:
            raise RuntimeError("symplectic rank profile census regression")
    return {
        "artifact_id": "cycle-3-b3-lane-b-rank-seven-v1",
        "author": "Hainan Zhao",
        "budget_ordinal": "B3",
        "cycle": 3,
        "status": "SEALED",
        "epistemic_status": "COMPUTATIONALLY_VERIFIED",
        "record_type": "LANE_B_PHYSICAL_SPIN_STRUCTURE_RANK_REDUCTION",
        "outcome": (
            "For the minimum-genus-three free 4x3x3 cubic box, an exact homology-frontier "
            "engine reduces 2^40 cycle enumeration to at most 16384 live states. Two "
            "independent labeled routes recover the physical intersection form. Exhaustion "
            "of all 1451520 ordered symplectic bases finds a basis with exact generic TT "
            "profile (2,4,7,4,2); the rank-seven row identity is derived from the y-z graph "
            "swap symmetry and certified by nonzero exact 7x7 minors."
        ),
        "success_level": 2,
        "gate_outcome": "GATE_2_POSITIVE_FINITE_INSTANCE_COMPRESSION",
        "claim_boundary": (
            "The rank reduction is exact for the pinned finite graph and tensor class. No "
            "size-uniform rank bound, held-out growing-genus recurrence, controlled "
            "thermodynamic limit, critical datum, or exact solution is claimed. The modular "
            "census proves full rank when full, but only the displayed survivor is promoted "
            "to an exact Q(t) rank-seven theorem in this artifact."
        ),
        "falsifier": (
            "Any frozen replay mismatch; disagreement of the cup and tree-cotree matrices; "
            "failure of the coefficientwise row identity; vanishing of both exact 7x7 minor "
            "witnesses; or an Sp(6,2) enumeration count other than 1451520."
        ),
        "exact_replay": {
            "genus_three_sectors": genus3,
            "physical_intersection": intersection,
            "physical_symplectic_ranks": ranks,
        },
        "frozen_hashes": freeze_inputs(
            ROOT, {label: (ROOT / path, digest) for label, (path, digest) in HASHES.items()}
        ),
        "runtime": check_runtime("cycle-3-lane-b-rank-seven"),
        "sealer": {
            "path": "proof/build_cycle3_lane_b_rank_reduction.py",
            "sha256": sha256(Path(__file__)),
        },
        "replay": {
            "genus_three": "python3 proof/verify_lane_b_genus3.py",
            "intersection": "python3 proof/verify_lane_b_intersection.py",
            "physical_ranks": "python3 proof/verify_lane_b_physical_ranks.py",
            "tests": "python3 -m unittest discover -s tests -v",
            "artifact_check": "python3 proof/build_cycle3_lane_b_rank_reduction.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
