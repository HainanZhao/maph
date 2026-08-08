#!/usr/bin/env python3
"""Seal the post-publication Lane B character-duality correction."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256  # noqa: E402
from proof.verify_lane_b_arbitrary_width_frontier import verify as verify_frontier  # noqa: E402
from proof.verify_lane_b_character_duality import verify as verify_duality  # noqa: E402
from proof.verify_lane_b_universal_canonical_ranks import verify as verify_ranks  # noqa: E402
from proof.verify_polynomial_tt_grid_cores import verify as verify_cores  # noqa: E402


OUTPUT = ROOT / "artifacts/cycle-18-b18-character-duality-correction-v1.json"
HASHES = {
    "decision": ("discovery/cycle-18-character-duality-correction.md", "f79425d03034060f68d0ca758395d1a43d483420478469d1c1da3d63d8b91942"),
    "failure_ledger": ("discovery/failure-ledger-cycle18.md", "dedeba10141dd549138cb4a17a074a3df7ee4fa197b9b05247f0ce649a8e0b39"),
    "proof": ("proof/character_duality_correction_proof.md", "65b8bafa38dcc5a4d521643d553ec185077fcaed4d5bae22858579c9e1cc47b3"),
    "duality_verifier": ("proof/verify_lane_b_character_duality.py", "9d20343bb47b134c203dbc9ef13c407292cdbaf7d7bd8f02a1a29f51e44e72e2"),
    "duality_test": ("tests/test_lane_b_character_duality.py", "ad4f08f13070e7bb420f13fae7e6aa04b2901a5c4b17fd2b8710bf95dcb153b3"),
    "closure_proof": ("proof/lane_b_arbitrary_width_closure_proof.md", "49e0a20b60dfed873cd38fc18063a761d4728c13457b00f6d22ba07655239586"),
    "telescoping_proof": ("proof/polynomial_tt_telescoping_proof.md", "d0fc97b884f31fdcefc0fd2318c6c79f18d2571a227e7dddaec051b163e15455"),
    "separator_proof": ("proof/abstract_spin_structure_separator_theorem.md", "2ac1da0b64e8c0312aa9db65c298f5830a767e6f426c369455c3ddba2123c399"),
    "rank_verifier": ("proof/verify_lane_b_universal_canonical_ranks.py", "d631149c9429d921359a6a67042b0e476cb681b9bc8aa63de42bcac6503662b0"),
    "core_verifier": ("proof/verify_polynomial_tt_grid_cores.py", "ce8b69d1d2570e971cd2d3fdce65ea93c40c1372287da448869455e8058b4082"),
    "frontier_verifier": ("proof/verify_lane_b_arbitrary_width_frontier.py", "f98f80b203eb93bd0c18deb37e80dbf7cdcbb58237129cba60c42cff3fa73615"),
    "prior_phase0": ("artifacts/cycle-13-b13-polynomial-tt-grid-cores-v1.json", "741e1f910177542255157d041cc3dc70998002dca23c2a7040f06d32ab3e6fa4"),
    "prior_closure": ("artifacts/cycle-7-b7-lane-b-arbitrary-width-closure-v1.json", "3caa6e9e2a170b6de7660a158719c762d733dcc9f022707143d6ff2aaa80320c"),
    "scaffold": ("proof/cycle_seal_v1.py", "c4a09e7baa8a5588d4c6855a533eb933c85791707ed9653437644c1e1ad6c163"),
}


def stable_ranks() -> dict[str, object]:
    payload = verify_ranks()
    for row in payload["cases"]:
        row.pop("wall_seconds", None)
    return payload


def stable_cores() -> dict[str, object]:
    payload = verify_cores()
    payload.pop("runtime", None)
    payload.pop("wall_seconds", None)
    return payload


def frontier_summary() -> dict[str, object]:
    payload = verify_frontier()
    cases = []
    for case in payload["cases"]:
        rows = case["length_rows"]
        cases.append({
            "width": case["width"],
            "lengths": [row["length"] for row in rows],
            "all_b_coordinate_modes_exact": all(row["all_b_modes_exact"] for row in rows),
            "all_atomic_maps_symplectic": all(
                row["atomic_intersection"] == row["canonical_intersection"] for row in rows
            ),
            "all_quadratic_polarizations_checked": all(
                row["quadratic_polarization_checked_on_generators_and_pairs"] for row in rows
            ),
        })
    return {"status": payload["claim_status"], "cases": cases}


def payload():
    duality = verify_duality()
    ranks = stable_ranks()
    cores = stable_cores()
    frontier = frontier_summary()
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
        "artifact_id": "cycle-18-b18-character-duality-correction-v1",
        "author": "Hainan Zhao",
        "budget_ordinal": "B18",
        "cycle": 18,
        "status": "SEALED",
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
            "unaffected_evidence": [
                "abstract separator theorem",
                "pair-cut factorization",
                "finite canonical rank certificates",
                "generic lower-bound encoders",
            ],
            "false_step_preserved": True,
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
        "runtime": check_runtime("cycle-18-character-duality-correction"),
        "sealer": {"path": "proof/build_cycle18_character_duality_correction.py", "sha256": sha256(Path(__file__))},
        "replay": {
            "duality": "python3 proof/verify_lane_b_character_duality.py",
            "ranks": "python3 proof/verify_lane_b_universal_canonical_ranks.py",
            "cores": "python3 proof/verify_polynomial_tt_grid_cores.py",
            "tests": "python3 -m unittest tests/test_lane_b_character_duality.py tests/test_lane_b_cochain_gauge.py tests/test_lane_b_arbitrary_width_frontier.py tests/test_global_phase_telescoping.py tests/test_polynomial_tt_grid_cores.py -v",
            "artifact_check": "python3 proof/build_cycle18_character_duality_correction.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
