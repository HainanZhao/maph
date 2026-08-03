#!/usr/bin/env python3
"""Seal Cycle 201/B038's linear regulator-invariant germ obstruction."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_201_two_scale_germ_covariance import run as covariance_run


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-201-b038-two-scale-germ-covariance-v1.json"
INPUTS = {
    "prior_regular_residue_jet": (
        ROOT / "artifacts/cycle-200-b037-regular-residue-jet-v1.json",
        "f5ca2891ed59bc82af8da8f8bfcfe7d35f834e205291ae640fd1c57009655cae",
    ),
    "prior_full_phase_boundary": (
        ROOT / "artifacts/cycle-199-b036-full-phase-abel-boundary-v1.json",
        "97e0100205df7e0ea73e9b61ab8e6278a146afe05d3000300ae57788be2c253e",
    ),
    "prior_endpoint_functional": (
        ROOT / "artifacts/cycle-198-b035-analytic-frequency-endpoint-v1.json",
        "78328f0e8df4ea566fea804cef79217ad1201ca028004d911b7f43871e8f9a3f",
    ),
    "preregistration": (
        ROOT / "docs/cycle-201-b038-two-scale-germ-covariance-preregistration-v1.md",
        "b05fd2c8a80758c2d2c80bc3625bd764b6d320f3014e7790fab429bc32d32f93",
    ),
    "replay": (
        ROOT / "proof/verify_cycle_201_two_scale_germ_covariance.py",
        "fdaabd5600ca0d247373a2881a3b36556a9a8d16dc5d85cdca69441dd6afc9de",
    ),
    "regression_test": (
        ROOT / "tests/test_cycle_201_two_scale_germ_covariance.py",
        "bc4b1109a5ad451fcaaf5394b5ed9945f76ab5feb5f4429f3fe142c8d31ec1f3",
    ),
    "prototype": (
        ROOT / "discovery/cycle-201-b038-two-scale-germ-covariance-prototype-v1.json",
        "137c98c245dfd8c4f8d3c2258e702a85903798f286583340fafbcf70e9af42b9",
    ),
    "cycle200_replay": (
        ROOT / "proof/verify_cycle_200_regular_residue_jet.py",
        "c93c8f6e9341e3c94714f558176a726ba30ac63c2a2e6056114e8a4328b0a2e9",
    ),
    "cycle199_replay": (
        ROOT / "proof/verify_cycle_199_full_phase_abel_boundary.py",
        "2ee95df4cf6b418ac2ad8736c6171ddc983412c7dd82567b56526aa88f585f0d",
    ),
    "cycle198_replay": (
        ROOT / "proof/verify_cycle_198_analytic_frequency_endpoint.py",
        "fd659f66af2d31dbe1e94d6956a22be211ce279cfb93253ee91e0fb2bebb169d",
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
    runtime = check_runtime("Cycle 201 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = covariance_run()
    action = result["source_regulator_action"]
    no_go = result["invariant_linear_functional_no_go"]
    rank = result["all_row_rank_consequence"]

    require(action["dilations"] == [2, 3, 5], "dilation ledger drift")
    require(action["regular_weight"] == 1, "regular weight drift")
    require(no_go["restriction_on_E_reg"] == "zero", "invariant restriction drift")
    require(rank["surviving_boundary_rank_upper_bound"] == 30, "surviving rank drift")
    require(rank["C198_distinct_target_basis_dimension"] == 36, "target census drift")
    require(rank["linear_all36_target_map_impossible"], "all-row no-go drift")

    return {
        "artifact_id": "cycle-201-b038-two-scale-germ-covariance-v1",
        "cycle": 201,
        "budget_ordinal": "B038",
        "epistemic_status": "PROVED",
        "status": "SEALED_LINEAR_REGULATOR_INVARIANT_TWO_SCALE_FUNCTIONAL_FALSIFIED",
        "claim_boundary": result["claim_boundary"],
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": (
                "No complex-linear Abel-rate-independent functional on the "
                "declared two-scale germ can retain the rank-36 regular "
                "component: regulator dilation forces its restriction to zero, "
                "leaving rank at most 30 and no linear all-36 T_6 map."
            ),
        },
        "source_regulator_action": action,
        "invariant_linear_functional_no_go": no_go,
        "all_row_rank_consequence": rank,
        "gate_outcome": result["gate_outcome"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "recommendation": (
                "Seal C201 as PROVED only for the complex-linear Abel-rate-"
                "independent functional class; the dilation argument exactly "
                "exhausts that category."
            ),
            "known_flaw": (
                "The no-go does not constrain homogeneous rate-covariant "
                "renormalizations, normal derivatives, nonlinear functionals, "
                "higher germs, or non-Abel continuations."
            ),
            "falsifier": (
                "Any regulator-dilation, fixed-boundary/scaled-regular "
                "decomposition, invariance equation, surviving-rank, T_6-"
                "independence, or replay discrepancy."
            ),
            "next_action": (
                "Preregister the source normal derivative "
                "R=lim_(lambda->0) lambda^(-1)(G_lambda-B) as a weight-one "
                "rate-covariant functional, then test its exact 36-row "
                "covariance and amplitude match without fitted normalization."
            ),
            "adopted": True,
            "reason": (
                "The source action is exact and the rank consequence is purely "
                "linear; the remaining categories have been kept out of the "
                "claim boundary."
            ),
        },
        "preregistration_preflight": {
            "cycle": 201,
            "manifest_sha256": sha256(ROOT / "docs/cycle-201-b038-two-scale-germ-covariance-preregistration-v1.md"),
            "validator": {
                "path": "../../tools/preregistration_check.py",
                "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
            },
        },
        "frozen_hashes": frozen,
        "replay": {
            "preflight_command": (
                "research prereg check docs/cycle-201-b038-two-scale-germ-covariance-preregistration-v1.md "
                "--expected-cycle 201 --allow-head-drift"
            ),
            "prototype_command": (
                "python3 proof/verify_cycle_201_two_scale_germ_covariance.py "
                "--output discovery/cycle-201-b038-two-scale-germ-covariance-prototype-v1.json"
            ),
            "test_command": "python3 -m unittest tests/test_cycle_201_two_scale_germ_covariance.py",
            "write_command": "python3 proof/build_cycle_201_two_scale_germ_covariance_v1.py --write",
            "check_command": "python3 proof/build_cycle_201_two_scale_germ_covariance_v1.py --check",
        },
        "runtime": runtime,
        "sealer": {
            "path": "proof/build_cycle_201_two_scale_germ_covariance_v1.py",
            "sha256": sha256(Path(__file__)),
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
