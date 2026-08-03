#!/usr/bin/env python3
"""Seal Cycle 207/B044's target-binomial factorwise recurrence obstruction."""
from __future__ import annotations

from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_207_target_binomial_recurrence import run as recurrence_run


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-207-b044-target-binomial-recurrence-v1.json"
INPUTS = {
    "prior_projective_packet": (
        ROOT / "artifacts/cycle-206-b043-projective-line-interface-v1.json",
        "a1ce1e2a0e0d9b42032dd984d9f7f7161f90e080bdf22d38650c097adfa90c8d",
    ),
    "prior_local_mellin": (
        ROOT / "artifacts/cycle-205-b042-mellin-b-pairing-v1.json",
        "477b4fba561c2a9f70d6193cc789f041f9ac65ae693c1961dbfd7afc9e6d0498",
    ),
    "prior_endpoint_functional": (
        ROOT / "artifacts/cycle-198-b035-analytic-frequency-endpoint-v1.json",
        "78328f0e8df4ea566fea804cef79217ad1201ca028004d911b7f43871e8f9a3f",
    ),
    "preregistration": (
        ROOT / "docs/cycle-207-b044-target-binomial-recurrence-preregistration-v1.md",
        "92efe7ce27ad7cf420268cc9c136f161601e7d4ec88da6967e565a3b63194d5d",
    ),
    "replay": (
        ROOT / "proof/verify_cycle_207_target_binomial_recurrence.py",
        "ca96ddc959520f093a1c6cb13b063e8530355568b4f2691ab275c5240fe3949f",
    ),
    "regression_test": (
        ROOT / "tests/test_cycle_207_target_binomial_recurrence.py",
        "870810e414938fd1320624feb6c41e0b880178a4ee5fcde5c51cd27a20f71f8b",
    ),
    "prototype": (
        ROOT / "discovery/cycle-207-b044-target-binomial-recurrence-prototype-v1.json",
        "d29fd6407413ef10874dbb33a3d066f5868b810caa2733c095f3b6263faba80f",
    ),
    "cycle206_replay": (
        ROOT / "proof/verify_cycle_206_projective_line_interface.py",
        "8e7769231af66c146f3e5b187bea6b4fe23f9c00c3359f2a606110e98019145a",
    ),
    "cycle198_replay": (
        ROOT / "proof/verify_cycle_198_analytic_frequency_endpoint.py",
        "fd659f66af2d31dbe1e94d6956a22be211ce279cfb93253ee91e0fb2bebb169d",
    ),
    "cycle190_replay": (
        ROOT / "proof/verify_cycle_190_balanced_helical_reflection.py",
        "69da849d11c00ec30a5bca1a1220e1616d3d31beb75c8b906e8a67a9b0c98469",
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
    runtime = check_runtime("Cycle 207 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = recurrence_run()
    basis = result["relation_basis_audit"]
    binomials = result["target_binomial_ledger"]

    require(basis["T1_T2_preserve_class"], "T1/T2 class law drift")
    require(basis["reflection_negates_class"], "reflection class law drift")
    require(binomials["target_binomial_count"] == 25, "target binomial census drift")
    require(
        binomials["factorwise_signature_mismatch_count"] == 25,
        "factorwise signature mismatch census drift",
    )
    require(
        binomials["factorwise_signature_match_count"] == 0,
        "unexpected factorwise signature match",
    )
    require(
        all(
            row["endpoint_value_status"] == "NOT_EVALUATED_NO_NONVANISHING_CLAIM"
            for row in binomials["records"]
        ),
        "endpoint-value claim drift",
    )

    return {
        "artifact_id": "cycle-207-b044-target-binomial-recurrence-v1",
        "cycle": 207,
        "budget_ordinal": "B044",
        "epistemic_status": "PROVED",
        "status": "SEALED_TARGET_BINOMIAL_FACTORWISE_RECURRENCE_ROUTE_FALSIFIED",
        "claim_boundary": result["claim_boundary"],
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": (
                "Every one of the 25 elementary C198 target binomials has "
                "mismatched four-factor recurrence signatures. No identity "
                "obtained solely by the declared factorwise T1/T2/reflection "
                "basis can make any of those binomials vanish."
            ),
        },
        "relation_basis_audit": basis,
        "target_binomial_ledger": binomials,
        "gate_outcome": result["gate_outcome"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "recommendation": (
                "Seal C207/B044 as PROVED only for failure of the declared "
                "factorwise T1/T2/reflection derivation on all 25 target squares, "
                "then move to a genuinely multifactor engine."
            ),
            "known_flaw": (
                "Signature mismatch does not evaluate any endpoint minor and "
                "excludes neither duplication/addition formulas, equation-(66) "
                "global pairings, determinant identities, nor direct certified "
                "endpoint evaluation."
            ),
            "falsifier": (
                "Any class formula, shift/reflection law, endpoint factor encoding, "
                "unoriented-signature census, common-scalar handling, or replay "
                "discrepancy."
            ),
            "next_action": (
                "Express one symmetry-representative 2-by-2 target minor through "
                "a polarized equation-(66) global pairing or determinant identity; "
                "an exact nonzero value falsifies projective equality, while "
                "vanishing must then be propagated to all 25 squares without "
                "factorwise matching."
            ),
            "adopted": True,
            "reason": (
                "The full finite recurrence census is exact, while the companion "
                "keeps every nonfactorwise identity and endpoint evaluation outside "
                "the claim boundary."
            ),
        },
        "preregistration_preflight": {
            "cycle": 207,
            "manifest_sha256": sha256(ROOT / "docs/cycle-207-b044-target-binomial-recurrence-preregistration-v1.md"),
            "validator": {
                "path": "../../tools/preregistration_check.py",
                "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
            },
        },
        "frozen_hashes": frozen,
        "replay": {
            "preflight_command": (
                "research prereg check docs/cycle-207-b044-target-binomial-recurrence-preregistration-v1.md "
                "--expected-cycle 207 --allow-head-drift"
            ),
            "prototype_command": (
                "python3 proof/verify_cycle_207_target_binomial_recurrence.py "
                "--output discovery/cycle-207-b044-target-binomial-recurrence-prototype-v1.json"
            ),
            "test_command": "python3 -m unittest tests/test_cycle_207_target_binomial_recurrence.py",
            "write_command": "python3 proof/build_cycle_207_target_binomial_recurrence_v1.py --write",
            "check_command": "python3 proof/build_cycle_207_target_binomial_recurrence_v1.py --check",
        },
        "runtime": runtime,
        "sealer": {
            "path": "proof/build_cycle_207_target_binomial_recurrence_v1.py",
            "sha256": sha256(Path(__file__)),
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
