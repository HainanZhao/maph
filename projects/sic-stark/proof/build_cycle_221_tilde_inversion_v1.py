#!/usr/bin/env python3
"""Seal Cycle 221/B058's forced tilde-inversion correction containment."""
from __future__ import annotations

from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_221_tilde_inversion import run as inversion_run


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-221-b058-tilde-inversion-v1.json"
INPUTS = {
    "prior_reflection_containment": (
        ROOT / "artifacts/cycle-220-b057-normalized-reflection-v1.json",
        "91340e0b369d0236ea3ffe99e14871b22545152dfa93a473511c0037344a7cc2",
    ),
    "preregistration": (
        ROOT / "docs/cycle-221-b058-tilde-inversion-preregistration-v1.md",
        "b571e041efc3e410be46a55b5f366305c0f1ed4c39469012920b2fa23817a208",
    ),
    "replay": (
        ROOT / "proof/verify_cycle_221_tilde_inversion.py",
        "a8db4b32f28b6e43246c11764f08fb60206a866c10e4f7e48a8b4f1783f93bd3",
    ),
    "regression_test": (
        ROOT / "tests/test_cycle_221_tilde_inversion.py",
        "26cbd53bcd3bcb37ab65ec7e00a9aecc2587454ca47df1ec83ef0da4330bdbc7",
    ),
    "prototype": (
        ROOT / "discovery/cycle-221-b058-tilde-inversion-prototype-v1.json",
        "02718677f90a650b5e5aef420f7f7017bd75015e2dbaec9444205dfcbfe64254",
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
    result = inversion_run()
    survivors = result["survivor_coordinate_audit"]
    correction = result["forced_pochhammer_audit"]
    shift = result["first_shift_normalization_audit"]
    downstream = result["downstream_identity_audit"]
    require(survivors["survivor_count"] == 2, "survivor count drift")
    require(
        correction["inversion_identity"] == "C(z;qtilde)*C(z^(-1);qtilde)=1",
        "Pochhammer inversion drift",
    )
    require(not shift["all_match"], "unexpected normalized first-shift match")
    require(all(not row["matches"] for row in shift["rows"]), "one survivor escaped mismatch")
    require(downstream["unnormalized_product_sector_match"], "forced product repair drift")
    return {
        "artifact_id": "cycle-221-b058-tilde-inversion-v1",
        "cycle": 221,
        "budget_ordinal": "B058",
        "epistemic_status": "PROVED",
        "status": "SEALED_FORCED_TILDE_CORRECTION_NORMALIZATION_MISMATCH",
        "claim_boundary": result["claim_boundary"],
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": "The uniquely forced tilde-sector Pochhammer ratio repairs the frozen unnormalized sector but leaves an exact first normalized-shift sign mismatch for both survivors, so it is not an accepted signed-k extension under the frozen direct continuation requirement.",
        },
        "survivor_coordinate_audit": survivors,
        "forced_pochhammer_audit": correction,
        "first_shift_normalization_audit": shift,
        "downstream_identity_audit": downstream,
        "gate_outcome": result["gate_outcome"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "evidence_scope_review": "The two survivors, forced Pochhammer ratio, exact inversion, first-shift invariance, phase exponents 1311/1450, and both-survivor sign mismatch were reviewed as one frozen construction.",
            "recommendation": "Seal C221/B058 as PROVED only for failure of the uniquely forced tilde-Pochhammer correction on the two frozen tau/u survivors.",
            "known_flaw": "The residual sign mismatch may be a label-cocycle effect; the result excludes neither a source-derived normalization multiplier nor a genuinely new signed product.",
            "falsifier": "Any survivor-coordinate, Pochhammer inversion/uniqueness, involutivity, first-shift invariance, phase-1311/1450, sine-factor, both-survivor, or replay discrepancy invalidates the seal.",
            "next_action": "Open a label-cocycle cycle: derive allowed root-of-unity multipliers from source normalization Z(m), solve exact Z/24 shift/reflection coboundary equations, and test both factorization identities before adjoining any multiplier.",
            "adopted": True,
            "reason": "The sole unmodified correction fails exactly, but a source-derived label cocycle remains a different construction.",
        },
        "preregistration_preflight": {
            "cycle": 221,
            "manifest_sha256": sha256(ROOT / "docs/cycle-221-b058-tilde-inversion-preregistration-v1.md"),
            "validator": {
                "path": "../../tools/preregistration_check.py",
                "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
            },
        },
        "frozen_hashes": frozen,
        "replay": {
            "preflight_command": "research prereg check docs/cycle-221-b058-tilde-inversion-preregistration-v1.md --expected-cycle 221 --allow-head-drift",
            "prototype_command": "python3 proof/verify_cycle_221_tilde_inversion.py --output discovery/cycle-221-b058-tilde-inversion-prototype-v1.json",
            "test_command": "python3 -m unittest tests/test_cycle_221_tilde_inversion.py",
            "write_command": "python3 proof/build_cycle_221_tilde_inversion_v1.py --write",
            "check_command": "python3 proof/build_cycle_221_tilde_inversion_v1.py --check",
        },
        "runtime": check_runtime("Cycle 221 seal"),
        "sealer": {"path": "proof/build_cycle_221_tilde_inversion_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
