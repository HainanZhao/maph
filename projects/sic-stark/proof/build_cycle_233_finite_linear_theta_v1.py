#!/usr/bin/env python3
"""Seal the Cycle 233/B070 finite linear-theta obstruction."""
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_233_finite_linear_theta import audit

R = Path(__file__).resolve().parents[1]
O = R / "artifacts/cycle-233-b070-finite-linear-theta-v1.json"
I = {
    "prior": (R / "artifacts/cycle-232-b069-multiplicative-theta-v1.json", "18ca8e8f87cc14708c17c596754cb2341366369300c57e336d665d54f01e27a9"),
    "prereg": (R / "docs/cycle-233-b070-finite-linear-theta-preregistration-v1.md", "c520e58beeacb222fe1141060be1dd15b071f22982d3fb4086a17ceba35affa0"),
    "replay": (R / "proof/verify_cycle_233_finite_linear_theta.py", "66d16070c6ef1c008c6bb6d7be4014b661705675c6900f40ee3fd9b2e1863b05"),
    "test": (R / "tests/test_cycle_233_finite_linear_theta.py", "3f28ff9cc9bdcc002e75c9b209b6f71bac3477bddeea115cf7b7a19ca43f7226"),
    "prototype": (R / "discovery/cycle-233-b070-finite-linear-theta-prototype-v1.json", "f3a25f879dd6b7512c5e3b3d28da414ce112f46704cbc2e18f6fc1bbee2f9d75"),
    "validator": (R / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
    "scaffold": (R / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    result = audit()
    require(result["completion"]["finite_linear_theta_completion_exists"] is False, "unearned finite completion")
    return {
        "artifact_id": "cycle-233-b070-finite-linear-theta-v1", "cycle": 233, "budget_ordinal": "B070",
        "epistemic_status": "PROVED", "status": "SEALED_FINITE_LINEAR_THETA_DIVISOR_OBSTRUCTION",
        "claim_boundary": "No finite q=1/576 theta product with linear period-dependent arguments absorbs the A residual. Nonlinear, multivariable, infinite, or other cochains and all AFK, fusion, Stark, and TCC claims remain open.",
        "finite_theta_audit": result,
        "companion_decision": {"identity": "/root/decision_companion_2", "evidence_scope_review": "The full A pole family, all four zero-lattice exclusions, projective-direction proof, and arbitrary-finite-family scope were reviewed.", "recommendation": "Seal C233 and open scale-iterated cochain testing.", "known_flaw": "Nonlinear, multivariable, or canonically regularized infinite theta products remain.", "falsifier": "Any residual pole family, all-factor zero-lattice solution, noncancellation, projective-direction distinctness, finite-theta direction bound, or replay discrepancy.", "next_action": "Normalize a scale-iterated residual cochain and test convergence, full divisor, reflection, and normalization.", "adopted": True},
        "frozen_hashes": freeze_inputs(R, I), "runtime": check_runtime("C233"),
        "sealer": {"path": "proof/build_cycle_233_finite_linear_theta_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=O, payload_factory=payload))
