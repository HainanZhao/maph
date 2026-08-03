#!/usr/bin/env python3
"""Seal Cycle 182's collapsed-target linear-operation obstruction."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-182-section-free-linear-operation-v1.json"
INPUTS = {
    "instructions": (ROOT / "AGENTS.md", "363495f0dbbe93e244b460c8eafb13247a8fb1f41be24f94c037ae9f6400c6f2"),
    "assembly": (ROOT / "artifacts/cycle-180-local-global-artin-assembly-v1.json", "00ed9e7d014d1e53e828390f589ed5b97ceacb8fba2ddf502b8f318707b7817f"),
    "transport": (ROOT / "artifacts/cycle-181-shintani-local-action-v1.json", "539e7179b060c471603154331327843b909487125b80278c2d76d346a3d930e4"),
    "prereg": (ROOT / "docs/cycle-182-section-free-linear-operation-preregistration-v1.md", "c66852b77b1bd6e002a77eb8293858cdcb846541bcc4a2c72d9844c4893896ca"),
    "replay": (ROOT / "proof/verify_cycle_182_section_free_linear_operation.py", "2113e889261c1506ccfc484aff9dc2876f3e39f6ae4e6b6d4c518447fd6c68b9"),
    "output": (ROOT / "discovery/cycle-182-section-free-linear-operation-prototype-v1.json", "672f42b44aba5a4d80a5732fe2f0ef67af724810300f39063d39814fb650f273"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 182 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = json.loads((ROOT / "discovery/cycle-182-section-free-linear-operation-prototype-v1.json").read_text())
    summary = result["summary"]
    solve = summary["action_solve"]
    require((summary["rows_checked"], summary["conductor_pushforwards_checked"], solve["equivariance_equations"], solve["unknowns"], solve["measure_span_rank"]) == (36, 36, 216, 36, 6), "operation census drift")
    require(not solve["consistent"] and not solve["equivariance_consistent_without_augmentation"], "linear obstruction drift")
    require(len(solve["identical_source_measure_conflicts"]) == 8, "collision witness count drift")
    require(summary["orientation_anchors"] == {"3,5": [1], "3,4": [2]}, "anchor drift")
    return {
        "artifact_id": "cycle-182-section-free-linear-operation-v1", "cycle": 182, "budget_ordinal": "B020", "epistemic_status": "PROVED", "status": "SEALED_COLLAPSED_UNIFORM_RAY_TARGET_LINEAR_CLASS_EMPTY",
        "claim_boundary": result["claim_boundary"],
        "outcome": {"epistemic_status": "PROVED", "statement": "No rational linear target action on the collapsed Q[C6] can make the canonical uniform assembled-set map Shintani equivariant; source-measure collisions already contradict equivariance."},
        "conventions": result["conventions"], "exact_prototype": {"source_output": "discovery/cycle-182-section-free-linear-operation-prototype-v1.json", "summary": summary},
        "gate_outcome": {"d6_interface": "COLLAPSED_UNIFORM_RAY_TARGET_FALSIFIED_CONDUCTOR_GRADED_TARGET_REQUIRED", "remaining_bottleneck": "Retain conductor grade in a section-free ray-algebra target and derive direct Shintani inter-grade maps before testing an additive operation.", "disallowed_pseudo_progress": ["discarding conductor grade again", "generalizing the obstruction to graded, nonlinear, fibre-resolved, or analytic operations", "using selected exponents, s,d, or target labels"]},
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "The next distinct method is the direct sum of six conductor-graded ray algebras with exact Shintani inter-grade maps."},
        "preregistration_preflight": {"cycle": 182, "manifest_sha256": sha256(ROOT / "docs/cycle-182-section-free-linear-operation-preregistration-v1.md"), "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"}},
        "frozen_hashes": frozen,
        "replay": {"preflight_command": "research prereg check docs/cycle-182-section-free-linear-operation-preregistration-v1.md --expected-cycle 182 --allow-head-drift", "prototype_command": "python3 proof/verify_cycle_182_section_free_linear_operation.py --output discovery/cycle-182-section-free-linear-operation-prototype-v1.json", "write_command": "python3 proof/build_cycle_182_section_free_linear_operation_v1.py --write", "check_command": "python3 proof/build_cycle_182_section_free_linear_operation_v1.py --check"},
        "runtime": runtime, "sealer": {"path": "proof/build_cycle_182_section_free_linear_operation_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
