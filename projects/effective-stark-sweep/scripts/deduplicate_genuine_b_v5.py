#!/usr/bin/env python3
"""Compute exact distinct normal-closure count for all 232 v5 B rows."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
W1 = ARTIFACTS / "w1-full-census-v1.json"
OLD = ARTIFACTS / "engine-b-two-route-analysis-v1.json"
RECOVERY = ARTIFACTS / "genuine-b-recovery-241-v1.json"
CATCHUP = ARTIFACTS / "genuine-b-index2-catchup-11-v1.json"
QUEUE = ARTIFACTS / "proxy-recovery-queue-v1.json"
ANCHOR = ARTIFACTS / "genuine-b-battery-anchor-v4.json"
SCREEN = ROOT / "scripts/screen_engine_b_genuine.gp"
OUTPUT = ARTIFACTS / "genuine-b-deduplication-v5.json"
TRANSCRIPTS = ARTIFACTS / "genuine-b-deduplication-v5"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_value(text: str, key: str) -> str:
    prefix = f"{key}="
    hits = [
        line[len(prefix):].strip()
        for line in text.splitlines()
        if line.startswith(prefix)
    ]
    if len(hits) != 1:
        raise RuntimeError(f"{key}: expected one value")
    return hits[0]


def main() -> None:
    if OUTPUT.exists() or TRANSCRIPTS.exists():
        raise RuntimeError("versioned B deduplication output exists")
    anchor = json.loads(ANCHOR.read_text(encoding="utf-8"))
    if anchor["verdict"] != "GENUINE_B_ANCHORS_3_OF_3_PASSED":
        raise RuntimeError("current genuine B anchor is open")
    rows = {
        row["case_id"]: row
        for row in json.loads(W1.read_text(encoding="utf-8"))["records"]
    }
    recovery_queue = set(
        json.loads(QUEUE.read_text(encoding="utf-8"))[
            "engine_b_actual_normal_closure"
        ]["case_ids"]
    )
    old_records = json.loads(OLD.read_text(encoding="utf-8"))["records"]
    stable = [
        row for row in old_records
        if row["classification"] == "TWO_ROUTE_PASS"
        and row["case_id"] not in recovery_queue
    ]
    rerun_ids = [
        row["case_id"]
        for row in json.loads(
            RECOVERY.read_text(encoding="utf-8")
        )["records"]
        if row["classification"] == "ENGINE_B_GENUINE_PASS"
    ] + [
        row["case_id"]
        for row in json.loads(
            CATCHUP.read_text(encoding="utf-8")
        )["records"]
        if row["classification"] == "ENGINE_B_GENUINE_PASS"
    ]
    if len(stable) != 131 or len(rerun_ids) != 101:
        raise RuntimeError("v5 B partition changed")
    records = [
        {
            "case_id": row["case_id"],
            "predicate_provenance": "GENUINE",
            "normal_closure_polynomial":
                row["normal_closure_absolute_field"],
            "source": "stable-modulus historical genuine reconstruction",
        }
        for row in stable
    ]
    screen = SCREEN.read_text(encoding="utf-8")
    TRANSCRIPTS.mkdir(parents=True)
    for index, case_id in enumerate(rerun_ids, start=1):
        row = rows[case_id]
        hnf = row["finite_ideal_hnf"]
        prelude = (
            f'CASE_ID="{case_id}";D_VALUE={row["d"]};'
            f"H11={hnf[0][0]};H12={hnf[0][1]};"
            f"H21={hnf[1][0]};H22={hnf[1][1]};\n"
        )
        completed = subprocess.run(
            ["gp", "-q"],
            input=prelude + screen,
            text=True,
            capture_output=True,
            cwd=ROOT,
            timeout=3600,
            check=False,
        )
        text = completed.stdout + completed.stderr
        transcript = TRANSCRIPTS / f"{case_id}.txt"
        transcript.write_text(text, encoding="utf-8")
        if completed.returncode:
            raise RuntimeError(f"{case_id}: GP exit {completed.returncode}")
        if int(text_value(text, "TWO_ROUTE_MATCH_COUNT")) == 0:
            raise RuntimeError(f"{case_id}: no genuine ray match")
        records.append(
            {
                "case_id": case_id,
                "predicate_provenance": "GENUINE",
                "normal_closure_polynomial": text_value(
                    text, "ACTUAL_NORMAL_CLOSURE_POLYNOMIAL"
                ),
                "source": "v5 common-stable-modulus reconstruction",
                "transcript": str(transcript.relative_to(ROOT)),
                "transcript_sha256": sha(transcript),
            }
        )
        if index % 20 == 0:
            print(f"B_DEDUP_RERUN={index}/101", flush=True)
    polynomials = {
        row["normal_closure_polynomial"] for row in records
    }
    payload = {
        "schema": "effective-stark-genuine-b-deduplication-v5",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "claim_tag": "VERIFIED_GENUINE_B_DEDUPLICATION",
        "predicate_provenance": "GENUINE",
        "occurrence_count": len(records),
        "distinct_normal_closure_count": len(polynomials),
        "records": records,
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (
                W1,
                OLD,
                RECOVERY,
                CATCHUP,
                QUEUE,
                ANCHOR,
                SCREEN,
                Path(__file__),
            )
        },
    }
    if len(records) != 232:
        raise RuntimeError("v5 B occurrence total changed")
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
