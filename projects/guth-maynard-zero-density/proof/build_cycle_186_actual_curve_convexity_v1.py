#!/usr/bin/env python3
"""Seal Cycle 186 actual-curve convexity grid exclusion."""
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
OUTPUT = ROOT / "artifacts/cycle-186-actual-curve-convexity-v1.json"
PREFLIGHT_VALIDATOR = REPOSITORY_ROOT / "tools/preregistration_check.py"
PREFLIGHT_VALIDATOR_HASH = "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-186-actual-curve-convexity-preregistration-v1.md", "ab2b1e9bf36e79a8fb6a656a70380132714a5e7a78f826ab63d0f00c572f91a2"),
    "document": (ROOT / "docs/cycle-186-actual-curve-convexity-v1.md", "4f60fcf8b0528b4705c930b138b20e88648f91bd98e8b7761cec5a108193f2eb"),
    "conventions": (ROOT / "conventions/actual_curve_convexity_v1.py", "3e87a79a0f9d79b582bedf6ee529e33e737db1082e74a92038466b497d699c00"),
    "tests": (ROOT / "tests/test_cycle_186_actual_curve_convexity_v1.py", "140c198e16859ce13afa4ec48455a39256acfbab5b027cbb70f0a1f37c88e23c"),
    "cycle182": (ROOT / "artifacts/cycle-182-fibre-line-rigidity-v1.json", "ec2aa8e41ea5682b8c3bcf7818d26205700121ef097cb34ef4344a03a0e593a8"),
    "cycle183": (ROOT / "artifacts/cycle-183-intercept-cleared-ray-box-v1.json", "4d74a23710ae5b48b6e0fc0ea99fc30a660c5b52efb2ef2f8179ad586dd9604f"),
    "cycle185_correction": (ROOT / "artifacts/cycle-185-three-label-curvature-convention-correction-v1.json", "aa00a6f2da56eeaeab6fb765333fce696bb085f6e91df4d240d881bb99303a1e"),
    "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
}


def exact_json(value: object) -> object:
    from fractions import Fraction
    if isinstance(value, Fraction):
        return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    if isinstance(value, dict):
        return {str(key): exact_json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [exact_json(item) for item in value]
    return value


def preflight() -> dict[str, object]:
    require(sha256(PREFLIGHT_VALIDATOR) == PREFLIGHT_VALIDATOR_HASH, "preflight validator hash mismatch")
    checked = validate_preregistration(INPUTS["preregistration"][0], expected_cycle=186, enforce_manifest_head=False)
    require(checked["parameters"]["phase"]["value"].startswith("z=exp"), "actual shifted phase absent")
    manifest = extract_manifest(INPUTS["preregistration"][0])
    require(any("weighted convexity" in item for item in manifest["formula_families"]), "convexity family absent")
    return exact_json({
        "schema": checked["schema"], "cycle": checked["cycle"],
        "manifest_sha256": checked["manifest_sha256"], "input_hashes": checked["input_hashes"],
        "parameters": checked["parameters"],
    })


def exact_checks() -> dict[str, object]:
    module = __import__("conventions.actual_curve_convexity_v1", fromlist=["verify_all"])
    rows = module.verify_all()
    regime = rows["samples"]["regime"]
    require(regime["certificate"]["status"] == "FORBIDDEN_DEEP_TRIPLE", "scale fixture did not exclude triple")
    return exact_json(rows)


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle182"][0], "SEALED_COMMON_INTERCEPT_FIBRE_LINE_RIGIDITY_AND_DENOMINATOR_CAPACITY")
    validate_prior(INPUTS["cycle183"][0], "SEALED_INTERCEPT_CLEARED_PRIMITIVE_RAY_BOX_SATURATION_CLASS")
    validate_prior(INPUTS["cycle185_correction"][0], "SEALED_CORRECTION_SHIFTED_EXPONENTIAL_CURVATURE_AND_ORIGINAL_CLAIM_WITHHELD")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="actual_curve_convexity_v1")
    return {
        "artifact_id": "cycle-186-actual-curve-convexity-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_ACTUAL_CURVE_LOCAL_CONVEXITY_GRID_EXCLUSION",
        "claim_boundary": "This proves a denominator-labelled local actual-exponential three-point exclusion. It proves no critical-box population bound, recurrence, density gain, or interval result.",
        "runtime": check_runtime("Cycle 186"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "preflight_validator": {"path": "../../tools/preregistration_check.py", "sha256": PREFLIGHT_VALIDATOR_HASH},
        "preregistration_preflight": preflight(),
        "actual_curve_result": {"epistemic_status": "PROVED", **exact_json(theorem)},
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "Either amplify the local exclusion with full rectangle weights to a strict critical-box saving, or preserve a separated-support model proving that local crowding exclusion alone cannot do so."},
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "preflight_command": "research prereg check docs/cycle-186-actual-curve-convexity-preregistration-v1.md --expected-cycle 186",
            "write_command": "python3 proof/build_cycle_186_actual_curve_convexity_v1.py --write",
            "check_command": "python3 proof/build_cycle_186_actual_curve_convexity_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_186_actual_curve_convexity_v1.py",
        },
        "exact_replay": exact_checks(),
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 186", output=OUTPUT, payload_factory=seal))
