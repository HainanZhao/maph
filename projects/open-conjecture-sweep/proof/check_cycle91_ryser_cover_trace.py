#!/usr/bin/env python3
"""Exact C91 deletion-cover trace CSP on the published 13-edge control."""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import runpy


CONTROL = Path(__file__).parents[1] / "discovery/cycle69_r6_extremal_control.py"


def load_control():
    namespace = runpy.run_path(str(CONTROL))
    edges = tuple(tuple(tuple(vertex) for vertex in edge) for edge in namespace["EDGES"])
    vertices = tuple(sorted({vertex for edge in edges for vertex in edge}))
    # The published labelling has six vertices in part 1 and five in each
    # remaining part, hence 31 vertices rather than a balanced 30.
    assert len(edges) == 13 and len(vertices) == 31
    return edges, vertices


def covers_all(choice: tuple[tuple[int, int], ...], edges) -> bool:
    chosen = set(choice)
    return all(chosen.intersection(edge) for edge in edges)


def direct_families(edges, vertices):
    """Route A: literal lexicographic four-subset audit."""
    families = []
    for deleted, edge in enumerate(edges):
        residual = edges[:deleted] + edges[deleted + 1:]
        assert not any(covers_all(choice, residual) for choice in combinations(vertices, 3))
        family = tuple(choice for choice in combinations(vertices, 4) if covers_all(choice, residual))
        assert family and all(not set(choice).intersection(edge) for choice in family)
        families.append(family)
    return tuple(families)


def recursive_covers(edges, vertices, size=4):
    """Route B: exact uncovered-edge branching, then canonical set deduplication."""
    answers = set()

    def visit(chosen):
        if len(chosen) > size:
            return
        uncovered = next((edge for edge in edges if not set(chosen).intersection(edge)), None)
        if uncovered is None:
            if len(chosen) == size:
                answers.add(tuple(sorted(chosen)))
            return
        if len(chosen) == size:
            return
        for vertex in uncovered:
            visit(chosen | {vertex})

    visit(frozenset())
    return tuple(sorted(answers))


def recursive_families(edges, vertices):
    families = []
    for deleted, edge in enumerate(edges):
        residual = edges[:deleted] + edges[deleted + 1:]
        family = recursive_covers(residual, vertices)
        assert family and all(not set(choice).intersection(edge) for choice in family)
        families.append(family)
    return tuple(families)


def trace(choice, edge):
    return frozenset(part for part, vertex in edge if (part, vertex) in choice)


def compatible(left_choice, left_edge, right_choice, right_edge):
    return bool(trace(left_choice, right_edge).intersection(trace(right_choice, left_edge)))


def csp_route_a(edges, families):
    """Direct domain recursion, choosing the most constrained unassigned edge."""
    assigned = {}

    def visit():
        if len(assigned) == len(edges):
            return dict(assigned)
        remaining = [index for index in range(len(edges)) if index not in assigned]
        ranked = []
        for index in remaining:
            allowed = []
            for candidate_index, candidate in enumerate(families[index]):
                if all(compatible(candidate, edges[index], assigned[other], edges[other]) for other in assigned):
                    allowed.append(candidate_index)
            ranked.append((len(allowed), index, allowed))
        _, index, allowed = min(ranked)
        for candidate_index in allowed:
            assigned[index] = families[index][candidate_index]
            result = visit()
            if result is not None:
                return result
            del assigned[index]
        return None

    return visit()


def csp_route_b(edges, families):
    """Independent exact CSP route: precompute pairwise compatibility masks."""
    masks = {}
    for left in range(len(edges)):
        for right in range(left + 1, len(edges)):
            masks[left, right] = {
                left_index: frozenset(right_index for right_index, right_choice in enumerate(families[right])
                                      if compatible(left_choice, edges[left], right_choice, edges[right]))
                for left_index, left_choice in enumerate(families[left])
            }
    choices = {}

    def agrees(index, candidate_index):
        for other, other_index in choices.items():
            low, high = sorted((index, other))
            if index == low:
                if other_index not in masks[low, high][candidate_index]:
                    return False
            elif candidate_index not in masks[low, high][other_index]:
                return False
        return True

    def visit(index=0):
        if index == len(edges):
            return dict(choices)
        for candidate_index in range(len(families[index])):
            if agrees(index, candidate_index):
                choices[index] = candidate_index
                result = visit(index + 1)
                if result is not None:
                    return result
                del choices[index]
        return None

    result = visit()
    if result is None:
        return None
    return {index: families[index][candidate_index] for index, candidate_index in result.items()}


def payload():
    edges, vertices = load_control()
    direct = direct_families(edges, vertices)
    recursive = recursive_families(edges, vertices)
    assert direct == recursive
    route_a = csp_route_a(edges, direct)
    route_b = csp_route_b(edges, recursive)
    assert (route_a is None) == (route_b is None)
    counts = [len(family) for family in direct]
    return {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "claim_boundary": "Exact result for one published tau=5 control and one frozen reciprocal trace CSP only; not Ryser r=6 or an integral matching reduction.",
        "vertices": len(vertices),
        "edges": len(edges),
        "tau": 5,
        "minimum_deletion_cover_size": 4,
        "family_counts": counts,
        "family_count_histogram": dict(sorted(Counter(counts).items())),
        "route_a_csp": "SAT" if route_a is not None else "UNSAT",
        "route_b_csp": "SAT" if route_b is not None else "UNSAT",
        "selected_covers": None if route_a is None else {
            str(index + 1): [list(vertex) for vertex in route_a[index]] for index in sorted(route_a)
        },
    }


if __name__ == "__main__":
    print(json.dumps(payload(), sort_keys=True))
