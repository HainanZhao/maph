#!/usr/bin/env python3
"""Audit Cycle 36's exact degree-one signed product functional."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle36-degree-one-pseudoexpectation"

EXPECTED_NORMALS = [
    [1, 1, 1, -4, 1, 1],
    [1, 1, 1, 1, 1, -4],
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, -5, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, -6, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
]
ORDINARY_HISTOGRAM = {"1": 117, "2": 121, "3": 230, "4": 359, "5": 342, "6": 158, "7": 46, "8": 15, "9": 3, "10": 1, "11": 1, "13": 1}
STRONG_HISTOGRAM = {"0": 282, "1": 583, "2": 351, "3": 129, "4": 35, "5": 7, "6": 2, "7": 2, "9": 1, "11": 1, "13": 1}


def audit() -> dict[str, object]:
    first = json.loads((OUT / "first-tranche.json").read_text(encoding="utf-8"))
    primary = json.loads((OUT / "result.json").read_text(encoding="utf-8"))
    independent = json.loads((OUT / "independent-replay.json").read_text(encoding="utf-8"))
    assert first["status"] == "CAP" and first["epistemic_status"] == "OBSERVED"
    assert (first["wall_seconds"], first["peak_rss_kib"]) == (397.43, 4378756)
    assert primary["status"] == "PASS" and primary["epistemic_status"] == "PROVED"
    assert (primary["search_states"], primary["dfs_calls"]) == (224, 232)
    assert primary["cycle35_control"]["degree_one_nonzero_count"] == 378
    assert primary["cycle35_control"]["degree_zero_nonzero"] == []
    assert primary["h11"] == {"status": "NO_PRODUCT_FUNCTIONAL", "constant_uncovered_time": 12, "local_pattern": [1, 1, 1, 1]}
    p199 = primary["p199"]
    assert p199["status"] == "COVER"
    assert (p199["root_predicate"], p199["root_alternatives"]) == (203, 2)
    assert p199["local_normals"] == EXPECTED_NORMALS
    assert [sum(row) for row in p199["local_normals"]] == [1] * 13
    assert p199["span_ranks"] == [5, 5, 6, 13, 13, 13, 12, 12, 13, 13, 13, 13, 13]
    classification = p199["predicate_classification"]
    assert classification["all_predicates_satisfy_ordinary_or_strong"] is True
    assert classification["ordinary_kill_histogram"] == ORDINARY_HISTOGRAM
    assert classification["strong_kill_histogram"] == STRONG_HISTOGRAM
    assert classification["predicates_with_strong_kill"] == 1112
    verification = p199["raw_generator_verification"]
    assert verification["local_masses"] == [1] * 13 and verification["global_mass"] == "1"
    assert verification["degree_zero_nonzero"] == [] and verification["degree_one_nonzero_count"] == 0
    assert verification["automatic_degree_one"] == 31768

    assert independent["status"] == "PASS" and independent["epistemic_status"] == "PROVED"
    replay = independent["p199"]
    assert replay["coordinate_dimensions"] == [6, 6, 7] + [14] * 10
    assert replay["local_masses"] == [1] * 13 and replay["global_mass"] == 1
    assert replay["degree_zero_generators"] == 1394 and replay["degree_zero_nonzero"] == 0
    assert replay["raw_degree_one_generators"] == 221646 and replay["degree_one_nonzero"] == 0
    assert replay["automatic_degree_one_generators"] == 31768
    assert replay["ordinary_kill_histogram"] == ORDINARY_HISTOGRAM
    assert replay["strong_kill_histogram"] == STRONG_HISTOGRAM
    assert replay["predicates_with_strong_kill"] == 1112
    assert replay["ordinary_or_strong_equivalence_pass"] is True
    assert replay["maximum_absolute_local_coefficient"] == 6
    return {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "claim_boundary": "degree-at-most-one direct predicates with one-hot coordinate multipliers, p199 base 4 / leaf 78",
        "degree_zero_generators": 1394,
        "degree_one_generators": 221646,
        "all_generator_contractions_zero": True,
        "local_masses": [1] * 13,
        "global_mass": 1,
        "maximum_absolute_local_coefficient": 6,
        "independent_direct_set_replay": "PASS",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
