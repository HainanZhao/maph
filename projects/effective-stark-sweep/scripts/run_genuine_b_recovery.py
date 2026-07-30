#!/usr/bin/env python3
"""Genuinely reconstruct and reclassify all 241 proxy-exposed B rows."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
SCREEN = ROOT / "scripts/screen_engine_b_genuine.gp"
INDEX_SCREEN = ROOT / "scripts/screen_genuine_normal_index.gp"
W1 = ARTIFACTS / "w1-full-census-v1.json"
QUEUE = ARTIFACTS / "proxy-recovery-queue-v1.json"
ANCHORS = ARTIFACTS / "genuine-b-battery-anchor-v3.json"
FULL_ANCHORS = ARTIFACTS / "r13-genuine-anchor-reproduction-v1.json"
OUTPUT = ARTIFACTS / "genuine-b-recovery-241-v1.json"
TRANSCRIPTS = ARTIFACTS / "genuine-b-recovery-241-v1"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_value(text: str, key: str) -> str:
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
    counts: dict[str, int] = {}
    for row in records:
        key = row["classification"]
        counts[key] = counts.get(key, 0) + 1
    payload = {
        "schema": "effective-stark-genuine-b-recovery-241-v1",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "claim_tag": (
            "VERIFIED_GENUINE_B_RECLASSIFICATION"
            if status == "COMPLETE"
            else "INCOMPLETE_NO_CENSUS_VERDICT"
        ),
        "predicate_provenance": "GENUINE",
        "status": status,
        "expected_case_count": 241,
        "completed_case_count": len(records),
        "classification_counts": dict(sorted(counts.items())),
        "records": records,
        "census_effect": (
            "UNFROZEN_UNTIL_COMPLETE"
            if status != "COMPLETE"
            else "READY_FOR_CENSUS_V5_AFTER_C_AND_INDEX_RECOVERY"
        ),
        "source_hashes": {
            str(W1.relative_to(ROOT)): sha(W1),
            str(QUEUE.relative_to(ROOT)): sha(QUEUE),
            str(SCREEN.relative_to(ROOT)): sha(SCREEN),
            str(INDEX_SCREEN.relative_to(ROOT)): sha(INDEX_SCREEN),
            str(ANCHORS.relative_to(ROOT)): sha(ANCHORS),
            str(FULL_ANCHORS.relative_to(ROOT)): sha(FULL_ANCHORS),
            "scripts/run_genuine_b_recovery.py": sha(Path(__file__)),
        },
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--timeout", type=int, default=3600)
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()

    anchors = json.loads(ANCHORS.read_text(encoding="utf-8"))
    full = json.loads(FULL_ANCHORS.read_text(encoding="utf-8"))
    if anchors["verdict"] != "GENUINE_B_ANCHORS_3_OF_3_PASSED":
        raise RuntimeError("genuine B anchor gate is not closed")
    if full["verdict"] != "ANCHOR_GATE_PASSED":
        raise RuntimeError("full 7/7 anchor gate is not closed")

    queue = json.loads(QUEUE.read_text(encoding="utf-8"))[
        "engine_b_actual_normal_closure"
    ]["case_ids"]
    if len(queue) != 241 or len(set(queue)) != 241:
        raise RuntimeError("B recovery queue is not the frozen 241")
    by_id = {
        row["case_id"]: row
        for row in json.loads(W1.read_text(encoding="utf-8"))["records"]
    }
    records: list[dict] = []
    if args.resume:
        if OUTPUT.exists():
            prior = json.loads(OUTPUT.read_text(encoding="utf-8"))
            for path, expected in prior["source_hashes"].items():
                if path == "scripts/run_genuine_b_recovery.py":
                    continue
                if sha(ROOT / path) != expected:
                    raise RuntimeError(
                        f"resume source hash mismatch: {path}"
                    )
            records = prior["records"]
    elif OUTPUT.exists() or TRANSCRIPTS.exists():
        raise RuntimeError("versioned output exists; pass --resume")
    completed_ids = {row["case_id"] for row in records}
    screen = SCREEN.read_text(encoding="utf-8")
    index_screen = INDEX_SCREEN.read_text(encoding="utf-8")
    queue_data = json.loads(QUEUE.read_text(encoding="utf-8"))[
        "engine_b_actual_normal_closure"
    ]
    former_passes = set(
        queue_data["former_proxy_pass_pending_case_ids"]
    )
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    processed_this_run = 0

    for case_id in queue:
        if case_id in completed_ids:
            continue
        if args.limit is not None and processed_this_run >= args.limit:
            break
        row = by_id[case_id]
        hnf = row["finite_ideal_hnf"]
        prelude = (
            f'CASE_ID="{case_id}";D_VALUE={row["d"]};'
            f"H11={hnf[0][0]};H12={hnf[0][1]};"
            f"H21={hnf[1][0]};H22={hnf[1][1]};\n"
        )
        try:
            completed = subprocess.run(
                ["gp", "-q"],
                input=prelude + index_screen,
                text=True,
                capture_output=True,
                cwd=ROOT,
                timeout=args.timeout,
                check=False,
            )
            index_text = completed.stdout + completed.stderr
            index_returncode = completed.returncode
            failure = (
                None
                if index_returncode == 0
                else f"INDEX_GP_EXIT_{index_returncode}"
            )
        except subprocess.TimeoutExpired as error:
            index_text = (error.stdout or "") + (error.stderr or "")
            if isinstance(index_text, bytes):
                index_text = index_text.decode(errors="replace")
            index_returncode = None
            failure = "INDEX_ONE_NODE_HOUR_CAP"
        index_transcript = TRANSCRIPTS / f"{case_id}.index.txt"
        index_transcript.write_text(index_text, encoding="utf-8")

        data: dict[str, object] = {}
        if failure is None:
            try:
                data = {
                    "normal_closure_relative_degree": int(
                        parse_value(
                            index_text,
                            "NORMAL_CLOSURE_RELATIVE_DEGREE",
                        )
                    ),
                    "derived_subgroup_order": int(
                        parse_value(
                            index_text, "DERIVED_SUBGROUP_ORDER"
                        )
                    ),
                    "maximal_abelian_relative_degree": int(
                        parse_value(
                            index_text,
                            "MAXIMAL_ABELIAN_RELATIVE_DEGREE",
                        )
                    ),
                    "index_complete": int(
                        parse_value(
                            index_text,
                            "GENUINE_NORMAL_INDEX_SCREEN_COMPLETE",
                        )
                    ),
                }
            except (RuntimeError, ValueError) as error:
                failure = f"INDEX_PARSE_ERROR:{error}"

        if failure is not None:
            classification = "FRONTIER_GENUINE_RECONSTRUCTION_FAILED"
        elif data["index_complete"] != 1:
            classification = "FRONTIER_INCOMPLETE"
        elif data["derived_subgroup_order"] == 1:
            classification = "HALT_ANOMALOUS_INDEX_ONE"
        elif data["derived_subgroup_order"] != 2:
            classification = (
                f"FRONTIER_INDEX_{data['derived_subgroup_order']}"
            )
        else:
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
                w2_text = completed.stdout + completed.stderr
                w2_returncode = completed.returncode
                w2_failure = (
                    None
                    if w2_returncode == 0
                    else f"W2_GP_EXIT_{w2_returncode}"
                )
            except subprocess.TimeoutExpired as error:
                w2_text = (error.stdout or "") + (error.stderr or "")
                if isinstance(w2_text, bytes):
                    w2_text = w2_text.decode(errors="replace")
                w2_returncode = None
                w2_failure = "W2_ONE_NODE_HOUR_CAP"
            w2_transcript = TRANSCRIPTS / f"{case_id}.w2.txt"
            w2_transcript.write_text(w2_text, encoding="utf-8")
            if w2_failure is None:
                try:
                    data.update(
                        {
                            "normal_closure_degree": int(
                                parse_value(
                                    w2_text,
                                    "ACTUAL_NORMAL_CLOSURE_DEGREE",
                                )
                            ),
                            "abelian_imaginary_base_count": int(
                                parse_value(
                                    w2_text,
                                    "ABELIAN_IMAGINARY_BASE_COUNT",
                                )
                            ),
                            "two_route_match_count": int(
                                parse_value(
                                    w2_text, "TWO_ROUTE_MATCH_COUNT"
                                )
                            ),
                            "w2_complete": int(
                                parse_value(
                                    w2_text,
                                    "ENGINE_B_GENUINE_SCREEN_COMPLETE",
                                )
                            ),
                        }
                    )
                except (RuntimeError, ValueError) as error:
                    w2_failure = f"W2_PARSE_ERROR:{error}"
            if w2_failure is not None:
                failure = w2_failure
                classification = (
                    "FRONTIER_GENUINE_RECONSTRUCTION_FAILED"
                )
            elif data["abelian_imaginary_base_count"] == 0:
                classification = (
                    "FRONTIER_NO_ABELIAN_IMAGINARY_BASE"
                )
            elif (
                data["two_route_match_count"]
                != data["abelian_imaginary_base_count"]
            ):
                classification = "HALT_TWO_ROUTE_MISMATCH"
            else:
                classification = "ENGINE_B_GENUINE_PASS"

        records.append(
            {
                "case_id": case_id,
                "d": row["d"],
                "finite_ideal_hnf": hnf,
                "finite_norm": row["finite_norm"],
                "former_proxy_classification": (
                    "TWO_ROUTE_PASS"
                    if case_id in former_passes
                    else "NO_ABELIAN_IMAGINARY_BASE"
                ),
                "predicate_provenance": "GENUINE",
                "classification": classification,
                "data": data,
                "failure": failure,
                "index_returncode": index_returncode,
                "index_transcript": str(
                    index_transcript.relative_to(ROOT)
                ),
                "index_transcript_sha256": sha(index_transcript),
                "w2_transcript": (
                    str(w2_transcript.relative_to(ROOT))
                    if data.get("derived_subgroup_order") == 2
                    else None
                ),
                "w2_transcript_sha256": (
                    sha(w2_transcript)
                    if data.get("derived_subgroup_order") == 2
                    else None
                ),
            }
        )
        processed_this_run += 1
        checkpoint(records, "RUNNING")
        print(
            f"GENUINE_B={len(records)}/241 CASE={case_id} "
            f"CLASS={classification}",
            flush=True,
        )
        if classification.startswith("HALT_"):
            checkpoint(records, "HALTED")
            raise SystemExit(2)

    status = "COMPLETE" if len(records) == 241 else "PAUSED"
    checkpoint(records, status)
    print(f"GENUINE_B_RECOVERY_STATUS={status}", flush=True)


if __name__ == "__main__":
    main()
