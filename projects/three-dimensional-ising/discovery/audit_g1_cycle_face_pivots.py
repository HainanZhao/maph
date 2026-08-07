#!/usr/bin/env python3
"""Reduce the correct terminal closure cycles modulo face boundaries."""

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
from discovery.audit_g1_gauge_tree_dual import _gauge_tree  # noqa: E402
from proof.verify_lane_b_genus3 import _cycle_basis, _rotation_faces  # noqa: E402
from src.conventions import cubic_box  # noqa: E402
from src.lane_b_universal_embedding import universal_checkerboard_rotation  # noqa: E402


def _basis(vectors):
    result = {}
    for vector in vectors:
        while vector:
            pivot = vector.bit_length() - 1
            if pivot in result:
                vector ^= result[pivot]
            else:
                result[pivot] = vector
                break
    return result


def _reduce(vector, basis):
    for pivot in sorted(basis, reverse=True):
        if (vector >> pivot) & 1:
            vector ^= basis[pivot]
    return vector


def _paths(vertices, edges, tree, root):
    adjacency = {vertex: [] for vertex in vertices}
    for edge_index in tree:
        edge = edges[edge_index]
        adjacency[edge.u].append((edge.v, edge_index))
        adjacency[edge.v].append((edge.u, edge_index))
    result = {root: 0}
    stack = [root]
    while stack:
        vertex = stack.pop()
        for neighbour, edge_index in adjacency[vertex]:
            if neighbour not in result:
                result[neighbour] = result[vertex] ^ (1 << edge_index)
                stack.append(neighbour)
    if len(result) != len(vertices):
        raise AssertionError("edge set is not a spanning tree")
    return result


def _row(width, encoder_tree):
    vertices, edges = cubic_box((5, width, width))
    faces, _ = _rotation_faces(
        vertices, edges, universal_checkerboard_rotation(5, width)
    )
    genus = (2 - (len(vertices) - len(edges) + len(faces))) // 2
    gauge_tree = _gauge_tree(len(edges), faces, _cycle_basis(vertices, edges), genus)
    root = (4, 0, 0)
    encoder_paths = _paths(vertices, edges, encoder_tree, root)
    gauge_paths = _paths(vertices, edges, gauge_tree, root)
    basis = _basis(faces)
    face_rank = len(basis)
    pivots = []
    for y in range(width):
        for z in range(width):
            terminal = (4, y, z)
            if terminal == root:
                continue
            cycle = encoder_paths[terminal] ^ gauge_paths[terminal]
            reduced = _reduce(cycle, basis)
            if not reduced:
                pivots.append({"terminal": [y, z], "pivot": None})
                continue
            pivot = reduced.bit_length() - 1
            basis[pivot] = reduced
            edge = edges[pivot]
            pivots.append({
                "terminal": [y, z],
                "pivot": pivot,
                "pivot_edge": [list(edge.u), list(edge.v)],
            })
    return {
        "width": width,
        "face_rank": face_rank,
        "terminal_quotient_rank": len(basis) - face_rank,
        "target": width * width - 1,
        "pivots": pivots,
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
        "status": "OBSERVED exact face-quotient pivot audit",
        "rows": rows,
        "claim_boundary": "Finite pivot patterns do not prove the symbolic shell induction.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-width", type=int, default=8)
    args = parser.parse_args()
    print(json.dumps(audit(args.maximum_width), indent=2, sort_keys=True))
