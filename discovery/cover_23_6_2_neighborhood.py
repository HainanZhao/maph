#!/usr/bin/env python3
"""Exact Hamming-neighborhood search around a two-pair-deficient covering."""

from __future__ import annotations

import argparse
import itertools
import json
import subprocess
from pathlib import Path

from cover_23_6_2_sat import B, K, V, CNF, parse_model, verify


NEAR = [
    [7, 8, 13, 16, 17, 20], [4, 7, 8, 10, 12, 15],
    [1, 5, 7, 8, 11, 23], [1, 6, 9, 13, 15, 21],
    [5, 6, 9, 16, 18, 22], [14, 15, 16, 17, 18, 23],
    [6, 10, 11, 20, 22, 23], [1, 2, 10, 11, 14, 16],
    [1, 3, 15, 17, 19, 22], [4, 5, 12, 13, 14, 22],
    [2, 7, 8, 18, 21, 22], [7, 8, 9, 14, 20, 21],
    [2, 3, 9, 13, 16, 23], [3, 5, 10, 11, 17, 21],
    [1, 3, 4, 12, 18, 20], [3, 6, 7, 8, 14, 19],
    [2, 5, 11, 15, 19, 20], [9, 10, 11, 13, 18, 19],
    [4, 12, 16, 19, 21, 23], [2, 4, 6, 9, 12, 17],
]
NEAR = [[v - 1 for v in block] for block in NEAR]


def build(radius: int) -> tuple[CNF, list[list[int]]]:
    cnf = CNF()
    x = [[cnf.var() for _ in range(V)] for _ in range(B)]
    for row in x:
        cnf.exactly(row, K)
    for u, v in itertools.combinations(range(V), 2):
        covering = []
        for b in range(B):
            y = cnf.var()
            covering.append(y)
            cnf.add(-y, x[b][u])
            cnf.add(-y, x[b][v])
            cnf.add(y, -x[b][u], -x[b][v])
        cnf.add(*covering)
    mismatches = []
    for b in range(B):
        old = set(NEAR[b])
        mismatches.extend(-x[b][v] if v in old else x[b][v] for v in range(V))
    cnf.at_most(mismatches, radius)
    return cnf, x


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("radius", type=int)
    parser.add_argument("--solver", default="cadical")
    args = parser.parse_args()
    if args.radius < 0 or args.radius % 2:
        raise SystemExit("radius must be a nonnegative even integer")
    cnf, x = build(args.radius)
    root = Path("discovery/out")
    cnf_path = root / f"cover-23-6-2-neighborhood-r{args.radius}.cnf"
    model_path = root / f"cover-23-6-2-neighborhood-r{args.radius}.model"
    cnf.write(cnf_path)
    with model_path.open("w", encoding="ascii") as model:
        result = subprocess.run([args.solver, "--sat", str(cnf_path)], stdout=model)
    if result.returncode not in (10, 20):
        raise SystemExit(f"solver failed with status {result.returncode}")
    values = parse_model(model_path)
    if values is None:
        print(json.dumps({"radius": args.radius, "status": "UNSATISFIABLE_UNCERTIFIED"}))
        return
    blocks = [[v for v in range(V) if x[b][v] in values] for b in range(B)]
    checked = verify(blocks)
    checked["radius"] = args.radius
    print(json.dumps(checked, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
