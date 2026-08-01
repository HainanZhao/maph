#!/usr/bin/env python3
"""Exact flat-monoid algebra for the frozen d=7, f=2 AFK pilot.

This is deliberately limited to the class-number-one pilot.  Kopp--Lagarias
Appendix A identifies the flat monoid with residue/sign data modulo global
units in that situation; the accompanying source note gives the direct
common-factor-equivalence proof.  No partial-zeta value is evaluated here.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from math import gcd
from pathlib import Path
import time


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery" / "tcc-flat-monoid-p1-adapter-v1.json"
PREREG = ROOT / "data" / "tcc-flat-monoid-p1-preregistration-v1.json"
SOURCE_NOTE = ROOT / "docs" / "tcc-flat-monoid-p1-source-interface-v1.md"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def multiply_residue(
    left: tuple[int, int], right: tuple[int, int], delta: int, f: int, d: int
) -> tuple[int, int]:
    """Multiply in O_f/d O_f in the basis 1, theta_f."""
    a, b = left
    c, e = right
    constant = f * f * delta * (delta - 1) // 4
    trace = f * delta
    return (
        (a * c - constant * b * e) % d,
        (a * e + b * c + trace * b * e) % d,
    )


def norm_residue(value: tuple[int, int], delta: int, f: int) -> int:
    a, b = value
    constant = f * f * delta * (delta - 1) // 4
    trace = f * delta
    return a * a + trace * a * b + constant * b * b


def orbit_monoid(
    *, delta: int, f: int, d: int, unit_actions: list[tuple[int, int, int]]
) -> dict[str, object]:
    """Return the quotient of residue/sign pairs by the stated unit actions."""
    ambient = {(a, b, sign) for a in range(d) for b in range(d) for sign in (-1, 1)}
    orbits: list[tuple[tuple[int, int, int], ...]] = []
    while ambient:
        start = min(ambient)
        orbit = {start}
        frontier = [start]
        while frontier:
            a, b, sign = frontier.pop()
            for u, v, unit_sign in unit_actions:
                product = multiply_residue((a, b), (u, v), delta, f, d)
                candidate = (product[0], product[1], sign * unit_sign)
                if candidate not in orbit:
                    orbit.add(candidate)
                    frontier.append(candidate)
        ambient -= orbit
        orbits.append(tuple(sorted(orbit)))
    orbits.sort(key=lambda orbit: orbit[0])
    lookup = {element: index for index, orbit in enumerate(orbits) for element in orbit}
    table = []
    for left in orbits:
        row = []
        representative = left[0]
        for right in orbits:
            other = right[0]
            product = multiply_residue(
                representative[:2], other[:2], delta, f, d
            )
            row.append(lookup[(product[0], product[1], representative[2] * other[2])])
        table.append(row)
    for i, row in enumerate(table):
        for j, product in enumerate(row):
            if table[j][i] != product:
                raise AssertionError("multiplication is not commutative")
            for k in range(len(orbits)):
                if table[product][k] != table[i][table[j][k]]:
                    raise AssertionError("multiplication is not associative")
    identity = lookup[(1 % d, 0, 1)]
    if any(table[identity][i] != i or table[i][identity] != i for i in range(len(orbits))):
        raise AssertionError("identity failure")
    primitive = []
    for orbit in orbits:
        representative = orbit[0]
        primitive.append(gcd(norm_residue(representative[:2], delta, f), d) == 1)
    return {
        "orbits": orbits,
        "lookup": lookup,
        "multiplication": table,
        "identity": identity,
        "primitive": primitive,
    }


def rref(rows: list[list[Fraction]]) -> tuple[list[list[Fraction]], list[int]]:
    matrix = [row[:] for row in rows if any(value for value in row)]
    if not matrix:
        return [], []
    column_count = len(matrix[0])
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(column_count):
        found = next((row for row in range(pivot_row, len(matrix)) if matrix[row][column]), None)
        if found is None:
            continue
        matrix[pivot_row], matrix[found] = matrix[found], matrix[pivot_row]
        pivot = matrix[pivot_row][column]
        matrix[pivot_row] = [value / pivot for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            scalar = matrix[row][column]
            matrix[row] = [
                value - scalar * pivot_value
                for value, pivot_value in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return matrix[:pivot_row], pivot_columns


def nullspace(matrix: list[list[int]]) -> list[list[Fraction]]:
    reduced, pivots = rref([[Fraction(value) for value in row] for row in matrix])
    columns = len(matrix[0]) if matrix else 0
    free = [column for column in range(columns) if column not in pivots]
    answer = []
    for free_column in free:
        vector = [Fraction(0) for _ in range(columns)]
        vector[free_column] = Fraction(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free_column]
        answer.append(vector)
    return answer


def vector_product(
    left: list[Fraction], right: list[Fraction], multiplication: list[list[int]]
) -> list[Fraction]:
    result = [Fraction(0) for _ in left]
    for i, left_value in enumerate(left):
        if not left_value:
            continue
        for j, right_value in enumerate(right):
            if right_value:
                result[multiplication[i][j]] += left_value * right_value
    return result


def span(vectors: list[list[Fraction]]) -> list[list[Fraction]]:
    return rref(vectors)[0]


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def radical_data(multiplication: list[list[int]]) -> dict[str, object]:
    size = len(multiplication)
    traces = [
        sum(1 for row in range(size) if multiplication[row][element] == row)
        for element in range(size)
    ]
    gram = [[traces[multiplication[i][j]] for j in range(size)] for i in range(size)]
    basis = nullspace(gram)
    powers = [len(basis)]
    current = basis
    while current:
        products = [
            vector_product(left, right, multiplication)
            for left in current
            for right in basis
        ]
        current = span(products)
        powers.append(len(current))
        if len(powers) > size + 1:
            raise AssertionError("radical nilpotence bound failed")
    return {
        "trace_gram": gram,
        "trace_rank": size - len(basis),
        "basis": [[fraction_text(value) for value in vector] for vector in basis],
        "power_dimensions": powers,
        "nilpotence_exponent_bound": len(powers) - 1,
    }


def encode_orbit(orbit: tuple[tuple[int, int, int], ...]) -> list[list[int]]:
    return [list(element) for element in orbit]


def build_case(
    *,
    name: str,
    delta: int,
    f: int,
    d: int,
    unit_actions: list[tuple[int, int, int]],
    expected_total: int,
    expected_primitive: int,
) -> dict[str, object]:
    monoid = orbit_monoid(
        delta=delta, f=f, d=d, unit_actions=unit_actions
    )
    total = len(monoid["orbits"])
    primitive = sum(monoid["primitive"])
    if (total, primitive) != (expected_total, expected_primitive):
        raise AssertionError((name, total, primitive))
    radical = radical_data(monoid["multiplication"])
    return {
        "name": name,
        "delta": delta,
        "form_conductor": f,
        "modulus_integer": d,
        "unit_actions": [list(action) for action in unit_actions],
        "element_count": total,
        "primitive_element_count": primitive,
        "identity_index": monoid["identity"],
        "elements": [encode_orbit(orbit) for orbit in monoid["orbits"]],
        "primitive_flags": monoid["primitive"],
        "multiplication_table": monoid["multiplication"],
        "radical": radical,
    }


def main() -> None:
    started = time.monotonic()
    prereg = json.loads(PREREG.read_text())
    d7 = build_case(
        name="AFK pilot d=7, K=Q(sqrt(2)), O_2",
        delta=8,
        f=2,
        d=7,
        # eta=3+2sqrt(2)=-5+theta_2 and -1; eta is positive at infinity_2.
        unit_actions=[(-5, 1, 1), (-1, 0, -1)],
        expected_total=17,
        expected_primitive=12,
    )
    d4 = build_case(
        name="D4 maximal-order calibration",
        delta=5,
        f=1,
        d=4,
        # epsilon=(1+sqrt(5))/2=-2+theta_1 is negative at infinity_2.
        unit_actions=[(-2, 1, -1), (-1, 0, -1)],
        expected_total=4,
        expected_primitive=2,
    )
    if d4["radical"]["trace_rank"] != 3:
        raise AssertionError("D4 trace-form rank changed")
    payload = {
        "schema": "tcc-flat-monoid-p1-adapter-v1",
        "claim_tag": "PROVED_FINITE_ALGEBRA_PILOT",
        "scope": (
            "The d=7,f=2 and D4 finite monoids under the class-number-one "
            "residue/sign quotient lemma. No AFK partial-zeta evaluation."
        ),
        "preregistration_sha256": digest(PREREG),
        "source_note_sha256": digest(SOURCE_NOTE),
        "source_hashes": prereg["input_sha256"],
        "cases": [d4, d7],
        "checks": {
            "D4_primitive_count_matches_phase0_ray_group_order": True,
            "D4_flat_monoid_trace_rank": 3,
            "D7_expected_total_and_primitive_counts": [17, 12],
            "trace_form_radical_method": (
                "Over Q, the Jacobson radical of a finite commutative algebra "
                "is the kernel of its regular-representation trace form."
            ),
            "target_functional_evaluated": False,
        },
        "wall_seconds": round(time.monotonic() - started, 6),
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("TCC_FLAT_MONOID_P1_ADAPTER=PASS")
    print(f"D7_MONOID_ELEMENTS={d7['element_count']}")
    print(f"D7_RADICAL_DIMENSION={len(d7['radical']['basis'])}")


if __name__ == "__main__":
    main()
