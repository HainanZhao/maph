#!/usr/bin/env python3
"""Seal Cycle 180 nonzero cross-label pair determinant and product split."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-180-cross-label-pair-determinant-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-180-cross-label-pair-determinant-preregistration-v1.md", "e6ebc55b7f16c79ffca9e291d54ad51126715910604f821472ad5591fdb9099b"),
    "document": (ROOT / "docs/cycle-180-cross-label-pair-determinant-v1.md", "adfa52275997e867bdbba009be645d95a8601c7a587a7f032b92bec329441617"),
    "conventions": (ROOT / "conventions/cross_label_pair_determinant_v1.py", "0995b4243e6d0c8c9d36a28d6b70ccdbb1987f73c0cce737d6ec19bf59a5741d"),
    "tests": (ROOT / "tests/test_cycle_180_cross_label_pair_determinant_v1.py", "0cd507bb9c63d49f6ddcf1bb2a88b06b42dffa1eef76d8592885fc25d44b7fb0"),
    "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "cycle178": (ROOT / "artifacts/cycle-178-diagonal-aware-fibre-extraction-v1.json", "72797b1e97002d532b7bff28305330cea6f35f2b0e3192b87f7fb4adf99b0e9a"),
    "cycle179": (ROOT / "artifacts/cycle-179-cross-label-geometric-tower-and-area-v1.json", "384d1b55bb2bd6bb797b9b3e727fca42a7fedb06aa145d7cb4df05d30f2adef5"),
}


def exact_json(value: object) -> object:
    if isinstance(value, Fraction):
        return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    if isinstance(value, dict):
        return {str(key): exact_json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [exact_json(item) for item in value]
    return value


def exact_checks() -> dict[str, object]:
    module = __import__("conventions.cross_label_pair_determinant_v1", fromlist=["verify_all"])
    rows = module.verify_all()
    samples = rows["samples"]
    determinant = samples["determinant"]
    require(determinant["labels"] == {"left": 1, "right": 2, "absolute_gap": 1}, "retained label fields")
    require(determinant["determinant_integer"] == 2 and determinant["determinant_error"] == 0, "nonzero determinant")
    require(samples["population"]["ordered_cross_label_rectangles"] == 54, "ordered rectangle normalization")
    require(samples["low_product"]["ordered_gap_triples"] == 25, "triple-divisor replay")
    require(samples["stable"]["determinant_lower_bound"] == 10, "stable shell comparison")
    return exact_json(rows)


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle178"][0], "SEALED_FIXED_BETA_HEAVY_FIBRE_SEEDED_PACKET_OR_CROSS_LABEL_REMAINDER")
    validate_prior(INPUTS["cycle179"][0], "SEALED_EXACT_RATIONAL_CROSS_LABEL_NO_GO_AND_AFFINE_AREA_RESONANCE_REDUCTION")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="cross_label_pair_determinant_v1")
    return {
        "artifact_id": "cycle-180-cross-label-pair-determinant-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_NONZERO_CROSS_LABEL_PAIR_DETERMINANT_AND_STABLE_SHELL_REDUCTION",
        "claim_boundary": "This proves a nonzero labelled cross-pair determinant, critical light-branch rectangle population, and low-product exclusion/stable-shell reduction. It proves no upper bound for the stable shell census, no recurrence, density gain, or interval result.",
        "runtime": check_runtime("Cycle 180"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "cross_label_pair_determinant": {"epistemic_status": "PROVED", **exact_json(theorem)},
        "critical_rectangle_reduction": {
            "epistemic_status": "PROVED",
            "statement": "Under the Cycle-178 light branch and X>=2^38, T>=X^(16/25) forces at least X^(32/25)/32 ordered distinct-label rectangles. Each retains two physical pairs, has D!=0, and obeys |D-de(alpha_ell-alpha_m)|<=4CH/X.",
        },
        "low_product_exclusion": {
            "epistemic_status": "PROVED",
            "statement": "The ordered-label r*d*e<(4C/pi)HDelta/X range has O(R^2 Delta K log^2 K)=X^(28/25+o(1)) rectangles, so it cannot carry the critical population.",
        },
        "stable_shell": {
            "epistemic_status": "PROVED",
            "statement": "Every surviving stable rectangle has pi*r*d*e/Delta <= |D| <= (2pi*exp(2pi*c)+pi)*r*d*e/Delta. The remaining census must retain the complete labelled rectangle and its D/product shells.",
        },
        "mentor_checkpoint": {
            "recommendation": "APPROVE SEAL",
            "initial_flaw": "The first checkpoint asked whether D!=0 required stable-product scope.",
            "resolution": "For D=0, the exact common slope a/d=b/e and the two row-specific pair errors force |alpha_ell-alpha_m|<=4C/X, contradicting the frozen distinct-label spacing globally; no product lower bound is used.",
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Prove a coefficient-preserving upper bound for the stable nonzero-determinant shell census, or construct a nonrational actual saturator for that census. Scalar product counts, raw pairs, exact-rational towers, and low-product rectangles are non-progress.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "exact_replay": exact_checks(),
        "replay": {
            "write_command": "python3 proof/build_cycle_180_cross_label_pair_determinant_v1.py --write",
            "check_command": "python3 proof/build_cycle_180_cross_label_pair_determinant_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_180_cross_label_pair_determinant_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 180", output=OUTPUT, payload_factory=seal))
