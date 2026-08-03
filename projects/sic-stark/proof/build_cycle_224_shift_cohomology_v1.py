#!/usr/bin/env python3
"""Seal Cycle 224/B061's frozen joint-shift construction containment."""
from __future__ import annotations

from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_224_shift_cohomology import run as cohomology_run


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-224-b061-shift-cohomology-v1.json"
INPUTS = {
    "prior_explicit_product": (
        ROOT / "artifacts/cycle-223-b060-explicit-signed-product-v1.json",
        "a54c11b4b12530480d449f5a9ae75106d8e1b17f94f2eba4aedfc6fef07db5f1",
    ),
    "preregistration": (
        ROOT / "docs/cycle-224-b061-shift-cohomology-preregistration-v1.md",
        "5eb57b4dea81efdb3f198f34760b2dc5560f09fa09eb75a35036b03031619878",
    ),
    "replay": (
        ROOT / "proof/verify_cycle_224_shift_cohomology.py",
        "14f5ee54d596e2775e9671fbd13fc2053b18af863d28552de8b21da5de2035aa",
    ),
    "regression_test": (
        ROOT / "tests/test_cycle_224_shift_cohomology.py",
        "981f9d260422383e8ceb7adcfc3f71cfe40d34f947255a2aa8699fe83159bbf6",
    ),
    "prototype": (
        ROOT / "discovery/cycle-224-b061-shift-cohomology-prototype-v1.json",
        "9ac751ac5f734748537145d53b26e4a7838625974d697613e4410f1faecdd962",
    ),
    "prior_product_replay": (
        ROOT / "proof/verify_cycle_223_explicit_signed_product.py",
        "817b49c05b84ded6f55650d6717349f8ad2b6ea2fc3588919dd14f2578ecc6bb",
    ),
    "prior_cocycle_replay": (
        ROOT / "proof/verify_cycle_222_z_label_cocycle.py",
        "a9400fb73f1c4dc456727735a6498c300f1762992625e61b4075dae20caf0d52",
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
    result = cohomology_run()
    solution = result["minimal_exponential_solution_audit"]
    commutator = result["commutator_audit"]
    reflection = result["combined_reflection_audit"]
    boundary = result["combined_boundary_audit"]
    require(solution["solution"] == "a=1", "cochain solution drift")
    require(commutator["integrable"], "shift cochain not integrable")
    require(reflection["candidate_count"] == 4, "combined candidate census drift")
    require(not reflection["all_match"], "unexpected frozen reflection closure")
    require(
        {row["combined_reflection_product"] for row in reflection["rows"]} == {-1},
        "reflection residual drift",
    )
    require(boundary["factorization_16_17"] == "not_reached_after_failed_reflection", "unearned factorization")
    return {
        "artifact_id": "cycle-224-b061-shift-cohomology-v1",
        "cycle": 224,
        "budget_ordinal": "B061",
        "epistemic_status": "PROVED",
        "status": "SEALED_FROZEN_SHIFT_COHOMOLOGY_REFLECTION_FAILURE",
        "claim_boundary": result["claim_boundary"],
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": "The unique minimal integrable shift cochain makes every frozen epsilon=+/-1 Pochhammer-times-parity product fail raw reflection by -1.",
        },
        "shift_action_audit": result["shift_action_audit"],
        "minimal_exponential_solution_audit": solution,
        "commutator_audit": commutator,
        "combined_reflection_audit": reflection,
        "combined_boundary_audit": boundary,
        "gate_outcome": result["gate_outcome"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "evidence_scope_review": "The D uniqueness, both shift residuals, commutator cell, raw-reflection action, Pochhammer/Gamma reduction, parity product, and all-four-candidate total sign were reviewed together.",
            "recommendation": "Seal amended C224/B061 as PROVED only for reflection failure of the frozen epsilon=+/-1 Pochhammer-times-parity-times-D construction.",
            "known_flaw": "The residual -1 may be removed by a newly preregistered normalization c with c^2=-1; the current result excludes neither that branch nor a changed signed state.",
            "falsifier": "Any D uniqueness, shift/commutator, raw-reflection action, Pochhammer/Gamma factor, parity product, all-four-candidate, or total-sign discrepancy invalidates the seal.",
            "next_action": "Open a new cycle freezing exactly the two reflection-forced constants c=+/-i derived from c^2=-1, then retest both shifts, reflection, double-sign involutivity—including whether sign reversal conjugates c—and equations (16)--(17) before any packet use.",
            "adopted": True,
            "reason": "The frozen epsilon=+/-1 branch is exhausted; c=+/-i is a distinct reflection-normalized construction.",
        },
        "preregistration_preflight": {
            "cycle": 224,
            "manifest_sha256": sha256(ROOT / "docs/cycle-224-b061-shift-cohomology-preregistration-v1.md"),
            "validator": {
                "path": "../../tools/preregistration_check.py",
                "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
            },
        },
        "frozen_hashes": frozen,
        "replay": {
            "preflight_command": "research prereg check docs/cycle-224-b061-shift-cohomology-preregistration-v1.md --expected-cycle 224 --allow-head-drift",
            "prototype_command": "python3 proof/verify_cycle_224_shift_cohomology.py --output discovery/cycle-224-b061-shift-cohomology-prototype-v1.json",
            "test_command": "python3 -m unittest tests/test_cycle_224_shift_cohomology.py",
            "write_command": "python3 proof/build_cycle_224_shift_cohomology_v1.py --write",
            "check_command": "python3 proof/build_cycle_224_shift_cohomology_v1.py --check",
        },
        "runtime": check_runtime("Cycle 224 seal"),
        "sealer": {"path": "proof/build_cycle_224_shift_cohomology_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
