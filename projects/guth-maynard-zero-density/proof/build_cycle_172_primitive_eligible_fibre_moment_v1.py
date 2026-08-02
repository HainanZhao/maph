#!/usr/bin/env python3
"""Seal Cycle 172 primitive eligible-fibre divisor-moment no-go."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-172-primitive-eligible-fibre-moment-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-172-primitive-eligible-fibre-moment-preregistration-v1.md", "b24de9befbef5cfd318326b1ed939526630639e33c501f340a67fa7cec23972c"),
    "document": (ROOT / "docs/cycle-172-primitive-eligible-fibre-moment-v1.md", "cf6ee29c13b25b835257521fe390bc239bde3d4a535568ff95ca1d1d6f86bb21"),
    "conventions": (ROOT / "conventions/primitive_eligible_fibre_moment_v1.py", "6bcac70c7a3a60a42cf8a7e5f86340d986befa7524043fc5eed5c136317b63e2"),
    "tests": (ROOT / "tests/test_cycle_172_primitive_eligible_fibre_moment_v1.py", "ec5c2d3fd288a0d38d81c6cccc59ca79492775ecbe4af8595936b5fb6c99e510"),
    "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "cycle171": (ROOT / "artifacts/cycle-171-eligibility-weighted-projective-content-v1.json", "c0f92b19840f61d4aa357ade9a0459887f93823d3f25e422e34e3719a96d0d8b"),
    "cycle167": (ROOT / "artifacts/cycle-167-affine-fibre-transport-v1.json", "7ba12c9d0534c0d0d151bce753fa24191c4e174af839ca12b86d65911779ed1b"),
}


def exact_checks() -> dict[str, object]:
    module = __import__("conventions.primitive_eligible_fibre_moment_v1", fromlist=["verify_all"])
    checked = module.verify_all()
    require("local-interface countermodel" in checked["boundary"], "claim boundary")
    record = module.verify_family(12)
    require(record["row_count"] == 5, "massed labelled fibre")
    require("g=c=u=v=1" in record["projective"], "two-factor avoidance")
    require("M=W/2" in record["moment"], "moment deficit")
    return checked


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle171"][0], "SEALED_ELIGIBILITY_WEIGHTED_PROJECTIVE_CONTENT_DIVISOR_WEB_AND_SHARP_TRANSFER")
    validate_prior(INPUTS["cycle167"][0], "SEALED_DIRECT_AFFINE_CROSS_LABEL_TRANSPORT_OR_OBSTRUCTION_CLASSIFIER")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="primitive_eligible_fibre_moment_v1")
    return {
        "artifact_id": "cycle-172-primitive-eligible-fibre-moment-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_PRIMITIVE_LOCAL_INTERFACE_DOES_NOT_FORCE_DIVISOR_MOMENT_SURPLUS",
        "claim_boundary": "This proves a finite signed abstract labelled local-interface countermodel and typed denominator-capacity obstruction family. Its negative alpha values lie outside the actual positive exponential curve, so it proves no statement about the actual global census, recurrence, skeleton, density, or intervals.",
        "runtime": check_runtime("Cycle 172"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "prior_context": {
            "epistemic_status": "PROVED",
            "cycle171_role": "provides the primitive two-factor content moment whose surplus is tested here",
            "cycle167_role": "provides the local divisibility/range/balance interface retained by the countermodel",
        },
        "primitive_fibre_no_go": {"epistemic_status": "PROVED", **theorem},
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_checks(),
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "On the actual positive exponential curve, use a global exponential/fibre invariant to force numerator/denominator divisor incidence or quantify its absence in the complete labelled banks."},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_172_primitive_eligible_fibre_moment_v1.py --write",
            "check_command": "python3 proof/build_cycle_172_primitive_eligible_fibre_moment_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_172_primitive_eligible_fibre_moment_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 172", output=OUTPUT, payload_factory=seal))
