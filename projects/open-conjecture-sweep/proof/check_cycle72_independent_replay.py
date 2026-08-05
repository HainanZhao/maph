#!/usr/bin/env python3
"""Reconcile complete C72 primary and independent replay shards."""
from __future__ import annotations

import json
from pathlib import Path
import sys


EXPECTED = {
    "distinct": (51, [0, 1, 2, 3, 4]),
    "double": (14, [0, 0, 1, 2, 3]),
    "double-double": (10, [0, 0, 1, 1, 2]),
}
EXPECTED_CASES = 52 * 15**5


def aggregate(rows, *, primary):
    assert len(rows) == 3
    assert all(row["status"] == "DONE" for row in rows)
    assert {row["shard"] for row in rows} == {0, 1, 2}
    assert {row["shards"] for row in rows} == {3}
    assert sum(row["cases"] for row in rows) == EXPECTED_CASES
    count_key = "assignments" if primary else "realized_cores"
    max_key = "max_extension_types" if primary else "max_extension_traces"
    sum_key = "canonical_hash_sum" if primary else "hash_sum"
    xor_key = "canonical_hash_xor" if primary else "hash_xor"
    xor_value = 0
    for row in rows:
        xor_value ^= row[xor_key]
    return {
        "cases": sum(row["cases"] for row in rows),
        "realized_cores": sum(row[count_key] for row in rows),
        "maximum_extension_traces": max(row[max_key] for row in rows),
        "hash_sum": sum(row[sum_key] for row in rows) % (1 << 64),
        "hash_xor": xor_value,
    }


def main():
    assert len(sys.argv) == 8, (
        "usage: checker SHAPE PRIMARY0 PRIMARY1 PRIMARY2 INDEPENDENT0 "
        "INDEPENDENT1 INDEPENDENT2"
    )
    shape = sys.argv[1]
    expected_filter, expected_side = EXPECTED[shape]
    primary = [json.loads(Path(name).read_text()) for name in sys.argv[2:5]]
    independent = [json.loads(Path(name).read_text()) for name in sys.argv[5:8]]
    assert {row["side_filter"] for row in primary} == {expected_filter}
    assert {row["shape"] for row in independent} == {shape}
    assert all(row["side_representative"] == expected_side for row in independent)
    assert all(row["side_domain_check"] == "PASS" for row in independent)
    a = aggregate(primary, primary=True)
    b = aggregate(independent, primary=False)
    assert a == b, {"primary": a, "independent": b}
    print(json.dumps({
        "status": "PASS",
        "epistemic_status": "PROVED",
        "shape": shape,
        "agreement": a,
        "claim_boundary": (
            "Two exhaustive implementations agree for this side-shape "
            "representative; global promotion also uses the proved "
            "side-shape reduction and structural C72 implication."
        ),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
