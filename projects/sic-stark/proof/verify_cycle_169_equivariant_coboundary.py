#!/usr/bin/env python3
"""Exact Cycle-169 normalized T-invariant coboundary test over C6."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from verify_cycle_166_fibre_torsor import build_payload as build_torsor_payload, shintani_step

MODULUS = 6
ANCHORS = ((3, 5), (3, 4))

def add(x, y): return ((x[0] + y[0]) % MODULUS, (x[1] + y[1]) % MODULUS)

def solve_field(rows, width, prime):
    matrix = [[value % prime for value in row] for row in rows]
    pivots = []
    pivot_row = 0
    for column in range(width):
        found = next((r for r in range(pivot_row, len(matrix)) if matrix[r][column]), None)
        if found is None:
            continue
        matrix[pivot_row], matrix[found] = matrix[found], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], -1, prime)
        matrix[pivot_row] = [(value * inverse) % prime for value in matrix[pivot_row]]
        for r in range(len(matrix)):
            if r != pivot_row and matrix[r][column]:
                factor = matrix[r][column]
                matrix[r] = [(value - factor * base) % prime for value, base in zip(matrix[r], matrix[pivot_row], strict=True)]
        pivots.append(column)
        pivot_row += 1
    inconsistent = any(all(value == 0 for value in row[:width]) and row[width] for row in matrix)
    solution = None
    if not inconsistent:
        solution = [0] * width
        for row, column in enumerate(pivots): solution[column] = matrix[row][width]
    return {"rank": len(pivots), "inconsistent": inconsistent, "solution": solution}

def build_payload():
    torsor = build_torsor_payload()
    rows = torsor["multiplier_rows"]
    points = sorted(tuple(row["characteristic"]) for row in rows)
    index = {point: i for i, point in enumerate(points)}
    graph = {}
    for orbit in torsor["transport_orbits"]:
        graph.update({tuple(point): label for point, label in zip(orbit["orbit"], orbit["lift_labels"], strict=True)})
    equations = []
    def equation(entries, rhs):
        row = [0] * (len(points) + 1)
        for point, coefficient in entries: row[index[point]] += coefficient
        row[-1] = rhs
        equations.append(row)
    zero = (0, 0)
    equation(((zero, 1),), 0)
    for point in points: equation(((shintani_step(point), 1), (point, -1)), 0)
    for point in ANCHORS: equation(((point, 1),), 0)
    defects = []
    for left in points:
        for right in points:
            total = add(left, right)
            defect = (graph[total] - graph[left] - graph[right]) % MODULUS
            equation(((total, 1), (left, -1), (right, -1)), defect)
            defects.append(defect)
    field_two = solve_field(equations, len(points), 2)
    field_three = solve_field(equations, len(points), 3)
    c6_solution = None
    verified = False
    if not field_two["inconsistent"] and not field_three["inconsistent"]:
        c6_solution = [next(value for value in range(6) if value % 2 == field_two["solution"][i] and value % 3 == field_three["solution"][i]) for i in range(len(points))]
        verified = all(sum(coefficient * c6_solution[index[point]] for point, coefficient in ((points[i], row[i]) for i in range(len(points)) if row[i])) % 6 == row[-1] % 6 for row in equations)
    return {"schema": "sic-stark-cycle-169-equivariant-coboundary-prototype-v1", "epistemic_status": "PROVED", "claim_boundary": "This exact finite result concerns only the normalized T-invariant action-groupoid coboundary quotient of the Cycle-166 graph defect. It defines no coefficient-to-logarithm operation, AFK interface, Stark identity, fusion theorem, or TCC identity.", "summary": {"states": len(points), "defect_equations": len(defects), "total_equations": len(equations), "defect_nonzero_count": sum(value != 0 for value in defects), "f2_rank": field_two["rank"], "f3_rank": field_three["rank"], "f2_inconsistent": field_two["inconsistent"], "f3_inconsistent": field_three["inconsistent"], "normalized_t_invariant_coboundary_exists": verified}, "f2_solution": field_two["solution"], "f3_solution": field_three["solution"], "c6_solution": c6_solution, "gate_outcome": {"equivariant_coboundary": "SURVIVES_EXACT_FINITE_TEST" if verified else "NONTRIVIAL_NORMALIZED_T_INVARIANT_CLASS", "scope": "normalized T-invariant 1-cochains on the fixed finite action groupoid"}}

def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--output", type=Path); args = parser.parse_args()
    encoded = json.dumps(build_payload(), indent=2, sort_keys=True) + "\n"
    if args.output: args.output.write_text(encoded)
    else: print(encoded, end="")

if __name__ == "__main__": main()
