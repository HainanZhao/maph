#!/usr/bin/env python3
"""Seal Cycle 173 positive-forward conservative balance obstruction."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-173-positive-forward-balance-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-173-positive-forward-balance-preregistration-v1.md", "c80186ba1b5f419606dbde63af6bb6ae3cae5c0568627645eabb85c00922187c"),
    "document": (ROOT / "docs/cycle-173-positive-forward-balance-v1.md", "db38814992841f68556acd06f40e1b2c6dcaae651194ff71bb4de831e549daee"),
    "conventions": (ROOT / "conventions/positive_forward_balance_v1.py", "ca3bf523d0b7df5a75b983d661638fec74aa8e0b4f1ca5214cd2db5efb797823"),
    "tests": (ROOT / "tests/test_cycle_173_positive_forward_balance_v1.py", "89e0e5c398e9de7c2a3715ee4da56399be712ad07cd7938cdec98893fa2c1063"),
    "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "cycle167": (ROOT / "artifacts/cycle-167-affine-fibre-transport-v1.json", "7ba12c9d0534c0d0d151bce753fa24191c4e174af839ca12b86d65911779ed1b"),
    "cycle172": (ROOT / "artifacts/cycle-172-primitive-eligible-fibre-moment-v1.json", "d375edd17584e89c5824cc5bb2a43511d99eda03ece86a9f123b338bceda5a5d"),
}


def exact_checks() -> dict[str, object]:
    module = __import__("conventions.positive_forward_balance_v1", fromlist=["verify_all"])
    checked = module.verify_all()
    require("positive-forward conservative-gate obstruction" in checked["boundary"], "claim boundary")
    contradiction = module.positive_forward_infeasible(y_bound=module.Q(101, 100), slack=module.Q(1))
    require(contradiction["strict_lower"] > 2, "strict positive squeeze")
    return checked


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle167"][0], "SEALED_DIRECT_AFFINE_CROSS_LABEL_TRANSPORT_OR_OBSTRUCTION_CLASSIFIER")
    validate_prior(INPUTS["cycle172"][0], "SEALED_PRIMITIVE_LOCAL_INTERFACE_DOES_NOT_FORCE_DIVISOR_MOMENT_SURPLUS")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="positive_forward_balance_v1")
    return {
        "artifact_id": "cycle-173-positive-forward-balance-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_POSITIVE_FORWARD_CONSERVATIVE_BALANCE_GATE_EMPTY",
        "claim_boundary": "This proves that the actual positive forward direct-map branch cannot satisfy the frozen Cycle-167 conservative balance, admissibility, and simultaneous dyadic-range gate. It does not rule out reverse orientation, extra strip slack, different maps, global coupling, recurrence, density, or intervals.",
        "runtime": check_runtime("Cycle 173"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "prior_context": {
            "epistemic_status": "PROVED",
            "cycle167_role": "supplies the direct forward affine map and conservative balance ledger",
            "cycle172_role": "shows that a signed abstract local countermodel does not settle the positive curve; positivity is used here",
        },
        "positive_forward_obstruction": {"epistemic_status": "PROVED", **theorem},
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_checks(),
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "Develop reverse-orientation, quantified-slack, or genuinely new transport/coupling machinery on the actual positive exponential curve."},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_173_positive_forward_balance_v1.py --write",
            "check_command": "python3 proof/build_cycle_173_positive_forward_balance_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_173_positive_forward_balance_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 173", output=OUTPUT, payload_factory=seal))
