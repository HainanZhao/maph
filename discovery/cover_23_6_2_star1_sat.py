#!/usr/bin/env python3
"""Exact canonical SAT branches for the star multiplicity partition (4)."""

from __future__ import annotations

import argparse
import itertools
import json
import subprocess
from pathlib import Path

from cover_23_6_2_sat import B, K, V, CNF, parse_model, verify


STAR = [
    {0, 1, 2, 3, 4, 5},
    {0, 1, 6, 7, 8, 9},
    {0, 1, 10, 11, 12, 13},
    {0, 1, 14, 15, 16, 17},
    {0, 18, 19, 20, 21, 22},
]


def build(point1_degree: int) -> tuple[CNF, list[list[int]]]:
    cnf = CNF()
    x = [[cnf.var() for _ in range(V)] for _ in range(B)]
    for row in x:
        cnf.exactly(row, K)

    # Unique repeated star point 1 has multiplicity four.  All remaining
    # points are singletons and may be relabelled into these five groups.
    for b in range(5):
        for v in range(V):
            cnf.add(x[b][v] if v in STAR[b] else -x[b][v])
    for b in range(5, B):
        cnf.add(-x[b][0])

    for b in range(5, B - 1):
        cnf.lex_greater_equal(x[b], x[b + 1])
    columns = [[x[b][v] for b in range(B)] for v in range(V)]
    for group in ([2, 3, 4, 5], [6, 7, 8, 9], [10, 11, 12, 13],
                  [14, 15, 16, 17], [18, 19, 20, 21, 22]):
        for left, right in zip(group, group[1:]):
            cnf.lex_greater_equal(columns[left], columns[right])

    for v in range(V):
        cnf.at_most([-x[b][v] for b in range(B)], B - 5)
        cnf.at_most([x[b][v] for b in range(B)], 10)
    cnf.exactly([x[b][1] for b in range(B)], point1_degree)
    if point1_degree == 5:
        for v in range(18):
            cnf.at_most([x[b][v] for b in range(B)], 5)
        for v in range(18, V):
            cnf.exactly([x[b][v] for b in range(B)], 6)
        forced = {1, 18, 19, 20, 21, 22}
        for v in range(V):
            cnf.add(x[5][v] if v in forced else -x[5][v])

    for u, v in itertools.combinations(range(V), 2):
        covering = []
        for b in range(B):
            y = cnf.var()
            covering.append(y)
            cnf.add(-y, x[b][u])
            cnf.add(-y, x[b][v])
            cnf.add(y, -x[b][u], -x[b][v])
        cnf.add(*covering)
    return cnf, x


def main() -> None:
    parser = argparse.ArgumentParser()
    # The repeated star point occurs in four of the five central blocks.  The
    # excess-spectrum theorem proves that a 20-cover has at least three
    # positive-excess points. Hence total degrees 9 (excess partition 4+1)
    # and 10 (partition 5) are impossible here; 5,...,8 exhaust the viable
    # degree cases for this star partition.
    parser.add_argument("degree", type=int, choices=range(5, 9))
    parser.add_argument("--solver", default="cadical")
    parser.add_argument("--time", type=int, default=300)
    parser.add_argument("--write-only", action="store_true")
    args = parser.parse_args()
    cnf, x = build(args.degree)
    root = Path("discovery/out")
    stem = root / f"cover-23-6-2-star1-degree{args.degree}"
    cnf.write(stem.with_suffix(".cnf"))
    if args.write_only:
        print(json.dumps({"degree": args.degree, "clauses": len(cnf.clauses), "variables": cnf.nvars}))
        return
    with stem.with_suffix(".model").open("w", encoding="ascii") as model:
        result = subprocess.run(
            [args.solver, "--sat", "-t", str(args.time), str(stem.with_suffix(".cnf"))],
            stdout=model,
        )
    if result.returncode == 0:
        print(json.dumps({"degree": args.degree, "status": "TIME_LIMIT"}))
        return
    if result.returncode not in (10, 20):
        raise SystemExit(f"solver failed with status {result.returncode}")
    values = parse_model(stem.with_suffix(".model"))
    if values is None:
        print(json.dumps({"degree": args.degree, "status": "UNSATISFIABLE_UNCERTIFIED"}))
        return
    blocks = [[v for v in range(V) if x[b][v] in values] for b in range(B)]
    checked = verify(blocks)
    checked["point1_degree"] = args.degree
    print(json.dumps(checked, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
