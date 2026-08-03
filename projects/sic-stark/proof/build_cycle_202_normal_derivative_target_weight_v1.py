#!/usr/bin/env python3
"""Seal Cycle 202/B039's normal-data fixed-target weight obstruction."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_202_normal_derivative_target_weight import run as normal_run


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-202-b039-normal-derivative-target-weight-v1.json"
INPUTS = {
    "prior_two_scale_germ": (
        ROOT / "artifacts/cycle-201-b038-two-scale-germ-covariance-v1.json",
        "4a0e02ae9bc419add49a49ac0de88a2e33524a94fa5cfaed24e2d52139b03204",
    ),
    "prior_regular_residue_jet": (
        ROOT / "artifacts/cycle-200-b037-regular-residue-jet-v1.json",
        "f5ca2891ed59bc82af8da8f8bfcfe7d35f834e205291ae640fd1c57009655cae",
    ),
    "prior_endpoint_functional": (
        ROOT / "artifacts/cycle-198-b035-analytic-frequency-endpoint-v1.json",
        "78328f0e8df4ea566fea804cef79217ad1201ca028004d911b7f43871e8f9a3f",
    ),
    "preregistration": (
        ROOT / "docs/cycle-202-b039-normal-derivative-target-weight-preregistration-v1.md",
        "f64950363aec2598ca1143edbc4d3623968b30bab773d647c4cbb38c71f32800",
    ),
    "replay": (
        ROOT / "proof/verify_cycle_202_normal_derivative_target_weight.py",
        "00da578ee6c67b1cbf67b8c8802804dd5af560bf29e67ba7aeb4d18b92c16116",
    ),
    "regression_test": (
        ROOT / "tests/test_cycle_202_normal_derivative_target_weight.py",
        "6aa15ce50362d52e0aa15812a168c63e90401eb5b0ae6b527dd0af2ce82bfe15",
    ),
    "prototype": (
        ROOT / "discovery/cycle-202-b039-normal-derivative-target-weight-prototype-v1.json",
        "1e7f1a7cea4b6fb461544926d059e9f4a3bcbebdc45ce2f316cc8bfef06f6311",
    ),
    "cycle201_replay": (
        ROOT / "proof/verify_cycle_201_two_scale_germ_covariance.py",
        "fdaabd5600ca0d247373a2881a3b36556a9a8d16dc5d85cdca69441dd6afc9de",
    ),
    "cycle200_replay": (
        ROOT / "proof/verify_cycle_200_regular_residue_jet.py",
        "c93c8f6e9341e3c94714f558176a726ba30ac63c2a2e6056114e8a4328b0a2e9",
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
    runtime = check_runtime("Cycle 202 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = normal_run()
    normal = result["normal_data"]
    targets = result["fixed_targets"]
    contradiction = result["direct_bridge_weight_contradiction"]

    require(normal["row_count"] == 36 and normal["rate_weight"] == 1, "normal ledger drift")
    require(targets["row_count"] == 36 and targets["all_endpoint_values_finite_nonzero"], "target ledger drift")
    require(targets["abel_rate_weight"] == 0, "target weight drift")
    require(contradiction["all_36_direct_equalities_impossible"], "direct bridge drift")
    require([row["q"] for row in contradiction["contradictions"]] == [2, 3, 5], "dilation drift")

    return {
        "artifact_id": "cycle-202-b039-normal-derivative-target-weight-v1",
        "cycle": 202,
        "budget_ordinal": "B039",
        "epistemic_status": "PROVED",
        "status": "SEALED_NORMAL_DATA_TO_FIXED_TARGET_DIRECT_LINEAR_MAP_FALSIFIED",
        "claim_boundary": result["claim_boundary"],
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": (
                "The rank-36 source normal packets have Abel-rate weight one, "
                "whereas each C198 endpoint target is finite, nonzero, and "
                "weight zero. Therefore no complex-linear rate-independent "
                "direct all-36 identification can map the former to the latter."
            ),
        },
        "normal_data": normal,
        "fixed_targets": targets,
        "direct_bridge_weight_contradiction": contradiction,
        "gate_outcome": result["gate_outcome"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "recommendation": (
                "Seal C202 as PROVED only for direct complex-linear rate-"
                "independent identification of the weight-one normal packets "
                "with the weight-zero C198 targets."
            ),
            "known_flaw": (
                "The weight mismatch does not exclude a geometrically twisted "
                "target, nonlinear ratios, higher germs, or non-Abel continuation."
            ),
            "falsifier": (
                "Any source dilation-weight, C198 finiteness/nonvanishing, "
                "target-weight, row coverage, linearity, or replay discrepancy."
            ),
            "next_action": (
                "Construct the geodesic normal line/density intrinsically and "
                "test whether tensoring E_reg with its inverse yields a canonical "
                "weight-zero 36-row map to T_6; lack of a source-defined "
                "trivialization is an exact obstruction."
            ),
            "adopted": True,
            "reason": (
                "The complete all-row source and target ledgers give a direct "
                "weight contradiction while preserving every broader bridge class "
                "outside this sealed claim."
            ),
        },
        "preregistration_preflight": {
            "cycle": 202,
            "manifest_sha256": sha256(ROOT / "docs/cycle-202-b039-normal-derivative-target-weight-preregistration-v1.md"),
            "validator": {
                "path": "../../tools/preregistration_check.py",
                "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
            },
        },
        "frozen_hashes": frozen,
        "replay": {
            "preflight_command": (
                "research prereg check docs/cycle-202-b039-normal-derivative-target-weight-preregistration-v1.md "
                "--expected-cycle 202 --allow-head-drift"
            ),
            "prototype_command": (
                "python3 proof/verify_cycle_202_normal_derivative_target_weight.py "
                "--output discovery/cycle-202-b039-normal-derivative-target-weight-prototype-v1.json"
            ),
            "test_command": "python3 -m unittest tests/test_cycle_202_normal_derivative_target_weight.py",
            "write_command": "python3 proof/build_cycle_202_normal_derivative_target_weight_v1.py --write",
            "check_command": "python3 proof/build_cycle_202_normal_derivative_target_weight_v1.py --check",
        },
        "runtime": runtime,
        "sealer": {
            "path": "proof/build_cycle_202_normal_derivative_target_weight_v1.py",
            "sha256": sha256(Path(__file__)),
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
