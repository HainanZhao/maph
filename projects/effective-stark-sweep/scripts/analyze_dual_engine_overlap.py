#!/usr/bin/env python3
"""Locate packet-level C passes inside corrected Engine-B pass cases."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
C_ANALYSIS = ROOT / "artifacts" / "engine-c-geometry-analysis-v1.json"
B_RESCREEN = ROOT / "artifacts" / "corrected-battery-b195-v1.json"
OUTPUT = ROOT / "artifacts" / "dual-engine-alignment-queue-v1.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    c_data = json.loads(C_ANALYSIS.read_text(encoding="utf-8"))
    b_data = json.loads(B_RESCREEN.read_text(encoding="utf-8"))
    if b_data["verdict"] != "CORRECTED_BATTERY_195_OF_195_PASSED":
        raise RuntimeError("corrected B population is not a closed gate")

    c_by_case: dict[str, list[dict]] = defaultdict(list)
    for packet in c_data["packet_records"]:
        c_by_case[packet["case_id"]].append(packet)
    b_pass = {
        record["case_id"]: record
        for record in b_data["records"]
        if record["passed"]
    }

    records = []
    for case_id in sorted(set(c_by_case) & set(b_pass)):
        packets = c_by_case[case_id]
        passing = [
            packet for packet in packets if packet["status"] == "GEOMETRY_PASS"
        ]
        if not passing:
            continue
        b_record = b_pass[case_id]
        records.append(
            {
                "case_id": case_id,
                "d": b_record["d"],
                "finite_norm": b_record["finite_norm"],
                "finite_ideal_hnf": b_record["finite_ideal_hnf"],
                "c_passing_packet_indices": [
                    packet["packet_index"] for packet in passing
                ],
                "c_passing_packet_bases": [
                    packet["linear_reinduction_bases"]
                    for packet in passing
                ],
                "c_all_packet_statuses": [
                    {
                        "packet_index": packet["packet_index"],
                        "status": packet["status"],
                    }
                    for packet in packets
                ],
                "b_abelian_imaginary_bases": b_record["actual"][
                    "abelian_imaginary_bases"
                ],
                "b_two_route_match_count": b_record["actual"][
                    "two_route_ray_subfield_match_count"
                ],
                "state": "ELEVATED_SAME_PACKET_ALIGNMENT_REQUIRED",
                "claim_boundary": (
                    "This is a packet-level C geometry pass and a case-level "
                    "B two-route pass, not yet two proofs of the same packet. "
                    "Promotion requires exact character/Artin-orbit alignment."
                ),
            }
        )

    records.sort(
        key=lambda record: (
            record["finite_norm"],
            record["d"],
            record["case_id"],
        )
    )
    payload = {
        "schema": "effective-stark-dual-engine-alignment-queue-v1",
        "claim_tag": "VERIFIED_GATE_INTERSECTION",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_hashes": {
            "engine_c_analysis_sha256": sha256(C_ANALYSIS),
            "corrected_b195_sha256": sha256(B_RESCREEN),
        },
        "candidate_count": len(records),
        "records": records,
        "protocol": {
            "priority": "IMMEDIATE_ELEVATION_AHEAD_OF_SINGLE_ENGINE_CLOSURES",
            "promotion_gate": (
                "Both engines independently identify the same exact packet "
                "and the same oriented Artin labeling."
            ),
            "mismatch_disposition": "HALT_AND_REPORT_ENGINE_DISAGREEMENT",
        },
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"DUAL_ENGINE_CANDIDATE_COUNT={len(records)}")
    for index, record in enumerate(records, start=1):
        print(
            f"DUAL_ENGINE_PRIORITY={index} CASE={record['case_id']} "
            f"NORM={record['finite_norm']}"
        )
    print(f"OUTPUT_SHA256={sha256(OUTPUT)}")


if __name__ == "__main__":
    main()
