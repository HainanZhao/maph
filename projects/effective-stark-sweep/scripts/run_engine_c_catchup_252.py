#!/usr/bin/env python3
"""Run complete Engine-C geometry on the 252 proxy-excluded quartic rows."""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
W1 = ARTIFACTS / "w1-full-census-v1.json"
QUEUE = ARTIFACTS / "proxy-recovery-queue-v1.json"
SCREEN = ROOT / "scripts/screen_engine_c_geometry.gp"
QUARANTINE = ROOT / "data/engine-c-tool-quarantine-v1.json"
OUTPUT = ARTIFACTS / "engine-c-catchup-252-v1.json"
TRANSCRIPTS = ARTIFACTS / "engine-c-catchup-252-v1"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def field(text: str, suffix: str) -> str | None:
    matches = [
        line.split("=", 1)[1]
        for line in text.splitlines()
        if "=" in line and line.split("=", 1)[0].endswith(suffix)
    ]
    if not matches:
        return None
    if len(matches) != 1:
        raise RuntimeError(f"multiple {suffix} fields")
    return matches[0]


def packet_status(text: str) -> tuple[str, dict]:
    pass_value = field(text, "_C_GEOMETRY_PASS")
    degree = field(text, "_NORMAL_CLOSURE_DEGREE")
    group = field(text, "_NORMAL_CLOSURE_GROUP")
    bases = field(text, "_LINEAR_REINDUCTION_BASES")
    base_present = field(text, "_REAL_BASE_PRESENT")
    if pass_value is None:
        raise RuntimeError("missing geometry verdict")
    if pass_value == "1":
        status = "GEOMETRY_PASS"
    elif degree != "16":
        status = "NORMAL_CLOSURE_ORDER_NE_16"
    elif group != "[16, 13]":
        status = "NORMAL_CLOSURE_GROUP_NOT_16_13"
    elif base_present != "1":
        status = "REAL_BASE_IDENTIFICATION_FAIL"
    else:
        status = "LINEAR_REINDUCTION_BASE_COUNT_FAIL"
    return status, {
        "normal_closure_degree": degree,
        "normal_closure_group": group,
        "linear_reinduction_bases": bases,
    }


def checkpoint(records: list[dict], status: str) -> None:
    packet_counts = Counter(
        packet["status"]
        for row in records
        for packet in row["packets"]
    )
    case_counts = Counter(row["classification"] for row in records)
    payload = {
        "schema": "effective-stark-engine-c-catchup-252-v1",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "claim_tag": (
            "VERIFIED_COMPLETE_C_CATCHUP"
            if status == "COMPLETE"
            else "INCOMPLETE_NO_CENSUS_VERDICT"
        ),
        "predicate_provenance": "GENUINE",
        "status": status,
        "expected_case_count": 252,
        "completed_case_count": len(records),
        "packet_taxonomy": dict(sorted(packet_counts.items())),
        "case_taxonomy": dict(sorted(case_counts.items())),
        "records": records,
        "source_hashes": {
            str(W1.relative_to(ROOT)): sha(W1),
            str(QUEUE.relative_to(ROOT)): sha(QUEUE),
            str(SCREEN.relative_to(ROOT)): sha(SCREEN),
            str(QUARANTINE.relative_to(ROOT)): sha(QUARANTINE),
            "scripts/run_engine_c_catchup_252.py": sha(Path(__file__)),
        },
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--timeout", type=int, default=3600)
    args = parser.parse_args()
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))[
        "engine_c_catch_up_geometry"
    ]["case_ids"]
    if len(queue) != 252 or len(set(queue)) != 252:
        raise RuntimeError("C catch-up queue changed")
    by_id = {
        row["case_id"]: row
        for row in json.loads(W1.read_text(encoding="utf-8"))["records"]
    }
    quarantined = {
        (row["case_id"], row["packet_index"]): row
        for row in json.loads(
            QUARANTINE.read_text(encoding="utf-8")
        )["entries"]
    }
    records: list[dict] = []
    if args.resume:
        if OUTPUT.exists():
            prior = json.loads(OUTPUT.read_text(encoding="utf-8"))
            for path, expected in prior["source_hashes"].items():
                if path == "scripts/run_engine_c_catchup_252.py":
                    continue
                if sha(ROOT / path) != expected:
                    raise RuntimeError(f"resume hash mismatch: {path}")
            records = prior["records"]
    elif OUTPUT.exists() or TRANSCRIPTS.exists():
        raise RuntimeError("versioned output exists; pass --resume")
    completed_ids = {row["case_id"] for row in records}
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    screen = SCREEN.read_text(encoding="utf-8")
    processed = 0

    for case_id in queue:
        if case_id in completed_ids:
            continue
        if args.limit is not None and processed >= args.limit:
            break
        row = by_id[case_id]
        expected_packets = row["c_quartic_count"] // 2
        hnf = row["finite_ideal_hnf"]
        packets = []
        for packet_index in range(1, expected_packets + 1):
            known_block = quarantined.get((case_id, packet_index))
            transcript = (
                TRANSCRIPTS / f"{case_id}-p{packet_index}.txt"
            )
            if known_block is not None:
                transcript.write_text(
                    "TOOL_BLOCKED_PARI_2_15_4=1\n",
                    encoding="utf-8",
                )
                packets.append(
                    {
                        "packet_index": packet_index,
                        "status": "TOOL_BLOCKED",
                        "known_quarantine": known_block,
                        "transcript": str(
                            transcript.relative_to(ROOT)
                        ),
                        "transcript_sha256": sha(transcript),
                    }
                )
                continue
            prelude = (
                f'CASE_ID="{case_id}";D_VALUE={row["d"]};'
                f"H11={hnf[0][0]};H12={hnf[0][1]};"
                f"H21={hnf[1][0]};H22={hnf[1][1]};"
                f"PACKET_FILTER={packet_index};\n"
            )
            try:
                completed = subprocess.run(
                    ["gp", "-q"],
                    input=prelude + screen,
                    text=True,
                    capture_output=True,
                    cwd=ROOT,
                    timeout=args.timeout,
                    check=False,
                )
                text = completed.stdout + completed.stderr
                failure = (
                    None
                    if completed.returncode == 0
                    else f"GP_EXIT_{completed.returncode}"
                )
            except subprocess.TimeoutExpired as error:
                text = (error.stdout or "") + (error.stderr or "")
                if isinstance(text, bytes):
                    text = text.decode(errors="replace")
                failure = "ONE_NODE_HOUR_CAP"
            transcript.write_text(text, encoding="utf-8")
            if failure is None:
                try:
                    status, details = packet_status(text)
                except RuntimeError as error:
                    failure = f"PARSE_ERROR:{error}"
            if failure is not None:
                status = "TOOL_BLOCKED"
                details = {"failure": failure}
            packets.append(
                {
                    "packet_index": packet_index,
                    "status": status,
                    **details,
                    "transcript": str(transcript.relative_to(ROOT)),
                    "transcript_sha256": sha(transcript),
                }
            )
        statuses = [packet["status"] for packet in packets]
        if "TOOL_BLOCKED" in statuses:
            classification = "HAS_TOOL_BLOCK"
        elif all(status == "GEOMETRY_PASS" for status in statuses):
            classification = "C_ELIGIBLE"
        elif any(status == "GEOMETRY_PASS" for status in statuses):
            classification = "MIXED_PASS_FAIL"
        else:
            classification = "NO_PACKET_PASSES"
        records.append(
            {
                "case_id": case_id,
                "d": row["d"],
                "finite_norm": row["finite_norm"],
                "finite_ideal_hnf": hnf,
                "packet_count": expected_packets,
                "classification": classification,
                "packets": packets,
            }
        )
        processed += 1
        checkpoint(records, "RUNNING")
        print(
            f"C_CATCHUP={len(records)}/252 CASE={case_id} "
            f"CLASS={classification}",
            flush=True,
        )
    checkpoint(records, "COMPLETE" if len(records) == 252 else "PAUSED")


if __name__ == "__main__":
    main()
