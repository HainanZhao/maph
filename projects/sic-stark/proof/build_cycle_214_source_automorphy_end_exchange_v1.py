#!/usr/bin/env python3
"""Seal Cycle 214/B051's source-automorphy end-exchange domain audit."""
from __future__ import annotations

from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_214_source_automorphy_end_exchange import run as automorphy_run


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-214-b051-source-automorphy-end-exchange-v1.json"
INPUTS = {
    "prior_stabilizer_covariance": (ROOT / "artifacts/cycle-188-stabilizer-covariance-v1.json", "5129382929e50457355c727d13d1f5ccded7f47774895b4893931d7eaead1973"),
    "prior_two_cusp_sections": (ROOT / "artifacts/cycle-211-b048-cusp-asymptotic-flat-sections-v1.json", "62b4afdbdf4ad2f9aa11e648929c54aa66219088689231373c7ad16635f8936c"),
    "prior_formal_pairing_obstruction": (ROOT / "artifacts/cycle-213-b050-two-ended-completion-v1.json", "4ee1cbeea41b05f9ea402d57e25a85765a8d2cb4f1690a9c5c4273a980c3743b"),
    "preregistration": (ROOT / "docs/cycle-214-b051-source-automorphy-end-exchange-preregistration-v1.md", "39298ea28f96b51391736d840341c5848af55c447d1f0fd57c342fa991918cd0"),
    "replay": (ROOT / "proof/verify_cycle_214_source_automorphy_end_exchange.py", "a22c53d5e7939687105ac0b5d4a4149a247a7b2769a77d69c888816f9edf2023"),
    "regression_test": (ROOT / "tests/test_cycle_214_source_automorphy_end_exchange.py", "93931461af7ec46a47d706031c604923cd5d0ad30c7662b8106c3a25e2a20493"),
    "prototype": (ROOT / "discovery/cycle-214-b051-source-automorphy-end-exchange-prototype-v1.json", "37a84dd90937a5849af69dda2975cc197cbe254ff4ef0e01fdf25223b731c83f"),
    "cycle188_replay": (ROOT / "proof/verify_cycle_188_stabilizer_covariance.py", "8132f5a4654115d438951d1cbf852ab659dc381bf93374f4db4ef80d227e49b2"),
    "cycle211_replay": (ROOT / "proof/verify_cycle_211_cusp_asymptotic_flat_sections.py", "0cef852e1ebf2db3b2fec48e4bc197ca79e3be9bbd14cd09a09ca73ab99d589d"),
    "multiplier_ledger": (ROOT / "scripts/dimension_six_stabilizer_ledger.py", "594a0d541478f340abe789234335f3ff1b2d874ad8fa3507ad95026c5cc6276b"),
    "preregistration_validator": (ROOT / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 214 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = automorphy_run()
    candidates = result["candidate_audit"]
    flow = result["flow_conjugacy_audit"]
    domain = result["source_domain_audit"]
    require(candidates["E_is_unique_frozen_candidate_exchanging_both_cusp_labels"], "candidate-census drift")
    require(flow["E_A6_E_inverse"] == flow["A6_inverse"], "A6 reversal drift")
    require(domain["E_covariance"]["same_beta_oriented_packet_identification"] == "NOT_SUPPLIED_BY_DECLARED_THEOREMS", "source-domain scope drift")
    return {
        "artifact_id": "cycle-214-b051-source-automorphy-end-exchange-v1",
        "cycle": 214,
        "budget_ordinal": "B051",
        "epistemic_status": "PROVED",
        "status": "SEALED_SOURCE_AUTOMORPHY_TRANSFORMED_TUPLE_END_EXCHANGE_CANDIDATE_ONLY",
        "claim_boundary": result["claim_boundary"],
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": "Among the frozen source candidates, E=J0*S uniquely exchanges the two cusp labels, preserves Q, and reverses A6. The cited AFK covariance is transformed-tuple covariance and supplies no action on the beta-oriented asymptotic packet or scalar dual pairing."
        },
        "candidate_audit": candidates,
        "flow_conjugacy_audit": flow,
        "source_domain_audit": domain,
        "gate_outcome": result["gate_outcome"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "evidence_scope_review": "C214 establishes the frozen candidate census and the exact source-domain role of E=J0*S; it identifies the unique available arithmetic reverser but not an action on the packet.",
            "recommendation": "Seal C214/B051 as PROVED only for the frozen candidate census and the exact source-domain role of E=J0S; it identifies the unique available arithmetic reverser but not an action on the packet.",
            "known_flaw": "The census covers only three declared GL2 candidates, and AFK transformed-tuple/conjugation covariance does not transport P(t), s, Lambda, or the beta-oriented equation-(66) carrier.",
            "falsifier": "Any candidate-completeness, label/sign, determinant, Q-preservation, beta-to-beta^-1, E*A6*E=A6^-1, AFK-hypothesis, or source-scope discrepancy invalidates the seal.",
            "next_action": "Open a new cycle deriving E directly on the equation-(66) Gamma_M parameters and phases; test whether it forces t->t^-1 and a conjugate-dual packet isomorphism exchanging e05 and e50, with an explicit scalar cocycle.",
            "adopted": True,
            "reason": "The available source theorem identifies an exact transformed-tuple reverser but does not bridge it to the analytic packet or its two asymptotic ends."
        },
        "preregistration_preflight": {
            "cycle": 214,
            "manifest_sha256": sha256(ROOT / "docs/cycle-214-b051-source-automorphy-end-exchange-preregistration-v1.md"),
            "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"}
        },
        "frozen_hashes": frozen,
        "replay": {
            "preflight_command": "research prereg check docs/cycle-214-b051-source-automorphy-end-exchange-preregistration-v1.md --expected-cycle 214 --allow-head-drift",
            "prototype_command": "python3 proof/verify_cycle_214_source_automorphy_end_exchange.py --output discovery/cycle-214-b051-source-automorphy-end-exchange-prototype-v1.json",
            "test_command": "python3 -m unittest tests/test_cycle_214_source_automorphy_end_exchange.py",
            "write_command": "python3 proof/build_cycle_214_source_automorphy_end_exchange_v1.py --write",
            "check_command": "python3 proof/build_cycle_214_source_automorphy_end_exchange_v1.py --check"
        },
        "runtime": runtime,
        "sealer": {"path": "proof/build_cycle_214_source_automorphy_end_exchange_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
