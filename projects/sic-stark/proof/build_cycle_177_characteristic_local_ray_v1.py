#!/usr/bin/env python3
"""Seal Cycle 177's p3-local-record collision result."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-177-characteristic-local-ray-v1.json"
INPUTS = {
    "instructions": (ROOT / "AGENTS.md", "363495f0dbbe93e244b460c8eafb13247a8fb1f41be24f94c037ae9f6400c6f2"),
    "section": (ROOT / "artifacts/cycle-164-oriented-ray-monoid-section-v1.json", "f1815f8641780570c15c7e9c6b40f9de8390358fb3dec0ac93aa311b78a6a26d"),
    "pairing": (ROOT / "artifacts/cycle-175-leading-residue-pairing-v1.json", "9ec7b4bf1a8a8ca87e586988e6e6d14e85aa597e163be032c9e668d128c593bb"),
    "transport": (ROOT / "artifacts/cycle-176-local-pairing-transport-v1.json", "b6e2d894d2f9f4f3434c1da08e655ed4e14ba3814e8ef14c84e96049909e1e74"),
    "prereg": (ROOT / "docs/cycle-177-characteristic-local-ray-preregistration-v1.md", "1cd0f214f53462ce855cf9265853fb038f961f48967e3ccc90e0eccacc01400f"),
    "replay": (ROOT / "proof/verify_cycle_177_characteristic_local_ray.py", "987e05f080a1b32216bbdc637da6a54abbe72f89db2390deede5364b060dd341"),
    "output": (ROOT / "discovery/cycle-177-characteristic-local-ray-prototype-v1.json", "fd45282f8db0cb4327ef037a224acac80c533e05f5b96a9a934dee88e33cd3a4"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 177 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = json.loads((ROOT / "discovery/cycle-177-characteristic-local-ray-prototype-v1.json").read_text())
    summary = result["summary"]
    require((summary["rows_checked"], summary["collision_count"], summary["map_determinacy"]) == (36, 8, False), "collision summary drift")
    require(summary["orientation_anchors"] == {"3,5": 1, "3,4": 2}, "anchor drift")
    return {
        "artifact_id": "cycle-177-characteristic-local-ray-v1", "cycle": 177, "budget_ordinal": "B015", "epistemic_status": "PROVED", "status": "SEALED_P3_LOCAL_RECORD_TO_LEAST_EXPONENT_FALSIFIED", "claim_boundary": result["claim_boundary"],
        "outcome": {"epistemic_status": "PROVED", "statement": "Eight preregistered p3-local records occur with distinct conductor-lowered least ray exponents, falsifying that named record-to-selected-exponent map."},
        "exact_prototype": {"source_output": "discovery/cycle-177-characteristic-local-ray-prototype-v1.json", "summary": summary, "collisions": result["collisions"]},
        "gate_outcome": {"d6_interface": "P3_LOCAL_RECORD_INSUFFICIENT_FOR_SELECTED_EXPONENT_FULL_CRT_SET_TEST_REQUIRED", "remaining_bottleneck": "Use a p2×p3 CRT local record and compare equal-record fibres with functorially defined admissible ray-exponent sets, not the least-exponent section.", "disallowed_pseudo_progress": ["calling the section-dependent collision an intrinsic ray-class no-go", "using s or d in the source record", "adding target-derived local features"]},
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "Cycle 178/B016: preregister the full modulus-6 CRT local record and test equal-record fibres against admissible exponent sets with no section selection."},
        "preregistration_preflight": {"cycle": 177, "manifest_sha256": sha256(ROOT / "docs/cycle-177-characteristic-local-ray-preregistration-v1.md"), "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"}},
        "frozen_hashes": frozen,
        "replay": {"preflight_command": "research prereg check docs/cycle-177-characteristic-local-ray-preregistration-v1.md --expected-cycle 177 --allow-head-drift", "prototype_command": "python3 proof/verify_cycle_177_characteristic_local_ray.py --output discovery/cycle-177-characteristic-local-ray-prototype-v1.json", "write_command": "python3 proof/build_cycle_177_characteristic_local_ray_v1.py --write", "check_command": "python3 proof/build_cycle_177_characteristic_local_ray_v1.py --check"},
        "runtime": runtime, "sealer": {"path": "proof/build_cycle_177_characteristic_local_ray_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
