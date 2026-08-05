#!/usr/bin/env python3
"""Classify whether C67 depth-capped simplex cells meet their equality strata."""

from __future__ import annotations

import csv
import itertools
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle67-boundary-positivity/bernstein"

CONSTRAINTS = {
    "cycle_equal": ((0,1,-1,0,0),(0,1,0,-1,0)),
    "cycle_zero": ((0,1,-1,0,0),(0,1,0,-1,0),(0,0,0,0,1)),
    "trans_equal": ((0,1,-2,0,0),(0,0,0,1,-1)),
    "trans_zero": ((0,1,0,0,0),(0,0,1,0,0),(0,0,0,1,-1)),
}


def solve_full_column_rank(matrix, rhs):
    rows = [[Fraction(value) for value in row] + [Fraction(target)]
            for row, target in zip(matrix, rhs)]
    columns = len(matrix[0])
    pivot_row = 0
    pivots = []
    for column in range(columns):
        selected = next((r for r in range(pivot_row, len(rows)) if rows[r][column]), None)
        if selected is None:
            return None
        rows[pivot_row], rows[selected] = rows[selected], rows[pivot_row]
        pivot = rows[pivot_row][column]
        rows[pivot_row] = [value/pivot for value in rows[pivot_row]]
        for r in range(len(rows)):
            if r != pivot_row and rows[r][column]:
                scale = rows[r][column]
                rows[r] = [a-scale*b for a,b in zip(rows[r], rows[pivot_row])]
        pivots.append(column)
        pivot_row += 1
    for row in rows:
        if all(not row[column] for column in range(columns)) and row[-1]:
            return None
    return [rows[index][-1] for index in range(columns)]


def intersects(vertices, constraints):
    images = [[sum(a*z for a,z in zip(row, vertex)) for row in constraints]
              for vertex in vertices]
    dimension = len(constraints)
    for size in range(1, dimension+2):
        for chosen in itertools.combinations(range(5), size):
            matrix = [[1 for _ in chosen]]
            matrix += [[images[index][coordinate] for index in chosen]
                       for coordinate in range(dimension)]
            solution = solve_full_column_rank(matrix, [1]+[0]*dimension)
            if solution is not None and all(value >= 0 for value in solution):
                return True
    return False


def main() -> int:
    result = {"status":"PASS","epistemic_status":"PROVED","families":{}}
    for name, constraints in CONSTRAINTS.items():
        with (OUT/f"{name}-unresolved.tsv").open(newline="",encoding="utf-8") as handle:
            rows=list(csv.DictReader(handle,delimiter="\t"))
        meeting=0
        for row in rows:
            vertices=[]
            for v in range(5):
                vertices.append(tuple(int(row[f"v{v}z{k}"]) for k in range(5)))
            meeting += intersects(vertices,constraints)
        result["families"][name]={
            "unresolved_cells":len(rows),
            "intersect_equality_stratum":meeting,
            "disjoint_from_equality_stratum":len(rows)-meeting,
        }
    result["claim_boundary"]=(
        "Exact intersection classification of depth-capped cells; cells meeting "
        "equality include neighborhoods and are not positivity certificates."
    )
    (OUT/"equality-intersection-summary.json").write_text(
        json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
