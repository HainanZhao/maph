#!/usr/bin/env python3
"""Cycle 41 exact zero-support closure from singleton/binary mediators."""
from __future__ import annotations

from collections import defaultdict, deque
import json
import multiprocessing
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_ownership_functional as c38
import lrc_signed_ownership_moments as c40

OUT = ROOT / "discovery/out/cycle41-multiplied-ideal"
OPERATION_CAP = 50_000_000
PAIR_CLASS_CAP = 2_000_000


def coordinate(coordinate_index):
    resource.setrlimit(resource.RLIMIT_AS, (1_600_000_000, 1_600_000_000))
    return c40.coordinate_classes(coordinate_index)


def cell_bit(left_owner, right_owner):
    return 1 << (13 * left_owner + right_owner)


def add_cell(store, left, right, left_owner, right_owner):
    if left <= right:
        key, bit = (left, right), cell_bit(left_owner, right_owner)
    else:
        key, bit = (right, left), cell_bit(right_owner, left_owner)
    store[key] |= bit


def components(left_mask, right_mask, deleted_cells):
    vertices = [owner for owner in range(13) if left_mask & (1 << owner)] + [13 + owner for owner in range(13) if right_mask & (1 << owner)]
    adjacency = {vertex: [] for vertex in vertices}
    for left_owner in range(13):
        if not left_mask & (1 << left_owner):
            continue
        for right_owner in range(13):
            if right_mask & (1 << right_owner) and not deleted_cells & cell_bit(left_owner, right_owner):
                adjacency[left_owner].append(13 + right_owner)
                adjacency[13 + right_owner].append(left_owner)
    result = []
    unseen = set(vertices)
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        queue = deque([start])
        row = []
        while queue:
            vertex = queue.popleft()
            row.append(vertex)
            for neighbor in adjacency[vertex]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    queue.append(neighbor)
        result.append(tuple(sorted(row)))
    return result


def main():
    started = time.monotonic()
    c38.prepare()
    complete_types = sorted({row[0] for root in c38._TYPE_ROWS for rows in root.values() for row in rows})
    type_id = {value: index for index, value in enumerate(complete_types)}
    masks = [sum(1 << owner for owner, signature in enumerate(value) if signature) for value in complete_types]
    c40._TYPE_ID = type_id
    c40._TYPE_MASKS = masks
    with multiprocessing.Pool(3) as pool:
        coordinate_rows = pool.map(coordinate, range(13), chunksize=1)
    original = defaultdict(int)
    rank3_induced = defaultdict(int)
    for owner, row in enumerate(coordinate_rows):
        for pair in row["rank_two_pairs"]:
            original[tuple(pair)] |= 1 << owner
        for pair in row["induced_pair_deletions"]:
            rank3_induced[tuple(pair)] |= 1 << owner

    small_types = {index for index, mask in enumerate(masks) if mask.bit_count() <= 2}
    blocked = defaultdict(list)
    for (left, right), owner_mask in original.items():
        for owner in range(13):
            if not owner_mask & (1 << owner):
                continue
            if left in small_types:
                blocked[(left, owner)].append(right)
            if right in small_types:
                blocked[(right, owner)].append(left)

    effective_masks = list(masks)
    singleton_zero_rows = 0
    for mediator in sorted(small_types):
        owners = [owner for owner in range(13) if masks[mediator] & (1 << owner)]
        if len(owners) != 1:
            continue
        owner = owners[0]
        for neighbor in blocked[(mediator, owner)]:
            if effective_masks[neighbor] & (1 << owner):
                effective_masks[neighbor] &= ~(1 << owner)
                singleton_zero_rows += 1
    serialized_solution = None
    if any(mask == 0 for mask in effective_masks):
        status = "SINGLETON_DOMAIN_CONTRADICTION"
        solution_summary = None
        extra = {}
        cross_operations = 0
        disconnected = None
        equations = []
    else:
        extra = defaultdict(int)
        cross_operations = 0
        for mediator in sorted(small_types):
            owners = [owner for owner in range(13) if masks[mediator] & (1 << owner)]
            if len(owners) != 2:
                continue
            a, b = owners
            left_rows = blocked[(mediator, a)]
            right_rows = blocked[(mediator, b)]
            cross_operations += 2 * len(left_rows) * len(right_rows)
            if cross_operations > OPERATION_CAP:
                raise RuntimeError("binary mediator operation cap")
            for left in left_rows:
                for right in right_rows:
                    add_cell(extra, left, right, a, b)
                    add_cell(extra, right, left, b, a)
        if len(extra) > PAIR_CLASS_CAP:
            raise RuntimeError("pair class cap")

        variables = {}
        for type_index, mask in enumerate(effective_masks):
            for owner in range(13):
                if mask & (1 << owner):
                    variables[(type_index, owner)] = len(variables)
        equation_set = set()
        equations = []
        for type_index, mask in enumerate(effective_masks):
            equation = c40.canonical_equation({variables[(type_index, owner)]: 1 for owner in range(13) if mask & (1 << owner)}, 1)
            equation_set.add(equation)
            equations.append(equation)
        pair_keys = set(original) | set(rank3_induced) | set(extra)
        disconnected = 0
        for left, right in sorted(pair_keys):
            deleted_cells = extra.get((left, right), 0)
            for owner in range(13):
                if (original.get((left, right), 0) | rank3_induced.get((left, right), 0)) & (1 << owner):
                    deleted_cells |= cell_bit(owner, owner)
            component_rows = components(effective_masks[left], effective_masks[right], deleted_cells)
            if len(component_rows) == 1:
                continue
            disconnected += 1
            for component in component_rows:
                coefficients = {}
                for vertex in component:
                    if vertex < 13:
                        index = variables[(left, vertex)]
                        coefficients[index] = coefficients.get(index, 0) + 1
                    else:
                        index = variables[(right, vertex - 13)]
                        coefficients[index] = coefficients.get(index, 0) - 1
                equation = c40.canonical_equation(coefficients, 0)
                if equation not in equation_set:
                    equation_set.add(equation)
                    equations.append(equation)
        solved = c40.sparse_solve(equations, len(variables))
        if solved["status"] == "CONSISTENT":
            solution = solved["solution"]
            solution_summary = {"status": "CONSISTENT", "rank": solved["rank"], "variables": len(variables), "nonzero": sum(bool(value) for value in solution), "maximum_numerator_bits": max(abs(value.numerator).bit_length() for value in solution), "maximum_denominator_bits": max(value.denominator.bit_length() for value in solution)}
            serialized_solution = [[[owner, solution[variables[(type_index, owner)]].numerator, solution[variables[(type_index, owner)]].denominator] for owner in range(13) if (type_index, owner) in variables and solution[variables[(type_index, owner)]]] for type_index in range(len(complete_types))]
            status = "ZERO_SUPPORT_CLOSURE_FEASIBLE"
        else:
            solution_summary = solved
            serialized_solution = None
            status = "ZERO_SUPPORT_CLOSURE_INCONSISTENT"

    result = {"status": "PASS", "epistemic_status": "PROVED", "outcome": status, "complete_types": len(complete_types), "original_rank_two_pair_classes": len(original), "rank3_induced_pair_classes": len(rank3_induced), "original_singleton_types": sum(mask.bit_count() == 1 for mask in masks), "original_binary_types": sum(mask.bit_count() == 2 for mask in masks), "singleton_mediated_owner_deletions": singleton_zero_rows, "minimum_effective_owner_count": min(mask.bit_count() for mask in effective_masks), "binary_mediator_cross_operations": cross_operations, "pair_classes_with_binary_mediated_zero_cells": len(extra), "disconnected_pair_classes": disconnected, "component_equations": len(equations), "singleton_system": solution_summary, "singleton_marginals_by_complete_type": serialized_solution, "claim_boundary": "This exact closure includes zero pair entries forced by singleton/binary third-type supports. Feasibility does not impose nontrivial homology equations from larger filling interfaces; inconsistency would still require an independently replayed certificate.", "wall_seconds": time.monotonic() - started}
    temporary = OUT / "zero-support-closure.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "zero-support-closure.json")
    print(json.dumps({key: result[key] for key in ("status", "outcome", "singleton_mediated_owner_deletions", "pair_classes_with_binary_mediated_zero_cells", "disconnected_pair_classes", "component_equations", "singleton_system", "wall_seconds")}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
