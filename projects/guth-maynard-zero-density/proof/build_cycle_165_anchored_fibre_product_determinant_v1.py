#!/usr/bin/env python3
"""Seal Cycle 165 beta-anchored fibre-product determinant inverse."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-165-anchored-fibre-product-determinant-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-165-seed-factorization-preregistration-v1.md", "efa39f9ed9a5ccb410b820dc250e2fdea33dfae600746a9c9f227a5711b42ca2"),
    "document": (ROOT / "docs/cycle-165-seed-factorization-v1.md", "42a921d13eb1bbd810cae9c45252d317656534ddf69dfd91ea48fdf876948961"),
    "conventions": (ROOT / "conventions/anchored_fibre_product_determinant_v1.py", "311f00755fb806a9b51bb8c3b9ba6f3bacff23c9d1140980c60aae49a27925e7"),
    "tests": (ROOT / "tests/test_cycle_165_anchored_fibre_product_determinant_v1.py", "ddf5cda51a6a8dea6d28fb1ed252b416a2a832cc1dc84fda5f5ceeab439aa44a"),
    "cycle63": (ROOT / "artifacts/cycle-63-log-transport-census-v1.json", "d5dc9dd9ff3f5636c98980d35f6f973d72f9e62c04644fe510b4f0de06d4f153"),
    "cycle67": (ROOT / "artifacts/cycle-67-seeded-packet-recurrence-v1.json", "85bd999fca3e1d675c0b3096a6cd287866d9e1aef227239b42b94b39ff585d02"),
}


def exact_checks() -> dict[str, object]:
    module = __import__("conventions.anchored_fibre_product_determinant_v1", fromlist=["Anchor"])
    anchors = (
        module.Anchor(3, 5, 1, 1), module.Anchor(6, 10, 2, 2),
        module.Anchor(9, 5, 3, 1), module.Anchor(3, 15, 1, 3),
    )
    d, dp, k = module.difference_data(anchors)
    data = module.first_rank_two_data(d, dp, k)
    require(module.pair_mass((3, 2, 1)) == 11, "pair-mass identity")
    require(module.convex_four_anchor_lower(11, 3) == 2, "discrete convexity")
    require(module.determinant3(d, tuple(-entry for entry in dp), k) == 0, "determinant sign")
    require(data is not None and (data.denominator, data.numerator, data.numerator_prime) == (-30, -10, -6), "Cramer signs")
    safety = module.packet_safety(-30, -10, strip_constant=1, h_diameter=10)
    require((safety["q"], safety["a"], safety["content"]) == (3, 1, 10), "signed gcd reduction")
    require(safety["range_safe"] and safety["error_interface"], "packet safety")
    require(module.primitive_rank_one_data((3, 6, 9), (5, 10, 15), (0, 0, 0)) == (3, 5, 0, (1, 2, 3)), "rank-one resonance")
    require(module.terminal_bank(d, dp, k, high_content=7) == "rank_two_high_first_seeded_packet", "terminal routing")
    return {
        "pair_mass_example": 11,
        "balanced_four_anchor_minimum": 2,
        "rank_two_example": {"D": -30, "N": -10, "N_prime": -6},
        "signed_packet_example": {"q": 3, "a": 1, "content": 10},
        "rank_one_example": {"r": 3, "s": 5, "t": 0, "v": [1, 2, 3]},
    }


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle63"][0], "SEALED_LOG_TRANSPORT_PAIR_CENSUS_LT_17_25_OPEN")
    validate_prior(INPUTS["cycle67"][0], "SEALED_SEEDED_X6_25_AP_RECURRENCE_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="anchored_fibre_product_determinant_v1")
    return {
        "artifact_id": "cycle-165-anchored-fibre-product-determinant-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_BETA_ANCHORED_FOUR_ANCHOR_PACKET_OR_RESONANCE_PLANE_CLASSIFICATION",
        "claim_boundary": "Conditional on a critical fixed-beta Cycle-63 census, this classifies labelled four-anchor witnesses. It does not bound the census or terminal banks and proves no transport, density, or interval gain.",
        "runtime": check_runtime("Cycle 165"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "source_context": {
            "epistemic_status": "PROVED",
            "cycle63_role": "fixed-beta strip census to be bounded below the critical exponent",
            "cycle67_role": "only a high-content branch with its retained base seed may propagate a packet",
        },
        "anchored_inverse": {"epistemic_status": "PROVED", **theorem},
        "terminal_banks": {
            "epistemic_status": "PROVED",
            "statement": "The disjoint rank-one, first-high, second-high, and low-low branches retain all labelled multiplicity; one has at least a quarter of the K_(4,2) witness count.",
        },
        "contained_route": {
            "epistemic_status": "PROVED",
            "statement": "The global compact-detector C4 route does not retain the original beta and is not a Cycle-67 seed compiler.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_checks(),
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Bound every terminal bank strictly below the Cycle-63 critical census threshold, or compile a retained high-content packet into the E7/E9 skeleton with a strict margin.",
        },
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_165_anchored_fibre_product_determinant_v1.py --write",
            "check_command": "python3 proof/build_cycle_165_anchored_fibre_product_determinant_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_165_anchored_fibre_product_determinant_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 165", output=OUTPUT, payload_factory=seal))
