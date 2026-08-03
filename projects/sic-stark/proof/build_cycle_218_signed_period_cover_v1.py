#!/usr/bin/env python3
"""Seal Cycle 218/B055's signed-period product-domain containment."""
from __future__ import annotations
from pathlib import Path
from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_218_signed_period_cover import run as cover_run

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-218-b055-signed-period-cover-v1.json"
INPUTS = {
    "prior_raw_groupoid": (ROOT / "artifacts/cycle-217-b054-source-transformation-groupoid-v1.json", "0b2a9562158499eff4bc26c5d85bdb81dc1b57c5d7fd689859f8be7f39f6a75a"),
    "preregistration": (ROOT / "docs/cycle-218-b055-signed-period-cover-preregistration-v1.md", "530b968eed1843ca72e7e8f5430c5126d8edb1d1c42d46d624efeefb76ad733f"),
    "replay": (ROOT / "proof/verify_cycle_218_signed_period_cover.py", "8fca003418e205595fa2474449574b7e2577a59e768d065df1eb663ccff7ddb3"),
    "regression_test": (ROOT / "tests/test_cycle_218_signed_period_cover.py", "baae7badf4918083e4c4349af0f77d70372bb088bda4f1f2d11401ae8144caa4"),
    "prototype": (ROOT / "discovery/cycle-218-b055-signed-period-cover-prototype-v1.json", "93a8058e9b77f085c45439605b4a2505b270e0d25c4311668662fc0cc9beacdf"),
    "source_audit": (ROOT / "scripts/dimension_six_ss_evaluation_audit.py", "24c9258e46a1233c552017f3b58de0d45acd0197c8c807579f090ca1332f626f"),
    "source_paper": (ROOT / "paper/sic-stark-dimension-six-boundary-fusion.tex", "347228e05a87946ca41bb31c118aae069b7fb6002fff4933d030a153cef21cb7"),
    "validator": (ROOT / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    frozen = freeze_inputs(ROOT, INPUTS)
    result = cover_run()
    scaling, swap = result["positive_scaling_audit"], result["swap_reindexing_audit"]
    sign, lift = result["signed_representative_domain_audit"], result["legal_lift_audit"]
    require(scaling["scale"] == 576, "scaling drift")
    require(swap["all_delta_sets_reindexed"], "swap census drift")
    require(not sign["raw_k_in_source_product_domain"], "domain drift")
    require(not lift["complete_raw_to_E_lift_available"], "lift scope drift")
    return {
        "artifact_id": "cycle-218-b055-signed-period-cover-v1", "cycle": 218, "budget_ordinal": "B055",
        "epistemic_status": "PROVED", "status": "SEALED_SIGNED_PERIOD_PRODUCT_DOMAIN_CONTAINMENT",
        "claim_boundary": result["claim_boundary"],
        "outcome": {"epistemic_status": "PROVED", "statement": "Positive scaling and finite swap relabeling are exact partial product laws, but the raw k=-24 state lies outside the source-defined product domain and cannot be lifted by convention."},
        "positive_scaling_audit": scaling, "swap_reindexing_audit": swap,
        "signed_representative_domain_audit": sign, "legal_lift_audit": lift,
        "gate_outcome": result["gate_outcome"],
        "companion_decision": {"identity": "/root/decision_companion_2", "evidence_scope_review": "C218 proves positive 576-scaling within the k>0 Gamma_M domain and complete 24-label Delta swap relabeling, while the raw k=-24 endpoint lies outside the frozen product definitions.", "recommendation": "Seal C218 as completed product-domain containment and open a new cycle; defining k<0 changes the function's domain and requires a new construction.", "known_flaw": "The result does not exclude a consistent signed-k extension or another source theorem supplying sign, ordering, normalization, and branch factors.", "falsifier": "Any k-domain, scaling homogeneity, Delta-set census, pr congruence, label map, normalization scope, raw/target sign, or replay discrepancy invalidates the seal.", "next_action": "Open a signed-k extension cycle at k=plus-or-minus 24, requiring agreement with k>0 products, involutivity, reflection, shifts, and both factorization identities; only after existence/uniqueness retest the affine state and cocycle.", "adopted": True, "reason": "A negative-k definition is a distinct construction, not an admissible reparameterization of the sealed source domain."},
        "preregistration_preflight": {"cycle": 218, "manifest_sha256": sha256(ROOT / "docs/cycle-218-b055-signed-period-cover-preregistration-v1.md"), "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"}},
        "frozen_hashes": frozen,
        "replay": {"preflight_command": "research prereg check docs/cycle-218-b055-signed-period-cover-preregistration-v1.md --expected-cycle 218 --allow-head-drift", "prototype_command": "python3 proof/verify_cycle_218_signed_period_cover.py --output discovery/cycle-218-b055-signed-period-cover-prototype-v1.json", "test_command": "python3 -m unittest tests/test_cycle_218_signed_period_cover.py", "write_command": "python3 proof/build_cycle_218_signed_period_cover_v1.py --write", "check_command": "python3 proof/build_cycle_218_signed_period_cover_v1.py --check"},
        "runtime": check_runtime("Cycle 218 seal"), "sealer": {"path": "proof/build_cycle_218_signed_period_cover_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
