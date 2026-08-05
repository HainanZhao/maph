#!/usr/bin/env python3
"""Exact aggregate audit for Cycle 41."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle41-multiplied-ideal"


def audit() -> dict[str, object]:
    initial = json.loads((OUT / "result.json").read_text(encoding="utf-8"))
    zero = json.loads((OUT / "zero-support-closure.json").read_text(encoding="utf-8"))
    boundary = json.loads((OUT / "small-boundary.json").read_text(encoding="utf-8"))
    replay = json.loads((OUT / "independent-replay.json").read_text(encoding="utf-8"))
    if initial["status"] != "PASS" or initial["selected_owner_rank_two_violations"] != 428849 or initial["integral_delta_witness_extends"]:
        raise AssertionError("initial delta falsifier")
    zero_expected = {"complete_types": 1318, "original_rank_two_pair_classes": 694792, "rank3_induced_pair_classes": 228252, "original_singleton_types": 17, "original_binary_types": 36, "singleton_mediated_owner_deletions": 52, "pair_classes_with_binary_mediated_zero_cells": 1811, "disconnected_pair_classes": 58, "component_equations": 1405}
    if zero["status"] != "PASS" or zero["epistemic_status"] != "PROVED" or zero["outcome"] != "ZERO_SUPPORT_CLOSURE_FEASIBLE":
        raise AssertionError("zero closure outcome")
    for key, value in zero_expected.items():
        if zero[key] != value:
            raise AssertionError(key)
    if zero["singleton_system"] != {"status": "CONSISTENT", "rank": 1347, "variables": 15371, "nonzero": 1318, "maximum_numerator_bits": 1, "maximum_denominator_bits": 1}:
        raise AssertionError("singleton system")
    if len(zero["singleton_marginals_by_complete_type"]) != 1318 or any(len(row) != 1 or row[0][1:] != [1, 1] for row in zero["singleton_marginals_by_complete_type"]):
        raise AssertionError("integral singleton candidate")
    boundary_expected = {"small_types": 135, "rank_three_type_tuples_reenumerated": 19661454, "small_rank_three_type_classes": 0, "type_triples_checked": 11279048, "distinct_homology_interfaces": 352495, "nonzero_h1_interfaces_gf2": 7892, "nonzero_h1_type_triples_gf2": 69927, "maximum_h1_dimension_gf2": 13, "rational_relation_interfaces": 7892, "aggregate_rational_relation_rows": 199452, "aggregate_allowed_tensor_cells": 125358, "exact_left_null_relation_evaluations": 1808327, "left_null_annihilation_terms_checked": 839392, "maximum_relation_coefficient_bits": 1, "exact_candidate_failures": 0}
    if boundary["status"] != "PASS" or boundary["epistemic_status"] != "PROVED":
        raise AssertionError("boundary status")
    for key, value in boundary_expected.items():
        if boundary[key] != value:
            raise AssertionError(key)
    replay_expected = {"rank_two_type_tuples": 6684938, "rank_three_type_tuples": 19661454, "small_rank_three_type_classes": 0, "owner_deletions": 52, "offdiagonal_zero_pair_classes": 1811, "disconnected_pair_classes": 58, "small_type_triples": 11279048, "small_interfaces": 352495, "nonzero_h1_interfaces": 7892, "nonzero_h1_type_triples": 69927, "dense_support_minimum_large_size": 9, "dense_pair_intersection_minimum_side": 7, "dense_triple_intersection_minimum_side": 6}
    if replay["status"] != "PASS" or replay["epistemic_status"] != "PROVED":
        raise AssertionError("independent status")
    for key, value in replay_expected.items():
        if replay[key] != value:
            raise AssertionError(f"independent {key}")
    if [row["nonzero_ordinal"] for row in replay["exact_reversed_pivot_controls"]] != [0, 34963, 69926]:
        raise AssertionError("independent controls")
    return {"status": "PASS", "complete_types": 1318, "rank_two_type_tuples": 6684938, "rank_three_type_tuples": 19661454, "small_type_triples": 11279048, "exact_relation_evaluations": 1808327, "independent_controls": 3, "dense_support_minimum": 9}


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True))
