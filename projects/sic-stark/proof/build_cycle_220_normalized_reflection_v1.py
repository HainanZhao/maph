#!/usr/bin/env python3
"""Seal Cycle 220/B057's normalized-reflection reduction containment."""
from __future__ import annotations

from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_220_normalized_reflection import run as reflection_run


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-220-b057-normalized-reflection-v1.json"
INPUTS = {
    "prior_diagonal_extension": (
        ROOT / "artifacts/cycle-219-b056-signed-k-extension-v1.json",
        "d305dc5e7ad3fc904b51ba4ce208938b7c0c675d8b865397d862420c54744291",
    ),
    "preregistration": (
        ROOT / "docs/cycle-220-b057-normalized-reflection-preregistration-v1.md",
        "9a7c3fdd865816ec7c37c6eabc345ebb511aba4b42432be31addd9d10ec2e2e9",
    ),
    "replay": (
        ROOT / "proof/verify_cycle_220_normalized_reflection.py",
        "ee18f4ef9d27c8c78b4c1e82982818eb21f5697efd0c5f3eb69d1bd1354b4f93",
    ),
    "regression_test": (
        ROOT / "tests/test_cycle_220_normalized_reflection.py",
        "20a6899d146f868e9ff752900f76238c1baf08364f82e8839f3c8ab176664c8b",
    ),
    "prototype": (
        ROOT / "discovery/cycle-220-b057-normalized-reflection-prototype-v1.json",
        "f96886957437d88914d8d2025a467801e23cf589faae81f678e99bebe2dcb91a",
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
    result = reflection_run()
    reduction = result["reflection_reduction_audit"]
    census = result["reflected_coordinate_census"]
    axioms = result["downstream_axiom_audit"]
    require(
        reduction["candidate_after_reduction"]
        == "H_abcd=Gamma_M(a*mu,b*m;c*omega1,d*omega2)",
        "reflection reduction drift",
    )
    require(census["candidate_count"] == 16, "reflected candidate census drift")
    require(census["survivor_count"] == 0, "unexpected reflected survivor")
    require(axioms["reflection_tested"], "reflection audit omitted")
    require(not axioms["involutivity_tested"], "unearned downstream test")
    return {
        "artifact_id": "cycle-220-b057-normalized-reflection-v1",
        "cycle": 220,
        "budget_ordinal": "B057",
        "epistemic_status": "PROVED",
        "status": "SEALED_NORMALIZED_REFLECTION_SIGN_FAMILY_FALSIFIED",
        "claim_boundary": result["claim_boundary"],
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": "The source normalized reflection reduces each frozen reflection-plus-sign candidate to a Cycle-219 diagonal sign lift, so its 16-member family has no raw product-coordinate survivor.",
        },
        "reflection_reduction_audit": reduction,
        "reflected_coordinate_census": census,
        "downstream_axiom_audit": axioms,
        "gate_outcome": result["gate_outcome"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "evidence_scope_review": "The source normalized reflection and its Q/label substitution reduce all 16 frozen reflection-plus-sign candidates exactly to C219's exhaustive diagonal census.",
            "recommendation": "Seal C220/B057 as PROVED only for failure of the 16 normalized-reflection-plus-sign candidates; reflection adds no new product-coordinate lift beyond C219.",
            "known_flaw": "The argument stays inside the positive-k meromorphic reflection law and neither defines nor excludes a signed product with an explicit theta/Pochhammer correction.",
            "falsifier": "Any normalized-reflection convention, Q/label substitution, reduction to the C219 diagonal candidates, corrected coefficient census, or replay discrepancy invalidates the seal.",
            "next_action": "Open a new cycle from the two tau/u survivors, for which the sole remaining product-coordinate defect is tilde-u -> -tilde-u; derive the forced tilde-sector Pochhammer/theta inversion factor and test involutivity, normalization, shifts, and factorization without fitted terms.",
            "adopted": True,
            "reason": "The reflection construction is exactly contained in the preceding diagonal family, while a correction factor would be a distinct new construction.",
        },
        "preregistration_preflight": {
            "cycle": 220,
            "manifest_sha256": sha256(ROOT / "docs/cycle-220-b057-normalized-reflection-preregistration-v1.md"),
            "validator": {
                "path": "../../tools/preregistration_check.py",
                "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
            },
        },
        "frozen_hashes": frozen,
        "replay": {
            "preflight_command": "research prereg check docs/cycle-220-b057-normalized-reflection-preregistration-v1.md --expected-cycle 220 --allow-head-drift",
            "prototype_command": "python3 proof/verify_cycle_220_normalized_reflection.py --output discovery/cycle-220-b057-normalized-reflection-prototype-v1.json",
            "test_command": "python3 -m unittest tests/test_cycle_220_normalized_reflection.py",
            "write_command": "python3 proof/build_cycle_220_normalized_reflection_v1.py --write",
            "check_command": "python3 proof/build_cycle_220_normalized_reflection_v1.py --check",
        },
        "runtime": check_runtime("Cycle 220 seal"),
        "sealer": {"path": "proof/build_cycle_220_normalized_reflection_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
