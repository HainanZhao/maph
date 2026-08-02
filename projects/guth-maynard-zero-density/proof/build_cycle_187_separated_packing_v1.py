#!/usr/bin/env python3
"""Seal Cycle 187 separated weighted-packing local no-go."""
from __future__ import annotations

from pathlib import Path
import sys
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = ROOT.parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))
from tools.preregistration_check import extract_manifest, validate_preregistration  # noqa: E402


SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-187-separated-packing-v1.json"
PREFLIGHT_VALIDATOR = REPOSITORY_ROOT / "tools/preregistration_check.py"
PREFLIGHT_VALIDATOR_HASH = "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-187-separated-packing-preregistration-v1.md", "2a2ec9aba8d9540ee26a1b387c9f89275bb26ab3c1432e68ac7b05f6ea5227bd"),
    "document": (ROOT / "docs/cycle-187-separated-packing-v1.md", "e0d5c99e7ef19c5dcbb42a519a9394d91dd7c83042bccf0cc07dd723f04918dc"),
    "conventions": (ROOT / "conventions/separated_packing_v1.py", "f85f0e49138c4c1008136e46b4e15b03a708b4768e1acb8db1dc2e86d04ef226"),
    "tests": (ROOT / "tests/test_cycle_187_separated_packing_v1.py", "02a11c88f4059e72244547406c7f23185b4e81cf7a195916729556140128dd5f"),
    "cycle185_correction": (ROOT / "artifacts/cycle-185-three-label-curvature-convention-correction-v1.json", "aa00a6f2da56eeaeab6fb765333fce696bb085f6e91df4d240d881bb99303a1e"),
    "cycle186": (ROOT / "artifacts/cycle-186-actual-curve-convexity-v1.json", "7b73391ad91bed211c0c99e86fdc6857edb8f56d34a24c6f06cf05555d723422"),
    "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
}


def exact_json(value: object) -> object:
    if isinstance(value, tuple):
        return [exact_json(item) for item in value]
    if isinstance(value, dict):
        return {str(key): exact_json(item) for key, item in value.items()}
    if isinstance(value, list):
        return [exact_json(item) for item in value]
    return value


def preflight() -> dict[str, object]:
    require(sha256(PREFLIGHT_VALIDATOR) == PREFLIGHT_VALIDATOR_HASH, "preflight validator hash mismatch")
    checked = validate_preregistration(INPUTS["preregistration"][0], expected_cycle=187, enforce_manifest_head=False)
    require("T=3^(2k)" in checked["parameters"]["power_ledger"]["value"], "aligned scale ledger absent")
    manifest = extract_manifest(INPUTS["preregistration"][0])
    require(any("separation multiplier" in item for item in manifest["formula_families"]), "separated support family absent")
    return {
        "schema": checked["schema"], "cycle": checked["cycle"],
        "manifest_sha256": checked["manifest_sha256"], "input_hashes": checked["input_hashes"],
        "parameters": checked["parameters"],
    }


def exact_checks() -> dict[str, object]:
    module = __import__("conventions.separated_packing_v1", fromlist=["verify_all"])
    rows = module.verify_all()
    ledger = rows["samples"]["separated_occupancy_k1"]
    require(8 * ledger["mass"]["ordered_cross_mass"] >= ledger["mass"]["critical_target"], "critical mass replay")
    require(ledger["support"]["minimum_pairwise_separation"] > ledger["parameters"]["T"], "separation replay")
    return exact_json(rows)


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle185_correction"][0], "SEALED_CORRECTION_SHIFTED_EXPONENTIAL_CURVATURE_AND_ORIGINAL_CLAIM_WITHHELD")
    validate_prior(INPUTS["cycle186"][0], "SEALED_ACTUAL_CURVE_LOCAL_CONVEXITY_GRID_EXCLUSION")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="separated_packing_v1")
    return {
        "artifact_id": "cycle-187-separated-packing-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_SEPARATED_WEIGHTED_LOCAL_PACKING_NO_GO",
        "claim_boundary": "This proves that the present mass/capacity/shell ledger plus C186-scale local spacing cannot force a critical-box saving. It is non-exponential and proves no analytic counterexample, recurrence, density gain, or interval result.",
        "runtime": check_runtime("Cycle 187"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "preflight_validator": {"path": "../../tools/preregistration_check.py", "sha256": PREFLIGHT_VALIDATOR_HASH},
        "preregistration_preflight": preflight(),
        "local_packing_result": {"epistemic_status": "PROVED", **exact_json(theorem)},
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "A future E13 continuation needs a global actual-exponential distribution theorem across separated labels or denominator windows; local triple exclusion and weighted occupancy alone are exhausted."},
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "preflight_command": "research prereg check docs/cycle-187-separated-packing-preregistration-v1.md --expected-cycle 187",
            "write_command": "python3 proof/build_cycle_187_separated_packing_v1.py --write",
            "check_command": "python3 proof/build_cycle_187_separated_packing_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_187_separated_packing_v1.py",
        },
        "exact_replay": exact_checks(),
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 187", output=OUTPUT, payload_factory=seal))
