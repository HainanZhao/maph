#!/usr/bin/env python3
"""Check the union accounting for the three C72 labelled-core count shards."""
import json
import sys
from pathlib import Path


def main():
    rows = [json.loads(Path(path).read_text()) for path in sys.argv[1:]]
    assert len(rows) == 3
    assert all(row["status"] == "DONE" for row in rows), rows
    assert {row["shard"] for row in rows} == {0, 1, 2}
    assert {row["shards"] for row in rows} == {3}
    assert sum(row["pair_codes_checked"] for row in rows) == rows[0]["total_pair_codes"]
    assert all(row["solutions"] < row["solution_limit"] for row in rows)
    print(json.dumps({"status":"PASS","epistemic_status":"PROVED","pair_codes":sum(row["pair_codes_checked"] for row in rows),"labelled_core_assignments":sum(row["solutions"] for row in rows)},sort_keys=True))


if __name__ == "__main__":
    main()
