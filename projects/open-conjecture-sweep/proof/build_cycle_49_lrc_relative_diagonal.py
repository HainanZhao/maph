#!/usr/bin/env python3
"""Seal Cycle 49's relative diagonal-fiber contraction boundary."""
from __future__ import annotations

import json
from pathlib import Path

from check_cycle_49_relative_diagonal import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle49-relative-diagonal"
OUTPUT = ROOT / "artifacts/cycle-49-b049-lrc-relative-diagonal-contraction-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-49-b049-lrc-relative-diagonal-contraction-preregistration-v1.md", "8ee9dbf432d3d03aa652b7a75934206ef1ab3676bab71c76ea4a1abf0f311d64"),
    "cycle48_artifact": (ROOT / "artifacts/cycle-48-b048-lrc-cube-rewrite-v1.json", "b9069dca26e99ab13d789806e4e71c16d9421bde5053e8ddf7a4766eb97d2836"),
    "idea_selection": (ROOT / "discovery/cycle49_relative_diagonal_idea_selection.md", "1ea09a57585f4eedeaf63fe9caf17b14d5771fdaa5067c38f2e1b00fb2f2b28e"),
    "relative_module": (ROOT / "discovery/lrc_relative_diagonal.py", "3d73fad7547a0a1448fc67898607b8588c0aa06babf2cfa6ffb7f0079d43175f"),
    "controls_engine": (ROOT / "discovery/lrc_relative_diagonal_controls.py", "f5b7cb8dcc3be8c101db6e9aed158964e90e370c2da1454c8c795488896d7e59"),
    "inventory_engine": (ROOT / "discovery/lrc_relative_diagonal_inventory.py", "74bf5a5c73e4919bd08b8b97d7c195a02887fca4a91444449a9399b88b607568"),
    "support_engine": (ROOT / "discovery/lrc_relative_diagonal_support_classify.py", "cc167581d64628b13e4c15e464c61a0dc1117d6d785b0f15622641c13ec3dcd2"),
    "deletion_engine": (ROOT / "discovery/lrc_relative_diagonal_deletion_classify.py", "3e77e6fd852dee8e6414dca49ac32f5b41abe7da7312da6cb20ce265ad05e6f4"),
    "full_audit_engine": (ROOT / "discovery/lrc_relative_diagonal_full_audit.py", "341cef8a1397f2371d6ad2a5d300a230ac93d820b84682affa3104e6901a77f9"),
    "controls": (OUT / "generic-controls.json", "51ebdab88fc54d98e69e64cb85a126511157dd0d44b7cd1ca9950d2e37a4cff1"),
    "inventory": (OUT / "inventory.json", "13b6d896b8876624f66d3709a3df2ddc6580135a3730376911f7925de728489a"),
    "support_classification": (OUT / "support-classification.json", "7f73938494401525d7f3e2bad907606f4bcbaa8934958520190d0e864db6ae31"),
    "deletion_classification": (OUT / "deletion-classification.json", "b82dc096b22acf3f8c292c1e5b206af87cdd0f6b4b2818de61a48a1d909b1743"),
    "full_audit": (OUT / "full-audit.json", "33bfa7d3c89d7556a61f1858ca37042341406eb282a8682893b9eeebe608852d"),
    "terminal_audit": (OUT / "terminal-audit.json", "de191c66a97d0878b95b0cbb99654aa8dabc3d2b3063039576bea4b68c0a9bcf"),
    "terminal_engine": (ROOT / "proof/check_cycle_49_terminal_exception.py", "49713a90d4b2259649931e82b4c4823c1480f223091bbde5b2c0c79a09e97d73"),
    "independent_replay": (ROOT / "proof/replay_cycle_49_relative_diagonal_independent.py", "62d805e6646a1b7336aa2ac7228a2669df5faf0606e7f6bf8668d04cbd5e36dc"),
    "independent_result": (OUT / "independent-replay.json", "191a0f67c29c975008ea71cca52c4c5e1e80e78d4d40e991d67fd439757a2b64"),
    "independent_diagnostic": (OUT / "independent-diagnostic.json", "0f13be3185ce5139d4715c2d44fcb2dd61fa3fc28febb49dc9464ad73e2540ae"),
    "soundness": (ROOT / "proof/cycle_49_relative_diagonal_soundness.md", "592474d210a348ecf2e65643a8546d5126281b102d5c4df77b7cecaea9d86b68"),
    "audit": (ROOT / "proof/check_cycle_49_relative_diagonal.py", "b8abc5cd83da3c94596ee548c921eb3603a139c4462f37e7069d25675852dcef"),
    "test": (ROOT / "tests/test_cycle_49_relative_diagonal.py", "6cf82cdcc65f0b8acdbebfe2fd2de20eaea1d56fe26a943fe244b108dff4b52d"),
    "full_audit_timing": (OUT / "run-full-audit.time", "5427b2dee52524242d7c8370a3d4b3ee4ba5db5a442490dbb27c05e366d43a9a"),
    "independent_timing": (OUT / "run-independent.time", "01634501760c063b80ba07909dbf5722904565d3c5fc5a8d3c35868ead590510"),
    "cube_rewrite": (ROOT / "discovery/lrc_cube_rewrite.py", "106a237501b9bf115e8df265c2075f0605c6a7776c1bd8fdd870adc1b01e4de9"),
    "cycle41_closure": (ROOT / "discovery/out/cycle41-multiplied-ideal/zero-support-closure.json", "a1f742592375d035f68d3dcd0ecde65c4ee6e7b78c96fa2a1ed18362e979037e"),
    "cycle29_interface": (ROOT / "discovery/out/cycle29-ownership-blocker/result.json", "b213f8b790b2f53e2de30d244ead973143973e236083d24b38fffb5234271f15"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "preregistration_validator": (ROOT / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def payload():
    checked = audit()
    controls = json.loads((OUT / "generic-controls.json").read_text())
    terminal = json.loads((OUT / "terminal-audit.json").read_text())
    return {
        "artifact_id": "cycle-49-b049-lrc-relative-diagonal-contraction-v1",
        "budget_ordinal": "B049", "cycle": 49,
        "record_type": "PROVED_RELATIVE_DIAGONAL_CONTRACTION_BOUNDARY",
        "recorded_at_utc": "2026-08-05T08:10:00Z", "status": "SEALED", "epistemic_status": "PROVED",
        "outcome": "The frozen two-stage diagonal-fiber cube-packet formula is a generic contraction under its explicit buffer hypotheses and closes 382,453,314 of 382,453,319 raw-valid unordered p199 type triples. Exactly five interfaces fail only the frozen pairwise-distinct buffer surrogate. The first, (4,4,5), is exactly fillable by an allowed repeated-owner alternative, proving BUFFER_INCOMPLETE rather than terminal relative homology. The remaining four labels are retained as unclassified under the surrogate.",
        "claim_boundary": "This proves the frozen generic support theorem and its complete p199-domain census, plus a scoped no-go for the pairwise-distinct buffer formula. It does not prove an unrestricted relative contraction, fill the other four exceptions, define a global lift map, prove every quadruple fills, or prove LRC(13).",
        "generic_theorems": {
            "cube_kernel": "Every alternating 2x2x2 cube preserves all three pair marginals.",
            "fiber_contraction": "A deleted pair fiber has total zero; a no-spill packet transfers every nonterminal coefficient to one terminal, which then vanishes.",
            "support_five": "Support size at least five in every owner coordinate supplies the frozen triple and pair buffers.",
        },
        "full_domain": {
            "raw_valid_unordered_type_triples": checked["raw_valid_type_triples"],
            "formula_closed": checked["frozen_formula_closed"],
            "buffer_incomplete": checked["buffer_incomplete"],
            "generic_support_closed": checked["generic_support_closed"],
            "deletion_signature_closed": checked["deletion_signature_closed"],
            "residual_counts": checked["residual_counts"],
            "exception_types": checked["exception_types"],
        },
        "first_exception": {
            "types": terminal["types"], "classification": terminal["classification"],
            "cube_kernel_dimension": terminal["cube_kernel_dimension"],
            "interpretation": "The unique full-support cube with repeated owner alternative is allowed and fills the defect; pairwise-distinctness was an overly strong sufficient surrogate.",
        },
        "controls": controls,
        "independent_replay": {
            "status": "PASS", "method": "Separately implemented reverse-order reconstruction without importing the principal relative-diagonal module.",
            "canonical_order_correction": "The first independent full replay exposed an all-same-support output-order mismatch. The bug was contained, a final canonical sort was added, and the full replay then agreed exactly on counts and all five labels.",
        },
        "cycle_decision": {
            "companion_identity": "/root/darwin_cycle25_short",
            "companion_advice": "Seal C49 as a pattern theorem and open one distinct deletion-aware packet block; do not make five post hoc repairs.",
            "selected_next_question": "Can a deletion-aware triple packet reuse alternate owners exactly when every cube vertex satisfies the actual deleted-pair constraints, and thereby close every (2,2,2) and (2,2,4) exception pattern without creating any new full-domain residual class?",
            "falsifier": "Any forbidden spill, nonzero preserved pair marginal, terminal residual, unfillable exception, or new residual structural pattern fails the theorem; no extra exception rule may be added.",
            "reason_C50_is_authorized": "C49 supplies a clear, exact, falsifiable next theorem route rather than mere finite continuation, satisfying the stated Cycle-49 clarity condition.",
        },
        "audit": checked,
        "resources": {**checked["resources"], "worker_cpus": [0, 1, 2], "reserved_cpu": 3},
        "runtime": check_runtime("Cycle 49 relative diagonal"),
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "replay": {
            "controls_command": ".venv/bin/python discovery/lrc_relative_diagonal_controls.py",
            "inventory_command": ".venv/bin/python discovery/lrc_relative_diagonal_inventory.py",
            "support_command": ".venv/bin/python discovery/lrc_relative_diagonal_support_classify.py",
            "deletion_command": ".venv/bin/python discovery/lrc_relative_diagonal_deletion_classify.py",
            "principal_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_relative_diagonal_full_audit.py",
            "terminal_command": ".venv/bin/python proof/check_cycle_49_terminal_exception.py",
            "independent_command": "taskset -c 0-2 .venv/bin/python proof/replay_cycle_49_relative_diagonal_independent.py",
            "audit_command": ".venv/bin/python proof/check_cycle_49_relative_diagonal.py",
            "test_command": ".venv/bin/python -m unittest tests.test_cycle_49_relative_diagonal -v",
            "check_command": ".venv/bin/python proof/build_cycle_49_lrc_relative_diagonal.py --check",
        },
        "sealer": {"path": "proof/build_cycle_49_lrc_relative_diagonal.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
