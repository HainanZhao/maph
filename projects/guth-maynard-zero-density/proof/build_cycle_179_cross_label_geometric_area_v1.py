#!/usr/bin/env python3
"""Seal Cycle 179 exact-rational tower and affine-area reduction."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-179-cross-label-geometric-tower-and-area-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-179-cross-label-geometric-tower-preregistration-v1.md", "d6c5d6628a8d6f4f53c26cea7846ac3710ca513317009fd9c81cee34c56ec8df"),
    "document": (ROOT / "docs/cycle-179-cross-label-geometric-tower-v1.md", "ae8eae9d5a8193df3242d76cd1d6445166979789e3a847d2760bf3f91bb3134c"),
    "conventions": (ROOT / "conventions/cross_label_geometric_area_v1.py", "f62d178d97efa4613a0de9ff5f436c0ec01325674e6f5a9be4d77931467f7ce5"),
    "tests": (ROOT / "tests/test_cycle_179_cross_label_geometric_area_v1.py", "07b7ca09ca97fe1ac1de89f4251dd742cfb39a223d27f2e0324cc6b44cd3e5fb"),
    "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "cycle63": (ROOT / "artifacts/cycle-63-log-transport-census-v1.json", "d5dc9dd9ff3f5636c98980d35f6f973d72f9e62c04644fe510b4f0de06d4f153"),
    "cycle178": (ROOT / "artifacts/cycle-178-diagonal-aware-fibre-extraction-v1.json", "72797b1e97002d532b7bff28305330cea6f35f2b0e3192b87f7fb4adf99b0e9a"),
    "cycle178_normalization": (ROOT / "artifacts/cycle-178-diagonal-aware-fibre-extraction-v1-normalization-correction.json", "0ab43286aa7bcdbe16a803e31242cd57f48b342610e47e9eeb6277d20908cba9"),
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
    module = __import__("conventions.cross_label_geometric_area_v1", fromlist=["verify_all"])
    rows = module.verify_all()
    samples = rows["samples"]
    require(samples["Bezout_recovery"]["recovered_base"] == Fraction(3, 2), "gcd compression")
    require(samples["integral_tower"]["ordered_cross_label_mass"] <= samples["integral_tower"]["uniform_cross_bound"], "integral base")
    require(samples["area"]["beta"] == Fraction(1, 2) and samples["area"]["area_error"] == 0, "nonzero-beta cancellation")
    require(samples["population"]["oriented_cross_label_triangles"] == 108, "triangle population")
    return exact_json(rows)


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle63"][0], "SEALED_LOG_TRANSPORT_PAIR_CENSUS_LT_17_25_OPEN")
    validate_prior(INPUTS["cycle178"][0], "SEALED_FIXED_BETA_HEAVY_FIBRE_SEEDED_PACKET_OR_CROSS_LABEL_REMAINDER")
    validate_prior(INPUTS["cycle178_normalization"][0], "SEALED_ORDERED_CROSS_LABEL_NORMALIZATION_CORRECTION")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="cross_label_geometric_area_v1")
    return {
        "artifact_id": "cycle-179-cross-label-geometric-tower-and-area-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_EXACT_RATIONAL_CROSS_LABEL_NO_GO_AND_AFFINE_AREA_RESONANCE_REDUCTION",
        "claim_boundary": "This proves exact-rational beta-zero cross-label towers are subcritical and reduces a light-branch direct-census failure to many labelled approximate affine-area resonances. It proves no upper bound for that area census, no aggregate recurrence, density gain, or interval result.",
        "runtime": check_runtime("Cycle 179"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "exact_rational_gcd_compression": {"epistemic_status": "PROVED", **exact_json(theorem)},
        "exact_rational_no_go": {
            "epistemic_status": "PROVED",
            "statement": "Every finite exact-rational positive-exponential label set compresses to one rational base u/v. At beta zero with exact rows, its ordered cross-label mass is O(H^2)=X^(22/25), so it cannot saturate the Cycle-178 X^(32/25) cross-label scale.",
        },
        "affine_area_reduction": {
            "epistemic_status": "PROVED",
            "statement": "Two actual rows at ell and one at m!=ell give an integer A with |A-h3(h2-h1)(alpha_ell-alpha_m)|<=2CH/X. In the Cycle-178 light branch, T>=X^(16/25) and X>=2^25 force at least X^(32/25)/4 ordered such triangles.",
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Bound the coefficient-preserving labelled affine-area resonance census, or construct a realized approximate cross-label saturator. Exact rational roots and independent same-label packets are no longer admissible obstruction candidates.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "exact_replay": exact_checks(),
        "replay": {
            "write_command": "python3 proof/build_cycle_179_cross_label_geometric_area_v1.py --write",
            "check_command": "python3 proof/build_cycle_179_cross_label_geometric_area_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_179_cross_label_geometric_area_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 179", output=OUTPUT, payload_factory=seal))
