#!/usr/bin/env python3
"""Seal Cycle 239/B076 rarefied-beta direct-embedding containment."""
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_239_rarefied_beta_embedding import audit


R = Path(__file__).resolve().parents[1]
O = R / "artifacts/cycle-239-b076-rarefied-beta-embedding-v1.json"
I = {
    "prior": (R / "artifacts/cycle-238-b075-faddeev-fourier-dualization-v1.json", "ff963b7e3e4dd238b939cd0c092b6831d1a55fe34ed205d8677b022c481ec9ab"),
    "prereg": (R / "docs/cycle-239-b076-rarefied-beta-embedding-preregistration-v1.md", "68828d9385bca990aafa22721a5c0aaede1e8e762193ef959da3c5a4dfce1fbd"),
    "replay": (R / "proof/verify_cycle_239_rarefied_beta_embedding.py", "5cb2012c26f2743f8156c999899456d290ff5b91f9d68539ea44048df17a2636"),
    "test": (R / "tests/test_cycle_239_rarefied_beta_embedding.py", "8771d03a69c0f03ef7c292f9400328e25daf49f172f5bbcb5edc1522d76611ae"),
    "validator": (R / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
    "scaffold": (R / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload():
    result = audit()
    require(result["status"] == "FALSIFIED_DIRECT_RAREFIED_BETA_KERNEL_EMBEDDING", "unearned rarefied-beta containment")
    return {
        "artifact_id": "cycle-239-b076-rarefied-beta-embedding-v1",
        "cycle": 239,
        "budget_ordinal": "B076",
        "epistemic_status": "PROVED",
        "status": "SEALED_DIRECT_RAREFIED_BETA_EMBEDDING_CONTAINMENT",
        "claim_boundary": "The cited S--S rarefied hyperbolic beta theorem (arXiv:1910.11747v4, equation (42)) cannot directly embed either frozen C228 residual word. Other multi-kernel identities, a separately proved mixed-base composition, targets, AFK, fusion, Stark, and TCC remain open.",
        "rarefied_beta_embedding_audit": result,
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "evidence_scope_review": "The literal equation-(42) lens/period, factor-count, plus/minus-pairing, balancing, contour, denominator/output conditions and the C228 slope/base/state census were reviewed.",
            "recommendation": "Seal C239 as failure of the literal rarefied-beta embedding and open a distinct construction cycle.",
            "known_flaw": "The theorem mismatch excludes neither another multi-kernel identity nor a newly proved mixed-base composition of single-kernel transforms.",
            "falsifier": "Any equation-(42) lens/period, factor-count, plus/minus pairing, balancing, contour, denominator/output, C228 slope/base/state, or replay discrepancy.",
            "next_action": "Construct the smallest mixed-base composition theorem from two C228 factors: freeze transform order, auxiliary variable, contours, and Fubini conditions, then prove or falsify exact two-kernel closure before attempting all four factors.",
            "adopted": True,
        },
        "frozen_hashes": freeze_inputs(R, I),
        "runtime": check_runtime("C239"),
        "sealer": {"path": "proof/build_cycle_239_rarefied_beta_embedding_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=O, payload_factory=payload))
