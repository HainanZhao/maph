#!/usr/bin/env python3
"""Analyze the completed Engine-C geometry transcript."""

from __future__ import annotations

import collections
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "artifacts" / "engine-c-geometry-full-v1.json"
TRANSCRIPT = (
    ROOT / "artifacts" / "engine-c-geometry-full-v1.transcript"
)
OUTPUT = ROOT / "artifacts" / "engine-c-geometry-analysis-v1.json"
CENSUS = ROOT / "artifacts" / "w1-full-census-v1.json"


HEADER = re.compile(r"^===== (RQ-\d+) PACKET (\d+) =====$")


def field(lines: list[str], suffix: str) -> str | None:
    matches = [
        line.split("=", 1)[1]
        for line in lines
        if line.split("=", 1)[0].endswith(suffix)
    ]
    if not matches:
        return None
    if len(matches) != 1:
        raise RuntimeError(f"multiple {suffix} fields")
    return matches[0]


def main() -> None:
    result = json.loads(RESULT.read_text())
    census = {
        row["case_id"]: row
        for row in json.loads(CENSUS.read_text())["records"]
    }
    sections = []
    current_header = None
    current_lines: list[str] = []
    for raw_line in TRANSCRIPT.read_text().splitlines():
        match = HEADER.match(raw_line)
        if match:
            if current_header is not None:
                sections.append((*current_header, current_lines))
            current_header = (match.group(1), int(match.group(2)))
            current_lines = []
        elif current_header is not None:
            current_lines.append(raw_line)
    if current_header is not None:
        sections.append((*current_header, current_lines))

    taxonomy = collections.Counter()
    cm_base_pairs = collections.Counter()
    packet_records = []
    for case_id, packet_index, lines in sections:
        blocked = any(
            line == "TOOL_BLOCKED_PARI_2_15_4=1" for line in lines
        )
        if blocked:
            taxonomy["TOOL_BLOCKED"] += 1
            packet_records.append({
                "case_id": case_id,
                "packet_index": packet_index,
                "status": "TOOL_BLOCKED",
            })
            continue
        pass_value = field(lines, "_C_GEOMETRY_PASS")
        degree = field(lines, "_NORMAL_CLOSURE_DEGREE")
        group = field(lines, "_NORMAL_CLOSURE_GROUP")
        bases = field(lines, "_LINEAR_REINDUCTION_BASES")
        base_present = field(lines, "_REAL_BASE_PRESENT")
        if pass_value is None:
            raise RuntimeError(
                f"{case_id} packet {packet_index}: missing verdict"
            )
        if pass_value == "1":
            status = "GEOMETRY_PASS"
            taxonomy[status] += 1
            if bases is None:
                raise RuntimeError("passing packet has no CM bases")
            cm_base_pairs[bases] += 1
        elif degree != "16":
            status = "NORMAL_CLOSURE_ORDER_NE_16"
            taxonomy[status] += 1
        elif group != "[16, 13]":
            status = "NORMAL_CLOSURE_GROUP_NOT_16_13"
            taxonomy[status] += 1
        elif base_present != "1":
            status = "REAL_BASE_IDENTIFICATION_FAIL"
            taxonomy[status] += 1
        else:
            status = "LINEAR_REINDUCTION_BASE_COUNT_FAIL"
            taxonomy[status] += 1
        packet_records.append({
            "case_id": case_id,
            "packet_index": packet_index,
            "status": status,
            "normal_closure_degree": degree,
            "normal_closure_group": group,
            "linear_reinduction_bases": bases,
        })

    expected = result["packet_count"]
    if len(packet_records) != expected:
        raise RuntimeError(
            f"expected {expected} packet records, got {len(packet_records)}"
        )
    if taxonomy["GEOMETRY_PASS"] != result["geometry_pass_count"]:
        raise RuntimeError("geometry pass count mismatch")
    if taxonomy["TOOL_BLOCKED"] != result["tool_blocked_packet_count"]:
        raise RuntimeError("tool-blocked count mismatch")

    case_status = collections.Counter()
    by_case: dict[str, list[str]] = collections.defaultdict(list)
    for packet in packet_records:
        by_case[packet["case_id"]].append(packet["status"])
    for statuses in by_case.values():
        if "TOOL_BLOCKED" in statuses:
            case_status["HAS_TOOL_BLOCK"] += 1
        elif all(status == "GEOMETRY_PASS" for status in statuses):
            case_status["ALL_PACKETS_PASS"] += 1
        elif any(status == "GEOMETRY_PASS" for status in statuses):
            case_status["MIXED_PASS_FAIL"] += 1
        else:
            case_status["NO_PACKET_PASSES"] += 1

    reroute_b = []
    final_frontier = []
    tool_blocked_cases = []
    complete_c = []
    for case_id, statuses in sorted(by_case.items()):
        if "TOOL_BLOCKED" in statuses:
            tool_blocked_cases.append(case_id)
        elif all(status == "GEOMETRY_PASS" for status in statuses):
            complete_c.append(case_id)
        else:
            row = census[case_id]
            b_pass = (
                row["b03_positive_not_minus_one"]
                and row["b06_negative_norm_not_one"]
                and row["shintani_index"] == 2
                and row["exactly_one_real_place_splitting"]
            )
            if b_pass:
                reroute_b.append(case_id)
            else:
                obstruction = (
                    "INDEX_GT_2"
                    if row["shintani_index"] != 2
                    else "REAL_PLACE_SPLITTING_FAIL"
                )
                final_frontier.append({
                    "case_id": case_id,
                    "obstruction": obstruction,
                })

    output = {
        "schema": "effective-stark-engine-c-geometry-analysis-v1",
        "result_sha256": hashlib.sha256(RESULT.read_bytes()).hexdigest(),
        "transcript_sha256":
            hashlib.sha256(TRANSCRIPT.read_bytes()).hexdigest(),
        "packet_count": len(packet_records),
        "packet_taxonomy": dict(sorted(taxonomy.items())),
        "case_taxonomy": dict(sorted(case_status.items())),
        "distinct_cm_base_pairs": len(cm_base_pairs),
        "top_cm_base_pairs": [
            {"pair": pair, "packet_count": count}
            for pair, count in cm_base_pairs.most_common(20)
        ],
        "case_routing_after_complete_c_gate": {
            "C_ELIGIBLE": len(complete_c),
            "REROUTE_B": len(reroute_b),
            "FRONTIER": len(final_frontier),
            "TOOL_BLOCKED": len(tool_blocked_cases),
        },
        "complete_c_case_ids": complete_c,
        "reroute_b_case_ids": reroute_b,
        "frontier_cases": final_frontier,
        "tool_blocked_case_ids": tool_blocked_cases,
        "packet_records": packet_records,
    }
    OUTPUT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "packet_taxonomy": output["packet_taxonomy"],
        "case_taxonomy": output["case_taxonomy"],
        "distinct_cm_base_pairs": output["distinct_cm_base_pairs"],
        "top_cm_base_pairs": output["top_cm_base_pairs"][:10],
        "case_routing_after_complete_c_gate":
            output["case_routing_after_complete_c_gate"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
