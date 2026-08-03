"""Seal C253/B090 direct hyperbolic-gamma continuation result."""
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_253_direct_hyperbolic_continuation import audit


R = Path(__file__).resolve().parents[1]
O = R / "artifacts/cycle-253-b090-direct-hyperbolic-continuation-v1.json"
I = {
    "prior_c249": (R / "artifacts/cycle-249-b086-common-jet-chamber-v1.json", "fc0bca22598fa6519657a607bc93b24ba5948dd0657f3f4c726b8aafafacb35a"),
    "prior_c249_replay": (R / "proof/verify_cycle_249_common_jet_chamber.py", "a2d154cc8efed0db3db97d2ca7e0237ed1716ecf1cfadec57098bf3455f3b507"),
    "prior_c250": (R / "artifacts/cycle-250-b087-graded-f3-jet-representation-v1.json", "f22c8b305a6e49066c8f77ab305bf3e29b621ddfca75fcca086683c61947b9b7"),
    "prior_c250_replay": (R / "proof/verify_cycle_250_graded_f3_jet_representation.py", "0229ae1aa9948559c03478f74e1a6d405487c6f37bb842dbf18ce245989b6bc7"),
    "prior_c251": (R / "artifacts/cycle-251-b088-residue-dual-cross-sign-v1.json", "d965cc663bf3bb5ba09b904419d16b2dfe8df5df7335d5c0b734087fee37971d"),
    "prior_c251_replay": (R / "proof/verify_cycle_251_residue_dual_cross_sign.py", "3ed67005d33c68ee97f1a4e03e2e5d66578f8c31c4125e4f4b8d7de6456a33ae"),
    "prior_c252": (R / "artifacts/cycle-252-b089-reciprocal-negative-alpha-v1.json", "8af8806e58bf9ee283acb5fb046a18df20637265fdb298acc514fbf0d12c8f1e"),
    "prior_c252_replay": (R / "proof/verify_cycle_252_reciprocal_negative_alpha.py", "82852c699c2a37edb7ad97e133ffe63e807cb029f365de6b5a881e23de9ff0ab"),
    "source_paper": (R / "paper/sic-stark-dimension-six-boundary-fusion.tex", "347228e05a87946ca41bb31c118aae069b7fb6002fff4933d030a153cef21cb7"),
    "prereg": (R / "docs/cycle-253-b090-direct-hyperbolic-continuation-preregistration-v1.md", "83d272ee70455c12a71bc7a3baac6858159be61113f502d0d889218a72f85274"),
    "replay": (R / "proof/verify_cycle_253_direct_hyperbolic_continuation.py", "04990c39feeb8f269f59a6dd857667a163491055614fa359f089da705a9307bf"),
    "test": (R / "tests/test_cycle_253_direct_hyperbolic_continuation.py", "595363425747cb2c7c3deaa2e8cd9d3b942abeea4caa5fd9681684c070cbfe65"),
    "validator": (R / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
    "scaffold": (R / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload():
    result = audit()
    target = result["target_test"]
    require(result["epistemic_status"] == "PROVED", "unproved C253 result")
    require(result["status"] == "DIRECT_CONTINUATION_EXISTS_BUT_UNCORRECTED_TARGET_MAP_FALSIFIED", "unexpected C253 status")
    require(result["theorem_audit"]["path"]["path_independent"], "continuation not established")
    require(target["all_eight_target_maps_fail_by_nonconstant_shift_quotient"], "target mismatch not established")
    require(not target["degree_0_to_3_jets_compared"], "selection-rule breach")
    return {
        "artifact_id": "cycle-253-b090-direct-hyperbolic-continuation-v1",
        "cycle": 253,
        "budget_ordinal": "B090",
        "epistemic_status": "PROVED",
        "status": "SEALED_DIRECT_CONTINUATION_EXISTS_UNCORRECTED_TARGET_MAP_FALSIFIED",
        "claim_boundary": result["claim_boundary"],
        "audit": result,
        "decision": {
            "basis": "Stokman's theorem uniquely continues every factor on the slit domain, but every continued beta-shift quotient is 1-X^-1 while its target quotient is 1-X.",
            "known_flaw": "A separately sourced nonconstant transition operator or full rarefied Gamma_M theorem could alter the target comparison.",
            "falsifier": "A failed Stokman hypothesis, normalization error, slit-domain obstruction, a constant equality of the two shift quotients, factor transcription error, or replay discrepancy.",
            "next_action": "C254/B091 independently replays the strongest continuation and target obstruction, audits whether any already sourced transition operator survives prior records, then closes TCC or freezes with the minimal handoff.",
        },
        "source_scope": {
            "stokman": "Hyperbolic beta integrals, Adv. Math. 190 (2005), Appendix, Proposition 6.1 and continuation after equation (6.8)",
            "sarkissian_spiridonov": "arXiv:1910.11747v4, equation (13)",
        },
        "frozen_hashes": freeze_inputs(R, I),
        "runtime": check_runtime("C253"),
        "sealer": {"path": "proof/build_cycle_253_direct_hyperbolic_continuation_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=O, payload_factory=payload))
