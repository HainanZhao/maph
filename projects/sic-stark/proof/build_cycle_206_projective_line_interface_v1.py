#!/usr/bin/env python3
"""Seal Cycle 206/B043's projective normal-packet construction."""
from __future__ import annotations

from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_206_projective_line_interface import run as projective_run


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-206-b043-projective-line-interface-v1.json"
INPUTS = {
    "prior_local_mellin": (
        ROOT / "artifacts/cycle-205-b042-mellin-b-pairing-v1.json",
        "477b4fba561c2a9f70d6193cc789f041f9ac65ae693c1961dbfd7afc9e6d0498",
    ),
    "prior_b_normal_bundle": (
        ROOT / "artifacts/cycle-204-b041-log-normal-bundle-v1.json",
        "d8be2371f47e1c2720db90e5640c7e8c64c0fabd0689bccab4f9aaaa85a63d16",
    ),
    "prior_normal_target_weight": (
        ROOT / "artifacts/cycle-202-b039-normal-derivative-target-weight-v1.json",
        "09f860f92611a953538d7dcd32a1040be92e15e412ce712a01bc538287c1c426",
    ),
    "prior_regular_packet": (
        ROOT / "artifacts/cycle-200-b037-regular-residue-jet-v1.json",
        "f5ca2891ed59bc82af8da8f8bfcfe7d35f834e205291ae640fd1c57009655cae",
    ),
    "prior_endpoint_functional": (
        ROOT / "artifacts/cycle-198-b035-analytic-frequency-endpoint-v1.json",
        "78328f0e8df4ea566fea804cef79217ad1201ca028004d911b7f43871e8f9a3f",
    ),
    "preregistration": (
        ROOT / "docs/cycle-206-b043-projective-line-interface-preregistration-v1.md",
        "9c981edb02b2c9ff119daa2e940e7b7f5340e7a506b9c3b179b35c5f78650afe",
    ),
    "replay": (
        ROOT / "proof/verify_cycle_206_projective_line_interface.py",
        "8e7769231af66c146f3e5b187bea6b4fe23f9c00c3359f2a606110e98019145a",
    ),
    "regression_test": (
        ROOT / "tests/test_cycle_206_projective_line_interface.py",
        "eb371ebbf13a6b7a7835482a08ec10488cb3a8933593857881d481f8c242ea14",
    ),
    "prototype": (
        ROOT / "discovery/cycle-206-b043-projective-line-interface-prototype-v1.json",
        "453862b27734109c2b415be403d7b5d3ec1f39a533b7b5cf89fd59b135f11092",
    ),
    "cycle205_replay": (
        ROOT / "proof/verify_cycle_205_mellin_b_pairing.py",
        "b88166f09d7b394237cad0303a8b571c63bbf7f021ec692dd64aa9d335b57932",
    ),
    "cycle202_replay": (
        ROOT / "proof/verify_cycle_202_normal_derivative_target_weight.py",
        "00da578ee6c67b1cbf67b8c8802804dd5af560bf29e67ba7aeb4d18b92c16116",
    ),
    "cycle200_replay": (
        ROOT / "proof/verify_cycle_200_regular_residue_jet.py",
        "c93c8f6e9341e3c94714f558176a726ba30ac63c2a2e6056114e8a4328b0a2e9",
    ),
    "cycle198_replay": (
        ROOT / "proof/verify_cycle_198_analytic_frequency_endpoint.py",
        "fd659f66af2d31dbe1e94d6956a22be211ce279cfb93253ee91e0fb2bebb169d",
    ),
    "stabilizer_ledger": (
        ROOT / "scripts/dimension_six_stabilizer_ledger.py",
        "594a0d541478f340abe789234335f3ff1b2d874ad8fa3507ad95026c5cc6276b",
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
    runtime = check_runtime("Cycle 206 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = projective_run()
    source = result["source_projective_packet"]
    binomials = result["elementary_binomial_ledger"]
    covariance = result["common_line_covariance"]
    comparison = result["c198_projective_comparison"]

    require(source["coordinate_count_per_h"] == 36, "source projective coordinate count drift")
    require(source["h_channel_count"] == 6, "source h-channel count drift")
    require(binomials["relation_count"] == 150, "source binomial count drift")
    require(binomials["denominator_free"], "source binomial denominator drift")
    require(binomials["all_relations_identically_zero"], "source binomial relation drift")
    require(covariance["source_projective_covariance"] == "PROVED", "projective covariance drift")
    require(comparison["all_36_targets_finite_nonzero"], "C198 target nonzero drift")
    require(
        comparison["comparison_status"] == "OPEN_REQUIRES_NEW_SOURCE_MULTIPLICATIVE_THEOREM",
        "projective target interface status drift",
    )

    return {
        "artifact_id": "cycle-206-b043-projective-line-interface-v1",
        "cycle": 206,
        "budget_ordinal": "B043",
        "epistemic_status": "PROVED",
        "status": "SEALED_SOURCE_PROJECTIVE_NORMAL_PACKET_TARGET_MULTIPLICATIVE_INTERFACE_OPEN",
        "claim_boundary": result["claim_boundary"],
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": (
                "The complete rank-36 normal packet has a denominator-free "
                "projective quotient with 150 source binomial relations and "
                "common-line A6 covariance. The frozen C198 result has not "
                "supplied the multiplicative relation needed for a projective "
                "source-to-target equality."
            ),
        },
        "source_projective_packet": source,
        "elementary_binomial_ledger": binomials,
        "common_line_covariance": covariance,
        "c198_projective_comparison": comparison,
        "gate_outcome": result["gate_outcome"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "recommendation": (
                "Seal C206/B043 as PROVED for the source projective packet and "
                "its 150 homogeneous relations, then move the gate to a "
                "target-side multiplicative/projective intertwiner test."
            ),
            "known_flaw": (
                "C198 gives labeled nonzero linear endpoint values but no "
                "multiplicative binomial theorem, and the source homogeneous "
                "coordinates have a common-factor base locus outside which the "
                "projective point must be stated."
            ),
            "falsifier": (
                "Any packet exponent, elementary-square, nonvanishing-domain, "
                "A6/common-line covariance, C198 label/nonzero ledger, or replay "
                "discrepancy."
            ),
            "next_action": (
                "Preregister an exact equation-(66) audit of the 25 target "
                "elementary binomials as a necessary condition; a certified "
                "nonzero binomial falsifies projective equality, while universal "
                "vanishing requires labeled row/column-ratio matching without "
                "fitted scalars."
            ),
            "adopted": True,
            "reason": (
                "The projective quotient removes the exact common normal weight "
                "without manufacturing the target-side multiplicative theorem; "
                "the source base locus is explicit."
            ),
        },
        "preregistration_preflight": {
            "cycle": 206,
            "manifest_sha256": sha256(ROOT / "docs/cycle-206-b043-projective-line-interface-preregistration-v1.md"),
            "validator": {
                "path": "../../tools/preregistration_check.py",
                "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
            },
        },
        "frozen_hashes": frozen,
        "replay": {
            "preflight_command": (
                "research prereg check docs/cycle-206-b043-projective-line-interface-preregistration-v1.md "
                "--expected-cycle 206 --allow-head-drift"
            ),
            "prototype_command": (
                "python3 proof/verify_cycle_206_projective_line_interface.py "
                "--output discovery/cycle-206-b043-projective-line-interface-prototype-v1.json"
            ),
            "test_command": "python3 -m unittest tests/test_cycle_206_projective_line_interface.py",
            "write_command": "python3 proof/build_cycle_206_projective_line_interface_v1.py --write",
            "check_command": "python3 proof/build_cycle_206_projective_line_interface_v1.py --check",
        },
        "runtime": runtime,
        "sealer": {
            "path": "proof/build_cycle_206_projective_line_interface_v1.py",
            "sha256": sha256(Path(__file__)),
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
