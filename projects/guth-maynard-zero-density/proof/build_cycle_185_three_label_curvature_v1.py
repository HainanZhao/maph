#!/usr/bin/env python3
"""Seal Cycle 185 three-label curvature exactifier and mass-only no-go."""
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
OUTPUT = ROOT / "artifacts/cycle-185-three-label-curvature-v1.json"
PREFLIGHT_VALIDATOR = REPOSITORY_ROOT / "tools/preregistration_check.py"
PREFLIGHT_VALIDATOR_HASH = "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-185-three-label-curvature-preregistration-v1.md", "04f83bd4137799d899961a8cb226881df80ccca188bfb4e8d7a4dcb75583015f"),
    "document": (ROOT / "docs/cycle-185-three-label-curvature-v1.md", "0c17db0d16d820623e7cb5f877f4876edc41e41bf12db87baf9c54738bbcf40c"),
    "conventions": (ROOT / "conventions/three_label_curvature_v1.py", "767e24ef170fb3f5e292dfbcbe700fc426ec25f988fa16dab9c35fed1c2e34e6"),
    "tests": (ROOT / "tests/test_cycle_185_three_label_curvature_v1.py", "171fa38116dc7ac16ec166c2ce9cafe40b4b006985036bb5d8c4995d38125889"),
    "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "cycle181": (ROOT / "artifacts/cycle-181-common-intercept-packet-v1.json", "1d7402f3233e5c2eebf5f391fcae98037ea63a543b868dd850a3744673cef21c"),
    "cycle182": (ROOT / "artifacts/cycle-182-fibre-line-rigidity-v1.json", "ec2aa8e41ea5682b8c3bcf7818d26205700121ef097cb34ef4344a03a0e593a8"),
    "cycle183": (ROOT / "artifacts/cycle-183-intercept-cleared-ray-box-v1.json", "4d74a23710ae5b48b6e0fc0ea99fc30a660c5b52efb2ef2f8179ad586dd9604f"),
    "cycle184": (ROOT / "artifacts/cycle-184-ray-box-determinant-orbit-v1.json", "02a9c3e61166c6a265dd5f14dd80043daf8f6de5063594161cb435b68a340e25"),
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
    checked = validate_preregistration(INPUTS["preregistration"][0], expected_cycle=185, enforce_manifest_head=False)
    require(checked["parameters"]["curvature_integer"]["value"] == "K=U_0^2*A_-*A_+ - U_-*U_+*A_0^2", "preflight curvature disagreement")
    manifest = extract_manifest(INPUTS["preregistration"][0])
    require(any("arithmetic-progression identity" in item for item in manifest["formula_families"]), "preflight exponential triple family absent")
    return exact_json({
        "schema": checked["schema"], "cycle": checked["cycle"],
        "manifest_sha256": checked["manifest_sha256"], "input_hashes": checked["input_hashes"],
        "parameters": checked["parameters"],
    })


def exact_checks() -> dict[str, object]:
    module = __import__("conventions.three_label_curvature_v1", fromlist=["verify_all"])
    rows = module.verify_all()
    occupancy = rows["samples"]["occupancy_k1"]
    require(8 * occupancy["mass"]["ordered_cross_mass"] >= occupancy["mass"]["critical_target"], "critical AP-free mass replay")
    require(occupancy["stable_shell"]["minimum_product"] >= occupancy["stable_shell"]["cutoff_upper"], "stable AP-free shell replay")
    return exact_json(rows)


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle181"][0], "SEALED_COMMON_INTERCEPT_EXACTIFICATION_AND_STABLE_PACKET_REDUCTION")
    validate_prior(INPUTS["cycle182"][0], "SEALED_COMMON_INTERCEPT_FIBRE_LINE_RIGIDITY_AND_DENOMINATOR_CAPACITY")
    validate_prior(INPUTS["cycle183"][0], "SEALED_INTERCEPT_CLEARED_PRIMITIVE_RAY_BOX_SATURATION_CLASS")
    validate_prior(INPUTS["cycle184"][0], "SEALED_LCM_RESONANCE_AND_SUBSEED_NONRATIONAL_LOCAL_DEFORMATION")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="three_label_curvature_v1")
    return {
        "artifact_id": "cycle-185-three-label-curvature-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_THREE_LABEL_EXACTIFIER_AND_MASS_ONLY_AP_FREE_NO_GO",
        "claim_boundary": "This proves a conditional three-label curvature exactifier and an abstract mass/capacity/stable-shell AP-free occupancy no-go. It proves no actual-exponential distribution theorem, populated-box bound, seeded recurrence, density gain, or interval result.",
        "runtime": check_runtime("Cycle 185"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "preflight_validator": {"path": "../../tools/preregistration_check.py", "sha256": PREFLIGHT_VALIDATOR_HASH},
        "preregistration_preflight": preflight(),
        "three_label_result": {"epistemic_status": "PROVED", **exact_json(theorem)},
        "local_no_go": {
            "epistemic_status": "PROVED",
            "statement": "No inference from critical cross mass, full-fibre capacity, and stable shells alone can force the arithmetic-progression label triple needed for curvature exactification: the explicit ternary-digit occupancy reaches X^(21/25) scale and has none. This does not model actual exponential approximants.",
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "A viable C186 engine must constrain the actual-exponential distribution of high-depth rational approximants or impose a cross-box coefficient relation that defeats the AP-free occupancy. A curvature identity or weighted AP count without that analytic input is non-progress for density.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "mentor_checkpoint": {
            "recommendation": "APPROVE_SEAL",
            "known_flaw": "The AP-free occupancy is deliberately non-exponential and therefore cannot be read as an analytic counterexample.",
            "falsifier": "An admissible deep AP-label triple with K_prime nonzero, failure of the syzygy or depth threshold, an AP in the ternary support, or failure of its stable-shell mass ledger.",
            "resolution": "Adopted: seal the conditional exactifier and abstract mass-only no-go only; retain the non-exponential boundary prominently.",
            "next_action": "Use actual-exponential rational-approximant distribution or cross-box coefficient entropy, not another mass/capacity-only AP argument.",
        },
        "exact_replay": exact_checks(),
        "replay": {
            "preflight_command": "research prereg check docs/cycle-185-three-label-curvature-preregistration-v1.md --expected-cycle 185",
            "write_command": "python3 proof/build_cycle_185_three_label_curvature_v1.py --write",
            "check_command": "python3 proof/build_cycle_185_three_label_curvature_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_185_three_label_curvature_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 185", output=OUTPUT, payload_factory=seal))
