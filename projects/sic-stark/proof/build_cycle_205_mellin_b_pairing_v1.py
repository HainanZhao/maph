#!/usr/bin/env python3
"""Seal Cycle 205/B042's local b-Mellin obstruction."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_205_mellin_b_pairing import run as mellin_run


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-205-b042-mellin-b-pairing-v1.json"
INPUTS = {
    "prior_b_normal_bundle": (
        ROOT / "artifacts/cycle-204-b041-log-normal-bundle-v1.json",
        "d8be2371f47e1c2720db90e5640c7e8c64c0fabd0689bccab4f9aaaa85a63d16",
    ),
    "prior_two_scale_germ": (
        ROOT / "artifacts/cycle-201-b038-two-scale-germ-covariance-v1.json",
        "4a0e02ae9bc419add49a49ac0de88a2e33524a94fa5cfaed24e2d52139b03204",
    ),
    "prior_regular_jet": (
        ROOT / "artifacts/cycle-200-b037-regular-residue-jet-v1.json",
        "f5ca2891ed59bc82af8da8f8bfcfe7d35f834e205291ae640fd1c57009655cae",
    ),
    "prior_endpoint_functional": (
        ROOT / "artifacts/cycle-198-b035-analytic-frequency-endpoint-v1.json",
        "78328f0e8df4ea566fea804cef79217ad1201ca028004d911b7f43871e8f9a3f",
    ),
    "preregistration": (
        ROOT / "docs/cycle-205-b042-mellin-b-pairing-preregistration-v1.md",
        "ff640e4506540bc8455ccd7ba6204e6ef5f86ad5a4846a9ed547fd188600740a",
    ),
    "replay": (
        ROOT / "proof/verify_cycle_205_mellin_b_pairing.py",
        "b88166f09d7b394237cad0303a8b571c63bbf7f021ec692dd64aa9d335b57932",
    ),
    "regression_test": (
        ROOT / "tests/test_cycle_205_mellin_b_pairing.py",
        "21bac78d92b2d7eb7dc32d26bc17567e24a49f31a6f670210b8ca92c4e3fe258",
    ),
    "prototype": (
        ROOT / "discovery/cycle-205-b042-mellin-b-pairing-prototype-v1.json",
        "0753962b10250131f43afb6d9a033a077504676c895138f360fc7353e1ffd6f8",
    ),
    "cycle204_replay": (
        ROOT / "proof/verify_cycle_204_log_normal_bundle.py",
        "3888db09f707091911b57f3f99beac2a03151d40ff81f2910cc685661d4cba31",
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
    runtime = check_runtime("Cycle 205 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = mellin_run()
    singularity = result["local_mellin_singularity"]
    rows = result["all_row_residue_ledger"]
    operations = result["local_operation_consequence"]

    require(singularity["forced_pole"] == "z=-1", "Mellin pole drift")
    require(singularity["forced_residue_abel_rate_weight"] == 1, "Mellin residue weight drift")
    require(singularity["leading_term_laurent_finite_coefficient"] == "0", "Mellin finite coefficient drift")
    require(rows["row_count"] == 36 and rows["rate_weight"] == 1, "Mellin row ledger drift")
    combination = operations["candidate_3_rate_independent_linear_combination_with_B"]
    require(combination["surviving_boundary_rank_upper_bound"] == 30, "Mellin boundary rank drift")

    return {
        "artifact_id": "cycle-205-b042-mellin-b-pairing-v1",
        "cycle": 205,
        "budget_ordinal": "B042",
        "epistemic_status": "PROVED",
        "status": "SEALED_LOCAL_B_MELLIN_FORCED_OPERATIONS_FIXED_TARGET_MAP_FALSIFIED",
        "claim_boundary": result["claim_boundary"],
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": (
                "The sole local b-Mellin pole forced by the first-order source "
                "germ is z=-1 with residue lambda*R of rate weight one. Its "
                "leading finite coefficient is zero, and no forced local "
                "operation supplies a direct all-36 fixed-target map."
            ),
        },
        "local_mellin_singularity": singularity,
        "all_row_residue_ledger": rows,
        "local_operation_consequence": operations,
        "gate_outcome": result["gate_outcome"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "recommendation": (
                "Seal C205 as PROVED only for the local first-order b-Mellin "
                "residue/finite-part class; that asymptotic is exactly exhausted."
            ),
            "known_flaw": (
                "The no-go does not constrain a global equation-(66) Mellin "
                "transform, line-valued/covariant target, projective ratios, "
                "nonlinear operation, higher germ, or non-Abel route."
            ),
            "falsifier": (
                "Any forced-pole location, residue weight, zero finite "
                "coefficient, first-order remainder boundary, rank-at-most-30, "
                "rate-invariance, or replay discrepancy."
            ),
            "next_action": (
                "Open a projective line-valued interface cycle: retain the common "
                "weight-one normal line, pass the 36 packet vector to projective "
                "ratios/cross-ratios where regulator scaling cancels, and test "
                "exact C198/A6 covariance before seeking one independent scalar "
                "normalization."
            ),
            "adopted": True,
            "reason": (
                "The local source asymptotic now has an exact Mellin accounting, "
                "while all global and projective routes remain explicitly outside "
                "the claim."
            ),
        },
        "preregistration_preflight": {
            "cycle": 205,
            "manifest_sha256": sha256(ROOT / "docs/cycle-205-b042-mellin-b-pairing-preregistration-v1.md"),
            "validator": {
                "path": "../../tools/preregistration_check.py",
                "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
            },
        },
        "frozen_hashes": frozen,
        "replay": {
            "preflight_command": (
                "research prereg check docs/cycle-205-b042-mellin-b-pairing-preregistration-v1.md "
                "--expected-cycle 205 --allow-head-drift"
            ),
            "prototype_command": (
                "python3 proof/verify_cycle_205_mellin_b_pairing.py "
                "--output discovery/cycle-205-b042-mellin-b-pairing-prototype-v1.json"
            ),
            "test_command": "python3 -m unittest tests/test_cycle_205_mellin_b_pairing.py",
            "write_command": "python3 proof/build_cycle_205_mellin_b_pairing_v1.py --write",
            "check_command": "python3 proof/build_cycle_205_mellin_b_pairing_v1.py --check",
        },
        "runtime": runtime,
        "sealer": {
            "path": "proof/build_cycle_205_mellin_b_pairing_v1.py",
            "sha256": sha256(Path(__file__)),
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
