#!/usr/bin/env python3
"""Seal Cycle 223/B060's explicit signed-product containment."""
from __future__ import annotations

from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_223_explicit_signed_product import run as product_run


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-223-b060-explicit-signed-product-v1.json"
INPUTS = {
    "prior_cocycle_torsor": (
        ROOT / "artifacts/cycle-222-b059-z-label-cocycle-v1.json",
        "83faa1a1fcad0f31f6cf142c5098069f82401ebf61e2b5244cb6fd0817bb0ae8",
    ),
    "preregistration": (
        ROOT / "docs/cycle-223-b060-explicit-signed-product-preregistration-v1.md",
        "8ffbe17f8f4d7e9d64c788575a75914a2065970d8a8f0a50626012839a517a24",
    ),
    "replay": (
        ROOT / "proof/verify_cycle_223_explicit_signed_product.py",
        "817b49c05b84ded6f55650d6717349f8ad2b6ea2fc3588919dd14f2578ecc6bb",
    ),
    "regression_test": (
        ROOT / "tests/test_cycle_223_explicit_signed_product.py",
        "6b565867cdf01462356fcc6995112448b9693e00c63847d2810805b2d70f382f",
    ),
    "prototype": (
        ROOT / "discovery/cycle-223-b060-explicit-signed-product-prototype-v1.json",
        "a19b1c6742ee4e64f88b12866cd3ef7b86dab2f0c030c7996ca6130aeacea722",
    ),
    "prior_tilde": (
        ROOT / "proof/verify_cycle_221_tilde_inversion.py",
        "a8db4b32f28b6e43246c11764f08fb60206a866c10e4f7e48a8b4f1783f93bd3",
    ),
    "prior_groupoid": (
        ROOT / "proof/verify_cycle_217_source_transformation_groupoid.py",
        "e038ffb0d9ab95d4eb6edfbf99eaf8ddbb046ba52fa46b8cb84b4c2bdeb3b465",
    ),
    "source_audit": (
        ROOT / "scripts/dimension_six_ss_evaluation_audit.py",
        "24c9258e46a1233c552017f3b58de0d45acd0197c8c807579f090ca1332f626f",
    ),
    "source_paper": (
        ROOT / "paper/sic-stark-dimension-six-boundary-fusion.tex",
        "347228e05a87946ca41bb31c118aae069b7fb6002fff4933d030a153cef21cb7",
    ),
    "validator": (
        ROOT / "../../tools/preregistration_check.py",
        "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
    ),
    "scaffold": (
        ROOT / "proof/cycle_seal_v1.py",
        "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1",
    ),
}


def payload() -> dict[str, object]:
    frozen = freeze_inputs(ROOT, INPUTS)
    result = product_run()
    candidates = result["candidate_state_audit"]
    first = result["first_shift_audit"]
    second = result["second_shift_audit"]
    downstream = result["downstream_identity_audit"]
    require(candidates["candidate_count"] == 4, "candidate census drift")
    require(first["all_match"], "first-shift parity repair drift")
    require(not second["all_match"], "unexpected second-shift closure")
    require(
        {row["residual"] for row in second["rows"]} == {"exp(pi*i*tilde-tau)"},
        "second-shift residual drift",
    )
    require(downstream["factorization_16_17"] == "not_reached_after_failed_second_shift", "unearned factorization")
    return {
        "artifact_id": "cycle-223-b060-explicit-signed-product-v1",
        "cycle": 223,
        "budget_ordinal": "B060",
        "epistemic_status": "PROVED",
        "status": "SEALED_EXPLICIT_PARITY_SIGNED_PRODUCT_SECOND_SHIFT_FAILURE",
        "claim_boundary": result["claim_boundary"],
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": "All four explicit parity-corrected candidates satisfy the first frozen shift but fail the second by the same nonconstant exp(pi*i*tilde-tau) factor.",
        },
        "candidate_state_audit": candidates,
        "first_shift_audit": first,
        "second_shift_audit": second,
        "downstream_identity_audit": downstream,
        "gate_outcome": result["gate_outcome"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "evidence_scope_review": "The complete survivor/epsilon census, reflection-label normalization, parity first-shift repair, second-shift ratio, and sigma/epsilon-independent residual were reviewed as one frozen construction.",
            "recommendation": "Seal C223/B060 as PROVED only for failure of the four parity-corrected signed-product candidates under the second shift.",
            "known_flaw": "The residual exp(pi*i*tilde-tau) excludes only period-only normalization; an argument-dependent exponential cochain or different product can still repair the shift law.",
            "falsifier": "Any survivor/epsilon census, reflection-label normalization, parity first-shift repair, second-shift ratio, sigma/epsilon independence, or replay discrepancy invalidates the seal.",
            "next_action": "Open a shift-cohomology cycle: freeze the two source shift actions, solve their exact multiplicative cocycle equations for a minimal argument-dependent exponential cochain, check commutator integrability and uniqueness, then retest reflection, involutivity, and both factorizations.",
            "adopted": True,
            "reason": "The specified four-candidate product family is exhausted; a nontrivial shift cochain is a distinct construction.",
        },
        "preregistration_preflight": {
            "cycle": 223,
            "manifest_sha256": sha256(ROOT / "docs/cycle-223-b060-explicit-signed-product-preregistration-v1.md"),
            "validator": {
                "path": "../../tools/preregistration_check.py",
                "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
            },
        },
        "frozen_hashes": frozen,
        "replay": {
            "preflight_command": "research prereg check docs/cycle-223-b060-explicit-signed-product-preregistration-v1.md --expected-cycle 223 --allow-head-drift",
            "prototype_command": "python3 proof/verify_cycle_223_explicit_signed_product.py --output discovery/cycle-223-b060-explicit-signed-product-prototype-v1.json",
            "test_command": "python3 -m unittest tests/test_cycle_223_explicit_signed_product.py",
            "write_command": "python3 proof/build_cycle_223_explicit_signed_product_v1.py --write",
            "check_command": "python3 proof/build_cycle_223_explicit_signed_product_v1.py --check",
        },
        "runtime": check_runtime("Cycle 223 seal"),
        "sealer": {"path": "proof/build_cycle_223_explicit_signed_product_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
