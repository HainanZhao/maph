#!/usr/bin/env python3
"""Seal Cycle 222/B059's source-normalization cocycle boundary."""
from __future__ import annotations

from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_222_z_label_cocycle import run as cocycle_run


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-222-b059-z-label-cocycle-v1.json"
INPUTS = {
    "prior_tilde_containment": (
        ROOT / "artifacts/cycle-221-b058-tilde-inversion-v1.json",
        "e81eeaf8df6bf860989682eb6c15f6d0d91598d391031dccec0b72fc739afeb9",
    ),
    "preregistration": (
        ROOT / "docs/cycle-222-b059-z-label-cocycle-preregistration-v1.md",
        "2146b3a72e691e0a142db58fbc84974709d3997ea575d9c0d5b53d5bf0296a25",
    ),
    "replay": (
        ROOT / "proof/verify_cycle_222_z_label_cocycle.py",
        "a9400fb73f1c4dc456727735a6498c300f1762992625e61b4075dae20caf0d52",
    ),
    "regression_test": (
        ROOT / "tests/test_cycle_222_z_label_cocycle.py",
        "16f41971d1abd244538b421911fb49cb19ff8e4574140d9ed093f6783f2321a8",
    ),
    "prototype": (
        ROOT / "discovery/cycle-222-b059-z-label-cocycle-prototype-v1.json",
        "b83a4bc17c82c32bea588dadddba0eb3df56c1e8b9c80329a4355e967662d3e1",
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
    result = cocycle_run()
    coboundary = result["first_shift_coboundary_audit"]
    reflection = result["formal_reflection_constraint_audit"]
    z_phase = result["source_z_phase_audit"]
    bridge = result["source_bridge_audit"]
    require(coboundary["orbit_size"] == 24, "cocycle orbit drift")
    require(reflection["compatibility"], "formal reflection compatibility drift")
    require(not z_phase["cross_sign_relation_supplied"], "unexpected source sign bridge")
    require(not bridge["source_defined_Z_minus"], "unexpected source Z-minus")
    require(not bridge["factorization_lambda_pullback_available"], "unexpected factorization pullback")
    return {
        "artifact_id": "cycle-222-b059-z-label-cocycle-v1",
        "cycle": 222,
        "budget_ordinal": "B059",
        "epistemic_status": "PROVED",
        "status": "SEALED_Z24_COCYCLE_TORSOR_SOURCE_NONSELECTION",
        "claim_boundary": result["claim_boundary"],
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": "The residual shift sign admits a unique-up-to-constant parity cocycle on Z/24 and is formally reflection-compatible, but the source supplies no cross-sign law, Z-minus, or factorization pullback selecting it as a signed-k normalization.",
        },
        "first_shift_coboundary_audit": coboundary,
        "formal_reflection_constraint_audit": reflection,
        "source_z_phase_audit": z_phase,
        "source_bridge_audit": bridge,
        "gate_outcome": result["gate_outcome"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "evidence_scope_review": "The complete Z/24 orbit, shift equation, torsor uniqueness, reflection parity, positive-k Z phase, and source-domain/factorization boundary were reviewed together.",
            "recommendation": "Seal C222/B059 as PROVED only for the Z/24 parity-cocycle torsor, reflection compatibility, and absence of a source-provided cross-sign normalization law; then open the explicit construction as a new cycle.",
            "known_flaw": "The match with positive-k xi(m)=(-1)^(m+1) is structural resemblance, not evidence that parity supplies the missing signed Gamma_M normalization or factorization pullback.",
            "falsifier": "Any orbit, shift equation, torsor uniqueness, parity/reflection, positive-k Z-phase, source-domain, or replay discrepancy invalidates the seal.",
            "next_action": "Define a candidate negative-k product using the two-survivor lift, forced tilde-Pochhammer factor, and lambda(m)=lambda0(-1)^m; freeze lambda0 via involutivity/reflection, then test both shifts and equations (16)--(17) exactly before any E or packet claim.",
            "adopted": True,
            "reason": "Finite phase algebra alone does not bridge the source domains; the explicit signed-product construction is a distinct, falsifiable engine.",
        },
        "preregistration_preflight": {
            "cycle": 222,
            "manifest_sha256": sha256(ROOT / "docs/cycle-222-b059-z-label-cocycle-preregistration-v1.md"),
            "validator": {
                "path": "../../tools/preregistration_check.py",
                "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
            },
        },
        "frozen_hashes": frozen,
        "replay": {
            "preflight_command": "research prereg check docs/cycle-222-b059-z-label-cocycle-preregistration-v1.md --expected-cycle 222 --allow-head-drift",
            "prototype_command": "python3 proof/verify_cycle_222_z_label_cocycle.py --output discovery/cycle-222-b059-z-label-cocycle-prototype-v1.json",
            "test_command": "python3 -m unittest tests/test_cycle_222_z_label_cocycle.py",
            "write_command": "python3 proof/build_cycle_222_z_label_cocycle_v1.py --write",
            "check_command": "python3 proof/build_cycle_222_z_label_cocycle_v1.py --check",
        },
        "runtime": check_runtime("Cycle 222 seal"),
        "sealer": {"path": "proof/build_cycle_222_z_label_cocycle_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
