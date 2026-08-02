#!/usr/bin/env python3
"""Seal Cycle 178 diagonal-aware actual-fibre extraction."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-178-diagonal-aware-fibre-extraction-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-178-diagonal-aware-fibre-preregistration-v1.md", "8d1ed887248f3cbcd6690a5ab3b08f41512bfb4fed6245a479b30188c2c9bbc7"),
    "document": (ROOT / "docs/cycle-178-diagonal-aware-fibre-extraction-v1.md", "69f3c797562238203956464017882df7a464a37ff86cfe953852090d71a839ba"),
    "conventions": (ROOT / "conventions/diagonal_aware_fibre_extraction_v1.py", "be26b6e997ce7edf3287015855afc35c514560519108d6befce1e62d4e34e821"),
    "tests": (ROOT / "tests/test_cycle_178_diagonal_aware_fibre_extraction_v1.py", "980ca4b1f3ddb078dc0dafb73e736d47e36ae579404ee7a3829aa72243705f39"),
    "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "cycle63": (ROOT / "artifacts/cycle-63-log-transport-census-v1.json", "d5dc9dd9ff3f5636c98980d35f6f973d72f9e62c04644fe510b4f0de06d4f153"),
    "cycle67": (ROOT / "artifacts/cycle-67-seeded-packet-recurrence-v1.json", "85bd999fca3e1d675c0b3096a6cd287866d9e1aef227239b42b94b39ff585d02"),
    "cycle177": (ROOT / "artifacts/cycle-177-actual-curve-rational-root-saturator-v1.json", "3bbe563ec6bac8e67f2bc0ef6f00d4f0b250af467aa14d144e3757254cd64ed1"),
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
    module = __import__("conventions.diagonal_aware_fibre_extraction_v1", fromlist=["verify_all"])
    rows = module.verify_all()
    positive = rows["samples"]["positive"]
    nonfirst = rows["samples"]["nonfirst_minimum"]
    zero = rows["samples"]["zero_numerator"]
    light = rows["samples"]["light"]
    require(positive["primitive_packet"]["q"] == 5 and positive["primitive_packet"]["a"] == 1, "positive branch")
    require(nonfirst["minimum_gap"]["left_row_index"] == 1 and nonfirst["seed"]["h"] == 20, "minimum-gap anchor")
    require(zero["primitive_packet"]["a"] == 0 and zero["primitive_packet"]["q"] == 1, "zero numerator retained")
    require(light["ordered_cross_label_mass"] == light["light_cross_lower_bound"], "sharp light diagonal example")
    return exact_json(rows)


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle63"][0], "SEALED_LOG_TRANSPORT_PAIR_CENSUS_LT_17_25_OPEN")
    validate_prior(INPUTS["cycle67"][0], "SEALED_SEEDED_X6_25_AP_RECURRENCE_OPEN")
    validate_prior(INPUTS["cycle177"][0], "SEALED_ACTUAL_POSITIVE_EXPONENTIAL_RAW_PAIR_CENSUS_SATURATOR")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="diagonal_aware_fibre_extraction_v1")
    return {
        "artifact_id": "cycle-178-diagonal-aware-fibre-extraction-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_FIXED_BETA_HEAVY_FIBRE_SEEDED_PACKET_OR_CROSS_LABEL_REMAINDER",
        "claim_boundary": "This proves an exact inverse from one heavy actual fixed-beta fibre to a primitive seed-and-error-preserving Cycle-67 packet, and a heavy/light cross-label decomposition. It proves no cross-label analytic estimate, E7/E9 skeleton bound, density gain, or interval result.",
        "runtime": check_runtime("Cycle 178"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "actual_fibre_inverse": {"epistemic_status": "PROVED", **exact_json(theorem)},
        "critical_dichotomy": {
            "epistemic_status": "PROVED",
            "statement": "For R=ceil(X^(6/25)), either N_ell>=2R+1 at some label and the actual fibre supplies a seeded packet of depth at least R, or every N_ell<=2R and U_cross=sum_(ell!=ell')N_ell N_ell' is at least T(T-2R). For X>=256, a direct-target failure T>=X^(16/25) in the light branch gives U_cross>=X^(32/25)/2.",
        },
        "cycle177_routing": {
            "epistemic_status": "PROVED",
            "statement": "The Cycle-177 rational-root ray is a heavy same-label fibre and routes to the seeded-packet branch; it is not cross-label mass.",
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Prove a coefficient-preserving upper bound for the retained cross-label mass, or construct a genuine actual positive-exponential cross-label saturator. The combinatorial dichotomy alone is not an E13 advance.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "exact_replay": exact_checks(),
        "replay": {
            "write_command": "python3 proof/build_cycle_178_diagonal_aware_fibre_extraction_v1.py --write",
            "check_command": "python3 proof/build_cycle_178_diagonal_aware_fibre_extraction_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_178_diagonal_aware_fibre_extraction_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 178", output=OUTPUT, payload_factory=seal))
