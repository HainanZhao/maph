#!/usr/bin/env python3
"""Test the cographic form of the recursive prefix encoder.

Duplicate a comb tree on the terminal slice inside an interface collar.  The
duplicates are the completion-tree edges.  Each is inserted parallel to its
original edge so as to create a digon.  The lifted independence criterion is
then equivalent to connectivity of the complementary dual edges.

This is a discovery audit; finite widths do not prove the parity-periodic
dual-connectivity induction.
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
from src.conventions import cubic_box  # noqa: E402
from src.lane_b_universal_embedding import universal_checkerboard_rotation  # noqa: E402


def _comb_pairs(width: int):
    pairs = []
    for y in range(width - 1):
        pairs.append(tuple(sorted(((4, y, 0), (4, y + 1, 0)))))
    for y in range(width):
        for z in range(width - 1):
            pairs.append(tuple(sorted(((4, y, z), (4, y, z + 1)))))
    if len(pairs) != width * width - 1:
        raise AssertionError("comb edge count failed")
    return pairs


def _augmented_faces(width: int):
    vertices, original_edges = cubic_box((5, width, width))
    original_index = {(edge.u, edge.v): i for i, edge in enumerate(original_edges)}
    comb = _comb_pairs(width)
    # Edge records are endpoint pairs.  Parallel completion copies follow all
    # original edges in the edge order.
    endpoints = [(edge.u, edge.v) for edge in original_edges] + comb
    completion = set(range(len(original_edges), len(endpoints)))
    completion_of = {
        original_index[pair]: len(original_edges) + i for i, pair in enumerate(comb)
    }

    rotation = universal_checkerboard_rotation(5, width)
    darts_at = {}
    for vertex in vertices:
        darts = []
        for neighbour in rotation[vertex]:
            pair = tuple(sorted((vertex, neighbour)))
            edge = original_index[pair]
            duplicate = completion_of.get(edge)
            # For pair u<v, duplicate-before-original at u and
            # duplicate-after-original at v creates one digon.
            if duplicate is not None and vertex == endpoints[edge][0]:
                darts.append((duplicate, vertex))
            darts.append((edge, vertex))
            if duplicate is not None and vertex == endpoints[edge][1]:
                darts.append((duplicate, vertex))
        darts_at[vertex] = darts

    position = {
        dart: i for vertex, darts in darts_at.items() for i, dart in enumerate(darts)
    }

    def reverse(dart):
        edge, vertex = dart
        u, v = endpoints[edge]
        return edge, (v if vertex == u else u)

    def successor(dart):
        rev = reverse(dart)
        edge, vertex = rev
        darts = darts_at[vertex]
        return darts[(position[rev] + 1) % len(darts)]

    unseen = {(edge, vertex) for edge, pair in enumerate(endpoints) for vertex in pair}
    faces = []
    dart_face = {}
    while unseen:
        start = min(unseen)
        current = start
        face = []
        while True:
            if current not in unseen:
                if current != start:
                    raise AssertionError("dart face traversal collided")
                break
            unseen.remove(current)
            dart_face[current] = len(faces)
            face.append(current)
            current = successor(current)
        faces.append(face)

    edge_faces = []
    for edge, (u, v) in enumerate(endpoints):
        edge_faces.append((dart_face[(edge, u)], dart_face[(edge, v)]))
    euler = len(vertices) - len(endpoints) + len(faces)
    genus = (2 - euler) // 2
    digons = sum(len(face) == 2 for face in faces)
    return original_edges, completion, faces, edge_faces, genus, digons


def _dual_components(face_count, edge_faces, retained):
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
    return len(seen), len(adjacency)


def audit(maximum_width: int):
    width = 4
    tree = set(_base_tree())
    rows = []
    while True:
        original_edges, completion, faces, edge_faces, genus, digons = _augmented_faces(width)
        selected = set(tree) | completion
        complement = set(range(len(edge_faces))) - selected
        reached, face_count = _dual_components(len(faces), edge_faces, complement)
        rows.append({
            "width": width,
            "genus": genus,
            "original_edge_count": len(original_edges),
            "completion_edge_count": len(completion),
            "face_count": face_count,
            "digon_count": digons,
            "selected_edge_count": len(selected),
            "dual_complement_edge_count": len(complement),
            "dual_reached_faces": reached,
            "dual_complement_connected": reached == face_count,
        })
        if width == maximum_width:
            break
        old_width = width
        width += 1
        tree = _embed(tree, old_width, width)
        _, edges = cubic_box((5, width, width))
        edge_index = {(edge.u, edge.v): i for i, edge in enumerate(edges)}
        tree |= {edge_index[pair] for pair in extension_pairs(old_width)}
    return {
        "status": "OBSERVED exact augmented-ribbon dual audit",
        "rows": rows,
        "claim_boundary": (
            "The cographic equivalence is exact.  These finite connectivity rows "
            "do not prove the two parity shell induction."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-width", type=int, default=10)
    args = parser.parse_args()
    print(json.dumps(audit(args.maximum_width), indent=2, sort_keys=True))
