#!/usr/bin/env python3
"""Seal Cycle 164's exact conductor-lowered ray-monoid section."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "cycle-164-oriented-ray-monoid-section-v1.json"

FROZEN_INPUTS = {
    "project_instructions": (ROOT / "AGENTS.md", "363495f0dbbe93e244b460c8eafb13247a8fb1f41be24f94c037ae9f6400c6f2"),
    "cycle_163_obstruction": (ROOT / "artifacts/cycle-163-spectral-ray-interface-v1.json", "165096dfab6f44c85c3d19bf1b1150d392a05310acd2b6c6da32686fd6b54240"),
    "preregistration": (ROOT / "docs/cycle-164-oriented-ray-monoid-preregistration-v1.md", "d0bb0c9eca6d10a92d9affe12b082504a6e11083fe3b97d6e203f7797c56efbc"),
    "decision_record": (ROOT / "docs/cycle-164-oriented-ray-monoid-section-v1.md", "6ff9f08f75c28039e5f00481692c9f85d1377b3a4b1ba32fd7926a73d65bd5c2"),
    "working_ledger": (ROOT / "discovery/cycle-164-oriented-ray-monoid-working-ledger.md", "5931bff479bc28918e0ca463c75aba22b11a9c7a413a2d4bf5786538e5fc135e"),
    "section_replay": (ROOT / "proof/verify_cycle_164_oriented_ray_monoid_section.py", "3b13e3b618ec5383b53eda80956460f696625e4a098d0023edfb747aaf3eb718"),
    "section_output": (ROOT / "discovery/cycle-164-oriented-ray-monoid-section-prototype-v1.json", "e63acf5500c60e1b6ec777141c324612786cdac307c7c9a5b6dfecea7320e6ec"),
    "test": (ROOT / "tests/test_cycle_164_oriented_ray_monoid_section.py", "fe8b8fa363865604baa80fb69c6b3d9d2046b1961e87a0d47157ccfb914412a4"),
    "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 164 ray-monoid section seal")
    frozen_hashes = freeze_inputs(ROOT, FROZEN_INPUTS)
    prototype = json.loads(
        (ROOT / "discovery/cycle-164-oriented-ray-monoid-section-prototype-v1.json").read_text()
    )
    summary = prototype["summary"]
    require(prototype["source"] == {"ray_cyc": [6], "generator_log": [1]}, "oriented C6 source changed")
    require(summary["rows_checked"] == 36, "wrong row count")
    require(summary["full_modulus_rows"] == 18, "full-modulus count changed")
    require(summary["lowered_modulus_rows"] == 18, "lowered-modulus count changed")
    require(summary["all_rows_in_projected_source_image"], "section totality failed")
    require(summary["full_modulus_recovery"], "full-modulus recovery failed")
    require(summary["orientation_anchors"] == {"3,5": 1, "3,4": 2}, "orientation anchors changed")
    return {
        "artifact_id": "cycle-164-oriented-ray-monoid-section-v1",
        "cycle": 164,
        "budget_ordinal": "B002",
        "epistemic_status": "PROVED",
        "status": "SEALED_CONDUCTOR_LOWERED_RAY_MONOID_SECTION",
        "claim_boundary": (
            "This exact finite result constructs only a convention-pinned conductor-lowered "
            "ray-monoid section. It proves no additive coefficient-to-logarithm operation, "
            "finite part, AFK cocycle compatibility, Stark identity, fusion theorem, or dimension-six TCC identity."
        ),
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": (
                "All 36 frozen characteristics admit the preregistered least-exponent section "
                "into one arithmetic-Frobenius-oriented C6 source; all 18 full-modulus rows "
                "recover their direct logs, including the two preserved anchors."
            ),
        },
        "exact_prototype": {
            "rows_checked": summary["rows_checked"],
            "full_modulus_rows": summary["full_modulus_rows"],
            "lowered_modulus_rows": summary["lowered_modulus_rows"],
            "all_rows_in_projected_source_image": summary["all_rows_in_projected_source_image"],
            "full_modulus_recovery": summary["full_modulus_recovery"],
            "orientation_anchors": summary["orientation_anchors"],
            "section_exponent_histogram": summary["section_exponent_histogram"],
            "source_output": "discovery/cycle-164-oriented-ray-monoid-section-prototype-v1.json",
        },
        "gate_outcome": {
            "d6_interface": "FINITE_RAY_MONOID_SECTION_SEALED_ADDITIVE_OPERATION_REQUIRED",
            "advance": "The common oriented finite ray-label state space is now exactly defined.",
            "remaining_bottleneck": "No outcome-blind additive coefficient-to-logarithm operation or AFK compatibility law has been defined.",
            "disallowed_pseudo_progress": [
                "treating the set-theoretic section as an AFK or TCC interface",
                "changing the least-exponent rule after inspecting additive or packet outputs",
                "returning to packet numerics without a defined operation",
            ],
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "Cycle 165/B003: preregister an outcome-blind additive-to-logarithmic operation "
                "class on the sealed section and seek exact compatibility or an exact falsifier of that named class."
            ),
        },
        "preregistration_preflight": {
            "cycle": 164,
            "manifest_sha256": sha256(ROOT / "docs/cycle-164-oriented-ray-monoid-preregistration-v1.md"),
            "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"},
        },
        "mentor_checkpoint": {
            "identity": "/root/decision_companion_2",
            "recommendation": "Seal Cycle 164/B002 only for the finite conductor-lowered ray-monoid section, then advance the interface gate.",
            "known_flaw": "The section is set-theoretic and supplies no coefficient operation, AFK compatibility, analytic continuation, or TCC implication.",
            "falsifier": "Replay discrepancy, nonfunctorial projection, failed anchor/direct-log recovery, or any claim beyond the frozen finite state space.",
            "next_action": "Preregister an outcome-blind additive-to-logarithmic operation class on this section and seek exact compatibility or an exact named-class falsifier.",
            "resolution": "ADOPTED",
        },
        "frozen_hashes": frozen_hashes,
        "replay": {
            "preflight_command": "research prereg check docs/cycle-164-oriented-ray-monoid-preregistration-v1.md --expected-cycle 164 --allow-head-drift",
            "prototype_command": "python3 proof/verify_cycle_164_oriented_ray_monoid_section.py --output discovery/cycle-164-oriented-ray-monoid-section-prototype-v1.json",
            "test_command": "python3 -m unittest tests.test_cycle_164_oriented_ray_monoid_section -v",
            "write_command": "python3 proof/build_cycle_164_oriented_ray_monoid_section_v1.py --write",
            "check_command": "python3 proof/build_cycle_164_oriented_ray_monoid_section_v1.py --check",
        },
        "runtime": runtime,
        "sealer": {"path": "proof/build_cycle_164_oriented_ray_monoid_section_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
