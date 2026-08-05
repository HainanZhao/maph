#!/usr/bin/env python3
"""Probe one exact feasibility witness for every generalized partition pair."""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys

from check_cycle72_general_core_feasibility import build
from cycle72_partition_shape_probe import blocker, types


def shape(partition):
    return tuple(sorted(Counter(partition).values(), reverse=True))


def main():
    rows = []
    for name in sys.argv[1:]:
        batch = json.loads(Path(name).read_text())
        assert batch["status"] == "DONE"
        rows.extend(row for row in batch["rows"] if row["status"] == "SAT")
    assert len(rows) == 1167
    histogram = Counter()
    maximum = -1
    maximum_rows = []
    bad = []
    for row in rows:
        edges = build(row)
        line_types = types(edges)
        cover = blocker(edges, line_types)
        key = (shape(row["sides"]), shape(row["central"]), len(line_types),
               None if cover is None else len(cover))
        histogram[key] += 1
        if len(line_types) > maximum:
            maximum = len(line_types)
            maximum_rows = [row]
        elif len(line_types) == maximum:
            maximum_rows.append(row)
        if cover is None:
            bad.append(row)
    payload = {
        "status": "PASS",
        "epistemic_status": "OBSERVED",
        "partition_pair_representatives": len(rows),
        "all_blocked": not bad,
        "maximum_extension_types": maximum,
        "maximum_rows": maximum_rows[:10],
        "bad_rows": bad[:1],
        "histogram": [
            {"side_shape": list(key[0]), "central_shape": list(key[1]),
             "extension_types": key[2], "blocker_size": key[3], "count": count}
            for key, count in sorted(histogram.items())
        ],
        "claim_boundary": "One deterministic feasible assignment per partition pair; not a map-level classification or universal theorem.",
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()

