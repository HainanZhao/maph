#!/usr/bin/env python3
"""Exact C86 census for the all-inclusion Hall transport mechanism."""
from __future__ import annotations

import itertools
import json


def members(family: int, n: int) -> tuple[int, ...]:
    return tuple(a for a in range(1 << n) if family >> a & 1)


def union_closed(rows: tuple[int, ...], family: int) -> bool:
    return all(family >> (a | b) & 1 for a in rows for b in rows)


def dimension(rows: tuple[int, ...]) -> int:
    ordered = sorted(rows, key=lambda a: (a.bit_count(), a))
    length: dict[int, int] = {}
    for b in ordered:
        length[b] = 1 + max((length[a] for a in ordered if a != b and a & ~b == 0), default=0)
    return max(length.values()) - 1


def separating(rows: tuple[int, ...], n: int) -> bool:
    columns = [tuple(bool(a >> x & 1) for a in rows) for x in range(n)]
    return len(set(columns)) == n


def optimal_elements(rows: tuple[int, ...], n: int) -> tuple[int, ...]:
    columns = [{a for a in rows if a >> x & 1} for x in range(n)]
    return tuple(x for x in range(n) if not any(columns[x] < columns[y] for y in range(n)))


def adjacency(rows: tuple[int, ...], x: int) -> tuple[tuple[int, ...], tuple[int, ...], dict[int, tuple[int, ...]]]:
    left = tuple(a for a in rows if not (a >> x & 1))
    right = tuple(b for b in rows if b >> x & 1)
    return left, right, {a: tuple(b for b in right if a & ~b == 0) for a in left}


def matching_saturates(rows: tuple[int, ...], x: int) -> bool:
    left, _right, graph = adjacency(rows, x)
    matched: dict[int, int] = {}

    def augment(a: int, seen: set[int]) -> bool:
        for b in graph[a]:
            if b in seen:
                continue
            seen.add(b)
            if b not in matched or augment(matched[b], seen):
                matched[b] = a
                return True
        return False

    return all(augment(a, set()) for a in left)


def hall_witness(rows: tuple[int, ...], x: int) -> tuple[tuple[int, ...], tuple[int, ...]] | None:
    left, _right, graph = adjacency(rows, x)
    for size in range(1, len(left) + 1):
        for subset in itertools.combinations(left, size):
            neighborhood = tuple(sorted({b for a in subset for b in graph[a]}))
            if len(neighborhood) < len(subset):
                return subset, neighborhood
    return None


def source_controls() -> dict:
    c19 = (0, 2, 4, 3, 5, 6, 7)
    c20 = (31, 23, 15, 29, 27, 30, 7, 19, 25, 28, 14, 3, 17, 12, 6, 24)
    assert union_closed(c19, sum(1 << a for a in c19)) and dimension(c19) == 3
    assert union_closed(c20, sum(1 << a for a in c20)) and dimension(c20) == 3
    c19_optimal = optimal_elements(c19, 3)
    assert 0 in c19_optimal and not matching_saturates(c19, 0)
    c20_optimal = optimal_elements(c20, 5)
    assert c20_optimal == tuple(range(5))
    immediate_cover_failures = []
    for x in range(5):
        for a in c20:
            if a >> x & 1:
                continue
            covers = [b for b in c20 if b >> x & 1 and a != b and a & ~b == 0
                      and not any(a != c and c != b and a & ~c == 0 and c & ~b == 0 for c in c20)]
            if not covers:
                immediate_cover_failures.append((x, a))
                break
    assert len(immediate_cover_failures) == 5
    c20_matchings = [matching_saturates(c20, x) for x in c20_optimal]
    c20_hall_witnesses = [hall_witness(c20, x) for x in c20_optimal]
    assert all(matching == (witness is None) for matching, witness in zip(c20_matchings, c20_hall_witnesses))
    return {
        "example_319": {"optimal_elements": list(c19_optimal), "optimal_1_hall_witness": hall_witness(c19, 0)},
        "example_320": {"optimal_elements": list(c20_optimal), "immediate_cover_failures": immediate_cover_failures,
                          "all_inclusion_matching": c20_matchings, "hall_witnesses": c20_hall_witnesses},
    }


def main() -> None:
    retained = 0
    first_failure = None
    verifier_disagreements = 0
    for family in range(1 << 16):
        rows = members(family, 4)
        if not rows or 15 not in rows or not union_closed(rows, family) or not separating(rows, 4) or dimension(rows) != 3:
            continue
        retained += 1
        optimals = optimal_elements(rows, 4)
        results = []
        for x in optimals:
            matching = matching_saturates(rows, x)
            witness = hall_witness(rows, x)
            verifier_disagreements += matching != (witness is None)
            results.append((x, matching, witness))
        if not any(matching for _x, matching, _witness in results) and first_failure is None:
            first_failure = {"family_sets": list(rows), "optimal_elements": list(optimals),
                             "per_optimal": [{"x": x, "matching_saturates": matching,
                                              "hall_deficient_left": list(witness[0]), "hall_neighborhood": list(witness[1])}
                                             for x, matching, witness in results]}
    assert verifier_disagreements == 0
    controls = source_controls()
    print(json.dumps({"epistemic_status": "PROVED", "family_masks": 65536, "retained_dimension_three": retained,
                      "all_optimal_hall_failures": 0 if first_failure is None else 1,
                      "first_all_optimal_failure": first_failure, "verifier_disagreements": verifier_disagreements,
                      "source_controls": controls, "status": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
