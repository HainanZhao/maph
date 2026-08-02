#!/usr/bin/env python3
"""Seal Cycle 184 LCM resonance and sub-seed nonrational deformation."""
from __future__ import annotations

from fractions import Fraction
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
OUTPUT = ROOT / "artifacts/cycle-184-ray-box-determinant-orbit-v1.json"
PREFLIGHT_VALIDATOR = REPOSITORY_ROOT / "tools/preregistration_check.py"
PREFLIGHT_VALIDATOR_HASH = "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-184-ray-box-determinant-orbit-preregistration-v1.md", "c01c60438a7531d0acefdc5e7565d868769f3f2aacbef3dfc6917179d899a428"),
    "document": (ROOT / "docs/cycle-184-ray-box-determinant-orbit-v1.md", "d284f32eac014f7d062b916246b334bcdd9372d784607f659fcc88808f06174a"),
    "conventions": (ROOT / "conventions/ray_box_determinant_orbit_v1.py", "67b868651fd4a1e0404a9ee14bca894533088181c5d01411ab36a74a0f4ab3fe"),
    "tests": (ROOT / "tests/test_cycle_184_ray_box_determinant_orbit_v1.py", "bfd2a5075819fcec2616be170432952189dc1ceef2e2b77636bcf2b57d1f7171"),
    "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "cycle180": (ROOT / "artifacts/cycle-180-cross-label-pair-determinant-v1.json", "cdf34df41021fd1b0eab05f34202b23ea3fec96f010fbf3f0467328084b0d91a"),
    "cycle181": (ROOT / "artifacts/cycle-181-common-intercept-packet-v1.json", "1d7402f3233e5c2eebf5f391fcae98037ea63a543b868dd850a3744673cef21c"),
    "cycle182": (ROOT / "artifacts/cycle-182-fibre-line-rigidity-v1.json", "ec2aa8e41ea5682b8c3bcf7818d26205700121ef097cb34ef4344a03a0e593a8"),
    "cycle183": (ROOT / "artifacts/cycle-183-intercept-cleared-ray-box-v1.json", "4d74a23710ae5b48b6e0fc0ea99fc30a660c5b52efb2ef2f8179ad586dd9604f"),
}


def exact_json(value: object) -> object:
    if isinstance(value, Fraction):
        return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    if isinstance(value, dict):
        return {str(key): exact_json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [exact_json(item) for item in value]
    return value


def preflight() -> dict[str, object]:
    require(sha256(PREFLIGHT_VALIDATOR) == PREFLIGHT_VALIDATOR_HASH, "preflight validator hash mismatch")
    checked = validate_preregistration(INPUTS["preregistration"][0], expected_cycle=184, enforce_manifest_head=False)
    parameters = checked["parameters"]
    require(parameters["determinant_relation"]["value"] == "F=w*A-u*B; D=k*q*v*F; F!=0", "preflight determinant disagreement")
    manifest = extract_manifest(INPUTS["preregistration"][0])
    require("bezout" in " ".join(manifest["formula_families"]).lower(), "preflight Bezout/divisibility family absent")
    return exact_json({
        "schema": checked["schema"], "cycle": checked["cycle"],
        "manifest_sha256": checked["manifest_sha256"], "input_hashes": checked["input_hashes"],
        "parameters": checked["parameters"],
    })


def exact_checks() -> dict[str, object]:
    module = __import__("conventions.ray_box_determinant_orbit_v1", fromlist=["verify_all"])
    rows = module.verify_all()
    family = rows["samples"]["family_T3"]
    require(family["fibres"]["all_depths_below_seed"], "sub-seed deformation replay")
    require(family["determinant"]["F"] != 0, "nonzero deformation determinant")
    require(family["populated_box"]["one_box_lower_bound"] < 3**23, "subcritical deformation mass")
    return exact_json(rows)


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle180"][0], "SEALED_NONZERO_CROSS_LABEL_PAIR_DETERMINANT_AND_STABLE_SHELL_REDUCTION")
    validate_prior(INPUTS["cycle181"][0], "SEALED_COMMON_INTERCEPT_EXACTIFICATION_AND_STABLE_PACKET_REDUCTION")
    validate_prior(INPUTS["cycle182"][0], "SEALED_COMMON_INTERCEPT_FIBRE_LINE_RIGIDITY_AND_DENOMINATOR_CAPACITY")
    validate_prior(INPUTS["cycle183"][0], "SEALED_INTERCEPT_CLEARED_PRIMITIVE_RAY_BOX_SATURATION_CLASS")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="ray_box_determinant_orbit_v1")
    return {
        "artifact_id": "cycle-184-ray-box-determinant-orbit-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_LCM_RESONANCE_AND_SUBSEED_NONRATIONAL_LOCAL_DEFORMATION",
        "claim_boundary": "This proves only exact LCM-resonance redundancy and a scale-matched nonrational two-label local deformation below the seed and critical box scales. It proves no bound, saturation, or impossibility theorem for a critical populated ray box, aggregate recurrence, density gain, or interval result.",
        "runtime": check_runtime("Cycle 184"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "preflight_validator": {"path": "../../tools/preregistration_check.py", "sha256": PREFLIGHT_VALIDATOR_HASH},
        "preregistration_preflight": preflight(),
        "determinant_orbit_result": {"epistemic_status": "PROVED", **exact_json(theorem)},
        "local_no_go": {
            "epistemic_status": "PROVED",
            "statement": "Within the C183 local determinant/orbit architecture, gcd(u,w)|F is exactly the LCM resonance generated by the two orbit errors; the nonrational deformation has all depths below X^(6/25) and one box only X^(11/25-o(1)). This rules out only an LCM-only forcing argument, not a population-sensitive critical-box theorem.",
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "A viable C185 engine must use three-label/shared-fibre compatibility or cross-box coefficient entropy to bound or transfer a populated family of varying LCM resonances, or construct a genuinely critical nonrational ray-box saturator. A single LCM relation or two-label deformation is non-progress for density.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "mentor_checkpoint": {
            "recommendation": "REFINE_THEN_SEAL",
            "known_flaw": "The X^(11/25-o(1)) deformation is subcritical and cannot establish saturation or impossibility for a critical X^(21/25-o(1)) box.",
            "falsifier": "A frozen orbit configuration violating the LCM identity, or failure of positivity, common intercept, stability, sub-seed depth, or box count in the deformation.",
            "resolution": "Adopted: the claim is narrowed to LCM_RESONANCE_REDUNDANCY only; the deformation is evidence against an LCM-only forcing step, not a critical-box barrier.",
            "next_action": "Test genuinely population-sensitive three-label/shared-fibre compatibility or cross-box coefficient entropy.",
        },
        "exact_replay": exact_checks(),
        "replay": {
            "preflight_command": "research prereg check docs/cycle-184-ray-box-determinant-orbit-preregistration-v1.md --expected-cycle 184",
            "write_command": "python3 proof/build_cycle_184_ray_box_determinant_orbit_v1.py --write",
            "check_command": "python3 proof/build_cycle_184_ray_box_determinant_orbit_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_184_ray_box_determinant_orbit_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 184", output=OUTPUT, payload_factory=seal))
