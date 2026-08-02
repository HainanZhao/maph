#!/usr/bin/env python3
"""Seal Cycle 147 strict-core signed-cell estimate."""
from __future__ import annotations

from math import pi
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-147-strict-core-signed-cell-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-147-strict-core-signed-cell-preregistration-v1.md", "ba444a6577d0f4c4e7660d16de89495f54a7ba48e884ea55160c154d00b18ebe"),
    "document": (ROOT / "docs/cycle-147-strict-core-signed-cell-v1.md", "687bc417d1e3b7145c38a1f44ce71d489a864fa4d00605ea201c79176df029c2"),
    "conventions": (ROOT / "conventions/strict_core_signed_cell_v1.py", "209b31e881f260aae039276608a7bc58637782998c11b0da524ee78799c0ea13"),
    "tests": (ROOT / "tests/test_cycle_147_strict_core_signed_cell_v1.py", "312087d0aa26156ed8043708da0ac55d08f68267d767feb273646bb83271fe26"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle123": (ROOT / "artifacts/cycle-123-joint-radial-alias-v1.json", "e700c21a422413abb6f35882d8d5a67b4ae4095b23c157da6397417b08f4da79"),
    "cycle146": (ROOT / "artifacts/cycle-146-balanced-highpass-mask-v1.json", "f78ab979c956af5932e5998d635d0844156fa9158169bb4294f453bd6f8f6d28"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle123"][0], "SEALED_JOINT_ALIAS_AMPLITUDE_PHASE_FACTORIZATION_BILINEAR_OPEN")
    validate_prior(INPUTS["cycle146"][0], "SEALED_SIGNED_HIGH_PASS_CELL_ENTROPY_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="strict_core_signed_cell_v1")
    module = __import__("conventions.strict_core_signed_cell_v1", fromlist=["phase_wedge_floor"])
    floor = module.phase_wedge_floor(
        support_ceiling=3.0,
        core_radius_scaled=1.0 / 36.0,
        atom_phase_wedge=pi / 12.0,
    )
    require(abs(floor - 0.5) < 1e-12, "strict-core half-plane floor")
    require("one half" in theorem["phase_wedge"], "phase-wedge lower bound")
    require("not bounded below" in theorem["actual_chart_scope"], "target-mass boundary")
    require("core--halo" in theorem["next_gate"], "bundle pivot")
    return {
        "artifact_id": "cycle-147-strict-core-signed-cell-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_COEFFICIENT_FAITHFUL_CORE_HALO_BUNDLE_OPEN",
        "claim_boundary": (
            "This artifact proves a positive real lower bound for a scoped "
            "strict-core signed cell under a nonnegative dyadic cutoff and a "
            "fixed coefficient-phase chart. It does not prove that the cell has "
            "target-sized mass and proves no paired norm, endpoint, complete "
            "moment, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 147"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "strict_core_signed_cell_theorem": {"epistemic_status": "PROVED", **theorem},
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "construct coefficient-faithful balanced core--halo bundles and "
                "prove a signed bundle estimate or a target-mass obstruction"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_147_strict_core_signed_cell_v1.py --write",
            "check_command": "python3 proof/build_cycle_147_strict_core_signed_cell_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_147_strict_core_signed_cell_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 147 sealer", output=OUTPUT, payload_factory=seal))
