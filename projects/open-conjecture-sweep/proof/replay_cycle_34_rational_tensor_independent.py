#!/usr/bin/env python3
"""Independent direct-set replay of Cycle 34's integer certificate."""
from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "discovery/out/cycle34-rational-tensor/result.json"
OUTPUT = ROOT / "discovery/out/cycle34-rational-tensor/independent-replay.json"
Q = 2786
VARIABLES = 1394
EXPECTED_HASH = "de06f7bea5bf1673f5a31d2febcac3e130fd67f5bf1ed6112e237b76a0cf5f84"


def covered_points(k: int, q: int, speed: int) -> set[int]:
    return {point for point in range(q) if (k + 1) * min(speed * point % q, (-speed * point) % q) < q}


def frozen_base() -> tuple[int, ...]:
    line = (ROOT / "discovery/out/cycle8-p199-strata.txt").read_text(encoding="utf-8").splitlines()[4]
    return tuple(map(int, line.split()))


def requirement(pair: tuple[int, int]) -> dict[int, bool]:
    return {coordinate: coordinate not in pair for coordinate in range(pair[1] + 1)}


def allowed_digits(base: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    pairs = list(itertools.combinations(range(13), 2))
    req2, req7 = requirement(pairs[1]), requirement(pairs[0])
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


def frozen_assignments(digit_rows: tuple[tuple[int, ...], ...]) -> list[tuple[int, ...]]:
    baseline = (0,) * 13
    rows = [baseline]
    seen = {baseline}
    for coordinate, digits in enumerate(digit_rows):
        for offset in range(len(digits)):
            candidate = [0] * 13
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


def independent_matrix() -> tuple[list[tuple[int, ...]], list[set[int]]]:
    base = frozen_base()
    digit_rows = allowed_digits(base)
    representatives = tuple(point for point in range(Q) if point <= (-point) % Q)
    if len(representatives) != VARIABLES:
        raise AssertionError("predicate count")
    option_uncovered: list[list[set[int]]] = []
    for coordinate, digits in enumerate(digit_rows):
        coordinate_options = []
        for digit in digits:
            covered = covered_points(13, Q, base[coordinate] + 199 * digit)
            if any((point in covered) != ((-point % Q) in covered) for point in representatives):
                raise AssertionError("negation invariance")
            coordinate_options.append({index for index, point in enumerate(representatives) if point not in covered})
        option_uncovered.append(coordinate_options)
    assignments = frozen_assignments(digit_rows)
    rows = []
    for assignment in assignments:
        uncovered = set(range(VARIABLES))
        for coordinate, offset in enumerate(assignment):
            uncovered.intersection_update(option_uncovered[coordinate][offset])
        rows.append(uncovered)
    return assignments, rows


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    outcome = source["outcome"]
    if source["status"] != "PASS" or outcome["status"] != "PROVED_RATIONAL_INCONSISTENCY":
        raise AssertionError("primary terminal status")
    assignments, rows = independent_matrix()
    assignment_hash = hashlib.sha256(b"".join(bytes(row) for row in assignments)).hexdigest()
    if assignment_hash != source["assignment_hash"] or assignment_hash != EXPECTED_HASH:
        raise AssertionError("assignment hash")

    terms = outcome["certificate_terms"]
    if len(terms) != 1229:
        raise AssertionError("certificate support")
    indices = [int(term["row_index"]) for term in terms]
    coefficients = [int(term["coefficient"]) for term in terms]
    if len(set(indices)) != len(indices) or min(indices) < 0 or max(indices) >= len(rows):
        raise AssertionError("certificate row indices")
    if indices[-1] != outcome["target_row"] or coefficients[0] <= 0:
        raise AssertionError("certificate ordering/normalization")
    divisor = 0
    for coefficient in coefficients:
        divisor = math.gcd(divisor, abs(coefficient))
    if divisor != 1:
        raise AssertionError("certificate is not primitive")

    column_sums = [0] * VARIABLES
    rhs_sum = 0
    for row_index, coefficient in zip(indices, coefficients):
        rhs_sum += coefficient
        for column in rows[row_index]:
            column_sums[column] += coefficient
    nonzero_columns = [index for index, value in enumerate(column_sums) if value]
    if nonzero_columns or rhs_sum == 0 or str(rhs_sum) != outcome["certificate_rhs"]:
        raise AssertionError("integer left-null replay")
    max_height = max(abs(value).bit_length() for value in coefficients)
    if max_height > outcome["height_bits"] or outcome["height_bits"] != 2807:
        raise AssertionError("certificate height")

    audit_prime = 2147483647
    modular_rhs = sum(value % audit_prime for value in coefficients) % audit_prime
    modular_columns = [0] * VARIABLES
    for row_index, coefficient in zip(indices, coefficients):
        residue = coefficient % audit_prime
        for column in rows[row_index]:
            modular_columns[column] = (modular_columns[column] + residue) % audit_prime
    if any(modular_columns) or modular_rhs != rhs_sum % audit_prime:
        raise AssertionError("supplementary audit-prime replay")

    result = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "assignment_hash": assignment_hash,
        "assignments": len(assignments),
        "predicate_columns": VARIABLES,
        "certificate_terms": len(terms),
        "primitive_gcd": divisor,
        "integer_predicate_sum": "ZERO",
        "integer_rhs_nonzero": True,
        "integer_rhs": str(rhs_sum),
        "max_coefficient_height_bits": max_height,
        "audit_prime": audit_prime,
        "audit_prime_predicate_sum": "ZERO",
    }
    temporary = OUTPUT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUTPUT)
    print(json.dumps({"status": "PASS", "certificate_terms": len(terms), "integer_predicate_sum": "ZERO", "integer_rhs_nonzero": True, "max_height_bits": max_height}, sort_keys=True))


if __name__ == "__main__":
    main()
