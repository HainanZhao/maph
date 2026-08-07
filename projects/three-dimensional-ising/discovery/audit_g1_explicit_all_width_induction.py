#!/usr/bin/env python3
"""Audit explicit parity-periodic w -> w+1 prefix-tree extensions at length five."""

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
    o = old_width
    if o < 4:
        raise ValueError("use the separate width-three base")
    result = set()

    def add(axis, x, y, z):
        left = (x, y, z)
        right = list(left)
        right[axis] += 1
        result.add(tuple(sorted((left, tuple(right)))))

    def all_shell_rails(x):
        for z in range(o + 1):
            add(0, x, o, z)
        for y in range(o):
            add(0, x, y, o)

    if o % 2 == 0:
        # First three slab transitions retain the complete new L-shell.
        for x in range(3):
            all_shell_rails(x)
        for z in range(o + 1):
            add(1, 0, o - 1, z)
        add(1, 0, 0, o)
        for y in range(1, o, 2):
            add(1, 0, y, o)
        for y in range(2, o, 2):
            add(2, 0, y, o - 1)
        add(1, 1, o - 2, o)
        add(0, 3, o, o)
        for y in range(2, o, 2):
            add(0, 3, y, o)
        for z in range(0, o, 2):
            add(1, 4, o - 1, z)
            add(1, 4, z, o)
            add(2, 4, o, z)
        add(2, 4, 0, o - 1)
    else:
        if o < 5:
            raise ValueError("the odd rule starts at width five")
        for x in range(3):
            all_shell_rails(x)
        for z in range(3, o + 1, 2):
            add(1, 0, o - 1, z)
        for y in {0, o - 2, *range(2, o, 2)}:
            add(1, 0, y, o)
        add(2, 0, o, 0)
        for z in range(1, o, 2):
            add(2, 0, o, z)
        add(1, 1, o - 1, 1)
        for y in range(1, o, 2):
            add(2, 1, y, o - 1)
        for z in range(0, o, 2):
            add(0, 3, o, z)
        add(0, 3, o, o)
        add(0, 3, 0, o)
        for z in range(1, o, 2):
            add(1, 4, o - 1, z)
            add(1, 4, z, o)
        for y in range(1, o, 2):
            add(2, 4, y, o - 1)
    expected = 10 * o + 5
    if len(result) != expected:
        raise AssertionError(f"extension count {len(result)} != {expected}")
    return result


def _base_tree():
    payload = json.loads((ROOT / "discovery/g1-prefix-encoder-w4-live.json").read_text())
    return next(row["selected_tree_edges"] for row in payload["rows"] if row["length"] == 5)


def _embed(tree, old_width, new_width):
    _, old_edges = cubic_box((5, old_width, old_width))
    _, new_edges = cubic_box((5, new_width, new_width))
    index = {(edge.u, edge.v): i for i, edge in enumerate(new_edges)}
    return {index[(old_edges[i].u, old_edges[i].v)] for i in tree}


def _rank_row(width, tree):
    vertices, edges = cubic_box((5, width, width))
    structural = _case(width, 5)["length_rows"][-1]
    labels = _labels(structural, edges)
    adjacency = {vertex: [] for vertex in vertices}
    for index in tree:
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
    boundary = [(4, y, z) for y in range(width) for z in range(width)]
    rank = _rank([paths[v] ^ paths[boundary[0]] for v in boundary[1:]])
    return {
        "width": width,
        "vertex_count": len(vertices),
        "edge_count": len(tree),
        "connected": len(paths) == len(vertices),
        "acyclic": len(tree) == len(vertices) - 1 and len(paths) == len(vertices),
        "genus": structural["genus"],
        "terminal_homology_rank": rank,
        "target": width * width - 1,
    }


def audit(maximum_width):
    width = 4
    tree = set(_base_tree())
    rows = [_rank_row(width, tree)]
    while width < maximum_width:
        new_width = width + 1
        tree = _embed(tree, width, new_width)
        _, edges = cubic_box((5, new_width, new_width))
        index = {(edge.u, edge.v): i for i, edge in enumerate(edges)}
        additions = {index[pair] for pair in extension_pairs(width)}
        tree |= additions
        width = new_width
        rows.append({"extension_edge_count": len(additions), **_rank_row(width, tree)})
    return {
        "status": "OBSERVED exact GF(2) explicit all-width induction audit",
        "maximum_width": maximum_width,
        "rows": rows,
        "claim_boundary": (
            "The edge formula is defined for every width >=4. Finite exact rows do not "
            "replace the symbolic proof of the homology-rank increment."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-width", type=int, default=8)
    args = parser.parse_args()
    print(json.dumps(audit(args.maximum_width), indent=2, sort_keys=True))
