"""Seal C242/B079 common affine-linear Minkowski cone containment."""
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_242_minkowski_common_contour import audit


R = Path(__file__).resolve().parents[1]
O = R / "artifacts/cycle-242-b079-minkowski-common-contour-v1.json"
I = {
    "prior_c228": (
        R / "artifacts/cycle-228-b065-f3-square-residual-block-v1.json",
        "2078970c02c1f1359de25394f57c9229dab4fef01c15894bc36b1ea177deafe4",
    ),
    "prior_c241": (
        R / "artifacts/cycle-241-b078-minkowski-self-duality-v1.json",
        "e354260e1803f98585be5a2dad197c839321d65755c4240448341e087eb7a93d",
    ),
    "prereg": (
        R / "docs/cycle-242-b079-minkowski-common-contour-preregistration-v1.md",
        "8ec7e0a190e3ebcc2f66747a79c0307a29c56193bceab9479debf0be290870fb",
    ),
    "replay": (
        R / "proof/verify_cycle_242_minkowski_common_contour.py",
        "ee7255d43e8b42807059efd6d789808e1fdaa8c8d75b8d5d5aad8315d66ad161",
    ),
    "test": (
        R / "tests/test_cycle_242_minkowski_common_contour.py",
        "8710ca095b3a3632f7f09afe29854816a186de61fc319d55934003ed30a44c44",
    ),
    "validator": (
        R / "../../tools/preregistration_check.py",
        "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
    ),
    "scaffold": (
        R / "proof/cycle_seal_v1.py",
        "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1",
    ),
}


def payload():
    result = audit()
    require(not result["common_affine_linear_cone_separator_exists"], "unearned contour containment")
    return {
        "artifact_id": "cycle-242-b079-minkowski-common-contour-v1",
        "cycle": 242,
        "budget_ordinal": "B079",
        "epistemic_status": "PROVED",
        "status": "SEALED_COMMON_AFFINE_LINEAR_MINKOWSKI_CONE_CONTAINMENT",
        "claim_boundary": "Under the frozen Galois-equivariant upper tilt and one fixed affine-linear cone normal per embedding, the paired C228 A/C residual words have no common pole/zero cone separator. This does not address one-word, nonlinear, piecewise-linear, factor-dependent, residue-corrected, or other-regularization contours; nor a mixed-base identity, AFK, fusion, Stark, or TCC.",
        "audit": result,
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "recommendation": "Seal C242/B079 as PROVED only for the frozen common affine-linear contour class.",
            "known_flaw": "The result does not exclude separate, nonlinear, piecewise-linear, factor-dependent, or residue-corrected contours.",
            "falsifier": "Any period-generator, embedding, tilt, cone orientation, A/C inequality, shared-normal assumption, all-16 coverage, or replay discrepancy.",
            "next_action": "Test a two-chamber Picard-Lefschetz contour with all crossed divisors and residues audited.",
            "adopted": True,
        },
        "frozen_hashes": freeze_inputs(R, I),
        "runtime": check_runtime("C242"),
        "sealer": {
            "path": "proof/build_cycle_242_minkowski_common_contour_v1.py",
            "sha256": sha256(Path(__file__)),
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=O, payload_factory=payload))
