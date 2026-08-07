#!/usr/bin/env python3
"""Homology audit of explicit prefix trees using only face-boundary reduction."""

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
from proof.verify_lane_b_genus3 import _rotation_faces  # noqa: E402
from src.conventions import cubic_box  # noqa: E402
from src.lane_b_universal_embedding import universal_checkerboard_rotation  # noqa: E402


def _echelon(vectors):
    basis = {}
    for vector in vectors:
        while vector:
            pivot = vector.bit_length() - 1
            if pivot in basis:
                vector ^= basis[pivot]
            else:
                basis[pivot] = vector
                break
    return basis


def _reduce(vector, basis):
    for pivot in sorted(basis, reverse=True):
        if (vector >> pivot) & 1:
            vector ^= basis[pivot]
    return vector


def audit_tree(width, tree, old_width=None):
    vertices, edges = cubic_box((5, width, width))
    edge_index = {(edge.u, edge.v): index for index, edge in enumerate(edges)}
    face_masks, _ = _rotation_faces(
        vertices, edges, universal_checkerboard_rotation(5, width)
    )
    face_basis = _echelon(face_masks)
    if len(face_basis) != len(face_masks) - 1:
        raise AssertionError("face boundaries have the wrong rank")

    adjacency = {vertex: [] for vertex in vertices}
    for index in tree:
        edge = edges[index]
        adjacency[edge.u].append((edge.v, index))
        adjacency[edge.v].append((edge.u, index))
    tree_paths = {vertices[0]: 0}
    stack = [vertices[0]]
    while stack:
        vertex = stack.pop()
        for neighbour, edge_index_value in adjacency[vertex]:
            if neighbour not in tree_paths:
                tree_paths[neighbour] = tree_paths[vertex] ^ (1 << edge_index_value)
                stack.append(neighbour)
    if len(tree_paths) != len(vertices):
        raise AssertionError("explicit edge set is disconnected")

    root = (4, 0, 0)
    completion = {}
    for y in range(width):
        for z in range(width):
            value = 0
            for yy in range(y):
                value ^= 1 << edge_index[((4, yy, 0), (4, yy + 1, 0))]
            for zz in range(z):
                value ^= 1 << edge_index[((4, y, zz), (4, y, zz + 1))]
            completion[(4, y, z)] = value
    homology_basis = dict(face_basis)
    pivots = []
    for y in range(width):
        for z in range(width):
            vertex = (4, y, z)
            if vertex == root:
                continue
            cycle = tree_paths[root] ^ tree_paths[vertex] ^ completion[vertex]
            reduced = _reduce(cycle, homology_basis)
            if not reduced:
                pivots.append({"terminal": [y, z], "pivot_edge": None})
                continue
            pivot = reduced.bit_length() - 1
            homology_basis[pivot] = reduced
            edge = edges[pivot]
            pivots.append({
                "terminal": [y, z],
                "pivot_edge": [list(edge.u), list(edge.v)],
                "new_shell_terminal": old_width is not None and (y >= old_width or z >= old_width),
            })
    homology_rank = len(homology_basis) - len(face_basis)
    return {
        "width": width,
        "face_count": len(face_masks),
        "face_boundary_rank": len(face_basis),
        "terminal_homology_rank": homology_rank,
        "target": width * width - 1,
        "pivots": pivots,
    }


def audit(maximum_width):
    width = 4
    tree = set(_base_tree())
    rows = [audit_tree(width, tree)]
    while width < maximum_width:
        old_width = width
        width += 1
        tree = _embed(tree, old_width, width)
        _, edges = cubic_box((5, width, width))
        index = {(edge.u, edge.v): i for i, edge in enumerate(edges)}
        tree |= {index[pair] for pair in extension_pairs(old_width)}
        rows.append(audit_tree(width, tree, old_width))
    return {
        "status": "OBSERVED exact GF(2) face-boundary homology audit",
        "rows": rows,
        "claim_boundary": (
            "The audit avoids canonical coordinates entirely. A finite pivot table is not "
            "an arbitrary-width proof until its two parity patterns are derived."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-width", type=int, default=8)
    args = parser.parse_args()
    print(json.dumps(audit(args.maximum_width), indent=2, sort_keys=True))
