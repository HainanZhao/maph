"""Seal C250/B087 graded positive-F3 jet representation."""
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_250_graded_f3_jet_representation import audit


R = Path(__file__).resolve().parents[1]
O = R / "artifacts/cycle-250-b087-graded-f3-jet-representation-v1.json"
I = {
    "c248_prereg": (R / "docs/cycle-248-b085-filtered-f3-jet-representation-preregistration-v1.md", "99e31440a9882bcfaccd33bc7d109b1522fbdb8d2fb7a6cce31f55f00efba7a9"),
    "prior_c226": (R / "artifacts/cycle-226-b063-signed-product-groupoid-v1.json", "c1c3fd23d20a3cd2e40a84dda8e0fade3b1aa873d5c8b66a2b532a1c79fb516c"),
    "prior_c226_replay": (R / "proof/verify_cycle_226_signed_product_groupoid.py", "51eb9d4f07b7c6a2a19ac4229d84badac876adfa0ca394a1cf2d5b2a5a5132b9"),
    "prior_c227": (R / "artifacts/cycle-227-b064-augmented-transport-normal-forms-v1.json", "a9e61b575078ff4ad1b3b16b47743cc7325ebec9ae75db746f7395db18c5a88c"),
    "prior_c227_replay": (R / "proof/verify_cycle_227_augmented_transport_normal_forms.py", "973fc04edd953d840a84d41647ad44279eb49b55944cc3de143b83f22dd5513c"),
    "prior_c228": (R / "artifacts/cycle-228-b065-f3-square-residual-block-v1.json", "2078970c02c1f1359de25394f57c9229dab4fef01c15894bc36b1ea177deafe4"),
    "prior_c228_replay": (R / "proof/verify_cycle_228_f3_square_residual_block.py", "3419d8d4f0e81cbfc8c970c3c1de5d16f6c79fa793042291156492796f683987"),
    "prior_c249": (R / "artifacts/cycle-249-b086-common-jet-chamber-v1.json", "fc0bca22598fa6519657a607bc93b24ba5948dd0657f3f4c726b8aafafacb35a"),
    "prior_c249_replay": (R / "proof/verify_cycle_249_common_jet_chamber.py", "a2d154cc8efed0db3db97d2ca7e0237ed1716ecf1cfadec57098bf3455f3b507"),
    "source_paper": (R / "paper/sic-stark-dimension-six-boundary-fusion.tex", "347228e05a87946ca41bb31c118aae069b7fb6002fff4933d030a153cef21cb7"),
    "prereg": (R / "docs/cycle-250-b087-graded-f3-jet-representation-preregistration-v1.md", "9ba7da47413d7a8293161d7662c4b615ea4cea81ae6f079ce71cb9c2ca65ba8a"),
    "replay": (R / "proof/verify_cycle_250_graded_f3_jet_representation.py", "0229ae1aa9948559c03478f74e1a6d405487c6f37bb842dbf18ce245989b6bc7"),
    "test": (R / "tests/test_cycle_250_graded_f3_jet_representation.py", "b5ce36991896fd0574f8cbf759db1e9b100032d546ad8ae80b30ddeee2a137b9"),
    "validator": (R / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
    "scaffold": (R / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload():
    result = audit()
    require(result["epistemic_status"] == "PROVED", "unproved C250 result")
    require(result["status"] == "GRADED_POSITIVE_F3_JET_REPRESENTATION_CONSTRUCTED", "unearned representation")
    require(result["representation"]["positive_A_C_edges_intertwined"], "missing positive A/C action")
    require(not result["representation"]["negative_k_or_cross_sign_law_derived"], "scope breach")
    require(all(path["matrix_identity_holds"] for path in result["paths"]), "operator mismatch")
    return {
        "artifact_id": "cycle-250-b087-graded-f3-jet-representation-v1",
        "cycle": 250,
        "budget_ordinal": "B087",
        "epistemic_status": "PROVED",
        "status": "SEALED_GRADED_POSITIVE_F3_JET_REPRESENTATION",
        "claim_boundary": result["claim_boundary"],
        "audit": result,
        "decision": {
            "basis": "All preregistered source-state, factor-order, fixed-chamber, coefficient, grading-normalization, and 4-by-4 operator checks pass exactly for both paths.",
            "known_flaw": "The representation is fixed-tilt and positive-path only; it supplies no endpoint, tilt-independence, negative-k, or cross-sign law.",
            "falsifier": "Any source factor transcription, c^(r-1) coefficient law, 24^(-2n) normalization, ordered-word coefficient, C228 comparison, or replay discrepancy.",
            "next_action": "Use the proved graded action as state for a new, explicitly source-derived orientation/cross-sign construction; do not infer such a law from positive functoriality alone.",
        },
        "frozen_hashes": freeze_inputs(R, I),
        "runtime": check_runtime("C250"),
        "sealer": {"path": "proof/build_cycle_250_graded_f3_jet_representation_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=O, payload_factory=payload))
