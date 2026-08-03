#!/usr/bin/env python3
"""Seal Cycle 219/B056's diagonal signed-k extension falsifier."""
from __future__ import annotations

from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_219_signed_k_extension import run as extension_run


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-219-b056-signed-k-extension-v1.json"
INPUTS = {
    "prior_signed_period_cover": (
        ROOT / "artifacts/cycle-218-b055-signed-period-cover-v1.json",
        "7b456c630bbcc40c632c4b8b0a9ffe0aa128a6bbacf51813a7b029bb13da40a6",
    ),
    "preregistration": (
        ROOT / "docs/cycle-219-b056-signed-k-extension-preregistration-v1.md",
        "69a4a95767173a5494e47bf722d74229b0420d317492ba13b410ed93a75d07c7",
    ),
    "replay": (
        ROOT / "proof/verify_cycle_219_signed_k_extension.py",
        "467ef8084bdb6e5dbcafdbf285973b5b1cbccbdff354fd57dd829060d71df532",
    ),
    "regression_test": (
        ROOT / "tests/test_cycle_219_signed_k_extension.py",
        "c28f93e47e3f7bda91e4db04c901b5b7b0e872d5e3ec15aea7b577cc5f9319e9",
    ),
    "prototype": (
        ROOT / "discovery/cycle-219-b056-signed-k-extension-prototype-v1.json",
        "90802e508355eb49b0b619326d6021633b5bc90269a0fcb2c980c5fb3305d75d",
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
    result = extension_run()
    census = result["coordinate_sign_census"]
    axioms = result["extension_axiom_audit"]
    require(census["candidate_count"] == 16, "diagonal census drift")
    require(census["survivor_count"] == 0, "unexpected diagonal survivor")
    require(len(census["tau_and_u_candidates"]) == 2, "tau/u constraint drift")
    require(all(not row["tilde_u"] for row in census["tau_and_u_candidates"]), "tilde-u conflict drift")
    require(not axioms["agreement_with_positive_product"], "unearned product agreement")
    return {
        "artifact_id": "cycle-219-b056-signed-k-extension-v1",
        "cycle": 219,
        "budget_ordinal": "B056",
        "epistemic_status": "PROVED",
        "status": "SEALED_DIAGONAL_SIGNED_K_EXTENSION_FALSIFIED",
        "claim_boundary": result["claim_boundary"],
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": "Every frozen diagonal sign lift fails at least one of tau, u, and tilde-u; therefore none defines a signed-k Gamma_M extension in that family.",
        },
        "coordinate_sign_census": census,
        "extension_axiom_audit": axioms,
        "gate_outcome": result["gate_outcome"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "evidence_scope_review": "The corrected 16-case census is exhaustive for the preregistered diagonal sign family. Its tau/u constraints force both remaining tilde-u coefficients to -1, leaving no product-coordinate survivor.",
            "recommendation": "Seal C219/B056 as PROVED only for nonexistence within the frozen 16 diagonal sign-lift family and open a new cycle.",
            "known_flaw": "The result excludes no non-diagonal construction using normalized reflection, theta/Pochhammer corrections, additive shifts, period swaps, label changes, or a new Gamma_M theorem.",
            "falsifier": "Any corrected tau/u/tilde-u coefficient, 16-candidate completeness, tau/u constraint, zero-survivor census, raw-state convention, or replay discrepancy invalidates the seal.",
            "next_action": "Preregister the smallest source-derived non-diagonal candidate: combine normalized reflection (33) with the required sign reversal, freezing its argument/label map and correction factor, then test product-coordinate agreement, involutivity, shifts, and both factorization identities before any packet comparison.",
            "adopted": True,
            "reason": "The diagonal family has been exhausted exactly, while the named non-diagonal constructions remain distinct, untested designs.",
        },
        "preregistration_preflight": {
            "cycle": 219,
            "manifest_sha256": sha256(ROOT / "docs/cycle-219-b056-signed-k-extension-preregistration-v1.md"),
            "validator": {
                "path": "../../tools/preregistration_check.py",
                "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
            },
        },
        "frozen_hashes": frozen,
        "replay": {
            "preflight_command": "research prereg check docs/cycle-219-b056-signed-k-extension-preregistration-v1.md --expected-cycle 219 --allow-head-drift",
            "prototype_command": "python3 proof/verify_cycle_219_signed_k_extension.py --output discovery/cycle-219-b056-signed-k-extension-prototype-v1.json",
            "test_command": "python3 -m unittest tests/test_cycle_219_signed_k_extension.py",
            "write_command": "python3 proof/build_cycle_219_signed_k_extension_v1.py --write",
            "check_command": "python3 proof/build_cycle_219_signed_k_extension_v1.py --check",
        },
        "runtime": check_runtime("Cycle 219 seal"),
        "sealer": {"path": "proof/build_cycle_219_signed_k_extension_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
