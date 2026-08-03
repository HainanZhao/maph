"""Seal C252/B089 reciprocal-base source-continuation result."""
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_252_reciprocal_negative_alpha import audit


R = Path(__file__).resolve().parents[1]
O = R / "artifacts/cycle-252-b089-reciprocal-negative-alpha-v1.json"
I = {
    "prior_c228": (R / "artifacts/cycle-228-b065-f3-square-residual-block-v1.json", "2078970c02c1f1359de25394f57c9229dab4fef01c15894bc36b1ea177deafe4"),
    "prior_c228_replay": (R / "proof/verify_cycle_228_f3_square_residual_block.py", "3419d8d4f0e81cbfc8c970c3c1de5d16f6c79fa793042291156492796f683987"),
    "prior_c249": (R / "artifacts/cycle-249-b086-common-jet-chamber-v1.json", "fc0bca22598fa6519657a607bc93b24ba5948dd0657f3f4c726b8aafafacb35a"),
    "prior_c249_replay": (R / "proof/verify_cycle_249_common_jet_chamber.py", "a2d154cc8efed0db3db97d2ca7e0237ed1716ecf1cfadec57098bf3455f3b507"),
    "prior_c250": (R / "artifacts/cycle-250-b087-graded-f3-jet-representation-v1.json", "f22c8b305a6e49066c8f77ab305bf3e29b621ddfca75fcca086683c61947b9b7"),
    "prior_c250_replay": (R / "proof/verify_cycle_250_graded_f3_jet_representation.py", "0229ae1aa9948559c03478f74e1a6d405487c6f37bb842dbf18ce245989b6bc7"),
    "prior_c251": (R / "artifacts/cycle-251-b088-residue-dual-cross-sign-v1.json", "d965cc663bf3bb5ba09b904419d16b2dfe8df5df7335d5c0b734087fee37971d"),
    "prior_c251_replay": (R / "proof/verify_cycle_251_residue_dual_cross_sign.py", "3ed67005d33c68ee97f1a4e03e2e5d66578f8c31c4125e4f4b8d7de6456a33ae"),
    "source_paper": (R / "paper/sic-stark-dimension-six-boundary-fusion.tex", "347228e05a87946ca41bb31c118aae069b7fb6002fff4933d030a153cef21cb7"),
    "prereg": (R / "docs/cycle-252-b089-reciprocal-negative-alpha-preregistration-v1.md", "0f66c6a17ac5e14a82b15d88ea8bfc5cd71b317b20d35a6486b077634b6fd871"),
    "replay": (R / "proof/verify_cycle_252_reciprocal_negative_alpha.py", "82852c699c2a37edb7ad97e133ffe63e807cb029f365de6b5a881e23de9ff0ab"),
    "test": (R / "tests/test_cycle_252_reciprocal_negative_alpha.py", "899753d59bdf426adfc75ffc71fe3cc23ca1a1e6029a60aa3067ea87639c6739"),
    "validator": (R / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
    "scaffold": (R / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload():
    result = audit()
    continuation = result["continuation_scope_audit"]
    require(result["epistemic_status"] == "PROVED", "unproved C252 scope result")
    require(result["status"] == "RECIPROCAL_BASE_RULE_FAILS_SOURCE_CONTINUATION_GATE", "unexpected C252 status")
    require(continuation["first_failed_prerequisite"] == 4, "selection-rule mismatch")
    require(not continuation["jets_compared"], "post-failure jet comparison")
    return {
        "artifact_id": "cycle-252-b089-reciprocal-negative-alpha-v1",
        "cycle": 252,
        "budget_ordinal": "B089",
        "epistemic_status": "PROVED",
        "status": "SEALED_RECIPROCAL_BASE_RULE_FAILS_SOURCE_CONTINUATION_GATE",
        "claim_boundary": result["claim_boundary"],
        "audit": result,
        "decision": {
            "basis": "The candidate passes its formal shifts and sign involution, but is only a disjoint-chamber definition and supplies no analytic bridge across the product boundary.",
            "known_flaw": "A direct integral representation or a separately proved modular-cancellation theorem may still construct the signed-period continuation.",
            "falsifier": "An algebraic shift error, an overlapping analytic chart already contained in the frozen rule, a checked source theorem proving this exact continuation, or replay discrepancy.",
            "next_action": "Use C253/B090 for one distinct direct meromorphic/integral continuation construction and test its signed-period hypotheses before any full-interface lift.",
        },
        "source_scope": {
            "sarkissian_spiridonov": "arXiv:1910.11747v4, equations (5), (13), and the fixed c=k>0 convention",
            "theta_boundary": "DLMF 20.2(ii)",
        },
        "frozen_hashes": freeze_inputs(R, I),
        "runtime": check_runtime("C252"),
        "sealer": {"path": "proof/build_cycle_252_reciprocal_negative_alpha_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=O, payload_factory=payload))
