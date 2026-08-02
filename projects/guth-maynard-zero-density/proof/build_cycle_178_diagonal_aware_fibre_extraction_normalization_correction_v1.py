#!/usr/bin/env python3
"""Seal the Cycle 178 ordered-cross-mass normalization correction."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256, validate_prior


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-178-diagonal-aware-fibre-extraction-v1-normalization-correction.json"
INPUTS = {
    "correction_document": (ROOT / "docs/cycle-178-diagonal-aware-fibre-extraction-normalization-correction-v1.md", "9b28c150eda0eaedc57cdb0c44b5ae78cbb082261589611237b27b9ea9ebb066"),
    "cycle178": (ROOT / "artifacts/cycle-178-diagonal-aware-fibre-extraction-v1.json", "72797b1e97002d532b7bff28305330cea6f35f2b0e3192b87f7fb4adf99b0e9a"),
    "cycle178_tests": (ROOT / "tests/test_cycle_178_diagonal_aware_fibre_extraction_v1.py", "980ca4b1f3ddb078dc0dafb73e736d47e36ae579404ee7a3829aa72243705f39"),
    "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
}


def exact_checks() -> dict[str, object]:
    counts = [1, 2, 3]
    ordered = sum(left * right for index, left in enumerate(counts) for other, right in enumerate(counts) if index != other)
    unordered = sum(counts[index] * counts[other] for index in range(len(counts)) for other in range(index + 1, len(counts)))
    total = sum(counts)
    diagonal = sum(value * value for value in counts)
    require(ordered == total * total - diagonal == 22, "ordered cross identity")
    require(unordered == 11 and ordered == 2 * unordered, "unordered normalization")
    return {"sample_counts": counts, "ordered": ordered, "unordered": unordered, "factor": 2}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle178"][0], "SEALED_FIXED_BETA_HEAVY_FIBRE_SEEDED_PACKET_OR_CROSS_LABEL_REMAINDER")
    return {
        "artifact_id": "cycle-178-diagonal-aware-fibre-extraction-v1-normalization-correction",
        "epistemic_status": "PROVED",
        "status": "SEALED_ORDERED_CROSS_LABEL_NORMALIZATION_CORRECTION",
        "claim_boundary": "This correction explicitly fixes Cycle 178's U_cross as the ordered sum over ell!=ell'. It does not alter the heavy-fibre inverse, cross-label bound, or any density/interval boundary.",
        "runtime": check_runtime("Cycle 178 normalization correction"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "correction": {
            "epistemic_status": "PROVED",
            "cause": "The displayed formula was ordered, but the prose did not make that convention maximally explicit.",
            "affected_claims": "None mathematically: U_cross=sum_(ell!=ell') is ordered. The correction prevents applying its constant to the unordered sum.",
            "ordered_statement": "U_cross=T^2-sum N_ell^2>=T(T-2R) in the light branch; hence U_cross>=X^(32/25)/2 under the Cycle-178 large-X direct-target failure assumptions.",
            "unordered_conversion": "sum_(ell<ell')N_ell N_ell'=U_cross/2, so its corresponding bound is X^(32/25)/4.",
            "mentor_disposition": "REFINE accepted: freeze ordered versus unordered normalization before commit.",
        },
        "exact_replay": exact_checks(),
        "replay": {
            "write_command": "python3 proof/build_cycle_178_diagonal_aware_fibre_extraction_normalization_correction_v1.py --write",
            "check_command": "python3 proof/build_cycle_178_diagonal_aware_fibre_extraction_normalization_correction_v1.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 178 correction", output=OUTPUT, payload_factory=seal))
