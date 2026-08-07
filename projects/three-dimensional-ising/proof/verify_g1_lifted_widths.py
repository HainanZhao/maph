#!/usr/bin/env python3
"""Independent exact replay of finite-width lifted-matroid G1 witnesses."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from discovery.search_g1_paired_fundamental_cycles import _labels  # noqa: E402
from proof.verify_lane_b_arbitrary_width_frontier import _case, _rank  # noqa: E402
from src.conventions import cubic_box  # noqa: E402


CASES = ((3, 10, 5), (4, 10, 9), (5, 7, 12), (6, 8, 20), (7, 7, 27))
PRIMES = (1_000_000_007, 1_000_000_009)


def _spanning_tree(vertices, edges, selected):
    position = {vertex: index for index, vertex in enumerate(vertices)}
    parent = list(range(len(vertices)))

    def find(value):
        while parent[value] != value:
            parent[value] = parent[parent[value]]
            value = parent[value]
        return value

    tree = []
    for edge_index in selected:
        edge = edges[edge_index]
        left, right = find(position[edge.u]), find(position[edge.v])
        if left != right:
            parent[right] = left
            tree.append(edge_index)
    if len(tree) != len(vertices) - 1:
        raise AssertionError("selected specialization is disconnected")
    return tree


def _fundamental_cycle_labels(vertices, edges, labels, tree, selected):
    adjacency = {vertex: [] for vertex in vertices}
    for edge_index in tree:
        edge = edges[edge_index]
        adjacency[edge.u].append((edge.v, edge_index))
        adjacency[edge.v].append((edge.u, edge_index))
    root = vertices[0]
    path_label = {root: 0}
    stack = [root]
    while stack:
        vertex = stack.pop()
        for neighbour, edge_index in adjacency[vertex]:
            if neighbour not in path_label:
                path_label[neighbour] = path_label[vertex] ^ labels[edge_index]
                stack.append(neighbour)
    return [
        path_label[edges[index].u] ^ path_label[edges[index].v] ^ labels[index]
        for index in selected if index not in set(tree)
    ]


def verify_case(width, length, handle_cut):
    source = ROOT / "discovery" / f"g1-lifted-unified-w{width}-live.json"
    payload = json.loads(source.read_text())
    selected = payload["trimmed_selected_edges"]
    vertices, edges = cubic_box((length, width, width))
    structural = _case(width, length)["length_rows"][-1]
    labels = _labels(structural, edges)
    tree = _spanning_tree(vertices, edges, selected)
    cycle_labels = _fundamental_cycle_labels(vertices, edges, labels, tree, selected)
    m = width * width - 1
    shift = 2 * handle_cut
    left_rank = _rank([label & ((1 << shift) - 1) for label in cycle_labels])
    right_rank = _rank([label >> shift for label in cycle_labels])
    if len(cycle_labels) != m or left_rank != m or right_rank != m:
        raise AssertionError("fundamental-cycle projection certificate failed")
    determinant_exponent = m * (1 << m)
    return {
        "shape": [length, width, width],
        "handle_cut": handle_cut,
        "selected_edge_count": len(selected),
        "tree_edge_count": len(tree),
        "cycle_dimension": len(cycle_labels),
        "left_projection_rank": left_rank,
        "right_projection_rank": right_rank,
        "unnormalized_unit_weight_determinant": f"+2^{determinant_exponent}",
        "determinant_residues": {
            str(prime): pow(2, determinant_exponent, prime) for prime in PRIMES
        },
    }


def verify():
    return {
        "status": "OBSERVED exact finite-width sparse specializations pending promotion",
        "cases": [verify_case(*case) for case in CASES],
        "claim_boundary": (
            "Each row proves generic nonuniform saturation at that width. "
            "The five rows do not prove arbitrary-width G1."
        ),
    }


def main():
    print(json.dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
