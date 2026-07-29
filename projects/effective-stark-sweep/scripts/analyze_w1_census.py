#!/usr/bin/env python3
"""Exact histogram, yield checkpoint, and conductor-norm trend analysis."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts" / "w1-full-census-v1.json"
KNOWN_ANCHORS_IN_RANGE = {"RQ-000057", "RQ-000099", "RQ-000113"}


def fraction_record(numerator: int, denominator: int) -> dict[str, object]:
    value = Fraction(numerator, denominator)
    return {
        "numerator": numerator,
        "denominator": denominator,
        "reduced": f"{value.numerator}/{value.denominator}",
        "decimal": float(value),
    }


def main() -> None:
    census = json.loads(SOURCE.read_text())
    records = census["records"]
    by_norm: dict[int, list[int]] = defaultdict(lambda: [0, 0])
    for row in records:
        norm = int(row["finite_norm"])
        by_norm[norm][0] += 1
        by_norm[norm][1] += row["verdict"] == "FRONTIER"

    quartiles = []
    for left, right in ((1, 25), (26, 50), (51, 75), (76, 100)):
        total = sum(by_norm[n][0] for n in range(left, right + 1))
        frontier = sum(by_norm[n][1] for n in range(left, right + 1))
        quartiles.append(
            {
                "norm_interval": [left, right],
                "total": total,
                "frontier": frontier,
                "frontier_share": fraction_record(frontier, total),
            }
        )
    monotone = all(
        Fraction(
            quartiles[index]["frontier"],
            quartiles[index]["total"],
        )
        < Fraction(
            quartiles[index + 1]["frontier"],
            quartiles[index + 1]["total"],
        )
        for index in range(3)
    )

    route_candidates = [
        row for row in records if row["verdict"] == "ROUTE_CANDIDATE"
    ]
    new_candidates = [
        row
        for row in route_candidates
        if row["case_id"] not in KNOWN_ANCHORS_IN_RANGE
    ]
    threshold = 15
    payload = {
        "schema": "effective-stark-w1-census-analysis-v1",
        "claim_tag": "VERIFIED_COUNTS",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "engine_histogram": dict(
            sorted(Counter(row["engine"] for row in route_candidates).items())
        ),
        "frontier_taxonomy": dict(
            sorted(
                Counter(
                    row["obstruction"]
                    for row in records
                    if row["verdict"] == "FRONTIER"
                ).items()
            )
        ),
        "yield_checkpoint": {
            "threshold": threshold,
            "known_anchor_case_ids_removed": sorted(KNOWN_ANCHORS_IN_RANGE),
            "structural_route_candidates_beyond_anchors": len(new_candidates),
            "verdict": (
                "PASS_CENSUS_PAPER_FRAMING"
                if len(new_candidates) >= threshold
                else "RESCOPE_FRONTIER_MAP"
            ),
            "boundary": (
                "W1 route eligibility, not packet-level PROVED status"
            ),
        },
        "norm_quartiles": quartiles,
        "frontier_share_strictly_increases_by_norm_quartile": monotone,
        "prediction_result": (
            "SUPPORTED_ON_FROZEN_QUARTILE_SUMMARY"
            if monotone
            else "NOT_SUPPORTED_ON_FROZEN_QUARTILE_SUMMARY"
        ),
        "per_norm": {
            str(norm): {
                "total": values[0],
                "frontier": values[1],
                "frontier_share": fraction_record(values[1], values[0]),
            }
            for norm, values in sorted(by_norm.items())
        },
    }
    serialized = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    output = ROOT / "artifacts" / "w1-census-analysis-v1.json"
    output.write_text(serialized)
    print(
        "YIELD_CHECKPOINT="
        f'{payload["yield_checkpoint"]["verdict"]}'
    )
    print(
        "STRUCTURAL_CANDIDATES_BEYOND_ANCHORS="
        f"{len(new_candidates)}"
    )
    print(f"NORM_QUARTILE_MONOTONE={int(monotone)}")
    print(f"OUTPUT_SHA256={hashlib.sha256(serialized.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
