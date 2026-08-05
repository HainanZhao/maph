#!/usr/bin/env python3
"""Exact control for the published 13-edge intersecting 6-partite system."""

from __future__ import annotations

import itertools
import json
from pathlib import Path


EDGES = [
 [(1,1),(2,4),(3,4),(4,5),(5,3),(6,5)], [(1,2),(2,5),(3,2),(4,5),(5,5),(6,3)],
 [(1,3),(2,4),(3,5),(4,3),(5,4),(6,3)], [(1,4),(2,1),(3,5),(4,4),(5,5),(6,5)],
 [(1,4),(2,5),(3,4),(4,2),(5,4),(6,4)], [(1,5),(2,2),(3,5),(4,5),(5,1),(6,4)],
 [(1,5),(2,5),(3,1),(4,3),(5,2),(6,5)], [(1,5),(2,4),(3,3),(4,2),(5,5),(6,2)],
 [(1,5),(2,3),(3,4),(4,4),(5,3),(6,3)], [(1,6),(2,2),(3,4),(4,3),(5,5),(6,1)],
 [(1,6),(2,4),(3,2),(4,4),(5,2),(6,4)], [(1,6),(2,5),(3,5),(4,1),(5,3),(6,2)],
 [(1,6),(2,3),(3,3),(4,5),(5,4),(6,5)],
]


def cover(vertices: tuple[tuple[int, int], ...], edges: list[set[tuple[int, int]]]) -> bool:
    chosen = set(vertices)
    return all(chosen & edge for edge in edges)


def minimum_cover(edges: list[set[tuple[int, int]]], upper: int = 6):
    vertices = sorted(set().union(*edges))
    for size in range(upper + 1):
        witness = next((choice for choice in itertools.combinations(vertices, size) if cover(choice, edges)), None)
        if witness is not None:
            return witness
    raise AssertionError("cap too small")


def main() -> None:
    edges = [set(edge) for edge in EDGES]
    assert all(left & right for i, left in enumerate(edges) for right in edges[i + 1:])
    full = minimum_cover(edges)
    assert len(full) == 5
    deletion = []
    for index, edge in enumerate(edges):
        witness = minimum_cover(edges[:index] + edges[index + 1:], upper=5)
        deletion.append({"deleted_edge": index + 1, "cover_size": len(witness),
                         "disjoint_from_deleted_edge": not(set(witness) & edge), "witness": witness})
    assert all(row["cover_size"] == 4 and row["disjoint_from_deleted_edge"] for row in deletion)
    print(json.dumps({"status":"PASS", "epistemic_status":"PROVED", "source":"Abu-Khazneh--Pokrovskiy 2014, Section 2.2",
      "claim_boundary":"Exact verification of the published 13-edge tau=5 control only; it does not imply a tau<=5 theorem.",
      "vertices":len(set().union(*edges)),"edges":len(edges),"tau":len(full),"full_cover":full,"edge_deletion_witnesses":deletion}, sort_keys=True))


if __name__ == "__main__":
    main()
