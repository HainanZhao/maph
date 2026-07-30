#!/usr/bin/env python3
"""Rebuild the full 8,200-row normal-closure index ledger genuinely."""

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
SCREEN = ROOT / "scripts/screen_genuine_normal_index.gp"
ANCHORS = ARTIFACTS / "genuine-b-battery-anchor-v3.json"
OUTPUT = ARTIFACTS / "genuine-index-ledger-8200-v3.json"
TRANSCRIPTS = ARTIFACTS / "genuine-index-ledger-8200-v3"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def value(text: str, key: str) -> str:
    prefix = f"{key}="
    hits = [
        line[len(prefix):].strip()
        for line in text.splitlines()
        if line.startswith(prefix)
    ]
    if len(hits) != 1:
        raise RuntimeError(f"{key}: expected one value, got {len(hits)}")
    return hits[0]


def checkpoint(records: list[dict], status: str) -> None:
    indices = Counter(row["derived_subgroup_order"] for row in records)
    payload = {
        "schema": "effective-stark-genuine-index-ledger-8200-v3",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "claim_tag": (
            "VERIFIED_GENUINE_INDEX_LEDGER"
            if status == "COMPLETE"
            else "INCOMPLETE_NO_W4_VERDICT"
        ),
        "predicate_provenance": "GENUINE",
        "status": status,
        "expected_representative_count": 8200,
        "completed_representative_count": len(records),
        "index_histogram": {
            str(key): count for key, count in sorted(indices.items())
        },
        "records": records,
        "source_hashes": {
            str(W1.relative_to(ROOT)): sha(W1),
            str(SCREEN.relative_to(ROOT)): sha(SCREEN),
            str(ANCHORS.relative_to(ROOT)): sha(ANCHORS),
            "scripts/run_genuine_index_8200.py": sha(Path(__file__)),
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
    anchors = json.loads(ANCHORS.read_text(encoding="utf-8"))
    if anchors["verdict"] != "GENUINE_B_ANCHORS_3_OF_3_PASSED":
        raise RuntimeError("genuine common-modulus anchor gate is open")
    rows = json.loads(W1.read_text(encoding="utf-8"))["records"]
    if len(rows) != 8200:
        raise RuntimeError("frozen census size changed")
    records: list[dict] = []
    if args.resume:
        if OUTPUT.exists():
            prior = json.loads(OUTPUT.read_text(encoding="utf-8"))
            for path, expected in prior["source_hashes"].items():
                if path == "scripts/run_genuine_index_8200.py":
                    continue
                if sha(ROOT / path) != expected:
                    raise RuntimeError(f"resume hash mismatch: {path}")
            records = prior["records"]
    elif OUTPUT.exists() or TRANSCRIPTS.exists():
        raise RuntimeError("versioned output exists; pass --resume")
    completed_ids = {row["case_id"] for row in records}
    screen = SCREEN.read_text(encoding="utf-8")
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    processed = 0

    for row in rows:
        case_id = row["case_id"]
        if case_id in completed_ids:
            continue
        if args.limit is not None and processed >= args.limit:
            break
        hnf = row["finite_ideal_hnf"]
        prelude = (
            f'CASE_ID="{case_id}";D_VALUE={row["d"]};'
            f"H11={hnf[0][0]};H12={hnf[0][1]};"
            f"H21={hnf[1][0]};H22={hnf[1][1]};\n"
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
        transcript = TRANSCRIPTS / f"{case_id}.txt"
        transcript.write_text(text, encoding="utf-8")
        if failure is not None:
            checkpoint(records, "HALTED")
            raise RuntimeError(f"{case_id}: {failure}")
        try:
            complete = int(
                value(text, "GENUINE_NORMAL_INDEX_SCREEN_COMPLETE")
            )
            normal_degree = int(
                value(text, "NORMAL_CLOSURE_RELATIVE_DEGREE")
            )
            abelian_degree = int(
                value(text, "MAXIMAL_ABELIAN_RELATIVE_DEGREE")
            )
            index = int(value(text, "DERIVED_SUBGROUP_ORDER"))
            common_ideal = value(text, "COMMON_STABLE_FINITE_IDEAL")
        except (RuntimeError, ValueError) as error:
            checkpoint(records, "HALTED")
            raise RuntimeError(f"{case_id}: {error}") from error
        if complete != 1:
            checkpoint(records, "HALTED")
            raise RuntimeError(f"{case_id}: incomplete index screen")
        if normal_degree != abelian_degree * index:
            checkpoint(records, "HALTED")
            raise RuntimeError(f"{case_id}: index quotient mismatch")
        if (
            index > 2
            and index % 2 == 1
            and row["support_count"] > 0
        ):
            checkpoint(records, "HALTED_ODD_INDEX")
            raise RuntimeError(
                f"{case_id}: anomalous odd genuine index {index}"
            )
        records.append(
            {
                "case_id": case_id,
                "d": row["d"],
                "finite_norm": row["finite_norm"],
                "finite_ideal_hnf": hnf,
                "common_stable_finite_ideal": common_ideal,
                "normal_closure_relative_degree": normal_degree,
                "maximal_abelian_relative_degree": abelian_degree,
                "derived_subgroup_order": index,
                "odd_index_non_substantive": (
                    index > 2
                    and index % 2 == 1
                    and row["support_count"] == 0
                ),
                "predicate_provenance": "GENUINE",
                "transcript": str(transcript.relative_to(ROOT)),
                "transcript_sha256": sha(transcript),
            }
        )
        processed += 1
        if len(records) % 25 == 0:
            checkpoint(records, "RUNNING")
            print(f"GENUINE_INDEX={len(records)}/8200", flush=True)
    checkpoint(records, "COMPLETE" if len(records) == 8200 else "PAUSED")


if __name__ == "__main__":
    main()
