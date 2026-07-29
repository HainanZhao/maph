#!/usr/bin/env python3
"""Recompute the ten frozen W1 spot checks one case at a time."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from run_w1_pilot import run_case


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    freeze = json.loads((ROOT / "data" / "w1-spotchecks-v1.json").read_text())
    census = json.loads(
        (ROOT / "artifacts" / "frozen-ideal-census-v1.json").read_text()
    )
    by_id = {row["case_id"]: row for row in census["cases"]}
    records = []
    for selection in freeze["cases"]:
        case = by_id[selection["case_id"]]
        fresh = run_case(case)
        checks = {
            "verdict": fresh["verdict"] == selection["expected_verdict"],
            "engine": fresh["engine"] == selection["expected_engine"],
            "bnfcertify": fresh["bnfcertify"] == 1,
        }
        if selection["expected_verdict"] == "FRONTIER":
            checks["obstruction"] = (
                fresh["obstruction"] == selection["expected_obstruction"]
            )
        passed = all(checks.values())
        records.append(
            {
                "case_id": selection["case_id"],
                "passed": passed,
                "checks": checks,
                "fresh_record": fresh,
            }
        )
        print(f'SPOTCHECK={selection["case_id"]} PASSED={int(passed)}')
    passed_count = sum(row["passed"] for row in records)
    payload = {
        "schema": "effective-stark-w1-spotcheck-results-v1",
        "claim_tag": "VERIFIED",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "passed_count": passed_count,
        "case_count": len(records),
        "records": records,
    }
    serialized = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    output = ROOT / "artifacts" / "w1-spotchecks-v1.json"
    output.write_text(serialized)
    print(f"PASSED_COUNT={passed_count}")
    print(f"OUTPUT_SHA256={hashlib.sha256(serialized.encode()).hexdigest()}")
    if passed_count != len(records):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
