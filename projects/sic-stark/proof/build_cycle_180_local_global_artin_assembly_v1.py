#!/usr/bin/env python3
"""Seal Cycle 180's local-global ray assembly."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-180-local-global-artin-assembly-v1.json"
INPUTS = {
    "instructions": (ROOT / "AGENTS.md", "363495f0dbbe93e244b460c8eafb13247a8fb1f41be24f94c037ae9f6400c6f2"),
    "section": (ROOT / "artifacts/cycle-164-oriented-ray-monoid-section-v1.json", "f1815f8641780570c15c7e9c6b40f9de8390358fb3dec0ac93aa311b78a6a26d"),
    "prior": (ROOT / "artifacts/cycle-179-p2-ray-quotient-v1.json", "0192cb7095b8e0c5e5507e92e0c5f06c79da51c9b41f39824f2fb656b341229d"),
    "prereg": (ROOT / "docs/cycle-180-local-global-artin-assembly-preregistration-v1.md", "859a5e89edfcfacb5ae145d0f18e40012b77df21631da6c34c34ef0fef207e3d"),
    "replay": (ROOT / "proof/verify_cycle_180_local_global_artin_assembly.py", "35f385cc6335fabc437afd19f33e351e328c2c11de38a20a3e0db4cb424af3db"),
    "output": (ROOT / "discovery/cycle-180-local-global-artin-assembly-prototype-v1.json", "a1715f66a7b4134d5a00d54e2e959445266ea0e5a63d595dc1f5c282dc8fc799"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 180 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = json.loads((ROOT / "discovery/cycle-180-local-global-artin-assembly-prototype-v1.json").read_text())
    summary = result["summary"]
    require((summary["rows_checked"], summary["distinct_lowered_moduli"], summary["transition_maps_checked"], summary["source_power_pairs_per_transition"]) == (36, 6, 18, 36), "assembly summary drift")
    require(summary["all_assembled_sets_equal_independent_ray_sets"], "independent ray equality drift")
    require(summary["orientation_anchors"] == {"3,5": [1], "3,4": [2]}, "orientation anchor drift")
    orders = [item["exact_sequence_quotient_order"] for item in result["moduli"]]
    require(orders == [1, 2, 2, 1, 2, 6], "ray quotient order drift")
    return {
        "artifact_id": "cycle-180-local-global-artin-assembly-v1", "cycle": 180, "budget_ordinal": "B018", "epistemic_status": "PROVED", "status": "SEALED_LOCAL_GLOBAL_RAY_ASSEMBLY_EXACT",
        "claim_boundary": result["claim_boundary"],
        "outcome": {"epistemic_status": "PROVED", "statement": "The six conductor-varying ray quotients and all 36 admissible exponent sets are exactly assembled from local residue-sign data modulo the global-unit image, with independent ray-arithmetic agreement."},
        "unit_theorem": result["unit_theorem"], "exact_prototype": {"source_output": "discovery/cycle-180-local-global-artin-assembly-prototype-v1.json", "summary": summary, "moduli": result["moduli"]},
        "gate_outcome": {"d6_interface": "RAY_ASSEMBLY_EXACT_CHARACTERISTIC_ACTION_LINK_REQUIRED", "remaining_bottleneck": "Relate the exact set-valued ray assembly to the A6/Shintani action on characteristics without choosing a section, then seek an additive coefficient/AFK operation.", "disallowed_pseudo_progress": ["calling ray assembly an additive coefficient operation", "using s,d or selected exponents to supply equivariance", "claiming TCC or fusion continuity"]},
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "The next engine, subject to companion review, is a direct A6/Shintani action on residue-sign/global-unit quotient classes and an exact set-valued equivariance test."},
        "preregistration_preflight": {"cycle": 180, "manifest_sha256": sha256(ROOT / "docs/cycle-180-local-global-artin-assembly-preregistration-v1.md"), "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"}},
        "frozen_hashes": frozen,
        "replay": {"preflight_command": "research prereg check docs/cycle-180-local-global-artin-assembly-preregistration-v1.md --expected-cycle 180 --allow-head-drift", "prototype_command": "python3 proof/verify_cycle_180_local_global_artin_assembly.py --output discovery/cycle-180-local-global-artin-assembly-prototype-v1.json", "write_command": "python3 proof/build_cycle_180_local_global_artin_assembly_v1.py --write", "check_command": "python3 proof/build_cycle_180_local_global_artin_assembly_v1.py --check"},
        "runtime": runtime, "sealer": {"path": "proof/build_cycle_180_local_global_artin_assembly_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
