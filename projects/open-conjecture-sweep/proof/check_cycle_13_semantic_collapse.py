#!/usr/bin/env python3
"""Exact symbolic audit that Cycle 13's typed maps add no row-76 images."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
from lrc_core_templates import C, K, MUS, clauses, coordinate, full_formula, normalize, sample_bases
from check_cycle_12_core_templates import structural, table


def variable_type(literal: int) -> str:
    variable = abs(literal)
    if variable <= K * C:
        return "x"
    if variable <= K * C + K:
        return "y2"
    return "y7"


def residue(literal: int) -> int:
    return (abs(literal) - 1) % C


def color(value: int) -> tuple[bool, bool]:
    return value % 2 == 0, value % 7 == 0


COLORS = {color(value) for value in range(C)}


def universal_kind(clause: frozenset[int]) -> str | None:
    literals = tuple(clause)
    if len(literals) == 2 and all(literal < 0 and variable_type(literal) == "x" for literal in literals):
        if len({coordinate(literal) for literal in literals}) == 1 and len({residue(literal) for literal in literals}) == 2:
            return "choice_at_most_one"
    if len(literals) == 2:
        negative_x = [literal for literal in literals if literal < 0 and variable_type(literal) == "x"]
        positive_y2 = [literal for literal in literals if literal > 0 and variable_type(literal) == "y2"]
        if len(negative_x) == len(positive_y2) == 1:
            if coordinate(negative_x[0]) == coordinate(positive_y2[0]) and residue(negative_x[0]) % 2 == 0:
                return "x_implies_y2"
    if len(literals) == K - 1 and all(literal < 0 and variable_type(literal) == "y2" for literal in literals):
        if len({coordinate(literal) for literal in literals}) == K - 1:
            return "y2_cardinality"
    return None


def invariant_coverage(clause: frozenset[int]) -> bool:
    if not clause or any(literal < 0 or variable_type(literal) != "x" for literal in clause):
        return False
    by_coordinate: dict[int, set[int]] = {}
    for literal in clause:
        by_coordinate.setdefault(coordinate(literal), set()).add(residue(literal))
    for values in by_coordinate.values():
        for divisor_color in COLORS:
            color_class = {value for value in range(C) if color(value) == divisor_color}
            if values & color_class and not color_class <= values:
                return False
    return True


def audit() -> dict[str, int]:
    # Replays Cycle 12's exact no-match boundary, including the selected subcore.
    structural()
    _, raw = clauses(MUS / "076.cnf")
    core = normalize(raw, sample_bases()[76])
    kinds = Counter()
    for index, clause in enumerate(core):
        kind = universal_kind(clause)
        if kind is not None:
            kinds[kind] += 1
        elif invariant_coverage(clause):
            kinds["color_invariant_coverage"] += 1
        else:
            raise AssertionError(f"clause {index} is neither universal nor color invariant")

    # Verify the claimed universal schemas occur with sufficient multiplicity
    # in an independently rebuilt target formula.
    target = Counter(full_formula(sample_bases()[0]))
    for first in range(C):
        for second in range(first + 1, C):
            clause = frozenset({-(1 + first), -(1 + second)})
            if target[clause] < 1:
                raise AssertionError("missing target exactly-one clause")
    for value in range(C):
        if value % 2 == 0:
            clause = frozenset({-(1 + value), 1 + K * C})
            if target[clause] < 1:
                raise AssertionError("missing target y2 channel clause")
    for omitted in range(K):
        clause = frozenset(-(1 + K * C + coordinate_index) for coordinate_index in range(K) if coordinate_index != omitted)
        if target[clause] < 1:
            raise AssertionError("missing target y2 cardinality clause")

    validation = table(MUS / "validation.tsv")
    external = table(MUS / "external.tsv")
    if any(row["status"] != "NO_MATCH" for row in validation + external):
        raise AssertionError("Cycle 12 residue-identity no-match boundary changed")
    return dict(kinds)


if __name__ == "__main__":
    result = audit()
    print("PASS clauses=293 " + " ".join(f"{key}={result[key]}" for key in sorted(result)))
