"""Seal C243/B080 finite-residue two-chamber contour containment."""
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_243_two_chamber_crossing import audit


R = Path(__file__).resolve().parents[1]
O = R / "artifacts/cycle-243-b080-two-chamber-crossing-v1.json"
I = {
    "prior_c228": (R / "artifacts/cycle-228-b065-f3-square-residual-block-v1.json", "2078970c02c1f1359de25394f57c9229dab4fef01c15894bc36b1ea177deafe4"),
    "prior_c229": (R / "artifacts/cycle-229-b066-f3-square-divisor-v1.json", "2a38f5332e40a8e07dae28027ad554426ca8a1d4f1d6e0ff8f83c2a44cc2ab69"),
    "prior_c242": (R / "artifacts/cycle-242-b079-minkowski-common-contour-v1.json", "9f8b8d4093dc6159761c36c346956d297638b4afadc3f997a05cce40b86584bd"),
    "prereg": (R / "docs/cycle-243-b080-two-chamber-crossing-preregistration-v1.md", "8470a740c792d688fedb2934d325e4bec55c0339634f5af040b630ab7385b5fd"),
    "replay": (R / "proof/verify_cycle_243_two_chamber_crossing.py", "65b4a813bce22c072833733014639486d5bbb6afdee64e98bcb939df465c1677"),
    "test": (R / "tests/test_cycle_243_two_chamber_crossing.py", "f6e09bfc0af1fe50fc0aefc70a4fe7c35be2a2a1d1a4e70a272068c8dd45b387"),
    "validator": (R / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
    "scaffold": (R / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload():
    result = audit()
    require(not result["finite_residue_ledger_available"], "unearned finite-ledger containment")
    return {
        "artifact_id": "cycle-243-b080-two-chamber-crossing-v1",
        "cycle": 243,
        "budget_ordinal": "B080",
        "epistemic_status": "PROVED",
        "status": "SEALED_FINITE_RESIDUE_TWO_CHAMBER_CONTAINMENT",
        "claim_boundary": "Every frozen continuous affine-normal A-to-C deformation crosses an infinite uncancelled C228 divisor family, so no finite Picard-Lefschetz-style residue ledger exists. This does not exclude Abel/zeta-renormalized infinite residues, nonlinear or otherwise regularized contours, a mixed-base identity, AFK, fusion, Stark, or TCC.",
        "audit": result,
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "recommendation": "Seal C243/B080 as PROVED only for the frozen continuous two-chamber deformation with a finite residue ledger.",
            "known_flaw": "The infinite family does not exclude an Abel/zeta-renormalized residue sum or nonlinear/differently regularized contours.",
            "falsifier": "Any wall location, mu_N family, side-change orientation, eight-factor zero audit, 12-divisibility condition, multiplicity, infinitude, or replay discrepancy.",
            "next_action": "Test a source-defined Abel-weighted 12-dissected wall-crossing sum and its rho-to-one continuation.",
            "adopted": True,
        },
        "frozen_hashes": freeze_inputs(R, I),
        "runtime": check_runtime("C243"),
        "sealer": {"path": "proof/build_cycle_243_two_chamber_crossing_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=O, payload_factory=payload))
