#!/usr/bin/env python3
"""Exact search for homology-injective trees on two sides of a flat separator."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from discovery.search_g1_all_rails import _basis, _reduce  # noqa: E402
from discovery.search_g1_paired_fundamental_cycles import (  # noqa: E402
    _labels,
    _matroid_intersection,
)
from proof.verify_lane_b_arbitrary_width_frontier import _case  # noqa: E402
from src.conventions import cubic_box  # noqa: E402


def _side(width, vertices, edges, labels, layer, handle_cut, side):
    if side == "left":
        side_vertices = [vertex for vertex in vertices if vertex[0] <= layer]
        edge_ids = [
            index for index, edge in enumerate(edges)
            if edge.u[0] <= layer and edge.v[0] <= layer
        ]
        homology = lambda value: value & ((1 << (2 * handle_cut)) - 1)
    else:
        side_vertices = [vertex for vertex in vertices if vertex[0] >= layer]
        edge_ids = [
            index for index, edge in enumerate(edges)
            if edge.u[0] >= layer and edge.v[0] >= layer
        ]
        homology = lambda value: value >> (2 * handle_cut)
    position = {vertex: index for index, vertex in enumerate(side_vertices)}
    incidence_bits = len(side_vertices) - 1

    def incidence(left, right):
        value = 0
        for vertex in (left, right):
            index = position[vertex]
            if index:
                value ^= 1 << (index - 1)
        return value

    boundary = [(layer, y, z) for y in range(width) for z in range(width)]
    root = boundary[0]
    completions = [incidence(root, vertex) for vertex in boundary[1:]]
    completion_basis = _basis(completions)
    if len(completion_basis) != width * width - 1:
        raise AssertionError("abstract separator completion lost rank")
    shift = incidence_bits
    mask = (1 << shift) - 1
    vectors = []
    for edge_id in edge_ids:
        edge = edges[edge_id]
        graphic = incidence(edge.u, edge.v)
        lifted = graphic | (homology(labels[edge_id]) << incidence_bits)
        contracted = _reduce(lifted, completion_basis)
        vectors.append((edge_id, graphic | (contracted << shift)))
    certificate = _matroid_intersection(vectors, mask, shift, True)
    selected = [edge_id for edge_id, _ in certificate["selected"]]
    target = len(side_vertices) - 1
    return {
        "vertex_count": len(side_vertices),
        "edge_count": len(edge_ids),
        "target_tree_edges": target,
        "maximum_common_size": len(selected),
        "criterion_met": len(selected) == target,
        "selected_tree_edges": selected if len(selected) == target else [],
        "min_max_partition": [
            certificate["rank_M1_on_complement"],
            certificate["rank_M2_on_reachable"],
        ],
    }


def search(width, length, handle_cut, separator_layer=None):
    row = _case(width, length)["length_rows"][-1]
    vertices, edges = cubic_box((length, width, width))
    labels = _labels(row, edges)
    cases = []
    layers = [separator_layer] if separator_layer is not None else range(length)
    for layer in layers:
        left = _side(width, vertices, edges, labels, layer, handle_cut, "left")
        right = _side(width, vertices, edges, labels, layer, handle_cut, "right")
        cases.append({
            "separator_layer": layer,
            "left": left,
            "right": right,
            "both_met": left["criterion_met"] and right["criterion_met"],
        })
    return {
        "status": "OBSERVED exact GF(2) relative-tree search",
        "shape": [length, width, width],
        "genus": row["genus"],
        "handle_cut": handle_cut,
        "cases": cases,
        "claim_boundary": (
            "A successful row proves a flat-separator tree specialization at this width. "
            "Failure does not rule out a moving canonical separator or a general lifted set."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", type=int, required=True)
    parser.add_argument("--length", type=int, required=True)
    parser.add_argument("--handle-cut", type=int, required=True)
    parser.add_argument("--separator-layer", type=int)
    args = parser.parse_args()
    print(json.dumps(search(**vars(args)), indent=2, sort_keys=True))
