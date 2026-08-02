#!/usr/bin/env python3
"""Seal Cycle 163's non-counted generated-handoff metadata correction."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "cycle-163-spectral-ray-interface-v2.json"
FROZEN_INPUTS = {
    "corrected_record": (
        ROOT / "artifacts/cycle-163-spectral-ray-interface-v1.json",
        "165096dfab6f44c85c3d19bf1b1150d392a05310acd2b6c6da32686fd6b54240",
    ),
    "correction_document": (
        ROOT / "docs/cycle-163-spectral-ray-interface-v2.md",
        "082e40d8f321c5842f1ac43ab3bef146e2907d673877e6d6ad873c4d7e05859f",
    ),
    "project_instructions": (
        ROOT / "AGENTS.md",
        "363495f0dbbe93e244b460c8eafb13247a8fb1f41be24f94c037ae9f6400c6f2",
    ),
    "test": (
        ROOT / "tests/test_cycle_163_status_correction.py",
        "6ecebb009141262e4d2db04f2689c859ae79bc6b4c08d5a2fdd63ed1d4486a1d",
    ),
    "sealing_scaffold": (
        ROOT / "proof/cycle_seal_v1.py",
        "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1",
    ),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 163 metadata correction")
    frozen_hashes = freeze_inputs(ROOT, FROZEN_INPUTS)
    original = json.loads(
        (ROOT / "artifacts/cycle-163-spectral-ray-interface-v1.json").read_text()
    )
    exact = original["exact_prototype"]
    require(original["cycle"] == 163, "wrong corrected cycle")
    require(original["budget_ordinal"] == "B001", "budget ordinal changed")
    require("remaining_target" not in original, "v1 does not require this correction")
    require(exact["eligible_rows"] == 18, "eligible result changed")
    require(exact["ineligible_rows"] == 18, "ineligible result changed")
    return {
        "artifact_id": "cycle-163-spectral-ray-interface-v2",
        "cycle": 163,
        "budget_ordinal": "B001",
        "record_kind": "METADATA_CORRECTION_NONCOUNTED",
        "correction_of": "cycle-163-spectral-ray-interface-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_FIXED_FULL_RAY_SELECTOR_METADATA_CORRECTION",
        "claim_boundary": (
            "This correction adds the generated-handoff target omitted from "
            "Cycle 163 v1. It changes no mathematical result, count, "
            "orientation anchor, gate boundary, or budget accounting."
        ),
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": (
                "The v1 artifact omitted remaining_target, causing the "
                "generated STATUS.md renderer to display no next target."
            ),
        },
        "inherited_exact_result": {
            "eligible_rows": exact["eligible_rows"],
            "ineligible_rows": exact["ineligible_rows"],
            "orientation_anchors": exact["orientation_anchors"],
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "Cycle 164/B002: preregister and test an "
                "orientation-preserving characteristic-dependent "
                "conductor-lowering/ray-monoid state space with an explicit "
                "map from every reduced object to one common "
                "arithmetic-Frobenius-oriented C6 primitive target."
            ),
        },
        "frozen_hashes": frozen_hashes,
        "replay": {
            "check_command": "python3 proof/build_cycle_163_spectral_ray_interface_v2.py --check",
            "test_command": "python3 -m unittest tests.test_cycle_163_status_correction -v",
            "write_command": "python3 proof/build_cycle_163_spectral_ray_interface_v2.py --write",
        },
        "runtime": runtime,
        "sealer": {
            "path": "proof/build_cycle_163_spectral_ray_interface_v2.py",
            "sha256": sha256(Path(__file__)),
        },
    }


if __name__ == "__main__":
    raise SystemExit(
        run_cli(description=__doc__, output=OUTPUT, payload_factory=payload)
    )
