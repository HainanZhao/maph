#!/usr/bin/env python3
"""Seal Cycle 47's connected-patch affine global-section theorem."""
from __future__ import annotations

import json
from pathlib import Path

from check_cycle_47_affine_descent import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle47-affine-descent"
OUTPUT = ROOT / "artifacts/cycle-47-b047-lrc-global-affine-descent-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-47-b047-lrc-global-affine-descent-preregistration-v1.md", "8cb7bb33ba2421f0a1303e902d6d4ee0143fb5936af77ea54f0d7b125f257777"),
    "cycle46_artifact": (ROOT / "artifacts/cycle-46-b046-lrc-global-cech-quotient-v1.json", "2bc5de2d3ce9e961bca63298ac163ccd53c523476e4bed2840aa267df17fb00d"),
    "idea_selection": (ROOT / "discovery/cycle47_affine_descent_idea_selection.md", "428729e61825a3702daad1b9baa8ecf6f63dc0b1438bc67006db450b7d658071"),
    "selector": (ROOT / "discovery/lrc_affine_descent_select.py", "a57d4cf96faf4078ac58c82e0d8a1acf5d77d5ee1ce5cfdca85ab364114e3e13"),
    "selection": (OUT / "selection.json", "eac88f41ac6ae261d407ba4e6026e121e25435fafe4a66911a3645454c4f5ac1"),
    "selection_timing": (OUT / "run-selection.time", "8881433f400f7616c8c64715e572db2e7492966ba05826479d78738ebca403db"),
    "actual_engine": (ROOT / "discovery/lrc_affine_descent_actual.py", "2e8459a9e65ef7ccf7216c79bec5e129430b5140ad6e382c93e0acee165dbe24"),
    "actual_result": (OUT / "canonical-section-localized.json", "e6052fe550514d8980ca21b0cee7f9f6d50bc0149de22e57da10b80e03274bbf"),
    "actual_timing": (OUT / "run-canonical-section-localized.time", "f2dafc337ae8ade10ad632846ea04c19331f188047a289f28b859d50c99ca5a1"),
    "control_engine": (ROOT / "discovery/lrc_affine_descent_controls.py", "4901b6bc15f198f9825e9d537de14bdaa6a2eff62b33fd3f9a9090d7ea60bf0b"),
    "control_result": (OUT / "generic-controls.json", "520b65cea08effcdb1184f1d8b23c406f7d9d60a07d97909e0982f0ed21deaa1"),
    "control_timing": (OUT / "run-generic-controls.time", "36f6d52b916dc6c91bc1f2fc2bfc12db8e01a9009059146cbeb1ae11dfe665b5"),
    "soundness": (ROOT / "proof/cycle_47_affine_descent_soundness.md", "86993552f8c43dfd644599b16e44005631481ed6beb845a441b86c4dce5585a4"),
    "independent_replay": (ROOT / "proof/replay_cycle_47_affine_descent_independent.py", "5af56164b4aecf1813e8bf88a6af7cc2d94dc9a789341982e55bc495bb8fc236"),
    "independent_result": (OUT / "independent-replay.json", "6260466f92df7db5a4eb7b637348079f33fc6b50781afad3e0175a3299f485b8"),
    "independent_timing": (OUT / "run-independent-full.time", "dc693a7e3436ce1046c9d8816e0ed5005d17d9c3c6dc9e0ff31411f11667189e"),
    "audit": (ROOT / "proof/check_cycle_47_affine_descent.py", "fc6b0f9326cddcb84b892449d37127093281d9e318b392ff229bc492ac054184"),
    "test": (ROOT / "tests/test_cycle_47_affine_descent.py", "d344b312c9e0d23d0b9f01ec0bd939d3c02f2e2720b3698d8bdb984df034ceef"),
    "cycle41_closure": (ROOT / "discovery/out/cycle41-multiplied-ideal/zero-support-closure.json", "a1f742592375d035f68d3dcd0ecde65c4ee6e7b78c96fa2a1ed18362e979037e"),
    "cycle29_interface": (ROOT / "discovery/out/cycle29-ownership-blocker/result.json", "b213f8b790b2f53e2de30d244ead973143973e236083d24b38fffb5234271f15"),
    "cycle43_coupling": (ROOT / "discovery/out/cycle43-moment-h2-coupling/canonical-coupling.json", "00737a038508ee4220b8ff158552afd976fab8e23194980de26879046566795b"),
    "cycle44_selection": (ROOT / "discovery/out/cycle44-nonanchor-coupling/selection.json", "22f517ae6c7eb1f11a65cf14d18ec0a918948cd290af08fdf0d2ef0e711fd1ff"),
    "cycle44_coupling": (ROOT / "discovery/out/cycle44-nonanchor-coupling/coupling.json", "32afe4526846a73f63969d8b1c95142a0bb94075b95273ec61ef31bc5f041eb9"),
    "ownership_interface": (ROOT / "discovery/lrc_ownership_functional.py", "2e4d63706aff0f0c71f13c06bd0dc63374f28c82a1e9ae4fd2b241141d843589"),
    "signed_moments": (ROOT / "discovery/lrc_signed_ownership_moments.py", "cb76981ee928abd7b25bf665a83a55e883587c2c89b26b35282226a0afbae5f3"),
    "transport": (ROOT / "discovery/lrc_multiplied_fill_probe.py", "3bb02b3fcc56f6d5f83c0719556bf41e5a7d1821ffb61c79150160c9e44990f6"),
    "sparse_solver": (ROOT / "discovery/lrc_moment_h2_coupling.py", "935e34313e50b324933c79a343a6f23747c66bb3845ea4ddbf9a9c1cefdb4870"),
    "face_builder": (ROOT / "discovery/lrc_nonanchor_coupling.py", "1508f00e1eeb66e104b0890dcb5019405c414ac95b13ff80c9e85232f5792945"),
    "localized_solver": (ROOT / "discovery/lrc_cech_total.py", "91e267ee6f661f632bc417a3cbdf76453c4a4f934d12717c9ecbb2363ce19272"),
    "complex_builder": (ROOT / "discovery/lrc_morse_critical_projection.py", "669991dedd193fa7d27aef1fa47995bac5fe59b2e5fb5858c7eafd0509326bb2"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "preregistration_validator": (ROOT / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def payload():
    checked = audit()
    selection = json.loads((OUT / "selection.json").read_text())
    actual = json.loads((OUT / "canonical-section-localized.json").read_text())
    independent = json.loads((OUT / "independent-replay.json").read_text())
    controls = json.loads((OUT / "generic-controls.json").read_text())
    return {
        "artifact_id": "cycle-47-b047-lrc-global-affine-descent-v1",
        "budget_ordinal": "B047", "cycle": 47,
        "record_type": "PROVED_CONNECTED_PATCH_AFFINE_GLOBAL_SECTION",
        "recorded_at_utc": "2026-08-05T03:26:06Z", "status": "SEALED", "epistemic_status": "PROVED",
        "outcome": "Raw occurrence-labeled and compressed unordered-face affine systems are exactly equivalent. On a new outcome-blind connected patch of 256 p199 type quadruples, the canonical lower-transport face rule gives one exact global rational section across all 447 incidence cycles. A full independent target-only audit checks all 185 face classes, 1,024 occurrences, 839 gluing identifications, and 256 fills with zero residuals.",
        "claim_boundary": "This is a generic finite descent equivalence and a finite global-section theorem on one frozen patch. It is not universal sheaf acyclicity, a new universal canonical-face construction, a full degree-four functional, a leaf certificate, or LRC(13).",
        "descent_theorem": {
            "statement": "Stabilizer-invariant canonical face coordinates and occurrence-labeled coordinates are related by explicit mutually inverse transport maps; exact gluing elimination preserves solutions and affine obstruction pairings.",
            "coefficient_ring": "Q",
            "rank_control": independent["descent_rank_control"],
        },
        "patch": {
            "selection": "outcome-blind SHA256 connected frontier, excluding all Cycle 43/44 quadruples",
            "quadruples": selection["selected_quadruples"], "old_interfaces_excluded": selection["old_interfaces"],
            **selection["incidence"],
        },
        "global_section": {
            "section_route": actual["section_route"], "face_classes": actual["face_classes"],
            "pair_classes": actual["pair_classes"], "local_stalks_nonempty": actual["local_stalks_nonempty"],
            "fill_routes": actual["fill_routes"], "face_routes": actual["face_routes"],
            "maximum_fill_nonzero": actual["maximum_fill_nonzero"],
            "maximum_coefficient_bits": actual["maximum_coefficient_bits"],
        },
        "negative_control": controls["inconsistent_three_stalk_loop"],
        "independent_replay": {
            "status": independent["status"], **independent["full_residual_audit"],
            "target_pair_flows_checked": independent["target_pair_flows_checked"],
            "material_route_records": independent["selected_records"],
        },
        "strategic_interpretation": "Shared-face compatibility alone is not the missing p199 obstruction on this dense unseen patch. The result reuses the canonical lower-transport face rule, so the next engine must seek a symbolic confluence/rewrite theorem or its smallest critical-pair falsifier rather than another finite census.",
        "cycle_decision": {
            "companion_identity": "/root/darwin_cycle25_short",
            "initial_review_flaw": "The preliminary independent route reconstructed only 56 of 185 faces and seven fills.",
            "repair": "Kept Cycle 47 live and completed the requested full independent residual audit over every face, occurrence, gluing identification, stabilizer, orientation, and fill.",
            "outcome": "SEAL_C47_AND_OPEN_CANONICAL_FACE_REWRITE_CONFLUENCE",
            "next_question": "Is the lower-pair-transport face rule locally confluent on every frozen critical-pair pattern of support masks and deleted diagonals, yielding a uniform symbolic fill rule?",
            "falsifier": "A smallest exact critical-pair diamond whose two admissible reductions give unequal constrained fills, or a raw interface violating the proposed formula.",
        },
        "audit": checked,
        "resources": {
            "worker_cpus": [1, 2], "reserved_cpu": 3,
            "selection_wall_seconds": selection["wall_seconds"],
            "actual_wall_seconds": actual["wall_seconds"], "actual_peak_rss_kib": 1173024,
            "independent_wall_seconds": independent["wall_seconds"], "independent_peak_rss_kib": 1152364,
        },
        "runtime": check_runtime("Cycle 47 affine descent"),
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "replay": {
            "selection_command": "taskset -c 2 .venv/bin/python discovery/lrc_affine_descent_select.py",
            "controls_command": "taskset -c 2 .venv/bin/python discovery/lrc_affine_descent_controls.py",
            "actual_command": "taskset -c 1-2 .venv/bin/python discovery/lrc_affine_descent_actual.py",
            "independent_command": "taskset -c 2 .venv/bin/python proof/replay_cycle_47_affine_descent_independent.py",
            "audit_command": ".venv/bin/python proof/check_cycle_47_affine_descent.py",
            "test_command": ".venv/bin/python -m unittest tests.test_cycle_47_affine_descent -v",
            "check_command": ".venv/bin/python proof/build_cycle_47_lrc_affine_descent.py --check",
        },
        "sealer": {"path": "proof/build_cycle_47_lrc_affine_descent.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
