#!/usr/bin/env python3
"""Seal Cycle 204/B041's bare b-normal weight obstruction."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_204_log_normal_bundle import run as b_run


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-204-b041-log-normal-bundle-v1.json"
INPUTS = {
    "prior_ordinary_normal_line": (
        ROOT / "artifacts/cycle-203-b040-inverse-normal-line-v1.json",
        "a8382ed299a8985f444510b5a18e2406692d2a82e1c5b428ba2f5440640f1f41",
    ),
    "prior_normal_target_weight": (
        ROOT / "artifacts/cycle-202-b039-normal-derivative-target-weight-v1.json",
        "09f860f92611a953538d7dcd32a1040be92e15e412ce712a01bc538287c1c426",
    ),
    "prior_two_scale_germ": (
        ROOT / "artifacts/cycle-201-b038-two-scale-germ-covariance-v1.json",
        "4a0e02ae9bc419add49a49ac0de88a2e33524a94fa5cfaed24e2d52139b03204",
    ),
    "prior_regular_jet": (
        ROOT / "artifacts/cycle-200-b037-regular-residue-jet-v1.json",
        "f5ca2891ed59bc82af8da8f8bfcfe7d35f834e205291ae640fd1c57009655cae",
    ),
    "preregistration": (
        ROOT / "docs/cycle-204-b041-log-normal-bundle-preregistration-v1.md",
        "1e6b411a0f8848c720e4bb5f206f96833b41834cf6ff8ed56b5d9ec3e29ca6f8",
    ),
    "replay": (
        ROOT / "proof/verify_cycle_204_log_normal_bundle.py",
        "3888db09f707091911b57f3f99beac2a03151d40ff81f2910cc685661d4cba31",
    ),
    "regression_test": (
        ROOT / "tests/test_cycle_204_log_normal_bundle.py",
        "7f3d8b7a172c85c8d04d6019ab11a91f5604dfe531506de94b2eb054c79ac3d7",
    ),
    "prototype": (
        ROOT / "discovery/cycle-204-b041-log-normal-bundle-prototype-v1.json",
        "712331535d307018306b439ed834773057d2690cba1706c89581519bb9246dab",
    ),
    "cycle203_replay": (
        ROOT / "proof/verify_cycle_203_inverse_normal_line.py",
        "76a569b5812d64e13e3c0a2533442a5765c40fa2c0535026bdf60e1e9b0d9b71",
    ),
    "cycle202_replay": (
        ROOT / "proof/verify_cycle_202_normal_derivative_target_weight.py",
        "00da578ee6c67b1cbf67b8c8802804dd5af560bf29e67ba7aeb4d18b92c16116",
    ),
    "cycle201_replay": (
        ROOT / "proof/verify_cycle_201_two_scale_germ_covariance.py",
        "fdaabd5600ca0d247373a2881a3b36556a9a8d16dc5d85cdca69441dd6afc9de",
    ),
    "cycle200_replay": (
        ROOT / "proof/verify_cycle_200_regular_residue_jet.py",
        "c93c8f6e9341e3c94714f558176a726ba30ac63c2a2e6056114e8a4328b0a2e9",
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
    runtime = check_runtime("Cycle 204 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = b_run()
    generators = result["b_generator_ledger"]
    tensors = result["tensor_weight_ledger"]
    targets = result["fixed_target_consequence"]

    require(generators["abel_rate_weight"] == 0, "b-generator weight drift")
    require(tensors["row_count"] == 36, "b-tensor census drift")
    require(tensors["all_candidate_abel_rate_weight"] == 1, "b-tensor weight drift")
    require(targets["direct_linear_fixed_target_map_impossible"], "b-target no-go drift")
    require([row["q"] for row in targets["contradictions"]] == [2, 3, 5], "dilation drift")

    return {
        "artifact_id": "cycle-204-b041-log-normal-bundle-v1",
        "cycle": 204,
        "budget_ordinal": "B041",
        "epistemic_status": "PROVED",
        "status": "SEALED_BARE_LOG_NORMAL_OBJECTS_FIXED_TARGET_MAP_FALSIFIED",
        "claim_boundary": result["claim_boundary"],
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": (
                "The b-normal generators are source-geometrically canonical, "
                "but have Abel-rate weight zero. Every declared tensor with the "
                "rank-36 normal packets retains weight one, so no direct linear "
                "fixed-target C198 amplitude map follows."
            ),
        },
        "b_generator_ledger": generators,
        "tensor_weight_ledger": tensors,
        "fixed_target_consequence": targets,
        "gate_outcome": result["gate_outcome"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "recommendation": (
                "Seal C204 as PROVED only for failure of the bare b-normal "
                "generators to convert the weight-one packets into fixed "
                "weight-zero C198 amplitudes."
            ),
            "known_flaw": (
                "The result excludes no source-derived b-pairing, Mellin "
                "residue/finite part, covariant target, nonlinear operation, "
                "higher germ, or non-Abel continuation."
            ),
            "falsifier": (
                "Any b-generator invariance, contraction/tensor weight, "
                "regulator-dilation, 36-row nonvanishing, target-weight, or "
                "replay discrepancy."
            ),
            "next_action": (
                "Derive an equation-(66) Mellin/b-pairing on the logarithmic "
                "normal variable, with homogeneity exponent fixed from the source "
                "asymptotic, then test whether its residue or finite part is "
                "regulator-independent and matches all 36 C198 targets."
            ),
            "adopted": True,
            "reason": (
                "The b-category was tested as a distinct construction and its "
                "precise remaining missing operation is now a source pairing, not "
                "a coordinate convention."
            ),
        },
        "preregistration_preflight": {
            "cycle": 204,
            "manifest_sha256": sha256(ROOT / "docs/cycle-204-b041-log-normal-bundle-preregistration-v1.md"),
            "validator": {
                "path": "../../tools/preregistration_check.py",
                "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
            },
        },
        "frozen_hashes": frozen,
        "replay": {
            "preflight_command": (
                "research prereg check docs/cycle-204-b041-log-normal-bundle-preregistration-v1.md "
                "--expected-cycle 204 --allow-head-drift"
            ),
            "prototype_command": (
                "python3 proof/verify_cycle_204_log_normal_bundle.py "
                "--output discovery/cycle-204-b041-log-normal-bundle-prototype-v1.json"
            ),
            "test_command": "python3 -m unittest tests/test_cycle_204_log_normal_bundle.py",
            "write_command": "python3 proof/build_cycle_204_log_normal_bundle_v1.py --write",
            "check_command": "python3 proof/build_cycle_204_log_normal_bundle_v1.py --check",
        },
        "runtime": runtime,
        "sealer": {
            "path": "proof/build_cycle_204_log_normal_bundle_v1.py",
            "sha256": sha256(Path(__file__)),
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
