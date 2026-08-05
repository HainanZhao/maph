#!/usr/bin/env python3
"""Exact terminal audit of Cycle 49's first frozen-buffer failure."""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
from lrc_cube_rewrite import normalized_cube, pair_marginals
from lrc_relative_diagonal import PAIRS, cell_allowed, serialize

OUT = ROOT / "discovery/out/cycle49-relative-diagonal"


def parse(rows):
    return {tuple(cell): Fraction(numerator, denominator) for cell, numerator, denominator in rows}


def main():
    full = json.loads((OUT / "full-audit.json").read_text())
    failure = full["first_failure"]
    inventory = json.loads((OUT / "inventory.json").read_text())
    type_rows = {row["index"]: row for row in inventory["types"]}
    supports = tuple(
        tuple(owner for owner in range(13) if type_rows[value]["support_mask"] & (1 << owner))
        for value in failure["types"]
    )
    assert tuple(map(len, supports)) == tuple(failure["support_sizes"]) == (2, 2, 2)
    pivot = tuple(failure["pivot"])
    alternatives = tuple(next(owner for owner in supports[index] if owner != pivot[index]) for index in range(3))
    cube = normalized_cube(pivot, alternatives)
    mobius = parse(failure["mobius"])
    pair_deleted = {(left, right): deleted for left, right, deleted in failure["pair_deleted"]}
    scale = -mobius[pivot] / cube[pivot]
    repaired = defaultdict(Fraction, mobius)
    for cell, value in cube.items():
        repaired[cell] += scale * value
    repaired = {cell: value for cell, value in repaired.items() if value}
    forbidden_before = {cell for cell in mobius if not cell_allowed(cell, pair_deleted, failure["triple_deleted"])}
    forbidden_after = {cell for cell in repaired if not cell_allowed(cell, pair_deleted, failure["triple_deleted"])}
    flows = {(left, right): parse(rows) for left, right, rows in failure["pair_flows"]}
    assert pair_marginals(mobius) == pair_marginals(repaired) == flows
    assert forbidden_before and not forbidden_after
    kernel_dimension = (len(supports[0]) - 1) * (len(supports[1]) - 1) * (len(supports[2]) - 1)
    assert kernel_dimension == 1
    restriction = [cube[cell] for cell in sorted(forbidden_before)]
    defect = [mobius[cell] for cell in sorted(forbidden_before)]
    assert defect == [-scale * value for value in restriction]
    result = {
        "status": "PASS", "epistemic_status": "PROVED", "stage": "FIRST_TERMINAL_EXCEPTION_AUDIT",
        "classification": "BUFFER_INCOMPLETE",
        "types": failure["types"], "supports": [list(values) for values in supports],
        "pair_deleted": failure["pair_deleted"], "triple_deleted": failure["triple_deleted"],
        "forbidden_cells": [list(cell) for cell in sorted(forbidden_before)],
        "cube_alternatives": list(alternatives), "cube_scale": [scale.numerator, scale.denominator],
        "cube_kernel_dimension": kernel_dimension,
        "restriction_column": [[value.numerator, value.denominator] for value in restriction],
        "defect_column": [[value.numerator, value.denominator] for value in defect],
        "repaired_tensor": serialize(repaired),
        "interpretation": "The first frozen pairwise-distinct-buffer failure is exactly filled by the unique full-support cube. It is not a terminal relative-homology obstruction.",
        "claim_boundary": "Exact audit of the lexicographically first buffer failure only; the remaining four require full enumeration and replay.",
    }
    path = OUT / "terminal-audit.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: result[key] for key in ("status", "classification", "types", "supports", "forbidden_cells", "cube_alternatives")}, sort_keys=True))


if __name__ == "__main__":
    main()
