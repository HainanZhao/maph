#!/usr/bin/env python3
"""Seal the abstract separator theorem and infinite K3,3 sharpness family."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256  # noqa: E402
from proof.verify_abstract_separator_k33_chain import verify  # noqa: E402


OUTPUT = ROOT / "artifacts/cycle-10-b9-abstract-separator-k33-sharpness-v1.json"
HASHES: dict[str, tuple[str, str]] = {
    "prior": ("artifacts/cycle-7-b7-lane-b-arbitrary-width-closure-v1.json", "3caa6e9e2a170b6de7660a158719c762d733dcc9f022707143d6ff2aaa80320c"),
    "selection": ("discovery/cycle-10-abstract-separator-selection.md", "af05d418c5241887689654ae06da4bb5f2c089c85e86087b8c4254cf5fa50f37"),
    "failure_ledger": ("discovery/failure-ledger-cycle10.md", "4fd28bd4caf797873571eca8c4f5690db5d33362421157a0f7f71e43b869cbcc"),
    "report": ("docs/cycle10-abstract-separator-theorem.md", "b0093bac245ccbd63a1401bc8c1964325e93773d23eb17af434b08468a2a8d2c"),
    "proof": ("proof/abstract_spin_structure_separator_theorem.md", "5baa6fa7038133c498c34719f25ccf8de311cce2e2920d6c07ffa0511ed82c9c"),
    "verifier": ("proof/verify_abstract_separator_k33_chain.py", "5d42cd1156a53d0bd3a41dcf371a7feb5b8b6cb04b112475b8b44a1dcb39ba2a"),
    "tests": ("tests/test_abstract_separator_k33_chain.py", "c6d10dc20c0437c1d2815f49bc70992a060f857fee5ca279d08eabd301f702ad"),
    "frontier_dependency": ("proof/verify_lane_b_arbitrary_width_frontier.py", "f98f80b203eb93bd0c18deb37e80dbf7cdcbb58237129cba60c42cff3fa73615"),
    "homology_dependency": ("proof/verify_lane_b_genus3.py", "1f5a944a1249525ff75b4a471da73e55709de169f0e53d0540ede14b1bb298a4"),
    "intersection_dependency": ("proof/verify_lane_b_intersection.py", "1b6b59d188dfdc033b1c37c0059ee3e068181c458a9da028d0a8e0f1a273abd9"),
    "rank_dependency": ("proof/verify_lane_b_universal_canonical_ranks.py", "d631149c9429d921359a6a67042b0e476cb681b9bc8aa63de42bcac6503662b0"),
    "width_dependency": ("proof/verify_lane_b_width_scaling.py", "2cb86284481e69b26bea8d9f7a52e91664a7b2b7869cdf1915795bef18926ae4"),
    "conventions": ("src/conventions.py", "b6b328f6b7b1725c39f4e4ba4084c275a141189b7efe32e9727c75488d705bb3"),
    "requirements": ("requirements.txt", "8347daed02ebf7b3c3cfa494e97049b7e0ab15b9af00a5addd843ed44381a64a"),
    "scaffold": ("proof/cycle_seal_v1.py", "c4a09e7baa8a5588d4c6855a533eb933c85791707ed9653437644c1e1ad6c163"),
}


def payload() -> dict[str, object]:
    replay = verify()
    r3 = [row for row in replay["rows"] if row["gadgets"] == 3]
    if len(r3) != 2:
        raise RuntimeError("missing two-prime three-gadget controls")
    for row in r3:
        witness = row["embeddable_zero_port_witness"]
        if witness["rank_certificate"]["rank"] != 4:
            raise RuntimeError("embeddable internal witness regressed")
        if witness["all_24_affine_symplectic_local_relabeling_ranks"] != [4] * 24:
            raise RuntimeError("local-relabeling obstruction regressed")
    return {
        "artifact_id": "cycle-10-b9-abstract-separator-k33-sharpness-v1",
        "author": "Hainan Zhao",
        "budget_ordinal": "B9",
        "cycle": 10,
        "status": "SEALED",
        "epistemic_status": "MIXED_PROVED_AND_CERTIFIED_NUMERICAL",
        "record_type": "ABSTRACT_SEPARATOR_THEOREM_AND_SHARP_NON_GRID_FAMILY",
        "outcome": (
            "Relative-chain phase factorization through a k-point separator gives handle-site "
            "bond at most 2^(k-1); H3 is exactly the additional no-factor-two condition at "
            "internal cuts. Toroidal K3,3 chains form an infinite sharpness family with generic "
            "pair rank two and non-end internal rank four."
        ),
        "gate_outcome": "UPGRADE_2_COMPLETE",
        "claim_boundary": (
            "The theorem is sufficient rather than necessary. The K3,3 family sharpens H3 but "
            "does not prove grid G1 or reduce the physical area-exponential carrier."
        ),
        "theorem": {
            "pair_bound": "2^(|S|-1) under H1-H2",
            "internal_bound": "2^(|S|-1) under H1-H3; otherwise twice the pair bound",
            "grid_corollary": "S has w^2 points and H3 holds",
            "non_grid_corollary": "toroidal K3,3 two-sum chains",
            "infinite_sharpness": "generic pair rank 2; every non-end internal rank 4",
        },
        "exact_replay": replay,
        "frozen_hashes": freeze_inputs(
            ROOT, {label: (ROOT / path, digest) for label, (path, digest) in HASHES.items()}
        ),
        "runtime": check_runtime("cycle-10-abstract-separator-k33-sharpness"),
        "sealer": {
            "path": "proof/build_cycle10_abstract_separator_theorem.py",
            "sha256": sha256(Path(__file__)),
        },
        "replay": {
            "verification": "python3 proof/verify_abstract_separator_k33_chain.py",
            "tests": "python3 -m unittest tests/test_abstract_separator_k33_chain.py -v",
            "artifact_check": "python3 proof/build_cycle10_abstract_separator_theorem.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
