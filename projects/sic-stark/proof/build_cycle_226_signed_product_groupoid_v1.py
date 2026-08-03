#!/usr/bin/env python3
"""Seal Cycle 226/B063's four-node signed-product groupoid containment."""
from __future__ import annotations

from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_226_signed_product_groupoid import run as groupoid_run


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-226-b063-signed-product-groupoid-v1.json"
INPUTS = {
    "prior_local_branch": (
        ROOT / "artifacts/cycle-225-b062-reflection-root-branch-v1.json",
        "34b7d4943566e57f8c153127449226ec3eae4865f692f17336f6e4f5a3c9c29f",
    ),
    "preregistration": (
        ROOT / "docs/cycle-226-b063-signed-product-groupoid-preregistration-v1.md",
        "32e85ff9b91ace04aa406e6d22bea27631bb3b174614f4c471b45945d1a20727",
    ),
    "replay": (
        ROOT / "proof/verify_cycle_226_signed_product_groupoid.py",
        "51eb9d4f07b7c6a2a19ac4229d84badac876adfa0ca394a1cf2d5b2a5a5132b9",
    ),
    "regression_test": (
        ROOT / "tests/test_cycle_226_signed_product_groupoid.py",
        "8835a045f28ef63878ce1441a5d8052a0778901c0cf23d433d7a83da9ddde96f",
    ),
    "prototype": (
        ROOT / "discovery/cycle-226-b063-signed-product-groupoid-prototype-v1.json",
        "a82eb5344934036a58f46ddc70e1f1293c573ef88497bcc895dfe05b65b9f879",
    ),
    "prior_groupoid": (
        ROOT / "proof/verify_cycle_217_source_transformation_groupoid.py",
        "e038ffb0d9ab95d4eb6edfbf99eaf8ddbb046ba52fa46b8cb84b4c2bdeb3b465",
    ),
    "source_audit": (
        ROOT / "scripts/dimension_six_ss_evaluation_audit.py",
        "24c9258e46a1233c552017f3b58de0d45acd0197c8c807579f090ca1332f626f",
    ),
    "source_paper": (
        ROOT / "paper/sic-stark-dimension-six-boundary-fusion.tex",
        "347228e05a87946ca41bb31c118aae069b7fb6002fff4933d030a153cef21cb7",
    ),
    "validator": (
        ROOT / "../../tools/preregistration_check.py",
        "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
    ),
    "scaffold": (
        ROOT / "proof/cycle_seal_v1.py",
        "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1",
    ),
}


def payload() -> dict[str, object]:
    frozen = freeze_inputs(ROOT, INPUTS)
    result = groupoid_run()
    edges = result["edge_inventory"]
    loops = result["raw_loop_audit"]
    boundary = result["construction_boundary_audit"]
    require(edges["directed_edge_count"] == 8, "edge census drift")
    require(edges["source_defined_edge_count"] == 4, "source product-domain census drift")
    require(edges["formal_negative_k_edge_count"] == 4, "negative-k edge census drift")
    require(all(not row["residuals_scalarized"] for row in edges["edges"]), "ordinary-gamma residual lost")
    require(loops["loop_count"] == 12, "raw loop census drift")
    require(loops["augmented_closed_loop_count"] == 0, "unearned augmented loop closure")
    require(not boundary["signed_product_groupoid_constructed"], "unearned signed-product groupoid")
    return {
        "artifact_id": "cycle-226-b063-signed-product-groupoid-v1",
        "cycle": 226,
        "budget_ordinal": "B063",
        "epistemic_status": "PROVED",
        "status": "SEALED_FOUR_NODE_SIGNED_PRODUCT_GROUPOID_CONTAINED",
        "claim_boundary": result["claim_boundary"],
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": "The four raw F2/F3 nodes do not support the preregistered state-complete signed-product groupoid: four edges lack a source-defined negative-k product input and none of the twelve raw loops closes after period, affine-argument, and label transport.",
        },
        "edge_inventory": edges,
        "raw_loop_audit": loops,
        "construction_boundary_audit": boundary,
        "gate_outcome": result["gate_outcome"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "evidence_scope_review": "The complete eight-edge inventory, all retained ordinary-gamma residuals, positive-versus-negative product-domain boundary, full twelve-loop period/argument/label transport, and the formal-versus-source distinction were reviewed together.",
            "recommendation": "Seal C226/B063 as PROVED only for containment of the frozen four-node raw-state groupoid; its authorized edges are incomplete and its formal matrix loops do not close in augmented state.",
            "known_flaw": "The negative-k transitions are formal diagnostics, not source identities, and nonclosure on four raw nodes does not exclude closure after adjoining period-scale, affine-argument, label, and residual-factor states.",
            "falsifier": "Any F2/F3 state map, authorized-edge domain, residual-factor transcription, period/argument/label transport, twelve-loop census, formal-versus-source distinction, or replay discrepancy invalidates the seal.",
            "next_action": "Open an enlarged semigroup/groupoid cycle deriving normal forms for the augmented period and affine actions—quotienting only by already proved positive scaling—then test whether reflection/swap identities close the 576-scaled loops before assigning any edge cocycle.",
            "adopted": True,
            "reason": "The raw graph is not the functional state space required by the factorization formulas; the next construction must first supply that larger state space rather than fit cochains to raw matrix loops.",
        },
        "preregistration_preflight": {
            "cycle": 226,
            "manifest_sha256": sha256(ROOT / "docs/cycle-226-b063-signed-product-groupoid-preregistration-v1.md"),
            "validator": {
                "path": "../../tools/preregistration_check.py",
                "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
            },
        },
        "frozen_hashes": frozen,
        "replay": {
            "preflight_command": "research prereg check docs/cycle-226-b063-signed-product-groupoid-preregistration-v1.md --expected-cycle 226 --allow-head-drift",
            "prototype_command": "python3 proof/verify_cycle_226_signed_product_groupoid.py --output discovery/cycle-226-b063-signed-product-groupoid-prototype-v1.json",
            "test_command": "python3 -m unittest tests/test_cycle_226_signed_product_groupoid.py",
            "write_command": "python3 proof/build_cycle_226_signed_product_groupoid_v1.py --write",
            "check_command": "python3 proof/build_cycle_226_signed_product_groupoid_v1.py --check",
        },
        "runtime": check_runtime("Cycle 226 seal"),
        "sealer": {
            "path": "proof/build_cycle_226_signed_product_groupoid_v1.py",
            "sha256": sha256(Path(__file__)),
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
