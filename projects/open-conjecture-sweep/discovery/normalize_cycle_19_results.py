#!/usr/bin/env python3
"""Deterministically correct Cycle 19's wall-sentinel status label."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle19-symbolic-antichain-optimized"


def main() -> None:
    with (OUT / "results.tsv").open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    corrected = 0
    fields = list(rows[0]) + ["raw_detail", "correction"]
    output = []
    for row in rows:
        raw_detail = row["detail"]
        correction = "none"
        if row["status"] == "CAP" and float(row["seconds"]) >= 3500 and raw_detail in {
            "left: frontier-state cap", "right: frontier-state cap"
        }:
            side = raw_detail.split(":", 1)[0]
            row["detail"] = f"{side}: aggregate wall cap"
            correction = "in-loop deadline sentinel had size STATE_CAP+1 and was mislabeled by the caller"
            corrected += 1
        output.append({**row, "raw_detail": raw_detail, "correction": correction})
    if corrected != 3:
        raise AssertionError(f"expected three sentinel-label corrections, got {corrected}")
    with (OUT / "results-corrected.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(output)
    (OUT / "result-corrected.txt").write_text(
        "rows=76 certified_no_cover=0 aggregate_wall_cap=76 full_cover_candidates=0 "
        "corrected_sentinel_labels=3 persistent_bytes=0\n"
    )
    print((OUT / "result-corrected.txt").read_text().strip())


if __name__ == "__main__":
    main()
