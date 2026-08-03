#!/usr/bin/env python3
"""Seal Cycle 200/B037's source regular/residue jet ledger."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_200_regular_residue_jet import run as jet_run


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-200-b037-regular-residue-jet-v1.json"
INPUTS = {
    "prior_full_phase_abel_boundary": (
        ROOT / "artifacts/cycle-199-b036-full-phase-abel-boundary-v1.json",
        "97e0100205df7e0ea73e9b61ab8e6278a146afe05d3000300ae57788be2c253e",
    ),
    "prior_endpoint_functional": (
        ROOT / "artifacts/cycle-198-b035-analytic-frequency-endpoint-v1.json",
        "78328f0e8df4ea566fea804cef79217ad1201ca028004d911b7f43871e8f9a3f",
    ),
    "prior_finite_anti_residue_sum": (
        ROOT / "artifacts/cycle-195-b032-finite-anti-residue-sum-v1.json",
        "7e4d7615414dbf49627c9ea9cfa2b5e0191502cd6a6915fa93d13085cd50ae8d",
    ),
    "prior_meromorphic_anti_channel": (
        ROOT / "artifacts/cycle-194-b031-meromorphic-anti-channel-v2.json",
        "c8eb1e91d496019ed52c8a9b2c48949a5b87a7e88b84857259f34b9a8d43d52d",
    ),
    "preregistration": (
        ROOT / "docs/cycle-200-b037-regular-residue-jet-preregistration-v1.md",
        "75a855b03fd5fb17bf9fbf6d38b0d90b73b599ff8774ce1f4986bf0d11c67c05",
    ),
    "replay": (
        ROOT / "proof/verify_cycle_200_regular_residue_jet.py",
        "c93c8f6e9341e3c94714f558176a726ba30ac63c2a2e6056114e8a4328b0a2e9",
    ),
    "regression_test": (
        ROOT / "tests/test_cycle_200_regular_residue_jet.py",
        "b1b90b8891850633ce2d726f5dc69d77c865c733672f50dbb6ad4c295915a4d2",
    ),
    "prototype": (
        ROOT / "discovery/cycle-200-b037-regular-residue-jet-prototype-v1.json",
        "bb215149c983b32ae19491d84a0b0d4379e156d8864d341293c57895381afb64",
    ),
    "cycle199_full_boundary_replay": (
        ROOT / "proof/verify_cycle_199_full_phase_abel_boundary.py",
        "2ee95df4cf6b418ac2ad8736c6171ddc983412c7dd82567b56526aa88f585f0d",
    ),
    "cycle199_character_comb_replay": (
        ROOT / "proof/verify_cycle_199_abel_character_comb.py",
        "b06e6493dac1ac4b3de5c7f5af9d19f0367947025c7774b6f049a8a6839ee07b",
    ),
    "cycle199_pole_geometry_replay": (
        ROOT / "proof/verify_cycle_199_abel_pole_geometry.py",
        "b92e7d3512b289fb411ecbd4ff65d5ed0c5af9c242f5223f44bd08c947555e3d",
    ),
    "cycle199_full_carrier_replay": (
        ROOT / "proof/verify_cycle_199_full_theta_carrier.py",
        "da80042d716df205b45f7b082d276da25f18508c92142a836b3fc7bfe552375f",
    ),
    "helical_zak": (
        ROOT / "scripts/dimension_six_helical_zak.py",
        "185f79ae0c3e5b560939a81551877cf0d14401100466793cc2d7fa4973061bf0",
    ),
    "alias_normalization": (
        ROOT / "scripts/dimension_six_alias_normalization.py",
        "b80fe677250136f1465679859f513bad7bccd49c8b72cc6e517a4fea300fe971",
    ),
    "preregistration_validator": (
        ROOT / "../../tools/preregistration_check.py",
        "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
    ),
    "scaffold": (
        ROOT / "proof/cycle_seal_v1.py",
        "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1",
    ),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 200 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = jet_run()
    poles = result["paired_pole_jet_parity"]
    regular = result["first_off_support_coefficient"]
    packets = result["full_packet_independence"]

    require(poles["retained_orders_through_five"] == [0, 2, 4], "jet parity drift")
    require(poles["odd_delta_jets_source_forbidden_by_pair_symmetry"], "odd-jet parity drift")
    require(poles["all_a_b_rank_upper_bound_through_order_five"] == 30, "pole rank bound drift")
    require("binom(5,b)" in poles["fixed_a_collision_witness"], "collision witness drift")
    require(regular["first_s_coefficient"] == "lambda/(1-cosh(c_beta*Lambda))", "regular coefficient drift")
    require("not a lambda-independent endpoint limit" in regular["rate_dependence"], "rate boundary drift")
    require(packets["analytic_function_rank"] == 36, "off-support rank drift")
    require(packets["row_count"] == 36, "packet census drift")

    return {
        "artifact_id": "cycle-200-b037-regular-residue-jet-v1",
        "cycle": 200,
        "budget_ordinal": "B037",
        "epistemic_status": "PROVED",
        "status": "SEALED_SYMMETRIC_POLE_JET_RANK30_AND_OFF_SUPPORT_PACKET_RANK36",
        "claim_boundary": result["claim_boundary"],
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": (
                "The paired symmetric pole sector of the frozen Abel family has "
                "only even delta jets through order five and cannot retain all "
                "36 rows (rank at most 30). The exact first off-support source "
                "Taylor coefficient instead carries 36 independent analytic "
                "full-character packets, but is Abel-rate dependent and is not "
                "a canonical endpoint object."
            ),
        },
        "paired_pole_jet_parity": poles,
        "first_off_support_coefficient": regular,
        "full_packet_independence": packets,
        "gate_outcome": result["gate_outcome"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "recommendation": (
                "Seal C200 as PROVED for the scoped symmetric endpoint-jet rank "
                "obstruction and the separate rank-36 off-support analytic packet "
                "ledger; keeping it live would conflate two target categories."
            ),
            "known_flaw": (
                "The rank-36 packet is a rate-dependent analytic germ, not a "
                "canonical endpoint distribution or regulator-independent AFK "
                "amplitude."
            ),
            "falsifier": (
                "Any i0 pairing/parity, jet-order, b-degree, rank-at-most-30, "
                "first off-support coefficient, residue-packet phase, analytic-"
                "rank-36, or replay discrepancy."
            ),
            "next_action": (
                "Open a new cycle defining a source-forced two-scale boundary-"
                "germ space that retains the Abel normal variable, then test "
                "whether covariance selects a unique regulator-independent "
                "functional mapping its 36 packet germs to T_6."
            ),
            "adopted": True,
            "reason": (
                "The two exact, noninterchangeable categories are now explicit: "
                "the endpoint pole jet is insufficient, while the rank-complete "
                "germ has not crossed the endpoint-functional boundary."
            ),
        },
        "preregistration_preflight": {
            "cycle": 200,
            "manifest_sha256": sha256(ROOT / "docs/cycle-200-b037-regular-residue-jet-preregistration-v1.md"),
            "validator": {
                "path": "../../tools/preregistration_check.py",
                "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
            },
        },
        "frozen_hashes": frozen,
        "replay": {
            "preflight_command": (
                "research prereg check docs/cycle-200-b037-regular-residue-jet-preregistration-v1.md "
                "--expected-cycle 200 --allow-head-drift"
            ),
            "prototype_command": (
                "python3 proof/verify_cycle_200_regular_residue_jet.py "
                "--output discovery/cycle-200-b037-regular-residue-jet-prototype-v1.json"
            ),
            "test_command": "python3 -m unittest tests/test_cycle_200_regular_residue_jet.py",
            "write_command": "python3 proof/build_cycle_200_regular_residue_jet_v1.py --write",
            "check_command": "python3 proof/build_cycle_200_regular_residue_jet_v1.py --check",
        },
        "runtime": runtime,
        "sealer": {
            "path": "proof/build_cycle_200_regular_residue_jet_v1.py",
            "sha256": sha256(Path(__file__)),
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
