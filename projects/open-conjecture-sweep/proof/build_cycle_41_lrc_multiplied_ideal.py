"""Seal Cycle 41's exact first multiplied ownership-ideal construction."""
from __future__ import annotations

import json
from pathlib import Path

from check_cycle_41_multiplied_ideal import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle41-multiplied-ideal"
OUTPUT = ROOT / "artifacts/cycle-41-b041-lrc-multiplied-ideal-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-41-b041-lrc-multiplied-ideal-preregistration-v1.md", "a1e49f5f9f8847a41caad6a8e99dc3f50679dcec221c549315b14de91f95ddfb"),
    "cycle40_artifact": (ROOT / "artifacts/cycle-40-b040-lrc-signed-moments-v1.json", "abe2c9b4d617bb952348ba01aa4138cbff4b56cc2f9e12fd248c0eb97c44f14e"),
    "idea_selection": (ROOT / "discovery/cycle41_multiplied_ideal_idea_selection.md", "8977da55af9e05f279e8a542af342734d884d51cb82e7eabbd191f5e50dcad12"),
    "integral_engine": (ROOT / "discovery/lrc_multiplied_ideal.py", "6147b6d2565d6f431370fff96cededfd90fc33735d47b65b26be4f519dbd6386"),
    "integral_result": (OUT / "result.json", "5590c4302fd7e81532df332f9074e8e6e8253fb6857fba6bd5ee24086b5eb0c3"),
    "integral_timing": (OUT / "run-integral-pair.time", "544df6388fa196f213df65dac5135e5f5cedb617960559be14150dc0f1b355ac"),
    "first_obstruction_checker": (ROOT / "proof/check_cycle_41_first_filling_obstruction.py", "f1cac26349b5887cac94b70ca85372e4f35fd182067f630b50cef5be89f0c011"),
    "first_obstruction": (OUT / "first-exact-obstruction.json", "f066c20af6cf6d29270180ec21d30706f1685e907796c8e86793187ca636bad7"),
    "first_obstruction_timing": (OUT / "run-first-exact.time", "cd5de482019c7fb23572bdbd0421224ecb61df8ee8e22351d9f68834b5c7fda4"),
    "zero_closure_engine": (ROOT / "discovery/lrc_multiplied_zero_closure.py", "ee65eeeda878cf2640f6052b5ba0ef02e9b7f0b15d379abebdb5382c8d53e8ae"),
    "zero_closure_result": (OUT / "zero-support-closure.json", "a1f742592375d035f68d3dcd0ecde65c4ee6e7b78c96fa2a1ed18362e979037e"),
    "zero_closure_timing": (OUT / "run-zero-closure.time", "b25ba4cca2fe167a3488531b260d596ba8d22b48e3cde4a12c4270f990dcbfd6"),
    "small_boundary_engine": (ROOT / "discovery/lrc_multiplied_small_boundary.py", "2ace8e26645cc0f72dd296d0cce40ece415f91cf15e3ba1ab1dd00a9522be217"),
    "small_boundary_result": (OUT / "small-boundary.json", "ebcef238ba561497f6e96e776a5765b486f6a0049b9cbb0da57c44243bb9cef9"),
    "small_boundary_timing": (OUT / "run-small-boundary-exact-audit.time", "351eed6ad2fb5c789f4b749780ac506e5e3fe541df3f830b33bc896980be4017"),
    "independent_replay": (ROOT / "proof/replay_cycle_41_multiplied_independent.py", "6bee5340fa589e04ca61d321b56b830d09b26465dc2f7650cc959549a9552a6c"),
    "independent_result": (OUT / "independent-replay.json", "66cf7d165b9b09594e318be693afeaceda5bd6f4e9f6edaee4c97a1a6f8661d5"),
    "independent_timing": (OUT / "run-independent.time", "001bdff3ff67827db52e98d6cedcce4457e447fe11182f71be69415e1ce8e930"),
    "soundness": (ROOT / "proof/cycle_41_multiplied_ideal_soundness.md", "09ffe8971705052a400a78c1bcb8c7e611439332698d96531f1ae525640d2d0f"),
    "audit": (ROOT / "proof/check_cycle_41_multiplied_ideal.py", "3de271e6fa247898288f31a8d0ec976761341ef17a651473f2cf0515d3d7d0f3"),
    "test": (ROOT / "tests/test_cycle_41_multiplied_ideal.py", "da29d74d64f40f3753b8b871501400f3e199dd73377079355b801767a032e76a"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "preregistration_validator": (ROOT / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def payload() -> dict[str, object]:
    checked = audit()
    initial = json.loads((OUT / "result.json").read_text(encoding="utf-8"))
    zero = json.loads((OUT / "zero-support-closure.json").read_text(encoding="utf-8"))
    boundary = json.loads((OUT / "small-boundary.json").read_text(encoding="utf-8"))
    replay = json.loads((OUT / "independent-replay.json").read_text(encoding="utf-8"))
    return {
        "artifact_id": "cycle-41-b041-lrc-multiplied-ideal-v1",
        "budget_ordinal": "B041",
        "cycle": 41,
        "record_type": "PROVED_SIGNED_FIRST_MULTIPLIED_IDEAL_CONSTRUCTION",
        "recorded_at_utc": "2026-08-04T19:41:27Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "A mass-one rational signed degree-three ownership functional exists on p199 base 4 / leaf 78 satisfying the Cycle 40 constraints and every Boolean-reduced ownership-literal multiple of every rank-two blocker.",
        "claim_boundary": "This is not positive, not a global ownership distribution, not a full-ideal functional, not a leaf certificate, and not LRC(13). Ownership-literal multiples of rank-three blockers and higher-degree generator multiples remain open.",
        "audit": checked,
        "contained_candidate_falsifier": {"epistemic_status": "PROVED", "selected_delta_rank_two_conflicts": initial["selected_owner_rank_two_violations"], "first_canonical_transport_nonboundary_types": [4, 64, 73], "meaning": "The initial delta/canonical pair choices fail, but the general signed pair transport remains feasible."},
        "pair_construction": {"epistemic_status": "PROVED", "singleton_owner_deletions": zero["singleton_mediated_owner_deletions"], "binary_mediated_zero_pair_classes": zero["pair_classes_with_binary_mediated_zero_cells"], "rank_three_induced_pair_classes": zero["rank3_induced_pair_classes"], "component_equations": zero["component_equations"], "disconnected_pair_classes": zero["disconnected_pair_classes"], "singleton_system": zero["singleton_system"]},
        "small_boundary": {"epistemic_status": "PROVED", "type_triples": boundary["type_triples_checked"], "interfaces": boundary["distinct_homology_interfaces"], "nonzero_h1_interfaces_gf2": boundary["nonzero_h1_interfaces_gf2"], "nonzero_h1_type_triples_gf2": boundary["nonzero_h1_type_triples_gf2"], "rational_left_null_evaluations": boundary["exact_left_null_relation_evaluations"], "left_null_annihilation_terms": boundary["left_null_annihilation_terms_checked"], "failures": boundary["exact_candidate_failures"], "small_rank_three_classes": boundary["small_rank_three_type_classes"]},
        "dense_boundary_theorem": {"epistemic_status": "PROVED", "support_gap": [6, 9], "large_support_minimum": 9, "pair_star_intersection_minimum_side": 7, "triple_star_intersection_minimum_side": 6, "mechanism": "degree-one Cech/Mayer-Vietoris star cover plus zero-pair-marginal octahedral rank-three corrections"},
        "independent_replay": {"status": replay["status"], "raw_rank_two_tuples": replay["rank_two_type_tuples"], "raw_rank_three_tuples": replay["rank_three_type_tuples"], "small_type_triples": replay["small_type_triples"], "interfaces": replay["small_interfaces"], "reversed_pivot_controls": replay["exact_reversed_pivot_controls"]},
        "cycle_decision": {"companion_identity": "/root/darwin_cycle25_short", "outcome": "SEALED_AND_OPEN_RECURSIVE_HORN_FILLING_PROTOTYPE", "scope_review": "Orientation, non-iterated degree-three cell semantics, low-dimensional nerve hypotheses, octahedral corrections, repeated-type symmetry, complete exact boundary census, and independent reconstruction passed.", "strongest_flaw": "The H1 star-cover argument does not automatically recurse because its pair intersections can have nonzero H1.", "next_action": "Open Cycle 42 for the smallest exact four-partite H2/horn-filling prototype under actual rank-one/two/three deletions, before any general degree-four campaign.", "falsifier": "An exact compatible 2-cycle with an independently checked nonboundary certificate refutes recursive horn filling on the selected interface."},
        "resources": {"worker_cpus": [0, 1, 2], "reserved_cpu": 3, "aggregate_wall_seconds": 1033.0, "principal_exact_wall_seconds": boundary["wall_seconds"], "independent_wall_seconds": replay["wall_seconds"], "peak_rss_kib": 1357308, "temporary_disk_cap_bytes": 5368709120},
        "runtime": check_runtime("Cycle 41 first multiplied ownership-ideal layer"),
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "replay": {"zero_closure_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_multiplied_zero_closure.py", "primary_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_multiplied_small_boundary.py", "independent_command": "taskset -c 0-2 .venv/bin/python proof/replay_cycle_41_multiplied_independent.py", "audit_command": ".venv/bin/python proof/check_cycle_41_multiplied_ideal.py", "test_command": ".venv/bin/python -m unittest tests.test_cycle_41_multiplied_ideal -v", "check_command": ".venv/bin/python proof/build_cycle_41_lrc_multiplied_ideal.py --check"},
        "sealer": {"path": "proof/build_cycle_41_lrc_multiplied_ideal.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
