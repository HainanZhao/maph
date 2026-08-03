#!/usr/bin/env python3
"""Seal the Cycle 232/B069 single-theta containment."""
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_232_multiplicative_theta import audit


R = Path(__file__).resolve().parents[1]
O = R / "artifacts/cycle-232-b069-multiplicative-theta-v1.json"
I = {
    "prior": (R / "artifacts/cycle-231-b068-cover-cochain-v1.json", "2e02d642d13345bdfa64e232dd56b3b2def155c01702cbc0f9cf5e16e2db39e1"),
    "prereg": (R / "docs/cycle-232-b069-multiplicative-theta-preregistration-v1.md", "a75a813ab181dfa811aafa73041a228a3fe8344b8c285471f57d62311874b868"),
    "replay": (R / "proof/verify_cycle_232_multiplicative_theta.py", "7f105e016cee870b5bb9fba410f9e1536f0f42283abe3d3eb478a2db9386a280"),
    "test": (R / "tests/test_cycle_232_multiplicative_theta.py", "1a7c424c00fbc0311096ee2c124893b7813750163ad85958fc733fdfe1a0f054"),
    "prototype": (R / "discovery/cycle-232-b069-multiplicative-theta-prototype-v1.json", "4172c225f61c07f880b7221b0a415cb8ee0c9623c38d8ec300bec9f4f28551c1"),
    "validator": (R / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
    "scaffold": (R / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    result = audit()
    require(result["principal_multiplier"]["tier_1"] == "PROVED", "missing theta construction")
    require(result["tier_2"]["absorbs_both_full_residuals"] is False, "unearned full absorption")
    return {
        "artifact_id": "cycle-232-b069-multiplicative-theta-v1",
        "cycle": 232,
        "budget_ordinal": "B069",
        "epistemic_status": "PROVED",
        "status": "SEALED_SINGLE_THETA_PRINCIPAL_CONSTRUCTION_FULL_RESIDUAL_CONTAINMENT",
        "claim_boundary": "The frozen single-theta candidate solves only the principal mu^(-4) multiplier and cannot absorb either full residual block. This excludes no finite or infinite theta product with period-dependent arguments, nor any other cochain, AFK, fusion, Stark, or TCC construction.",
        "theta_audit": result,
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "evidence_scope_review": "The single-valued theta construction, direct quasi-periodicity, A/C nonzero pole witnesses, and all frozen zero-lattice exclusions were reviewed.",
            "recommendation": "Seal C232 as the completed single-theta containment and open the period-dependent theta-product design cycle.",
            "known_flaw": "Products of shifted/scaled theta factors may contain the residual hyperplane divisor orbits.",
            "falsifier": "Any theta product/quasi-periodicity, H multiplier, residual pole, zero-lattice exclusion, A/C coverage, single-theta scope, or replay discrepancy.",
            "next_action": "Compute full residual divisor classes modulo mu->576*mu, then test the minimal period-dependent theta product from orbit representatives.",
            "adopted": True,
        },
        "frozen_hashes": freeze_inputs(R, I),
        "runtime": check_runtime("C232"),
        "sealer": {"path": "proof/build_cycle_232_multiplicative_theta_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=O, payload_factory=payload))
