#!/usr/bin/env python3
"""Independently verify the eleven canonical C(23,6,2) star branches."""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "discovery"))

from cover_23_6_2_bounded_experiment import BRANCHES  # noqa: E402
from cover_23_6_2_sat import SURVIVING_EXCESS_PATTERNS  # noqa: E402
from cover_23_6_2_star_cases import SUPPORTS, canonical_star  # noqa: E402


Edge = tuple[int, int]
Graph = tuple[Edge, ...]


def canonical_multigraph(edges: tuple[Edge, ...]) -> Graph:
    """Return the least relabeling after deleting isolated vertices."""

    vertices = sorted({vertex for edge in edges for vertex in edge})
    relabeled = tuple(
        sorted(
            (vertices.index(left), vertices.index(right))
            for left, right in edges
        )
    )
    candidates: list[Graph] = []
    for permutation in itertools.permutations(range(len(vertices))):
        candidate = tuple(
            sorted(
                tuple(sorted((permutation[left], permutation[right])))
                for left, right in relabeled
            )
        )
        candidates.append(candidate)
    return min(candidates)


def enumerate_three_edge_orbits() -> set[Graph]:
    """Enumerate loopless three-edge multigraphs on at most five vertices."""

    possible_edges = tuple(itertools.combinations(range(5), 2))
    return {
        canonical_multigraph(edges)
        for edges in itertools.combinations_with_replacement(possible_edges, 3)
    }


def partitions(total: int, maximum: int | None = None) -> set[tuple[int, ...]]:
    """Enumerate decreasing positive integer partitions of ``total``."""

    if total == 0:
        return {()}
    ceiling = min(total, maximum if maximum is not None else total)
    result: set[tuple[int, ...]] = set()
    for first in range(ceiling, 0, -1):
        for tail in partitions(total - first, first):
            result.add((first, *tail))
    return result


def verify_star(supports: list[tuple[int, ...]]) -> tuple[int, ...]:
    """Reconstruct a star and return its nontrivial point multiplicities."""

    rows, singleton_groups = canonical_star(supports)
    assert len(rows) == 5
    assert all(len(row) == 6 and 0 in row for row in rows)
    assert set().union(*rows) == set(range(23))
    assert sum(len(group) for group in singleton_groups) == 22 - len(supports)
    multiplicities = {
        point: sum(point in row for row in rows) for point in range(1, 23)
    }
    assert all(value >= 1 for value in multiplicities.values())
    assert sum(value - 1 for value in multiplicities.values()) == 3
    return tuple(sorted(value for value in multiplicities.values() if value > 1))


def main() -> None:
    assert verify_star([(0, 1, 2, 3)]) == (4,)
    for name, supports in SUPPORTS.items():
        expected = (2, 3) if name.startswith("32-") else (2, 2, 2)
        assert verify_star(supports) == expected

    triple_supports = {
        name: canonical_multigraph(tuple(tuple(edge) for edge in supports))
        for name, supports in SUPPORTS.items()
        if name.startswith("222-")
    }
    enumerated = enumerate_three_edge_orbits()
    assert len(enumerated) == 7
    assert len(set(triple_supports.values())) == 7
    assert set(triple_supports.values()) == enumerated

    intersection_sizes = {
        len(set(supports[0]).intersection(supports[1]))
        for name, supports in SUPPORTS.items()
        if name.startswith("32-")
    }
    assert intersection_sizes == {0, 1, 2}

    expected_branches = {"4", *SUPPORTS}
    assert len(expected_branches) == 11
    assert set(BRANCHES) == expected_branches

    enumerated_excess = {
        partition for partition in partitions(5) if len(partition) >= 3
    }
    encoded_excess = {
        tuple(
            sorted(
                (
                    excess
                    for excess, count in counts.items()
                    for _ in range(count)
                ),
                reverse=True,
            )
        )
        for counts in SURVIVING_EXCESS_PATTERNS.values()
    }
    assert enumerated_excess == encoded_excess

    print(
        json.dumps(
            {
                "branch_count": len(BRANCHES),
                "multiplicity_four_orbits": 1,
                "replication_patterns": len(encoded_excess),
                "star_representatives_checked": len(SUPPORTS) + 1,
                "three_plus_two_orbits": len(intersection_sizes),
                "two_plus_two_plus_two_orbits": len(enumerated),
                "status": "STAR_ORBIT_ENUMERATION_PASS",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
