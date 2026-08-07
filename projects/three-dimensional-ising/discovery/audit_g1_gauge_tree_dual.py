#!/usr/bin/env python3
"""Audit the correct gauge-tree closures of the recursive prefix tree.

The raw homology-label construction kills a specific spanning-tree complement
of the graph cycle space.  Terminal chains must be closed through that gauge
tree, not through an unrelated terminal comb.  This script reconstructs the
gauge tree and tests the ordinary cographic certificate for the union of the
encoder tree with the gauge-tree terminal subtree.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from discovery.audit_g1_explicit_all_width_induction import (  # noqa: E402
    _base_tree,
    _embed,
    extension_pairs,
)
from proof.verify_lane_b_genus3 import (  # noqa: E402
    _add_labeled_vector,
    _cycle_basis,
    _rotation_faces,
    _vector_independent,
)
from src.conventions import cubic_box  # noqa: E402
from src.lane_b_universal_embedding import universal_checkerboard_rotation  # noqa: E402


def _gauge_tree(edge_count, faces, cycles, genus):
    basis = {}
    for face in faces:
        _add_labeled_vector(basis, face, 0)
    quotient_count = 0
    for cycle in cycles:
        if _vector_independent(basis, cycle):
            _add_labeled_vector(basis, cycle, 1 << quotient_count)
            quotient_count += 1
    if quotient_count != 2 * genus:
        raise AssertionError("homology quotient dimension mismatch")
    tree = set()
    for edge in range(edge_count):
        unit = 1 << edge
        if _vector_independent(basis, unit):
            _add_labeled_vector(basis, unit, 0)
            tree.add(edge)
    return tree


def _terminal_subtree(vertices, edges, tree, terminals):
    adjacency = {vertex: [] for vertex in vertices}
    for edge_index in tree:
        edge = edges[edge_index]
        adjacency[edge.u].append((edge.v, edge_index))
        adjacency[edge.v].append((edge.u, edge_index))
    root = terminals[0]
    parent = {root: (None, None)}
    stack = [root]
    while stack:
        vertex = stack.pop()
        for neighbour, edge_index in adjacency[vertex]:
            if neighbour not in parent:
                parent[neighbour] = (vertex, edge_index)
                stack.append(neighbour)
    if len(parent) != len(vertices):
        raise AssertionError("gauge complement is not a spanning tree")
    result = set()
    for terminal in terminals[1:]:
        vertex = terminal
        while vertex != root:
            previous, edge_index = parent[vertex]
            result.add(edge_index)
            vertex = previous
    return result


def _dual_reach(face_count, edge_faces, retained):
    adjacency = [[] for _ in range(face_count)]
    for edge in retained:
        left, right = edge_faces[edge]
        adjacency[left].append(right)
        adjacency[right].append(left)
    seen = {0}
    stack = [0]
    while stack:
        face = stack.pop()
        for neighbour in adjacency[face]:
            if neighbour not in seen:
                seen.add(neighbour)
                stack.append(neighbour)
    return len(seen)


def _row(width, encoder_tree):
    vertices, edges = cubic_box((5, width, width))
    faces, face_walks = _rotation_faces(
        vertices, edges, universal_checkerboard_rotation(5, width)
    )
    genus = (2 - (len(vertices) - len(edges) + len(faces))) // 2
    cycles = _cycle_basis(vertices, edges)
    gauge_tree = _gauge_tree(len(edges), faces, cycles, genus)
    terminals = [(4, y, z) for y in range(width) for z in range(width)]
    completion = _terminal_subtree(vertices, edges, gauge_tree, terminals)
    union = set(encoder_tree) | completion
    edge_index = {(edge.u, edge.v): index for index, edge in enumerate(edges)}
    incident = [[] for _ in edges]
    for face, walk in enumerate(face_walks):
        for offset, left in enumerate(walk):
            right = walk[(offset + 1) % len(walk)]
            incident[edge_index[tuple(sorted((left, right)))]] .append(face)
    if any(len(pair) != 2 for pair in incident):
        raise AssertionError("each edge must have two incident face darts")
    edge_faces = [tuple(pair) for pair in incident]
    complement = set(range(len(edges))) - union
    reached = _dual_reach(len(faces), edge_faces, complement)
    cycle_dimension = len(union) - len(vertices) + 1
    return {
        "width": width,
        "genus": genus,
        "gauge_tree_edge_count": len(gauge_tree),
        "completion_subtree_edge_count": len(completion),
        "encoder_completion_union_edge_count": len(union),
        "union_cycle_dimension": cycle_dimension,
        "target": width * width - 1,
        "dual_face_count": len(faces),
        "dual_reached_faces": reached,
        "dual_complement_connected": reached == len(faces),
    }


def audit(maximum_width):
    width = 4
    tree = set(_base_tree())
    rows = []
    while True:
        rows.append(_row(width, tree))
        if width == maximum_width:
            break
        old_width = width
        width += 1
        tree = _embed(tree, old_width, width)
        _, edges = cubic_box((5, width, width))
        edge_index = {(edge.u, edge.v): i for i, edge in enumerate(edges)}
        tree |= {edge_index[pair] for pair in extension_pairs(old_width)}
    return {
        "status": "OBSERVED exact gauge-tree/cographic audit",
        "rows": rows,
        "claim_boundary": (
            "Finite dual-connectivity checks are not the symbolic even/odd shell proof."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-width", type=int, default=12)
    args = parser.parse_args()
    print(json.dumps(audit(args.maximum_width), indent=2, sort_keys=True))
