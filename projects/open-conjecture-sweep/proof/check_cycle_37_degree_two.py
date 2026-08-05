#!/usr/bin/env python3
"""Audit Cycle 37's exact degree-two signed product functional."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle37-degree-two-product"

EXPECTED_NORMALS = [
    [0, 1, 0, 0, 0, 0],
    [1, -4, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, -5, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, -5, 0, 1, 0],
    [1, 0, 1, 0, -5, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, -5, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
]
ORDINARY = {"1": 101, "2": 70, "3": 98, "4": 254, "5": 380, "6": 289, "7": 144, "8": 42, "9": 9, "10": 5, "11": 1, "13": 1}
STRONG = {"0": 338, "1": 580, "2": 332, "3": 107, "4": 23, "5": 7, "6": 3, "7": 1, "9": 1, "11": 1, "13": 1}


def audit() -> dict[str, object]:
    primary = json.loads((OUT / "result.json").read_text(encoding="utf-8"))
    independent = json.loads((OUT / "independent-replay.json").read_text(encoding="utf-8"))
    assert primary["status"] == "PASS" and primary["epistemic_status"] == "PROVED"
    assert (primary["search_states"], primary["dfs_calls"]) == (7012, 8514)
    assert len(primary["cycle36_control"]["predicate_classification"]["escaping_predicates"]) == 54
    assert primary["cycle36_control"]["raw_degree_two"]["degree_two_nonzero_count"] == 2010
    assert primary["h11"] == {"status": "NO_PRODUCT_FUNCTIONAL", "constant_uncovered_time": 12, "local_pattern": [1, 1, 1, 1]}
    p199 = primary["p199"]
    assert p199["status"] == "COVER" and (p199["root_predicate"], p199["root_alternatives"]) == (203, 2)
    assert p199["local_normals"] == EXPECTED_NORMALS
    assert [sum(row) for row in EXPECTED_NORMALS] == [1] * 13
    assert p199["span_ranks"] == [5, 5, 6, 13, 13, 13, 12, 12, 13, 13, 13, 13, 13]
    classification = p199["predicate_classification"]
    assert classification["all_predicates_satisfy_three_or_strong"] is True
    assert classification["escaping_predicates"] == []
    assert classification["ordinary_kill_histogram"] == ORDINARY
    assert classification["strong_kill_histogram"] == STRONG
    assert classification["predicates_with_strong_kill"] == 1056
    assert p199["lower_degree_verification"]["degree_zero_nonzero"] == []
    assert p199["lower_degree_verification"]["degree_one_nonzero_count"] == 0
    assert p199["degree_two_verification"] == {"raw_degree_two_generators": 16170400, "degree_two_nonzero_count": 0, "first_nonzero_labels": []}

    assert independent["status"] == "PASS" and independent["epistemic_status"] == "PROVED"
    replay = independent["p199"]
    assert replay["coordinate_dimensions"] == [6, 6, 7] + [14] * 10
    assert replay["local_masses"] == [1] * 13 and replay["global_mass"] == 1
    assert (replay["degree_zero_generators"], replay["degree_zero_nonzero"]) == (1394, 0)
    assert (replay["raw_degree_one_generators"], replay["degree_one_nonzero"]) == (221646, 0)
    assert (replay["raw_degree_two_generators"], replay["degree_two_nonzero"]) == (16170400, 0)
    assert replay["ordinary_kill_histogram"] == ORDINARY and replay["strong_kill_histogram"] == STRONG
    assert replay["predicates_with_strong_kill"] == 1056
    assert replay["three_or_strong_equivalence_pass"] is True
    assert replay["maximum_absolute_local_coefficient"] == 5
    return {"status": "PASS", "epistemic_status": "PROVED", "claim_boundary": "degree-at-most-two direct-predicate one-hot calculus, p199 base 4 / leaf 78", "degree_zero_generators": 1394, "degree_one_generators": 221646, "degree_two_generators": 16170400, "all_generator_contractions_zero": True, "local_masses": [1] * 13, "global_mass": 1, "maximum_absolute_local_coefficient": 5, "independent_full_raw_replay": "PASS"}


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
