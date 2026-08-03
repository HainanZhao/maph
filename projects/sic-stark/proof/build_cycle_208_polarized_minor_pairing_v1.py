#!/usr/bin/env python3
"""Seal Cycle 208/B045's full determinantal pullback criterion."""
from __future__ import annotations

from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_208_polarized_minor_pairing import run as pullback_run


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-208-b045-polarized-minor-pairing-v1.json"
INPUTS = {
    "prior_target_recurrence_obstruction": (
        ROOT / "artifacts/cycle-207-b044-target-binomial-recurrence-v1.json",
        "5393ca0cab06f8f7b37a64aaf006c7da74acb8437c0cd50fe98fd8d88a85bf09",
    ),
    "prior_projective_packet": (
        ROOT / "artifacts/cycle-206-b043-projective-line-interface-v1.json",
        "a1ce1e2a0e0d9b42032dd984d9f7f7161f90e080bdf22d38650c097adfa90c8d",
    ),
    "prior_endpoint_functional": (
        ROOT / "artifacts/cycle-198-b035-analytic-frequency-endpoint-v1.json",
        "78328f0e8df4ea566fea804cef79217ad1201ca028004d911b7f43871e8f9a3f",
    ),
    "preregistration": (
        ROOT / "docs/cycle-208-b045-polarized-minor-pairing-preregistration-v1.md",
        "d03bda52d9bb3660cfcdf817bebad814500cb4c56e998fc6492bedfece449f2d",
    ),
    "replay": (
        ROOT / "proof/verify_cycle_208_polarized_minor_pairing.py",
        "4b54f4c7b82072def905b23abff54ca368274d353ec79aeaaba446f481ee302d",
    ),
    "regression_test": (
        ROOT / "tests/test_cycle_208_polarized_minor_pairing.py",
        "e8301735b59db52f9869f6a9731285760bbd5763ecdbef8b6ffde4aed85612bd",
    ),
    "prototype": (
        ROOT / "discovery/cycle-208-b045-polarized-minor-pairing-prototype-v1.json",
        "48ff89f1307bf0945731be907d3fd95f49eccd3742dd503e95b6ed6b610c7927",
    ),
    "cycle207_replay": (
        ROOT / "proof/verify_cycle_207_target_binomial_recurrence.py",
        "ca96ddc959520f093a1c6cb13b063e8530355568b4f2691ab275c5240fe3949f",
    ),
    "cycle206_replay": (
        ROOT / "proof/verify_cycle_206_projective_line_interface.py",
        "8e7769231af66c146f3e5b187bea6b4fe23f9c00c3359f2a606110e98019145a",
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
    runtime = check_runtime("Cycle 208 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = pullback_run()
    reduction = result["exact_reduction_audit"]
    source = result["source_rank_one_ideal"]
    pullbacks = result["diagonal_pullbacks"]
    witness = result["nonmembership_witness"]
    a6 = result["a6_audit"]

    require(reduction["identity_count"] == 225, "formal pullback identity census drift")
    require(reduction["all_identities_checked"], "formal pullback identity drift")
    require(source["coordinate_count"] == 36, "source coordinate census drift")
    require(source["generator_count"] == 225, "full source-minor census drift")
    require(pullbacks["coefficient_count"] == 36, "coefficient census drift")
    require(pullbacks["pullback_count"] == 225, "full target-minor census drift")
    require(witness["witness_count"] == 225, "nonmembership witness census drift")
    require(a6["A6_mod_6"] == [[1, 0], [0, 1]], "A6 label action drift")
    require(a6["coefficient_constraints_from_A6"] == 0, "A6 coefficient claim drift")
    require(not a6["all_square_reduction_from_A6"], "invalid A6 propagation claim")
    require(
        result["gate_outcome"]["source_interface_coefficients"] == "OPEN_NOT_SUPPLIED",
        "source coefficient status drift",
    )

    return {
        "artifact_id": "cycle-208-b045-polarized-minor-pairing-v1",
        "cycle": 208,
        "budget_ordinal": "B045",
        "epistemic_status": "PROVED",
        "status": "SEALED_FULL_DETERMINANTAL_PULLBACK_CRITERION_SOURCE_COEFFICIENT_INTERFACE_OPEN",
        "claim_boundary": result["claim_boundary"],
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": (
                "For the declared full label-preserving diagonal family, all 225 "
                "target two-by-two minor pullbacks belong to the full rank-one "
                "source ideal exactly when the 36 coefficient array has all 225 "
                "rank-one minors zero. The result neither derives nor selects a "
                "coefficient array."
            ),
        },
        "exact_reduction_audit": reduction,
        "source_rank_one_ideal": source,
        "diagonal_pullbacks": pullbacks,
        "nonmembership_witness": witness,
        "a6_audit": a6,
        "gate_outcome": result["gate_outcome"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "evidence_scope_review": (
                "The complete result is suitable only as the full 225-minor "
                "coordinate-ring pullback criterion for label-preserving diagonal maps."
            ),
            "recommendation": (
                "Seal C208/B045 as PROVED only for the full 225-minor "
                "coordinate-ring pullback criterion for label-preserving diagonal maps."
            ),
            "known_flaw": (
                "The criterion is conditional and supplies no source-authorized "
                "coefficients c, no actual J, no target-minor vanishing, and no "
                "projective amplitude equality; A6 contributes no coefficient "
                "determination because it fixes every label mod 6."
            ),
            "falsifier": (
                "Any determinantal-ideal, pullback formula, monomial "
                "nonvanishing modulo the rank-one ideal, 225-minor census, A6 "
                "label action, or replay discrepancy invalidates the seal."
            ),
            "next_action": (
                "Open a distinct cycle freezing a source-derived equation-(66) "
                "or translation-covariant construction of c; use c_(a,b)=r_a*s_b, "
                "derive r_a and s_b without endpoint fitting, then test the "
                "resulting J against the full labeled C198 projective target."
            ),
            "adopted": True,
            "reason": (
                "The exact reduction, all-ones rank-one nonmembership witness, "
                "and complete A6 census establish the stated criterion while the "
                "companion keeps every coefficient construction and target equality "
                "outside its boundary."
            ),
        },
        "preregistration_preflight": {
            "cycle": 208,
            "manifest_sha256": sha256(ROOT / "docs/cycle-208-b045-polarized-minor-pairing-preregistration-v1.md"),
            "validator": {
                "path": "../../tools/preregistration_check.py",
                "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
            },
        },
        "frozen_hashes": frozen,
        "replay": {
            "preflight_command": (
                "research prereg check docs/cycle-208-b045-polarized-minor-pairing-preregistration-v1.md "
                "--expected-cycle 208 --allow-head-drift"
            ),
            "prototype_command": (
                "python3 proof/verify_cycle_208_polarized_minor_pairing.py "
                "--output discovery/cycle-208-b045-polarized-minor-pairing-prototype-v1.json"
            ),
            "test_command": "python3 -m unittest tests/test_cycle_208_polarized_minor_pairing.py",
            "write_command": "python3 proof/build_cycle_208_polarized_minor_pairing_v1.py --write",
            "check_command": "python3 proof/build_cycle_208_polarized_minor_pairing_v1.py --check",
        },
        "runtime": runtime,
        "sealer": {
            "path": "proof/build_cycle_208_polarized_minor_pairing_v1.py",
            "sha256": sha256(Path(__file__)),
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
