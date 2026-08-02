#!/usr/bin/env python3
"""Seal Cycle 183 intercept-cleared primitive ray-box saturation class."""
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
from tools.preregistration_check import validate_preregistration  # noqa: E402


SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-183-intercept-cleared-ray-box-v1.json"
PREFLIGHT_VALIDATOR = REPOSITORY_ROOT / "tools/preregistration_check.py"
PREFLIGHT_VALIDATOR_HASH = "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-183-intercept-cleared-ray-box-preregistration-v1.md", "4ba2b229f952f8a65a25e93f1d535143b46b2070bbb2e095495d2cf7293d8865"),
    "document": (ROOT / "docs/cycle-183-intercept-cleared-ray-box-v1.md", "740d876c1254c396414348e54b0397d5da2c1fe6199b18a31837abbc2ca7812c"),
    "conventions": (ROOT / "conventions/intercept_cleared_ray_box_v1.py", "f0acf34e0e7c2e205595fd92fccd41fa9153973d3b7f6192fcefd96e544087e6"),
    "tests": (ROOT / "tests/test_cycle_183_intercept_cleared_ray_box_v1.py", "e1098c3a50e9e7cd956892e9d3cac01076439315f6c6365c41db0ee62d26c17d"),
    "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "cycle180": (ROOT / "artifacts/cycle-180-cross-label-pair-determinant-v1.json", "cdf34df41021fd1b0eab05f34202b23ea3fec96f010fbf3f0467328084b0d91a"),
    "cycle181": (ROOT / "artifacts/cycle-181-common-intercept-packet-v1.json", "1d7402f3233e5c2eebf5f391fcae98037ea63a543b868dd850a3744673cef21c"),
    "cycle182": (ROOT / "artifacts/cycle-182-fibre-line-rigidity-v1.json", "ec2aa8e41ea5682b8c3bcf7818d26205700121ef097cb34ef4344a03a0e593a8"),
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
    checked = validate_preregistration(INPUTS["preregistration"][0], expected_cycle=183, enforce_manifest_head=False)
    parameters = checked["parameters"]
    require(parameters["dyadic_box_cap"]["value"] == "B_box=bit_length(2R)^4*bit_length(H)^2*bit_length(Delta)", "preflight box-cap disagreement")
    require(parameters["stable_product"]["value"] == "r*k*q*U*V >= (4C/pi)*H*Delta/X", "preflight product disagreement")
    return exact_json({
        "schema": checked["schema"],
        "cycle": checked["cycle"],
        "manifest_sha256": checked["manifest_sha256"],
        "input_hashes": checked["input_hashes"],
        "parameters": checked["parameters"],
    })


def exact_checks() -> dict[str, object]:
    module = __import__("conventions.intercept_cleared_ray_box_v1", fromlist=["verify_all"])
    rows = module.verify_all()
    sample = rows["samples"]
    rectangle = sample["rectangle"]
    require(rectangle["determinants"]["D"] == 2 and rectangle["determinants"]["F"] == 1, "ray determinant replay")
    require(rectangle["left_ray"]["clearing"]["u"] == 1 and rectangle["right_ray"]["clearing"]["u"] == 2, "intercept clearing replay")
    require(sample["box"]["stable_rectangle_count"] == 2, "dyadic box replay")
    return exact_json(rows)


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle180"][0], "SEALED_NONZERO_CROSS_LABEL_PAIR_DETERMINANT_AND_STABLE_SHELL_REDUCTION")
    validate_prior(INPUTS["cycle181"][0], "SEALED_COMMON_INTERCEPT_EXACTIFICATION_AND_STABLE_PACKET_REDUCTION")
    validate_prior(INPUTS["cycle182"][0], "SEALED_COMMON_INTERCEPT_FIBRE_LINE_RIGIDITY_AND_DENOMINATOR_CAPACITY")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="intercept_cleared_ray_box_v1")
    return {
        "artifact_id": "cycle-183-intercept-cleared-ray-box-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_INTERCEPT_CLEARED_PRIMITIVE_RAY_BOX_SATURATION_CLASS",
        "claim_boundary": "This proves an exact populated primitive-ray candidate saturation class inside one common-intercept stable packet. It proves no upper bound inside that class, aggregate recurrence, density gain, or interval result.",
        "runtime": check_runtime("Cycle 183"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "preflight_validator": {"path": "../../tools/preregistration_check.py", "sha256": PREFLIGHT_VALIDATOR_HASH},
        "preregistration_preflight": preflight(),
        "intercept_cleared_ray_box": {"epistemic_status": "PROVED", **exact_json(theorem)},
        "critical_packet_consequence": {
            "epistemic_status": "PROVED",
            "statement": "A Cycle-181 critical stable packet W>=X^(21/25)/64 has one fully retained seven-field primitive-ray box of at least W/[bit_length(2R)^4*bit_length(H)^2*bit_length(Delta)] = X^(21/25-o(1)) actual ordered rectangles.",
        },
        "mentor_checkpoint": {
            "recommendation": "APPROVE SEAL",
            "known_flaw": "The ray-box class is a necessary populated inverse object only; it is not an upper bound. The cap must retain the inherited 0<c<1 label chart and all pair multipliers.",
            "resolution": "Within that boundary the mentor found no flaw: u|h, D=k*q*v*F, F!=0, the divided stable comparison, and the seven-field partition are all retained.",
            "next_action": "Attack one populated box through w*A-u*B=F and the two rational-slope approximations, or construct a box-level actual saturator.",
        },
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "Bound a populated primitive-ray box coefficient-preservingly, force its mass into a seeded recurrence, or construct it as a genuine nonrational actual exponential saturator. A dyadic box selection alone is not density or interval progress."},
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "exact_replay": exact_checks(),
        "replay": {
            "preflight_command": "research prereg check docs/cycle-183-intercept-cleared-ray-box-preregistration-v1.md --expected-cycle 183",
            "write_command": "python3 proof/build_cycle_183_intercept_cleared_ray_box_v1.py --write",
            "check_command": "python3 proof/build_cycle_183_intercept_cleared_ray_box_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_183_intercept_cleared_ray_box_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 183", output=OUTPUT, payload_factory=seal))
