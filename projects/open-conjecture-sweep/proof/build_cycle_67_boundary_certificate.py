"""Seal C67's exact fixed-S3 endpoint-boundary theorem."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.check_cycle67_boundary_certificate import audit
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256


H = {
    "c64": ("artifacts/cycle-64-b064-fiber-minimization-v1.json", "141097ac5719461203b118046adf16e9d85655bfcb084a55221f95ad582c66b7"),
    "c66": ("artifacts/cycle-66-b066-s3-pivot-audit-v1.json", "14ef49fea76ac01d9c9cc985d8997123d9e0a587c0a8be3c92de254692fdb8c6"),
    "prereg": ("docs/cycle-67-b067-s3-boundary-positivity-preregistration-v1.md", "26940b67a6c11174d3e879dbddf0095de31a12969cf703c0cfb8441f43423be7"),
    "idea": ("discovery/cycle67_boundary_idea_selection.md", "3e9bb90807abae0ff209ae8868c7cf260022a2b76c83f05d5aac0d5ebc454786"),
    "source_polynomial": ("discovery/out/cycle63-orbit-minimizer/source-polynomial.tsv", "64940bd62507415c112c26a72bef08799a97d5db40d7cf79700703ed5c966948"),
    "orbit_polynomial": ("discovery/out/cycle63-orbit-minimizer/orbit-polynomial.tsv", "1966204bef5189f821885223ac7b3a7bcb0828543b6d7dbf28dd2daad8c784c4"),
    "pullbacks": ("proof/cycle67_boundary_pullbacks.py", "7e5282787383608e9234c8216de6d761f559d360edd3c6401c104cc11037dca9"),
    "grid": ("proof/cycle67_boundary_grid.cpp", "084c4d20ffef300d87ec8617d5f0770f94277a687c6b251582d539d714a36b65"),
    "chart_algebra": ("proof/cycle67_equality_blowup.py", "0ed0fe005416ee34270d0d1acd9497dbfc39c5733212115fc8166a06de20cd0c"),
    "orbit_algebra": ("proof/cycle67_equality_blowup_orbit.py", "940732009abb7eee5992ae884ba89feee98ad6c815bae6fe4da9a829d4472386"),
    "invariant_forms": ("proof/cycle67_emit_scaled_chart_forms.py", "fbdd45debcc1b338b72bb78f31101d5ff2ae7a1207d092eccab430912a440a6b"),
    "source_forms": ("proof/cycle67_emit_scaled_pullback_forms.py", "e4baac5ad33af89ea95a7697c43207e31a0b2a3a16cd44554306343f3f665896"),
    "invariant_expander": ("proof/cycle67_expand_charts_fast.cpp", "f27deb7a360e6c5d47a2ef7dc624d7def37833e31c22b5c068b9c43cc8bf23a5"),
    "source_expander": ("proof/cycle67_expand_pullbacks_fast.cpp", "3918d51527ada103f348be7a3884394e4b3bc1ce9eac3d838f007951886c7e17"),
    "factor_stripper": ("proof/cycle67_strip_boundary_factors.py", "05b395e63252b3ed149d14a842badd83967503a58b78ad36a731992bae43b590"),
    "factor_checker": ("proof/check_cycle67_boundary_factors.py", "663e6916dfeb37d4d85174653a1cdee7f4ea6279640ef5c9f9d0f7d4eeb8e63e"),
    "hessian": ("proof/cycle67_trans_hessian_quotients.py", "b5baf63b22c8e40a053ae29a761d003b22ba588ec6740e14ec336c6d1fe469c5"),
    "curve": ("proof/cycle67_trans_curve_restrictions.py", "6541397c766ebdb625bf0a13b4d3895c7956d5e48ad3457ccd613460ba2ab7c0"),
    "equal_joint": ("proof/cycle67_trans_joint_blowup.py", "008ad5e68d2eb92ac41888777aa166b9734ebbd06dde6bf658e117cd5ae7ebae"),
    "transzero_joint": ("proof/cycle67_transzero_joint_blowup.py", "2eaf5ae64243554fa694cf59c966dcb968d6e949f4017cbede7f4bf8fa01404c"),
    "cyclezero_corner": ("proof/cycle67_cyclezero_corner_blowup.py", "9d3bcfcc3396e9a43501712c3f14b538408e63ff181068f23c0b9d4d786466d7"),
    "bernstein": ("proof/cycle67_tensor_bernstein.cpp", "da6fbb9050c94b6b8421e84c103f8ab11d4e2fac599feafadec0563dacd79da3"),
    "soundness": ("proof/cycle_67_boundary_blowup_soundness.md", "60d9029d1a852a5feb3f5e86d68991bc46e9c2c33933cecf4cbfe103bd4192b3"),
    "audit": ("proof/check_cycle67_boundary_certificate.py", "35d622a393c64292c226a18077d5a483179b79188fe01c2ebc07570d196dfb3f"),
    "replay": ("proof/replay_cycle67_boundary_certificate.sh", "36e4020d4d9d80723b6e540ac886115839d0bd840eebc3ea3ace3ceb0414f4ce"),
    "test": ("tests/test_cycle_67_boundary_certificate.py", "04851f73f019f02034c67063cd9f2f53646f7beb553bdf78b35a538365de7984"),
    "scaffold": ("proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "validator": ("../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def payload():
    checked = audit()
    return {
        "artifact_id": "cycle-67-b067-s3-boundary-positivity-v1",
        "budget_ordinal": "B067",
        "cycle": 67,
        "record_type": "PROVED_FIXED_S3_ENDPOINT_BOUNDARY_THEOREM",
        "recorded_at_utc": "2026-08-05T12:12:15Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": (
            "For every nonnegative S3 function in any of the four C64 fiber "
            "endpoint families, N(a)-N(a_cl) is nonnegative. Exact equality "
            "blow-ups isolate the curves 1-y-3x+xy=0 and 3x-1=0; 31 exact "
            "tensor-Bernstein charts cover all exceptional divisors."
        ),
        "claim_boundary": checked["claim_boundary"],
        "audit": checked,
        "cycle_decision": {
            "companion_identity": "/root/darwin_cycle25_short",
            "companion_advice": (
                "Seal after the integrated source/invariant and chart-coverage "
                "audit; open a distinct interior cycle. Prefer an exact chord-"
                "remainder test, with resultant/Sturm exclusion as fallback."
            ),
            "decision": (
                "Seal the endpoint theorem and open the next cycle on exact "
                "interior-fiber control; do not infer interior positivity from endpoints."
            ),
            "next_question": (
                "Does the degree-at-most-five C64 fiber deficit admit a nonnegative "
                "exact chord remainder, or can an exact feasible interior point be negative?"
            ),
            "falsifier": (
                "One exact endpoint point with negative deficit refutes this artifact; "
                "one exact feasible interior point with negative deficit refutes the "
                "fixed-S3 comparison."
            ),
        },
        "contained_correction": {
            "finding": (
                "An exploratory source optimizer assumed denominator 64 while endpoint "
                "pullbacks require LCM 11943936; -DNDEBUG suppressed its assertion."
            ),
            "effect": (
                "The faulty exploratory output was never promoted. The corrected explicit "
                "LCM route matches all nine invariant charts coefficient-for-coefficient."
            ),
        },
        "frozen_hashes": freeze_inputs(ROOT, {key: (ROOT / path, expected) for key, (path, expected) in H.items()}),
        "runtime": check_runtime("c67"),
        "sealer": {"path": "proof/build_cycle_67_boundary_certificate.py", "sha256": sha256(Path(__file__))},
        "replay": {
            "full": "C67_REPLAY_THREADS=3 proof/replay_cycle67_boundary_certificate.sh",
            "audit": "python3 proof/check_cycle67_boundary_certificate.py",
            "test": "python3 -m unittest tests/test_cycle_67_boundary_certificate.py",
            "check": "python3 proof/build_cycle_67_boundary_certificate.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(
        description=__doc__,
        output=ROOT / "artifacts/cycle-67-b067-s3-boundary-positivity-v1.json",
        payload_factory=payload,
    ))
