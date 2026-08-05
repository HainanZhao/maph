#!/usr/bin/env python3
"""Audit Cycle 19's corrected symbolic-antichain performance boundary."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle19-symbolic-antichain-optimized"
OLD17 = ROOT / "discovery/out/cycle17-time-deficit/lp-results.tsv"
OLD18 = ROOT / "discovery/out/cycle18-pair-choice/results.tsv"


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def audit() -> dict[str, int]:
    boundary17 = {
        (int(row["base_index"]), int(row["leaf_ordinal"]))
        for row in table(OLD17) if row["status"] == "NO_LP_DEFICIT"
    }
    expected = [
        (int(row["base_index"]), int(row["leaf_ordinal"]))
        for row in table(OLD18) if row["status"] == "UNRESOLVED"
    ]
    if len(expected) != 76 or any(item not in boundary17 for item in expected):
        raise AssertionError("frozen target boundary mismatch")
    raw, corrected = table(OUT / "results.tsv"), table(OUT / "results-corrected.tsv")
    if len(raw) != 76 or len(corrected) != 76:
        raise AssertionError("result row count mismatch")
    actual = [(int(row["base_index"]), int(row["leaf_ordinal"])) for row in corrected]
    if actual != expected:
        raise AssertionError("result order mismatch")
    corrections = 0
    partial = 0
    for source, final in zip(raw, corrected, strict=True):
        if any(source[key] != final[key] for key in source if key != "detail"):
            raise AssertionError("correction altered a non-detail field")
        if final["raw_detail"] != source["detail"] or final["status"] != "CAP":
            raise AssertionError("raw provenance/status mismatch")
        elapsed = float(source["seconds"])
        if source["detail"] in {"left: frontier-state cap", "right: frontier-state cap"}:
            if elapsed < 3500 or final["detail"] not in {"left: aggregate wall cap", "right: aggregate wall cap"}:
                raise AssertionError("invalid deadline-sentinel correction")
            if "in-loop deadline sentinel" not in final["correction"]:
                raise AssertionError("missing correction reason")
            corrections += 1
        elif source["detail"] != final["detail"] or final["correction"] != "none":
            raise AssertionError("spurious correction")
        if int(source["generated_children"]) > 0:
            partial += 1
        if source["left_path"] != "-" or source["right_path"] != "-":
            raise AssertionError("capped row retained an asserted final frontier")
    result = {
        "rows": len(corrected),
        "aggregate_wall_caps": sum(row["detail"].endswith("aggregate wall cap") for row in corrected),
        "sentinel_label_corrections": corrections,
        "partially_executed_rows": partial,
        "certified": sum(row["status"] == "CERTIFIED_NO_COVER" for row in corrected),
        "candidates": sum(row["status"] == "FULL_COVER_CANDIDATE" for row in corrected),
    }
    if result != {"rows": 76, "aggregate_wall_caps": 76, "sentinel_label_corrections": 3, "partially_executed_rows": 3, "certified": 0, "candidates": 0}:
        raise AssertionError("headline mismatch")
    return result


if __name__ == "__main__":
    print("PASS " + " ".join(f"{key}={value}" for key, value in audit().items()))
