#!/usr/bin/env python3
"""Run the genuine normal-closure Engine-B battery on the three B anchors."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "scripts/screen_engine_b_genuine.gp"
OUTPUT = ROOT / "artifacts/genuine-b-battery-anchor-v1.json"
TRANSCRIPT = ROOT / "artifacts/genuine-b-battery-anchor-v1.transcript"
CASES = [
    ("B-d5-ray5", 3, [[5, 0], [0, 5]]),
    ("B-d7-disc8", 2, [[14, 0], [0, 14]]),
    ("B-d7-disc32", 2, [[14, 0], [0, 14]]),
]


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--transcript", type=Path, default=TRANSCRIPT)
    args = parser.parse_args()
    output = args.output.resolve()
    transcript = args.transcript.resolve()
    if output.exists() or transcript.exists():
        raise RuntimeError("versioned genuine-anchor output already exists")
    screen = SCREEN.read_text(encoding="utf-8")
    records = []
    transcript_parts = []
    for case_id, d, hnf in CASES:
        prelude = (
            f'CASE_ID="{case_id}";D_VALUE={d};'
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
        transcript_parts.append(
            f"===== {case_id} =====\n{text}\n"
        )
        try:
            provenance = value(text, "PREDICATE_PROVENANCE")
            derived_order = int(value(text, "DERIVED_SUBGROUP_ORDER"))
            base_count = int(value(text, "ABELIAN_IMAGINARY_BASE_COUNT"))
            match_count = int(value(text, "TWO_ROUTE_MATCH_COUNT"))
            complete = int(
                value(text, "ENGINE_B_GENUINE_SCREEN_COMPLETE")
            )
        except (RuntimeError, ValueError):
            provenance = "MISSING"
            derived_order = 0
            base_count = 0
            match_count = 0
            complete = 0
        passed = (
            completed.returncode == 0
            and provenance == "GENUINE"
            and derived_order == 2
            and base_count > 0
            and match_count == base_count
            and complete == 1
        )
        records.append(
            {
                "anchor_id": case_id,
                "d": d,
                "finite_ideal_hnf": hnf,
                "predicate_provenance": provenance,
                "derived_subgroup_order": derived_order,
                "abelian_imaginary_base_count": base_count,
                "two_route_match_count": match_count,
                "passed": passed,
                "returncode": completed.returncode,
                "output_sha256": hashlib.sha256(
                    text.encode()
                ).hexdigest(),
            }
        )
        if not passed:
            break
    transcript.write_text("".join(transcript_parts), encoding="utf-8")
    all_passed = len(records) == len(CASES) and all(
        row["passed"] for row in records
    )
    payload = {
        "schema": "effective-stark-genuine-b-battery-anchor-v1",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "claim_tag": (
            "VERIFIED_GENUINE_B_ANCHOR_GATE"
            if all_passed
            else "FAILED_GATE"
        ),
        "predicate_provenance": "GENUINE",
        "expected_anchor_count": len(CASES),
        "passed_anchor_count": sum(row["passed"] for row in records),
        "records": records,
        "verdict": (
            "GENUINE_B_ANCHORS_3_OF_3_PASSED"
            if all_passed
            else "GENUINE_B_ANCHOR_MISMATCH"
        ),
        "source_hashes": {
            str(SCREEN.relative_to(ROOT)): sha(SCREEN),
            str(transcript.relative_to(ROOT)): sha(transcript),
            "scripts/run_genuine_b_anchor_battery.py": sha(Path(__file__)),
        },
    }
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if not all_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
