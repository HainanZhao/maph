#!/usr/bin/env python3
"""Seal Cycle 18 without modifying historical frozen proof-input paths."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof import build_cycle18_character_duality_correction as helpers  # noqa: E402
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256  # noqa: E402
from proof.verify_lane_b_character_duality import verify as verify_duality  # noqa: E402


OUTPUT = ROOT / "artifacts/cycle-18-b18-character-duality-correction-v3.json"
HASHES = {
    "decision": ("discovery/cycle-18-character-duality-correction.md", "f79425d03034060f68d0ca758395d1a43d483420478469d1c1da3d63d8b91942"),
    "failure_ledger": ("discovery/failure-ledger-cycle18.md", "dedeba10141dd549138cb4a17a074a3df7ee4fa197b9b05247f0ce649a8e0b39"),
    "proof": ("proof/character_duality_correction_proof.md", "65b8bafa38dcc5a4d521643d553ec185077fcaed4d5bae22858579c9e1cc47b3"),
    "manuscript": ("paper/canonical-spin-structure-compression/main.tex", "145f01df0684ccbb85cbbe2e90f6aa632b6eeb0ce9dca5db94b28a35b4992d3f"),
    "duality_verifier": ("proof/verify_lane_b_character_duality.py", "9d20343bb47b134c203dbc9ef13c407292cdbaf7d7bd8f02a1a29f51e44e72e2"),
    "duality_test": ("tests/test_lane_b_character_duality.py", "ad4f08f13070e7bb420f13fae7e6aa04b2901a5c4b17fd2b8710bf95dcb153b3"),
    "rank_verifier": ("proof/verify_lane_b_universal_canonical_ranks.py", "d631149c9429d921359a6a67042b0e476cb681b9bc8aa63de42bcac6503662b0"),
    "core_verifier": ("proof/verify_polynomial_tt_grid_cores.py", "ce8b69d1d2570e971cd2d3fdce65ea93c40c1372287da448869455e8058b4082"),
    "frontier_verifier": ("proof/verify_lane_b_arbitrary_width_frontier.py", "f98f80b203eb93bd0c18deb37e80dbf7cdcbb58237129cba60c42cff3fa73615"),
    "prior_phase0": ("artifacts/cycle-13-b13-polynomial-tt-grid-cores-v1.json", "741e1f910177542255157d041cc3dc70998002dca23c2a7040f06d32ab3e6fa4"),
    "prior_closure": ("artifacts/cycle-7-b7-lane-b-arbitrary-width-closure-v1.json", "3caa6e9e2a170b6de7660a158719c762d733dcc9f022707143d6ff2aaa80320c"),
    "v1_helper_builder": ("proof/build_cycle18_character_duality_correction.py", "d6700aa8f947785b5a20a3924cf3328d3a779f7370bd80c4916d1558d8658972"),
    "v2_artifact": ("artifacts/cycle-18-b18-character-duality-correction-v2.json", "cb2e52e32fd79a6ebdb6f58d0967e1d18f76ecca588faf1fbd8a3e564ff8d927"),
    "v2_builder": ("proof/build_cycle18_character_duality_correction_v2.py", "59bd3beb4294376e47e193e2725d3b5a339473a10ad8b1907667ea6d3b30aed1"),
    "archive_correction": ("discovery/cycle18-character-duality-archive-compatibility-correction.md", "7a9b72d3dcdf8b9d98778670d94340f35d6e3b5a46babbc1f6ecb1bde1d31d29"),
    "scaffold": ("proof/cycle_seal_v1.py", "c4a09e7baa8a5588d4c6855a533eb933c85791707ed9653437644c1e1ad6c163"),
}


def payload():
    duality = verify_duality()
    ranks = helpers.stable_ranks()
    cores = helpers.stable_cores()
    cores.pop("peak_rss_kib", None)
    frontier = helpers.frontier_summary()
    if not all(row["beta_unchanged"] for row in duality["cases"]):
        raise RuntimeError("H3 beta transport regressed")
    if any(case["canonical_binary_rank_profile"][7:10] != [256, 256, 256]
           for case in ranks["cases"] if case["shape"] == [10, 3, 3]):
        raise RuntimeError("width-three internal rank replay regressed")
    if not all(row["direct_core_matches_independent_reference"] for row in cores["rows"]):
        raise RuntimeError("polynomial core replay regressed")
    if not all(row["all_b_coordinate_modes_exact"] for row in frontier["cases"]):
        raise RuntimeError("finite geometric b-coordinate firewall regressed")
    return {
        "artifact_id": "cycle-18-b18-character-duality-correction-v3",
        "author": "Hainan Zhao",
        "budget_ordinal": "B18",
        "cycle": 18,
        "status": "SEALED",
        "supersedes": "cycle-18-b18-character-duality-correction-v2",
        "record_type": "POST_PUBLICATION_CHARACTER_DUALITY_CORRECTION",
        "epistemic_status": "PROVED_WITH_EXACT_TWO_ROUTE_AUDIT",
        "correction": {
            "error": "The released H3 proof used PD(b_i), extracting x_i, for the lambda_b character that multiplies y_i.",
            "cause": "Homology generators and their symplectically crossed coordinate cocycles were assigned the same subscript without an explicit dual table.",
            "affected_claims_before_repair": [
                "arbitrary-width internal-cut bond d_w",
                "binary-coordinate polynomial TT bond d_w",
                "G1 equality insofar as it uses that upper bound",
            ],
            "false_step_preserved": True,
        },
        "archival_correction": {
            "error": "v2 placed corrected prose at historical frozen-input paths",
            "affected_claims": "none",
            "historical_inputs_restored": True,
            "mathematical_fields_changed": False,
        },
        "corrected_theorem": {
            "character_table": "lambda_a uses alpha_i=PD(b_i); lambda_b uses beta_i=PD(a_i)",
            "geometric_H3": "a pushed-off exposed meridian is a proper arc in the planar cut collar and its cocycle is relative-exact",
            "triangular_transport": "alpha_j=tilde alpha_j+sum_k U_kj beta_k; beta_j=tilde beta_j",
            "internal_bond": "2^(w^2-1) for every n,w in the checkerboard filtration",
        },
        "outcome": "The arbitrary-width H3 and internal-cut bond are restored with the correct meridian-dual character; the old longitude-H3 proof is withdrawn.",
        "gate_outcome": "CHARACTER_DUALITY_CORRECTION_PROVED_PENDING_RELEASE",
        "claim_boundary": "No homogeneous arbitrary-width, thermodynamic-limit, critical-temperature, or exact-solution claim is added.",
        "exact_replay": {
            "character_duality": duality,
            "finite_geometric_firewall": frontier,
            "canonical_binary_ranks": ranks,
            "polynomial_grid_cores": cores,
        },
        "frozen_hashes": freeze_inputs(ROOT, {k: (ROOT / p, h) for k, (p, h) in HASHES.items()}),
        "runtime": check_runtime("cycle-18-character-duality-correction-v3"),
        "sealer": {"path": "proof/build_cycle18_character_duality_correction_v3.py", "sha256": sha256(Path(__file__))},
        "replay": {
            "duality": "python3 proof/verify_lane_b_character_duality.py",
            "ranks": "python3 proof/verify_lane_b_universal_canonical_ranks.py",
            "cores": "python3 proof/verify_polynomial_tt_grid_cores.py",
            "tests": "python3 -m unittest tests/test_lane_b_character_duality.py tests/test_lane_b_cochain_gauge.py tests/test_lane_b_arbitrary_width_frontier.py tests/test_global_phase_telescoping.py tests/test_polynomial_tt_grid_cores.py -v",
            "artifact_check": "python3 proof/build_cycle18_character_duality_correction_v3.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
