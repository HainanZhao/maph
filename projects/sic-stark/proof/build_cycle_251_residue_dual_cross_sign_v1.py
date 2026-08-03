"""Seal C251/B088 canonical residue-dual cross-sign falsifier."""
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_251_residue_dual_cross_sign import audit


R = Path(__file__).resolve().parents[1]
O = R / "artifacts/cycle-251-b088-residue-dual-cross-sign-v1.json"
I = {
    "prior_c219": (R / "artifacts/cycle-219-b056-signed-k-extension-v1.json", "d305dc5e7ad3fc904b51ba4ce208938b7c0c675d8b865397d862420c54744291"),
    "prior_c228": (R / "artifacts/cycle-228-b065-f3-square-residual-block-v1.json", "2078970c02c1f1359de25394f57c9229dab4fef01c15894bc36b1ea177deafe4"),
    "prior_c228_replay": (R / "proof/verify_cycle_228_f3_square_residual_block.py", "3419d8d4f0e81cbfc8c970c3c1de5d16f6c79fa793042291156492796f683987"),
    "prior_c249": (R / "artifacts/cycle-249-b086-common-jet-chamber-v1.json", "fc0bca22598fa6519657a607bc93b24ba5948dd0657f3f4c726b8aafafacb35a"),
    "prior_c249_replay": (R / "proof/verify_cycle_249_common_jet_chamber.py", "a2d154cc8efed0db3db97d2ca7e0237ed1716ecf1cfadec57098bf3455f3b507"),
    "prior_c250": (R / "artifacts/cycle-250-b087-graded-f3-jet-representation-v1.json", "f22c8b305a6e49066c8f77ab305bf3e29b621ddfca75fcca086683c61947b9b7"),
    "prior_c250_replay": (R / "proof/verify_cycle_250_graded_f3_jet_representation.py", "0229ae1aa9948559c03478f74e1a6d405487c6f37bb842dbf18ce245989b6bc7"),
    "source_paper": (R / "paper/sic-stark-dimension-six-boundary-fusion.tex", "347228e05a87946ca41bb31c118aae069b7fb6002fff4933d030a153cef21cb7"),
    "prereg": (R / "docs/cycle-251-b088-residue-dual-cross-sign-preregistration-v1.md", "6427ec214c69e334b01b64023364f7a024ea922277cdae410a9ce490b2b0b16f"),
    "replay": (R / "proof/verify_cycle_251_residue_dual_cross_sign.py", "3ed67005d33c68ee97f1a4e03e2e5d66578f8c31c4125e4f4b8d7de6456a33ae"),
    "test": (R / "tests/test_cycle_251_residue_dual_cross_sign.py", "de4752b1797f11a7c33dde2ae277e39b368bb44f8747fc1acd0e979c2df180e3"),
    "validator": (R / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
    "scaffold": (R / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload():
    result = audit()
    orientation = result["orientation_test"]
    require(result["epistemic_status"] == "PROVED", "unproved C251 result")
    require(result["status"] == "CANONICAL_RESIDUE_DUAL_CROSS_SIGN_FALSIFIED", "unearned falsifier")
    require(orientation["canonical_orientation_maps_outside_source_product_domain"], "orientation remained source-defined")
    require(not orientation["degree_0_to_3_contragredient_coefficients_compared"], "selection-rule breach")
    return {
        "artifact_id": "cycle-251-b088-residue-dual-cross-sign-v1",
        "cycle": 251,
        "budget_ordinal": "B088",
        "epistemic_status": "PROVED",
        "status": "SEALED_CANONICAL_RESIDUE_DUAL_CROSS_SIGN_FALSIFIED",
        "claim_boundary": result["claim_boundary"],
        "audit": result,
        "decision": {
            "basis": "The canonical residue adjoints are exact, but all eight orientation-reflected period pairs have negative determinant, leave C249's source product domain, and differ from their A/C targets by an extra alpha sign.",
            "known_flaw": "The result excludes only the canonical pairing and uncorrected omega1 orientation reversal on the fixed rank-four chamber.",
            "falsifier": "Any residue-adjoint identity error, period-pair transcription error, nonnegative reflected determinant, in-domain reflected q base, or replay discrepancy.",
            "next_action": "A new engine must derive an analytic negative-alpha continuation with explicit branch/monodromy and correction factor before it can act on the C250 jets.",
        },
        "frozen_hashes": freeze_inputs(R, I),
        "runtime": check_runtime("C251"),
        "sealer": {"path": "proof/build_cycle_251_residue_dual_cross_sign_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=O, payload_factory=payload))
