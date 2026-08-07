#!/usr/bin/env python3
"""Seal the all-size fixed-transverse Lane B compression theorem."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from proof.cycle_seal_v1 import check_runtime,freeze_inputs,run_cli,sha256  # noqa: E402
from proof.verify_lane_b_character_transfer import verify as verify_character  # noqa: E402
from proof.verify_lane_b_heldout import verify as verify_heldout  # noqa: E402
from proof.verify_lane_b_recursive import verify as verify_recursive  # noqa: E402
from proof.verify_lane_b_recursive6 import verify as verify_recursive6  # noqa: E402
from proof.verify_lane_b_recursive_family import verify as verify_family  # noqa: E402


OUTPUT=ROOT/"artifacts/cycle-4-b4-lane-b-bounded-theta-transfer-v1.json"
HASHES={
    "prior":("artifacts/cycle-3-b3-lane-b-rank-seven-v1.json","b9d95dee5f70ef35c79dbbfb1852e430d3e732d0e03b9449da08b4fb6ee7a3d3"),
    "selection":("discovery/cycle-4-lane-b-heldout-selection.md","c1ab37c01c9ebd019402c94a5dad97ad1d79feaf11b1c9bd92d175c276f752b2"),
    "relative_note":("discovery/cycle-4-relative-theta-bridge.md","4ca5ae3017a1316e1288a863c3d7eb5355849ae59541755dfcca59ecca9c7354"),
    "source_audit":("discovery/cycle4-grid-genus-source-audit.md","2add7bc695f4906edde4e27bf49aa225be6a9ca21efe2569ae0908ef4de6dc09"),
    "failure_ledger":("discovery/failure-ledger-cycle4.md","966a2ad5b3b6202184373e16b34a983bfa7417b5d327e7550f54afce707f3191"),
    "report":("docs/cycle4-lane-b-recursive-compression-report.md","3ba93b80e5779ec65e2717300e4b925af2cf4773e491b6b5c652d4d80c040d78"),
    "proof_note":("proof/lane_b_bounded_theta_transfer_proof.md","fdd7eafd3611d9146c816675310d46111646d2dcd30255a4683a2cbfa70b70cb"),
    "conventions":("src/conventions.py","b6b328f6b7b1725c39f4e4ba4084c275a141189b7efe32e9727c75488d705bb3"),
    "genus3_rotation":("src/lane_b_genus3.py","9129a873a842fceb4744fd41a6ebb2c2c83d0c62b8a1f9c673ba90d725bf265f"),
    "recursive5_rotation":("src/lane_b_recursive.py","20c7faea3b243ec2ed6e3d8c2b9761fd1cada6c9b3a8ad5fc1f0faa9cee2166c"),
    "recursive6_rotation":("src/lane_b_recursive6.py","a615b8a745e8aee78398e6fa1fdfcc78a8ce3800c92c471a6ebde90be9a86b61"),
    "recursive_family":("src/lane_b_recursive_family.py","2c945132811228cb33acc8a98d1602d3e7133c474b219ceaab73a4e8e72b171e"),
    "heldout_verifier":("proof/verify_lane_b_heldout.py","2fc2105a9bf295e88bd222111b67c990685ecf3fbfb4102195a4d56a9be7d213"),
    "recursive5_verifier":("proof/verify_lane_b_recursive.py","92f232cf1040be67598df6d210e80002b51974153798ba7390e31fc33a3841ac"),
    "recursive6_verifier":("proof/verify_lane_b_recursive6.py","e1bdf6675e1fb8869a02f2ee2a378fcfccb2403e55d41aa3740a6449aeae22cc"),
    "family_verifier":("proof/verify_lane_b_recursive_family.py","1f5bc7cefc988cf14234631ec887248120eaebce2c430e5b2e4d443a0e62a400"),
    "character_verifier":("proof/verify_lane_b_character_transfer.py","6f5dd13a4e21243e86f8914842c081a9fc70ae2b0eea3f0c4ed69054c3058234"),
    "genus4_no_cover":("proof/verify_lane_b_genus4_no_cover_6x3x3.cpp","574304a693ebbaab2825a66e702264b74103c460d48d10a4fd715884a69baa11"),
    "heldout_tests":("tests/test_lane_b_heldout.py","131d8ca37a4868683131be7c56c9cd984eadb8eb1b10b11d32e6ad5d6044ce96"),
    "recursive5_tests":("tests/test_lane_b_recursive.py","f591367929b8ac04ef205934b9d2d3f899d0db8b227ed2aa99f0c54cc7d57921"),
    "recursive6_tests":("tests/test_lane_b_recursive6.py","4841f729d71e839b09c5ea1c4c9855e5f93bf4fbeb821689d0785ae23d950364"),
    "family_tests":("tests/test_lane_b_recursive_family.py","c310b50cede5fde223d7dd85fd5e4363f84281a1eec6626c0ffec22bf68cb1ed"),
    "character_tests":("tests/test_lane_b_character_transfer.py","87142532b85f41a121bb517425fd037462899589bc4c9a09bdacf4ee15af9778"),
    "artifact_tests":("tests/test_cycle4_lane_b_recursive_compression.py","926b98c9e31e809c1a705bee082b192369940de1655f2872b039f7928dc4df11"),
    "requirements":("requirements.txt","8347daed02ebf7b3c3cfa494e97049b7e0ab15b9af00a5addd843ed44381a64a"),
    "scaffold":("proof/cycle_seal_v1.py","c4a09e7baa8a5588d4c6855a533eb933c85791707ed9653437644c1e1ad6c163"),
}


def payload()->dict[str,object]:
    heldout=verify_heldout()
    recursive=verify_recursive()
    recursive6=verify_recursive6()
    family=verify_family()
    character=verify_character()
    if heldout["gate_outcome"]!="DIRECT_HANDLE_EXTENSION_FALSIFIED":
        raise RuntimeError("held-out direct-extension falsifier regression")
    if recursive["relative_boundary"]["defect_dimension"]!=1:
        raise RuntimeError("first relative defect regression")
    if recursive6["minimum_genus_certificate"]["minimum_orientable_genus"]!=5:
        raise RuntimeError("length-six minimum-genus regression")
    if recursive6["recurrence_control"]!={
        "steps_compared":["4->5","5->6"],
        "boundary_defect_dimensions":[1,1],
        "active_topological_window_widths":[3,3],
        "added_edge_semantic_pattern_repeats":True,
    }:
        raise RuntimeError("held-out recursive pattern regression")
    transfer=family["collective_transfer"]
    if transfer["uniform_handle_site_TT_rank_upper_bound"]!=1024:
        raise RuntimeError("uniform handle-site TT bound regression")
    if transfer["uniform_binary_site_TT_rank_upper_bound"]!=2048:
        raise RuntimeError("uniform binary-site TT bound regression")
    if family["minimum_genus_theorem"]["minimum_genus_formula"]!="L-1":
        raise RuntimeError("all-size minimum-genus theorem regression")
    if not all(
        evaluation["all_agree"]
        for case in character["cases"]
        for evaluation in case["evaluations"]
    ):
        raise RuntimeError("independent character transfer mismatch")
    return {
        "artifact_id":"cycle-4-b4-lane-b-bounded-theta-transfer-v1",
        "author":"Hainan Zhao",
        "budget_ordinal":"B4",
        "cycle":4,
        "status":"SEALED",
        "epistemic_status":"PROVED",
        "record_type":"LANE_B_MINIMUM_GENUS_BOUNDED_RELATIVE_THETA_TRANSFER",
        "outcome":(
            "For every free Lx3x3 box with L>=4, a period-two minimum-genus rotation "
            "gives an exact nested relative-homology recurrence. The full 4^(L-1) Walsh "
            "tensor, and hence the full F(q) tensor, has handle-site TT rank at most 1024 "
            "and binary-site TT rank at most 2048 uniformly in L. Direct storage is "
            "exponential in L; the exact representation uses "
            "bounded local matrices and O(L) cores."
        ),
        "success_level":2,
        "gate_outcome":"GATES_3_AND_4_POSITIVE_FIXED_TRANSVERSE_COMPRESSION",
        "claim_boundary":(
            "The theorem is for free boxes with fixed 3x3 transverse section. It does not "
            "cover growing transverse dimensions, periodic or antiperiodic closure, the full "
            "three-dimensional thermodynamic limit, beta_c, or critical exponents. The 3D "
            "Ising model is not solved."
        ),
        "falsifier":(
            "Any frozen replay failure; mismatch in either local rotation/label table; failure "
            "of the Millichap--Salinas Theorem 4 hypothesis map; disagreement of the two "
            "intersection routes; failure of the independent character-transfer controls; or "
            "a handle-cut rank above 1024 or binary-site TT rank above 2048."
        ),
        "novelty_boundary":(
            "The minimum-genus formula is prior work. No priority claim is made here for the "
            "period-two nested-homology or bounded-TT construction pending a dedicated search."
        ),
        "exact_replay":{
            "independent_heldout_falsifier":heldout,
            "first_relative_step":recursive,
            "second_relative_step":recursive6,
            "all_size_family":family,
            "independent_character_transfer":character,
        },
        "frozen_hashes":freeze_inputs(
            ROOT,{label:(ROOT/path,digest) for label,(path,digest) in HASHES.items()}
        ),
        "runtime":check_runtime("cycle-4-lane-b-bounded-theta-transfer"),
        "sealer":{"path":"proof/build_cycle4_lane_b_recursive_compression.py","sha256":sha256(Path(__file__))},
        "replay":{
            "heldout":"python3 proof/verify_lane_b_heldout.py",
            "relative_4_to_5":"python3 proof/verify_lane_b_recursive.py",
            "relative_5_to_6":"python3 proof/verify_lane_b_recursive6.py",
            "all_size_family":"python3 proof/verify_lane_b_recursive_family.py",
            "character_transfer":"python3 proof/verify_lane_b_character_transfer.py",
            "tests":"python3 -m unittest discover -s tests -v",
            "artifact_check":"python3 proof/build_cycle4_lane_b_recursive_compression.py --check",
        },
    }


if __name__=="__main__":
    raise SystemExit(run_cli(description=__doc__,output=OUTPUT,payload_factory=payload))
