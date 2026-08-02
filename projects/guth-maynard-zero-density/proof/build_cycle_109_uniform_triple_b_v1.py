#!/usr/bin/env python3
"""Seal Cycle 109 uniform complete smooth triple-B kernel."""
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
OUTPUT = ROOT / "artifacts/cycle-109-uniform-triple-b-v1.json"
INPUTS = {
    "discovery_candidate": (ROOT / "discovery/cycle-109-uniform-triple-b-candidate-v1.md", "270735ecefedbc93b2a7cf0aba5046bf8cf2e58885a5627b5a5a587a5e6b6624"),
    "preregistration": (ROOT / "docs/cycle-109-uniform-triple-b-preregistration-v1.md", "5d316489d5605ef268e7b966a9e608e47373a714b8bc46fa1c53a23d37a61186"),
    "document": (ROOT / "docs/cycle-109-uniform-triple-b-v1.md", "e6e049377ca3fbeda852e2b247f63e836224233fbdeaf005e1b9ace4c1ae9cc5"),
    "conventions": (ROOT / "conventions/uniform_triple_b_v1.py", "9596514308890e2be651a4acfb223e8c4c4a9a91dd402b19cb55f611b241ce99"),
    "tests": (ROOT / "tests/test_cycle_109_uniform_triple_b_v1.py", "4872224eaba7c22f5224e9c863a7991325ddc6e0ff1e88cc662a56254d2ae63c"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle81": (ROOT / "artifacts/cycle-81-exact-q-transform-v1.json", "0753d455a2e9428b28f1b9dac59b04fd57008db562370202a300a38a818631a4"),
    "cycle87": (ROOT / "artifacts/cycle-87-mellin-alias-atlas-v1.json", "68b88ccd4ce3e5371906e3b0da3c254056b79bad9504880ebbff04b9cebce8ca"),
    "cycle90": (ROOT / "artifacts/cycle-90-equal-height-bprocess-v1.json", "a24a63110e26fff4672c8b8e2cca27569a00885dec7b8c934f8ca3971967c3de"),
    "cycle100": (ROOT / "artifacts/cycle-100-critical-fiber-atlas-v1.json", "2b5de8802840ce6411ef9b1eef887d4619ecb04d1c71fe520491db4cb01b2da1"),
    "cycle108": (ROOT / "artifacts/cycle-108-triple-b-jacobian-v1.json", "c030327447462241e056c593bc799e7fec472d6663faf17d5f8a9dbab8424813"),
}


def seal() -> dict[str, Any]:
    expected = {
        "cycle81": "SEALED_EXACT_Q_TRANSFORM_LOG_RESONANCE_PROJECTOR_OPEN",
        "cycle87": "SEALED_MELLIN_ALIAS_TRICHOTOMY_BOUND_OR_WEB_OPEN",
        "cycle90": "SEALED_EQUAL_HEIGHT_BPROCESS_SADDLE_DISCREPANCY_OR_WEB_OPEN",
        "cycle100": "SEALED_GENERIC_CRITICAL_FIBER_BOUND_CROSS_VALUATION_AND_LOW_HEIGHT_OPEN",
        "cycle108": "SEALED_LEADING_PERFECT_POWER_SCALE_SUMMABLE_PAYLOAD_REMAINDERS_OPEN",
    }
    for label, status in expected.items():
        validate_prior(INPUTS[label][0], status)
    theorem = load_record(
        root=ROOT,
        path=INPUTS["conventions"][0],
        module_name="uniform_triple_b_v1",
    )
    require("ell^(-3/2)" in theorem["complete_kernel"], "complete kernel decay")
    require("fixed smooth" in theorem["smooth_model"], "registered symbol class")
    require("distinct core" in theorem["boundary"], "aggregation boundary")
    return {
        "artifact_id": "cycle-109-uniform-triple-b-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_FULL_SMOOTH_PERFECT_POWER_SCALE_RAY_SUMMABLE",
        "claim_boundary": (
            "This artifact proves a self-contained oscillatory-integral lemma and uses "
            "it to bound the complete registered smooth triple-B scale kernel by "
            "C_W ell^(-3/2). Distinct cores, nonsmooth variants, other root branches, "
            "moments, density, and intervals remain open."
        ),
        "runtime": check_runtime("Cycle 109"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "prior_context": {
            "epistemic_status": "PROVED",
            "roles": {
                "cycle81": "fixed smooth exact transform weights",
                "cycle87": "stationary alias kernel",
                "cycle90": "smooth logarithmic B-process convention",
                "cycle100": "no inherited Mobius sign",
                "cycle108": "leading Jacobian scale law",
            },
        },
        "uniform_kernel_theorem": {"epistemic_status": "PROVED", **theorem},
        "closed_scale_sector": {
            "epistemic_status": "PROVED",
            "statement": (
                "sum over every actual coefficient scale on a fixed perfect-power core "
                "is <3C_W uniformly, including exact base-phase resonance"
            ),
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "aggregate distinct perfect-power and large-degree irrational cores, "
                "then control weak and simple-root branches"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_109_uniform_triple_b_v1.py --write",
            "check_command": "python3 proof/build_cycle_109_uniform_triple_b_v1.py --check",
            "test_command": (
                "python3 -m unittest tests/test_cycle_109_uniform_triple_b_v1.py "
                "tests/test_cycle_seal_v1.py"
            ),
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 109 sealer", output=OUTPUT, payload_factory=seal))
