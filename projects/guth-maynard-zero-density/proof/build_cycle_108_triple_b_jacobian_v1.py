#!/usr/bin/env python3
"""Seal Cycle 108 triple-B leading Jacobian summability."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import (
    check_runtime,
    freeze_inputs,
    load_record,
    require,
    run_cli,
    sha256,
    validate_prior,
)


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-108-triple-b-jacobian-v1.json"
INPUTS = {
    "discovery_candidate": (ROOT / "discovery/cycle-108-triple-b-jacobian-candidate-v1.md", "aaa6db705e732adfab054b8875ebc1ecdc3afc569018f3bc548f9f39f1f908a2"),
    "preregistration": (ROOT / "docs/cycle-108-triple-b-jacobian-preregistration-v1.md", "823fefeeaf48012f6536f245f16d389b21deb57f5a5b81569f2066b0e2c0d00c"),
    "document": (ROOT / "docs/cycle-108-triple-b-jacobian-v1.md", "fbd72a1510b3fd8236e47c7d1e3489fe89d128c45412641edc8f5fe25026eea7"),
    "conventions": (ROOT / "conventions/triple_b_jacobian_v1.py", "33c5260601c3db8bb026d64985fcb37e8e699f46682d5201c6ea7446b0a9baac"),
    "tests": (ROOT / "tests/test_cycle_108_triple_b_jacobian_v1.py", "bc62c174c862a589809a5bae0e777ad338a5dc81194572831868ba569fcdd27c"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle107": (ROOT / "artifacts/cycle-107-actual-scale-phase-v1.json", "189d2515ac835f25b14ff060604317c0a5210050b0c4ec06be567935caf28319"),
}


def seal() -> dict[str, Any]:
    validate_prior(
        INPUTS["cycle107"][0],
        "SEALED_ACTUAL_SCALE_GEOMETRIC_PHASE_RESONANCE_OR_BV_CANCELLATION",
    )
    theorem = load_record(
        root=ROOT,
        path=INPUTS["conventions"][0],
        module_name="triple_b_jacobian_v1",
    )
    require("ell^(-3/2)" in theorem["jacobian"], "Jacobian scale law")
    require("subpower" in theorem["implication"], "subpower closure interface")
    require("remainders" in theorem["boundary"], "remainder boundary")
    return {
        "artifact_id": "cycle-108-triple-b-jacobian-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_LEADING_PERFECT_POWER_SCALE_SUMMABLE_PAYLOAD_REMAINDERS_OPEN",
        "claim_boundary": (
            "This artifact proves scale invariance of the stationary points, the exact "
            "ell^(-3/2) triple-B Jacobian law, and absolute/BV summability of the leading "
            "scale ray. Arithmetic payload weights, non-invariant cutoffs, remainders, "
            "other cores, moments, density, and intervals remain open."
        ),
        "runtime": check_runtime("Cycle 108"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "prior_context": {
            "epistemic_status": "PROVED",
            "cycle107_role": "supply the actual scale ray and geometric stationary phase",
        },
        "jacobian_theorem": {"epistemic_status": "PROVED", **theorem},
        "closed_leading_sector": {
            "epistemic_status": "PROVED",
            "statement": (
                "the leading perfect-power scale sum is <=3 J0 sup|omega_ell| "
                "and loses no power under a subpower residual envelope"
            ),
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "trace and bound the actual arithmetic payload envelope and uniform "
                "stationary-phase remainders, then aggregate different cores"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_108_triple_b_jacobian_v1.py --write",
            "check_command": "python3 proof/build_cycle_108_triple_b_jacobian_v1.py --check",
            "test_command": (
                "python3 -m unittest tests/test_cycle_108_triple_b_jacobian_v1.py "
                "tests/test_cycle_seal_v1.py"
            ),
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 108 sealer", output=OUTPUT, payload_factory=seal))
