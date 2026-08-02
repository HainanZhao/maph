#!/usr/bin/env python3
"""Seal Cycle 177 actual positive-exponential rational-root saturator."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-177-actual-curve-rational-root-saturator-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-177-actual-curve-census-preregistration-v1.md", "34969772328ce8b5c816d01ad70306d99d35013c338ad2103898b4f2f42085c0"),
    "document": (ROOT / "docs/cycle-177-actual-curve-census-v1.md", "b4ed10cf48bdbf21eb3d4fc072a5c828d1445ef189584cb7c199db28a91458ad"),
    "conventions": (ROOT / "conventions/actual_curve_rational_root_saturator_v1.py", "cf62665f7d316ebc67aefeda16aad8b984a972b40f21a039d9df8f5400001c04"),
    "sanity_scan": (ROOT / "discovery/cycle_177_actual_curve_rational_root_scan_v1.py", "e195abaad3b7c0ca5dd91f4b1e1fa4fdd9e909995dc88da1569a73d6d66058f0"),
    "tests": (ROOT / "tests/test_cycle_177_actual_curve_rational_root_saturator_v1.py", "b9949f868c6190ce3933e401372e3334c4fd22ceb6a74197feebbb08287fc1bc"),
    "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "cycle63": (ROOT / "artifacts/cycle-63-log-transport-census-v1.json", "d5dc9dd9ff3f5636c98980d35f6f973d72f9e62c04644fe510b4f0de06d4f153"),
    "cycle64": (ROOT / "artifacts/cycle-64-farey-packet-transport-v1.json", "60a78bc81f2916e594221a1258a35024b96e67ecf5d2af6bc9a53731d1cdc76f"),
    "cycle65": (ROOT / "artifacts/cycle-65-depth-packet-ledger-v1.json", "f86cecfa996a7583990a24a6060167a700fa8cca54c199ec92cdf2f3c8637a2d"),
    "cycle67": (ROOT / "artifacts/cycle-67-seeded-packet-recurrence-v1.json", "85bd999fca3e1d675c0b3096a6cd287866d9e1aef227239b42b94b39ff585d02"),
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
    module = __import__("conventions.actual_curve_rational_root_saturator_v1", fromlist=["verify_all"])
    rows = module.verify_all()
    ledger = rows["exponents"]
    require(ledger["pair_target_gap"] == Fraction(1, 5), "raw pair gap")
    require(ledger["triple_target_gap"] == Fraction(1, 5), "triple gap")
    require(ledger["packet_depth_surplus"] == Fraction(1, 5), "packet depth")
    require(module.pair_weight(80, 5) >= module.pair_lower_bound(80, 5), "integer pair lower bound")
    require(module.seeded_packet(80, 5)["row_count"] == 9, "seeded central fan")
    return exact_json(rows)


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle63"][0], "SEALED_LOG_TRANSPORT_PAIR_CENSUS_LT_17_25_OPEN")
    validate_prior(INPUTS["cycle64"][0], "SEALED_LOG_FAREY_PACKET_MASS_OR_LOW_DENOMINATOR_RECURRENCE_OPEN")
    validate_prior(INPUTS["cycle65"][0], "SEALED_LOG_DEPTH_PACKET_DISCREPANCY_OR_X6_25_AP_RECURRENCE_OPEN")
    validate_prior(INPUTS["cycle67"][0], "SEALED_SEEDED_X6_25_AP_RECURRENCE_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="actual_curve_rational_root_saturator_v1")
    return {
        "artifact_id": "cycle-177-actual-curve-rational-root-saturator-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_ACTUAL_POSITIVE_EXPONENTIAL_RAW_PAIR_CENSUS_SATURATOR",
        "claim_boundary": "This proves a continuous-scale actual-positive-exponential rational-root family with raw Cycle-63 pair mass X^(22/25-o(1)). It disproves the uniform raw pair target X^(17/25+o(1)), but does not bound or refute the full fixed-beta triple census, prove a density gain, or prove an interval result.",
        "runtime": check_runtime("Cycle 177"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "rational_root_saturator": {"epistemic_status": "PROVED", **exact_json(theorem)},
        "raw_pair_no_go": {
            "epistemic_status": "PROVED",
            "statement": "For every fixed 0<c<1, a fixed rational root r and the continuous subsequence Delta_L=2*pi*L/log(1+1/r), X_L=Delta_L^(5/3) give an admissible label ell=L with P>>_c X_L^(22/25), so an unqualified uniform raw pair bound below X^(17/25) is false.",
        },
        "structured_exception": {
            "epistemic_status": "PROVED",
            "statement": "At beta=0 the constructed label has X^(11/25+o(1)) exact triple rows and a central exact seeded q=r,a=1 packet of depth X^(11/25+o(1)); this is a one-label structured exception, not a lower bound for the complete triple census.",
        },
        "sanity_scan": {
            "epistemic_status": "RECOGNIZED",
            "statement": "The frozen 100-decimal scan on r in {1,2,3,5,8} and L in {10,100,1000} found every prescribed rational-root label inside the c=1/4 chart and no failed multiplier; the scan is not used for the proof.",
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Replace the raw pair route by a diagonal-aware direct triple census after extracting heavy seeded packets, or prove a heavy-actual-packet-to-seeded-recurrence theorem strong enough for E7/E9. Any further pair statistic must exclude or explicitly retain same-label rational-root rays.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "exact_replay": exact_checks(),
        "replay": {
            "write_command": "python3 proof/build_cycle_177_actual_curve_rational_root_saturator_v1.py --write",
            "check_command": "python3 proof/build_cycle_177_actual_curve_rational_root_saturator_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_177_actual_curve_rational_root_saturator_v1.py",
            "discovery_command": "python3 discovery/cycle_177_actual_curve_rational_root_scan_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 177", output=OUTPUT, payload_factory=seal))
