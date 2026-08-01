#!/usr/bin/env python3
"""Independent exact audit of the frozen d=12,f=3 flat-monoid algebra."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "discovery" / "tcc-flat-monoid-p1-overlap-adapter-v1.json"


def mul(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    # theta_3^2 - 39 theta_3 + 351 = 0 in O_3 for discriminant 13.
    a, b = x
    c, d = y
    return ((a * c - 351 * b * d) % 12, (a * d + b * c + 39 * b * d) % 12)


def parse(value: str) -> Fraction:
    return Fraction(value)


def rref(rows: list[list[Fraction]]) -> tuple[list[list[Fraction]], list[int]]:
    matrix = [row[:] for row in rows if any(row)]
    pivots: list[int] = []
    target = 0
    for column in range(len(matrix[0]) if matrix else 0):
        source = next((row for row in range(target, len(matrix)) if matrix[row][column]), None)
        if source is None:
            continue
        matrix[target], matrix[source] = matrix[source], matrix[target]
        pivot = matrix[target][column]
        matrix[target] = [entry / pivot for entry in matrix[target]]
        for row in range(len(matrix)):
            if row != target and matrix[row][column]:
                scalar = matrix[row][column]
                matrix[row] = [entry - scalar * base for entry, base in zip(matrix[row], matrix[target])]
        pivots.append(column)
        target += 1
        if target == len(matrix):
            break
    return matrix[:target], pivots


def vector_product(
    x: list[Fraction], y: list[Fraction], table: list[list[int]]
) -> list[Fraction]:
    result = [Fraction(0) for _ in x]
    for i, xi in enumerate(x):
        for j, yj in enumerate(y):
            if xi and yj:
                result[table[i][j]] += xi * yj
    return result


def main() -> None:
    payload = json.loads(ARTIFACT.read_text())
    case = payload["case"]
    if (case["delta"], case["form_conductor"], case["modulus_integer"]) != (13, 3, 12):
        raise AssertionError("frozen pilot changed")
    elements = [[tuple(point) for point in orbit] for orbit in case["elements"]]
    table = case["multiplication_table"]
    if len(elements) != 50 or len(table) != 50:
        raise AssertionError("element count changed")
    seen = {point for orbit in elements for point in orbit}
    if len(seen) != 288:
        raise AssertionError("ambient residue/sign partition changed")
    locator = {point: index for index, orbit in enumerate(elements) for point in orbit}
    if len(locator) != 288:
        raise AssertionError("orbits overlap")
    actions = [(10, 1, 1), (11, 0, -1)]  # -14 mod 12 and -1 mod 12
    for orbit in elements:
        for a, b, sign in orbit:
            for u, v, unit_sign in actions:
                product = mul((a, b), (u, v))
                if (product[0], product[1], sign * unit_sign) not in orbit:
                    raise AssertionError("unit orbit is not closed")
    for i, left in enumerate(elements):
        for j, right in enumerate(elements):
            product = mul(left[0][:2], right[0][:2])
            expected = locator[(product[0], product[1], left[0][2] * right[0][2])]
            if table[i][j] != expected:
                raise AssertionError("multiplication table disagreement")
    traces = [sum(table[row][element] == row for row in range(50)) for element in range(50)]
    gram = [[traces[table[i][j]] for j in range(50)] for i in range(50)]
    if gram != case["radical"]["trace_gram"]:
        raise AssertionError("trace gram disagreement")
    _, pivots = rref([[Fraction(entry) for entry in row] for row in gram])
    if len(pivots) != 31:
        raise AssertionError("trace rank changed")
    radical = [[parse(entry) for entry in vector] for vector in case["radical"]["basis"]]
    if len(radical) != 19:
        raise AssertionError("radical dimension changed")
    for vector in radical:
        if any(sum(Fraction(gram[row][column]) * vector[column] for column in range(50)) for row in range(50)):
            raise AssertionError("listed radical basis is not in trace kernel")
    _, radical_pivots = rref(radical)
    if len(radical_pivots) != 19:
        raise AssertionError("listed radical vectors are dependent")
    j2 = rref([vector_product(x, y, table) for x in radical for y in radical])[0]
    if len(j2) != 2:
        raise AssertionError("J squared dimension changed")
    j3 = [vector_product(x, y, table) for x in j2 for y in radical]
    if any(any(entry for entry in vector) for vector in j3):
        raise AssertionError("J cubed is nonzero")
    print("TCC_FLAT_MONOID_P1_OVERLAP_ADAPTER_AUDIT=PASS")
    print("D12_TRACE_RANK=31")
    print("D12_RADICAL_POWER_DIMENSIONS=[19,2,0]")


if __name__ == "__main__":
    main()
