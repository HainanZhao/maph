#!/usr/bin/env python3
"""Light exact audit of the explicit prefix-tree recursion at larger widths.

Unlike the canonical frontier verifier, this computes only raw edge homology
labels.  The terminal path rank is invariant under an invertible homology
coordinate change, so no symplectic normalization or all-q payload is needed.
"""

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
from proof.verify_lane_b_arbitrary_width_frontier import _rank  # noqa: E402
from proof.verify_lane_b_genus3 import (  # noqa: E402
    _cycle_basis,
    _edge_homology_labels,
    _rotation_faces,
)
from src.conventions import cubic_box  # noqa: E402
from src.lane_b_universal_embedding import universal_checkerboard_rotation  # noqa: E402


def _row(width: int, tree: set[int]):
    started = time.monotonic()
    vertices, edges = cubic_box((5, width, width))
    faces, _ = _rotation_faces(
        vertices, edges, universal_checkerboard_rotation(5, width)
    )
    genus = (2 - (len(vertices) - len(edges) + len(faces))) // 2
    labels, face_rank = _edge_homology_labels(
        len(edges), faces, _cycle_basis(vertices, edges), genus
    )
    adjacency = {vertex: [] for vertex in vertices}
    for edge_index in tree:
        edge = edges[edge_index]
        adjacency[edge.u].append((edge.v, edge_index))
        adjacency[edge.v].append((edge.u, edge_index))
    root = (4, 0, 0)
    paths = {root: 0}
    stack = [root]
    while stack:
        vertex = stack.pop()
        for neighbour, edge_index in adjacency[vertex]:
            if neighbour not in paths:
                paths[neighbour] = paths[vertex] ^ labels[edge_index]
                stack.append(neighbour)
    terminal = [
        paths[(4, y, z)]
        for y in range(width)
        for z in range(width)
        if (y, z) != (0, 0)
    ]
    return {
        "width": width,
        "genus": genus,
        "face_boundary_rank": face_rank,
        "tree_connected": len(paths) == len(vertices),
        "tree_edge_count": len(tree),
        "terminal_rank": _rank(terminal),
        "target": width * width - 1,
        "wall_seconds": time.monotonic() - started,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }


def audit(maximum_width: int):
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
        "status": "OBSERVED exact GF(2) raw-homology audit",
        "rows": rows,
        "claim_boundary": (
            "Raw and canonical homology coordinates differ invertibly, so each finite "
            "rank is exact.  No finite maximum width proves the symbolic recursion."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-width", type=int, default=12)
    args = parser.parse_args()
    print(json.dumps(audit(args.maximum_width), indent=2, sort_keys=True))
