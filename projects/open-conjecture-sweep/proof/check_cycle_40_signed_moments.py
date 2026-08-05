#!/usr/bin/env python3
"""Lightweight exact audit for Cycle 40."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def audit() -> dict[str, object]:
    out = ROOT / "discovery/out/cycle40-signed-moments"
    result = json.loads((out / "result.json").read_text(encoding="utf-8"))
    replay = json.loads((out / "independent-replay.json").read_text(encoding="utf-8"))
    if result["status"] != "PASS" or result["epistemic_status"] != "PROVED":
        raise AssertionError("primary status")
    if result["outcome"] != "COMPLETE_MOMENT_CONSTRUCTION":
        raise AssertionError("construction outcome")
    expected = {
        "complete_types": 1318,
        "rank_two_pair_classes": 694912,
        "disconnected_pair_classes": 54,
        "deduplicated_graph_classes": 7497,
        "deduplicated_component_equations": 1426,
        "uniform_component_failures": 104,
        "rank_two_type_tuples": 6684938,
        "rank_three_type_tuples": 19661454,
    }
    for key, value in expected.items():
        if result[key] != value:
            raise AssertionError(key)
    singleton = result["singleton_system"]
    if singleton != {"status": "CONSISTENT", "selection": "SPARSE_EXACT", "rank": 1371, "nonzero_variables": 1318, "maximum_numerator_bits": 1, "maximum_denominator_bits": 1}:
        raise AssertionError("singleton system")
    marginals = result["singleton_marginals_by_complete_type"]
    if len(marginals) != 1318 or any(len(row) != 1 or row[0][1:] != [1, 1] for row in marginals):
        raise AssertionError("serialized singleton marginals")
    triple = result["triple_completion"]
    if (triple["classes"], triple["initial_failing_classes"], triple["induced_pair_deletion_classes"], triple["binary_triple_type_classes"], triple["unresolved_kernel_mask_classes_after_induced_pair_zeros"]) != (693, 36, 228252, 0, 0):
        raise AssertionError("triple completion")
    if replay["status"] != "PASS" or replay["epistemic_status"] != "PROVED" or not replay["mass_one_signed_degree_three_moment_family_exists"]:
        raise AssertionError("independent outcome")
    replay_expected = {"complete_types": 1318, "pair_classes": 694912, "disconnected_pair_classes": 54, "graph_classes": 7497, "induced_pair_deletion_classes": 228252, "triple_mask_classes": 693, "initial_nonsurjective_triple_classes": 36, "unresolved_triple_classes": 0, "binary_triple_type_classes": 0}
    for key, value in replay_expected.items():
        if replay[key] != value:
            raise AssertionError(f"independent {key}")
    if [row["pair_index"] for row in replay["transport_controls"]] != [0, 347456, 694911]:
        raise AssertionError("transport controls")
    return {"status": "PASS", "complete_types": 1318, "pair_classes": 694912, "triple_classes": 693, "induced_pair_deletions": 228252, "unresolved": 0}


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True))
