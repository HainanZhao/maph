#!/usr/bin/env python3
"""Lightweight exact audit for Cycle 38."""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def audit() -> dict[str, object]:
    result = json.loads((ROOT / "discovery/out/cycle38-ownership-functional/result.json").read_text(encoding="utf-8"))
    replay = json.loads((ROOT / "discovery/out/cycle38-ownership-functional/independent-replay.json").read_text(encoding="utf-8"))
    prior = json.loads((ROOT / "discovery/out/cycle29-ownership-blocker/result.json").read_text(encoding="utf-8"))["p199"]
    if result["status"] != replay["status"] or result["epistemic_status"] != "PROVED":
        raise AssertionError("result status")
    if result["interface"] != {"distinct_complete_global_types": 1318, "nonzero_support_assignments": 14406, "times": 2786}:
        raise AssertionError("interface census")
    expected_tuples = [423647, 423647, 593829, 2497722, 2427236, 2427489, 2427237, 2568205, 2356758, 2568204, 2497721, 2568205, 2568203]
    expected_moments = [150, 100, 1, 1, 5, 5, 5, -1, -25, 100, -20, 4, 1]
    roots = result["roots"]
    if [row["root"] for row in roots] != list(range(13)) or [row["status"] for row in roots] != ["OBSTRUCTED"] * 13:
        raise AssertionError("root statuses")
    if [row["complete_type_tuples"] for row in roots] != expected_tuples:
        raise AssertionError("type tuple census")
    if [row["first_nonzero"]["moment"] for row in roots] != expected_moments:
        raise AssertionError("root moments")
    for root, row in enumerate(roots):
        coordinate = prior["coordinates"][root]
        if row["symbolic_patterns"] != coordinate["symbolic_pattern_count"]:
            raise AssertionError("symbolic pattern projection")
        if row["concrete_blockers"] != coordinate["concrete_blocker_count"]:
            raise AssertionError("concrete blocker projection")
        if row["first_nonzero"]["rank"] != 2 or not row["nonzero_type_tuples_by_rank"].get("2"):
            raise AssertionError("rank-two obstruction")
        if sum(row["tuple_counts_by_rank"].values()) != row["complete_type_tuples"]:
            raise AssertionError("tuple rank partition")
        if sum(row["concrete_counts_by_rank"].values()) != row["concrete_blockers"]:
            raise AssertionError("concrete rank partition")
    if sum(expected_tuples) != result["complete_type_tuples"] or result["exact_moment_evaluations"] != 26348103:
        raise AssertionError("global tuple census")
    if sum(row["concrete_blockers"] for row in roots) != result["concrete_blockers"] or result["concrete_blockers"] != prior["concrete_blocker_count"]:
        raise AssertionError("global blocker census")
    if result["span"]["mass_one_extension_exists"] or result["span"]["rank_of_nonzero_root_columns"] != 13:
        raise AssertionError("span outcome")
    witnesses = replay["root_witnesses"]
    if [row["root"] for row in witnesses] != list(range(13)) or [row["moment"] for row in witnesses] != expected_moments:
        raise AssertionError("independent witnesses")
    certificate = replay["augmented_system_left_null_certificate"]
    multipliers = certificate["blocker_row_multipliers"]
    mass = certificate["mass_row_multiplier"]
    if any(multipliers[index] * expected_moments[index] + mass for index in range(13)):
        raise AssertionError("left-null coefficient product")
    if certificate["left_product_with_coefficient_matrix"] != [0] * 13 or certificate["left_product_with_right_hand_side"] != mass or mass == 0:
        raise AssertionError("left-null RHS")
    if math.prod(expected_moments) == 0 or replay["root_diagonal_rank"] != 13 or replay["mass_one_span_extension_exists"]:
        raise AssertionError("diagonal obstruction")
    return {"status": "PASS", "roots": 13, "symbolic_patterns": 12264, "concrete_blockers": 190867444, "complete_type_tuples": 26348103, "direct_support_assignments_per_witness": 14406, "augmented_left_null_rhs": mass}


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True))
