#!/usr/bin/env python3
"""Cycle 40: exact signed ownership moment construction and completion test."""
from __future__ import annotations

from collections import defaultdict, deque
from fractions import Fraction
import itertools
import json
import math
import multiprocessing
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_ownership_functional as c38

OUT = ROOT / "discovery/out/cycle40-signed-moments"
EQUATION_CAP = 1_000_000
CLASS_CAP = 1_000_000
WALL_CAP = 1800
_TYPE_ID = {}
_TYPE_MASKS = []


def coordinate_classes(coordinate: int) -> dict[str, object]:
    resource.setrlimit(resource.RLIMIT_AS, (1_258_291_200, 1_258_291_200))
    rank_two = set()
    rank_three_masks = set()
    induced_pair_deletions = set()
    binary_triples = set()
    rank_two_tuples = rank_three_tuples = 0
    patterns = sorted(c38._COORDINATES[coordinate]["patterns"], key=lambda row: (row["rank"], row["signatures"]))
    for pattern in patterns:
        rank = int(pattern["rank"])
        if rank not in (2, 3):
            continue
        groups = [c38._TYPE_ROWS[coordinate][int(signature)] for signature in pattern["signatures"]]
        for type_rows in itertools.product(*groups):
            ids = tuple(_TYPE_ID[row[0]] for row in type_rows)
            if rank == 2:
                rank_two_tuples += 1
                rank_two.add(tuple(sorted(ids)))
            else:
                rank_three_tuples += 1
                masks = tuple(_TYPE_MASKS[index] for index in ids)
                rank_three_masks.add(tuple(sorted(masks)))
                if not triple_kernel_surjective(tuple(sorted(masks))):
                    for singleton_index, mask in enumerate(masks):
                        if mask == 1 << coordinate:
                            other = tuple(sorted(ids[index] for index in range(3) if index != singleton_index))
                            induced_pair_deletions.add(other)
                    if masks[0] == masks[1] == masks[2] and masks[0].bit_count() == 2:
                        binary_triples.add(tuple(sorted(ids)))
    return {"coordinate": coordinate, "rank_two_tuples": rank_two_tuples, "rank_three_tuples": rank_three_tuples, "rank_two_pairs": sorted(rank_two), "rank_three_mask_classes": sorted(rank_three_masks), "induced_pair_deletions": sorted(induced_pair_deletions), "binary_triples": sorted(binary_triples)}


def graph_components(left_mask: int, right_mask: int, deleted_diagonal: int):
    vertices = [index for index in range(13) if left_mask & (1 << index)] + [13 + index for index in range(13) if right_mask & (1 << index)]
    adjacency = {vertex: [] for vertex in vertices}
    for left in range(13):
        if not left_mask & (1 << left):
            continue
        for right in range(13):
            if not right_mask & (1 << right) or (left == right and deleted_diagonal & (1 << left)):
                continue
            adjacency[left].append(13 + right)
            adjacency[13 + right].append(left)
    components = []
    unseen = set(vertices)
    while unseen:
        start = min(unseen)
        queue = deque([start])
        unseen.remove(start)
        component = []
        while queue:
            vertex = queue.popleft()
            component.append(vertex)
            for neighbor in adjacency[vertex]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    queue.append(neighbor)
        components.append(tuple(sorted(component)))
    return tuple(sorted(components)), adjacency


def canonical_equation(coefficients: dict[int, int], rhs: int):
    items = tuple(sorted((index, value) for index, value in coefficients.items() if value))
    if not items:
        return items, rhs
    if items[0][1] < 0:
        items = tuple((index, -value) for index, value in items)
        rhs = -rhs
    divisor = math.gcd(abs(rhs), *(abs(value) for _, value in items))
    return tuple((index, value // divisor) for index, value in items), rhs // divisor


def sparse_solve(equations, variable_count: int):
    basis = {}
    for equation_index, (items, rhs) in enumerate(equations):
        row = {index: Fraction(value) for index, value in items}
        value = Fraction(rhs)
        while row:
            pivot = min(row)
            if pivot not in basis:
                scale = row[pivot]
                row = {index: coefficient / scale for index, coefficient in row.items()}
                value /= scale
                basis[pivot] = (row, value, equation_index)
                break
            base_row, base_value, _source = basis[pivot]
            factor = row[pivot]
            for index, coefficient in base_row.items():
                row[index] = row.get(index, Fraction(0)) - factor * coefficient
                if not row[index]:
                    del row[index]
            value -= factor * base_value
        else:
            if value:
                return {"status": "INCONSISTENT", "rank": len(basis), "failed_equation": equation_index}
    solution = [Fraction(0)] * variable_count
    for pivot in sorted(basis, reverse=True):
        row, rhs, _source = basis[pivot]
        solution[pivot] = rhs - sum(coefficient * solution[index] for index, coefficient in row.items() if index != pivot)
    for items, rhs in equations:
        if sum(Fraction(value) * solution[index] for index, value in items) != rhs:
            raise AssertionError("sparse singleton replay")
    return {"status": "CONSISTENT", "rank": len(basis), "solution": solution}


def triple_kernel_surjective(masks: tuple[int, int, int]) -> bool:
    intersection = masks[0] & masks[1] & masks[2]
    if not intersection:
        return True
    sizes = [mask.bit_count() for mask in masks]
    if min(sizes) == 1:
        return False
    if intersection.bit_count() == 2 and masks[0] == masks[1] == masks[2] == intersection:
        return False
    return True


def main() -> None:
    global _TYPE_ID, _TYPE_MASKS
    OUT.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    interface = c38.prepare()
    complete_types = sorted({row[0] for root in c38._TYPE_ROWS for rows in root.values() for row in rows})
    _TYPE_ID = {value: index for index, value in enumerate(complete_types)}
    _TYPE_MASKS = [sum(1 << coordinate for coordinate, signature in enumerate(value) if signature) for value in complete_types]
    if len(complete_types) != 1318 or min(mask.bit_count() for mask in _TYPE_MASKS) < 1:
        raise AssertionError("complete owner supports")

    with multiprocessing.Pool(3) as pool:
        coordinate_rows = pool.map(coordinate_classes, range(13), chunksize=1)
    if sum(row["rank_two_tuples"] for row in coordinate_rows) != 6_684_938 or sum(row["rank_three_tuples"] for row in coordinate_rows) != 19_661_454:
        raise AssertionError("type tuple census")
    pair_deleted = defaultdict(int)
    triple_classes = set()
    induced_pair_deletions = defaultdict(int)
    binary_triples = set()
    for row in coordinate_rows:
        coordinate = int(row["coordinate"])
        for pair in row["rank_two_pairs"]:
            pair_deleted[tuple(pair)] |= 1 << coordinate
        triple_classes.update(tuple(values) for values in row["rank_three_mask_classes"])
        for pair in row["induced_pair_deletions"]:
            induced_pair_deletions[tuple(pair)] |= 1 << coordinate
            pair_deleted[tuple(pair)] |= 1 << coordinate
        binary_triples.update(tuple(values) for values in row["binary_triples"])
    if len(pair_deleted) > CLASS_CAP or len(triple_classes) > CLASS_CAP:
        raise RuntimeError("class cap")

    variables = {}
    for type_id, mask in enumerate(_TYPE_MASKS):
        for owner in range(13):
            if mask & (1 << owner):
                variables[(type_id, owner)] = len(variables)
    equation_set = set()
    equations = []
    for type_id, mask in enumerate(_TYPE_MASKS):
        coefficients = {variables[(type_id, owner)]: 1 for owner in range(13) if mask & (1 << owner)}
        equation = canonical_equation(coefficients, 1)
        equation_set.add(equation)
        equations.append(equation)

    disconnected_pairs = 0
    graph_class_counts = defaultdict(int)
    first_disconnected = None
    for (left, right), deleted in sorted(pair_deleted.items()):
        components, _adjacency = graph_components(_TYPE_MASKS[left], _TYPE_MASKS[right], deleted)
        graph_class_counts[(_TYPE_MASKS[left], _TYPE_MASKS[right], deleted, components)] += 1
        if len(components) == 1:
            continue
        disconnected_pairs += 1
        if first_disconnected is None:
            first_disconnected = {"left_type": left, "right_type": right, "left_owner_mask": _TYPE_MASKS[left], "right_owner_mask": _TYPE_MASKS[right], "deleted_diagonal": deleted, "components": [list(row) for row in components]}
        for component in components:
            coefficients = {}
            for vertex in component:
                if vertex < 13:
                    index = variables[(left, vertex)]
                    coefficients[index] = coefficients.get(index, 0) + 1
                else:
                    index = variables[(right, vertex - 13)]
                    coefficients[index] = coefficients.get(index, 0) - 1
            equation = canonical_equation(coefficients, 0)
            if equation not in equation_set:
                equation_set.add(equation)
                equations.append(equation)
                if len(equations) > EQUATION_CAP:
                    raise RuntimeError("equation cap")

    uniform = [Fraction(0)] * len(variables)
    for type_id, mask in enumerate(_TYPE_MASKS):
        value = Fraction(1, mask.bit_count())
        for owner in range(13):
            if mask & (1 << owner):
                uniform[variables[(type_id, owner)]] = value
    uniform_failures = sum(1 for items, rhs in equations if sum(Fraction(value) * uniform[index] for index, value in items) != rhs)
    if uniform_failures:
        solved = sparse_solve(equations, len(variables))
        if solved["status"] != "CONSISTENT":
            singleton = {"status": "INCONSISTENT", "rank": solved["rank"], "failed_equation": solved["failed_equation"]}
            solution = None
        else:
            solution = solved["solution"]
            singleton = {"status": "CONSISTENT", "selection": "SPARSE_EXACT", "rank": solved["rank"], "nonzero_variables": sum(bool(value) for value in solution), "maximum_numerator_bits": max(abs(value.numerator).bit_length() for value in solution), "maximum_denominator_bits": max(value.denominator.bit_length() for value in solution)}
    else:
        solution = uniform
        singleton = {"status": "CONSISTENT", "selection": "UNIFORM_ON_ALLOWED", "rank": None, "nonzero_variables": sum(bool(value) for value in solution), "maximum_numerator_bits": 1, "maximum_denominator_bits": max(value.denominator.bit_length() for value in solution)}

    failing_triples = [values for values in sorted(triple_classes) if not triple_kernel_surjective(values)]
    unresolved_kernel_classes = [values for values in failing_triples if values[0] == values[1] == values[2] and values[0].bit_count() == 2]
    triple = {"classes": len(triple_classes), "surjective_classes": len(triple_classes) - len(failing_triples), "initial_failing_classes": len(failing_triples), "first_failing_class": list(failing_triples[0]) if failing_triples else None, "induced_pair_deletion_classes": len(induced_pair_deletions), "binary_triple_type_classes": len(binary_triples), "unresolved_kernel_mask_classes_after_induced_pair_zeros": len(unresolved_kernel_classes), "unresolved_kernel_mask_classes": [list(row) for row in unresolved_kernel_classes]}
    if solution is None:
        status = "PAIR_INCONSISTENT"
        epistemic = "PROVED"
    elif binary_triples:
        status = "PAIR_FEASIBLE_BINARY_TRIPLE_EQUATIONS_OPEN"
        epistemic = "PROVED"
    else:
        status = "COMPLETE_MOMENT_CONSTRUCTION"
        epistemic = "PROVED"
    serialized_marginals = None if solution is None else [
        [[owner, solution[variables[(type_id, owner)]].numerator, solution[variables[(type_id, owner)]].denominator] for owner in range(13) if (type_id, owner) in variables and solution[variables[(type_id, owner)]]]
        for type_id in range(len(complete_types))
    ]
    result = {
        "status": "PASS",
        "epistemic_status": epistemic,
        "outcome": status,
        "interface": interface,
        "complete_types": len(complete_types),
        "owner_mask_classes": len(set(_TYPE_MASKS)),
        "minimum_allowed_owners": min(mask.bit_count() for mask in _TYPE_MASKS),
        "singleton_variables": len(variables),
        "rank_two_pair_classes": len(pair_deleted),
        "disconnected_pair_classes": disconnected_pairs,
        "deduplicated_graph_classes": len(graph_class_counts),
        "deduplicated_component_equations": len(equations),
        "uniform_component_failures": uniform_failures,
        "first_disconnected_pair": first_disconnected,
        "singleton_system": singleton,
        "singleton_marginals_by_complete_type": serialized_marginals,
        "triple_completion": triple,
        "rank_two_type_tuples": 6_684_938,
        "rank_three_type_tuples": 19_661_454,
        "wall_seconds": time.monotonic() - started,
    }
    temporary = OUT / "result.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "result.json")
    print(json.dumps({"status": "PASS", "outcome": status, "pair_classes": len(pair_deleted), "equations": len(equations), "uniform_failures": uniform_failures, "triple_classes": len(triple_classes), "initial_triple_failures": len(failing_triples), "induced_pair_deletions": len(induced_pair_deletions), "binary_triples": len(binary_triples), "wall_seconds": result["wall_seconds"]}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
