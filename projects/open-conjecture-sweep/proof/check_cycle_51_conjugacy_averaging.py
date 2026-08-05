#!/usr/bin/env python3
"""Audit the exact finite conjugacy-averaging census for Cycle 51."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle51-conjugacy-averaging"


def rows(path):
    with path.open() as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def audit():
    principal = json.loads((OUT / "summary.json").read_text())
    independent = json.loads((OUT / "independent-summary.json").read_text())
    first = rows(OUT / "comparison-rows.tsv")
    second = rows(OUT / "independent-comparison-rows.tsv")
    assert principal["status"] == independent["status"] == "PASS"
    assert principal["edge_count"] == 15
    assert principal["comparison_rows"] == independent["comparison_rows"] == len(first) == len(second) == 840
    assert principal["negative_rows"] == independent["negative_rows"] == 0
    assert principal["first_countermodel"] is None and independent["first_countermodel"] is None
    assert sorted(tuple(row.items()) for row in first) == sorted(tuple(row.items()) for row in second)
    counts = {}
    for row in first:
        key = (row["family"], row["group"])
        counts[key] = counts.get(key, 0) + 1
        assert int(row["comparison_sign"]) >= 0
    assert counts == {
        ("all_indicator", "S3"): 64,
        ("all_indicator", "D8"): 256,
        ("all_indicator", "Q8"): 256,
        ("subgroup_product", "S3"): 12,
        ("subgroup_product", "S4"): 252,
    }
    with (OUT / "direct-s3-controls.tsv").open() as handle:
        controls = list(csv.DictReader(handle, delimiter="\t"))
    assert len(controls) == 3
    assert all(row["direct_numerator"] == row["normalized_times_group"] for row in controls)
    return {
        "status": "PASS", "epistemic_status": "PROVED", "edge_count": 15,
        "rows": len(first), "negative_rows": 0, "family_counts": {f"{a}:{b}": n for (a, b), n in counts.items()},
        "normalized_left_assignments": 64 * 6**4 + 256 * 8**4 * 2 + 12 * 6**4 + 252 * 24**4,
        "claim_boundary": "Exact agreement on the frozen finite groups/functions only; a full pass neither proves Zhao's all-group comparison nor Sidorenko.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True))
