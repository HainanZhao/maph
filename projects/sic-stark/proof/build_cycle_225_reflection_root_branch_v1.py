#!/usr/bin/env python3
"""Seal Cycle 225/B062's reflection-root local branch containment."""
from __future__ import annotations

from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_225_reflection_root_branch import run as branch_run


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-225-b062-reflection-root-branch-v1.json"
INPUTS = {
    "prior_shift_branch": (
        ROOT / "artifacts/cycle-224-b061-shift-cohomology-v1.json",
        "a24b0573942c5bd869240f7444f6db0542e5a0899d64e1ba1704625c8a5e7a26",
    ),
    "preregistration": (
        ROOT / "docs/cycle-225-b062-reflection-root-branch-preregistration-v1.md",
        "8b2188e3befa2f7ce7a8f4a9e0f3938110dd94be659ce64154c6eb6bdcdaf921",
    ),
    "replay": (
        ROOT / "proof/verify_cycle_225_reflection_root_branch.py",
        "3f4867787a55a42f3d594df4bd5e898edddbd035c5c3777f879aeea477c57317",
    ),
    "regression_test": (
        ROOT / "tests/test_cycle_225_reflection_root_branch.py",
        "83f3a808464ba7f5494f65d116ac1b6a31a90ed65875ceb9411821447a190ae9",
    ),
    "prototype": (
        ROOT / "discovery/cycle-225-b062-reflection-root-branch-prototype-v1.json",
        "d59f79bb701c28e586a98a7cb0901b3bc245ed888f0b06db809cc1c352c5c823",
    ),
    "prior_shift_replay": (
        ROOT / "proof/verify_cycle_224_shift_cohomology.py",
        "14f5ee54d596e2775e9671fbd13fc2053b18af863d28552de8b21da5de2035aa",
    ),
    "prior_product_replay": (
        ROOT / "proof/verify_cycle_223_explicit_signed_product.py",
        "817b49c05b84ded6f55650d6717349f8ad2b6ea2fc3588919dd14f2578ecc6bb",
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
    result = branch_run()
    roots = result["root_branch_audit"]
    action = result["double_sign_action_audit"]
    factors = result["factorization_state_audit"]
    acceptance = result["acceptance_audit"]
    require(roots["candidate_count"] == 4, "root branch census drift")
    require(all(row["first_shift"] and row["second_shift"] for row in roots["rows"]), "shift closure drift")
    require(all(row["conjugate_action_involutive"] for row in action["rows"]), "conjugate involutivity drift")
    require(not factors["equation_16_pullback_defined"], "unearned F2 pullback")
    require(not factors["equation_17_pullback_defined"], "unearned F3 pullback")
    require(not acceptance["accepted_signed_extension"], "unearned extension")
    return {
        "artifact_id": "cycle-225-b062-reflection-root-branch-v1",
        "cycle": 225,
        "budget_ordinal": "B062",
        "epistemic_status": "PROVED",
        "status": "SEALED_REFLECTION_ROOT_LOCAL_BRANCH_FACTORIZATION_UNDEFINED",
        "claim_boundary": result["claim_boundary"],
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": "The c=+/-i local branch satisfies both shifts and reflection, with conjugate double sign involutivity, but lacks both required factorization target states and therefore is not a signed Gamma_M extension.",
        },
        "root_branch_audit": roots,
        "double_sign_action_audit": action,
        "factorization_state_audit": factors,
        "acceptance_audit": acceptance,
        "gate_outcome": result["gate_outcome"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "evidence_scope_review": "The four-branch census, both shifts, -c^2 reflection condition, c-to-conjugate(c) involutivity, factorization target states, and replay were reviewed together.",
            "recommendation": "Seal C225/B062 as PROVED only for the c=+/-i local signed-product branch satisfying shifts, reflection, and conjugate double-sign involutivity; record factorization compatibility as untested because the required states are undefined.",
            "known_flaw": "Local identities at one signed state do not define a Gamma_M theorem or show that the F2/F3 factorization groupoid closes consistently.",
            "falsifier": "Any four-branch census, shift, -c^2 reflection, c-to-conjugate(c) involutivity, required-intermediate-state, or replay discrepancy invalidates the seal.",
            "next_action": "Open a state-complete signed-product groupoid cycle over the full raw four-state orbit and its positive representatives; assign cochains before testing, then solve the F2/F3 edge and loop-consistency equations with every residual factor retained.",
            "adopted": True,
            "reason": "The local branch has exact identities but its missing target states are a categorical boundary, not a scalar correction.",
        },
        "preregistration_preflight": {
            "cycle": 225,
            "manifest_sha256": sha256(ROOT / "docs/cycle-225-b062-reflection-root-branch-preregistration-v1.md"),
            "validator": {
                "path": "../../tools/preregistration_check.py",
                "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
            },
        },
        "frozen_hashes": frozen,
        "replay": {
            "preflight_command": "research prereg check docs/cycle-225-b062-reflection-root-branch-preregistration-v1.md --expected-cycle 225 --allow-head-drift",
            "prototype_command": "python3 proof/verify_cycle_225_reflection_root_branch.py --output discovery/cycle-225-b062-reflection-root-branch-prototype-v1.json",
            "test_command": "python3 -m unittest tests/test_cycle_225_reflection_root_branch.py",
            "write_command": "python3 proof/build_cycle_225_reflection_root_branch_v1.py --write",
            "check_command": "python3 proof/build_cycle_225_reflection_root_branch_v1.py --check",
        },
        "runtime": check_runtime("Cycle 225 seal"),
        "sealer": {"path": "proof/build_cycle_225_reflection_root_branch_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
