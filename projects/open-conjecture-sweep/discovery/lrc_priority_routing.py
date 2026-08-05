#!/usr/bin/env python3
"""Cycle 39: exact CEGAR for the full priority/fallback ownership span."""
from __future__ import annotations

from collections import defaultdict
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

OUT = ROOT / "discovery/out/cycle39-priority-routing"
ROW_CAP = 512
SEPARATOR_CAP = 50_000_000
WALL_CAP = 1800
_SEPARATOR_COUNTER = None
_DEADLINE = 0.0


class Cap(Exception):
    pass


def reserve_separator() -> None:
    global _SEPARATOR_COUNTER
    with _SEPARATOR_COUNTER.get_lock():
        _SEPARATOR_COUNTER.value += 1
        if _SEPARATOR_COUNTER.value > SEPARATOR_CAP:
            raise Cap("aggregate separator moment cap")
    if time.monotonic() > _DEADLINE:
        raise Cap("aggregate wall cap")


def contractions(root: int, types: tuple[tuple[int, ...], ...]) -> tuple[list[int], list[list[int]], tuple[int, ...]]:
    rank = len(types)
    others = tuple(coordinate for coordinate in range(13) if coordinate != root)
    root_factors = []
    q = [[0] * (1 << rank) for _ in range(13)]
    for subset in range(1 << rank):
        for coordinate, normal in enumerate(c38._NORMALS):
            q[coordinate][subset] = sum(
                weight
                for option, weight in enumerate(normal)
                if all(not (types[index][coordinate] & (1 << option)) for index in range(rank) if subset & (1 << index))
            )
        root_factors.append(sum(
            weight
            for option, weight in enumerate(c38._NORMALS[root])
            if all(bool(types[index][root] & (1 << option)) != bool(subset & (1 << index)) for index in range(rank))
        ))
    return root_factors, q, others


def section_moment(root: int, types: tuple[tuple[int, ...], ...], predecessor_mask: int) -> int:
    root_factors, q, others = contractions(root, types)
    full_subset = (1 << len(types)) - 1
    total = 0
    for subset, root_factor in enumerate(root_factors):
        if not root_factor:
            continue
        value = root_factor
        for offset, coordinate in enumerate(others):
            value *= q[coordinate][full_subset if predecessor_mask & (1 << offset) else subset]
            if not value:
                break
        total += value
    return total


def candidate_moment(root: int, types: tuple[tuple[int, ...], ...], candidate: dict[int, Fraction]) -> Fraction:
    """Evaluate a sparse section mixture while reusing all local contractions."""
    root_factors, q, others = contractions(root, types)
    full_subset = (1 << len(types)) - 1
    total = Fraction(0)
    for subset, root_factor in enumerate(root_factors):
        if not root_factor:
            continue
        mixture = Fraction(0)
        for predecessor_mask, coefficient in candidate.items():
            value = 1
            for offset, coordinate in enumerate(others):
                value *= q[coordinate][full_subset if predecessor_mask & (1 << offset) else subset]
                if not value:
                    break
            mixture += coefficient * value
        total += root_factor * mixture
    return total


def complete_row(root: int, types: tuple[tuple[int, ...], ...]) -> list[int]:
    root_factors, q, others = contractions(root, types)
    full_subset = (1 << len(types)) - 1
    row = [0] * 4096
    for subset, root_factor in enumerate(root_factors):
        if not root_factor:
            continue
        values = [1]
        for coordinate in others:
            outside = q[coordinate][subset]
            inside = q[coordinate][full_subset]
            size = len(values)
            expanded = [0] * (2 * size)
            for mask, value in enumerate(values):
                expanded[mask] = value * outside
                expanded[mask + size] = value * inside
            values = expanded
        for mask, value in enumerate(values):
            row[mask] += root_factor * value
    return row


def reduce_vector(vector, basis):
    residual = [Fraction(value) for value in vector]
    combination: dict[int, Fraction] = {}
    for pivot in sorted(basis):
        factor = residual[pivot]
        if not factor:
            continue
        base_vector, base_representation = basis[pivot]
        residual = [left - factor * right for left, right in zip(residual, base_vector)]
        for column, coefficient in base_representation.items():
            combination[column] = combination.get(column, Fraction(0)) + factor * coefficient
            if not combination[column]:
                del combination[column]
    return residual, combination


def affine_candidate(rows: list[list[int]]) -> dict[int, Fraction] | None:
    dimension = len(rows) + 1
    target = [Fraction(1)] + [Fraction(0)] * len(rows)
    basis = {}
    for column in range(4096):
        vector = [Fraction(1)] + [Fraction(row[column]) for row in rows]
        residual, used = reduce_vector(vector, basis)
        if any(residual):
            pivot = next(index for index, value in enumerate(residual) if value)
            scale = residual[pivot]
            normalized = [value / scale for value in residual]
            representation = {column: Fraction(1, 1) / scale}
            for prior, coefficient in used.items():
                representation[prior] = representation.get(prior, Fraction(0)) - coefficient / scale
                if not representation[prior]:
                    del representation[prior]
            basis[pivot] = (normalized, representation)
        residual_target, target_combination = reduce_vector(target, basis)
        if not any(residual_target):
            if sum(target_combination.values(), Fraction(0)) != 1:
                raise AssertionError("candidate mass")
            for row in rows:
                if sum(coefficient * row[index] for index, coefficient in target_combination.items()):
                    raise AssertionError("candidate selected row")
            return target_combination
    return None


def modular_pivot_columns(rows: list[list[int]], prime: int) -> list[int]:
    dimension = len(rows) + 1
    basis = {}
    selected = []
    for column in range(4096):
        vector = [1] + [row[column] % prime for row in rows]
        for pivot in sorted(basis):
            factor = vector[pivot]
            if factor:
                base_vector = basis[pivot]
                vector = [(left - factor * right) % prime for left, right in zip(vector, base_vector)]
        if not any(vector):
            continue
        pivot = next(index for index, value in enumerate(vector) if value)
        inverse = pow(vector[pivot], -1, prime)
        basis[pivot] = [(value * inverse) % prime for value in vector]
        selected.append(column)
        if len(selected) == dimension:
            return selected
    return selected


def solve_selected_square(rows: list[list[int]], columns: list[int]) -> dict[int, Fraction]:
    dimension = len(rows) + 1
    if len(columns) != dimension:
        raise AssertionError("square column count")
    matrix = []
    for equation in range(dimension):
        coefficients = [1 if equation == 0 else rows[equation - 1][column] for column in columns]
        matrix.append([Fraction(value) for value in coefficients] + [Fraction(1 if equation == 0 else 0)])
    for variable in range(dimension):
        pivot = next((row for row in range(variable, dimension) if matrix[row][variable]), None)
        if pivot is None:
            raise AssertionError("modular-selected rational singularity")
        matrix[variable], matrix[pivot] = matrix[pivot], matrix[variable]
        scale = matrix[variable][variable]
        matrix[variable] = [value / scale for value in matrix[variable]]
        for row in range(dimension):
            if row == variable or not matrix[row][variable]:
                continue
            factor = matrix[row][variable]
            matrix[row] = [left - factor * right for left, right in zip(matrix[row], matrix[variable])]
    candidate = {columns[index]: matrix[index][-1] for index in range(dimension) if matrix[index][-1]}
    if sum(candidate.values(), Fraction(0)) != 1 or any(sum(value * row[column] for column, value in candidate.items()) for row in rows):
        raise AssertionError("fast candidate replay")
    return candidate


def affine_candidate_fast(rows: list[list[int]]) -> dict[int, Fraction] | None:
    dimension = len(rows) + 1
    for prime in (2147483647, 2147483629):
        columns = modular_pivot_columns(rows, prime)
        if len(columns) == dimension:
            return solve_selected_square(rows, columns)
    return affine_candidate(rows)


def integer_left_null(rows: list[list[int]]) -> list[int]:
    equation_count = len(rows) + 1
    columns = [[1] + [row[column] for row in rows] for column in range(4096)]
    matrix = [[Fraction(columns[column][equation]) for equation in range(equation_count)] for column in range(4096)]
    pivot_columns = []
    pivot_row = 0
    for variable in range(equation_count):
        pivot = next((row for row in range(pivot_row, len(matrix)) if matrix[row][variable]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][variable]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][variable]:
                continue
            factor = matrix[row][variable]
            matrix[row] = [left - factor * right for left, right in zip(matrix[row], matrix[pivot_row])]
        pivot_columns.append(variable)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    free = [index for index in range(equation_count) if index not in pivot_columns]
    candidates = []
    for free_column in free:
        vector = [Fraction(0)] * equation_count
        vector[free_column] = 1
        for row, pivot in enumerate(pivot_columns):
            vector[pivot] = -matrix[row][free_column]
        if vector[0]:
            candidates.append(vector)
    if not candidates:
        raise AssertionError("missing left-null separator")
    vector = candidates[0]
    denominator = math.lcm(*(value.denominator for value in vector))
    integers = [int(value * denominator) for value in vector]
    divisor = math.gcd(*integers)
    integers = [value // divisor for value in integers]
    if integers[0] < 0:
        integers = [-value for value in integers]
    if not integers[0] or any(integers[0] + sum(integers[index + 1] * rows[index][column] for index in range(len(rows))) for column in range(4096)):
        raise AssertionError("left-null replay")
    return integers


def iter_type_tuples(root: int, minimum_rank: int, maximum_rank: int):
    coordinate = c38._COORDINATES[root]
    patterns = sorted((row for row in coordinate["patterns"] if minimum_rank <= int(row["rank"]) <= maximum_rank), key=lambda row: (row["rank"], row["signatures"]))
    for pattern in patterns:
        signatures = tuple(map(int, pattern["signatures"]))
        groups = [c38._TYPE_ROWS[root][signature] for signature in signatures]
        for type_rows in itertools.product(*groups):
            yield {
                "rank": len(signatures),
                "signatures": signatures,
                "types": tuple(row[0] for row in type_rows),
                "multiplicity": math.prod(row[1] for row in type_rows),
                "representative_times": tuple(row[2] for row in type_rows),
            }


def serialize_witness(witness) -> dict[str, object]:
    return {"rank": witness["rank"], "signatures": list(witness["signatures"]), "global_types": [list(row) for row in witness["types"]], "multiplicity": witness["multiplicity"], "representative_times": list(witness["representative_times"])}


def deserialize_witness(row: dict[str, object]) -> dict[str, object]:
    return {"rank": int(row["rank"]), "signatures": tuple(map(int, row["signatures"])), "types": tuple(tuple(map(int, value)) for value in row["global_types"]), "multiplicity": int(row["multiplicity"]), "representative_times": tuple(map(int, row["representative_times"]))}


def write_checkpoint(root: int, witnesses: list[dict[str, object]]) -> None:
    path = OUT / f"root-{root:02d}-checkpoint.json"
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps({"root": root, "witnesses": witnesses}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def separate(root: int, candidate: dict[int, Fraction], minimum_rank: int, maximum_rank: int):
    checked = 0
    for witness in iter_type_tuples(root, minimum_rank, maximum_rank):
        reserve_separator()
        checked += 1
        value = candidate_moment(root, witness["types"], candidate)
        if value:
            return witness, value, checked
    return None, Fraction(0), checked


def process_root(root: int) -> dict[str, object]:
    c38_witness = c38._C38_RESULT["roots"][root]["first_nonzero"]
    initial = {"rank": 2, "signatures": tuple(c38_witness["signatures"]), "types": tuple(tuple(row) for row in c38_witness["global_types"]), "multiplicity": c38_witness["multiplicity"], "representative_times": tuple(c38_witness["representative_times"])}
    checkpoint_path = OUT / f"root-{root:02d}-checkpoint.json"
    if checkpoint_path.exists():
        checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
        witnesses = checkpoint["witnesses"]
        frozen_witnesses = [deserialize_witness(row) for row in witnesses]
    else:
        witnesses = [serialize_witness(initial)]
        frozen_witnesses = [initial]
        write_checkpoint(root, witnesses)
    rows = [complete_row(root, witness["types"]) for witness in frozen_witnesses]
    if rows[0][0] != int(c38_witness["moment"]):
        raise AssertionError("Cycle 38 empty-predecessor control")
    rounds = 0
    checked_total = 0
    while True:
        rounds += 1
        if len(rows) > ROW_CAP or time.monotonic() > _DEADLINE:
            raise Cap("row or wall cap")
        candidate = affine_candidate_fast(rows)
        if candidate is None:
            certificate = integer_left_null(rows)
            return {"root": root, "status": "INFEASIBLE", "rounds": rounds, "selected_rows": len(rows), "separator_type_tuples": checked_total, "witnesses": witnesses, "left_null_certificate": certificate}
        failure, value, checked = separate(root, candidate, 1, 2)
        checked_total += checked
        if failure is not None:
            rows.append(complete_row(root, failure["types"]))
            serialized = serialize_witness(failure)
            serialized["candidate_value"] = [value.numerator, value.denominator]
            witnesses.append(serialized)
            write_checkpoint(root, witnesses)
            continue
        failure, value, checked = separate(root, candidate, 3, 3)
        checked_total += checked
        if failure is not None:
            rows.append(complete_row(root, failure["types"]))
            serialized = serialize_witness(failure)
            serialized["candidate_value"] = [value.numerator, value.denominator]
            witnesses.append(serialized)
            write_checkpoint(root, witnesses)
            continue
        return {"root": root, "status": "FEASIBLE", "rounds": rounds, "selected_rows": len(rows), "separator_type_tuples": checked_total, "witnesses": witnesses, "candidate": [[column, value.numerator, value.denominator] for column, value in sorted(candidate.items())]}


def worker_init(counter, deadline) -> None:
    global _SEPARATOR_COUNTER, _DEADLINE
    _SEPARATOR_COUNTER = counter
    _DEADLINE = deadline
    resource.setrlimit(resource.RLIMIT_AS, (1_258_291_200, 1_258_291_200))


def process_root_safe(root: int) -> dict[str, object]:
    try:
        return process_root(root)
    except Cap as error:
        return {"root": root, "status": "CAP", "reason": str(error)}


def main() -> None:
    global _SEPARATOR_COUNTER, _DEADLINE
    OUT.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    c38.prepare()
    c38._C38_RESULT = json.loads((ROOT / "discovery/out/cycle38-ownership-functional/result.json").read_text(encoding="utf-8"))
    prior_result = None
    prior_path = OUT / "result.json"
    if prior_path.exists():
        prior_result = json.loads(prior_path.read_text(encoding="utf-8"))
    targets = list(range(13)) if prior_result is None or not prior_result.get("capped_roots") else list(map(int, prior_result["capped_roots"]))
    retained = {} if prior_result is None else {int(row["root"]): row for row in prior_result["roots"] if int(row["root"]) not in targets}
    prior_separator_evaluations = 0 if prior_result is None else int(prior_result.get("separator_moment_evaluations", 0))
    counter = multiprocessing.Value("q", 0)
    deadline = started + WALL_CAP
    with multiprocessing.Pool(3, initializer=worker_init, initargs=(counter, deadline)) as pool:
        resumed = pool.map(process_root_safe, targets, chunksize=1)
    for row in resumed:
        retained[int(row["root"])] = row
    roots = [retained[root] for root in range(13)]
    _SEPARATOR_COUNTER = counter
    _DEADLINE = deadline
    feasible = [row["root"] for row in roots if row["status"] == "FEASIBLE"]
    capped = [row["root"] for row in roots if row["status"] == "CAP"]
    result = {"status": "CAP" if capped else "PASS", "epistemic_status": "OBSERVED" if capped else "PROVED", "roots": roots, "feasible_roots": feasible, "capped_roots": capped, "mass_one_priority_span_extension_exists": bool(feasible) if not capped else None, "resumed_roots": targets, "separator_moment_evaluations_this_tranche": counter.value, "separator_moment_evaluations": prior_separator_evaluations + counter.value, "wall_seconds": time.monotonic() - started}
    temporary = OUT / "result.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "result.json")
    print(json.dumps({"status": result["status"], "feasible_roots": feasible, "capped_roots": capped, "selected_rows": [row.get("selected_rows") for row in roots], "separator_evaluations": counter.value, "wall_seconds": result["wall_seconds"]}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
