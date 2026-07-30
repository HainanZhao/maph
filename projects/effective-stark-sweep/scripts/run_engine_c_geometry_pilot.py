#!/usr/bin/env python3
"""Run the exact Engine-C geometry screen on a frozen diverse pilot."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CENSUS = ROOT / "artifacts" / "w1-full-census-v1.json"
GP_SCRIPT = ROOT / "scripts" / "screen_engine_c_geometry.gp"
QUARANTINE = ROOT / "data" / "engine-c-tool-quarantine-v1.json"
def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_scalar(lines: list[str], key: str) -> str:
    prefix = f"{key}="
    values = [line[len(prefix):] for line in lines if line.startswith(prefix)]
    if len(values) != 1:
        raise RuntimeError(f"expected one {key}, got {len(values)}")
    return values[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true")
    arguments = parser.parse_args()
    census = json.loads(CENSUS.read_text())
    quarantine_data = json.loads(QUARANTINE.read_text())
    quarantined = {
        (entry["case_id"], entry["packet_index"]): entry
        for entry in quarantine_data["entries"]
    }
    candidates = [
        row for row in census["records"] if row.get("engine") == "C"
    ]
    # Freeze diversity by taking the first occurrence of each
    # (field, one-place group, both-place group) signature, then fill
    # to 20 by increasing case id.
    if arguments.full:
        selected = candidates
        output_path = (
            ROOT / "artifacts" / "engine-c-geometry-full-v1.json"
        )
        transcript_path = (
            ROOT / "artifacts" / "engine-c-geometry-full-v1.transcript"
        )
        selection = "all 817 frozen structural Engine-C candidates"
    else:
        selected = []
        signatures = set()
        for row in candidates:
            signature = (
                row["d"], tuple(row["one_cyc"]), tuple(row["both_cyc"])
            )
            if signature not in signatures:
                signatures.add(signature)
                selected.append(row)
        for row in candidates:
            if row not in selected:
                selected.append(row)
            if len(selected) == 20:
                break
        selected = selected[:20]
        output_path = (
            ROOT / "artifacts" / "engine-c-geometry-pilot-v1.json"
        )
        transcript_path = (
            ROOT / "artifacts" / "engine-c-geometry-pilot-v1.transcript"
        )
        selection = "first 20 after signature-diverse prefix"

    records = []
    blocked_packets = []
    transcript_path.write_text("")
    for row in selected:
        hnf = row["finite_ideal_hnf"]
        expected_packets = row["c_quartic_count"] // 2
        if expected_packets < 1:
            raise RuntimeError(
                f"{row['case_id']}: no quartic inverse pair"
            )
        packet_count = 0
        pass_count = 0
        for packet_index in range(1, expected_packets + 1):
            quarantine_entry = quarantined.get(
                (row["case_id"], packet_index)
            )
            if quarantine_entry is not None:
                blocked_packets.append(quarantine_entry)
                with transcript_path.open("a") as transcript_file:
                    transcript_file.write(
                        f"===== {row['case_id']} PACKET "
                        f"{packet_index} =====\n"
                        "TOOL_BLOCKED_PARI_2_15_4=1\n"
                    )
                continue
            prelude = (
                f'CASE_ID="{row["case_id"]}";\n'
                f'D_VALUE={row["d"]};\n'
                f'H11={hnf[0][0]};H12={hnf[0][1]};'
                f'H21={hnf[1][0]};H22={hnf[1][1]};\n'
                f'PACKET_FILTER={packet_index};\n'
            )
            try:
                completed = subprocess.run(
                    ["gp", "-q"],
                    input=(prelude + GP_SCRIPT.read_text()).encode(),
                    check=True,
                    capture_output=True,
                    cwd=ROOT,
                )
            except subprocess.CalledProcessError as error:
                failure = {
                    "schema": "effective-stark-engine-c-geometry-failure-v9",
                    "case_id": row["case_id"],
                    "packet_index": packet_index,
                    "completed_case_count": len(records),
                    "returncode": error.returncode,
                    "stdout": error.stdout.decode(errors="replace"),
                    "stderr": error.stderr.decode(errors="replace"),
                }
                failure_path = (
                    ROOT / "artifacts" /
                    "engine-c-geometry-failed-v9.json"
                )
                failure_path.write_text(
                    json.dumps(failure, indent=2, sort_keys=True) + "\n"
                )
                raise
            text = completed.stdout.decode()
            lines = [
                line.strip() for line in text.splitlines() if line.strip()
            ]
            with transcript_path.open("a") as transcript_file:
                transcript_file.write(
                    f"===== {row['case_id']} PACKET "
                    f"{packet_index} =====\n{text}"
                )
            try:
                packet_count += int(parse_scalar(lines, "PACKET_COUNT"))
                pass_count += int(
                    parse_scalar(lines, "GEOMETRY_PASS_COUNT")
                )
            except (RuntimeError, ValueError) as error:
                failure = {
                    "schema": "effective-stark-engine-c-geometry-failure-v9",
                    "case_id": row["case_id"],
                    "packet_index": packet_index,
                    "completed_case_count": len(records),
                    "returncode": completed.returncode,
                    "parse_error": str(error),
                    "stdout": text,
                    "stderr": completed.stderr.decode(errors="replace"),
                }
                failure_path = (
                    ROOT / "artifacts" /
                    "engine-c-geometry-failed-v9.json"
                )
                failure_path.write_text(
                    json.dumps(failure, indent=2, sort_keys=True) + "\n"
                )
                raise
        blocked_for_case = sum(
            entry["case_id"] == row["case_id"]
            for entry in blocked_packets
        )
        if packet_count + blocked_for_case != expected_packets:
            raise RuntimeError(
                f"{row['case_id']}: expected {expected_packets} packets, "
                f"screened {packet_count}, blocked {blocked_for_case}"
            )
        records.append({
            "case_id": row["case_id"],
            "d": row["d"],
            "finite_norm": row["finite_norm"],
            "finite_ideal_hnf": hnf,
            "one_cyc": row["one_cyc"],
            "both_cyc": row["both_cyc"],
            "packet_count": expected_packets,
            "screened_packet_count": packet_count,
            "geometry_pass_count": pass_count,
            "tool_blocked_packet_count": blocked_for_case,
        })
        if arguments.full and len(records) % 100 == 0:
            print(f"COMPLETED={len(records)}", flush=True)
    output = {
        "schema": "effective-stark-engine-c-geometry-pilot-v1",
        "source_census_sha256": sha256(CENSUS),
        "screen_sha256": sha256(GP_SCRIPT),
        "quarantine_sha256": sha256(QUARANTINE),
        "selection": selection,
        "case_count": len(records),
        "packet_count": sum(row["packet_count"] for row in records),
        "screened_packet_count": sum(
            row["screened_packet_count"] for row in records
        ),
        "tool_blocked_packet_count": len(blocked_packets),
        "tool_blocked_packets": blocked_packets,
        "geometry_pass_count": sum(
            row["geometry_pass_count"] for row in records
        ),
        "records": records,
    }
    output_path.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
