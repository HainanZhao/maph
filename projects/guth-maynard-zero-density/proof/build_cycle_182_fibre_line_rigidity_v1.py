#!/usr/bin/env python3
"""Seal Cycle 182 common-intercept fibre-line rigidity."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-182-fibre-line-rigidity-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-182-fibre-line-rigidity-preregistration-v1.md", "a1f4b9406461063ffe043eeaebbcf3d50761f84429ad6088177e87381666cf99"),
    "document": (ROOT / "docs/cycle-182-fibre-line-rigidity-v1.md", "8a5b42c271698350549df5bebafbd897d40b523a23f0104d8230f985093d8ac2"),
    "conventions": (ROOT / "conventions/fibre_line_rigidity_v1.py", "30e4424b6aa3e61317dec7c06e37d4adf57a28fa6e7b11f5b47a03f2023a3de6"),
    "tests": (ROOT / "tests/test_cycle_182_fibre_line_rigidity_v1.py", "ad7df082a125462f74c734e460e79b7ff5ef31e3ea0573c16acc1c1f7eb21ea2"),
    "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "cycle181": (ROOT / "artifacts/cycle-181-common-intercept-packet-v1.json", "1d7402f3233e5c2eebf5f391fcae98037ea63a543b868dd850a3744673cef21c"),
}


def exact_json(value: object) -> object:
    if isinstance(value, Fraction):
        return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    if isinstance(value, dict):
        return {str(key): exact_json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [exact_json(item) for item in value]
    return value


def exact_checks() -> dict[str, object]:
    module = __import__("conventions.fibre_line_rigidity_v1", fromlist=["verify_all"])
    rows = module.verify_all()
    fibre = rows["samples"]["fibre"]
    require(fibre["primitive_slope"]["value"] == Fraction(1, 4), "primitive slope replay")
    require(fibre["common_intercept"]["value"] == Fraction(-1, 2), "common intercept replay")
    require(fibre["common_intercept"]["denominator"] == 2, "intercept denominator replay")
    require(fibre["primitive_slope"]["denominator"] == 4, "v divides U replay")
    require(fibre["fibre_count"] == 3 and fibre["extreme_gap"] == 8, "completed fibre replay")
    require(fibre["packet_state"]["product_shell"] == "stable", "retained packet shell")
    return exact_json(rows)


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle181"][0], "SEALED_COMMON_INTERCEPT_EXACTIFICATION_AND_STABLE_PACKET_REDUCTION")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="fibre_line_rigidity_v1")
    return {
        "artifact_id": "cycle-182-fibre-line-rigidity-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_COMMON_INTERCEPT_FIBRE_LINE_RIGIDITY_AND_DENOMINATOR_CAPACITY",
        "claim_boundary": "This proves rational-line rigidity, lattice completion, and primitive-denominator capacity for one common-intercept packet. It proves no in-packet census bound, aggregate recurrence, density gain, or interval result.",
        "runtime": check_runtime("Cycle 182"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "fibre_line_rigidity": {"epistemic_status": "PROVED", **exact_json(theorem)},
        "packet_consequence": {
            "epistemic_status": "PROVED",
            "statement": "Within a fixed rho=p/v packet, each non-singleton participating fibre has one primitive slope A/U, v|U, one base-height residue modulo U, and a complete step-U segment of at most 1+H/U actual rows. The full stable determinant/product and residual state remains attached.",
        },
        "mentor_checkpoint": {
            "recommendation": "APPROVE SEAL",
            "known_flaw": "The completion argument must use the full actual fibre and affine interpolation between its extreme rows; it cannot infer missing rows from a selected pair alone.",
            "resolution": "A packet-member pair first identifies rho=p/v at its label. The shared primitive slope then extends that line to every actual row in the full fibre; only the extreme rows support lattice completion.",
            "next_action": "Turn the X^(21/25) packet mass into a dyadic (U,N) ledger: force a depth-X^(6/25) seeded fibre or bound the remaining primitive rational-slope labels.",
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Prove a coefficient-preserving upper bound for stable cross-label rectangles in one primitive common-intercept line packet, or construct a nonrational actual saturator for it. Fibre-line rigidity alone is not a census bound or recurrence.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "exact_replay": exact_checks(),
        "replay": {
            "write_command": "python3 proof/build_cycle_182_fibre_line_rigidity_v1.py --write",
            "check_command": "python3 proof/build_cycle_182_fibre_line_rigidity_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_182_fibre_line_rigidity_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 182", output=OUTPUT, payload_factory=seal))
