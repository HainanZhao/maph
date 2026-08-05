#!/usr/bin/env python3
"""Audit union accounting and aggregate pattern counts for generalized C72 cores."""
import json
import sys
from pathlib import Path


def main():
    rows = [json.loads(Path(path).read_text()) for path in sys.argv[1:]]
    assert len(rows) == 3
    assert all(row["status"] == "DONE" for row in rows), rows
    assert {row["shard"] for row in rows} == {0, 1, 2}
    assert {row["shards"] for row in rows} == {3}
    assert len({row["case_total"] for row in rows}) == 1
    assert sum(row["cases_checked"] for row in rows) == rows[0]["case_total"]
    assert all(row["solutions"] < row["solution_limit"] for row in rows)
    patterns = [tuple(item["sides"]) for item in rows[0]["patterns"]]
    assert len(patterns) == len(set(patterns)) == 52
    assert all([tuple(item["sides"]) for item in row["patterns"]] == patterns for row in rows)
    counts = [sum(row["patterns"][i]["solutions"] for row in rows) for i in range(52)]
    nonzero = [{"sides": list(patterns[i]), "solutions": counts[i]} for i in range(52) if counts[i]]
    result = {"status":"PASS","epistemic_status":"PROVED","cases":sum(row["cases_checked"] for row in rows),"generalized_core_assignments":sum(counts),"nonzero_patterns":nonzero}
    assert result["generalized_core_assignments"] == sum(row["solutions"] for row in rows)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
