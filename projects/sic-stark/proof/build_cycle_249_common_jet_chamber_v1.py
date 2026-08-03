"""Seal C249/B086 common fixed upper chamber for C228 residual jets."""
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_249_common_jet_chamber import audit


R = Path(__file__).resolve().parents[1]
O = R / "artifacts/cycle-249-b086-common-jet-chamber-v1.json"
I = {
    "prior_c228": (R / "artifacts/cycle-228-b065-f3-square-residual-block-v1.json", "2078970c02c1f1359de25394f57c9229dab4fef01c15894bc36b1ea177deafe4"),
    "prior_c245": (R / "artifacts/cycle-245-b082-a-principal-coefficients-v1.json", "74f0e4e3f91a7554e5cc1cb5145a146de3d54a74a98da13cf739878300ad3a65"),
    "prior_c228_replay": (R / "proof/verify_cycle_228_f3_square_residual_block.py", "3419d8d4f0e81cbfc8c970c3c1de5d16f6c79fa793042291156492796f683987"),
    "prior_c245_replay": (R / "proof/verify_cycle_245_a_principal_coefficients.py", "63829b316a362844f97bcfac4321bea5da8f0588e26b7ec2130d9dd3fc06d986"),
    "source_paper": (R / "paper/sic-stark-dimension-six-boundary-fusion.tex", "347228e05a87946ca41bb31c118aae069b7fb6002fff4933d030a153cef21cb7"),
    "prereg": (R / "docs/cycle-249-b086-common-jet-chamber-preregistration-v1.md", "c79df4ef48f8b67e2a1f2c4ed0cab711110661564fd8993b54d91146a18f69f9"),
    "replay": (R / "proof/verify_cycle_249_common_jet_chamber.py", "a2d154cc8efed0db3db97d2ca7e0237ed1716ecf1cfadec57098bf3455f3b507"),
    "test": (R / "tests/test_cycle_249_common_jet_chamber.py", "fc0f610bcdd362f478ee02194f4b722d456d8e9c97ca0015eb62a379a74c04b7"),
    "validator": (R / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
    "scaffold": (R / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload():
    result = audit()
    require(result["epistemic_status"] == "PROVED", "unproved C249 result")
    require(result["status"] == "COMMON_FIXED_UPPER_CHAMBER_FOR_C228_JETS", "unearned chamber result")
    require(result["factor_count"] == 8, "wrong frozen factor coverage")
    require(all(row["analytic_jet"]["leading_coefficient_nonzero"] for row in result["factors"]), "undefined normalized germ")
    return {
        "artifact_id": "cycle-249-b086-common-jet-chamber-v1",
        "cycle": 249,
        "budget_ordinal": "B086",
        "epistemic_status": "PROVED",
        "status": "SEALED_COMMON_FIXED_UPPER_CHAMBER_FOR_C228_JETS",
        "claim_boundary": "At the frozen two-embedding regularization w_sigma=t_sigma+i, all eight C228 ordinary-gamma factors have |q|<1 and |qtilde|<1. Their normalized germs have nonzero leading coefficients and absolutely convergent degree-0:3 q-product/Lambert-series jets. This proves no endpoint limit, no C248 path representation, no negative-k or cross-sign law, packet map, canonical current, contour identity, mixed-base transform, B-Fourier covariance, AFK, fusion, Stark, or TCC.",
        "audit": result,
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "reviewed_work": "C249 exact determinant audit for all eight C228 A/C factors at both embeddings, fixed-tilt q-product inequalities, normalized-germ factorization, and degree-0:3 Lambert-series convergence statement.",
            "recommendation": "Seal C249/B086 with the factorwise fixed-tilt analytic-domain result.",
            "known_flaw": "The certificate supplies no compatibility of the jets with C248 coordinate-aware path composition and no endpoint or tilt-independence statement.",
            "falsifier": "Any retained factor with nonpositive determinant, a product base outside the unit disk, or a zero/undefined normalized leading coefficient.",
            "next_action": "Open a distinct cycle reconstructing the C248 positive filtered path representation using this frozen chamber; do not retrofit C248 or promote the certificate to a cross-sign result.",
            "adopted": True,
        },
        "frozen_hashes": freeze_inputs(R, I),
        "runtime": check_runtime("C249"),
        "sealer": {"path": "proof/build_cycle_249_common_jet_chamber_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=O, payload_factory=payload))
