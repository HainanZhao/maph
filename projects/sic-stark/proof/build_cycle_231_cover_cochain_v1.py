#!/usr/bin/env python3
"""Seal the Cycle 231/B068 universal-cover quadratic-ansatz obstruction."""
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_231_cover_cochain import audit


R = Path(__file__).resolve().parents[1]
O = R / "artifacts/cycle-231-b068-cover-cochain-v1.json"
I = {
    "prior": (R / "artifacts/cycle-230-b067-f3-square-divisor-coboundary-v1.json", "401b4842b018d0eecd3daaee28275fd3dd1398bc2f5cf3af3afd458f8e93cee0"),
    "prereg": (R / "docs/cycle-231-b068-cover-cochain-preregistration-v1.md", "e1bb370a27cc4bf1b3108016cc55f688f45c89782379353218cbfb27d73b6215"),
    "replay": (R / "proof/verify_cycle_231_cover_cochain.py", "81b903e273adcdcf54609f219759d41f3472c03551791815ceb57b2e649a4600"),
    "test": (R / "tests/test_cycle_231_cover_cochain.py", "c5225431cd93da3a6cf9145c608d5ebf3f57a923707b615eb584e7fbb2cedf33"),
    "prototype": (R / "discovery/cycle-231-b068-cover-cochain-prototype-v1.json", "4d96f4c88087e3c79f32f2eb8e617fa827788fe14844cca8ed26105ab33182c7"),
    "validator": (R / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
    "scaffold": (R / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    result = audit()
    require(result["descent"]["descends_single_valuedly"] is False, "unexpected descent")
    require(result["coefficient_comparison"]["exact_deck_w_coefficient_in_units_pi_i_over_log_576"] == "-8", "deck coefficient")
    return {
        "artifact_id": "cycle-231-b068-cover-cochain-v1",
        "cycle": 231,
        "budget_ordinal": "B068",
        "epistemic_status": "PROVED",
        "status": "SEALED_QUADRATIC_COVER_COCHAIN_DESCENT_OBSTRUCTION",
        "claim_boundary": "The formal principal-part scaling equation has no single-valued solution in the frozen quadratic-exponential cover ansatz. This does not exclude periodic-corrected, nonquadratic, essential, enlarged-action, full residual-gamma, AFK, fusion, Stark, or TCC constructions.",
        "cover_cochain_audit": result,
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "evidence_scope_review": "The forced A*log(576)=-2 coefficient, every integer constant branch, and the nonzero deck w coefficient were reviewed; the formal principal-part scope is appropriate.",
            "recommendation": "Seal C231 as the completed quadratic-exponential ansatz obstruction and open a new periodic-correction engine.",
            "known_flaw": "A log(576)-periodic correction, including multiplicative theta functions, is not covered.",
            "falsifier": "Any scaling-coefficient comparison, integer constant branch, deck-action formula, nonzero w coefficient, ansatz completeness claim, or replay discrepancy.",
            "next_action": "Open a forced multiplicative-theta engine with q=1/576; test its quasi-periodicity, full four-gamma residual quotient, reflection, and source normalization.",
            "adopted": True,
        },
        "frozen_hashes": freeze_inputs(R, I),
        "runtime": check_runtime("C231"),
        "sealer": {"path": "proof/build_cycle_231_cover_cochain_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=O, payload_factory=payload))
