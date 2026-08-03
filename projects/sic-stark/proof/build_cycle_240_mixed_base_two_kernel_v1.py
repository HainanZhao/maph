#!/usr/bin/env python3
"""Seal Cycle 240/B077 Faddeev two-kernel common-period containment."""
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_240_mixed_base_two_kernel import audit


R = Path(__file__).resolve().parents[1]
O = R / "artifacts/cycle-240-b077-mixed-base-two-kernel-v1.json"
I = {
    "prior": (R / "artifacts/cycle-239-b076-rarefied-beta-embedding-v1.json", "e5e7e2e94a593158fcfcc6b03926832f0b3402b1556d67f10120c3ba7400607b"),
    "prereg": (R / "docs/cycle-240-b077-mixed-base-two-kernel-preregistration-v1.md", "18032c898ff701c41ded6d198f420500df14fae89124d62069a75e76497fc656"),
    "replay": (R / "proof/verify_cycle_240_mixed_base_two_kernel.py", "ee8899c3b5c61c23366cef78eac60143a5c1ab2d37640ad465767315219add3c"),
    "test": (R / "tests/test_cycle_240_mixed_base_two_kernel.py", "31c0f0528320ac092d46fa3ad71cc9a57ac5c78184fdc0d112146a88e72d2cc9"),
    "validator": (R / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
    "scaffold": (R / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload():
    result = audit()
    require(result["status"] == "FALSIFIED_FADDEEV_TWO_KERNEL_COMMON_PERIOD_CLOSURE", "unearned two-kernel containment")
    return {
        "artifact_id": "cycle-240-b077-mixed-base-two-kernel-v1",
        "cycle": 240,
        "budget_ordinal": "B077",
        "epistemic_status": "PROVED",
        "status": "SEALED_FADDEEV_TWO_KERNEL_COMMON_PERIOD_CONTAINMENT",
        "claim_boundary": "Faddeev's cited FTD/MIR pair cannot close either frozen first C228 factor pair because they have no common period system up to scaling and swap. A genuinely mixed-base or higher-dimensional transform, targets, AFK, fusion, Stark, and TCC remain open.",
        "mixed_base_two_kernel_audit": result,
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "evidence_scope_review": "The endpoint minimal polynomial, A/C base encoding, ordered/swapped determinants, Faddeev common-period hypothesis, contour-instantiation boundary, and replay scope were reviewed.",
            "recommendation": "Seal C240 only for failure of the frozen common-period FTD/MIR construction.",
            "known_flaw": "Nonproportional pairs exclude only scale/swap identification in one normalized period system, not a genuinely mixed-base or higher-dimensional transform.",
            "falsifier": "Any minimal-polynomial, ordered/swapped determinant, A/C base encoding, common-period theorem hypothesis, contour-instantiation, or replay discrepancy.",
            "next_action": "Open a Minkowski two-embedding engine over Q(sqrt(21)): combine Galois-related period pairs into one R^2 lattice kernel, freeze trace pairing and Fourier normalization, and test exact lattice self-duality before a mixed-base integral identity.",
            "adopted": True,
        },
        "frozen_hashes": freeze_inputs(R, I),
        "runtime": check_runtime("C240"),
        "sealer": {"path": "proof/build_cycle_240_mixed_base_two_kernel_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=O, payload_factory=payload))
