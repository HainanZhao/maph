#!/usr/bin/env python3
"""Build the post-geometry, post-W2, post-A-dedup research queues."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CENSUS = ROOT / "artifacts" / "w1-full-census-v1.json"
C_GEOMETRY = ROOT / "artifacts" / "engine-c-geometry-analysis-v1.json"
B_ANALYSIS = ROOT / "artifacts" / "engine-b-two-route-analysis-v1.json"
A_ANALYSIS = ROOT / "artifacts" / "engine-a-queue-analysis-v1.json"
A_FIELDS = ROOT / "artifacts" / "engine-a-field-census-v1.json"
OUTPUT = ROOT / "artifacts" / "identification-queues-v2.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    census = json.loads(CENSUS.read_text())
    by_id = {row["case_id"]: row for row in census["records"]}
    c_geometry = json.loads(C_GEOMETRY.read_text())
    b_analysis = json.loads(B_ANALYSIS.read_text())
    a_analysis = json.loads(A_ANALYSIS.read_text())
    a_fields = json.loads(A_FIELDS.read_text())

    full_b = [row for row in census["records"] if row.get("engine") == "B"]
    full_b.extend(
        by_id[case_id] for case_id in c_geometry["reroute_b_case_ids"]
    )
    screened_b = {row["case_id"] for row in b_analysis["records"]}
    pending_b = sorted(
        (row for row in full_b if row["case_id"] not in screened_b),
        key=lambda row: (
            2 * math.prod(row["both_cyc"]),
            row["finite_norm"],
            row["d"],
            row["case_id"],
        ),
    )
    b_pass = [
        row["case_id"] for row in b_analysis["records"]
        if row["classification"] == "TWO_ROUTE_PASS"
    ]
    b_no_base = [
        row["case_id"] for row in b_analysis["records"]
        if row["classification"] == "NO_ABELIAN_IMAGINARY_BASE"
    ]

    payload = {
        "schema": "effective-stark-identification-queues-v2",
        "claim_tag": "VERIFIED_QUEUE",
        "source_hashes": {
            path.name: sha(path)
            for path in [
                CENSUS, C_GEOMETRY, B_ANALYSIS, A_ANALYSIS, A_FIELDS
            ]
        },
        "ordering": ["C", "B", "A"],
        "engine_c": {
            "structural_rows": 817,
            "geometry_eligible_case_count":
                len(c_geometry["complete_c_case_ids"]),
            "geometry_eligible_case_ids":
                c_geometry["complete_c_case_ids"],
            "rerouted_to_b_case_count":
                len(c_geometry["reroute_b_case_ids"]),
            "frontier_case_count":
                len(c_geometry["frontier_cases"]),
            "tool_blocked_case_count":
                len(c_geometry["tool_blocked_case_ids"]),
            "next_gate":
                "Stark hypotheses, exact unit lattice, Arb orientation",
        },
        "engine_b": {
            "post_c_reroute_queue_count": len(full_b),
            "degree_at_most_40_screened_count": len(screened_b),
            "two_route_pass_count": len(b_pass),
            "two_route_pass_case_ids": b_pass,
            "no_abelian_imaginary_base_count": len(b_no_base),
            "no_abelian_imaginary_base_case_ids": b_no_base,
            "degree_above_40_pending_count": len(pending_b),
            "degree_above_40_pending_case_ids":
                [row["case_id"] for row in pending_b],
            "next_gate":
                "deduplicated divisor tables, then Arb identification",
        },
        "engine_a": {
            "structural_rows": a_analysis["case_count"],
            "verified_trivial_x_equals_one_count":
                a_analysis["trivial_packet_count"],
            "nontrivial_case_count": a_fields["case_count"],
            "quadratic_packet_occurrence_count":
                a_fields["quadratic_packet_occurrence_count"],
            "distinct_absolute_quartic_field_count":
                a_fields["distinct_absolute_quartic_field_count"],
            "next_gate": (
                "exact regulator indices and Euler factors, after "
                "individual C/B identification"
            ),
        },
        "priority_cases": [
            {
                "case_id": "RQ-000129",
                "engine": "C",
                "state":
                    "exact reinduction/unit lattice; Arb orientation pending",
            },
            {
                "case_id": "RQ-000419",
                "engine": "B",
                "state":
                    "two-route W2 and safe exponent 4032 verified; W3 pending",
            },
            {
                "case_id": "RQ-004467",
                "engine": "B",
                "state": (
                    "two-route W2 and safe exponent 13810176 verified; "
                    "lower W3 priority because of exponent"
                ),
            },
        ],
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "c_eligible": payload["engine_c"]["geometry_eligible_case_count"],
        "b_pass": payload["engine_b"]["two_route_pass_count"],
        "b_pending": payload["engine_b"]["degree_above_40_pending_count"],
        "a_trivial": payload["engine_a"][
            "verified_trivial_x_equals_one_count"
        ],
        "a_distinct_fields": payload["engine_a"][
            "distinct_absolute_quartic_field_count"
        ],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
