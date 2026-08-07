#!/usr/bin/env python3
"""Canonical exact SAT cases for star partitions (3+2) and (2+2+2)."""

from __future__ import annotations

import argparse
import itertools
import json
import subprocess
from pathlib import Path

from cover_23_6_2_sat import (
    B,
    K,
    V,
    CNF,
    add_surviving_replication_patterns,
    parse_model,
    verify,
)


SUPPORTS = {
    # Multiplicities 3+2, classified by support intersection.
    "32-overlap0": [(0, 1, 2), (3, 4)],
    "32-overlap1": [(0, 1, 2), (0, 3)],
    "32-overlap2": [(0, 1, 2), (0, 1)],
    # Three two-block supports: loopless 3-edge multigraphs on <=5 vertices.
    "222-triple": [(0, 1), (0, 1), (0, 1)],
    "222-double-share": [(0, 1), (0, 1), (0, 2)],
    "222-double-disjoint": [(0, 1), (0, 1), (2, 3)],
    "222-triangle": [(0, 1), (0, 2), (1, 2)],
    "222-star": [(0, 1), (0, 2), (0, 3)],
    "222-path": [(0, 1), (0, 2), (2, 3)],
    "222-path-edge": [(0, 1), (0, 2), (3, 4)],
}


def canonical_star(supports: list[tuple[int, ...]]) -> tuple[list[set[int]], list[list[int]]]:
    repeated = len(supports)
    rows = [{0} for _ in range(5)]
    for point, support in enumerate(supports, 1):
        for block in support:
            rows[block].add(point)
    next_point = repeated + 1
    singleton_groups = []
    for row in rows:
        group = list(range(next_point, next_point + K - len(row)))
        row.update(group)
        singleton_groups.append(group)
        next_point += len(group)
    assert next_point == V
    assert all(len(row) == K for row in rows)
    return rows, singleton_groups


def build(case: str) -> tuple[CNF, list[list[int]], list[set[int]]]:
    star, singleton_groups = canonical_star(SUPPORTS[case])
    cnf = CNF()
    x = [[cnf.var() for _ in range(V)] for _ in range(B)]
    for row in x:
        cnf.exactly(row, K)
    for b in range(5):
        for v in range(V):
            cnf.add(x[b][v] if v in star[b] else -x[b][v])
    for b in range(5, B):
        cnf.add(-x[b][0])
    for b in range(5, B - 1):
        cnf.lex_greater_equal(x[b], x[b + 1])
    columns = [[x[b][v] for b in range(B)] for v in range(V)]
    # Repeated star points with the same support are interchangeable as well.
    # Sorting their full columns is therefore a sound additional quotient of
    # the residual symmetry (notably in the 222-triple branch).
    support_classes: dict[tuple[int, ...], list[int]] = {}
    for point, support in enumerate(SUPPORTS[case], 1):
        support_classes.setdefault(tuple(sorted(support)), []).append(point)
    for group in support_classes.values():
        for left, right in zip(group, group[1:]):
            cnf.lex_greater_equal(columns[left], columns[right])
    for group in singleton_groups:
        for left, right in zip(group, group[1:]):
            cnf.lex_greater_equal(columns[left], columns[right])
    for v in range(V):
        cnf.at_most([-x[b][v] for b in range(B)], B - 5)
        cnf.at_most([x[b][v] for b in range(B)], 8)
    add_surviving_replication_patterns(cnf, x)
    for u, v in itertools.combinations(range(V), 2):
        covering = []
        for b in range(B):
            y = cnf.var()
            covering.append(y)
            cnf.add(-y, x[b][u])
            cnf.add(-y, x[b][v])
            cnf.add(y, -x[b][u], -x[b][v])
        cnf.add(*covering)
    return cnf, x, star


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("case", choices=sorted(SUPPORTS))
    parser.add_argument("--solver", default="cadical")
    parser.add_argument("--time", type=int, default=600)
    args = parser.parse_args()
    cnf, x, _ = build(args.case)
    root = Path("discovery/out")
    stem = root / f"cover-23-6-2-{args.case}"
    cnf.write(stem.with_suffix(".cnf"))
    print(json.dumps({"case": args.case, "clauses": len(cnf.clauses), "variables": cnf.nvars}))
    with stem.with_suffix(".model").open("w", encoding="ascii") as model:
        result = subprocess.run(
            [args.solver, "--sat", "-t", str(args.time), str(stem.with_suffix(".cnf"))],
            stdout=model,
        )
    if result.returncode == 0:
        print(json.dumps({"case": args.case, "status": "TIME_LIMIT"}))
        return
    if result.returncode not in (10, 20):
        raise SystemExit(f"solver failed with status {result.returncode}")
    values = parse_model(stem.with_suffix(".model"))
    if values is None:
        print(json.dumps({"case": args.case, "status": "UNSATISFIABLE_UNCERTIFIED"}))
        return
    blocks = [[v for v in range(V) if x[b][v] in values] for b in range(B)]
    checked = verify(blocks)
    checked["star_case"] = args.case
    print(json.dumps(checked, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
