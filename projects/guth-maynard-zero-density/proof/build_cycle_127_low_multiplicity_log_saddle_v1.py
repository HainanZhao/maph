#!/usr/bin/env python3
"""Seal Cycle 127 low-multiplicity logarithmic-saddle ledger."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-127-low-multiplicity-log-saddle-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-127-low-multiplicity-log-saddle-preregistration-v1.md", "5b76a9cc95a917c914ae1b301f71e06ba2b9580c5245663741f893ecc49f99af"),
    "document": (ROOT / "docs/cycle-127-low-multiplicity-log-saddle-v1.md", "0100c016603ba072f96b702022151fbb3f3ccd54ad2f5d4ae31a034758d684ce"),
    "conventions": (ROOT / "conventions/low_multiplicity_log_saddle_v1.py", "0fee647baa0f77c4af998d615bb9a60f3855c4ab2fa1418f55429004a814c3ac"),
    "tests": (ROOT / "tests/test_cycle_127_low_multiplicity_log_saddle_v1.py", "2d1636ef6cecbf44d3a4777a444fa23ad26ae280e92e286dc56144806c83e6b4"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle126": (ROOT / "artifacts/cycle-126-freiman-recurrence-v1.json", "c228988b1549f129522a68f5b10698768ae3581b367166a9253048b67aeb92e5"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle126"][0], "SEALED_COMMON_RATIONAL_MULTIPLIER_CHAIN_DEPTH_ANCHOR_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="low_multiplicity_log_saddle_v1")
    module = __import__("conventions.low_multiplicity_log_saddle_v1", fromlist=["exponent_ledger"])
    left = module.exponent_ledger(Fraction(16, 25), Fraction(0))
    require(left["volume_margin"] == Fraction(1, 25), "volume margin")
    require(left["hs_derivative_weighted"] == Fraction(3, 5), "HS derivative")
    require("never closes" in theorem["hs_barrier"], "one-dimensional barrier")
    require("sum_h|P(hD)|^2<<HL" in theorem["mellin_target"], "Mellin target")
    require("loses the factor D" in theorem["generic_loss"], "generic loss")
    require("no sampled-Mellin" in theorem["boundary"], "claim boundary")
    return {
        "artifact_id": "cycle-127-low-multiplicity-log-saddle-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_LOW_MULTIPLICITY_VOLUME_MARGIN_MELLIN_DIAGONAL_OPEN",
        "claim_boundary": (
            "This artifact proves the one-dimensional Huxley--Sargos ledger, "
            "joint volume margin, and exact sampled-Mellin target. It proves no "
            "sampled-Mellin estimate, low-multiplicity or simple-root closure, "
            "complete moment, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 127"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "low_multiplicity_log_saddle_theorem": {"epistemic_status": "PROVED", **theorem},
        "lower_endpoint_ledger": {
            "epistemic_status": "PROVED",
            "volume_margin": str(left["volume_margin"]),
            "hs_derivative_exponent": str(left["hs_derivative_weighted"]),
            "target": str(left["target"]),
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "prove the diagonal sampled-Mellin mean square on a compact "
                "lower-band region or extract its logarithmic-major-arc web"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_127_low_multiplicity_log_saddle_v1.py --write",
            "check_command": "python3 proof/build_cycle_127_low_multiplicity_log_saddle_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_127_low_multiplicity_log_saddle_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 127 sealer", output=OUTPUT, payload_factory=seal))
