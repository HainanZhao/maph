#!/usr/bin/env python3
"""Seal the Gate B5 spin-transfer equivalence and width-rank certificates."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256  # noqa: E402
from proof.verify_lane_b_spin_parity_intertwiner import verify as verify_bridge  # noqa: E402
from proof.verify_lane_b_width_scaling import verify as verify_widths  # noqa: E402


OUTPUT = ROOT / "artifacts/cycle-5-b5-lane-b-width-rank-audit-v1.json"
HASHES = {
    "prior": ("artifacts/cycle-4-b4-lane-b-bounded-theta-transfer-v1.json", "3bbc61164f68eaaed3b1babcdd9e782da06aa0ccfc90637f81de27501c7dcb8d"),
    "selection": ("discovery/cycle-5-b5-width-scaling-selection.md", "14b421b684c30a0b7f3e76096620084918f39240df517baf1c01a9cd46ce5bb7"),
    "source_audit": ("discovery/cycle5-source-and-novelty-audit.md", "8344fce4986687d8da1645f338826c04b3fbcb560f7b2f09b96feb07d5d67363"),
    "failure_ledger": ("discovery/failure-ledger-cycle5.md", "fab61724a28e2d669ddf9c99b27d93b882cd803396a29314ea21ad42bc81ea2f"),
    "report": ("docs/cycle5-lane-b-width-rank-audit.md", "406ded7a75a7af2575fd231ae45cd22eff492664938eafc831aedde36caf69c5"),
    "proof_note": ("proof/lane_b_width_scaling_proof.md", "a287e31b0c46c1e79e7a91a5b8154f42a7a80a74af877a0977ab7f5abe7e77d7"),
    "conventions": ("src/conventions.py", "b6b328f6b7b1725c39f4e4ba4084c275a141189b7efe32e9727c75488d705bb3"),
    "bridge_module": ("src/lane_b_spin_parity_intertwiner.py", "f48b300fce4a65cdd5b97d1bf0cf44dc52388c7f990c8c61c2a0f381c9c8ba28"),
    "width_module": ("src/lane_b_width_scaling.py", "e7468a053ced5587bbe8a595c34b560b10b0b1e8ed715efd40e0177a596da49d"),
    "bridge_verifier": ("proof/verify_lane_b_spin_parity_intertwiner.py", "0051d6d93f7f374928fafe64ab8b29acf1944cba83cfbd686927f49f6c1efa60"),
    "width_verifier": ("proof/verify_lane_b_width_scaling.py", "2cb86284481e69b26bea8d9f7a52e91664a7b2b7869cdf1915795bef18926ae4"),
    "transfer_engine": ("proof/lane_b_width4_character_transfer.cpp", "dd7f5f3e381ae3759eaa8d86a930d968ab3ac75773646ba69c52d59f77e1d940"),
    "bridge_tests": ("tests/test_lane_b_spin_parity_intertwiner.py", "1e8d837e12988b795951c62a9fd0411cc30ece43d3368ce0722480eddb82ed74"),
    "width_tests": ("tests/test_lane_b_width_scaling.py", "aff07ab0cb98a6c85441e4ed06cc2aeedc0c191c19f724d94912e03abb262bb3"),
    "artifact_tests": ("tests/test_cycle5_lane_b_width_rank_audit.py", "c6b191094d62c0dc0ba7b1f8724c9e8f13f7c4ff7107c90a675736a841c436dc"),
    "requirements": ("requirements.txt", "8347daed02ebf7b3c3cfa494e97049b7e0ab15b9af00a5addd843ed44381a64a"),
    "scaffold": ("proof/cycle_seal_v1.py", "c4a09e7baa8a5588d4c6855a533eb933c85791707ed9653437644c1e1ad6c163"),
}


def payload() -> dict[str, object]:
    bridge = verify_bridge()
    widths = verify_widths()
    if bridge["controls"][0]["identity"] != "Q H = 2^(w^2) H K":
        raise RuntimeError("spin/parity intertwiner regression")
    for prime, audit in widths["prime_audits"].items():
        if not audit["independent_transfer_control"]["all_agree"]:
            raise RuntimeError(f"independent transfer mismatch at prime {prime}")
        for width, expected in (("w3", 8), ("w4", 32)):
            for regime, case in audit[width]["cases"].items():
                if max(case["binary_flattening_ranks"]) != expected:
                    raise RuntimeError(f"rank regression {prime} {width} {regime}")
                certificate = next(iter(case["central_full_minor_mod_prime"].values()))
                if not certificate["determinant"]:
                    raise RuntimeError(f"zero determinant {prime} {width} {regime}")
    return {
        "artifact_id": "cycle-5-b5-lane-b-width-rank-audit-v1",
        "author": "Hainan Zhao",
        "budget_ordinal": "B5",
        "cycle": 5,
        "status": "SEALED",
        "epistemic_status": "MIXED_PROVED_AND_CERTIFIED_NUMERICAL",
        "record_type": "LANE_B_TRANSFER_EQUIVALENCE_AND_FIXED_BASIS_RANK_CERTIFICATES",
        "outcome": (
            "The homology-frontier carrier is exactly the conventional global-spin-flip "
            "quotient transfer in a Walsh basis. In frozen coordinates at n=4, the central "
            "twist flattenings have full ranks 8 at w=3 and 32 at w=4 for nonuniform, "
            "homogeneous anisotropic, and homogeneous isotropic specializations, certified "
            "over two prime fields with replayable elimination transcripts."
        ),
        "gate_outcome": "B5_CARRIER_NOVELTY_KILLED_FIXED_BASIS_RANKS_SURVIVE_B6_REQUIRED",
        "claim_boundary": (
            "Full rank is proved only for the frozen homology basis, bit ordering, widths "
            "three and four, and longitudinal size four. It is not an optimized-basis lower "
            "bound, an asymptotic area law, a saturation theorem, or a cubic-box result. The "
            "conditional all-width R(w) ansatz is not promoted. The 3D Ising model is not solved."
        ),
        "attribution": (
            "All-size minimum genus at w=3 invokes Millichap--Salinas Theorem 4; our embedding "
            "attains that prior value. The 256-state carrier is conventional transfer space."
        ),
        "falsifier": (
            "Any frozen replay mismatch; a failure of QH=2^(w^2)HK; disagreement between "
            "independent spin and parity transfers; a zero recorded central determinant; a "
            "noninvertible normalization denominator; or a mismatch of the frozen labels, "
            "basis, ordering, prime, specialization, or elimination transcript."
        ),
        "exact_replay": {"intertwiner": bridge, "width_rank_audit": widths},
        "principal_replay_benchmark": {
            "command": "python3 proof/verify_lane_b_width_scaling.py",
            "wall_seconds": 21.37,
            "peak_rss_kib": 116516,
            "threads": 3,
        },
        "frozen_hashes": freeze_inputs(
            ROOT, {label: (ROOT / path, digest) for label, (path, digest) in HASHES.items()}
        ),
        "runtime": check_runtime("cycle-5-lane-b-width-rank-audit"),
        "sealer": {"path": "proof/build_cycle5_lane_b_width_rank_audit.py", "sha256": sha256(Path(__file__))},
        "replay": {
            "intertwiner": "python3 proof/verify_lane_b_spin_parity_intertwiner.py",
            "width_ranks": "python3 proof/verify_lane_b_width_scaling.py",
            "tests": "python3 -m unittest discover -s tests -v",
            "artifact_check": "python3 proof/build_cycle5_lane_b_width_rank_audit.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
