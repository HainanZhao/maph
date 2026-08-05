#!/usr/bin/env python3
"""Independent set-based witness replay and highest-pivot odd-field audit."""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import multiprocessing
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "discovery/out/cycle33-odd-tensor/result.json"
OUTPUT = ROOT / "discovery/out/cycle33-odd-tensor/independent-replay.json"
Q = 2786


def bad(speed: int) -> set[int]:
    return {point for point in range(Q) if 14 * min(speed * point % Q, (-speed * point) % Q) < Q}


def bad_h11(speed: int) -> set[int]:
    return {point for point in range(44) if 4 * min(speed * point % 44, (-speed * point) % 44) < 44}


def base4() -> tuple[int, ...]:
    return tuple(map(int, (ROOT / "discovery/out/cycle8-p199-strata.txt").read_text().splitlines()[4].split()))


def requirements(pair: tuple[int, int]) -> dict[int, bool]:
    left, right = pair
    return {coordinate: coordinate not in pair for coordinate in range(right + 1)}


def allowed(base: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    pairs = list(itertools.combinations(range(13), 2))
    req2, req7 = requirements(pairs[1]), requirements(pairs[0])
    result = []
    for coordinate, residue in enumerate(base):
        digits = []
        for digit in range(14):
            speed = (residue + 199 * digit) % 14
            if coordinate in req2 and ((speed % 2 == 0) != req2[coordinate]):
                continue
            if coordinate in req7 and ((speed % 7 == 0) != req7[coordinate]):
                continue
            digits.append(digit)
        result.append(tuple(digits))
    return tuple(result)


def assignment_rows(digit_rows: tuple[tuple[int, ...], ...]) -> list[tuple[int, ...]]:
    baseline = (0,) * 13
    rows = [baseline]
    seen = {baseline}
    for coordinate, digits in enumerate(digit_rows):
        for offset in range(len(digits)):
            candidate = list(baseline)
            candidate[coordinate] = offset
            value = tuple(candidate)
            if value not in seen:
                rows.append(value)
                seen.add(value)
    rng = random.Random(320032)
    while len(rows) < 4243:
        value = tuple(rng.randrange(len(digits)) for digits in digit_rows)
        if value not in seen:
            rows.append(value)
            seen.add(value)
    return rows


def build_rows() -> tuple[list[tuple[int, ...]], list[int], str]:
    base = base4()
    digit_rows = allowed(base)
    reps = tuple(point for point in range(Q) if point <= (-point) % Q)
    option_bad = []
    for coordinate, digits in enumerate(digit_rows):
        coordinate_rows = []
        for digit in digits:
            covered = bad(base[coordinate] + 199 * digit)
            if any((point in covered) != ((-point % Q) in covered) for point in reps):
                raise AssertionError("independent negation")
            coordinate_rows.append({index for index, point in enumerate(reps) if point not in covered})
        option_bad.append(coordinate_rows)
    assignments = assignment_rows(digit_rows)
    equations = []
    for digits in assignments:
        uncovered = set(range(len(reps)))
        for coordinate, offset in enumerate(digits):
            uncovered &= option_bad[coordinate][offset]
        equations.append(sum(1 << index for index in uncovered))
    digest = hashlib.sha256(b"".join(bytes(row) for row in assignments)).hexdigest()
    return assignments, equations, digest


def subtract(left: tuple[int, ...], right: tuple[int, ...], factor: int, field: int, mask: int) -> tuple[int, ...]:
    left_union = 0
    right_union = 0
    for plane in left:
        left_union |= plane
    for plane in right:
        right_union |= plane
    left_classes = (mask ^ left_union,) + left
    right_classes = (mask ^ right_union,) + right
    result = [0] * (field - 1)
    for a, a_bits in enumerate(left_classes):
        for b, b_bits in enumerate(right_classes):
            residue = (a - factor * b) % field
            if residue:
                result[residue - 1] |= a_bits & b_bits
    return tuple(result)


def scale(row: tuple[int, ...], factor: int, field: int) -> tuple[int, ...]:
    result = [0] * (field - 1)
    for residue, plane in enumerate(row, start=1):
        target = residue * factor % field
        if target:
            result[target - 1] |= plane
    return tuple(result)


def get(row: tuple[int, ...], position: int) -> int:
    bit = 1 << position
    return next((residue for residue, plane in enumerate(row, start=1) if plane & bit), 0)


def highest_elimination(job: tuple[int, list[int]]) -> dict[str, int | str]:
    field, equations = job
    variables = 1394
    mask = (1 << (variables + 1)) - 1
    coefficient_mask = (1 << variables) - 1
    basis = {}
    reductions = 0
    for coefficients in reversed(equations):
        row = (coefficients | (1 << variables),) + (0,) * (field - 2)
        while True:
            support = 0
            for plane in row:
                support |= plane & coefficient_mask
            if not support:
                if get(row, variables):
                    return {"field": field, "status": "INCONSISTENT", "rank_before_contradiction": len(basis), "reductions": reductions}
                break
            pivot = support.bit_length() - 1
            factor = get(row, pivot)
            if pivot not in basis:
                basis[pivot] = scale(row, pow(factor, -1, field), field)
                break
            row = subtract(row, basis[pivot], factor, field, mask)
            reductions += 1
    return {"field": field, "status": "CONSISTENT", "rank": len(basis), "reductions": reductions}


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    assignments, equations, digest = build_rows()
    if digest != source["assignment_hash"] or len(assignments) != 4243:
        raise AssertionError("independent assignment rows")
    field_results = []
    lookup = {row: index for index, row in enumerate(assignments)}
    for field_row in source["fields"]:
        field = field_row["field"]
        sums = [0] * 1394
        rhs = 0
        terms = field_row["contradiction_terms"]
        for term in terms:
            assignment = tuple(term["assignment"])
            coefficient = term["coefficient"]
            if assignment not in lookup or not 0 < coefficient < field:
                raise AssertionError("independent provenance term")
            rhs = (rhs + coefficient) % field
            bits = equations[lookup[assignment]]
            while bits:
                bit = bits & -bits
                index = bit.bit_length() - 1
                sums[index] = (sums[index] + coefficient) % field
                bits ^= bit
        if rhs != 1 or any(sums):
            raise AssertionError("independent left-null replay")
        field_results.append({"field": field, "contradiction_size": len(terms), "predicate_sum": "ZERO", "rhs_sum": 1})
    with multiprocessing.Pool(2) as pool:
        reverse = pool.map(highest_elimination, [(field, equations) for field in (3, 5)], chunksize=1)
    if any(row["status"] != "INCONSISTENT" for row in reverse):
        raise AssertionError("independent highest-pivot elimination")
    h11_covered = [bad_h11(1 + 11 * digit) for digit in range(4)]
    if any(12 in h11_covered[digit] for digit in range(4)):
        raise AssertionError("independent H11 identity")
    result = {"status": "PASS", "epistemic_status": "PROVED", "assignment_hash": digest, "h11": {"base": [1, 1, 1], "constant_uncovered_time": 12, "fields": [3, 5]}, "fields": field_results, "highest_pivot_replays": reverse}
    temporary = OUTPUT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUTPUT)
    print(json.dumps({"status": "PASS", "fields": field_results, "highest_pivot": reverse}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
