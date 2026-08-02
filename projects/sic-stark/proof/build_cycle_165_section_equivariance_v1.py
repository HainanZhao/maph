#!/usr/bin/env python3
"""Seal Cycle 165's exact pointwise section-equivariance obstruction."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "cycle-165-section-equivariance-v1.json"
FROZEN_INPUTS = {
    "project_instructions": (ROOT / "AGENTS.md", "363495f0dbbe93e244b460c8eafb13247a8fb1f41be24f94c037ae9f6400c6f2"),
    "cycle_164_section": (ROOT / "artifacts/cycle-164-oriented-ray-monoid-section-v1.json", "f1815f8641780570c15c7e9c6b40f9de8390358fb3dec0ac93aa311b78a6a26d"),
    "preregistration": (ROOT / "docs/cycle-165-section-equivariance-preregistration-v1.md", "e9323694fd97174f3d74033a92d9dc9bef39b36927943361f52814a7a9265290"),
    "decision_record": (ROOT / "docs/cycle-165-section-equivariance-v1.md", "3111b17cb50e39ad6e7d77f37f0edab5b3f67fc33e2567e5f46f2b99471a620c"),
    "working_ledger": (ROOT / "discovery/cycle-165-section-equivariance-working-ledger.md", "85c03fb21eef207d5805ba8c56a2706010555c8198acc152d01eab9c2af7780f"),
    "equivariance_replay": (ROOT / "proof/verify_cycle_165_section_equivariance.py", "6b9b2dcc9584dbb901b0cddd74487ee46b9cc4cf57880bb0e9001fe3636c83f8"),
    "equivariance_output": (ROOT / "discovery/cycle-165-section-equivariance-prototype-v1.json", "37fe29c7a13eb24ef39c1f1f603e3387262919c1a775d2195d7baf145082a323"),
    "test": (ROOT / "tests/test_cycle_165_section_equivariance.py", "b9068888004b6d002f91d27bd2d604da8c90a7d060d0614a4247d1af48847ad8"),
    "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 165 section-equivariance seal")
    frozen_hashes = freeze_inputs(ROOT, FROZEN_INPUTS)
    prototype = json.loads(
        (ROOT / "discovery/cycle-165-section-equivariance-prototype-v1.json").read_text()
    )
    summary = prototype["summary"]
    witness = summary["first_fibre_instability_witness"]
    require(summary["rows_checked"] == 36, "wrong row count")
    require(summary["target_actions_checked"] == 46656, "incomplete target-action census")
    require(summary["compatible_target_actions"] == 0, "unexpected compatible target action")
    require(not summary["section_equivariant_descent_exists"], "descent unexpectedly exists")
    require(witness == {
        "source_label": 0, "first_point": [0, 0], "first_successor_label": 0,
        "second_point": [0, 1], "second_successor_label": 3,
        "successor_labels": [0, 1, 2, 3, 4],
    }, "ordered fibre witness changed")
    return {
        "artifact_id": "cycle-165-section-equivariance-v1",
        "cycle": 165,
        "budget_ordinal": "B003",
        "epistemic_status": "PROVED",
        "status": "SEALED_POINTWISE_SECTION_EQUIVARIANCE_FALSIFIED",
        "claim_boundary": (
            "This exact finite result falsifies only deterministic pointwise label-respecting "
            "section pushforwards with a target set action. It does not rule out non-pointwise, "
            "nonlinear, fibre-resolved, characteristic-dependent, or analytic coefficient-to-logarithm operations."
        ),
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": "No one of the 46,656 target maps C6->C6 intertwines the preregistered pointwise section pushforward with the frozen Shintani action.",
        },
        "exact_prototype": {
            "rows_checked": summary["rows_checked"],
            "target_actions_checked": summary["target_actions_checked"],
            "compatible_target_actions": summary["compatible_target_actions"],
            "section_equivariant_descent_exists": summary["section_equivariant_descent_exists"],
            "fibre_instability_witness_count": summary["fibre_instability_witness_count"],
            "first_fibre_instability_witness": witness,
            "source_output": "discovery/cycle-165-section-equivariance-prototype-v1.json",
        },
        "gate_outcome": {
            "d6_interface": "POINTWISE_SECTION_EQUIVARIANT_OPERATION_FALSIFIED",
            "falsified_operation_class": "deterministic_pointwise_label_respecting_section_pushforward",
            "remaining_bottleneck": "A fibre-resolved or otherwise non-pointwise outcome-blind operation remains to be constructed and tested.",
            "disallowed_pseudo_progress": [
                "treating the pointwise-class obstruction as an interface or TCC no-go",
                "discarding the fibre coordinate again before proving a replacement covariance law",
                "fitting a target action after inspecting a continuous packet or Stark value",
            ],
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Cycle 166/B004: preregister a fibre-resolved C6-torsor state space, frozen multiplier law, preserved anchors, and the smallest exact intertwining-or-falsifier test."
        },
        "preregistration_preflight": {
            "cycle": 165,
            "manifest_sha256": sha256(ROOT / "docs/cycle-165-section-equivariance-preregistration-v1.md"),
            "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"},
        },
        "mentor_checkpoint": {
            "identity": "/root/decision_companion_2",
            "recommendation": "Seal Cycle 165/B003 only for the frozen pointwise label-respecting section-equivariant operation class; authorize the fibre-resolved C6-torsor/multiplier engine.",
            "known_flaw": "The obstruction says nothing about non-pointwise, nonlinear, fibre-resolved, characteristic-dependent, or analytic operations.",
            "falsifier": "Any replay/census discrepancy, transform-direction error, invalid collision witness, or broader interpretation invalidates the seal.",
            "next_action": "Preregister a fibre-resolved C6-torsor state space, frozen multiplier law, preserved orientation/anchors, and the smallest exact intertwining-or-falsifier test.",
            "resolution": "ADOPTED",
        },
        "frozen_hashes": frozen_hashes,
        "replay": {
            "preflight_command": "research prereg check docs/cycle-165-section-equivariance-preregistration-v1.md --expected-cycle 165 --allow-head-drift",
            "prototype_command": "python3 proof/verify_cycle_165_section_equivariance.py --output discovery/cycle-165-section-equivariance-prototype-v1.json",
            "test_command": "python3 -m unittest tests.test_cycle_165_section_equivariance -v",
            "write_command": "python3 proof/build_cycle_165_section_equivariance_v1.py --write",
            "check_command": "python3 proof/build_cycle_165_section_equivariance_v1.py --check",
        },
        "runtime": runtime,
        "sealer": {"path": "proof/build_cycle_165_section_equivariance_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
