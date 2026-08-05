#!/usr/bin/env python3
"""Audit Cycle 35's exact rank-one local product measure."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle35-local-product-measure"

EXPECTED_NORMALS = [
    [1, -3, 1, 1, 0, 1],
    [-2, 1, 1, 0, 1, 0],
    [1, 1, 1, -5, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
EXPECTED_KILLS = [709, 540, 1050, 204, 328, 200, 200, 199, 200, 204, 200, 200, 200]
EXPECTED_SPAN_KILLS = [709, 540, 1050, 33, 114, 30, 15, 100, 30, 30, 30, 30, 30]


def audit() -> dict[str, object]:
    first = json.loads((OUT / "first-tranche.json").read_text(encoding="utf-8"))
    primary = json.loads((OUT / "result.json").read_text(encoding="utf-8"))
    independent = json.loads((OUT / "independent-replay.json").read_text(encoding="utf-8"))
    assert first["status"] == "PASS" and first["p199"]["status"] == "CAP"
    assert first["p199"]["flat_states"] == 1_000_000
    assert first["h11"]["status"] == "NO_COVER"
    assert primary["status"] == "PASS" and primary["epistemic_status"] == "PROVED"
    assert primary["first_tranche"] == {"status": "CAP", "flat_states": 1_000_000, "wall_seconds": 428.98}
    assert primary["second_tranche_states"] == 26
    assert primary["h11"] == {"status": "NO_COVER", "root_predicate": 12, "root_feasible_coordinates": 0, "root_branches": []}
    p199 = primary["p199"]
    assert p199["status"] == "COVER"
    assert (p199["root_predicate"], p199["root_feasible_coordinates"]) == (203, 1)
    assert p199["root_branches"] == [{"root_coordinate": 5, "status": "COVER", "memoized_no_cover_states": 0}]
    selection = sorted(p199["selection"], key=lambda row: row["coordinate"])
    assert [row["normal"] for row in selection] == EXPECTED_NORMALS
    assert [sum(row["normal"]) for row in selection] == [1] * 13
    assert [row["cover_count"] for row in selection] == EXPECTED_KILLS
    assert [row["span_guaranteed_cover_count"] for row in selection] == EXPECTED_SPAN_KILLS
    assert p199["verification"] == {"local_masses": [1] * 13, "global_mass": "1", "minimum_killing_coordinates": 1, "maximum_killing_coordinates": 13}

    assert independent["status"] == "PASS" and independent["epistemic_status"] == "PROVED"
    replay = independent["p199"]
    assert replay["predicate_columns"] == 1394
    assert replay["coordinate_dimensions"] == [6, 6, 7] + [14] * 10
    assert replay["local_masses"] == [1] * 13 and replay["global_mass"] == 1
    assert replay["coordinate_kill_counts"] == EXPECTED_KILLS
    assert replay["all_predicates_annihilated"] is True
    assert (replay["minimum_killing_coordinates"], replay["maximum_killing_coordinates"]) == (1, 13)
    assert replay["killing_coordinate_histogram"] == {"1": 181, "2": 303, "3": 383, "4": 282, "5": 146, "6": 70, "7": 21, "8": 5, "9": 1, "11": 1, "13": 1}
    assert replay["single_killer_counts"] == [27, 19, 50, 13, 4, 12, 4, 9, 17, 5, 9, 9, 3]
    assert replay["maximum_absolute_local_coefficient"] == 5
    assert independent["h11"] == {"constant_uncovered_time": 12, "local_pattern": [1, 1, 1, 1], "product_measure": False}
    return {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "claim_boundary": "rank-one rational product signed measure, p199 base 4 / leaf 78 direct predicates only",
        "predicate_columns": 1394,
        "coordinates": 13,
        "local_masses": [1] * 13,
        "global_mass": 1,
        "all_predicates_annihilated": True,
        "minimum_killing_coordinates": 1,
        "maximum_absolute_local_coefficient": 5,
        "independent_direct_mask_replay": "PASS",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
