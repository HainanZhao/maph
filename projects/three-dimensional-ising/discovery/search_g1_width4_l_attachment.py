#!/usr/bin/env python3
"""Structured w=3 -> w=4 tree extensions on the seven new slice vertices."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import random
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from discovery.search_g1_paired_fundamental_cycles import (  # noqa: E402
    _fundamental_labels,
    _labels,
    _matroid_intersection,
)
from discovery.search_g1_width_induction import _basis, _reduce  # noqa: E402
from proof.verify_g1_paired_cycle_w3 import CHORDS, TREE_EDGES  # noqa: E402
from proof.verify_lane_b_arbitrary_width_frontier import _case, _rank  # noqa: E402
from src.conventions import cubic_box  # noqa: E402


def search(trials: int, seed: int):
    length = 10
    old_vertices, old_edges = cubic_box((length, 3, 3))
    vertices, edges = cubic_box((length, 4, 4))
    edge_index = {(edge.u, edge.v): index for index, edge in enumerate(edges)}
    fixed_tree = {edge_index[(old_edges[index].u, old_edges[index].v)] for index in TREE_EDGES}
    old_chords = [edge_index[(old_edges[index].u, old_edges[index].v)] for index in CHORDS]
    new_sites = [(y, z) for y in range(4) for z in range(4) if y == 3 or z == 3]
    longitudinal = {
        edge_index[((layer, y, z), (layer + 1, y, z))]
        for y, z in new_sites for layer in range(length - 1)
    }
    # Component graph after contracting the old 3x3x10 tree to ROOT=-1.
    component_edges = []
    for site in new_sites:
        y, z = site
        old_neighbours = []
        if y == 3 and z < 3:
            old_neighbours.append((2, z))
        if z == 3 and y < 3:
            old_neighbours.append((y, 2))
        for old in old_neighbours:
            component_edges.append((-1, site, old))
    for left in new_sites:
        for right in new_sites:
            if left < right and abs(left[0] - right[0]) + abs(left[1] - right[1]) == 1:
                component_edges.append((left, right, None))

    structural = _case(4, length)["length_rows"][-1]
    labels = _labels(structural, edges)
    shift = 18
    mask = (1 << shift) - 1
    rng = random.Random(seed)
    best = None
    nodes = [-1] + new_sites
    node_index = {node: index for index, node in enumerate(nodes)}
    for trial in range(trials):
        parent = list(range(len(nodes)))

        def find(value):
            while parent[value] != value:
                parent[value] = parent[parent[value]]
                value = parent[value]
            return value

        types = component_edges[:]
        rng.shuffle(types)
        component_tree = []
        for left, right, old in types:
            a, b = find(node_index[left]), find(node_index[right])
            if a != b:
                parent[b] = a
                component_tree.append((left, right, old, rng.randrange(length)))
        if len(component_tree) != 7:
            raise AssertionError("new-site component tree is not spanning")
        attachment_edges = set()
        for left, right, old, layer in component_tree:
            if left == -1:
                new = right
                pair = tuple(sorted(((layer, *old), (layer, *new))))
            else:
                pair = tuple(sorted(((layer, *left), (layer, *right))))
            attachment_edges.add(edge_index[pair])
        tree = fixed_tree | longitudinal | attachment_edges
        if len(tree) != len(vertices) - 1:
            raise AssertionError("structured extension has the wrong tree size")
        fundamental = _fundamental_labels(vertices, edges, labels, tree)
        by_edge = dict(fundamental)
        old_labels = [by_edge[index] for index in old_chords]
        if _rank([value & mask for value in old_labels]) != 8 or _rank(
            [value >> shift for value in old_labels]
        ) != 8:
            raise AssertionError("structured extension lost the old paired core")
        left_basis = _basis([value & mask for value in old_labels])
        right_basis = _basis([value >> shift for value in old_labels])
        quotient = []
        original = {}
        for edge, value in fundamental:
            if edge in old_chords:
                continue
            packed = _reduce(value & mask, left_basis) | (
                _reduce(value >> shift, right_basis) << shift
            )
            quotient.append((edge, packed))
            original[edge] = value
        additional = _matroid_intersection(quotient, mask, shift)
        score = 8 + len(additional)
        if best is None or score > best["total_common_rank"]:
            selected = [edge for edge, _ in additional]
            best = {
                "trial": trial,
                "total_common_rank": score,
                "additional_rank": len(additional),
                "component_tree_with_layers": component_tree,
                "tree_edges": sorted(tree),
                "old_chords": old_chords,
                "old_fundamental_labels": old_labels,
                "additional_chords": selected,
                "additional_full_labels": [original[edge] for edge in selected],
                "additional_quotient_labels": [value for _, value in additional],
            }
            if score == 15:
                break
    return {
        "status": "OBSERVED randomized exact GF(2) structured construction search",
        "shape": [length, 4, 4],
        "handle_cut": 9,
        "old_core_rank": 8,
        "target": 15,
        "trials": trials,
        "seed": seed,
        "component_edge_types": component_edges,
        "best": best,
        "claim_boundary": (
            "A score 15 witness is exact. A lower score only falsifies the sampled L-attachment "
            "trees and layer assignments, not the general paired-cycle criterion."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=20260807)
    args = parser.parse_args()
    print(json.dumps(search(args.trials, args.seed), indent=2, sort_keys=True))
