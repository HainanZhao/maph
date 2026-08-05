#!/usr/bin/env python3
"""Seal Cycle 48's Möbius cube repair and literal-confluence no-go."""
from __future__ import annotations

import json
from pathlib import Path

from check_cycle_48_cube_rewrite import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle48-cube-rewrite"
OUTPUT = ROOT / "artifacts/cycle-48-b048-lrc-cube-rewrite-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-48-b048-lrc-cube-rewrite-preregistration-v1.md", "7cef7d7ecfcc55aaea9932d6b8f48ec66eb1a28fd5e8ea4eb330659b575cc0a1"),
    "cycle47_artifact": (ROOT / "artifacts/cycle-47-b047-lrc-global-affine-descent-v1.json", "05b3b3b36691c933481a953a8415aba093db6c7e2db52917aabae47091c845bf"),
    "idea_selection": (ROOT / "discovery/cycle48_cube_rewrite_idea_selection.md", "286cd1bee48283e8a5e1fa19c7b4e69ec43bbe10788cdb564e81fed0c55dfaa4"),
    "rewrite_module": (ROOT / "discovery/lrc_cube_rewrite.py", "106a237501b9bf115e8df265c2075f0605c6a7776c1bd8fdd870adc1b01e4de9"),
    "selector": (ROOT / "discovery/lrc_cube_rewrite_select.py", "774eb105d308b390b075169b5a04ac6795d995e1a23a04096c7c342a32e32852"),
    "selection": (OUT / "selection.json", "84137a655a2ef241557c4024ced74d4cb18f64d27a0f2c06d5ba56ceae2d73fc"),
    "selection_timing": (OUT / "run-selection.time", "05090be0b87b90c150e271be55f83b7d444ffd998cf51c1c48d07f8d30c71e44"),
    "control_engine": (ROOT / "discovery/lrc_cube_rewrite_controls.py", "56a04ab19df01ef0fe9ddbc2495b88efd6fbf374b9cb5be9de29e19cfffdbfa3"),
    "control_result": (OUT / "generic-controls.json", "5de016105e10e44c31786105254659007d6671eab88fb4683cc64ec8e9542166"),
    "control_timing": (OUT / "run-generic-controls.time", "a60338404d089ff3f41d4a5c782da2d8eb724eebfda9822fa8e181abb6ad0f5a"),
    "actual_engine": (ROOT / "discovery/lrc_cube_rewrite_actual.py", "fa8dc7a73d56315eb5c92fcd07cc5e6c719d53551d87d17d2e9c695ec3015f4a"),
    "actual_result": (OUT / "actual.json", "436182b5cfea6acae25c46f7f8bf6fc88f06c6c08b4a094aca0a268ba0037f84"),
    "actual_timing": (OUT / "run-actual.time", "5fcb8cb692053ba21d0d5d1d96f33657f4908094bf8bd40988a0f82e392e6841"),
    "soundness": (ROOT / "proof/cycle_48_cube_rewrite_soundness.md", "ef4950de15c7e44b8c59b4d2c6d95dece631f1b9908f199e50d70134a05ae126"),
    "independent_selector": (ROOT / "proof/check_cycle_48_selector_independent.py", "9c742187dbd034798b406a4319b0244b58204505eb4fb4bd9e46e4f85ccace42"),
    "independent_selection": (OUT / "independent-selection.json", "54f14e6aae29e824716991d0b30bc213b4e108196b735679e6d0b05e8b8d99b0"),
    "independent_selection_timing": (OUT / "run-independent-selection.time", "1aed6dee8120add0e2bda9d185611dcf6ce08b7e780972c8e2f8a2ed9c11cb73"),
    "independent_replay": (ROOT / "proof/replay_cycle_48_cube_rewrite_independent.py", "e46f7533466bd3377329fd4710ed5d2d5d4cd913752c278b6a345a19860e6915"),
    "independent_result": (OUT / "independent-replay.json", "47ec9493f744464a12589d8ff50fa8f0e4cd3858d7a41762bdd96f80fb78321f"),
    "independent_timing": (OUT / "run-independent.time", "ae9128e9270d66d77da38998924637ebe0333a5a165a93ddf4c1e7ddea6a4b6b"),
    "audit": (ROOT / "proof/check_cycle_48_cube_rewrite.py", "1ecd94c59022b615abbf073acc648d112bc64e1d42e3804d3e0650978ef46de1"),
    "test": (ROOT / "tests/test_cycle_48_cube_rewrite.py", "106bf396af0c6121e68beab22d8f5841e7778f63d1df9876da7612c2c12759ef"),
    "cycle41_closure": (ROOT / "discovery/out/cycle41-multiplied-ideal/zero-support-closure.json", "a1f742592375d035f68d3dcd0ecde65c4ee6e7b78c96fa2a1ed18362e979037e"),
    "cycle29_interface": (ROOT / "discovery/out/cycle29-ownership-blocker/result.json", "b213f8b790b2f53e2de30d244ead973143973e236083d24b38fffb5234271f15"),
    "cycle47_selection": (ROOT / "discovery/out/cycle47-affine-descent/selection.json", "eac88f41ac6ae261d407ba4e6026e121e25435fafe4a66911a3645454c4f5ac1"),
    "ownership_interface": (ROOT / "discovery/lrc_ownership_functional.py", "2e4d63706aff0f0c71f13c06bd0dc63374f28c82a1e9ae4fd2b241141d843589"),
    "signed_moments": (ROOT / "discovery/lrc_signed_ownership_moments.py", "cb76981ee928abd7b25bf665a83a55e883587c2c89b26b35282226a0afbae5f3"),
    "transport": (ROOT / "discovery/lrc_multiplied_fill_probe.py", "3bb02b3fcc56f6d5f83c0719556bf41e5a7d1821ffb61c79150160c9e44990f6"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "preregistration_validator": (ROOT / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def payload():
    checked = audit()
    selection = json.loads((OUT / "selection.json").read_text())
    actual = json.loads((OUT / "actual.json").read_text())
    independent_selection = json.loads((OUT / "independent-selection.json").read_text())
    independent = json.loads((OUT / "independent-replay.json").read_text())
    controls = json.loads((OUT / "generic-controls.json").read_text())
    return {
        "artifact_id": "cycle-48-b048-lrc-cube-rewrite-v1",
        "budget_ordinal": "B048", "cycle": 48,
        "record_type": "PROVED_MOBIUS_CUBE_REPAIR_AND_CONFLUENCE_NO_GO",
        "recorded_at_utc": "2026-08-05T06:15:49Z", "status": "SEALED", "epistemic_status": "PROVED",
        "outcome": "A closed Möbius formula extends three compatible pair transports, signed 2x2x2 cubes preserve every pair marginal, and lexicographically triangular cube reduction terminates. Every one of 512 outcome-blind p199 structural faces repairs exactly, but every one of the 314 faces with an initial forbidden defect has a literal nonjoinable reached critical diamond. Deterministic construction survives; literal confluence is refuted on every nontrivial frozen start.",
        "claim_boundary": "The formula, cube-kernel identity, and triangular termination criterion are generic. Repair and nonconfluence counts are proved only for the frozen 512-face corpus. This does not prove a universal p199 face constructor, every quadruple fills, a degree-four functional, a leaf certificate, or LRC(13).",
        "generic_theorems": {
            "mobius_extension": "M=P01 tensor delta2 + P02 tensor delta1 + delta0 tensor P12 - 2 delta000 has the three prescribed pair marginals when their singleton marginals are the distinguished point masses.",
            "cube_kernel": "Every signed 2x2x2 alternating cube has zero in all three pair marginals.",
            "triangular_termination": "A reducer whose other forbidden cells are later in the frozen order kills its pivot without reintroducing earlier defects; finite scanning terminates.",
        },
        "corpus": {
            "hash_candidates": independent_selection["candidates"],
            "descriptor_strata": independent_selection["descriptor_strata"],
            "selected_faces": actual["selected_faces"],
            "mobius_defect_faces": actual["mobius_defect_faces"],
            "repair_status_counts": actual["repair_status_counts"],
            "confluence_status_counts": actual["confluence_status_counts"],
            "aggregate_forbidden_cells": actual["aggregate_forbidden_cells"],
            "aggregate_cube_candidates": actual["aggregate_cube_candidates"],
            "aggregate_repair_steps": actual["aggregate_repair_steps"],
            "aggregate_critical_diamonds": actual["aggregate_critical_diamonds"],
        },
        "literal_confluence_falsifier": actual["first_nonconfluent"],
        "negative_controls": {
            "unrepaired_structural_zero": controls["unrepaired_structural_zero"],
            "literal_nonjoinable_diamond": controls["literal_nonjoinable_diamond"],
            "nonkernel_move_rejected": controls["nonkernel_move_rejected"],
        },
        "comparison_quarantine": {
            "cycle47_overlap": actual["comparison_overlap"],
            "equal": actual["comparison_equal"],
            "zero_marginal_unequal": actual["comparison_zero_marginal_differences"],
            "interpretation": "Performed only after principal classification; equality is a consistency check and was never a selection rule.",
        },
        "independent_replay": {
            "selector_status": independent_selection["status"],
            "material_status": independent["status"],
            "faces": independent["faces"],
            "method": "Independent reverse candidate/cell order, direct marginal sums, and no import of the principal rewrite module.",
        },
        "questioning_correction": {
            "rejected_idea": "Remove each forbidden coefficient with one cube having seven allowed companion vertices.",
            "exact_reason": "If a pivot violates the 01 diagonal, changing only coordinate 2 leaves a second cube vertex with the same forbidden 01 pair; a zero-marginal cube cannot isolate that defect.",
            "implication": "A new engine must contract coupled forbidden fibers or use their relative homology, not independent defect deletion.",
        },
        "cycle_decision": {
            "companion_identity": "/root/darwin_cycle25_short",
            "companion_strongest_flaw": "Zero total on each deleted pair fiber is insufficient by itself because packet moves may spill into the other pair strata or terminate on an unavailable cell.",
            "outcome": "SEAL_C48_AND_OPEN_C49_RELATIVE_DIAGONAL_CONTRACTION",
            "next_question": "Does the allowed three-way cell complex admit a diagonal-stratum filtration whose cube packets explicitly contract every zero-pair-marginal defect, with zero terminal triple-intersection group under frozen support/buffer hypotheses?",
            "falsifier": "An exact surviving relative cycle or dual cochain in the terminal group, or a full-domain p199 interface violating the preregistered buffer hypothesis.",
            "user_stop_gate": "Cycle 49 is the final clarity gate for Problem 1. If it yields neither a clear theorem route nor a decisive structural obstruction, pause LRC(13) immediately and create one concise handoff; do not open Cycle 50.",
        },
        "audit": checked,
        "resources": {
            **checked["resources"],
            "worker_cpus": [1, 2], "reserved_cpu": 3,
            "selection_peak_rss_kib": 1253728,
            "actual_peak_rss_kib": 448032,
            "independent_selection_peak_rss_kib": 1182348,
            "independent_replay_peak_rss_kib": 446268,
        },
        "runtime": check_runtime("Cycle 48 cube rewrite"),
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "replay": {
            "selection_command": "taskset -c 2 .venv/bin/python discovery/lrc_cube_rewrite_select.py",
            "controls_command": "taskset -c 2 .venv/bin/python discovery/lrc_cube_rewrite_controls.py",
            "actual_command": "taskset -c 2 .venv/bin/python discovery/lrc_cube_rewrite_actual.py",
            "independent_selection_command": "taskset -c 1 .venv/bin/python proof/check_cycle_48_selector_independent.py",
            "independent_material_command": "taskset -c 2 .venv/bin/python proof/replay_cycle_48_cube_rewrite_independent.py",
            "audit_command": ".venv/bin/python proof/check_cycle_48_cube_rewrite.py",
            "test_command": ".venv/bin/python -m unittest tests.test_cycle_48_cube_rewrite -v",
            "check_command": ".venv/bin/python proof/build_cycle_48_lrc_cube_rewrite.py --check",
        },
        "sealer": {"path": "proof/build_cycle_48_lrc_cube_rewrite.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
