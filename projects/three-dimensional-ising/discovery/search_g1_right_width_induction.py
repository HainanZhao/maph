#!/usr/bin/env python3
"""Force a globally compatible right tree across a width increment."""

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
from proof.verify_lane_b_arbitrary_width_frontier import _case, _rank  # noqa: E402
from src.conventions import cubic_box  # noqa: E402


def _load_tree(path, side):
    payload = json.loads(Path(path).read_text())
    if "cases" in payload:
        return payload["cases"][0][side]["selected_tree_edges"]
    return payload["selected"]


def search(old_width, new_width, source, side="right", length=9, layer=4):
    if new_width <= old_width:
        raise ValueError("new width must exceed old width")
    old_tree = _load_tree(source, side)
    _, old_edges = cubic_box((length, old_width, old_width))
    vertices, edges = cubic_box((length, new_width, new_width))
    edge_index = {(edge.u, edge.v): index for index, edge in enumerate(edges)}
    fixed = [edge_index[(old_edges[index].u, old_edges[index].v)] for index in old_tree]

    structural = _case(new_width, length)["length_rows"][-1]
    labels = _labels(structural, edges)
    side_genus = _case(new_width, layer + 1)["length_rows"][-1]["genus"]
    if side == "right":
        side_vertices = [vertex for vertex in vertices if vertex[0] >= layer]
        edge_ids = [
            index for index, edge in enumerate(edges)
            if edge.u[0] >= layer and edge.v[0] >= layer
        ]
        homology = lambda value: value >> (2 * side_genus)
    else:
        side_vertices = [vertex for vertex in vertices if vertex[0] <= layer]
        edge_ids = [
            index for index, edge in enumerate(edges)
            if edge.u[0] <= layer and edge.v[0] <= layer
        ]
        homology = lambda value: value & ((1 << (2 * side_genus)) - 1)
    position = {vertex: index for index, vertex in enumerate(side_vertices)}
    incidence_bits = len(side_vertices) - 1

    def incidence(left, right):
        value = 0
        for vertex in (left, right):
            index = position[vertex]
            if index:
                value ^= 1 << (index - 1)
        return value

    boundary = [(layer, y, z) for y in range(new_width) for z in range(new_width)]
    completion = _basis([incidence(boundary[0], vertex) for vertex in boundary[1:]])
    graphic = {}
    lifted = {}
    for edge_id in edge_ids:
        edge = edges[edge_id]
        column = incidence(edge.u, edge.v)
        graphic[edge_id] = column
        lifted[edge_id] = _reduce(
            column | (homology(labels[edge_id]) << incidence_bits), completion
        )
    fixed_graphic = _basis([graphic[index] for index in fixed])
    fixed_lifted = _basis([lifted[index] for index in fixed])
    fixed_independent = len(fixed_graphic) == len(fixed_lifted) == len(fixed)
    shift = incidence_bits
    mask = (1 << shift) - 1
    fixed_set = set(fixed)
    quotient = [
        (
            index,
            _reduce(graphic[index], fixed_graphic)
            | (_reduce(lifted[index], fixed_lifted) << shift),
        )
        for index in edge_ids if index not in fixed_set
    ]
    certificate = _matroid_intersection(quotient, mask, shift, True)
    needed = len(side_vertices) - 1 - len(fixed)
    additions = [index for index, _ in certificate["selected"]]
    selected = fixed + additions[:needed] if fixed_independent and len(additions) >= needed else []
    return {
        "status": "OBSERVED exact GF(2) global-side width-induction search",
        "old_width": old_width,
        "new_width": new_width,
        "length": length,
        "side": side,
        "source": str(source),
        "fixed_edge_count": len(fixed),
        "fixed_graphic_rank": len(fixed_graphic),
        "fixed_lifted_rank": len(fixed_lifted),
        "fixed_independent": fixed_independent,
        "additional_needed": needed,
        "maximum_additional": len(additions),
        "criterion_met": fixed_independent and len(additions) >= needed,
        "selected": selected,
        "final_graphic_rank": _rank([graphic[index] for index in selected]),
        "final_lifted_rank": _rank([lifted[index] for index in selected]),
        "min_max_partition": [
            certificate["rank_M1_on_complement"],
            certificate["rank_M2_on_reachable"],
        ],
        "claim_boundary": (
            "A successful finite width extension is not an arbitrary-width construction. "
            "A dependent fixed set proves only failure of literal nesting."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--old-width", type=int, required=True)
    parser.add_argument("--new-width", type=int, required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--side", choices=("left", "right"), default="right")
    args = parser.parse_args()
    print(json.dumps(search(**vars(args)), indent=2, sort_keys=True))
