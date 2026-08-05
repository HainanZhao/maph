"""Seal C64's exact uniform S3 fiber-minimum reduction."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.check_cycle_64_fiber_packet import audit
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256


H = {
    "prior": ("artifacts/cycle-63-b063-orbit-minimizer-v1.json", "e469288e90c1615e9b3cb15183ca88e4b98062b7ca41e34df535b5eaf8e0c562"),
    "prereg": ("docs/cycle-64-b064-fiber-minimization-preregistration-v1.md", "90cf0135925a287ea296cd27e56f705e01c0deac9bb2724aacf53c5d519becc2"),
    "idea": ("discovery/cycle64_fiber_minimization_idea_selection.md", "7fdba7d322a1fd4e4c8efdbed48dbf2f98cc6e6a40b2fd6f3928c6ecc542690c"),
    "anchor_source": ("discovery/cycle64_anchor_elimination.py", "7faf8c8d2c10fa6d1fa0363a43b7c37fc77f6b7ec6c782cf40f3606ad625abf8"),
    "bound_source": ("proof/cycle64_fiber_resultant_bound.py", "44931ff35fb39fe1688321fe30d094e5420e828f4111d59e85b863d8134fcbc5"),
    "leading_source": ("proof/cycle64_resultant_leading_coefficient.py", "539fa4a5c4db610622f9075d935e89bb7d3658da3f2eca5c437776f38d2103a3"),
    "soundness": ("proof/cycle_64_fiber_minimization_soundness.md", "d2a7bd1c05afe965430f38602468a39fe9e04ee7c4f70bc019168ede15898485"),
    "audit": ("proof/check_cycle_64_fiber_packet.py", "a0ffd4958af0a2cf25686d7a65d3c288e436deb00a76890ee9b8ec82d29d7ed9"),
    "test": ("tests/test_cycle_64_fiber_packet.py", "51bea8a35ead4a11066dcaf8938d5436687064cbfe44548951614460bf761fef"),
    "boundary_source": ("discovery/cycle64_boundary_factor.py", "7590d2d9f6776ee4db7b8feb7b05d1be714839cacc5755a8e36fa41065e025f4"),
    "orbit_polynomial": ("discovery/out/cycle63-orbit-minimizer/orbit-polynomial.tsv", "1966204bef5189f821885223ac7b3a7bcb0828543b6d7dbf28dd2daad8c784c4"),
    "anchor_a1": ("discovery/out/cycle64-fiber-minimization/anchor-a1.json", "eba61cf776e3cc9502aed76be5700343010665f2e5e2a7a16c77bfb06895babf"),
    "anchor_a1_resultant": ("discovery/out/cycle64-fiber-minimization/anchor-a1-resultant.tsv", "5f3c7cf3b363fa2ee9d49904304bc12f8bba25bfe0a3e5aec5a7b47f6772b8be"),
    "anchor_a2": ("discovery/out/cycle64-fiber-minimization/anchor-a2.json", "02e532ba7b9ae0838964f3dc668f17482d55953432579154459a1b115711d843"),
    "anchor_a2_resultant": ("discovery/out/cycle64-fiber-minimization/anchor-a2-resultant.tsv", "303c55db7445357f04b0eb6a110c402b8b47f31a1975bc658899cb6390c04447"),
    "anchor_a3": ("discovery/out/cycle64-fiber-minimization/anchor-a3.json", "327e84b0b995d244ca7f8d60630473e2c67c8fab89299ad16d133300ea24b9f1"),
    "anchor_a3_resultant": ("discovery/out/cycle64-fiber-minimization/anchor-a3-resultant.tsv", "c67b10ca0d856eea4160a06acab16c70bbaf43a705b430ba6f1338c8363cb47d"),
    "leading_result": ("discovery/out/cycle64-fiber-minimization/resultant-leading-coefficient.json", "5ed0ea2f56960fc9709945e9755874d31ff933109001a291f94acf8075a5419e"),
    "bound_result": ("discovery/out/cycle64-fiber-minimization/resultant-bound.json", "3f37b53843fc1cc56d2931d08230370c574e8cf02d93bb76b84ef0e2b5c80d35"),
    "boundary_t_zero": ("discovery/out/cycle64-fiber-minimization/boundary-t_zero.json", "36c3f1c7143824984a9b4e6130e7c697bde429ae539195329a7033a148867cd0"),
    "boundary_c_zero": ("discovery/out/cycle64-fiber-minimization/boundary-c_zero.json", "4efb3fb9aaee7857cee37bfd2296d70d1555a9c922ae51041cb2316c05ee3c4c"),
    "boundary_r_zero": ("discovery/out/cycle64-fiber-minimization/boundary-r_zero.json", "b801ad08743a30b057d892d21ec437dc4123beff3fce72efb2fdd054f2066e52"),
    "boundary_r_max": ("discovery/out/cycle64-fiber-minimization/boundary-r_max.json", "fa9ec8e21b4bf538bdfc6f2ac45fe63f2d4399b1d7a8e2a1f1b997621805d3e6"),
    "packet_audit": ("discovery/out/cycle64-fiber-minimization/packet-audit.json", "9cb0b1e7f65a682d4ab7e93c41c12f2b804c25254291a32503ada71702028976"),
    "scaffold": ("proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "validator": ("../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def payload():
    checked = audit()
    return {
        "artifact_id": "cycle-64-b064-fiber-minimization-v1",
        "budget_ordinal": "B064",
        "cycle": 64,
        "record_type": "PROVED_UNIFORM_FINITE_S3_FIBER_MINIMUM_REDUCTION",
        "recorded_at_utc": "2026-08-05T10:40:14Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "Every fixed outer S3 invariant fiber has its minimum on four explicit endpoint families or among at most 156 isolated algebraic pairs; a constant nonzero u^26 Sylvester coefficient makes the reduction uniform with no genericity exception.",
        "claim_boundary": checked["claim_boundary"],
        "audit": checked,
        "cycle_decision": {
            "companion_identity": "/root/darwin_cycle25_short",
            "companion_advice": "Seal C64 as a finite-per-fiber reduction, then leave the stronger Zhao route and test one fixed unequal-weight 2x2 bipartite step-graphon family with a hard stop.",
            "next_question": "Does the actual Sidorenko deficit for K5,5 minus C10 remain nonnegative over the complete unequal-weight 2x2 bipartite step-graphon family, or is there an exactly reconstructible negative point?",
            "falsifier": "An exact negative step-graphon deficit is a Sidorenko counterexample; a pass is bounded evidence unless accompanied by a reusable exact global extremal reduction.",
        },
        "frozen_hashes": freeze_inputs(ROOT, {key: (ROOT / path, expected) for key, (path, expected) in H.items()}),
        "runtime": check_runtime("c64"),
        "sealer": {"path": "proof/build_cycle_64_fiber_packet.py", "sha256": sha256(Path(__file__))},
        "replay": {
            "anchors": "for a in a1 a2 a3; do python3 discovery/cycle64_anchor_elimination.py $a discovery/out/cycle63-orbit-minimizer/orbit-polynomial.tsv discovery/out/cycle64-fiber-minimization/anchor-$a.json; done",
            "leading": "python3 proof/cycle64_resultant_leading_coefficient.py discovery/out/cycle63-orbit-minimizer/orbit-polynomial.tsv discovery/out/cycle64-fiber-minimization/anchor-a3-resultant.tsv discovery/out/cycle64-fiber-minimization/anchor-a1-resultant.tsv discovery/out/cycle64-fiber-minimization/resultant-leading-coefficient.json",
            "bound": "python3 proof/cycle64_fiber_resultant_bound.py discovery/out/cycle63-orbit-minimizer/orbit-polynomial.tsv discovery/out/cycle64-fiber-minimization/anchor-a3.json discovery/out/cycle64-fiber-minimization/resultant-leading-coefficient.json discovery/out/cycle64-fiber-minimization/resultant-bound.json",
            "audit": "python3 proof/check_cycle_64_fiber_packet.py",
            "test": "python3 -m unittest tests/test_cycle_64_fiber_packet.py",
            "check": "python3 proof/build_cycle_64_fiber_packet.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(
        description=__doc__,
        output=ROOT / "artifacts/cycle-64-b064-fiber-minimization-v1.json",
        payload_factory=payload,
    ))
