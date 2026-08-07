#!/usr/bin/env python3
"""Audit the explicit w -> w+2 odd-width prefix-tree extension."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from discovery.search_g1_paired_fundamental_cycles import _labels  # noqa: E402
from proof.verify_lane_b_arbitrary_width_frontier import _case, _rank  # noqa: E402
from src.conventions import cubic_box  # noqa: E402


def extension_pairs(old_width):
    """Edges added when adjoining the last two rows and columns at length 4."""
    o = old_width
    if o < 5 or o % 2 == 0:
        raise ValueError("the explicit extension is for odd old_width >= 5")
    width = o + 2
    result = set()

    def add(axis, x, y, z):
        left = (x, y, z)
        right = list(left)
        right[axis] += 1
        result.add(tuple(sorted((left, tuple(right)))))

    # Layer zero.
    for y in range(0, o - 1, 2):
        for z in (o, o + 1):
            add(1, 0, y, z)
    add(1, 0, 1, o + 1)
    for y in range(3, o - 1, 2):
        add(1, 0, y, o)
    for z in list(range(1, o - 1, 2)) + [o, o + 1]:
        add(1, 0, o - 1, z)
    for z in range(width):
        add(1, 0, o, z)
    for y in range(2, o, 2):
        add(2, 0, y, o)
    for z in range(1, o - 1, 2):
        add(2, 0, o, z)
    for z in (o, o + 1):
        add(0, 0, 0, z)
    add(0, 0, 1, o)
    for y in range(2, o):
        for z in (o, o + 1):
            add(0, 0, y, z)
    for y in (o, o + 1):
        for z in range(width):
            add(0, 0, y, z)

    # Layer one and its outgoing rails.
    add(1, 1, 0, o + 1)
    for y in (1, 3):
        if y < o:
            add(2, 1, y, o - 1)
    add(2, 1, o, 0)
    for y in range(o):
        for z in (o, o + 1):
            add(0, 1, y, z)
    for y in (o, o + 1):
        for z in range(width):
            add(0, 1, y, z)

    # Layer two has only outgoing rails.
    add(0, 2, 0, o)
    for y in range(1, o, 2):
        add(0, 2, y, o + 1)
    for z in range(0, o + 2, 2):
        add(0, 2, o, z)
    add(0, 2, o + 1, o)

    # Terminal layer.
    for y in range(o - 1):
        add(1, 3, y, o)
    for z in list(range(1, o, 2)) + [o]:
        add(1, 3, o - 1, z)
    for z in range(0, o, 2):
        add(1, 3, o, z)
    for y in range(0, o, 2):
        add(2, 3, y, o)
    for z in list(range(1, o, 2)) + [o]:
        add(2, 3, o + 1, z)
    return result


def _base_tree():
    payload = json.loads((ROOT / "discovery/g1-prefix-encoder-w5-live.json").read_text())
    return next(row["selected_tree_edges"] for row in payload["rows"] if row["length"] == 4)


def _embed_tree(tree, old_width, new_width):
    _, old_edges = cubic_box((4, old_width, old_width))
    _, new_edges = cubic_box((4, new_width, new_width))
    index = {(edge.u, edge.v): i for i, edge in enumerate(new_edges)}
    return {index[(old_edges[i].u, old_edges[i].v)] for i in tree}


def _tree_rank(width, selected):
    vertices, edges = cubic_box((4, width, width))
    row = _case(width, 4)["length_rows"][-1]
    labels = _labels(row, edges)
    adjacency = {vertex: [] for vertex in vertices}
    for index in selected:
        edge = edges[index]
        adjacency[edge.u].append((edge.v, index))
        adjacency[edge.v].append((edge.u, index))
    paths = {vertices[0]: 0}
    stack = [vertices[0]]
    while stack:
        vertex = stack.pop()
        for neighbour, edge_index in adjacency[vertex]:
            if neighbour not in paths:
                paths[neighbour] = paths[vertex] ^ labels[edge_index]
                stack.append(neighbour)
    boundary = [(3, y, z) for y in range(width) for z in range(width)]
    rank = _rank([paths[vertex] ^ paths[boundary[0]] for vertex in boundary[1:]])
    return {
        "edge_count": len(selected),
        "vertex_count": len(vertices),
        "connected": len(paths) == len(vertices),
        "acyclic": len(selected) == len(vertices) - 1 and len(paths) == len(vertices),
        "genus": row["genus"],
        "terminal_homology_rank": rank,
        "target": width * width - 1,
    }


def audit(maximum_width):
    tree = set(_base_tree())
    width = 5
    rows = [{"width": width, **_tree_rank(width, tree)}]
    while width + 2 <= maximum_width:
        new_width = width + 2
        tree = _embed_tree(tree, width, new_width)
        _, edges = cubic_box((4, new_width, new_width))
        index = {(edge.u, edge.v): i for i, edge in enumerate(edges)}
        additions = {index[pair] for pair in extension_pairs(width)}
        tree |= additions
        width = new_width
        rows.append({
            "width": width,
            "extension_edge_count": len(additions),
            **_tree_rank(width, tree),
        })
    return {
        "status": "OBSERVED exact GF(2) explicit odd-width induction audit",
        "maximum_width": maximum_width,
        "rows": rows,
        "claim_boundary": (
            "The formula is explicit for every odd width, but finite audits do not replace "
            "a symbolic proof of its homology-rank increment."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-width", type=int, default=9)
    args = parser.parse_args()
    print(json.dumps(audit(args.maximum_width), indent=2, sort_keys=True))
