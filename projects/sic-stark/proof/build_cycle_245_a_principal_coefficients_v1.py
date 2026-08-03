"""Seal C245/B082 A-word principal-coefficient recurrence."""
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_245_a_principal_coefficients import audit


R = Path(__file__).resolve().parents[1]
O = R / "artifacts/cycle-245-b082-a-principal-coefficients-v1.json"
I = {
    "prior_c228": (R / "artifacts/cycle-228-b065-f3-square-residual-block-v1.json", "2078970c02c1f1359de25394f57c9229dab4fef01c15894bc36b1ea177deafe4"),
    "prior_c243": (R / "artifacts/cycle-243-b080-two-chamber-crossing-v1.json", "505846925694811b8f34b6c48120b56b406e15eb9e7e1a044e7763cea8d30896"),
    "prior_c244": (R / "artifacts/cycle-244-b081-constructed-abel-current-v1.json", "58589f8ef0d37a6d26a2084ffb77527970309657ebfcdaacdd9f91cbedcc388a"),
    "prereg": (R / "docs/cycle-245-b082-a-principal-coefficients-preregistration-v1.md", "bc092530194d073f308b32b909c0316d1ff8b96017e461bb66713a3286ca5fac"),
    "replay": (R / "proof/verify_cycle_245_a_principal_coefficients.py", "63829b316a362844f97bcfac4321bea5da8f0588e26b7ec2130d9dd3fc06d986"),
    "test": (R / "tests/test_cycle_245_a_principal_coefficients.py", "0b25c069a068abd94b823c0419730a1bb4b980aeebdf99616667df5f52338019"),
    "validator": (R / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
    "scaffold": (R / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload():
    result = audit()
    recurrence = result["recurrence"]
    require(recurrence["exact_recurrence_family_derived"], "missing exact recurrence")
    require(recurrence["all_multiplier_factors_nonzero"], "unproved multiplier nonvanishing")
    require(result["galois"]["epistemic_status"] == "PROVED", "missing embedding covariance")
    require(not result["growth"]["tempered_bound_proved"], "unearned temperedness")
    return {
        "artifact_id": "cycle-245-b082-a-principal-coefficients-v1",
        "cycle": 245,
        "budget_ordinal": "B082",
        "epistemic_status": "PROVED",
        "status": "SEALED_A_PRINCIPAL_COEFFICIENT_RECURRENCE",
        "claim_boundary": "For the frozen C228 A residual word, the exact double-pole principal coefficients obey an all-N nonzero finite-product recurrence and embedding-re-evaluation covariance in the common upper q-product chamber. This proves neither a polynomial/tempered bound nor source authorization, a contour identity, a mixed-base transform, B-Fourier covariance, AFK, fusion, Stark, or TCC.",
        "audit": result,
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "reviewed_work": "C245 exact shift decompositions, Laurent double-pole ratio, nonvanishing audit, and common-upper-chamber embedding re-evaluation.",
            "recommendation": "Seal C245/B082 only for the exact recurrence, nonvanishing, and C-linear embedding-re-evaluation covariance; open a distinct fixed-tilt growth-bound cycle.",
            "known_flaw": "No uniform small-divisor lower bound, fixed tilt, constants C,d, temperedness, canonical current, source authorization, or A-to-C identity.",
            "falsifier": "A shift, Laurent ratio, multiplier nonvanishing, determinant/chamber, embedding-re-evaluation, or replay discrepancy; for the deferred bound, any certified violation at frozen epsilon_0,C,d.",
            "next_action": "Open a distinct fixed-tilt A-word coefficient-bound question with epsilon_0, C, d, norm/embedding convention, and failure rule frozen before computation.",
            "adopted": True,
        },
        "frozen_hashes": freeze_inputs(R, I),
        "runtime": check_runtime("C245"),
        "sealer": {"path": "proof/build_cycle_245_a_principal_coefficients_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=O, payload_factory=payload))
