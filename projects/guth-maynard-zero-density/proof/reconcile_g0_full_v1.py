#!/usr/bin/env python3
"""Authoritative fixed-scope reconciliation of the frozen G0 gate."""
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
OUTPUT = ROOT / "artifacts/g0-full-reconstruction-v1.json"

# PLAN.md is deliberately absent: adopting this decision must update PLAN
# without invalidating the evidence that authorized the update.
FROZEN = {
    "cycle1_preregistration": ("docs/cycle-1-g0-preregistration.md", "150b4ee03383aa9be8d2301bbbc39644cb3464682a9c634b3143c1ada4fd7cf4"),
    "cycle2_preregistration": ("docs/cycle-2-g0-analytic-preregistration.md", "e07ecf8783983d20ad435bdcd1c4b0922eee0c6419b26bdd34d7a34b92a2fb63"),
    "dependency_graph": ("artifacts/g0-theorem-dependency-graph-v1.json", "14f80b35774a3994c93e1a08de34afb2aefff7023e1797932e6fb4d78af1281b"),
    "source_manifest": ("artifacts/source-manifest-verification-v3.json", "cdea13dfba737cb4b065aa0de3dcc62f9afbe5fffe37837ddd27c67a6aed594b"),
    "cycle1_reconciliation": ("artifacts/cycle-1-route-reconciliation-v3.json", "2a8c2a8edf06b9c5bfd0ae5d98e64a9f174555841aa41e3133850d94938943a8"),
    "stream_b_reconciliation": ("artifacts/cycle-2-stream-b-route-reconciliation-v2.json", "5aa163187d8365a72bfbc662e3e3d64a1efbdf18cdc26f150e6dee7b19e3c052"),
    "stream_c_reconciliation": ("artifacts/cycle-2-stream-c-two-route-reconciliation-v2.json", "b69e0caeb5d5ed5c8072acb62263d15c2b02470df0c10889287508837c9e706d"),
    "literature_gate": ("artifacts/cycle-2-g0-literature-source-gate-audit-v1.json", "e26f039a1914b67b23cf9ce1e0fe459b696601ee4b05aa7019e88a9a096cd13e"),
    "literature_gate_replay": ("proof/audit_g0_literature_source_gates_v1.py", "7bb8b6de5cfff2acaaa2bab215b9c3a0fc8abd8e646476d858d6f1019c3b5366"),
    "hostile_gate_audit": ("artifacts/g0-final-gate-audit-v1.json", "1d349dc86166f7fb98ebcaaba32fe9171f3d85f0118d436e5d19279e73a5db2e"),
    "hostile_gate_replay": ("proof/audit_g0_final_gate_v1.py", "79def8d85bb94108a01bc75696cf5b884de0dff3f352fe4ffab06a62577c6af4"),
    "resource_config": ("artifacts/cycle-2-g0-per-route-resource-gate-config-v1.json", "8b4df0a64085f58a5fd21444ecb28317e70fee145d356f25c7f54052483f1378"),
    "resource_performance": ("artifacts/cycle-2-g0-per-route-resource-gate-performance-v1.json", "04127a01c96c86c0aa5fbf8673de97e42efc8022eba54e02afed019831a01afb"),
    "resource_replay": ("proof/run_cycle2_g0_resource_gate_v1.py", "60627c41eb28347cb3ee321d7d256f973c8481643a25d5a8842bfafc3c6a6533"),
    "matrix_v3_correction": ("artifacts/g0-dependency-evidence-matrix-v3.json", "d66a2ee235658f8d4fd92864e6a8737fc47a56ea745464fcd77945217207ac66"),
    "matrix_v3_replay": ("proof/audit_g0_dependency_evidence_v3.py", "c85df329914e47d691070402289d4fca6d8afdefcd6254c27d4ee439b0d7c453"),
}

EXPECTED_GRAPH_IDS = {
    "GM-T1.1", "GM-ZD-TYPE-SPLIT", "EXT-MP-L24",
    "GM-ZD-SMOOTH-SEPARATE", "GM-ZD-APPLY-T1.1", "EXT-MVT",
    "INGHAM", "HUXLEY", "GM-T1.2", "GM-ENV-30-13",
    "EXT-EXPLICIT-FORMULA", "EXT-NEAR-ONE-DENSITY",
    "EXT-VK-ZERO-FREE", "GM-C1.3", "GM-C1.4",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(key: str) -> dict[str, Any]:
    return json.loads((ROOT / FROZEN[key][0]).read_text(encoding="utf-8"))


def verify_frozen_inputs() -> dict[str, str]:
    hashes: dict[str, str] = {}
    for key, (relative, expected) in FROZEN.items():
        actual = sha256(ROOT / relative)
        assert actual == expected, f"frozen G0 input changed: {relative}"
        hashes[key] = actual
    commands = (
        ("proof/audit_cycle1_routes.py", "--check", "artifacts/cycle-1-route-reconciliation-v3.json"),
        ("proof/reconcile_cycle2_stream_b_routes_v2.py", "--check", "artifacts/cycle-2-stream-b-route-reconciliation-v2.json"),
        ("proof/reconcile_cycle2_stream_c_two_routes_v2.py", "--check"),
        ("proof/build_source_manifest_v3.py", "--check"),
        ("proof/audit_g0_literature_source_gates_v1.py", "--check"),
        ("proof/audit_g0_final_gate_v1.py", "--check"),
        ("proof/audit_g0_dependency_evidence_v3.py", "--check"),
        ("proof/run_cycle2_g0_resource_gate_v1.py", "--check-config", "artifacts/cycle-2-g0-per-route-resource-gate-config-v1.json"),
    )
    for command in commands:
        subprocess.run((sys.executable, *command), cwd=ROOT, check=True,
                       capture_output=True, text=True)
    return hashes


def adjudicate() -> dict[str, Any]:
    hashes = verify_frozen_inputs()
    graph = load("dependency_graph")
    manifest = load("source_manifest")
    cycle1 = load("cycle1_reconciliation")
    stream_b = load("stream_b_reconciliation")
    stream_c = load("stream_c_reconciliation")
    literature = load("literature_gate")
    hostile = load("hostile_gate_audit")
    config = load("resource_config")
    performance = load("resource_performance")
    matrix = load("matrix_v3_correction")

    graph_ids = {row["id"] for row in graph["nodes"]}
    hostile_nodes = {row["id"] for row in hostile["inherited_dependency_nodes"]}
    assert graph_ids == hostile_nodes == EXPECTED_GRAPH_IDS

    assert cycle1["passed"] is True
    assert len(cycle1["labeled_comparisons"]) == 24
    assert all(row["agree"] for row in cycle1["labeled_comparisons"].values())

    b_rows = stream_b["canonical_mapping_table"]
    assert stream_b["epistemic_status"] == "PROVED"
    assert len(b_rows) == 7
    assert all(row["epistemic_status"] == "PROVED" for row in b_rows)
    assert all(row["comparison_status"].startswith("AGREED") for row in b_rows)
    assert stream_b["agreement_summary"]["coverage_gaps_open"] == 0

    c_rows = stream_c["preregistered_label_coverage"]
    assert stream_c["epistemic_status"] == "PROVED"
    assert len(c_rows) == 26
    assert stream_c["independent_narrow_stream_c_pass"]["gaps"] == []
    assert all(row["agreement"] == "EXACT" for row in c_rows)
    assert all(row["route_a_status"] == row["route_b_status"] == "PROVED" for row in c_rows)

    source_rows = literature["source_gates"]
    assert literature["epistemic_status"] == "PROVED"
    assert literature["recommendation"]["source_hypothesis_gate"] == "PASS"
    assert len(source_rows) == 8 and all(row["status"] == "PROVED" for row in source_rows)
    assert literature["unread_or_disjunctive_source_audit"]["result"] == "NO UNREAD OR DISJUNCTIVE SOURCE ON THE SELECTED PROMOTED PATH"
    assert manifest["verification"]["verified"] is True and len(manifest["items"]) == 41

    assert hostile["recommendation"]["status"] == "PASS"
    assert hostile["route_independence_and_circularity"]["status"] == "NO_CIRCULARITY_OBSERVED"
    assert len(hostile["inherited_dependency_nodes"]) == len(EXPECTED_GRAPH_IDS)

    expected_routes = [row["id"] for row in config["routes"]]
    measured = performance["route_results"]
    assert [row["id"] for row in measured] == expected_routes
    assert len(measured) == 4 and performance["resource_gate"]["gate_status"] == "PASS"
    for row in measured:
        assert row["gate_status"] == "PASS"
        assert row["subprocess_returncode"] == row["time_exit_status"] == 0
        assert row["parse_error"] is None
        assert Decimal(row["wall_seconds"]) < Decimal(60)
        assert row["max_rss_kib"] < 262144

    correction = matrix["v2_in_place_refresh_correction"]
    assert correction["pre_refresh_v2_identity"].startswith("UNRECOVERABLE_FROM_LOCAL_WORKTREE")
    assert correction["post_refresh_v2_sha256"] == "504cc31047ba8191cd1996ee7238cf3f95ab8e007f75824b39307999abb131ae"

    graph_evidence = {
        row["id"]: {
            "evidence": row["evidence"],
            "status": "CLOSED",
            "epistemic_status": "PROVED within the cited bounded source/application claim",
        }
        for row in hostile["inherited_dependency_nodes"]
    }
    resource_rows = [
        {
            "id": row["id"],
            "wall_seconds": row["wall_seconds"],
            "max_rss_kib": row["max_rss_kib"],
            "status": "PASS",
            "epistemic_status": "OBSERVED",
        }
        for row in measured
    ]
    gates = [
        {"id": "G0-CYCLE1-EXACT", "requirement": "two independent exact derivations reproduce every frozen exponent and boundary", "evidence": "24/24 exact labeled comparisons in Cycle-1 reconciliation v3", "status": "PASS", "epistemic_status": "PROVED"},
        {"id": "G0-ANALYTIC-NODES", "requirement": "every inherited unread/indirect node is checked or removed from the selected path", "evidence": "15/15 graph nodes mapped; 8/8 selected literature/source gates pass; unused alternatives are explicitly excluded", "status": "PASS", "epistemic_status": "PROVED"},
        {"id": "G0-STREAM-B", "requirement": "all Section 13.1 application transfers reconcile independently", "evidence": "7/7 Stream-B reconciliation rows agree with zero open coverage gaps", "status": "PASS", "epistemic_status": "PROVED"},
        {"id": "G0-DOWNSTREAM-TWO-ROUTE", "requirement": "both downstream routes agree on every boundary and secondary condition", "evidence": "26/26 Stream-C labels agree exactly with zero gaps", "status": "PASS", "epistemic_status": "PROVED"},
        {"id": "G0-SOURCE-CONVENTIONS", "requirement": "source hashes, locators, conventions, and transformations reconcile", "evidence": "41-item source manifest, 8 source gates, official formula chain, and shared-route hashes all verify", "status": "PASS", "epistemic_status": "PROVED for exact checked identities and published-source hypotheses"},
        {"id": "G0-INDEPENDENCE", "requirement": "the two routes are genuinely independent and reconciliation is non-circular", "evidence": "separate route implementations and sealed outputs; hostile structural audit found no cross-route replay/artifact dependency", "status": "PASS", "epistemic_status": "OBSERVED structural audit"},
        {"id": "G0-RESOURCES", "requirement": "each current route exits zero in strictly under 60 seconds and 256 MiB", "evidence": resource_rows, "status": "PASS", "epistemic_status": "OBSERVED host-specific measurements"},
    ]
    assert all(row["status"] == "PASS" for row in gates)

    return {
        "artifact_id": "g0-full-reconstruction-v1",
        "certificate_version": 1,
        "epistemic_status": "PROVED",
        "claim_boundary": "PROVED authoritative adjudication that the frozen G0 reconstruction gate passes, conditional on the cited published analytic theorems whose selected hypotheses were checked. This is an exact reconstruction of published Guth--Maynard consequences, not a new zero-density theorem, not a new short-interval exponent, and not evidence for any G1 candidate.",
        "decision": {
            "gate": "G0",
            "status": "PASS",
            "open_blockers": [],
            "authorized_next_path": "P1 critical-cell and extremizer atlas, after its search parameters are preregistered",
            "epistemic_status": "PROVED exact gate adjudication",
        },
        "frozen_dependencies": hashes,
        "gate_rows": gates,
        "inherited_dependency_nodes": graph_evidence,
        "counts": {
            "cycle1_exact_labels": 24,
            "stream_b_reconciliation_rows": 7,
            "stream_c_reconciliation_labels": 26,
            "inherited_graph_nodes": 15,
            "selected_source_gates": 8,
            "source_manifest_items": 41,
            "resource_routes": 4,
        },
        "corrections_preserved": {
            "g0_matrix_v2_in_place_refresh": "CONTAINED by matrix v3; pre-refresh identity remains unrecoverable and is not guessed",
            "stream_c_legacy_timing_bytes": "CONTAINED by timing-free Stream-C reconciliation v2 semantic identities",
            "official_formula_provenance": "CORRECTED by official source closure v4; author-copy license/byte-identity claims are not used",
            "stale_huxley_title_metadata": "OBSERVED non-blocking maintenance finding; frozen hash and equation locator identify the checked article",
        },
        "non_promotions": [
            "no improvement beyond 30/13",
            "no uniform short-interval exponent below 17/30",
            "no almost-all exponent below 2/15",
            "no method-saturation theorem",
            "no L-function-family extension",
        ],
        "falsifier": "Any failed frozen hash/check, open inherited node, nonexact route label, circular route dependency, or route measurement at or above a strict resource ceiling invalidates this certificate and reopens G0.",
        "replay": {
            "script_sha256": sha256(Path(__file__)),
            "write_command": "python3 projects/guth-maynard-zero-density/proof/reconcile_g0_full_v1.py --write",
            "check_command": "python3 projects/guth-maynard-zero-density/proof/reconcile_g0_full_v1.py --check",
        },
    }


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = render(adjudicate())
    if args.write:
        OUTPUT.write_text(payload, encoding="utf-8")
        print(f"wrote {OUTPUT.relative_to(ROOT)}")
        return 0
    if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != payload:
        print("G0 full reconstruction mismatch; rerun with --write", file=sys.stderr)
        return 1
    print(json.dumps({"artifact": OUTPUT.name, "gate": "G0", "status": "PASS", "verified": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
