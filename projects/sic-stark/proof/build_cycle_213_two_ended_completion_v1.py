#!/usr/bin/env python3
"""Seal Cycle 213/B050's formal two-ended scalar-pairing obstruction."""
from __future__ import annotations

from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_213_two_ended_completion import run as completion_run


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-213-b050-two-ended-completion-v1.json"
INPUTS = {
    "prior_two_cusp_sections": (ROOT / "artifacts/cycle-211-b048-cusp-asymptotic-flat-sections-v1.json", "62b4afdbdf4ad2f9aa11e648929c54aa66219088689231373c7ad16635f8936c"),
    "prior_two_sign_orientation": (ROOT / "artifacts/cycle-212-b049-logarithmic-axis-to-packet-orientation-v1.json", "8af644a7d17e4e9959d1cff95fc2a7a9128f45dfd91ec10b83789c076c7898c5"),
    "preregistration": (ROOT / "docs/cycle-213-b050-two-ended-completion-preregistration-v1.md", "9ce3d02d20c9cf8d7152036921f3759e1120e55f263fb1a3f6442994a2fbc286"),
    "replay": (ROOT / "proof/verify_cycle_213_two_ended_completion.py", "0c2f56ff6195d7cf83f797af8aa6b7613f7dc1113c17194173b7436ca87644d4"),
    "regression_test": (ROOT / "tests/test_cycle_213_two_ended_completion.py", "e796cdf769f06b34f1e53856092fc7a302da253fc4095c2c132b9d7af45becf4"),
    "prototype": (ROOT / "discovery/cycle-213-b050-two-ended-completion-prototype-v1.json", "1a64f096c1112e837dd6bb45ec9a68bba72a810cc680705ccadfb981b9dce4ff"),
    "cycle211_replay": (ROOT / "proof/verify_cycle_211_cusp_asymptotic_flat_sections.py", "0cef852e1ebf2db3b2fec48e4bc197ca79e3be9bbd14cd09a09ca73ab99d589d"),
    "multiplier_ledger": (ROOT / "scripts/dimension_six_stabilizer_ledger.py", "594a0d541478f340abe789234335f3ff1b2d874ad8fa3507ad95026c5cc6276b"),
    "preregistration_validator": (ROOT / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 213 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = completion_run()
    multiplier = result["a6_cusp_multiplier_audit"]
    scalar = result["scalar_pairing_audit"]
    cross = result["cross_pairing_audit"]
    require(multiplier["common_multiplier_exponent_mod_48"] == 8, "cusp multiplier drift")
    require(scalar["zeta_48_squared_exponent_mod_48"] == 16, "squared multiplier drift")
    require(scalar["nonzero_scalar_pairing_dimension"] == 0, "scalar-pairing obstruction drift")
    require(cross["exchange_invariant"], "cross-pairing exchange drift")
    require(not cross["descends_to_iota_coinvariant_quotient"], "cross-pairing quotient drift")
    return {
        "artifact_id": "cycle-213-b050-two-ended-completion-v1",
        "cycle": 213,
        "budget_ordinal": "B050",
        "epistemic_status": "PROVED",
        "status": "SEALED_FORMAL_TWO_ENDED_SCALAR_PAIRING_OBSTRUCTION",
        "claim_boundary": result["claim_boundary"],
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": "In the declared formal two-cusp completion with common A6 multiplier zeta_48^8, every complex-bilinear strictly scalar A6-invariant pairing vanishes. This is a scoped formal obstruction, not an analytic or arithmetic fusion result."
        },
        "a6_cusp_multiplier_audit": multiplier,
        "formal_completion_audit": result["formal_completion_audit"],
        "scalar_pairing_audit": scalar,
        "quarantined_cross_pairing_context": {
            "epistemic_status": "PROVED",
            "audit": cross,
            "promotion_status": "NOT_A_FUSION_INVARIANT_AND_NOT_A_SOURCE_AUTHORIZED_DESCENT",
            "reason": "It needs a constructed multiplier line and constructed exchange; it is retained only to prevent a future scalarization or quotient-descent misreading."
        },
        "gate_outcome": result["gate_outcome"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "evidence_scope_review": "C213 establishes the formal two-ended representation and strictly scalar complex-bilinear invariant-form obstruction. The character-valued/conjugate-line construction is a distinct engine.",
            "recommendation": "Seal C213/B050 as PROVED only for the formal two-ended representation and the strictly scalar complex-bilinear invariant-form obstruction; the character-valued/conjugate-line construction is a distinct engine.",
            "known_flaw": "W, the end exchange, and multiplier line M are not yet derived from an analytic or arithmetic source, and complex-bilinear failure does not exclude sesquilinear or dual-line pairings.",
            "falsifier": "Any cusp multiplier, zeta_48 order, bilinear invariance equation, exchange symmetry, fixed-space restriction, coinvariant-descent, or replay discrepancy invalidates the seal.",
            "next_action": "Open a new cycle deriving the end exchange and multiplier line from source conjugation/theta automorphy, then test a canonical W tensor W-bar or W tensor W-dual scalar pairing before any fusion or C198 claim.",
            "adopted": True,
            "reason": "The frozen multiplier exactly rules out the declared scalar complex-bilinear family, while the remaining dual/conjugate constructions require a genuinely new source-authorized engine."
        },
        "preregistration_preflight": {
            "cycle": 213,
            "manifest_sha256": sha256(ROOT / "docs/cycle-213-b050-two-ended-completion-preregistration-v1.md"),
            "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"}
        },
        "frozen_hashes": frozen,
        "replay": {
            "preflight_command": "research prereg check docs/cycle-213-b050-two-ended-completion-preregistration-v1.md --expected-cycle 213 --allow-head-drift",
            "prototype_command": "python3 proof/verify_cycle_213_two_ended_completion.py --output discovery/cycle-213-b050-two-ended-completion-prototype-v1.json",
            "test_command": "python3 -m unittest tests/test_cycle_213_two_ended_completion.py",
            "write_command": "python3 proof/build_cycle_213_two_ended_completion_v1.py --write",
            "check_command": "python3 proof/build_cycle_213_two_ended_completion_v1.py --check"
        },
        "runtime": runtime,
        "sealer": {"path": "proof/build_cycle_213_two_ended_completion_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
