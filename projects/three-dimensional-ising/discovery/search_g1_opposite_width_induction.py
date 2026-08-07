#!/usr/bin/env python3
"""Exact nested-tree search for the opposite checkerboard prefix phase.

This is a discovery tool.  It asks whether a tree already selected at width
``w`` can be retained verbatim at width ``w+1`` while preserving both the
graphic tree condition and injectivity of the terminal-to-homology map.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from discovery.search_g1_all_rails import _basis, _reduce  # noqa: E402
from discovery.search_g1_paired_fundamental_cycles import (  # noqa: E402
    _matroid_intersection,
)
from proof.verify_lane_b_arbitrary_width_frontier import _rank  # noqa: E402
from proof.verify_lane_b_genus3 import (  # noqa: E402
    _cycle_basis,
    _edge_homology_labels,
    _rotation_faces,
)
from src.conventions import cubic_box  # noqa: E402
from src.lane_b_universal_embedding import universal_checkerboard_rotation  # noqa: E402


def opposite_checkerboard_rotation(width):
    """The local five-layer rotation induced by global layers 1,...,5."""
    parent = universal_checkerboard_rotation(6, width)
    vertices, _ = cubic_box((5, width, width))
    return {
        vertex: tuple(
            (neighbour[0] - 1, neighbour[1], neighbour[2])
            for neighbour in parent[(vertex[0] + 1, vertex[1], vertex[2])]
            if neighbour[0] >= 1
        )
        for vertex in vertices
    }


def _tree_pairs(payload, width):
    if isinstance(payload, list):
        row = next(row for row in payload if row["width"] == width)
        return {tuple(map(tuple, pair)) for pair in row["tree_pairs"]}
    return {tuple(map(tuple, pair)) for pair in payload["tree_pairs"]}


def _search_pairs(old_width, new_width, fixed_pairs):
    if new_width <= old_width:
        raise ValueError("new width must exceed old width")
    vertices, edges = cubic_box((5, new_width, new_width))
    edge_index = {(edge.u, edge.v): index for index, edge in enumerate(edges)}
    fixed = [edge_index[pair] for pair in sorted(fixed_pairs)]
    faces, _ = _rotation_faces(
        vertices, edges, opposite_checkerboard_rotation(new_width)
    )
    genus = (2 - (len(vertices) - len(edges) + len(faces))) // 2
    labels, _ = _edge_homology_labels(
        len(edges), faces, _cycle_basis(vertices, edges), genus
    )

    position = {vertex: index for index, vertex in enumerate(vertices)}
    incidence_bits = len(vertices) - 1

    def incidence(left, right):
        value = 0
        for vertex in (left, right):
            index = position[vertex]
            if index:
                value ^= 1 << (index - 1)
        return value

    terminals = [(4, y, z) for y in range(new_width) for z in range(new_width)]
    completion = _basis([incidence(terminals[0], vertex) for vertex in terminals[1:]])
    graphic = []
    lifted = []
    for edge, label in zip(edges, labels):
        boundary = incidence(edge.u, edge.v)
        graphic.append(boundary)
        lifted.append(_reduce(boundary | (label << incidence_bits), completion))

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
        for index in range(len(edges))
        if index not in fixed_set
    ]
    certificate = _matroid_intersection(quotient, mask, shift, True)
    additions = [index for index, _ in certificate["selected"]]
    needed = len(vertices) - 1 - len(fixed)
    selected = fixed + additions[:needed] if fixed_independent and len(additions) >= needed else []
    return {
        "status": "OBSERVED exact GF(2) opposite-phase width-induction search",
        "old_width": old_width,
        "new_width": new_width,
        "fixed_edge_count": len(fixed),
        "fixed_graphic_rank": len(fixed_graphic),
        "fixed_lifted_rank": len(fixed_lifted),
        "fixed_independent": fixed_independent,
        "additional_needed": needed,
        "maximum_additional": len(additions),
        "criterion_met": fixed_independent and len(additions) >= needed,
        "selected_tree_pairs": [
            [list(edges[index].u), list(edges[index].v)] for index in selected
        ],
        "final_graphic_rank": _rank([graphic[index] for index in selected]),
        "final_lifted_rank": _rank([lifted[index] for index in selected]),
        "min_max_partition": [
            certificate["rank_M1_on_complement"],
            certificate["rank_M2_on_reachable"],
        ],
        "claim_boundary": (
            "A successful finite extension is not an arbitrary-width construction. "
            "A dependent fixed set disproves only literal nesting."
        ),
    }


def search(old_width, new_width, source):
    old_payload = json.loads(Path(source).read_text())
    return _search_pairs(old_width, new_width, _tree_pairs(old_payload, old_width))


def chain(start_width, final_width, source):
    payload = json.loads(Path(source).read_text())
    pairs = _tree_pairs(payload, start_width)
    rows = []
    for old_width in range(start_width, final_width):
        row = _search_pairs(old_width, old_width + 1, pairs)
        rows.append(row)
        if not row["criterion_met"]:
            break
        pairs = {
            tuple(map(tuple, pair)) for pair in row["selected_tree_pairs"]
        }
    return {
        "status": "OBSERVED exact GF(2) nested opposite-phase tree chain",
        "rows": rows,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--old-width", type=int, required=True)
    parser.add_argument("--new-width", type=int, required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--chain-to", type=int)
    args = parser.parse_args()
    if args.chain_to is None:
        print(json.dumps(search(args.old_width, args.new_width, args.source), indent=2, sort_keys=True))
    else:
        print(json.dumps(chain(args.old_width, args.chain_to, args.source), indent=2, sort_keys=True))
