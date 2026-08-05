#!/usr/bin/env python3
"""Cycle 33 exact degree-zero GF(3)/GF(5) tensor elimination."""
from __future__ import annotations

import hashlib
import itertools
import json
import multiprocessing
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_gf2_tensor as source

OUT = ROOT / "discovery/out/cycle33-odd-tensor"
FIELDS = (3, 5)
EQUATION_CAP = 8192
NODE_CAP = 10_000_000
REDUCTION_CAP = 6_000_000


def value(planes: tuple[int, ...], position: int) -> int:
    bit = 1 << position
    for residue, plane in enumerate(planes, start=1):
        if plane & bit:
            return residue
    return 0


def scale(planes: tuple[int, ...], factor: int, field: int) -> tuple[int, ...]:
    result = [0] * (field - 1)
    for residue, plane in enumerate(planes, start=1):
        target = residue * factor % field
        if target:
            result[target - 1] |= plane
    return tuple(result)


def subtract(left: tuple[int, ...], right: tuple[int, ...], factor: int, field: int, full_mask: int) -> tuple[int, ...]:
    left_union = 0
    right_union = 0
    for plane in left:
        left_union |= plane
    for plane in right:
        right_union |= plane
    left_classes = (full_mask ^ left_union,) + left
    right_classes = (full_mask ^ right_union,) + right
    result = [0] * (field - 1)
    for left_value, left_plane in enumerate(left_classes):
        for right_value, right_plane in enumerate(right_classes):
            target = (left_value - factor * right_value) % field
            if target:
                result[target - 1] |= left_plane & right_plane
    return tuple(result)


def binary_row(coefficients: int, variables: int, field: int) -> tuple[int, ...]:
    return (coefficients | (1 << variables),) + (0,) * (field - 2)


def verify_combination(equations: list[int], terms: list[tuple[int, int]], variables: int, field: int) -> None:
    vector_mask = (1 << (variables + 1)) - 1
    total = (0,) * (field - 1)
    for index, coefficient in terms:
        row = binary_row(equations[index], variables, field)
        total = subtract(total, row, (-coefficient) % field, field, vector_mask)
    if value(total, variables) != 1:
        raise AssertionError("contradiction RHS normalization")
    if any(plane & ((1 << variables) - 1) for plane in total):
        raise AssertionError("contradiction predicate sum")


def eliminate(equations: list[int], variables: int, field: int) -> dict[str, object]:
    vector_mask = (1 << (variables + 1)) - 1
    provenance_mask = (1 << EQUATION_CAP) - 1
    coefficient_mask = (1 << variables) - 1
    basis: dict[int, tuple[tuple[int, ...], tuple[int, ...]]] = {}
    reductions = 0
    for index, coefficients in enumerate(equations):
        row = binary_row(coefficients, variables, field)
        provenance = ((1 << index),) + (0,) * (field - 2)
        while True:
            support = 0
            for plane in row:
                support |= plane & coefficient_mask
            if not support:
                rhs = value(row, variables)
                if rhs:
                    normalized = scale(provenance, pow(rhs, -1, field), field)
                    terms = []
                    for residue, plane in enumerate(normalized, start=1):
                        bits = plane & ((1 << len(equations)) - 1)
                        while bits:
                            bit = bits & -bits
                            terms.append((bit.bit_length() - 1, residue))
                            bits ^= bit
                    terms.sort()
                    verify_combination(equations, terms, variables, field)
                    return {"status": "INCONSISTENT", "rank": len(basis), "reductions": reductions, "contradiction_terms": terms}
                break
            pivot = (support & -support).bit_length() - 1
            pivot_value = value(row, pivot)
            if pivot not in basis:
                inverse = pow(pivot_value, -1, field)
                basis[pivot] = (scale(row, inverse, field), scale(provenance, inverse, field))
                break
            row = subtract(row, basis[pivot][0], pivot_value, field, vector_mask)
            provenance = subtract(provenance, basis[pivot][1], pivot_value, field, provenance_mask)
            reductions += 1
            if reductions > REDUCTION_CAP:
                return {"status": "CAP", "reason": "row reduction cap", "rank": len(basis), "reductions": reductions}

    solution = [0] * variables
    for pivot in sorted(basis, reverse=True):
        row = basis[pivot][0]
        total = 0
        for residue, plane in enumerate(row, start=1):
            bits = plane & coefficient_mask & ~((1 << (pivot + 1)) - 1)
            while bits:
                bit = bits & -bits
                total += residue * solution[bit.bit_length() - 1]
                bits ^= bit
        solution[pivot] = (value(row, variables) - total) % field
    for coefficients in equations:
        total = 0
        bits = coefficients
        while bits:
            bit = bits & -bits
            total += solution[bit.bit_length() - 1]
            bits ^= bit
        if total % field != 1:
            raise AssertionError("candidate equation replay")
    return {"status": "CONSISTENT", "rank": len(basis), "reductions": reductions, "solution": solution}


def tensor_counterexample(solution: list[int], bad_terms: tuple[tuple[int, ...], ...], field: int, node_state: dict[str, int]) -> tuple[int, ...] | None:
    planes = [0] * (field - 1)
    for index, coefficient in enumerate(solution):
        if coefficient:
            planes[coefficient - 1] |= 1 << index
    support = 0
    for plane in planes:
        support |= plane
    memo: set[tuple[int, int]] = set()
    coordinates = len(bad_terms)

    def weighted(active: int) -> int:
        return sum(residue * (active & plane).bit_count() for residue, plane in enumerate(planes, start=1)) % field

    def search(coordinate: int, active: int, prefix: tuple[int, ...]) -> tuple[int, ...] | None:
        node_state["nodes"] += 1
        if node_state["nodes"] > NODE_CAP:
            raise RuntimeError("tensor verifier node cap")
        if active == 0:
            return prefix + (0,) * (coordinates - coordinate)
        if coordinate == coordinates:
            return None if weighted(active) == 1 else prefix
        key = (coordinate, active)
        if key in memo:
            return None
        for digit, bad in enumerate(bad_terms[coordinate]):
            found = search(coordinate + 1, active & bad, prefix + (digit,))
            if found is not None:
                return found
        memo.add(key)
        return None

    return search(0, support, ())


def run_field(job: tuple[int, list[int], tuple[tuple[int, ...], ...], list[tuple[int, ...]], str]) -> dict[str, object]:
    field, initial_equations, option_masks, assignments, assignment_hash = job
    variables = 1394
    equations = list(initial_equations)
    rows = list(assignments)
    full = (1 << variables) - 1
    bad_terms = tuple(tuple(full ^ covered for covered in coordinate) for coordinate in option_masks)
    nodes = {"nodes": 0}
    rounds = 0
    while rounds < 64:
        rounds += 1
        outcome = eliminate(equations, variables, field)
        if outcome["status"] == "INCONSISTENT":
            terms = outcome["contradiction_terms"]
            return {
                "field": field,
                "status": "INCONSISTENT_EVALUATION_SUBSYSTEM",
                "assignment_hash": assignment_hash,
                "equations": len(equations),
                "rounds": rounds,
                "rank": outcome["rank"],
                "row_reductions": outcome["reductions"],
                "tensor_verifier_nodes": nodes["nodes"],
                "contradiction_size": len(terms),
                "contradiction_terms": [{"assignment": list(rows[index]), "coefficient": coefficient} for index, coefficient in terms],
            }
        if outcome["status"] == "CAP":
            return {"field": field, "status": "CAP", "reason": outcome["reason"], "rank": outcome["rank"], "row_reductions": outcome["reductions"], "equations": len(equations), "rounds": rounds}
        solution = outcome["solution"]
        counterexample = tensor_counterexample(solution, bad_terms, field, nodes)
        if counterexample is None:
            return {
                "field": field,
                "status": "CERTIFICATE_PENDING_INDEPENDENT_REPLAY",
                "assignment_hash": assignment_hash,
                "equations": len(equations),
                "rounds": rounds,
                "rank": outcome["rank"],
                "row_reductions": outcome["reductions"],
                "tensor_verifier_nodes": nodes["nodes"],
                "coefficients": [{"time_index": index, "coefficient": coefficient} for index, coefficient in enumerate(solution) if coefficient],
            }
        if counterexample in rows or len(equations) >= EQUATION_CAP:
            return {"field": field, "status": "CAP", "reason": "repeated counterexample or equation cap", "equations": len(equations), "rounds": rounds, "tensor_verifier_nodes": nodes["nodes"]}
        rows.append(counterexample)
        equations.append(source.equation(counterexample, option_masks, variables) & full)
    return {"field": field, "status": "CAP", "reason": "round cap", "equations": len(equations), "rounds": rounds, "tensor_verifier_nodes": nodes["nodes"]}


def h11_control() -> dict[str, object]:
    masks = [source.mask(3, 44, 1 + 11 * digit) for digit in range(4)]
    for digits in itertools.product(range(4), repeat=3):
        union = masks[digits[0]] | masks[digits[1]] | masks[digits[2]]
        if union & (1 << 12):
            raise AssertionError("H11 time 12 covered")
    return {"base": [1, 1, 1], "assignments": 64, "coefficient_time": 12, "coefficient": 1, "fields": [3, 5], "status": "PASS"}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    prepared = source.p199_prepare()
    assignments = source.initial_assignments(prepared["allowed"])
    if len(assignments) != 4243 or len(prepared["reps"]) != 1394:
        raise AssertionError("frozen row geometry")
    encoded = b"".join(bytes(row) for row in assignments)
    assignment_hash = hashlib.sha256(encoded).hexdigest()
    variables = 1394
    full = (1 << variables) - 1
    equations = [source.equation(row, prepared["option_masks"], variables) & full for row in assignments]
    jobs = [(field, equations, prepared["option_masks"], assignments, assignment_hash) for field in FIELDS]
    with multiprocessing.Pool(2) as pool:
        fields = pool.map(run_field, jobs, chunksize=1)
    result = {"status": "PASS", "epistemic_status": "OBSERVED", "assignment_hash": assignment_hash, "h11": h11_control(), "fields": fields, "wall_seconds": time.monotonic() - started}
    temporary = OUT / "result.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "result.json")
    print(json.dumps({"status": "PASS", "assignment_hash": assignment_hash, "fields": [{"field": row["field"], "status": row["status"], "rank": row.get("rank"), "contradiction_size": row.get("contradiction_size")} for row in fields], "wall_seconds": result["wall_seconds"]}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
