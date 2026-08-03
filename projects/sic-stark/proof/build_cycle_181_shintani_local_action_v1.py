#!/usr/bin/env python3
"""Seal Cycle 181's direct Shintani local-action result."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-181-shintani-local-action-v1.json"
INPUTS = {
    "instructions": (ROOT / "AGENTS.md", "363495f0dbbe93e244b460c8eafb13247a8fb1f41be24f94c037ae9f6400c6f2"),
    "section": (ROOT / "artifacts/cycle-164-oriented-ray-monoid-section-v1.json", "f1815f8641780570c15c7e9c6b40f9de8390358fb3dec0ac93aa311b78a6a26d"),
    "prior": (ROOT / "artifacts/cycle-180-local-global-artin-assembly-v1.json", "00ed9e7d014d1e53e828390f589ed5b97ceacb8fba2ddf502b8f318707b7817f"),
    "prereg": (ROOT / "docs/cycle-181-shintani-local-action-preregistration-v1.md", "24f308be98e6c9cfa28908d2c82b594dd99b5c698ce5121018eff2fe42a0a4b9"),
    "replay": (ROOT / "proof/verify_cycle_181_shintani_local_action.py", "980f1c1cca9534f0233835b12078ca04c86eecf849f64958774acfbab295a623"),
    "output": (ROOT / "discovery/cycle-181-shintani-local-action-prototype-v1.json", "beed812494154f058b970791112cf76d29ffe6960c32b3736e9e871f1d99f95f"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 181 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = json.loads((ROOT / "discovery/cycle-181-shintani-local-action-prototype-v1.json").read_text())
    summary = result["summary"]
    require((summary["rows_checked"], summary["shintani_edges_checked"], summary["third_returns_checked"], summary["conductor_transitions_checked"]) == (36, 36, 36, 18), "transport summary drift")
    require(summary["all_direct_relations_equal_independent_ray_differences"] and summary["all_third_returns_equal_kernel"], "transport validation drift")
    return {
        "artifact_id": "cycle-181-shintani-local-action-v1", "cycle": 181, "budget_ordinal": "B019", "epistemic_status": "PROVED", "status": "SEALED_DIRECT_SET_VALUED_SHINTANI_RAY_TRANSPORT",
        "claim_boundary": result["claim_boundary"],
        "outcome": {"epistemic_status": "PROVED", "statement": "The Shintani action induces an exact source-built, set-valued transport on the conductor-varying local ray quotient; it agrees independently with all ray-set differences and third returns."},
        "conventions": result["conventions"], "exact_prototype": {"source_output": "discovery/cycle-181-shintani-local-action-prototype-v1.json", "summary": summary},
        "gate_outcome": {"d6_interface": "SET_VALUED_RAY_TRANSPORT_EXACT_ADDITIVE_OPERATION_REQUIRED", "remaining_bottleneck": "Construct a section-free additive operation from AFK/characteristic data into a ray-group-algebra target, constrained by this direct transport, or exactly contain a named operation class.", "disallowed_pseudo_progress": ["calling set-valued transport an AFK coefficient map", "selecting exponents or reintroducing s,d", "claiming Stark, fusion, or TCC control"]},
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "The next distinct method is a section-free additive source module and ray-group-algebra operation with exact A6 equivariance and anchors."},
        "preregistration_preflight": {"cycle": 181, "manifest_sha256": sha256(ROOT / "docs/cycle-181-shintani-local-action-preregistration-v1.md"), "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"}},
        "frozen_hashes": frozen,
        "replay": {"preflight_command": "research prereg check docs/cycle-181-shintani-local-action-preregistration-v1.md --expected-cycle 181 --allow-head-drift", "prototype_command": "python3 proof/verify_cycle_181_shintani_local_action.py --output discovery/cycle-181-shintani-local-action-prototype-v1.json", "write_command": "python3 proof/build_cycle_181_shintani_local_action_v1.py --write", "check_command": "python3 proof/build_cycle_181_shintani_local_action_v1.py --check"},
        "runtime": runtime, "sealer": {"path": "proof/build_cycle_181_shintani_local_action_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
