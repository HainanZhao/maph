#!/usr/bin/env python3
"""Lightweight exact audit for Cycle 39."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def audit() -> dict[str, object]:
    result = json.loads((ROOT / "discovery/out/cycle39-priority-routing/result.json").read_text(encoding="utf-8"))
    replay = json.loads((ROOT / "discovery/out/cycle39-priority-routing/independent-replay.json").read_text(encoding="utf-8"))
    expected_rows = [1, 134, 1, 1, 78, 1, 102, 20, 1, 231, 1, 1, 1]
    expected_mass = [150, 4500, 1, 1, 3, 5, 75, 3, 25, 150, 20, 4, 1]
    if result["status"] != replay["status"] or result["epistemic_status"] != "PROVED":
        raise AssertionError("status")
    if result["feasible_roots"] or result["capped_roots"] or result["mass_one_priority_span_extension_exists"]:
        raise AssertionError("span outcome")
    roots = result["roots"]
    if [row["root"] for row in roots] != list(range(13)) or [row["status"] for row in roots] != ["INFEASIBLE"] * 13:
        raise AssertionError("root outcomes")
    if [row["selected_rows"] for row in roots] != expected_rows:
        raise AssertionError("selected row counts")
    if [row["left_null_certificate"][0] for row in roots] != expected_mass:
        raise AssertionError("mass coefficients")
    for row in roots:
        if row["selected_rows"] != len(row["witnesses"]) or len(row["left_null_certificate"]) != row["selected_rows"] + 1:
            raise AssertionError("certificate shape")
        if any(int(witness["rank"]) != 2 for witness in row["witnesses"]):
            raise AssertionError("rank-two closure")
    if sum(expected_rows) != 573 or result["separator_moment_evaluations"] != 2515986 or result["separator_moment_evaluations_this_tranche"] != 1725301:
        raise AssertionError("CEGAR census")
    if replay["total_selected_rows"] != 573 or replay["total_priority_columns"] != 53248 or replay["priority_columns_per_root"] != 4096:
        raise AssertionError("independent census")
    if replay["direct_support_assignment_checks"] != 331338 or replay["maximum_certificate_coefficient_bits"] != 13:
        raise AssertionError("independent controls")
    if replay["mass_one_priority_span_extension_exists"] or [row["certificate_mass_coefficient"] for row in replay["roots"]] != expected_mass:
        raise AssertionError("independent certificates")
    if not all(row["all_4096_columns_zero"] for row in replay["roots"]):
        raise AssertionError("certificate column replay")
    for root in (1, 9):
        checkpoint = json.loads((ROOT / f"discovery/out/cycle39-priority-routing/root-{root:02d}-checkpoint.json").read_text(encoding="utf-8"))
        if checkpoint["witnesses"] != roots[root]["witnesses"]:
            raise AssertionError("resumed checkpoint")
    return {"status": "PASS", "roots": 13, "priority_columns": 53248, "selected_rank_two_rows": 573, "direct_support_assignment_checks": 331338, "maximum_certificate_bits": 13}


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True))
