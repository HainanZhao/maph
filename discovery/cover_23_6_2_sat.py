#!/usr/bin/env python3
"""Exact SAT search and independent witness check for a 20-block C(23,6,2).

The CNF uses labelled blocks.  Fixing block 0 to {0,...,5} is without loss
of generality.  Auxiliary variables encode row cardinalities and pairwise
conjunctions.  A SAT model is accepted only after direct coverage checking.
"""

from __future__ import annotations

import argparse
import itertools
import json
import subprocess
from pathlib import Path


V = 23
B = 20
K = 6


class CNF:
    def __init__(self) -> None:
        self.nvars = 0
        self.clauses: list[list[int]] = []

    def var(self) -> int:
        self.nvars += 1
        return self.nvars

    def add(self, *lits: int) -> None:
        self.clauses.append(list(lits))

    def at_most(self, lits: list[int], bound: int) -> None:
        """Sinz sequential-counter encoding of sum(lits) <= bound."""
        n = len(lits)
        if bound < 0:
            self.add()
            return
        if bound >= n:
            return
        if bound == 0:
            for lit in lits:
                self.add(-lit)
            return
        # s[i][j]: among literals 0..i, at least j+1 are true.
        s = [[self.var() for _ in range(bound)] for _ in range(n - 1)]
        self.add(-lits[0], s[0][0])
        for j in range(1, bound):
            self.add(-s[0][j])
        for i in range(1, n - 1):
            self.add(-lits[i], s[i][0])
            self.add(-s[i - 1][0], s[i][0])
            for j in range(1, bound):
                self.add(-lits[i], -s[i - 1][j - 1], s[i][j])
                self.add(-s[i - 1][j], s[i][j])
            self.add(-lits[i], -s[i - 1][bound - 1])
        self.add(-lits[-1], -s[-1][bound - 1])

    def exactly(self, lits: list[int], value: int) -> None:
        self.at_most(lits, value)
        self.at_most([-lit for lit in lits], len(lits) - value)

    def lex_greater_equal(self, left: list[int], right: list[int]) -> None:
        """Require left >= right lexicographically, with 1 > 0."""
        assert len(left) == len(right)
        equal_prefix = self.var()
        self.add(equal_prefix)
        for a, b in zip(left, right):
            # At the first difference, 0/1 is forbidden.
            self.add(-equal_prefix, a, -b)
            next_equal = self.var()
            # next_equal iff equal_prefix and a == b.
            self.add(-next_equal, equal_prefix)
            self.add(-next_equal, -a, b)
            self.add(-next_equal, a, -b)
            self.add(-equal_prefix, a, b, next_equal)
            self.add(-equal_prefix, -a, -b, next_equal)
            equal_prefix = next_equal

    def write(self, path: Path) -> None:
        with path.open("w", encoding="ascii") as out:
            out.write(f"p cnf {self.nvars} {len(self.clauses)}\n")
            for clause in self.clauses:
                out.write(" ".join(map(str, clause)) + " 0\n")


def build(star_repeats: int | None = None) -> tuple[CNF, list[list[int]]]:
    cnf = CNF()
    x = [[cnf.var() for _ in range(V)] for _ in range(B)]

    # Every block has exactly six points.
    for row in x:
        cnf.exactly(row, K)

    # Relabel points so that the first block is canonical.
    for v, lit in enumerate(x[0]):
        cnf.add(lit if v < K else -lit)

    # Since sum_v r_v = 120 and every r_v >= 5, at least eighteen points
    # have replication exactly five.  Label one of them 0.  Lexicographic
    # row order then puts precisely its five incident blocks first.
    for b in range(B):
        cnf.add(x[b][0] if b < 5 else -x[b][0])

    # Eliminate all block-label permutations.
    for b in range(B - 1):
        cnf.lex_greater_equal(x[b], x[b + 1])

    # Eliminate point-label permutations inside and outside the fixed block.
    # Columns are compared from block 0 downward.
    columns = [[x[b][v] for b in range(B)] for v in range(V)]
    for v in (list(range(1, K - 1)) + list(range(K, K + 8))
              + list(range(K + 9, K + 11)) + list(range(K + 12, V - 1))):
        cnf.lex_greater_equal(columns[v], columns[v + 1])

    # Every point occurs at least ceil(22/5)=5 times.  This is redundant but
    # exposes a strong necessary condition early to the solver.
    for v in range(V):
        cnf.at_most([-x[b][v] for b in range(B)], B - 5)

    # At most five points can have replication above five.  Hence the
    # 17-point complement of block 0 contains at least twelve degree-five
    # points; label twelve of them 6,...,17.
    for v in range(K, K + 12):
        cnf.at_most([x[b][v] for b in range(B)], 5)

    # In the five-block star at 0, 25 slots cover the other 22 points, so at
    # most three distinct points are repeated.  At least nine outside points
    # are therefore both degree-five and star-singletons; label them 6,...,14.
    for v in range(K, K + 9):
        cnf.at_most([x[b][v] for b in range(5)], 1)

    if star_repeats == 1:
        # The unique repeated point has star multiplicity four.  Choose block
        # 0 through it and label it 1; lexicographic row order then places its
        # four incident star blocks first.  Every other noncentral point is a
        # star singleton.
        for b in range(5):
            cnf.add(x[b][1] if b < 4 else -x[b][1])
        for v in range(2, V):
            cnf.at_most([x[b][v] for b in range(5)], 1)
        cnf.lex_greater_equal(columns[K + 8], columns[K + 9])
    elif star_repeats is not None:
        # z_v iff v occurs in at least two of the five blocks through 0.
        # Since those blocks have exactly three excess nonzero-point
        # incidences, the exhaustive possibilities have 1, 2, or 3 such
        # repeated points (multiplicity partitions 4, 3+2, or 2+2+2).
        repeated = []
        for v in range(1, V):
            z = cnf.var()
            repeated.append(z)
            witnesses = []
            for b, c in itertools.combinations(range(5), 2):
                w = cnf.var()
                witnesses.append(w)
                cnf.add(-w, x[b][v])
                cnf.add(-w, x[c][v])
                cnf.add(w, -x[b][v], -x[c][v])
                cnf.add(-w, z)
            cnf.add(-z, *witnesses)
        cnf.exactly(repeated, star_repeats)

    # y[b,u,v] iff both endpoints occur in block b; each pair needs some y.
    for u, v in itertools.combinations(range(V), 2):
        covering: list[int] = []
        for b in range(B):
            y = cnf.var()
            covering.append(y)
            cnf.add(-y, x[b][u])
            cnf.add(-y, x[b][v])
            cnf.add(y, -x[b][u], -x[b][v])
        cnf.add(*covering)
    return cnf, x


def parse_model(path: Path) -> set[int] | None:
    values: set[int] = set()
    status = None
    for line in path.read_text(encoding="ascii").splitlines():
        if line.startswith("s "):
            status = line
        if line.startswith("v "):
            values.update(int(z) for z in line.split()[1:] if int(z) > 0)
    if status and "UNSATISFIABLE" in status:
        return None
    if not status or "SATISFIABLE" not in status:
        raise RuntimeError(f"solver did not return a decision: {status!r}")
    return values


def verify(blocks: list[list[int]]) -> dict[str, object]:
    assert len(blocks) == B
    assert all(len(block) == K and len(set(block)) == K for block in blocks)
    counts = {(u, v): 0 for u, v in itertools.combinations(range(V), 2)}
    for block in blocks:
        for pair in itertools.combinations(sorted(block), 2):
            counts[pair] += 1
    uncovered = [list(pair) for pair, count in counts.items() if count == 0]
    replications = [sum(v in block for block in blocks) for v in range(V)]
    return {
        "blocks": [[v + 1 for v in block] for block in blocks],
        "covered_pairs": sum(count > 0 for count in counts.values()),
        "maximum_pair_multiplicity": max(counts.values()),
        "pair_excess": sum(count - 1 for count in counts.values()),
        "replications": replications,
        "status": "VERIFIED_20_BLOCK_COVER" if not uncovered else "INVALID",
        "uncovered_pairs": uncovered,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf", type=Path, default=Path("discovery/out/cover-23-6-2.cnf"))
    parser.add_argument("--model", type=Path, default=Path("discovery/out/cover-23-6-2.model"))
    parser.add_argument("--solver", default="cadical")
    parser.add_argument("--star-repeats", type=int, choices=(1, 2, 3))
    parser.add_argument("--generate-only", action="store_true")
    args = parser.parse_args()
    cnf, x = build(args.star_repeats)
    args.cnf.parent.mkdir(parents=True, exist_ok=True)
    cnf.write(args.cnf)
    print(json.dumps({"clauses": len(cnf.clauses), "cnf": str(args.cnf), "variables": cnf.nvars}))
    if args.generate_only:
        return
    with args.model.open("w", encoding="ascii") as model:
        result = subprocess.run([args.solver, str(args.cnf)], stdout=model, check=False)
    if result.returncode not in (10, 20):
        raise SystemExit(f"solver failed with status {result.returncode}")
    values = parse_model(args.model)
    if values is None:
        print(json.dumps({"status": "UNSATISFIABLE_UNCERTIFIED"}))
        return
    blocks = [[v for v in range(V) if x[b][v] in values] for b in range(B)]
    checked = verify(blocks)
    print(json.dumps(checked, indent=2, sort_keys=True))
    if checked["status"] != "VERIFIED_20_BLOCK_COVER":
        raise SystemExit("invalid SAT model")


if __name__ == "__main__":
    main()
