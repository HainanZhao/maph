#!/usr/bin/env python3
"""Block-variable exact encoding of the canonical star-(4) branch."""

from __future__ import annotations

import argparse
import itertools
import json
import subprocess
from pathlib import Path

from cover_23_6_2_sat import CNF, parse_model, verify
from cover_23_6_2_star1_sat import STAR


POINTS = tuple(range(2, 23))
GROUPS = [set(range(2, 6)), set(range(6, 10)), set(range(10, 14)),
          set(range(14, 18)), set(range(18, 23))]


def build() -> tuple[CNF, list[tuple[int, ...]], list[int]]:
    cnf = CNF()
    blocks = list(itertools.combinations(POINTS, 6))
    selected = [cnf.var() for _ in blocks]
    containing_pair: dict[tuple[int, int], list[int]] = {
        pair: [] for pair in itertools.combinations(POINTS, 2)
        if not any(set(pair) <= group for group in GROUPS)
    }
    for block, lit in zip(blocks, selected):
        for pair in itertools.combinations(block, 2):
            if pair in containing_pair:
                containing_pair[pair].append(lit)
    for lits in containing_pair.values():
        cnf.add(*lits)

    # Pair coverage gives degree >= ceil(16/5)=4 for every point.  Therefore
    # at most fourteen selected six-sets forces equality in both the block
    # count and every point degree: 21*4 = 14*6 = 84.
    cnf.at_most(selected, 14)
    return cnf, blocks, selected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", default="cadical")
    parser.add_argument("--time", type=int, default=600)
    args = parser.parse_args()
    cnf, blocks, selected = build()
    root = Path("discovery/out")
    cnf_path = root / "cover-23-6-2-star1-setcover.cnf"
    model_path = root / "cover-23-6-2-star1-setcover.model"
    cnf.write(cnf_path)
    print(json.dumps({"clauses": len(cnf.clauses), "variables": cnf.nvars}))
    with model_path.open("w", encoding="ascii") as model:
        result = subprocess.run(
            [args.solver, "--sat", "-t", str(args.time), str(cnf_path)],
            stdout=model,
        )
    if result.returncode == 0:
        print(json.dumps({"status": "TIME_LIMIT"}))
        return
    if result.returncode not in (10, 20):
        raise SystemExit(f"solver failed with status {result.returncode}")
    values = parse_model(model_path)
    if values is None:
        print(json.dumps({"status": "UNSATISFIABLE_UNCERTIFIED"}))
        return
    remainder = [list(block) for block, lit in zip(blocks, selected) if lit in values]
    full = [sorted(block) for block in STAR] + [[1, 18, 19, 20, 21, 22]] + remainder
    checked = verify(full)
    checked["selected_remainder_blocks"] = len(remainder)
    print(json.dumps(checked, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
