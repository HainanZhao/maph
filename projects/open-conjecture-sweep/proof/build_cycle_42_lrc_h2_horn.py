"""Seal Cycle 42's exact selected-interface ambient H2 census."""
from __future__ import annotations

import json
from pathlib import Path

from check_cycle_42_h2_horn import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle42-h2-horn"
OUTPUT = ROOT / "artifacts/cycle-42-b042-lrc-h2-horn-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-42-b042-lrc-h2-horn-preregistration-v1.md", "7b629b6137368b029ae6559558a45223d192cfe15b61b7b10151a0155d106cf8"),
    "cycle41_artifact": (ROOT / "artifacts/cycle-41-b041-lrc-multiplied-ideal-v1.json", "5bff8d5b4848ad9381404c79de782033e26c3b1bd9d48078a752ae8611df6307"),
    "idea_selection": (ROOT / "discovery/cycle42_h2_horn_idea_selection.md", "2108a801d6a2a979e6e33a9232f23203f4efcfcea29bc80aed45a9d52772ebf4"),
    "census_engine": (ROOT / "discovery/lrc_h2_horn.py", "b64440c78b10d3cfd2dc61d16f02f5cc9c3c4848d45978e2e62c7753c37df82a"),
    "census": (OUT / "gf2-census.json", "948341955d3c3275878fbe415c5aee9831e364242fea03d30fc97394cfdc1976"),
    "initial_timing": (OUT / "run-gf2-census.time", "79e9e04d4120b4631b3993b402139d13d8e3da62e695658f11c93a830c480210"),
    "rational_timing": (OUT / "run-rational-census.time", "40d837aab0d0b7388da02430100fbdc39ba6dd30930249b1a8bc9ff2890f3ca8"),
    "first_checker": (ROOT / "proof/check_cycle_42_first_h2_coupling.py", "fc28f2c24a19f82faf538d226b128e8cd7ad930ce6291689505c2a45c856255e"),
    "first_result": (OUT / "first-rational-coupling.json", "c57ecfa61649341cf51fd82890640b32dbc00e576d9f5b08115290b0f9e977cd"),
    "first_timing": (OUT / "run-first-rational.time", "3f60acb200dfb1e0c8b8c47d6d72bdfacc4d2676599cdd4e5150cd9a39979d36"),
    "independent_replay": (ROOT / "proof/replay_cycle_42_h2_horn_independent.py", "8c8ee228b111ef5c66bcdb47ebb4a6fdf6af34cf51a21315007f433a40323ef2"),
    "independent_result": (OUT / "independent-replay.json", "6af808cb2fbaff6bb51f0c626a0c9d4944ffb9ebb249661bc1fabaed78bcde35"),
    "independent_timing": (OUT / "run-independent.time", "ed30fbe404276ce1623381f1650b738e1d1bb746b3f289ccb63eb0baa1f5f056"),
    "soundness": (ROOT / "proof/cycle_42_h2_horn_soundness.md", "94b96f7d2802e6d5d280a7effd26b9f42e653fbf90c7c5322770ffb0b684c77c"),
    "audit": (ROOT / "proof/check_cycle_42_h2_horn.py", "93124bf2e4f94b2979f9f4133dc60085843fc6fb25704dba5d31de0d8f5d584a"),
    "test": (ROOT / "tests/test_cycle_42_h2_horn.py", "0c4a1df38ef9c20480870971db4f543f07a5635f2408294fb017a378cedc3497"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "preregistration_validator": (ROOT / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def payload():
    checked = audit()
    census = json.loads((OUT / "gf2-census.json").read_text(encoding="utf-8"))
    first = json.loads((OUT / "first-rational-coupling.json").read_text(encoding="utf-8"))
    replay = json.loads((OUT / "independent-replay.json").read_text(encoding="utf-8"))
    distinct_nonzero = sum(row["h2_q"] > 0 for row in census["rows"])
    return {
        "artifact_id": "cycle-42-b042-lrc-h2-horn-v1",
        "budget_ordinal": "B042",
        "cycle": 42,
        "record_type": "PROVED_SELECTED_AMBIENT_H2_CENSUS",
        "recorded_at_utc": "2026-08-04T20:20:00Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "Among 3,954 preregistered four-type interfaces, exactly 3,893 have nonzero rational H2; the actual canonical Cycle 41 moment cycle on the first such interface is nevertheless the boundary of one allowed tetrahedron.",
        "claim_boundary": "This is a selected ambient-topology census, not all four-type interfaces, not evidence that the Cycle 41 functional fails, not a full degree-four functional, not a leaf certificate, and not LRC(13). Only the first nonzero-H2 interface is coupled to the canonical moment cycle.",
        "selection": {"anchors": census["anchors"], "raw_interfaces": census["raw_interfaces"], "distinct_structural_complexes": census["distinct_interfaces"], "rank_three_deleted_classes": census["relevant_rank_three_classes"]},
        "homology": {"epistemic_status": "PROVED", "nonzero_raw_interfaces_q": census["nonzero_h2_q"], "nonzero_distinct_complexes_q": distinct_nonzero, "maximum_h2_q": census["maximum_h2_q"], "gf2_q_dimension_disagreements": census["field_dimension_disagreements"], "maximum_elimination_coefficient_bits": census["maximum_rational_coefficient_bits"], "aggregate_simplices_raw": census["aggregate_cells"]},
        "first_interface": {"types": first["types"], "complex": first["complex"], "canonical_nonboundary_pairing": first["canonical_class"]["pairing"], "canonical_cycle_support": len(first["canonical_class"]["primitive_cycle"]), "canonical_cochain_support": len(first["canonical_class"]["dual_cochain"]), "moment_cycle_support": first["moment_cycle_nonzero"], "moment_filling_status": first["moment_filling_status"], "moment_fill_tetrahedra": len(first["moment_fill"])},
        "independent_replay": {"status": replay["status"], "route": "direct type/signature membership, reverse structural enumeration, and highest-pivot exact elimination", "raw_interfaces": replay["raw_interfaces"], "distinct_interfaces": replay["distinct_interfaces"], "nonzero_h2_q": replay["nonzero_h2_q"], "first_moment_filling_status": replay["first_interface"]["moment_filling_status"]},
        "audit": checked,
        "cycle_decision": {"companion_identity": "/root/darwin_cycle25_short", "outcome": "SEAL_AMBIENT_TOPOLOGY_AND_OPEN_FULL_MOMENT_COUPLING", "scope_review": "Ambient H2 is abundant and exact, but it is irrelevant to extension unless the actual signed moment cycle has nonzero class; the first actual class fills.", "strongest_flaw": "Only the first of 3,893 nonzero-H2 raw interfaces was moment-coupled, and even a future nonboundary canonical class would not rule out another degree-three choice or degree-four signed functional.", "next_action": "Open Cycle 43 for exact canonical moment-H2 coupling across all 409 structural complexes / 3,954 raw selected interfaces, escalating to coherent face-choice variables if the canonical assignment fails.", "falsifier": "A verified actual moment cycle with nonzero dual-cochain pairing refutes the canonical Cycle 41 transport extension on that interface."},
        "resources": {"worker_cpus": [0, 1, 2], "reserved_cpu": 3, "cycle_wall_upper_bound_seconds": 1200, "principal_rational_wall_seconds": census["wall_seconds"], "independent_wall_seconds": replay["wall_seconds"], "peak_rss_kib": 1084924, "temporary_disk_cap_bytes": 5368709120},
        "runtime": check_runtime("Cycle 42 selected ambient H2 census"),
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "replay": {"census_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_h2_horn.py", "first_coupling_command": "taskset -c 0 .venv/bin/python proof/check_cycle_42_first_h2_coupling.py", "independent_command": "taskset -c 0-2 .venv/bin/python proof/replay_cycle_42_h2_horn_independent.py", "audit_command": ".venv/bin/python proof/check_cycle_42_h2_horn.py", "test_command": ".venv/bin/python -m unittest tests.test_cycle_42_h2_horn -v", "check_command": ".venv/bin/python proof/build_cycle_42_lrc_h2_horn.py --check"},
        "sealer": {"path": "proof/build_cycle_42_lrc_h2_horn.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
