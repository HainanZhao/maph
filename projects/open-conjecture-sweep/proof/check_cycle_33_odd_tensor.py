#!/usr/bin/env python3
"""Audit Cycle 33's exact degree-zero GF(3)/GF(5) boundaries."""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle33-odd-tensor"
ASSIGNMENT_HASH = "de06f7bea5bf1673f5a31d2febcac3e130fd67f5bf1ed6112e237b76a0cf5f84"


def audit() -> dict[str, object]:
    primary = json.loads((OUT / "result.json").read_text(encoding="utf-8"))
    independent = json.loads((OUT / "independent-replay.json").read_text(encoding="utf-8"))
    assert primary["status"] == independent["status"] == "PASS"
    assert primary["assignment_hash"] == independent["assignment_hash"] == ASSIGNMENT_HASH
    assert primary["h11"] == {
        "assignments": 64,
        "base": [1, 1, 1],
        "coefficient": 1,
        "coefficient_time": 12,
        "fields": [3, 5],
        "status": "PASS",
    }
    assert independent["h11"] == {
        "base": [1, 1, 1],
        "constant_uncovered_time": 12,
        "fields": [3, 5],
    }

    expected = {
        3: {"rank": 1228, "reductions": 416035, "size": 802, "counts": {1: 403, 2: 399}},
        5: {"rank": 1228, "reductions": 488805, "size": 985, "counts": {1: 223, 2: 238, 3: 284, 4: 240}},
    }
    primary_fields = {row["field"]: row for row in primary["fields"]}
    independent_fields = {row["field"]: row for row in independent["fields"]}
    replay_fields = {row["field"]: row for row in independent["highest_pivot_replays"]}
    assert set(primary_fields) == set(independent_fields) == set(replay_fields) == {3, 5}
    for field, exp in expected.items():
        row = primary_fields[field]
        assert row["status"] == "INCONSISTENT_EVALUATION_SUBSYSTEM"
        assert row["assignment_hash"] == ASSIGNMENT_HASH
        assert (row["equations"], row["rounds"], row["rank"], row["row_reductions"], row["tensor_verifier_nodes"], row["contradiction_size"]) == (
            4243, 1, exp["rank"], exp["reductions"], 0, exp["size"]
        )
        counts = Counter(term["coefficient"] for term in row["contradiction_terms"])
        assert dict(counts) == exp["counts"]
        independent_row = independent_fields[field]
        assert independent_row == {
            "contradiction_size": exp["size"],
            "field": field,
            "predicate_sum": "ZERO",
            "rhs_sum": 1,
        }
        replay = replay_fields[field]
        assert replay["status"] == "INCONSISTENT"
    assert replay_fields[3]["rank_before_contradiction"] == 1227
    assert replay_fields[5]["rank_before_contradiction"] == 1228

    return {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "claim_boundary": "degree-zero GF(3) and GF(5), H11 base (1,1,1) and p199 base 4 / leaf 78 only",
        "assignment_hash": ASSIGNMENT_HASH,
        "p199_predicate_columns": 1394,
        "p199_evaluation_rows": 4243,
        "contradiction_sizes": {"GF3": 802, "GF5": 985},
        "degree_zero_identities": {"GF3": False, "GF5": False},
        "independent_replay": "PASS",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
