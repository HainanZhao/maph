#!/usr/bin/env python3
"""Exact extension-type blockers for every generalized C72 core orbit."""

from __future__ import annotations
import argparse
from itertools import combinations, product
import json
from pathlib import Path

SHAPE_SIDES = {"221": (0, 0, 1, 1, 2), "2111": (0, 0, 1, 2, 3), "11111": (0, 1, 2, 3, 4)}


def core_from(sides, pairs, maps):
    edges = []
    for i in range(6):
        line = [(0, "v")]
        for q in range(5):
            repeated = [j for j in range(5) if sides[j] == q and i in pairs[j]]
            assert len(repeated) <= 1
            line.append((q + 1, f"r{repeated[0]}" if repeated else f"b{q}_{i}"))
        edges.append(frozenset(line))
    for j in range(5):
        line = [(0, f"f{j}")]
        for q in range(5):
            indices = [i for i in range(6) if maps[j][i] == q]
            if q == sides[j]:
                assert sorted(indices) == sorted(pairs[j])
                line.append((q + 1, f"r{j}"))
            else:
                assert len(indices) == 1
                i = indices[0]
                assert not any(sides[ell] == q and i in pairs[ell] for ell in range(5))
                line.append((q + 1, f"b{q}_{i}"))
        edges.append(frozenset(line))
    return tuple(edges)


def defect(edges):
    return sum(len(a & b) - 1 for a, b in combinations(edges, 2))


def tau(edges, cap=5):
    vertices = tuple(sorted(set().union(*edges)))
    for size in range(cap + 1):
        for choice in combinations(vertices, size):
            if all(set(choice) & edge for edge in edges):
                return size
    return None


def extension_types(edges):
    by_side = []
    for q in range(6):
        old = tuple(sorted(v for v in set().union(*edges) if v[0] == q))
        by_side.append(old + ((q, "fresh"),))
    answer = []
    for choice in product(*by_side):
        line = frozenset(choice)
        if all(len(line & edge) == 1 for edge in edges):
            answer.append(line)
    return tuple(answer)


def universal_blocker(edges, types, cap=5):
    vertices = tuple(sorted(set().union(*edges)))
    index = {v: i for i, v in enumerate(vertices)}
    families = list(edges) + [frozenset(v for v in line if v in index) for line in types]
    coverage = [0] * len(vertices)
    for f, family in enumerate(families):
        for vertex in family:
            coverage[index[vertex]] |= 1 << f
    target = (1 << len(families)) - 1
    for size in range(cap + 1):
        for choice in combinations(range(len(vertices)), size):
            mask = 0
            for v in choice:
                mask |= coverage[v]
            if mask == target:
                return tuple(vertices[v] for v in choice)
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("orbit_files", nargs=3, type=Path)
    args = parser.parse_args()
    rows = []
    for path in args.orbit_files:
        payload = json.loads(path.read_text())
        assert payload["status"] == "PASS"
        shape = payload["shape"]
        sides = SHAPE_SIDES[shape]
        for orbit, representative in enumerate(payload["representatives"]):
            pairs = tuple(tuple(x) for x in representative["pairs"])
            maps = tuple(tuple(x) for x in representative["maps"])
            edges = core_from(sides, pairs, maps)
            assert all(len(edge) == 6 and {v[0] for v in edge} == set(range(6)) for edge in edges)
            assert all(a & b for a, b in combinations(edges, 2))
            assert defect(edges) == 5
            types = extension_types(edges)
            blocker = universal_blocker(edges, types)
            rows.append({"shape":shape,"orbit":orbit,"vertices":len(set().union(*edges)),"core_tau":tau(edges),"extension_types":len(types),"blocker":list(blocker) if blocker is not None else None,"blocker_size":len(blocker) if blocker is not None else None})
    assert len(rows) == 16
    result = {"status":"PASS","epistemic_status":"PROVED","orbits":len(rows),"all_have_five_blocker":all(row["blocker_size"] is not None and row["blocker_size"] <= 5 for row in rows),"rows":rows,"claim_boundary":"Exact universal core-vertex blockers for the 16 generalized D=5 equality-core orbits. Promotion to D>=6 also requires the structural derivation from an arbitrary equality-case counterexample."}
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
