"""Seal C244/B081 constructed Abel-current infrastructure."""
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_244_constructed_abel_current import audit

R = Path(__file__).resolve().parents[1]
O = R / "artifacts/cycle-244-b081-constructed-abel-current-v1.json"
I = {
    "prior_c228": (R / "artifacts/cycle-228-b065-f3-square-residual-block-v1.json", "2078970c02c1f1359de25394f57c9229dab4fef01c15894bc36b1ea177deafe4"),
    "prior_c229": (R / "artifacts/cycle-229-b066-f3-square-divisor-v1.json", "2a38f5332e40a8e07dae28027ad554426ca8a1d4f1d6e0ff8f83c2a44cc2ab69"),
    "prior_c239": (R / "artifacts/cycle-239-b076-rarefied-beta-embedding-v1.json", "e5e7e2e94a593158fcfcc6b03926832f0b3402b1556d67f10120c3ba7400607b"),
    "prior_c243": (R / "artifacts/cycle-243-b080-two-chamber-crossing-v1.json", "505846925694811b8f34b6c48120b56b406e15eb9e7e1a044e7763cea8d30896"),
    "prereg": (R / "docs/cycle-244-b081-constructed-abel-current-preregistration-v1.md", "d272dac4a7858eda8d7c08685f32f69b5848f69fe5410cfd9b923439ce8cffda"),
    "replay": (R / "proof/verify_cycle_244_constructed_abel_current.py", "3bddd8d8160e48d80db67a6d222506f2d2fc648699b739b8fa153afad3e5f95b"),
    "test": (R / "tests/test_cycle_244_constructed_abel_current.py", "c30aff735e03384bfde9137e527b924f91ac5790bb75a0b14e6b4bcccf4b60b2"),
    "validator": (R / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
    "scaffold": (R / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload():
    result = audit()
    require(result["boundary"]["locally_finite"], "unearned boundary current")
    require(not result["normalization_ambiguity"]["intrinsic_regulator_normalization_available"], "unearned normalization")
    return {"artifact_id": "cycle-244-b081-constructed-abel-current-v1", "cycle": 244, "budget_ordinal": "B081", "epistemic_status": "PROVED", "status": "SEALED_CONSTRUCTED_LOCAL_FINITE_CURRENT_NONCANONICAL", "claim_boundary": "The constructed Galois-equivariant 12-dissected A-residual current has a locally finite rho-to-one distributional boundary but no intrinsic lambda^N regulator normalization. It is not source-authorized and proves no contour identity, mixed-base transform, B-Fourier covariance, AFK, fusion, Stark, or TCC.", "audit": result, "companion_decision": {"identity": "/root/decision_companion_2", "recommendation": "Seal C244 only for the constructed locally finite boundary and lambda^N nonuniqueness.", "known_flaw": "No source authorization, intrinsic coefficient normalization, temperedness, or A-to-C contour identity.", "falsifier": "Any trace/norm, properness, 11-class, Galois, boundary, bump, lambda-axiom, or replay discrepancy.", "next_action": "Derive actual A-word principal coefficients and their recurrence/growth.", "adopted": True}, "frozen_hashes": freeze_inputs(R, I), "runtime": check_runtime("C244"), "sealer": {"path": "proof/build_cycle_244_constructed_abel_current_v1.py", "sha256": sha256(Path(__file__))}}


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=O, payload_factory=payload))
