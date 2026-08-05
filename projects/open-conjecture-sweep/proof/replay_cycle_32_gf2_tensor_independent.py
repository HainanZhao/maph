#!/usr/bin/env python3
"""Independent exact replay of Cycle 32's GF(2) outcomes."""
from __future__ import annotations

import itertools
import json
import math
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "discovery/out/cycle32-gf2-tensor/result.json"
OUTPUT = ROOT / "discovery/out/cycle32-gf2-tensor/independent-replay.json"
Q = 2786


def bad(k: int, q: int, speed: int) -> set[int]:
    return {point for point in range(q) if (k + 1) * min(speed * point % q, (-speed * point) % q) < q}


def base4() -> tuple[int, ...]:
    return tuple(map(int, (ROOT / "discovery/out/cycle8-p199-strata.txt").read_text().splitlines()[4].split()))


def req(pair: tuple[int, int]) -> dict[int, bool]:
    left, right = pair
    return {coordinate: coordinate not in pair for coordinate in range(right + 1)}


def allowed(base: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    pairs = list(itertools.combinations(range(13), 2))
    req2, req7 = req(pairs[1]), req(pairs[0])
    rows = []
    for coordinate, residue in enumerate(base):
        values = []
        for digit in range(14):
            speed = (residue + 199 * digit) % 14
            if coordinate in req2 and ((speed % 2 == 0) != req2[coordinate]):
                continue
            if coordinate in req7 and ((speed % 7 == 0) != req7[coordinate]):
                continue
            values.append(digit)
        rows.append(tuple(values))
    return tuple(rows)


def assignments(digit_rows: tuple[tuple[int, ...], ...]) -> list[tuple[int, ...]]:
    baseline = (0,) * 13
    rows = [baseline]
    seen = {baseline}
    for coordinate, digits in enumerate(digit_rows):
        for offset in range(len(digits)):
            candidate = list(baseline)
            candidate[coordinate] = offset
            value = tuple(candidate)
            if value not in seen:
                seen.add(value)
                rows.append(value)
    rng = random.Random(320032)
    while len(rows) < 4243:
        value = tuple(rng.randrange(len(digits)) for digits in digit_rows)
        if value not in seen:
            seen.add(value)
            rows.append(value)
    return rows


def rows() -> tuple[list[tuple[int, ...]], list[int]]:
    base = base4()
    digit_rows = allowed(base)
    reps = tuple(point for point in range(Q) if point <= (-point) % Q)
    option_bad = []
    for coordinate, digits in enumerate(digit_rows):
        coordinate_rows = []
        for digit in digits:
            covered = bad(13, Q, base[coordinate] + 199 * digit)
            if any((point in covered) != ((-point % Q) in covered) for point in reps):
                raise AssertionError("independent negation")
            coordinate_rows.append({index for index, point in enumerate(reps) if point not in covered})
        option_bad.append(coordinate_rows)
    assignment_rows = assignments(digit_rows)
    equations = []
    for digits in assignment_rows:
        uncovered = set(range(len(reps)))
        for coordinate, offset in enumerate(digits):
            uncovered &= option_bad[coordinate][offset]
        equations.append(sum(1 << index for index in uncovered) | (1 << len(reps)))
    return assignment_rows, equations


def reverse_elimination(equations: list[int], variables: int) -> tuple[str, int]:
    mask = (1 << variables) - 1
    basis = {}
    for source in reversed(equations):
        row = source
        while row & mask:
            pivot = (row & mask).bit_length() - 1
            if pivot not in basis:
                basis[pivot] = row
                break
            row ^= basis[pivot]
        else:
            if row >> variables:
                return "INCONSISTENT", len(basis)
    return "CONSISTENT", len(basis)


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    h11_masks = [[bad(3, 44, 1 + 11 * digit) for digit in range(4)] for _coordinate in range(3)]
    h11_rows = []
    for digits in itertools.product(range(4), repeat=3):
        union = set().union(*(h11_masks[index][digit] for index, digit in enumerate(digits)))
        if union == set(range(44)) or 12 in union:
            raise AssertionError("independent H11 degree-zero identity")
        h11_rows.append(digits)
    if source["h11"]["selected_base"] != [1, 1, 1] or source["h11"]["coefficient_times"] != [12]:
        raise AssertionError("H11 source result")

    assignment_rows, equations = rows()
    variables = 1394
    contradiction = [tuple(row) for row in source["p199"]["contradiction_assignments"]]
    lookup = {row: index for index, row in enumerate(assignment_rows)}
    if len(contradiction) != 577 or any(row not in lookup for row in contradiction):
        raise AssertionError("independent contradiction assignments")
    xor = 0
    for row in contradiction:
        xor ^= equations[lookup[row]]
    if xor != 1 << variables:
        raise AssertionError("independent contradiction XOR")
    status, reverse_rank = reverse_elimination(equations, variables)
    if status != "INCONSISTENT":
        raise AssertionError("independent reverse elimination")
    result = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "h11": {"base": [1, 1, 1], "assignments": len(h11_rows), "constant_uncovered_time": 12, "coefficient_weight": 1},
        "p199": {"assignments": len(equations), "predicate_columns": variables, "contradiction_size": len(contradiction), "contradiction_xor": "constant_one", "reverse_elimination_status": status, "reverse_elimination_rank_before_contradiction": reverse_rank},
    }
    temporary = OUTPUT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUTPUT)
    print(json.dumps({"status": "PASS", "h11_time": 12, "p199_contradiction_size": len(contradiction), "reverse_rank": reverse_rank}, sort_keys=True))


if __name__ == "__main__":
    main()
