#!/usr/bin/env python3
"""Seal the arbitrary-width canonical spin-structure closure theorem."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256  # noqa: E402
from proof.verify_lane_b_arbitrary_width_frontier import verify as verify_structure  # noqa: E402
from proof.verify_lane_b_universal_canonical_ranks import verify as verify_ranks  # noqa: E402


OUTPUT = ROOT / "artifacts/cycle-7-b7-lane-b-arbitrary-width-closure-v1.json"
HASHES: dict[str, tuple[str, str]] = {
    "prior": ("artifacts/cycle-6-b6-lane-b-longitudinal-saturation-v1.json", "103e52a1a2f8d95081654dbfd4b16b005d8bb9b61bb3c9abc2ab5bb292665d39"),
    "selection": ("discovery/cycle-7-arbitrary-width-canonical-closure-selection.md", "772bb9ddf7a86d6625b8e16578f9b66f5334de18feb4977ad67ff4d4ecba75ec"),
    "failure_ledger": ("discovery/failure-ledger-cycle7.md", "cf5c6a7e94dc6c59fa317a4a2ff3a58afcf4798bff384cd34c941ce13a6fa9bf"),
    "report": ("docs/cycle7-lane-b-arbitrary-width-closure.md", "367c643a91e33c11f37c2c6a515bd417e406926aeb6a6cd200be9de52704fc68"),
    "proof": ("proof/lane_b_arbitrary_width_closure_proof.md", "9cb716648b4e8bc8995a62f610c9f55321572960a9b8b6a343949e4125784ede"),
    "embedding": ("src/lane_b_universal_embedding.py", "62e57075103f4f2f252f30f9bd1e01c63820656455900b6db0b875e5294ab430"),
    "width_module": ("src/lane_b_width_scaling.py", "e7468a053ced5587bbe8a595c34b560b10b0b1e8ed715efd40e0177a596da49d"),
    "conventions": ("src/conventions.py", "b6b328f6b7b1725c39f4e4ba4084c275a141189b7efe32e9727c75488d705bb3"),
    "structural_verifier": ("proof/verify_lane_b_arbitrary_width_frontier.py", "f98f80b203eb93bd0c18deb37e80dbf7cdcbb58237129cba60c42cff3fa73615"),
    "rank_verifier": ("proof/verify_lane_b_universal_canonical_ranks.py", "d631149c9429d921359a6a67042b0e476cb681b9bc8aa63de42bcac6503662b0"),
    "width_verifier_dependency": ("proof/verify_lane_b_width_scaling.py", "2cb86284481e69b26bea8d9f7a52e91664a7b2b7869cdf1915795bef18926ae4"),
    "intersection_dependency": ("proof/verify_lane_b_intersection.py", "1b6b59d188dfdc033b1c37c0059ee3e068181c458a9da028d0a8e0f1a273abd9"),
    "homology_dependency": ("proof/verify_lane_b_genus3.py", "1f5a944a1249525ff75b4a471da73e55709de169f0e53d0540ede14b1bb298a4"),
    "transfer_engine": ("proof/lane_b_width4_character_transfer.cpp", "dd7f5f3e381ae3759eaa8d86a930d968ab3ac75773646ba69c52d59f77e1d940"),
    "tests": ("tests/test_lane_b_arbitrary_width_frontier.py", "10b16e3901faafb75a8f693428f83a7ddd665aa125c854ff6b2b95b58ba1b0a9"),
    "requirements": ("requirements.txt", "8347daed02ebf7b3c3cfa494e97049b7e0ab15b9af00a5addd843ed44381a64a"),
    "scaffold": ("proof/cycle_seal_v1.py", "c4a09e7baa8a5588d4c6855a533eb933c85791707ed9653437644c1e1ad6c163"),
}


def payload() -> dict[str, object]:
    structure = verify_structure()
    ranks = verify_ranks()
    for case in structure["cases"]:
        for row in case["length_rows"]:
            if row["explicit_checkerboard_lagrangian_rank"] != row["genus"]:
                raise RuntimeError("checkerboard Lagrangian rank regression")
            if row["atomic_intersection"] != row["canonical_intersection"]:
                raise RuntimeError("canonical intersection regression")
    w3 = [case for case in ranks["cases"] if case["shape"] == [10, 3, 3]]
    if any(case["central_certificate"]["rank"] != 256 for case in w3):
        raise RuntimeError("width-three canonical saturation regression")
    for case in ranks["cases"]:
        case.pop("wall_seconds", None)
    return {
        "artifact_id": "cycle-7-b7-lane-b-arbitrary-width-closure-v1",
        "author": "Hainan Zhao",
        "budget_ordinal": "B7",
        "cycle": 7,
        "status": "SEALED",
        "epistemic_status": "MIXED_PROVED_AND_CERTIFIED_NUMERICAL",
        "record_type": "LANE_B_ARBITRARY_WIDTH_CANONICAL_CLOSURE",
        "outcome": (
            "For the explicit nested checkerboard embedding of every G_(n,w), every pair "
            "and internal cut of the complete spin-structure tensor factors through only "
            "the ordinary even frontier V_w of size 2^(w^2-1)."
        ),
        "gate_outcome": "G0_FULL_ARBITRARY_WIDTH_UPPER_CLOSURE",
        "claim_boundary": (
            "Generic tightness is proved only at width three and remains conjectural for "
            "arbitrary width. The theorem does not compress the physical area-exponential "
            "carrier and gives no cubic free energy, critical temperature, exponents, or "
            "solution of the three-dimensional Ising model."
        ),
        "theorem": {
            "family": "P_n square P_w square P_w with n,w>=2 and free longitudinal boundaries",
            "embedding": "next-even restricted checkerboard ribbon embedding",
            "canonical_order": "checkerboard co-core Lagrangian, slab then lexicographic",
            "pair_cut_upper": "2^(w^2-1)",
            "internal_cut_upper": "2^(w^2-1)",
            "weights": "arbitrary nonuniform edge weights over a commutative polynomial ring",
            "classification": "G0",
        },
        "exact_replay": {"structural_firewall": structure, "rank_certificates": ranks},
        "principal_replay_benchmark": {
            "command": "python3 proof/verify_lane_b_universal_canonical_ranks.py",
            "wall_seconds_approximate": 275,
            "threads": 3,
            "cases": 12,
        },
        "frozen_hashes": freeze_inputs(
            ROOT, {label: (ROOT / path, digest) for label, (path, digest) in HASHES.items()}
        ),
        "runtime": check_runtime("cycle-7-lane-b-arbitrary-width-closure"),
        "sealer": {
            "path": "proof/build_cycle7_lane_b_arbitrary_width_closure.py",
            "sha256": sha256(Path(__file__)),
        },
        "replay": {
            "structure": "python3 proof/verify_lane_b_arbitrary_width_frontier.py",
            "ranks": "python3 proof/verify_lane_b_universal_canonical_ranks.py",
            "tests": "python3 -m unittest tests/test_lane_b_arbitrary_width_frontier.py -v",
            "artifact_check": "python3 proof/build_cycle7_lane_b_arbitrary_width_closure.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
