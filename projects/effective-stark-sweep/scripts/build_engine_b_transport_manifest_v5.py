#!/usr/bin/env python3
"""Freeze the v5 Engine-B member-transport manifest without promotion."""

from __future__ import annotations

from collections import defaultdict
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
DEDUP = ARTIFACTS / "genuine-b-deduplication-v5.json"
W1 = ARTIFACTS / "w1-full-census-v1.json"
V5 = ARTIFACTS / "full-census-yield-declaration-v5.json"
OLD_ANALYSIS = ARTIFACTS / "engine-b-two-route-analysis-v1.json"
OLD_COVERAGE = ARTIFACTS / "engine-b-closure-w2-coverage-v1.json"
PREREGISTRATION = ROOT / "data/census-paper-preregistration-amendment-v12.json"
OUTPUT = ARTIFACTS / "engine-b-transport-manifest-v5.json"

BANKED_REPRESENTATIVES = {
    "RQ-000021", "RQ-000108", "RQ-000190", "RQ-000419",
    "RQ-000458", "RQ-001107", "RQ-002057", "RQ-002955",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if OUTPUT.exists():
        raise RuntimeError("versioned v5 transport manifest already exists")
    preregistration = json.loads(PREREGISTRATION.read_text())
    if preregistration["status"] != "FROZEN_BEFORE_V5_ENGINE_B_MEMBER_TRANSPORT_MANIFEST":
        raise RuntimeError("transport preregistration is not frozen")
    sources = (DEDUP, W1, V5, OLD_ANALYSIS, OLD_COVERAGE, PREREGISTRATION)
    expected_hashes = preregistration["source_hashes"]
    for source in (DEDUP, W1, V5, OLD_COVERAGE):
        relative = str(source.relative_to(ROOT))
        if sha256(source) != expected_hashes[relative]:
            raise RuntimeError(f"{relative}: preregistered source changed")

    v5 = json.loads(DEDUP.read_text())
    w1 = {row["case_id"]: row for row in json.loads(W1.read_text())["records"]}
    v5_ids = {row["case_id"] for row in v5["records"]}
    declared_b_ids = {
        row["case_id"]
        for row in json.loads(V5.read_text())["classification_records"]
        if row["verdict"] == "ENGINE_B_ELIGIBLE"
    }
    if v5_ids != declared_b_ids or len(v5_ids) != 232:
        raise RuntimeError("v5 Engine-B population changed")
    if len(v5["records"]) != 232 or v5["distinct_normal_closure_count"] != 88:
        raise RuntimeError("v5 deduplication totals changed")

    old_analysis = json.loads(OLD_ANALYSIS.read_text())
    old_ids = {
        row["case_id"] for row in old_analysis["records"]
        if row["classification"] == "TWO_ROUTE_PASS"
    }
    old_polynomials = {
        row["normal_closure_absolute_field"] for row in old_analysis["records"]
        if row["classification"] == "TWO_ROUTE_PASS"
    }
    old_pending = set(json.loads(OLD_COVERAGE.read_text())["occurrence_identity_coverage"]["member_case_ids"])
    if len(old_ids) != 195 or len(old_polynomials) != 59 or len(old_pending) != 159:
        raise RuntimeError("historical Engine-B scope changed")
    if not old_ids <= v5_ids or not old_pending <= v5_ids:
        raise RuntimeError("v5 removed a historical Engine-B member")
    if len(v5_ids - old_ids) != 37 or len(v5_ids - old_pending) != 73:
        raise RuntimeError("v5 reconciliation changed")
    if not BANKED_REPRESENTATIVES <= v5_ids:
        raise RuntimeError("a banked representative is absent from v5")

    by_polynomial: dict[str, list[dict]] = defaultdict(list)
    for record in v5["records"]:
        by_polynomial[record["normal_closure_polynomial"]].append(record)
    closures = []
    member_records = []
    for index, polynomial in enumerate(sorted(by_polynomial), start=1):
        closure_id = f"B5-{index:03d}"
        members = sorted(
            by_polynomial[polynomial],
            key=lambda r: (w1[r["case_id"]]["finite_norm"], r["case_id"]),
        )
        member_ids = [member["case_id"] for member in members]
        banked = sorted(BANKED_REPRESENTATIVES & set(member_ids))
        closures.append({
            "closure_id": closure_id,
            "normal_closure_polynomial": polynomial,
            "canonical_member": member_ids[0],
            "member_count": len(member_ids),
            "member_ids": sorted(member_ids),
            "legacy_polynomial_key_present": polynomial in old_polynomials,
            "banked_representative_ids": banked,
            "transport_status": "UNSTARTED_NO_MEMBER_PROMOTION",
        })
        for member in members:
            case_id = member["case_id"]
            row = w1[case_id]
            member_records.append({
                "case_id": case_id,
                "closure_id": closure_id,
                "is_canonical_member": case_id == member_ids[0],
                "is_historical_v4_engine_b": case_id in old_ids,
                "is_historical_pending_member": case_id in old_pending,
                "is_banked_representative": case_id in BANKED_REPRESENTATIVES,
                "d": row["d"],
                "finite_ideal_hnf": row["finite_ideal_hnf"],
                "finite_norm": row["finite_norm"],
                "support_orders": row["support_orders"],
                "transport_status": "UNSTARTED_NO_CASE_LEVEL_PACKET_CLAIM",
            })
    if len(closures) != 88 or len(member_records) != 232:
        raise RuntimeError("manifest grouping changed")
    if sum(member["is_historical_v4_engine_b"] for member in member_records) != 195:
        raise RuntimeError("historical member reconciliation changed")
    if sum(c["legacy_polynomial_key_present"] for c in closures) != 59:
        raise RuntimeError("historical polynomial-key reconciliation changed")

    payload = {
        "schema": "effective-stark-engine-b-transport-manifest-v5",
        "claim_tag": "VERIFIED_V5_TRANSPORT_SCOPE_ONLY",
        "claim_boundary": {
            "closure_membership_proves_member_packet": False,
            "banked_representative_promotes_other_members": False,
            "member_transport_completed": False,
        },
        "counts": {
            "v5_engine_b_rows": len(member_records),
            "v5_distinct_normal_closures": len(closures),
            "historical_v4_engine_b_rows_retained": len(old_ids),
            "historical_pending_member_ids_retained": len(old_pending),
            "new_v5_engine_b_rows": len(v5_ids - old_ids),
            "v5_rows_outside_historical_pending_member_list": len(v5_ids - old_pending),
            "historical_v4_polynomial_keys_retained": len(old_polynomials),
            "v5_polynomial_keys_absent_from_historical_ledger": len(closures) - len(old_polynomials),
            "banked_representatives": len(BANKED_REPRESENTATIVES),
            "member_transport_completed": 0,
        },
        "closures": closures,
        "members": sorted(member_records, key=lambda r: r["case_id"]),
        "required_member_obligations": preregistration["member_transport_obligations"],
        "source_hashes": {
            str(source.relative_to(ROOT)): sha256(source) for source in sources
        },
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
