#!/usr/bin/env python3
"""Diagnose the contracted dual quotient in the opposite encoder shell.

This is scratch exact-combinatorial code for Cycle 12.  It reconstructs the
quotient from the declared rotation, gauge tree, and encoder recurrence.  It
does not certify the arbitrary-width induction.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from discovery.audit_g1_gauge_tree_dual import _gauge_tree
from discovery.audit_g1_opposite_explicit_all_width import (
    base_tree_pairs,
    exceptional_pairs,
    extension_pairs,
    opposite_checkerboard_rotation,
)
from proof.verify_g1_arbitrary_width_generic_tightness import _square_descriptor
from proof.verify_lane_b_genus3 import (
    _cycle_basis,
    _edge_homology_labels,
    _rotation_faces,
)
from src.conventions import cubic_box


def _induced_parts(nodes, adjacency):
    unseen = set(nodes)
    parts = []
    owner = {}
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        part = {start}
        stack = [start]
        while stack:
            node = stack.pop()
            for neighbour in adjacency[node]:
                if neighbour in unseen:
                    unseen.remove(neighbour)
                    part.add(neighbour)
                    stack.append(neighbour)
        index = len(parts)
        parts.append(part)
        for node in part:
            owner[node] = index
    return parts, owner


def _edge(left, right):
    return frozenset((left, right))


def predicted_parent_edges(width):
    """The symbolic parent families printed in the Cycle-12 manuscript."""
    r = width - 2
    result = set()
    if width % 2:
        root = (0, 0, 0, r)
        for j in range(1, r - 1, 2):
            result.add(_edge((0, 0, 0, j), root))
        for j in range(0, r, 2):
            result.add(_edge((0, 0, 1, j), root))
            result.add(_edge((1, 0, r, j), root))
            result.add(_edge((1, 2, r, j), root))
            result.add(_edge((0, 1, j, r), (0, 0, 1, r - 1)))
            result.add(_edge((2, 0, j, r), (0, 1, j, r)))
            result.add(_edge((2, 2, j, r), (0, 1, j, r)))
        e_values = (0,) if width == 5 else range(2, r, 2)
        for j in e_values:
            result.add(_edge((0, 0, r, j), (1, 0, r, j)))
        return root, result

    root = (0, 0, r, 1)
    for j in range(1, r, 2):
        result.add(_edge((0, 0, 0, j), root))
        result.add(_edge((1, 3, r, j), root))
        result.add(_edge((2, 3, j, r), root))
    for j in range(0, r - 1, 2):
        result.add(_edge((0, 0, 1, j), root))
    for j in range(3, r - 1, 2):
        result.add(_edge((0, 0, j, r), (2, 3, j, r)))
        result.add(_edge((2, 1, j, r), (0, 0, j, r)))
    for j in range(3, r, 2):
        result.add(_edge((0, 1, r, j), (1, 3, r, j)))
        result.add(_edge((1, 1, r, j), (0, 1, r, j)))
    result.add(_edge((0, 2, 1, r), (2, 3, 1, r)))
    result.add(_edge((0, 2, r - 1, r), (2, 3, r - 1, r)))
    result.add(_edge((0, 2, r, 1), (1, 3, r, 1)))
    result.add(_edge((1, 1, r, 1), (0, 2, r, 1)))
    result.add(_edge((2, 1, 1, r), (0, 2, 1, r)))
    result.add(_edge((2, 1, r - 1, r), (0, 2, r - 1, r)))
    result.add(_edge((0, 0, 1, r), (2, 1, 1, r)))
    result.add(_edge((0, 0, r - 1, r), (2, 1, r - 1, r)))
    result.add(_edge((0, 1, r, 1), (1, 1, r, 1)))
    return root, result


def quotient_row(width, tree_pairs):
    vertices, edges = cubic_box((5, width, width))
    edge_index = {(edge.u, edge.v): index for index, edge in enumerate(edges)}
    tree = {edge_index[pair] for pair in tree_pairs}
    exceptional = {edge_index[pair] for pair in exceptional_pairs(width)}

    faces, walks = _rotation_faces(
        vertices, edges, opposite_checkerboard_rotation(width)
    )
    genus = (2 - (len(vertices) - len(edges) + len(faces))) // 2
    cycles = _cycle_basis(vertices, edges)
    _labels, _face_rank = _edge_homology_labels(
        len(edges), faces, cycles, genus
    )
    gauge = _gauge_tree(len(edges), faces, cycles, genus)
    retained_chords = (tree - gauge) - exceptional
    retained_dual_edges = set(range(len(edges))) - gauge - retained_chords

    old_vertices, old_edges = cubic_box((5, width - 1, width - 1))
    _old_faces, old_walks = _rotation_faces(
        old_vertices, old_edges, opposite_checkerboard_rotation(width - 1)
    )
    old_squares = {
        _square_descriptor(walk) for walk in old_walks if len(walk) == 4
    }
    descriptors = [_square_descriptor(walk) for walk in walks]
    common = {
        index for index, descriptor in enumerate(descriptors)
        if descriptor in old_squares
    }
    changed = set(range(len(walks))) - common

    incidences = [[] for _ in edges]
    for face, walk in enumerate(walks):
        for left, right in zip(walk, walk[1:] + walk[:1]):
            incidences[edge_index[tuple(sorted((left, right)))]].append(face)
    if any(len(pair) != 2 for pair in incidences):
        raise AssertionError("noncellular edge incidence")

    adjacency = [[] for _ in walks]
    for edge in retained_dual_edges:
        left, right = incidences[edge]
        adjacency[left].append(right)
        adjacency[right].append(left)

    old_parts, old_owner = _induced_parts(common, adjacency)
    new_parts, new_owner = _induced_parts(changed, adjacency)
    offset = len(old_parts)
    quotient = [set() for _ in range(offset + len(new_parts))]
    for face in common:
        for neighbour in adjacency[face]:
            if neighbour in changed:
                left = old_owner[face]
                right = offset + new_owner[neighbour]
                quotient[left].add(right)
                quotient[right].add(left)

    outer_face = next(index for index, walk in enumerate(walks) if len(walk) != 4)
    root = offset + new_owner[outer_face]
    distance = {root: 0}
    parent = {}
    queue = deque([root])
    while queue:
        node = queue.popleft()
        for neighbour in sorted(quotient[node]):
            if neighbour not in distance:
                distance[neighbour] = distance[node] + 1
                parent[neighbour] = node
                queue.append(neighbour)

    representatives = []
    for part in old_parts + new_parts:
        representatives.append(min((descriptors[face] for face in part), key=repr))

    edge_count = sum(map(len, quotient)) // 2
    quotient_edges = {
        _edge(representatives[left], representatives[right])
        for left, neighbours in enumerate(quotient)
        for right in neighbours
        if left < right
    }
    predicted_root, predicted_edges = predicted_parent_edges(width)
    layers = [
        Counter(distance.values())[layer]
        for layer in range(max(distance.values()) + 1)
    ]
    return {
        "width": width,
        "root": representatives[root],
        "vertex_count": len(quotient),
        "edge_count": edge_count,
        "reached_count": len(distance),
        "is_tree": len(distance) == len(quotient) and edge_count == len(quotient) - 1,
        "predicted_root_matches": representatives[root] == predicted_root,
        "predicted_edge_set_matches": quotient_edges == predicted_edges,
        "layers": layers,
        "parents": [
            {
                "layer": distance[node],
                "child": representatives[node],
                "parent": representatives[parent[node]],
            }
            for node in sorted(parent, key=lambda item: (distance[item], repr(representatives[item])))
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--minimum-width", type=int, default=5)
    parser.add_argument("--maximum-width", type=int, default=12)
    args = parser.parse_args()
    tree = base_tree_pairs()
    rows = []
    for width in range(4, args.maximum_width + 1):
        if width >= args.minimum_width:
            rows.append(quotient_row(width, tree))
        tree |= extension_pairs(width)
    print(json.dumps({"status": "OBSERVED", "rows": rows}, indent=2))


if __name__ == "__main__":
    main()
