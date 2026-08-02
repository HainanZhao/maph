#!/usr/bin/env python3
"""Seal Cycle 110 perfect-power primitive-split summability."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import (
    check_runtime,
    freeze_inputs,
    load_record,
    require,
    run_cli,
    sha256,
    validate_prior,
)


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-110-perfect-power-split-sum-v1.json"
INPUTS = {
    "discovery_candidate": (ROOT / "discovery/cycle-110-perfect-power-split-candidate-v1.md", "0e9692107c814e359fef715404810089b7b0dfa269f8deb09ad97c7bd7c7bac1"),
    "preregistration": (ROOT / "docs/cycle-110-perfect-power-split-preregistration-v1.md", "f1d09ed297aacca521bc2546c344a4c0f0f43213f0077e971e285389c383cda2"),
    "document": (ROOT / "docs/cycle-110-perfect-power-split-sum-v1.md", "0258325c3534534a78b565fda2c23f4f87ff015a3e29724fa1eed7c7ec669c07"),
    "conventions": (ROOT / "conventions/perfect_power_split_sum_v1.py", "5fb8c7afd5af68527b7ff6ed9a0d7136e5392aee888f3c76bc7813b4c02c8ed8"),
    "tests": (ROOT / "tests/test_cycle_110_perfect_power_split_sum_v1.py", "ed881eb56205e15db9a2b0795af7cfe9ddf3134ba39a55c437af4e52f6c3b916"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle99": (ROOT / "artifacts/cycle-99-critical-rational-ray-v1.json", "69e453fea12a404c17078169ac605c17b05109b99c74e0dd82f830e1ecdf2ee6"),
    "cycle102": (ROOT / "artifacts/cycle-102-cross-valuation-inverse-v1.json", "1f4d27e5e1c269b04d3779634d6deaaa5ae21eb3f9352de781bc33b396c002ff"),
    "cycle106": (ROOT / "artifacts/cycle-106-beta-free-saturation-v1.json", "0e681ebf90d531a9564677779016642afbb73cf6c0cc47760b4b17db4b2bf3d1"),
    "cycle109": (ROOT / "artifacts/cycle-109-uniform-triple-b-v1.json", "da481a16c7a9e027d53104282410e2bad73fcaf6157a9ea3fe61ffeb8d74f432"),
}


def seal() -> dict[str, Any]:
    expected = {
        "cycle99": "SEALED_STRONG_NEAR_DOUBLE_CRITICAL_RAYS_WEAK_AND_FIBER_OPEN",
        "cycle102": "SEALED_EXACT_CROSS_VALUATION_CORE_CONDITIONAL_COLOUR_CONCENTRATION",
        "cycle106": "SEALED_UNSIGNED_ALL_SCALE_SATURATOR_BETA_PAYLOAD_LOCK",
        "cycle109": "SEALED_FULL_SMOOTH_PERFECT_POWER_SCALE_RAY_SUMMABLE",
    }
    for label, status in expected.items():
        validate_prior(INPUTS[label][0], status)
    theorem = load_record(
        root=ROOT,
        path=INPUTS["conventions"][0],
        module_name="perfect_power_split_sum_v1",
    )
    require("less than 4" in theorem["uniform_split_sum"], "uniform split bound")
    require("4*tau(W)" in theorem["degree_aggregation"], "mode aggregation")
    require("anchor prefactor" in theorem["boundary"], "normalization boundary")
    return {
        "artifact_id": "cycle-110-perfect-power-split-sum-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_PERFECT_POWER_SPLIT_WEIGHT_UNIFORMLY_SUMMABLE",
        "claim_boundary": (
            "This artifact proves a uniform bound below four for the normalized "
            "Jacobian weight over every primitive split of one perfect-power label, "
            "and a 4*tau(W) bound over all degrees at one strong mode. The common "
            "chart/anchor prefactor and nonsmooth payload remain open."
        ),
        "runtime": check_runtime("Cycle 110"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "prior_context": {
            "epistemic_status": "PROVED",
            "roles": {
                "cycle99": "injective strong critical label per signed mode",
                "cycle102": "exact primitive split and cross factors",
                "cycle106": "perfect-power coefficient formulas",
                "cycle109": "absolute summability along each actual scale ray",
            },
        },
        "split_sum_theorem": {"epistemic_status": "PROVED", **theorem},
        "finite_falsifier": {
            "epistemic_status": "OBSERVED",
            "box": "2<=d<=80, 1<=n0,r0<=12, gcd(n0,r0)=1",
            "rows": 7189,
            "maximum": 0.816496580927726,
            "witness": [3, 1, 1],
            "proof_role": "none",
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "make the chart/anchor prefactor uniform across modes and then close "
                "the irrational large-degree, weak, and simple-root branches"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_110_perfect_power_split_sum_v1.py --write",
            "check_command": "python3 proof/build_cycle_110_perfect_power_split_sum_v1.py --check",
            "test_command": (
                "python3 -m unittest tests/test_cycle_110_perfect_power_split_sum_v1.py "
                "tests/test_cycle_seal_v1.py"
            ),
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 110 sealer", output=OUTPUT, payload_factory=seal))
