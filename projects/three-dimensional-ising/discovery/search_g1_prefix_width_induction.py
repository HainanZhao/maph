#!/usr/bin/env python3
"""Extend an exact odd-width prefix encoder from w to w+2."""

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


def _source_tree(width, length):
    payload = json.loads(
        (ROOT / "discovery" / f"g1-prefix-encoder-w{width}-live.json").read_text()
    )
    row = next(item for item in payload["rows"] if item["length"] == length)
    if not row["criterion_met"]:
        raise ValueError("source row is not a full encoder")
    return row["selected_tree_edges"]


def search(old_width, length, delta=2):
    new_width = old_width + delta
    old_vertices, old_edges = cubic_box((length, old_width, old_width))
    vertices, edges = cubic_box((length, new_width, new_width))
    edge_index = {(edge.u, edge.v): index for index, edge in enumerate(edges)}
    fixed = [
        edge_index[(old_edges[index].u, old_edges[index].v)]
        for index in _source_tree(old_width, length)
    ]
    row = _case(new_width, length)["length_rows"][-1]
    labels = _labels(row, edges)
    position = {vertex: index for index, vertex in enumerate(vertices)}
    incidence_bits = len(vertices) - 1

    def incidence(left, right):
        value = 0
        for vertex in (left, right):
            index = position[vertex]
            if index:
                value ^= 1 << (index - 1)
        return value

    boundary = [
        (length - 1, y, z) for y in range(new_width) for z in range(new_width)
    ]
    root = boundary[0]
    completion_basis = _basis([incidence(root, vertex) for vertex in boundary[1:]])
    graphic = []
    lifted = []
    for edge, label in zip(edges, labels):
        column = incidence(edge.u, edge.v)
        graphic.append(column)
        lifted.append(_reduce(column | (label << incidence_bits), completion_basis))
    fixed_graphic = _basis([graphic[index] for index in fixed])
    fixed_lifted = _basis([lifted[index] for index in fixed])
    fixed_independent = len(fixed_graphic) == len(fixed_lifted) == len(fixed)
    shift = incidence_bits
    mask = (1 << shift) - 1
    quotient = [
        (
            index,
            _reduce(graphic[index], fixed_graphic)
            | (_reduce(lifted[index], fixed_lifted) << shift),
        )
        for index in range(len(edges)) if index not in set(fixed)
    ]
    certificate = _matroid_intersection(quotient, mask, shift, True)
    additional = [index for index, _ in certificate["selected"]]
    needed = len(vertices) - 1 - len(fixed)
    selected = fixed + additional[:needed]
    return {
        "status": "OBSERVED exact GF(2) width-induction search",
        "old_width": old_width,
        "new_width": new_width,
        "length": length,
        "fixed_edge_count": len(fixed),
        "fixed_common_independent": fixed_independent,
        "additional_needed": needed,
        "maximum_additional": len(additional),
        "criterion_met": fixed_independent and len(additional) >= needed,
        "selected_tree_edges": selected if fixed_independent and len(additional) >= needed else [],
        "final_graphic_rank": _rank([graphic[index] for index in selected]),
        "final_contracted_lifted_rank": _rank([lifted[index] for index in selected]),
        "min_max_partition": [
            certificate["rank_M1_on_complement"],
            certificate["rank_M2_on_reachable"],
        ],
        "claim_boundary": (
            "A successful row is one exact width-extension witness. "
            "It does not prove that the extension exists for every odd width."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--old-width", type=int, required=True)
    parser.add_argument("--length", type=int, default=4)
    parser.add_argument("--delta", type=int, default=2)
    args = parser.parse_args()
    print(json.dumps(search(**vars(args)), indent=2, sort_keys=True))
