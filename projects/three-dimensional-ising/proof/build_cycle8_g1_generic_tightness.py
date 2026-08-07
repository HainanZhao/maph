#!/usr/bin/env python3
"""Seal arbitrary-width generic nonuniform tightness of the Lane B carrier."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256  # noqa: E402
from proof.verify_g1_buffered_factorization import verify as verify_buffered  # noqa: E402
from proof.verify_g1_lifted_widths import verify as verify_lifted  # noqa: E402
from proof.verify_g1_paired_cycle_w3 import verify as verify_width_three  # noqa: E402


OUTPUT = ROOT / "artifacts/cycle-8-b11-g1-generic-tightness-v1.json"
HASHES: dict[str, tuple[str, str]] = {
    "prior_g0": ("artifacts/cycle-7-b7-lane-b-arbitrary-width-closure-v1.json", "3caa6e9e2a170b6de7660a158719c762d733dcc9f022707143d6ff2aaa80320c"),
    "goal": ("LANE_B_GOAL.md", "0f32445279363c13d18947418d9e3c138dceda89f3142a7bb4d90f7b5a3ef62b"),
    "selection": ("discovery/cycle-8-g1-controllability-selection.md", "6eb04ee167e6ac596efc0590cb75ea5ec9a7ef1ecb8eb1c02728361939010eab"),
    "failure_ledger": ("discovery/failure-ledger-cycle8.md", "5149aee2706a4d54e0151ebced3bc06906f93ad171496349a0c19bef46af8e8b"),
    "report": ("docs/cycle8-g1-generic-tightness.md", "9377e5bb778c78235b96d0478fc1e1be8390a3b5f581cbefad51b50ce1a459d7"),
    "proof": ("proof/g1_arbitrary_width_generic_tightness.md", "dbee185445d85eae852e3d083942425e4867182799c29c3a9c0bba45f46c67fe"),
    "matroid_proof": ("proof/g1_lifted_matroid_specialization.md", "9dc38ea305a040975da8e7328f38f19f5491ab38b1ec2cd08e99495418bf9c98"),
    "normal_verifier": ("proof/verify_g1_arbitrary_width_generic_tightness.py", "4d55b1fc8667261d19ca9e89c276d7763c41c629b336471de519565e5e14e63b"),
    "buffered_verifier": ("proof/verify_g1_buffered_factorization.py", "8859db6ae70c2189f6bb3276728d05c383f471f6fada2f48b85e549dcfba725f"),
    "finite_width_verifier": ("proof/verify_g1_lifted_widths.py", "ad6060f47077f9b43b58cb822b8f2522caf375907e4de581b1ac7652accdfa45"),
    "width_three_verifier": ("proof/verify_g1_paired_cycle_w3.py", "5ceee917c21e24670a09b5bfb03176f87b814ecf55b470eb05b838e8bb06156b"),
    "normal_tree": ("discovery/audit_g1_explicit_all_width_induction.py", "f09d171714830d230914783b9f270d139a5262302f81b4794587044236c035be"),
    "normal_common_basis": ("discovery/audit_g1_explicit_common_basis.py", "07d84fe4ab0d6058b95e8e1ac95e047440e2b89c251cf7f6f5a9a39d897f01df"),
    "gauge_dual": ("discovery/audit_g1_gauge_tree_dual.py", "2fb515e3580409809d25a1646f59e19c06c61d2caa44b91945581cffbcbf204a"),
    "opposite_tree": ("discovery/audit_g1_opposite_explicit_all_width.py", "cdfbd0e26ef1d65d0229054556a516d73d41a5317e298e95a0faa653ff9108d4"),
    "matroid_engine": ("discovery/search_g1_paired_fundamental_cycles.py", "9d7445cdbe81844b800de8cb0104b77f27db3f597a13946c6dee0fcebc4f9ecb"),
    "w3_witness": ("discovery/g1-lifted-unified-w3-live.json", "6a2966b3bd9936abf8263199c3fa52092fb17c5ba8452e3cc42caff5a9d0d1c4"),
    "w4_witness": ("discovery/g1-lifted-unified-w4-live.json", "46d102c9f5475ffa697c4c7ea6a0045fa0d47d076adbdf17a990c23d90984625"),
    "w5_witness": ("discovery/g1-lifted-unified-w5-live.json", "ba6cffab6bb8557204d7490a72a054fc3b43491554564e4fc7e1b9527f349988"),
    "w6_witness": ("discovery/g1-lifted-unified-w6-live.json", "bb43ffa1cde9ee743295d47653ce52ffbc3b55ded6f904dd75df7f4e9d489681"),
    "w7_witness": ("discovery/g1-lifted-unified-w7-live.json", "c57097c9cbee5441a7f4a3c55945804cfb662aeeb7f79cfe689eb764c4641852"),
    "normal_tests": ("tests/test_g1_arbitrary_width_generic_tightness.py", "b8af00fedd4b3637ec3bf9373e8222be8ccde28113d29328bfccd5cf69c08d2e"),
    "buffered_tests": ("tests/test_g1_buffered_factorization.py", "41a5fb09b3fd6f15c3d7ed2a95ac6aa4bd0199d44f7c087e9d78be14581a1167"),
    "frontier_dependency": ("proof/verify_lane_b_arbitrary_width_frontier.py", "f98f80b203eb93bd0c18deb37e80dbf7cdcbb58237129cba60c42cff3fa73615"),
    "homology_dependency": ("proof/verify_lane_b_genus3.py", "1f5a944a1249525ff75b4a471da73e55709de169f0e53d0540ede14b1bb298a4"),
    "conventions": ("src/conventions.py", "b6b328f6b7b1725c39f4e4ba4084c275a141189b7efe32e9727c75488d705bb3"),
    "embedding": ("src/lane_b_universal_embedding.py", "62e57075103f4f2f252f30f9bd1e01c63820656455900b6db0b875e5294ab430"),
    "requirements": ("requirements.txt", "8347daed02ebf7b3c3cfa494e97049b7e0ab15b9af00a5addd843ed44381a64a"),
    "scaffold": ("proof/cycle_seal_v1.py", "c4a09e7baa8a5588d4c6855a533eb933c85791707ed9653437644c1e1ad6c163"),
}


def payload() -> dict[str, object]:
    buffered = verify_buffered(maximum_symbolic_width=20, maximum_global_width=6)
    finite = verify_lifted()
    width_three = verify_width_three()
    for row in buffered["global_coordinate_rows"]:
        if row["left_terminal_rank"] != row["target"] or row["right_terminal_rank"] != row["target"]:
            raise RuntimeError("buffered global-coordinate rank regressed")
    for row in finite["cases"]:
        if row["left_projection_rank"] != row["cycle_dimension"] or row["right_projection_rank"] != row["cycle_dimension"]:
            raise RuntimeError("independent finite-width witness regressed")
    return {
        "artifact_id": "cycle-8-b11-g1-generic-tightness-v1",
        "author": "Hainan Zhao",
        "budget_ordinal": "B11",
        "cycle": 8,
        "status": "SEALED",
        "epistemic_status": "PROVED_WITH_EXACT_GF2_AND_TWO_PRIME_REPLAY",
        "record_type": "LANE_B_GENERIC_NONUNIFORM_TIGHTNESS",
        "outcome": (
            "For every w>=3, the canonical checkerboard all-spin-structure tensor has "
            "generic nonuniform saturation R_infinity(w)=2^(w^2-1); n=11 is a uniform "
            "sufficient length."
        ),
        "gate_outcome": "G1_AND_UPGRADE_1_COMPLETE",
        "claim_boundary": (
            "The theorem is over independent nonuniform edge weights and therefore on a "
            "nonempty open subset of positive ferromagnetic weights. It does not prove "
            "homogeneous anisotropic or isotropic tightness, any particular-temperature "
            "nonvanishing, a sub-area carrier, or a cubic thermodynamic limit."
        ),
        "theorem": {
            "widths": "all integers w>=3",
            "sufficient_length": 11,
            "rank": "2^(w^2-1)",
            "upper_route": "sealed Cycle 7 canonical separator factorization",
            "lower_route": (
                "normal left encoder + opposite-phase right encoder + invertible two-slab "
                "buffer, proving separate reachability and observability"
            ),
        },
        "exact_replay": {
            "buffered_arbitrary_width_hypotheses": buffered,
            "independent_lifted_matroid_widths_3_to_7": finite,
            "dense_width_three_minor": width_three,
        },
        "frozen_hashes": freeze_inputs(
            ROOT, {label: (ROOT / path, digest) for label, (path, digest) in HASHES.items()}
        ),
        "runtime": check_runtime("cycle-8-g1-generic-tightness"),
        "sealer": {
            "path": "proof/build_cycle8_g1_generic_tightness.py",
            "sha256": sha256(Path(__file__)),
        },
        "replay": {
            "verification": (
                "python3 proof/verify_g1_buffered_factorization.py "
                "--maximum-symbolic-width 20 --maximum-global-width 6"
            ),
            "independent_finite_widths": "python3 proof/verify_g1_lifted_widths.py",
            "width_three": "python3 proof/verify_g1_paired_cycle_w3.py",
            "tests": (
                "python3 -m unittest tests.test_g1_arbitrary_width_generic_tightness "
                "tests.test_g1_buffered_factorization -v"
            ),
            "artifact_check": "python3 proof/build_cycle8_g1_generic_tightness.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
