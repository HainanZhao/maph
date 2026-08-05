#!/usr/bin/env python3
"""Exact bounded extension control for the C71 D=5 equality core.

This constructs the core witness emitted by cycle71_defect5_core_csp.cpp.
It is deliberately a finite prototype: each prospective new line uses a
vertex already present in its part, or one distinguished fresh vertex in that
part.  It never claims to enumerate arbitrary global completions.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product


PAIRS = ((0, 4), (0, 3), (0, 2), (0, 1), (0, 1))
MAPS = (
    (0, 1, 3, 2, 0, 4),
    (1, 0, 3, 1, 4, 2),
    (2, 1, 2, 0, 4, 3),
    (3, 3, 0, 2, 4, 1),
    (4, 4, 3, 0, 2, 1),
)


@dataclass(frozen=True)
class Core:
    edges: tuple[frozenset[tuple[int, str]], ...]
    side_vertices: tuple[tuple[tuple[int, str], ...], ...]


def construct_core() -> Core:
    edges: list[frozenset[tuple[int, str]]] = []
    for i in range(6):
        line = [(0, "v")]
        for q in range(5):
            label = f"r{q}" if i in PAIRS[q] else f"b{q}_{i}"
            line.append((q + 1, label))
        edges.append(frozenset(line))
    for j in range(5):
        line = [(0, f"f{j}")]
        for q in range(5):
            if q == j:
                label = f"r{q}"
            else:
                matches = [i for i in range(6) if MAPS[j][i] == q]
                if len(matches) != 1:
                    raise AssertionError((j, q, matches))
                label = f"b{q}_{matches[0]}"
            line.append((q + 1, label))
        edges.append(frozenset(line))
    side_vertices = tuple(
        tuple(sorted({v for edge in edges for v in edge if v[0] == side}))
        for side in range(6)
    )
    return Core(tuple(edges), side_vertices)


def defect(edges: tuple[frozenset[tuple[int, str]], ...]) -> int:
    return sum(len(a & b) - 1 for a, b in combinations(edges, 2))


def check_hypergraph(edges: tuple[frozenset[tuple[int, str]], ...]) -> None:
    for edge in edges:
        assert len(edge) == 6
        assert {side for side, _ in edge} == set(range(6))
    for a, b in combinations(edges, 2):
        assert len(a & b) >= 1


def covers_of_size(edges: tuple[frozenset[tuple[int, str]], ...], size: int):
    vertices = tuple(sorted(set().union(*edges)))
    for cover in combinations(vertices, size):
        chosen = frozenset(cover)
        if all(chosen & edge for edge in edges):
            yield chosen


def minimum_cover(edges: tuple[frozenset[tuple[int, str]], ...], upper: int = 6):
    for size in range(upper + 1):
        witness = next(covers_of_size(edges, size), None)
        if witness is not None:
            return witness
    return None


def transversal_number(edges: tuple[frozenset[tuple[int, str]], ...], upper: int = 6) -> int | None:
    witness = minimum_cover(edges, upper)
    return len(witness) if witness is not None else None


def candidate_lines(core: Core) -> tuple[frozenset[tuple[int, str]], ...]:
    alphabets = tuple(
        vertices + ((side, "fresh"),) for side, vertices in enumerate(core.side_vertices)
    )
    candidates = []
    for tup in product(*alphabets):
        candidate = frozenset(tup)
        if all(len(candidate & edge) == 1 for edge in core.edges):
            candidates.append(candidate)
    return tuple(candidates)


def main() -> None:
    core = construct_core()
    check_hypergraph(core.edges)
    assert defect(core.edges) == 5
    core_tau = transversal_number(core.edges)
    assert core_tau is not None
    minimum_covers = tuple(covers_of_size(core.edges, core_tau))
    covers5 = tuple(covers_of_size(core.edges, 5))
    assert covers5
    candidates = candidate_lines(core)
    assert candidates
    retained = []
    destructive = []
    for candidate in candidates:
        whole = core.edges + (candidate,)
        assert defect(whole) == 5
        if any(cover & candidate for cover in covers5):
            retained.append(candidate)
        else:
            destructive.append(candidate)
    print(f"CORE edges={len(core.edges)} vertices={sum(map(len, core.side_vertices))} D={defect(core.edges)} tau={core_tau}")
    print(f"MINIMUM_COVERS size={core_tau} count={len(minimum_covers)}")
    for cover in minimum_covers[:3]:
        print(f"MINIMUM_COVER {sorted(cover)}")
    print(f"COVERS5 count={len(covers5)}")
    print(f"CANDIDATES exact_linear={len(candidates)} retained_by_core_cover={len(retained)} destructive_to_all_core_5covers={len(destructive)}")
    for index, candidate in enumerate(candidates):
        tau = transversal_number(core.edges + (candidate,))
        print(f"CANDIDATE {index} tau={tau} {sorted(candidate)}")
    compatible_pairs = [
        (i, j) for i, j in combinations(range(len(candidates)), 2)
        if len(candidates[i] & candidates[j]) == 1
    ]
    print(f"CANDIDATE_COMPATIBLE_PAIRS count={len(compatible_pairs)} pairs={compatible_pairs}")
    for i, j in compatible_pairs:
        extension = core.edges + (candidates[i], candidates[j])
        witness = minimum_cover(extension)
        print(f"PAIR_EXTENSION {i},{j} D={defect(extension)} tau={len(witness)} cover={sorted(witness)}")
    for side, vertices in enumerate(core.side_vertices):
        print(f"SIDE {side} vertices={len(vertices)} labels={' '.join(label for _, label in vertices)}")
    if destructive:
        for candidate in destructive[:3]:
            tau = transversal_number(core.edges + (candidate,))
            print(f"DESTRUCTIVE candidate={sorted(candidate)} tau={tau}")


if __name__ == "__main__":
    main()
