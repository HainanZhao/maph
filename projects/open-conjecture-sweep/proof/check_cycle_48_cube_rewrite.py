#!/usr/bin/env python3
"""Audit Cycle 48's serialized Möbius/cube rewrite classification."""
from __future__ import annotations

from collections import Counter
from fractions import Fraction
import itertools
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
from lrc_cube_rewrite import cell_allowed, pair_marginals

OUT = ROOT / "discovery/out/cycle48-cube-rewrite"


def parse(rows):
    return {tuple(cell): Fraction(numerator, denominator) for cell, numerator, denominator in rows}


def audit():
    selection = json.loads((OUT / "selection.json").read_text())
    controls = json.loads((OUT / "generic-controls.json").read_text())
    actual = json.loads((OUT / "actual.json").read_text())
    independent = json.loads((OUT / "independent-replay.json").read_text())
    independent_selection = json.loads((OUT / "independent-selection.json").read_text())
    assert selection["status"] == controls["status"] == actual["status"] == independent["status"] == independent_selection["status"] == "PASS"
    assert selection["selected_faces"] == actual["selected_faces"] == independent["faces"] == 512
    assert independent_selection["selected_faces"] == 512
    assert independent_selection["candidates"] == selection["deduplicated_candidates"]
    assert independent_selection["descriptor_strata"] == selection["descriptor_strata"]
    assert len({tuple(row["types"]) for row in selection["selected"]}) == 512
    repair_counts = Counter()
    confluence_counts = Counter()
    aggregate = Counter()
    for ordinal, (source, row, replay) in enumerate(zip(selection["selected"], actual["records"], independent["records"], strict=True)):
        assert row["ordinal"] == replay["ordinal"] == ordinal
        assert source["types"] == row["types"] == replay["types"]
        assert source["selection_hash"] == row["selection_hash"]
        supports = tuple(tuple(values) for values in source["supports"])
        pair_deleted = {(left, right): deleted for left, right, deleted in source["pair_deleted"]}
        triple_deleted = source["triple_deleted"]
        flows = {(left, right): parse(values) for left, right, values in source["pair_flows"]}
        mobius = parse(row["mobius"])
        repaired = parse(row["repaired_tensor"])
        assert pair_marginals(mobius) == pair_marginals(repaired) == flows
        forbidden = {cell for cell in itertools.product(*supports) if not cell_allowed(tuple(source["types"]), cell, pair_deleted, triple_deleted)}
        assert len(forbidden) == row["forbidden_cells"] and not (set(repaired) & forbidden)
        assert row["repair_status"] != "UNREPAIRED" and row["first_missing"] is None
        assert replay["repair_status"] == row["repair_status"] and replay["confluence_status"] == row["confluence_status"]
        if row["first_diamond"]:
            difference = parse(row["first_diamond"]["difference"])
            normal = parse(row["first_diamond"]["normal_form"])
            assert all(not values for values in pair_marginals(difference).values())
            assert all(not values for values in pair_marginals(normal).values())
            assert normal and row["confluence_status"] == "NONCONFLUENT"
        repair_counts[row["repair_status"]] += 1
        confluence_counts[row["confluence_status"]] += 1
        aggregate["forbidden"] += row["forbidden_cells"]
        aggregate["cubes"] += row["cube_candidates"]
        aggregate["steps"] += row["repair_steps"]
        aggregate["diamonds"] += row["critical_diamonds_tested"]
    assert dict(sorted(repair_counts.items())) == actual["repair_status_counts"] == independent["repair_status_counts"]
    assert dict(sorted(confluence_counts.items())) == actual["confluence_status_counts"] == independent["confluence_status_counts"]
    assert aggregate == Counter({
        "forbidden": actual["aggregate_forbidden_cells"], "cubes": actual["aggregate_cube_candidates"],
        "steps": actual["aggregate_repair_steps"], "diamonds": actual["aggregate_critical_diamonds"],
    })
    selected_support_cells = sum(math.prod(row["support_sizes"]) for row in selection["selected"])
    control_support_upper = controls["cube_kernel_checks"] * 4**3 + 4 * 4**3
    support_cells_upper = selected_support_cells + control_support_upper
    material_entry_operations_upper = 0
    for source, row in zip(selection["selected"], actual["records"], strict=True):
        face_cells = math.prod(source["support_sizes"])
        material_entry_operations_upper += (
            2 * face_cells
            + 8 * row["repair_steps"]
            + row["critical_diamonds_tested"] * (14 + 8 * row["forbidden_cells"])
        )
    tensor_entry_operations_upper = (
        2 * independent_selection["mobius_nonzeros"]
        + 2 * material_entry_operations_upper
        + 100_000
    )
    maximum_forbidden_cells = max(row["forbidden_cells"] for row in actual["records"])
    fraction_height_bits_upper = independent_selection["maximum_mobius_fraction_bits"] + maximum_forbidden_cells + 2
    aggregate_wall_seconds = sum(
        row.get("wall_seconds", 1) for row in (selection, controls, actual, independent_selection, independent)
    )
    temporary_disk_bytes = sum(path.stat().st_size for path in OUT.iterdir() if path.is_file())
    assert support_cells_upper < 2_000_000
    assert tensor_entry_operations_upper < 100_000_000
    assert fraction_height_bits_upper < 131_072
    assert aggregate_wall_seconds < 14_400
    assert temporary_disk_bytes < 5_368_709_120
    resources = {
        "selected_support_cells": selected_support_cells,
        "support_cells_upper": support_cells_upper,
        "tensor_entry_operations_upper": tensor_entry_operations_upper,
        "fraction_height_bits_upper": fraction_height_bits_upper,
        "aggregate_wall_seconds": aggregate_wall_seconds,
        "temporary_disk_bytes": temporary_disk_bytes,
    }
    return {
        "status": "PASS", "faces": 512, "repair_status_counts": dict(sorted(repair_counts.items())),
        "confluence_status_counts": dict(sorted(confluence_counts.items())),
        "mobius_defect_faces": actual["mobius_defect_faces"],
        "aggregate_forbidden_cells": aggregate["forbidden"], "aggregate_cube_candidates": aggregate["cubes"],
        "aggregate_repair_steps": aggregate["steps"], "aggregate_critical_diamonds": aggregate["diamonds"],
        "resources": resources,
    }


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True))
