#!/usr/bin/env python3
"""Seal the immutable convention correction for Cycle 185."""
from __future__ import annotations

from pathlib import Path
import sys
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = ROOT.parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))
from tools.preregistration_check import extract_manifest, validate_preregistration  # noqa: E402


SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-185-three-label-curvature-convention-correction-v1.json"
PREFLIGHT_VALIDATOR = REPOSITORY_ROOT / "tools/preregistration_check.py"
PREFLIGHT_VALIDATOR_HASH = "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-185-three-label-curvature-convention-correction-preregistration-v1.md", "2df7259d22b224f1676af45a6796dc4aad6e33972b14b7b5e3b1e642d216d39b"),
    "document": (ROOT / "docs/cycle-185-three-label-curvature-convention-correction-v1.md", "e4d6dca79a7f02822a6ecf002e2f24451c2d36d569ec3f12022a7e7711606cea"),
    "correction_conventions": (ROOT / "conventions/three_label_curvature_convention_correction_v1.py", "797f0bc400da978ee6fb452eea5fec6575e65f99e2452823ba9f04a041d2d3ae"),
    "correction_tests": (ROOT / "tests/test_cycle_185_three_label_curvature_convention_correction_v1.py", "ed83ddaf1b8a0cd1ee9811d28e3118af5fb7e3acdcaab927190d232aaccd0737"),
    "affected_artifact": (ROOT / "artifacts/cycle-185-three-label-curvature-v1.json", "b636e04db7b64e0cbc1ce3dc932905bd64b3491475501b835df487c477ee049f"),
    "affected_conventions": (ROOT / "conventions/three_label_curvature_v1.py", "767e24ef170fb3f5e292dfbcbe700fc426ec25f988fa16dab9c35fed1c2e34e6"),
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
    checked = validate_preregistration(INPUTS["preregistration"][0], expected_cycle=185, enforce_manifest_head=False)
    require(checked["parameters"]["corrected_invariant"]["value"].startswith("K_plus="), "shifted correction invariant absent")
    manifest = extract_manifest(INPUTS["preregistration"][0])
    require(any("alpha_ell=exp" in item for item in manifest["formula_families"]), "pinned phase convention absent")
    return exact_json({
        "schema": checked["schema"], "cycle": checked["cycle"],
        "manifest_sha256": checked["manifest_sha256"], "input_hashes": checked["input_hashes"],
        "parameters": checked["parameters"],
    })


def exact_checks() -> dict[str, object]:
    module = __import__("conventions.three_label_curvature_convention_correction_v1", fromlist=["verify_all"])
    rows = module.verify_all()
    require(rows["samples"]["unshifted_failure"]["unshifted_difference"] != 0, "original identity was not falsified")
    require(rows["samples"]["shifted_curvature"]["K_plus"] == 0, "shifted product fixture failed")
    return exact_json(rows)


def seal() -> dict[str, Any]:
    theorem = load_record(root=ROOT, path=INPUTS["correction_conventions"][0], module_name="three_label_curvature_convention_correction_v1")
    return {
        "artifact_id": "cycle-185-three-label-curvature-convention-correction-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_CORRECTION_SHIFTED_EXPONENTIAL_CURVATURE_AND_ORIGINAL_CLAIM_WITHHELD",
        "claim_boundary": "This correction withholds Cycle 185's unshifted alpha curvature claim and proves only the shifted-numerator local identity. It proves no actual-exponential distribution theorem, populated-box bound, seeded recurrence, density gain, or interval result.",
        "affected_artifact": {
            "path": "artifacts/cycle-185-three-label-curvature-v1.json",
            "sha256": INPUTS["affected_artifact"][1],
            "disposition": "immutable; the original unshifted curvature theorem, its K syzygy, and its depth exactification are withheld. The abstract AP-free mass/capacity/stable-shell no-go is unaffected.",
        },
        "correction": {
            "cause": "The pinned ray slope is alpha_ell=z^ell-1, but the original record applied the product identity for z^ell directly to alpha_ell.",
            "corrected_invariant": "K_plus=U_0^2*(A_-+U_-)*(A_++U_+)-U_-*U_+*(A_0+U_0)^2",
            "unaffected": "The AP-free occupancy and its claim boundary do not invoke the false alpha product identity.",
            "required_downstream_action": "Use only this correction's shifted-numerator result; rederive any downstream use of Cycle 185 before promotion.",
        },
        "runtime": check_runtime("Cycle 185 convention correction"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "preflight_validator": {"path": "../../tools/preregistration_check.py", "sha256": PREFLIGHT_VALIDATOR_HASH},
        "preregistration_preflight": preflight(),
        "corrected_local_result": {"epistemic_status": "PROVED", **exact_json(theorem)},
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "preflight_command": "research prereg check docs/cycle-185-three-label-curvature-convention-correction-preregistration-v1.md --expected-cycle 185",
            "write_command": "python3 proof/build_cycle_185_three_label_curvature_convention_correction_v1.py --write",
            "check_command": "python3 proof/build_cycle_185_three_label_curvature_convention_correction_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_185_three_label_curvature_convention_correction_v1.py",
        },
        "exact_replay": exact_checks(),
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 185 correction", output=OUTPUT, payload_factory=seal))
