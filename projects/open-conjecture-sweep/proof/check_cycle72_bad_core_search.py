#!/usr/bin/env python3
"""Independently validate C72 direct bad-core search outputs and witnesses."""
from __future__ import annotations

from itertools import combinations, product
import json
from pathlib import Path
import sys


def build(row):
    sides = row["sides"]
    central = row["central"]
    pairs = [tuple(p) for p in row["pairs"]]
    maps = row["maps"]
    star = {}
    for j in range(5):
        for i in pairs[j]:
            key = (sides[j], i)
            assert key not in star or star[key] == (sides[j] + 1, f"r{j}")
            star[key] = (sides[j] + 1, f"r{j}")
    for q in range(5):
        for i in range(6):
            star.setdefault((q, i), (q + 1, f"b{q}_{i}"))

    edges = []
    for i in range(6):
        edges.append(frozenset({(0, "v")} | {star[(q, i)] for q in range(5)}))
    for j in range(5):
        edge = {(0, f"c{central[j]}")}
        for q in range(5):
            indices = [i for i in range(6) if maps[j][i] == q]
            if q == sides[j]:
                assert sorted(indices) == sorted(pairs[j])
                edge.add((q + 1, f"r{j}"))
            else:
                assert len(indices) == 1
                i = indices[0]
                assert star[(q, i)][1].startswith("b")
                edge.add(star[(q, i)])
        edges.append(frozenset(edge))
    return tuple(edges)


def extension_traces(edges):
    universe = set().union(*edges)
    alphabets = []
    for q in range(6):
        old = tuple(sorted(v for v in universe if v[0] == q))
        alphabets.append(old + ((q, "fresh"),))
    traces = set()
    for line in product(*alphabets):
        line = frozenset(line)
        if all(len(line & edge) == 1 for edge in edges):
            traces.add(frozenset(line & universe))
    return tuple(sorted(traces, key=lambda x: tuple(sorted(x))))


def blocker(edges, traces):
    family = tuple(edges) + tuple(traces)
    seen = [set() for _ in range(6)]

    def dfs(chosen, depth):
        if chosen in seen[depth]:
            return None
        seen[depth].add(chosen)
        uncovered = [line for line in family if chosen.isdisjoint(line)]
        if not uncovered:
            return chosen
        if depth == 5:
            return None
        branch = min(uncovered, key=len)
        for vertex in sorted(branch):
            answer = dfs(chosen | frozenset({vertex}), depth + 1)
            if answer is not None:
                return answer
        return None

    return dfs(frozenset(), 0)


def validate_assignment(row):
    edges = build(row)
    assert len(edges) == 11
    assert all(len(edge) == 6 and {q for q, _ in edge} == set(range(6))
               for edge in edges)
    assert all(a & b for a, b in combinations(edges, 2))
    assert all(len(edges[j] & edges[k]) == 1
               for j in range(6, 11) for k in range(6, j))
    defect = sum(len(a & b) - 1 for a, b in combinations(edges, 2))
    assert defect == 5
    traces = extension_traces(edges)
    answer = blocker(edges, traces)
    assert len(traces) == row["extension_types"]
    assert (answer is not None) == row["has_blocker"]
    return len(set().union(*edges)), len(traces), answer


def main():
    rows = [json.loads(Path(name).read_text()) for name in sys.argv[1:]]
    assert rows
    assert all(row["status"] in {"BAD_CORE", "TYPE_CAP", "ASSIGNMENT_CAP", "DONE"}
               and row["epistemic_status"] == "PROVED" for row in rows)
    first_details = [validate_assignment(row["first"])
                     for row in rows if "first" in row]
    bad = [row["bad"] for row in rows if row["status"] == "BAD_CORE"]
    details = [validate_assignment(row) for row in bad]
    assert all(answer is None for _, _, answer in details)
    complete_side = None
    if (len(rows) == 3
            and all(row["status"] == "DONE" for row in rows)
            and len({row["side_filter"] for row in rows}) == 1
            and rows[0]["side_filter"] >= 0):
        assert {row["shards"] for row in rows} == {3}
        assert {row["shard"] for row in rows} == {0, 1, 2}
        # There are Bell(5) = 52 central restricted-growth strings and
        # C(6,2)^5 pair choices.  The C++ sharding key is the case ordinal,
        # so these three residues are a disjoint exhaustive union.
        expected_cases = 52 * 15**5
        assert sum(row["cases"] for row in rows) == expected_cases
        complete_side = {
            "side_filter": rows[0]["side_filter"],
            "shards": 3,
            "cases_expected_and_reported": expected_cases,
            "realized_cores": sum(row["assignments"] for row in rows),
            "maximum_extension_types": max(row["max_extension_types"] for row in rows),
        }
        if all("canonical_hash_sum" in row and "canonical_hash_xor" in row
               for row in rows):
            complete_side["canonical_hash_sum"] = (
                sum(row["canonical_hash_sum"] for row in rows) % (1 << 64)
            )
            value = 0
            for row in rows:
                value ^= row["canonical_hash_xor"]
            complete_side["canonical_hash_xor"] = value
    print(json.dumps({
        "status": "PASS",
        "epistemic_status": "PROVED",
        "outputs_checked": len(rows),
        "bad_cores_validated": len(bad),
        "bad_core_details": [
            {"core_vertices": vertices, "extension_types": types}
            for vertices, types, _ in details
        ],
        "first_assignments_validated": len(first_details),
        "assignments_reported": sum(row["assignments"] for row in rows),
        "complete_filtered_side": complete_side,
        "claim_boundary": (
            "A non-null complete_filtered_side validates exhaustive shard "
            "accounting for that one side filter and emitted witnesses; it "
            "does not cover other side filters or prove Ryser."
        ),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
