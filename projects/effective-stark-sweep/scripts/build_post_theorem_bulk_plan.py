#!/usr/bin/env python3
"""Freeze closure-batched B, staged C, A, and overlap queues."""

from __future__ import annotations

from collections import defaultdict
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
B_SOURCE = ROOT / "artifacts/engine-b-two-route-analysis-v1.json"
C_SOURCE = ROOT / "artifacts/engine-c-e-inventory-v1.json"
A_THEOREM = ROOT / "data/engine-a-uniform-theorem-v1.json"
OVERLAPS = ROOT / "artifacts/dual-engine-alignment-queue-v1.json"
OUTPUT = ROOT / "artifacts/post-theorem-bulk-plan-v1.json"

CLOSED_B_CASES = {
    "RQ-000021",
    "RQ-000108",
    "RQ-000190",
    "RQ-000419",
    "RQ-000458",
    "RQ-001107",
    "RQ-002057",
    "RQ-002955",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    b = json.loads(B_SOURCE.read_text())
    c = json.loads(C_SOURCE.read_text())
    a = json.loads(A_THEOREM.read_text())
    overlaps = json.loads(OVERLAPS.read_text())
    by_closure = defaultdict(list)
    for record in b["records"]:
        if record["classification"] == "TWO_ROUTE_PASS":
            by_closure[record["normal_closure_absolute_field"]].append(
                record
            )
    if len(by_closure) != 59:
        raise RuntimeError("B closure count changed")

    closed, remaining = [], []
    for index, (polynomial, records) in enumerate(
        sorted(by_closure.items()), start=1
    ):
        case_ids = sorted(record["case_id"] for record in records)
        banked = sorted(CLOSED_B_CASES & set(case_ids))
        item = {
            "closure_index": index,
            "normal_closure_absolute_field": polynomial,
            "normal_closure_degree": records[0]["normal_closure_degree"],
            "abelian_imaginary_bases":
                records[0]["abelian_imaginary_bases"],
            "occurrence_count": len(records),
            "case_ids": case_ids,
            "canonical_representative": min(
                records,
                key=lambda record: (
                    record["finite_norm"], record["case_id"]
                ),
            )["case_id"],
            "banked_verified_cases": banked,
        }
        (closed if banked else remaining).append(item)
    if len(closed) != 8 or len(remaining) != 51:
        raise RuntimeError("expected 8 banked and 51 remaining B closures")

    direct_banked = len(CLOSED_B_CASES)
    all_b_occurrences = sum(
        item["occurrence_count"] for item in closed + remaining
    )
    extra_members_banked_closures = (
        sum(item["occurrence_count"] for item in closed) - direct_banked
    )
    remaining_closure_occurrences = sum(
        item["occurrence_count"] for item in remaining
    )

    remaining_overlaps = [
        record for record in overlaps["records"]
        if record["case_id"] != "RQ-000458"
    ]
    if len(remaining_overlaps) != 10:
        raise RuntimeError("remaining overlap count changed")

    output = {
        "schema": "effective-stark-post-theorem-bulk-plan-v1",
        "claim_tag": "VERIFIED_QUEUE_DECOMPOSITION",
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (B_SOURCE, C_SOURCE, A_THEOREM, OVERLAPS)
        },
        "engine_a": {
            "gate": a["bulk_gate"],
            "nontrivial_occurrences": 1560,
            "supported_character_occurrences": 2232,
            "distinct_quartic_fields": 912,
            "execution": (
                "Deduplicate by quartic field, verify the exact finite "
                "theorem record once, then transport and orient every "
                "occurrence."
            ),
        },
        "engine_b": {
            "eligible_occurrences": all_b_occurrences,
            "distinct_closures": len(by_closure),
            "banked_closure_count": len(closed),
            "remaining_closure_count": len(remaining),
            "remaining_closure_occurrence_count":
                remaining_closure_occurrences,
            "unverified_members_of_banked_closures":
                extra_members_banked_closures,
            "remaining_occurrence_identities":
                all_b_occurrences - direct_banked,
            "protocol": [
                "One two-route/divisor audit per normal closure.",
                "One canonical W3 packet identification per closure.",
                "Exact member-modulus ray-class and orientation transport; closure equality alone does not promote an occurrence."
            ],
            "banked_closures": closed,
            "remaining_closures": remaining,
        },
        "engine_c": {
            "eligible_cases": c["scope"]["eligible_case_count"],
            "eligible_packet_occurrences":
                c["scope"]["eligible_packet_occurrence_count"],
            "distinct_packet_fields":
                c["scope"]["distinct_packet_field_count"],
            "open_on_banked_e_2_4": c["case_staging"][
                "BANKED_GENERAL_E_2_4"
            ],
            "blocked_on_general_e_gt_4": c["case_staging"][
                "BLOCKED_GENERAL_E_GT_4"
            ],
            "minimum_e_histogram_fields":
                c["field_minimum_e_histogram"],
            "minimum_e_histogram_occurrences":
                c["occurrence_minimum_e_histogram"],
            "protocol": (
                "Run all-e<=4 cases on banked lemmas. Queue every case "
                "with any packet minimum e>4 behind the general-e "
                "normalization and orientation work; Q(sqrt(6)) is the "
                "e=(8,12) control."
            ),
        },
        "remaining_overlap_alignment_queue": {
            "state": "READY_AFTER_BULK_PLAN_FREEZE",
            "candidate_count": len(remaining_overlaps),
            "records": remaining_overlaps,
            "claim_boundary": (
                "Alignment checks only; no DUAL_PROVED promotion without "
                "two independent W3 bundles."
            ),
        },
        "w4_gate": (
            "OPEN_ONLY_AFTER_A_B_C_BULK_AND_OCCURRENCE_TRANSPORT_CLOSE"
        ),
        "w4_queue": [
            "index distribution",
            "FRONTIER share versus conductor norm",
            "safe-exponent growth law",
            "packet polynomial families",
            "dimension-tower recurrences"
        ],
    }
    OUTPUT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "a_fields": output["engine_a"]["distinct_quartic_fields"],
        "b_remaining_closures":
            output["engine_b"]["remaining_closure_count"],
        "b_remaining_occurrence_identities":
            output["engine_b"]["remaining_occurrence_identities"],
        "c_open_cases":
            output["engine_c"]["open_on_banked_e_2_4"]["case_count"],
        "c_blocked_cases":
            output["engine_c"]["blocked_on_general_e_gt_4"]["case_count"],
        "remaining_overlaps":
            output["remaining_overlap_alignment_queue"]["candidate_count"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
