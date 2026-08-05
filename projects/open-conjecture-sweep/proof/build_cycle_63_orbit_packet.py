"""Seal C63's exact continuous S3 orbit and stationary-stratum reduction."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.check_cycle_63_orbit_packet import audit
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256


H = {
    "prior": ("artifacts/cycle-62-b062-kkt-exchange-v1.json", "366297591f8e9170dadd90b10f7479f48724c65da473258f4e54330ff5e7f8ac"),
    "prereg": ("docs/cycle-63-b063-orbit-minimizer-preregistration-v1.md", "1b4fa4bbcb0d0e37ccca6a5fa6d631ed606935a381eede788b76db6c37c98a7b"),
    "idea": ("discovery/cycle63_orbit_invariant_idea_selection.md", "0c5f651eb7941346136fd706ea559fb143c1b37d564fab8357f467edf197e484"),
    "source_builder": ("proof/cycle63_s3_source_polynomial.cpp", "032a175fb02ce8e38631253c1da5c2e360e4fc013f38cdab767d44f239d85bc5"),
    "orbit_reducer": ("proof/cycle63_reduce_orbit.py", "26022a7de0299027e4884f7497a8d12cc481bd8f9293f21787908d3e679a2d78"),
    "orbit_checker": ("proof/check_cycle63_orbit_polynomial.py", "e5a7cc048b44595067a71b9aba09643da7a3e44811b6cb70a7980a473baa260d"),
    "elementary_reducer": ("proof/cycle63_elementary_symmetric.py", "53b8ba0dc6f3163d86204bb4720a0b163737e54c5ae0ff75798ebdcbb47e08d3"),
    "stationary_builder": ("proof/cycle63_stationary_system.py", "81244a7c46939d24a500e1e61e3ada1102e691cf0bd0e0f8c1d36491e153f58c"),
    "soundness": ("proof/cycle_63_orbit_realizability.md", "2dca6574f655dffa226731e70b90123507c7556711fbfede30bcec454f4693c0"),
    "audit": ("proof/check_cycle_63_orbit_packet.py", "a2726bb5cfe6eae62fa3abbb5f3b62d0d447934a86073845b627ccca886dfd41"),
    "test": ("tests/test_cycle_63_orbit_packet.py", "433c3e9a669229948da9ecec662fd0bf51f8d370d80cf96b2ab3b489d65d7961"),
    "schur_probe_source": ("discovery/cycle63_schur_probe.cpp", "e8d70f3602a51cefcd38eab243e71d4e0f2949d0d36d24a8fee22789f6ded030"),
    "modular_source": ("discovery/cycle63_modular_dimension.py", "280aec9f3aabd25ba617fa20a44d80d0952152755b32a8016a1ac826ee904d69"),
    "source_polynomial": ("discovery/out/cycle63-orbit-minimizer/source-polynomial.tsv", "64940bd62507415c112c26a72bef08799a97d5db40d7cf79700703ed5c966948"),
    "orbit_polynomial": ("discovery/out/cycle63-orbit-minimizer/orbit-polynomial.tsv", "1966204bef5189f821885223ac7b3a7bcb0828543b6d7dbf28dd2daad8c784c4"),
    "orbit_summary": ("discovery/out/cycle63-orbit-minimizer/orbit-summary.json", "26158d6e6c1cf1fda350e4a996a756bc40dc6756bc8ef08b6c0738e3e4769860"),
    "orbit_audit": ("discovery/out/cycle63-orbit-minimizer/orbit-audit.json", "fc235c50e901d146b731397adab8c8ae8a11db84b706926f74284308856afeb7"),
    "elementary_polynomial": ("discovery/out/cycle63-orbit-minimizer/elementary-polynomial.tsv", "f2064408d20f66311f1f544d46edd205dcf964d67e0a4ddb0f209305c4f1bf7e"),
    "elementary_summary": ("discovery/out/cycle63-orbit-minimizer/elementary-summary.json", "8b1b41f628a3386a503c6cf7f272b1020ce512037364f9bb58af621570338a9d"),
    "stationary_system": ("discovery/out/cycle63-orbit-minimizer/generic-stationary-system.tsv", "c73e6a17d890a7dc5df8a02a5f90e39294c3d333be0ea845c3964f2eface57f0"),
    "stationary_summary": ("discovery/out/cycle63-orbit-minimizer/generic-stationary-summary.json", "bafab22514ca7dc7d27b61e8fb2c05f9a2aee2f7e884db57df78544c9581d259"),
    "modular_result": ("discovery/out/cycle63-orbit-minimizer/modular-dimension-32003.json", "f3c7adf507cca197791f69d422d71659d519356d456abee69484cd2a047a5a40"),
    "schur_probe_1": ("discovery/out/cycle63-orbit-minimizer/schur-probe-630631.json", "9e598fb91898c6b5cc1535c4bab30bfb8e0f09c5ab25f53491cc7d6f9745f33f"),
    "schur_probe_2": ("discovery/out/cycle63-orbit-minimizer/schur-probe-630632.json", "5c365103c5490aa6fd72a653e029dc390536cb8926a96ed53408dd206169c537"),
    "schur_probe_3": ("discovery/out/cycle63-orbit-minimizer/schur-probe-630633.json", "52fb23f3e1cf80f9bc20ab14d56440b618cc109839c2ea4e4175b2b605371f49"),
    "packet_audit": ("discovery/out/cycle63-orbit-minimizer/packet-audit.json", "2d811b69706c9a158daae21b49e45de55c69b9059db32212a1ed497fd9936dbd"),
    "prior_derivatives": ("discovery/out/cycle62-kkt-exchange/exchange-derivatives.tsv", "61e9cd5dfe1dc2469ad40578e7951fc9744116a6225258311fe4bad4b4861dec"),
    "scaffold": ("proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "validator": ("../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def payload():
    checked = audit()
    return {
        "artifact_id": "cycle-63-b063-orbit-minimizer-v1",
        "budget_ordinal": "B063",
        "cycle": 63,
        "record_type": "PROVED_CONTINUOUS_S3_ORBIT_AND_STATIONARY_REDUCTION",
        "recorded_at_utc": "2026-08-05T10:22:33Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "The continuous normalized S3 Zhao deficit has an exact six-coordinate semialgebraic quotient, an independently larger S3-by-C2 symmetry that removes the orientation invariant, and explicit multiplicity-stratified stationary equations.",
        "claim_boundary": checked["claim_boundary"],
        "audit": checked,
        "cycle_decision": {
            "companion_identity": "/root/darwin_cycle25_short",
            "companion_advice": "Seal the exact quotient reduction and open one distinct fiberwise invariant-minimization cycle; do not elevate separate Schur-convexity to the primary target.",
            "next_question": "For fixed e,t,c,r2, can exact low-degree minimization over the feasible (u,s2) fiber force minima to explicit fiber boundaries or finitely certified interior branches?",
            "falsifier": "An exact feasible invariant tuple with negative deficit refutes S3 Zhao comparison; an exchange reversal refutes only the stronger Schur route.",
        },
        "resource_observations": {
            "source_expansion_wall_seconds": 0.63,
            "orbit_reduction_wall_seconds": 14.05,
            "independent_audit_wall_seconds": 12.55,
            "three_parallel_schur_probes_wall_seconds": 4.4,
            "generic_modular_groebner": "WALL_CAP_AT_300_SECONDS_BEFORE_BASIS",
        },
        "frozen_hashes": freeze_inputs(ROOT, {key: (ROOT / path, expected) for key, (path, expected) in H.items()}),
        "runtime": check_runtime("c63"),
        "sealer": {"path": "proof/build_cycle_63_orbit_packet.py", "sha256": sha256(Path(__file__))},
        "replay": {
            "source": "g++ -O3 -DNDEBUG -std=c++20 proof/cycle63_s3_source_polynomial.cpp -o /tmp/c63-source && /tmp/c63-source discovery/out/cycle63-orbit-minimizer",
            "orbit": "python3 proof/cycle63_reduce_orbit.py discovery/out/cycle63-orbit-minimizer/source-polynomial.tsv discovery/out/cycle63-orbit-minimizer",
            "elementary": "python3 proof/cycle63_elementary_symmetric.py discovery/out/cycle63-orbit-minimizer/orbit-polynomial.tsv discovery/out/cycle63-orbit-minimizer",
            "stationary": "python3 proof/cycle63_stationary_system.py discovery/out/cycle63-orbit-minimizer/elementary-polynomial.tsv discovery/out/cycle63-orbit-minimizer",
            "audit": "python3 proof/check_cycle_63_orbit_packet.py",
            "test": "python3 -m unittest tests/test_cycle_63_orbit_packet.py",
            "check": "python3 proof/build_cycle_63_orbit_packet.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(
        description=__doc__,
        output=ROOT / "artifacts/cycle-63-b063-orbit-minimizer-v1.json",
        payload_factory=payload,
    ))
