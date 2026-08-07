#!/usr/bin/env python3
"""Audit the closed-form common basis inside the recursive prefix tree."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import resource
import sys
import time

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


def excluded_pairs(width: int):
    """Closed-form redundant chords; widths 2k and 2k+1 share the rule."""
    if width < 4:
        raise ValueError("the common-basis formula starts at width four")
    k = width // 2
    result = {((0, 3, 2), (0, 3, 3))}
    for y in range(5, 2 * k, 2):
        result.add(((0, y, 0), (0, y, 1)))
    for a in range(1, k - 2):
        y = 2 * a + 1
        for b in range(a + 2, k):
            z = 2 * b
            result.add(((1, y, z), (1, y, z + 1)))
    return {tuple(sorted(pair)) for pair in result}


def _component_terminal_counts(vertices, edges, retained, terminals):
    adjacency = {vertex: [] for vertex in vertices}
    for edge_index in retained:
        edge = edges[edge_index]
        adjacency[edge.u].append(edge.v)
        adjacency[edge.v].append(edge.u)
    terminal_set = set(terminals)
    unseen = set(vertices)
    counts = []
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        stack = [start]
        count = 0
        while stack:
            vertex = stack.pop()
            count += vertex in terminal_set
            for neighbour in adjacency[vertex]:
                if neighbour in unseen:
                    unseen.remove(neighbour)
                    stack.append(neighbour)
        counts.append(count)
    return sorted(counts)


def _edge_faces(edges, face_walks):
    edge_index = {(edge.u, edge.v): index for index, edge in enumerate(edges)}
    incident = [[] for _ in edges]
    for face, walk in enumerate(face_walks):
        for offset, left in enumerate(walk):
            right = walk[(offset + 1) % len(walk)]
            incident[edge_index[tuple(sorted((left, right)))]] .append(face)
    if any(len(pair) != 2 for pair in incident):
        raise AssertionError("bad face incidence")
    return incident


def _dual_reach(face_count, edge_faces, retained):
    adjacency = [[] for _ in range(face_count)]
    for edge_index in retained:
        left, right = edge_faces[edge_index]
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
    started = time.monotonic()
    vertices, edges = cubic_box((5, width, width))
    faces, face_walks = _rotation_faces(
        vertices, edges, universal_checkerboard_rotation(5, width)
    )
    genus = (2 - (len(vertices) - len(edges) + len(faces))) // 2
    gauge_tree = _gauge_tree(
        len(edges), faces, _cycle_basis(vertices, edges), genus
    )
    edge_index = {(edge.u, edge.v): index for index, edge in enumerate(edges)}
    excluded = {edge_index[pair] for pair in excluded_pairs(width)}
    chords = set(encoder_tree) - gauge_tree
    if not excluded <= chords:
        raise AssertionError("closed-form exclusions are not encoder chords")
    common = chords - excluded
    terminals = [(4, y, z) for y in range(width) for z in range(width)]
    component_counts = _component_terminal_counts(
        vertices, edges, set(encoder_tree) - common, terminals
    )
    dual_retained = set(range(len(edges))) - gauge_tree - common
    dual_reached = _dual_reach(
        len(faces), _edge_faces(edges, face_walks), dual_retained
    )
    return {
        "width": width,
        "genus": genus,
        "chord_count": len(chords),
        "excluded_count": len(excluded),
        "common_basis_count": len(common),
        "target": width * width - 1,
        "encoder_components_after_common_deletion": len(component_counts),
        "each_component_has_one_terminal": component_counts == [1] * (width * width),
        "dual_face_count": len(faces),
        "dual_reached_faces": dual_reached,
        "dual_complement_connected": dual_reached == len(faces),
        "wall_seconds": time.monotonic() - started,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
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
        "status": "OBSERVED exact closed-form common-basis audit",
        "rows": rows,
        "claim_boundary": (
            "The formula is defined for every width.  Finite rows validate but do not "
            "replace the symbolic encoder-component and dual-shell proofs."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-width", type=int, default=20)
    args = parser.parse_args()
    print(json.dumps(audit(args.maximum_width), indent=2, sort_keys=True))
