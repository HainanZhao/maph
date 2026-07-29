#!/usr/bin/env python3
"""Run the preregistered bounded W1 structural pilot."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts" / "frozen-ideal-census-v1.json"
GP_SOURCE = ROOT / "scripts" / "screen_w1_case.gp"


def gp_literal(value: str) -> object:
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [int(item.strip()) for item in inner.split(",")]
    if value.lstrip("-").isdigit():
        return int(value)
    return value


def run_case(case: dict[str, object]) -> dict[str, object]:
    hnf = case["finite_ideal_hnf"]
    prefix = (
        f'CASE_ID="{case["case_id"]}";D_VALUE={case["D"]};'
        f"H11={hnf[0][0]};H12={hnf[0][1]};"
        f"H21={hnf[1][0]};H22={hnf[1][1]};\n"
    )
    completed = subprocess.run(
        ["gp", "-q"],
        cwd=ROOT,
        input=prefix + GP_SOURCE.read_text() + "\n",
        text=True,
        capture_output=True,
        check=False,
        timeout=3600,
    )
    fatal_stderr = "\n".join(
        line for line in completed.stderr.splitlines() if "Warning:" not in line
    )
    if completed.returncode or "***" in fatal_stderr:
        raise RuntimeError(
            f'{case["case_id"]} failed:\n{completed.stdout}\n{completed.stderr}'
        )
    result: dict[str, object] = {}
    for line in completed.stdout.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            result[key.lower()] = gp_literal(value)
    required = {
        "case_id",
        "bnfcertify",
        "support_count",
        "verdict",
        "engine",
        "obstruction",
    }
    if not required <= result.keys():
        raise RuntimeError(f"missing output in {case['case_id']}: {result}")
    result["finite_ideal_hnf"] = hnf
    result["source_case_sha256"] = hashlib.sha256(
        json.dumps(case, sort_keys=True).encode()
    ).hexdigest()
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--d-max", type=int, default=13)
    parser.add_argument("--norm-max", type=int, default=12)
    parser.add_argument(
        "--full-census",
        action="store_true",
        help="require the exact frozen D<=200, norm<=100 range",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "artifacts" / "w1-pilot-v1.json",
    )
    args = parser.parse_args()
    if args.full_census and (args.d_max != 200 or args.norm_max != 100):
        raise SystemExit(
            "--full-census requires --d-max 200 --norm-max 100"
        )
    source = json.loads(SOURCE.read_text())
    cases = [
        case
        for case in source["cases"]
        if case["D"] <= args.d_max and case["finite_norm"] <= args.norm_max
    ]
    records = []
    for index, case in enumerate(cases, start=1):
        record = run_case(case)
        records.append(record)
        print(
            f'CASE={index}/{len(cases)} ID={record["case_id"]} '
            f'VERDICT={record["verdict"]} ENGINE={record["engine"]} '
            f'OBSTRUCTION={record["obstruction"]}',
            flush=True,
        )
    verdict_counts = Counter(str(row["verdict"]) for row in records)
    engine_counts = Counter(
        str(row["engine"]) for row in records if row["engine"] != "NONE"
    )
    obstruction_counts = Counter(
        str(row["obstruction"])
        for row in records
        if row["obstruction"] != "NONE"
    )
    payload = {
        "schema": (
            "effective-stark-w1-structural-census-v1"
            if args.full_census
            else "effective-stark-w1-pilot-v1"
        ),
        "claim_tag": "VERIFIED_STRUCTURAL_SCREEN",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": {
            "D_max": args.d_max,
            "norm_max": args.norm_max,
            "case_count": len(cases),
            "purpose": (
                "complete frozen maximal-order structural census"
                if args.full_census
                else "bounded structural-screen validation, not the Phase-1 yield gate"
            ),
        },
        "source_census_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "screen_source_sha256": hashlib.sha256(GP_SOURCE.read_bytes()).hexdigest(),
        "verdict_counts": dict(sorted(verdict_counts.items())),
        "engine_counts": dict(sorted(engine_counts.items())),
        "obstruction_counts": dict(sorted(obstruction_counts.items())),
        "records": records,
    }
    serialized = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(serialized)
    print(f"CASE_COUNT={len(records)}")
    print(f"ENGINE_COUNTS={dict(engine_counts)}")
    print(f"OBSTRUCTION_COUNTS={dict(obstruction_counts)}")
    print(f"OUTPUT_SHA256={hashlib.sha256(serialized.encode()).hexdigest()}")
    print(f"OUTPUT={args.output}")


if __name__ == "__main__":
    main()
