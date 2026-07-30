#!/usr/bin/env python3
"""Close the 11 index-two rows exposed only by genuine v5 integration."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
W1 = ARTIFACTS / "w1-full-census-v1.json"
INDEX = ARTIFACTS / "genuine-index-ledger-8200-v3.json"
SCREEN = ROOT / "scripts/screen_engine_b_genuine.gp"
OUTPUT = ARTIFACTS / "genuine-b-index2-catchup-11-v1.json"
TRANSCRIPTS = ARTIFACTS / "genuine-b-index2-catchup-11-v1"
CASE_IDS = [
    "RQ-000393",
    "RQ-000581",
    "RQ-000958",
    "RQ-001073",
    "RQ-002165",
    "RQ-002726",
    "RQ-005402",
    "RQ-005404",
    "RQ-006312",
    "RQ-007732",
    "RQ-007836",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def value(text: str, key: str) -> int:
    prefix = f"{key}="
    hits = [
        line[len(prefix):].strip()
        for line in text.splitlines()
        if line.startswith(prefix)
    ]
    if len(hits) != 1:
        raise RuntimeError(f"{key}: expected one value")
    return int(hits[0])


def main() -> None:
    if OUTPUT.exists() or TRANSCRIPTS.exists():
        raise RuntimeError("versioned catch-up output exists")
    rows = {
        row["case_id"]: row
        for row in json.loads(W1.read_text(encoding="utf-8"))["records"]
    }
    indices = {
        row["case_id"]: row
        for row in json.loads(INDEX.read_text(encoding="utf-8"))["records"]
    }
    screen = SCREEN.read_text(encoding="utf-8")
    TRANSCRIPTS.mkdir(parents=True)
    records = []
    for case_id in CASE_IDS:
        row = rows[case_id]
        index = indices[case_id]
        if index["derived_subgroup_order"] != 2:
            raise RuntimeError(f"{case_id}: not genuine index two")
        if 2 * index["normal_closure_relative_degree"] > 40:
            raise RuntimeError(f"{case_id}: exceeds degree cap")
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
        base_count = value(text, "ABELIAN_IMAGINARY_BASE_COUNT")
        match_count = value(text, "TWO_ROUTE_MATCH_COUNT")
        complete = value(text, "ENGINE_B_GENUINE_SCREEN_COMPLETE")
        if match_count != base_count:
            raise RuntimeError(f"{case_id}: two-route mismatch")
        classification = (
            "ENGINE_B_GENUINE_PASS"
            if base_count > 0 and complete == 1
            else "FRONTIER_NO_ABELIAN_IMAGINARY_BASE"
        )
        records.append(
            {
                "case_id": case_id,
                "predicate_provenance": "GENUINE",
                "normal_closure_absolute_degree":
                    2 * index["normal_closure_relative_degree"],
                "abelian_imaginary_base_count": base_count,
                "two_route_match_count": match_count,
                "classification": classification,
                "transcript": str(transcript.relative_to(ROOT)),
                "transcript_sha256": sha(transcript),
            }
        )
    counts = {
        key: sum(row["classification"] == key for row in records)
        for key in sorted({row["classification"] for row in records})
    }
    payload = {
        "schema": "effective-stark-genuine-b-index2-catchup-11-v1",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "claim_tag": "VERIFIED_GENUINE_B_CATCHUP",
        "predicate_provenance": "GENUINE",
        "case_count": len(records),
        "classification_counts": counts,
        "records": records,
        "source_hashes": {
            str(W1.relative_to(ROOT)): sha(W1),
            str(INDEX.relative_to(ROOT)): sha(INDEX),
            str(SCREEN.relative_to(ROOT)): sha(SCREEN),
            "scripts/run_genuine_b_index2_catchup.py":
                sha(Path(__file__)),
        },
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
