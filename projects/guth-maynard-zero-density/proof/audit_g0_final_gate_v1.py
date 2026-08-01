#!/usr/bin/env python3
"""Hostile, fixed-scope final G0 gate audit; not the authoritative reconciliation."""
from __future__ import annotations

import argparse
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "g0-final-gate-audit-v1.json"
FROZEN = {
    "cycle1_preregistration": ("docs/cycle-1-g0-preregistration.md", "150b4ee03383aa9be8d2301bbbc39644cb3464682a9c634b3143c1ada4fd7cf4"),
    "cycle2_preregistration": ("docs/cycle-2-g0-analytic-preregistration.md", "e07ecf8783983d20ad435bdcd1c4b0922eee0c6419b26bdd34d7a34b92a2fb63"),
    "inherited_dependency_graph": ("artifacts/g0-theorem-dependency-graph-v1.json", "14f80b35774a3994c93e1a08de34afb2aefff7023e1797932e6fb4d78af1281b"),
    "source_manifest_v3": ("artifacts/source-manifest-verification-v3.json", "cdea13dfba737cb4b065aa0de3dcc62f9afbe5fffe37837ddd27c67a6aed594b"),
    "source_manifest_v3_builder": ("proof/build_source_manifest_v3.py", "74b23bd528436b7a9651aad4654a8ed424363c11dae4325cfdb8fb5f65e21c15"),
    "cycle1_reconciliation": ("artifacts/cycle-1-route-reconciliation-v3.json", "2a8c2a8edf06b9c5bfd0ae5d98e64a9f174555841aa41e3133850d94938943a8"),
    "cycle1_replay": ("proof/audit_cycle1_routes.py", "7e3ca915e6e62d9fcfdcc5ae83da59a15dc1e3ead27b24f020ea7de413e38ee1"),
    "stream_b_reconciliation": ("artifacts/cycle-2-stream-b-route-reconciliation-v2.json", "5aa163187d8365a72bfbc662e3e3d64a1efbdf18cdc26f150e6dee7b19e3c052"),
    "stream_b_replay": ("proof/reconcile_cycle2_stream_b_routes_v2.py", "90ed534d22405807ece4f7b0d43e6df273a1740f705f7c4835f2aa784e948207"),
    "stream_c_reconciliation": ("artifacts/cycle-2-stream-c-two-route-reconciliation-v2.json", "b69e0caeb5d5ed5c8072acb62263d15c2b02470df0c10889287508837c9e706d"),
    "stream_c_replay": ("proof/reconcile_cycle2_stream_c_two_routes_v2.py", "6b41bdb14e3757fdca182016e237e64a58230b06baf5be847d7448921207386b"),
    "official_source_closure": ("artifacts/cycle-2-stream-c-explicit-formula-source-closure-v4.json", "1c4ecc54be6f681be788084c3637f1101996869e09015edac8cf41e6ab39d5f0"),
    "official_source_checker": ("proof/check_cycle_2_stream_c_explicit_formula_sources_v4.py", "72107f1f31e51d2aa9d0ea0eb22c247a1643e58a898232a7fd02c3dee5508064"),
    "official_sword_audit": ("artifacts/cycle-2-mit-sword-official-bitstream-audit-v1.json", "6b4bd931a33a075d39aefc905e27e24767a9a0f08b82947afdfea46accefc4b7"),
    "official_sword_audit_replay": ("proof/audit_mit_sword_official_bitstream_v1.py", "00e6a46e575502c4ef525ce04007b701d4535a5b4e3710dbac4f2fc6bb9cc596"),
    "resource_config": ("artifacts/cycle-2-g0-per-route-resource-gate-config-v1.json", "8b4df0a64085f58a5fd21444ecb28317e70fee145d356f25c7f54052483f1378"),
    "resource_performance": ("artifacts/cycle-2-g0-per-route-resource-gate-performance-v1.json", "04127a01c96c86c0aa5fbf8673de97e42efc8022eba54e02afed019831a01afb"),
    "resource_replay": ("proof/run_cycle2_g0_resource_gate_v1.py", "60627c41eb28347cb3ee321d7d256f973c8481643a25d5a8842bfafc3c6a6533"),
    "route_a_v5": ("artifacts/cycle-2-stream-c-route-a-v5.json", "eaa6e831a147b8a509b0ddd2523515444cc3dfc6f4dc5cff0723097da047d150"),
    "route_a_v5_replay": ("proof/replay_cycle2_stream_c_route_a_v5.py", "34cc195040d61ea7bd5bb142ad244ae21fc3a1f86b7c093cdfa00fbd5f3bf076"),
    "route_b_v5": ("artifacts/cycle-2-stream-c-route-b-v5.json", "62b98779c5e65266ff0c81c26f312c73ce9a4462534e9d6a0395ef7fc9ed87c5"),
    "route_b_v5_replay": ("proof/replay_short_intervals_stream_c_route_b_v5.py", "444defd7fb03b679603dd2e65cc1ac32c1810aed07c26f80036601e00f4ef6f1"),
}
GRAPH_TO_EVIDENCE = {
    "GM-T1.1": "cycle1_reconciliation", "GM-ZD-TYPE-SPLIT": "stream_b_reconciliation", "EXT-MP-L24": "stream_b_reconciliation", "GM-ZD-SMOOTH-SEPARATE": "stream_b_reconciliation", "GM-ZD-APPLY-T1.1": "stream_b_reconciliation", "EXT-MVT": "stream_b_reconciliation", "INGHAM": "cycle1_reconciliation", "HUXLEY": "cycle1_reconciliation", "GM-T1.2": "cycle1_reconciliation", "GM-ENV-30-13": "cycle1_reconciliation", "EXT-EXPLICIT-FORMULA": "official_source_closure", "EXT-NEAR-ONE-DENSITY": "stream_c_reconciliation", "EXT-VK-ZERO-FREE": "stream_c_reconciliation", "GM-C1.3": "stream_c_reconciliation", "GM-C1.4": "stream_c_reconciliation",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str) -> dict[str, Any]:
    return json.loads((ROOT / FROZEN[name][0]).read_text())


def verify() -> dict[str, str]:
    hashes = {}
    for name, (relative, expected) in FROZEN.items():
        actual = sha256(ROOT / relative)
        assert actual == expected, f"frozen hash mismatch: {relative}"
        hashes[name] = actual
    for command in (
        [sys.executable, str(ROOT / "proof/audit_cycle1_routes.py"), "--check", str(ROOT / FROZEN["cycle1_reconciliation"][0])],
        [sys.executable, str(ROOT / "proof/reconcile_cycle2_stream_b_routes_v2.py"), "--check", str(ROOT / FROZEN["stream_b_reconciliation"][0])],
        [sys.executable, str(ROOT / "proof/reconcile_cycle2_stream_c_two_routes_v2.py"), "--check"],
        [sys.executable, str(ROOT / "proof/build_source_manifest_v3.py"), "--check"],
        [sys.executable, str(ROOT / "proof/check_cycle_2_stream_c_explicit_formula_sources_v4.py")],
        [sys.executable, str(ROOT / "proof/audit_mit_sword_official_bitstream_v1.py"), "--check"],
        [sys.executable, str(ROOT / "proof/run_cycle2_g0_resource_gate_v1.py"), "--check-config", str(ROOT / FROZEN["resource_config"][0])],
        [sys.executable, str(ROOT / "proof/replay_cycle2_stream_c_route_a_v5.py"), "--check", str(ROOT / FROZEN["route_a_v5"][0])],
        [sys.executable, str(ROOT / "proof/replay_short_intervals_stream_c_route_b_v5.py"), "--check"],
    ):
        subprocess.run(command, check=True, capture_output=True, text=True)
    return hashes


def certificate() -> dict[str, Any]:
    hashes = verify()
    cycle1, stream_b, stream_c = load("cycle1_reconciliation"), load("stream_b_reconciliation"), load("stream_c_reconciliation")
    source, closure, sword = load("source_manifest_v3"), load("official_source_closure"), load("official_sword_audit")
    config, performance = load("resource_config"), load("resource_performance")
    route_a, route_b = load("route_a_v5"), load("route_b_v5")
    assert cycle1["passed"] and len(cycle1["labeled_comparisons"]) == 24
    assert all(value["agree"] for value in cycle1["labeled_comparisons"].values())
    assert stream_b["epistemic_status"] == "PROVED" and len(stream_b["canonical_mapping_table"]) == 7
    assert all(row["comparison_status"].startswith("AGREED") for row in stream_b["canonical_mapping_table"])
    coverage = stream_c["preregistered_label_coverage"]
    assert len(coverage) == 26 and all(row["agreement"] == "EXACT" and row["route_a_status"] == row["route_b_status"] == "PROVED" for row in coverage)
    assert source["verification"]["verified"] and len(source["items"]) == 41
    assert closure["epistemic_status"] == "PROVED" and sword["epistemic_status"] == "OBSERVED"
    assert route_a["result_labels"]["uniform_theta"] == route_b["exact_transfer_invariants"]["uniform_theta"] == "17/30"
    assert route_a["result_labels"]["almost_all_theta"] == route_b["exact_transfer_invariants"]["almost_all_theta"] == "2/15"
    assert performance["resource_gate"]["gate_status"] == "PASS" and len(performance["route_results"]) == len(config["routes"]) == 4
    assert all(row["gate_status"] == "PASS" and Decimal(row["wall_seconds"]) < Decimal(60) and row["max_rss_kib"] < 262144 for row in performance["route_results"])
    graph_ids = [node["id"] for node in load("inherited_dependency_graph")["nodes"]]
    assert set(graph_ids) == set(GRAPH_TO_EVIDENCE)
    route_a_text, route_b_text = (ROOT / FROZEN["route_a_v5_replay"][0]).read_text().lower(), (ROOT / FROZEN["route_b_v5_replay"][0]).read_text().lower()
    assert "replay_short_intervals_stream_c_route_b" not in route_a_text and "stream-c-route-b-v5.json" not in route_a_text
    assert "replay_cycle2_stream_c_route_a" not in route_b_text and "stream-c-route-a-v5.json" not in route_b_text
    source_checker = (ROOT / FROZEN["official_source_checker"][0]).read_text().lower()
    assert "route_a" not in source_checker and "route_b" not in source_checker
    return {
        "artifact_id": "g0-final-gate-audit-v1", "epistemic_status": "OBSERVED",
        "claim_boundary": "Hostile fixed-scope gate audit. It evaluates whether the frozen WP0/preregistration requirements have evidence; it is not the authoritative global reconciliation and does not edit PLAN.",
        "governance_note": "PLAN.md §6 WP0 was consulted to identify the gate, but is intentionally not hash-frozen: an authoritative adoption of a G0 decision must be able to update PLAN without staling this audit.",
        "frozen_dependencies": hashes,
        "cycle1_required_labels": {"count": 24, "labels": sorted(cycle1["labeled_comparisons"]), "status": "CLOSED by exact two-route reconciliation", "epistemic_status": "OBSERVED"},
        "stream_b_required_nodes": {"count": 7, "ids": [row["id"] for row in stream_b["canonical_mapping_table"]], "status": "CLOSED by narrow two-route reconciliation", "epistemic_status": "OBSERVED"},
        "stream_c_required_labels": {"count": 26, "labels": [row["label"] for row in coverage], "status": "CLOSED by v5 hostile two-route reconciliation", "epistemic_status": "OBSERVED"},
        "inherited_dependency_nodes": [{"id": node, "evidence": GRAPH_TO_EVIDENCE[node], "status": "CLOSED within the cited bounded claim"} for node in graph_ids],
        "source_hash_locator_conditions": {"source_manifest_v3": "verified 41-item manifest", "official_formula_chain": "source closure v4 is PROVED; independent SWORD audit remains OBSERVED corroboration", "shared_route_hashes": "Stream-C reconciliation v2 checks equal closure/checker/SWORD/PDF/metadata/GM hashes", "epistemic_status": "OBSERVED"},
        "route_independence_and_circularity": {"cycle1": cycle1["route_independence"], "stream_b": stream_b["canonical_status"], "stream_c": "Route A v5 text has no Route-B reference; Route B v5 text has no Route-A reference; shared official-source checker has neither route reference; reconciliation occurs only after both sealed outputs.", "status": "NO_CIRCULARITY_OBSERVED", "epistemic_status": "OBSERVED"},
        "resource_gate": {"required": config["required_outcome"], "route_results": [{"id": row["id"], "wall_seconds": row["wall_seconds"], "max_rss_kib": row["max_rss_kib"], "status": row["gate_status"]} for row in performance["route_results"]], "status": "PASS OBSERVED operational evidence", "epistemic_status": "OBSERVED"},
        "tag_validity": {"PROVED": "Retained only for the bounded exact/source/application claims made by the sealed records.", "OBSERVED": "This audit's recommendation, source-manifest metadata role, SWORD provenance corroboration, and host resource observations remain OBSERVED.", "forbidden_promotion": ["no new zero-density theorem", "no new short-interval exponent", "no claim beyond the published GM density theorem condition"]},
        "recommendation": {"status": "PASS", "basis": "All frozen WP0, Cycle-1, Cycle-2, inherited-node, source/hash, v5 two-route-label, independence, and four-route resource conditions are closed by the checked evidence.", "scope": "Recommendation only; the authoritative project record must decide whether to adopt it.", "epistemic_status": "OBSERVED"},
        "replay": {"script_sha256": sha256(Path(__file__)), "write_command": "python3 projects/guth-maynard-zero-density/proof/audit_g0_final_gate_v1.py --write", "epistemic_status": "OBSERVED"},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = json.dumps(certificate(), indent=2, sort_keys=True) + "\n"
    if args.write:
        OUTPUT.write_text(payload)
        print(f"wrote {OUTPUT.relative_to(ROOT)}")
        return 0
    if not OUTPUT.is_file() or OUTPUT.read_text() != payload:
        print("final G0 gate audit mismatch; rerun with --write", file=sys.stderr)
        return 1
    print(json.dumps({"artifact": OUTPUT.name, "verified": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
