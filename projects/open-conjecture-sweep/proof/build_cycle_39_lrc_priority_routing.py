"""Seal Cycle 39's exact full priority-section span obstruction."""
from __future__ import annotations

import json
from pathlib import Path

from check_cycle_39_priority_routing import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle39-priority-routing"
OUTPUT = ROOT / "artifacts/cycle-39-b039-lrc-priority-routing-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-39-b039-lrc-priority-routing-preregistration-v1.md", "ed82c6d5c11f7ac61dfa416d05e1bf2dc05172b1540779681dfedc5fd13af9a2"),
    "cycle29_artifact": (ROOT / "artifacts/cycle-29-b029-lrc-ownership-blocker-v2.json", "faf097ebcc22e9e18055cbf4139aef30e17ee85e86ea2096d43b31873f6e8d09"),
    "cycle37_artifact": (ROOT / "artifacts/cycle-37-b037-lrc-degree-two-product-v1.json", "0e606c64704f08158fa4a04b98737450b83ada03cb67b601f1680bff75b3265a"),
    "cycle38_artifact": (ROOT / "artifacts/cycle-38-b038-lrc-ownership-functional-v1.json", "d9be66e3b18f3d06ad975d2dbf37696835279afb7a9504d744227572bdaf5a13"),
    "idea_selection": (ROOT / "discovery/cycle39_priority_routing_idea_selection.md", "5fb66dcb07f14f281f9a11c43070933510c8de4b252deb70d7dbc6f35c76fa14"),
    "primary_engine": (ROOT / "discovery/lrc_priority_routing.py", "81bbe6d3e9e02e7ecd4be9a8bd8a56c0b855900f449ad9c63a9e7502fa85672c"),
    "primary_result": (OUT / "result.json", "3ba18ed40ff2edfec6e9d93786f1f10f14932e57ad549b0c453afc97ae92d183"),
    "first_tranche_timing": (OUT / "run-tranche1.time", "a5e55afad1d103cf18f43ab332637eaa7812e71c3c3f75d1b6f4118a7145a230"),
    "second_tranche_timing": (OUT / "run-tranche2.time", "3eeea491894ee40f77a4941848405c263dd37d06a114547b8ea620395bb17221"),
    "final_timing": (OUT / "run.time", "4e45ba662365ef600ebf857549a1c86cd284e49bf04c44cd7c59d9ef033bedd6"),
    "root1_checkpoint": (OUT / "root-01-checkpoint.json", "97fcc1f47343a1bc626fb21be4713033c02f9e57dae826f16d86b35353370079"),
    "root9_checkpoint": (OUT / "root-09-checkpoint.json", "709caff8e3126e41d4a39b4fa63f05ddcc8eae4f8696562970a5c118391e40b8"),
    "independent_replay": (ROOT / "proof/replay_cycle_39_priority_routing_independent.py", "df20a007e0ffd26d44bfb887e2db5635ef5f6fa29ef5d0bbef01aac152935f32"),
    "independent_result": (OUT / "independent-replay.json", "3621b12c0c33bd1a61c25dc1d0e2afa3233fea31cc18772242919e400eef40cc"),
    "independent_timing": (OUT / "independent-replay.time", "f956d519d849a2e50270d48801bd4c5f06edf3528fd6ca4571bc2e4f5fd68111"),
    "audit": (ROOT / "proof/check_cycle_39_priority_routing.py", "498e3039ca5bdef1fb637be06affebdd552dcb2ba9653f75f2770664602e9fb7"),
    "soundness": (ROOT / "proof/cycle_39_priority_routing_soundness.md", "6f1ac963b8ddc9247a2595ac0c387d91e2d4d759a7e1daa8137a8ed5e5fd4fd4"),
    "test": (ROOT / "tests/test_cycle_39_priority_routing.py", "da8d3dbc980f0e44673b8c3e6032749f43b83954dd9e5916c32dbc5efaab511f"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "preregistration_validator": (ROOT / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def payload() -> dict[str, object]:
    checked = audit()
    result = json.loads((OUT / "result.json").read_text(encoding="utf-8"))
    replay = json.loads((OUT / "independent-replay.json").read_text(encoding="utf-8"))
    return {
        "artifact_id": "cycle-39-b039-lrc-priority-routing-v1",
        "budget_ordinal": "B039",
        "cycle": 39,
        "record_type": "PROVED_PRIORITY_ROUTING_SPAN_NO_GO",
        "recorded_at_utc": "2026-08-04T18:23:26Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "All thirteen fallback blocks of the complete 53,248-section deterministic priority/fallback ownership span are exactly inconsistent with mass one and the rank-two blocker equations for p199 base 4 / leaf 78. Independent replay verifies 573 selected rows and every integer left-null product across all section columns.",
        "claim_boundary": "This closes the signed span of all deterministic priority orders with one fallback at the unmultiplied ownership-generator layer for one leaf. It does not constrain arbitrary pair-correlated or nonlocal routing, generator multiples, the ownership ideal, the leaf, or LRC(13).",
        "audit": checked,
        "proved_basis": {"epistemic_status": "PROVED", "statement": "For a fixed fallback, a priority order's blocker moments depend exactly on the subset of the other twelve coordinates preceding the fallback; the resulting 4096 sections are complete for all priority orders with that fallback.", "fallback_blocks": 13, "columns_per_block": 4096, "total_section_columns": 53248, "block_diagonal_by_fallback": True},
        "obstruction": {"epistemic_status": "PROVED", "rank_needed": 2, "selected_rows_by_root": [row["selected_rows"] for row in result["roots"]], "total_selected_rows": replay["total_selected_rows"], "mass_coefficients_by_root": [row["left_null_certificate"][0] for row in result["roots"]], "independent_all_column_replay": "PASS", "direct_support_assignment_checks": replay["direct_support_assignment_checks"], "maximum_certificate_coefficient_bits": replay["maximum_certificate_coefficient_bits"]},
        "contained_resource_tranches": {"first": {"status": "WALL_CAP", "mathematical_conclusion": None}, "second": {"status": "CAP", "closed_roots": 11, "capped_roots": [1, 9], "separator_evaluations": 790685}, "final": {"status": "PASS", "resumed_roots": [1, 9], "separator_evaluations": result["separator_moment_evaluations_this_tranche"]}},
        "cycle_decision": {
            "companion_identity": "/root/darwin_cycle25_short",
            "outcome": "SEALED_FOR_PAIR_CORRELATED_OWNERSHIP_MOMENTS",
            "scope_review": "The 53,248-section span strictly contains Cycle 38's thirteen rooted maps, and the predecessor-subset theorem makes the no-go genuinely broader. Full independent certificate replay is complete.",
            "strongest_flaw": "Single-fallback priority sections may miss joint routing correlations; pairwise moments may still miss genuinely higher-order correlations.",
            "independent_ideas": ["signed degree-two ownership-moment/cochain system", "pair-correlated routing kernel with local marginal consistency", "interpret later left-null witnesses cohomologically rather than opening a separate engine"],
            "falsifier": "Any quotient/raw incidence mismatch, marginal inconsistency, priority-section row mismatch, or invalid exact certificate invalidates the affected claim.",
            "next_action": "Open Cycle 40 for an exact signed pair-correlated ownership-moment system imposing totality, exclusivity, marginal consistency, and rank-one/two blockers; validate every rank-three blocker before interpretation.",
        },
        "resources": {"worker_cpus": [0, 1, 2], "reserved_cpu": 3, "cumulative_primary_wall_seconds": 5155.60, "independent_wall_seconds": replay["wall_seconds"], "cumulative_wall_seconds": 5336.73, "peak_rss_kib": 138456, "separator_evaluations_in_recorded_continuations": result["separator_moment_evaluations"], "temporary_disk_cap_bytes": 5368709120},
        "runtime": check_runtime("Cycle 39 full priority-section routing"),
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "replay": {"primary_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_priority_routing.py", "independent_command": "taskset -c 0 .venv/bin/python proof/replay_cycle_39_priority_routing_independent.py", "audit_command": ".venv/bin/python proof/check_cycle_39_priority_routing.py", "test_command": ".venv/bin/python -m unittest tests.test_cycle_39_priority_routing -v", "check_command": ".venv/bin/python proof/build_cycle_39_lrc_priority_routing.py --check"},
        "sealer": {"path": "proof/build_cycle_39_lrc_priority_routing.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
