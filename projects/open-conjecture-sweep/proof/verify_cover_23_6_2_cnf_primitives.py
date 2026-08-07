#!/usr/bin/env python3
"""Exhaustively check the covering encoder's reusable CNF primitives."""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "discovery"))

from cover_23_6_2_sat import CNF  # noqa: E402


def satisfiable(clauses: list[list[int]]) -> bool:
    """Small independent DPLL implementation used only for finite controls."""

    def search(current: tuple[tuple[int, ...], ...], values: dict[int, bool]) -> bool:
        while True:
            reduced: list[tuple[int, ...]] = []
            units: list[int] = []
            for clause in current:
                if any(values.get(abs(lit)) == (lit > 0) for lit in clause):
                    continue
                undecided = tuple(lit for lit in clause if abs(lit) not in values)
                if not undecided:
                    return False
                reduced.append(undecided)
                if len(undecided) == 1:
                    units.append(undecided[0])
            if not reduced:
                return True
            if not units:
                current = tuple(reduced)
                break
            for literal in units:
                variable, value = abs(literal), literal > 0
                if variable in values and values[variable] != value:
                    return False
                values[variable] = value
            current = tuple(reduced)

        literal = current[0][0]
        variable = abs(literal)
        for value in (literal > 0, literal < 0):
            extended = dict(values)
            extended[variable] = value
            if search(current, extended):
                return True
        return False

    return search(tuple(tuple(clause) for clause in clauses), {})


def fixed_satisfiable(cnf: CNF, fixed: dict[int, bool]) -> bool:
    units = [[variable if value else -variable] for variable, value in fixed.items()]
    return satisfiable([*cnf.clauses, *units])


def check_at_most() -> int:
    rows = 0
    for size in range(1, 8):
        for bound in range(-1, size + 1):
            cnf = CNF()
            inputs = [cnf.var() for _ in range(size)]
            cnf.at_most(inputs, bound)
            for bits in itertools.product((False, True), repeat=size):
                observed = fixed_satisfiable(cnf, dict(zip(inputs, bits)))
                assert observed == (sum(bits) <= bound)
                rows += 1
    return rows


def check_exactly() -> int:
    rows = 0
    for size in range(1, 7):
        for value in range(size + 1):
            cnf = CNF()
            inputs = [cnf.var() for _ in range(size)]
            cnf.exactly(inputs, value)
            for bits in itertools.product((False, True), repeat=size):
                observed = fixed_satisfiable(cnf, dict(zip(inputs, bits)))
                assert observed == (sum(bits) == value)
                rows += 1
    return rows


def check_guarded_exactly() -> int:
    rows = 0
    for size in range(1, 6):
        for value in range(size + 1):
            cnf = CNF()
            guard = cnf.var()
            inputs = [cnf.var() for _ in range(size)]
            cnf.guarded_exactly(guard, inputs, value)
            for enabled in (False, True):
                for bits in itertools.product((False, True), repeat=size):
                    fixed = {guard: enabled, **dict(zip(inputs, bits))}
                    observed = fixed_satisfiable(cnf, fixed)
                    assert observed == (not enabled or sum(bits) == value)
                    rows += 1
    return rows


def check_lexicographic() -> int:
    rows = 0
    for size in range(1, 6):
        for left_bits in itertools.product((False, True), repeat=size):
            for right_bits in itertools.product((False, True), repeat=size):
                cnf = CNF()
                left = [cnf.var() for _ in range(size)]
                right = [cnf.var() for _ in range(size)]
                cnf.lex_greater_equal(left, right)
                fixed = {
                    **dict(zip(left, left_bits)),
                    **dict(zip(right, right_bits)),
                }
                observed = fixed_satisfiable(cnf, fixed)
                assert observed == (left_bits >= right_bits)
                rows += 1
    return rows


def check_conjunction() -> int:
    rows = 0
    cnf = CNF()
    left, right, conjunction = cnf.var(), cnf.var(), cnf.var()
    cnf.add(-conjunction, left)
    cnf.add(-conjunction, right)
    cnf.add(conjunction, -left, -right)
    for left_value, right_value, conjunction_value in itertools.product(
        (False, True), repeat=3
    ):
        fixed = {
            left: left_value,
            right: right_value,
            conjunction: conjunction_value,
        }
        observed = fixed_satisfiable(cnf, fixed)
        assert observed == (
            conjunction_value == (left_value and right_value)
        )
        rows += 1
    return rows


def main() -> None:
    result = {
        "at_most_rows": check_at_most(),
        "conjunction_rows": check_conjunction(),
        "exactly_rows": check_exactly(),
        "guarded_exactly_rows": check_guarded_exactly(),
        "lexicographic_rows": check_lexicographic(),
        "status": "CNF_PRIMITIVES_EXHAUSTIVE_PASS",
    }
    result["total_rows"] = sum(
        value for key, value in result.items() if key.endswith("_rows")
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
