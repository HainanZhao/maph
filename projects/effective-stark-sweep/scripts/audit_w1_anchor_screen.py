#!/usr/bin/env python3
"""Regression-check the W1 structural screen on the seven anchors."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from run_w1_pilot import run_case


ROOT = Path(__file__).resolve().parents[1]


ANCHORS = [
    {
        "id": "A-d4-ray4",
        "D": 5,
        "modulus": 4,
        "expect": {"one_cyc": [2], "support_max": 2, "route_predicate": "A"},
    },
    {
        "id": "B-d5-ray5",
        "D": 3,
        "modulus": 5,
        "expect": {"one_cyc": [8], "support_max": 8, "route_predicate": "B"},
    },
    {
        "id": "B-d7-disc8",
        "D": 2,
        "modulus": 14,
        "expect": {
            "one_cyc": [6, 2],
            "support_max": 6,
            "route_predicate": "B",
        },
    },
    {
        "id": "B-d7-disc32",
        "D": 2,
        "modulus": 14,
        "expect": {
            "one_cyc": [6, 2],
            "support_max": 6,
            "route_predicate": "B",
        },
    },
    {
        "id": "B-d8-ray12-lower",
        "D": 5,
        "modulus": 12,
        "expect": {
            "one_cyc": [2, 2],
            "support_max": 2,
            "route_predicate": "B",
        },
    },
    {
        "id": "C-d8-ray24-primitive",
        "D": 5,
        "modulus": 24,
        "expect": {
            "one_cyc": [4, 2, 2],
            "support_max": 4,
            "route_predicate": "C",
        },
    },
    {
        "id": "A-d8-ray8",
        "D": 5,
        "modulus": 8,
        "expect": {
            "one_cyc": [2, 2],
            "support_max": 2,
            "route_predicate": "A",
        },
    },
]


def check_route(record: dict[str, object], expected: str) -> bool:
    if expected == "A":
        return int(record["max_support_order"]) <= 2
    if expected == "B":
        return (
            int(record["shintani_index"]) == 2
            and int(record["exactly_one_real_place_splitting"]) == 1
            and int(record["b03_positive_not_minus_one"]) == 1
            and int(record["b06_negative_norm_not_one"]) == 1
        )
    if expected == "C":
        return (
            int(record["c_structural"]) == 1
            and int(record["c_projective_failures"]) == 0
        )
    raise ValueError(expected)


def main() -> None:
    records = []
    failed = []
    for anchor in ANCHORS:
        modulus = int(anchor["modulus"])
        record = run_case(
            {
                "case_id": anchor["id"],
                "D": anchor["D"],
                "finite_ideal_hnf": [[modulus, 0], [0, modulus]],
            }
        )
        expect = anchor["expect"]
        checks = {
            "bnfcertify": record["bnfcertify"] == 1,
            "one_cyc": record["one_cyc"] == expect["one_cyc"],
            "support_max": record["max_support_order"] == expect["support_max"],
            "historical_route_predicate": check_route(
                record, str(expect["route_predicate"])
            ),
        }
        passed = all(checks.values())
        if not passed:
            failed.append(anchor["id"])
        records.append(
            {
                "anchor_id": anchor["id"],
                "historical_engine": expect["route_predicate"],
                "passed": passed,
                "checks": checks,
                "screen_record": record,
            }
        )
        print(f'ANCHOR={anchor["id"]} PASSED={int(passed)}')
    payload = {
        "schema": "effective-stark-w1-anchor-regression-v1",
        "claim_tag": "VERIFIED",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "anchor_count": len(records),
        "passed_count": len(records) - len(failed),
        "failed": failed,
        "records": records,
        "interpretation": (
            "This checks necessary W1 structural predicates for each "
            "historical route. It does not replace the seven end-to-end "
            "anchor reproduction artifact."
        ),
    }
    serialized = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    output = ROOT / "artifacts" / "w1-anchor-regression-v1.json"
    output.write_text(serialized)
    print(f"PASSED_COUNT={payload['passed_count']}")
    print(f"OUTPUT_SHA256={hashlib.sha256(serialized.encode()).hexdigest()}")
    print(f"OUTPUT={output}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
