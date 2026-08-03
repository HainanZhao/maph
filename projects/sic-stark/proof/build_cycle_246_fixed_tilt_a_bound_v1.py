"""Seal C246/B083 fixed-tilt A-word coefficient bound."""
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_246_fixed_tilt_a_bound import audit


R = Path(__file__).resolve().parents[1]
O = R / "artifacts/cycle-246-b083-fixed-tilt-a-bound-v1.json"
I = {
    "prior_c228": (R / "artifacts/cycle-228-b065-f3-square-residual-block-v1.json", "2078970c02c1f1359de25394f57c9229dab4fef01c15894bc36b1ea177deafe4"),
    "prior_c244": (R / "artifacts/cycle-244-b081-constructed-abel-current-v1.json", "58589f8ef0d37a6d26a2084ffb77527970309657ebfcdaacdd9f91cbedcc388a"),
    "prior_c245": (R / "artifacts/cycle-245-b082-a-principal-coefficients-v1.json", "74f0e4e3f91a7554e5cc1cb5145a146de3d54a74a98da13cf739878300ad3a65"),
    "prereg": (R / "docs/cycle-246-b083-fixed-tilt-a-bound-preregistration-v1.md", "64b6697a0ac294d5d2c741468d515f3369c9e1ee41a97cdda338eb3cd2f882b4"),
    "replay": (R / "proof/verify_cycle_246_fixed_tilt_a_bound.py", "fd7661a7932f80688d3cc731f5b2624aac19bce1efb5fd5c1179e0a2df84a57d"),
    "test": (R / "tests/test_cycle_246_fixed_tilt_a_bound.py", "fed6a12ef1798fb3e5fbb6441995242420f1faaff52a3965f438db6936004e75"),
    "validator": (R / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
    "scaffold": (R / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload():
    result = audit()
    bound = result["bound"]
    require(bound["epistemic_status"] == "PROVED", "unproved bound")
    require(bound["C"] == "2^40000000" and bound["d"] == 0, "unfrozen bound constants")
    require(bound["all_N"], "finite-only bound")
    require(not bound["numerical_sampling_used"], "numerical-only bound")
    return {
        "artifact_id": "cycle-246-b083-fixed-tilt-a-bound-v1",
        "cycle": 246,
        "budget_ordinal": "B083",
        "epistemic_status": "PROVED",
        "status": "SEALED_FIXED_TILT_A_COEFFICIENT_BOUND",
        "claim_boundary": "At the frozen common upper tilt w_sigma=t_sigma+i, the normalized C245 source-defined A-word principal coefficients satisfy max(|kappa_N^+/kappa_1^+|,|kappa_N^-/kappa_1^-|)<=2^40000000 for every N>=1. This neither controls epsilon-to-zero nor removes C244's lambda^N ambiguity; it proves no canonical current, source authorization, contour identity, mixed-base transform, B-Fourier covariance, AFK, fusion, Stark, or TCC.",
        "audit": result,
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "reviewed_work": "C246 exact root/period bounds at w_sigma=t_sigma+i, three factor-class audit at both embeddings, 230/50 product ledger, and analytic product estimate.",
            "recommendation": "Seal C246/B083 as the narrow fixed-tilt normalized A-word boundedness result.",
            "known_flaw": "Fixed epsilon=1 does not control epsilon-to-zero and does not remove C244 lambda^N ambiguity; no canonical boundary current, source authorization, or A-to-C identity follows.",
            "falsifier": "Any determinant/period bound, factor count, exponent-to-r^N reduction, elementary product inequality, or replay discrepancy; demonstrated fixed-tilt dependence refutes later regulator-independent promotion.",
            "next_action": "Open a distinct uniqueness/regulator-independence engine only if it freezes a new question and preserves this boundary.",
            "adopted": True,
        },
        "frozen_hashes": freeze_inputs(R, I),
        "runtime": check_runtime("C246"),
        "sealer": {"path": "proof/build_cycle_246_fixed_tilt_a_bound_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=O, payload_factory=payload))
