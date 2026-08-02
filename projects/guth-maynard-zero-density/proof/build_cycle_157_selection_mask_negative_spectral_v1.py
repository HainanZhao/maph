#!/usr/bin/env python3
"""Seal Cycle 157 raw mask obstruction and negative spectral localization."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-157-selection-mask-negative-spectral-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-157-selection-mask-cone-preregistration-v1.md", "9b374064ac5ef96d889e8989e75c7c4d59654e394be05e6282f07991a322620b"),
    "document": (ROOT / "docs/cycle-157-selection-mask-negative-spectral-v1.md", "f66ea5cc18ce68bc8db6e9f20a0e824630918d0b2b11fee87ef60ed4cd39a69b"),
    "conventions": (ROOT / "conventions/selection_mask_negative_spectral_v1.py", "539f690bab5eb234d98da7aff5daa92c8b051be47e1dbdd2281e30e5c55e8f67"),
    "tests": (ROOT / "tests/test_cycle_157_selection_mask_negative_spectral_v1.py", "c105ac8c61698e7769a203c099ba42e60159e8ca8b4c3e7694ad76a114b2b4d0"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle145": (ROOT / "artifacts/cycle-145-vector-autocorrelation-v1.json", "5989739fe7de6e80782e98d38b60226b0eb5aa95e630a10587427dc12a77d41a"),
    "cycle154": (ROOT / "artifacts/cycle-154-coefficient-escape-localization-v1.json", "3d17a6773aa714d83c12bc7beddbde5bfefc499f82ba7848f79cdf3cd7f28184"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle145"][0], "SEALED_ARITHMETIC_SELECTION_MASK_AUTOCORRELATION_OPEN")
    validate_prior(INPUTS["cycle154"][0], "SEALED_CONDITIONAL_FINITE_LABELLED_ESCAPE_LOCALIZATION")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="selection_mask_negative_spectral_v1")
    module = __import__("conventions.selection_mask_negative_spectral_v1", fromlist=["spectral_ledger", "negative_energy_localization"])
    row = module.spectral_ledger(
        eigenvalues=(Fraction(3), Fraction(-2)),
        coefficient_projection_squares=(Fraction(1, 2), Fraction(1)),
        external_weight=Fraction(1),
    )
    aggregate = module.negative_energy_localization((row,), Fraction(1, 2))
    require(row["real_hermitian_correlation"] == Fraction(-1, 2), "Hermitian signed correlation")
    require(aggregate["negative_spectral_energy"] >= Fraction(1, 2), "negative spectral retention")
    require("no extra factor of two" in theorem["hermitianization"], "factor convention")
    require("not PSD" in theorem["zero_diagonal_obstruction"], "raw Gram obstruction")
    return {
        "artifact_id": "cycle-157-selection-mask-negative-spectral-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_RAW_ZERO_DIAGONAL_GRAM_OBSTRUCTION_COEFFICIENT_NEGATIVE_SPECTRAL_ALIGNMENT_OPEN",
        "claim_boundary": (
            "This artifact proves a raw fixed-difference Gram obstruction and conditional coefficient-weighted negative spectral "
            "localization. It does not prove actual eigenspace alignment, finite block concentration, an approximate Gram transport, "
            "a coefficient partition, a moment, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 157"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "selection_mask_negative_spectral_theorem": {"epistemic_status": "PROVED", **theorem},
        "sample": {"epistemic_status": "PROVED", **{key: str(value) for key, value in row.items()}},
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "prove the actual negative spectral energy concentrates in a fixed labelled block family, or preserve a quantitative "
                "block-complexity inverse with the coefficient and anchor labels"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_157_selection_mask_negative_spectral_v1.py --write",
            "check_command": "python3 proof/build_cycle_157_selection_mask_negative_spectral_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_157_selection_mask_negative_spectral_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 157 sealer", output=OUTPUT, payload_factory=seal))
