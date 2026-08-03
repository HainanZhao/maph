"""Seal C247/B084 frozen one-q tilt-cocycle falsifier."""
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_247_a_tilt_cocycle import audit


R = Path(__file__).resolve().parents[1]
O = R / "artifacts/cycle-247-b084-a-tilt-cocycle-v1.json"
I = {
    "prior_c228": (R / "artifacts/cycle-228-b065-f3-square-residual-block-v1.json", "2078970c02c1f1359de25394f57c9229dab4fef01c15894bc36b1ea177deafe4"),
    "prior_c244": (R / "artifacts/cycle-244-b081-constructed-abel-current-v1.json", "58589f8ef0d37a6d26a2084ffb77527970309657ebfcdaacdd9f91cbedcc388a"),
    "prior_c245": (R / "artifacts/cycle-245-b082-a-principal-coefficients-v1.json", "74f0e4e3f91a7554e5cc1cb5145a146de3d54a74a98da13cf739878300ad3a65"),
    "prior_c246": (R / "artifacts/cycle-246-b083-fixed-tilt-a-bound-v1.json", "e66bc471b9a65e3512b1d97e86926942dbeba1094276dcb1fccac9233af429e6"),
    "prereg": (R / "docs/cycle-247-b084-a-tilt-cocycle-preregistration-v1.md", "e188c3334ec4cb7359668a8ae414a8098d27ec1e3d610999a5269800ad90b1cd"),
    "replay": (R / "proof/verify_cycle_247_a_tilt_cocycle.py", "2dce77a0f72ec37a6b1f8e51fc03b3cf34d06d1e3c5c2eb8d03144deb8dfb8b2"),
    "test": (R / "tests/test_cycle_247_a_tilt_cocycle.py", "d8ec63d2b2013d7cfac29f9858529c0b81d612c60f17111b9cfdfe3c5ac88dfd"),
    "validator": (R / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
    "scaffold": (R / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload():
    result = audit()
    require(result["epistemic_status"] == "PROVED", "unproved phase result")
    require(result["status"] == "FROZEN_ONE_Q_TILT_COCHAIN_FALSIFIED", "unearned engine failure")
    require(result["q_bases"]["not_equal_for_any_positive_tilt"], "common-q premise survived")
    require(not result["q_series_degree_two_inspected"], "forbidden q-series continuation")
    return {
        "artifact_id": "cycle-247-b084-a-tilt-cocycle-v1",
        "cycle": 247,
        "budget_ordinal": "B084",
        "epistemic_status": "PROVED",
        "status": "SEALED_FROZEN_ONE_Q_TILT_COCHAIN_FALSIFIED",
        "claim_boundary": "For every positive plus-embedding tilt, the C247 A1/A4 and A2/A3 source multiplier bases differ even modulo integers, so the preregistered single-q tilt-cocycle/base-only-stability engine cannot be formed. This does not exclude a two-base or multi-base cocycle and does not identify C244's constructed coefficients with the C245 source line, normalize a current, authorize a source identity, or prove a contour identity, mixed-base transform, B-Fourier covariance, AFK, fusion, Stark, or TCC.",
        "audit": result,
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "reviewed_work": "C247 exact C228 phase-role derivation, root-identity subtraction, positive-tilt imaginary-sign certificate, and preregistered stop before the q^2 test.",
            "recommendation": "Seal C247/B084 as PROVED: FROZEN_ONE_Q_TILT_COCHAIN_FALSIFIED.",
            "known_flaw": "It cannot exclude a two-base or multi-base transport and says nothing about source-to-current identification.",
            "falsifier": "A corrected C228 role assignment or exact phase calculation yielding theta-eta in Z at a positive tilt.",
            "next_action": "Open a genuinely multi-base tilt-cocycle cycle only with both bases, branch/transport law, and a predeclared holonomy or Cauchy criterion frozen before work.",
            "adopted": True,
        },
        "frozen_hashes": freeze_inputs(R, I),
        "runtime": check_runtime("C247"),
        "sealer": {"path": "proof/build_cycle_247_a_tilt_cocycle_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=O, payload_factory=payload))
