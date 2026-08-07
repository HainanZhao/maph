#!/usr/bin/env python3
"""Exact GF(2) audit of the lifted-matroid sufficient criterion for G1.

This is discovery code.  It constructs no exponential flattening.  The two
represented matroids have columns (boundary(e), left-homology(e)) and
(boundary(e), right-homology(e)).  A connected common-independent set of
size |V|-1+w^2-1 has a cycle space of dimension w^2-1 on which both homology
projections are injective.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from discovery.search_g1_paired_fundamental_cycles import (  # noqa: E402
    _labels,
    _matroid_intersection,
)
from proof.verify_lane_b_arbitrary_width_frontier import _case, _rank  # noqa: E402
from src.conventions import cubic_box  # noqa: E402


def _incidence_columns(vertices, edges):
    """Pinned unoriented incidence columns over GF(2)."""
    position = {vertex: index for index, vertex in enumerate(vertices)}
    columns = []
    for edge in edges:
        value = 0
        for vertex in (edge.u, edge.v):
            index = position[vertex]
            if index:
                value ^= 1 << (index - 1)
        columns.append(value)
    return columns


def _connected(vertices, edges, selected):
    adjacency = {vertex: [] for vertex in vertices}
    for index in selected:
        edge = edges[index]
        adjacency[edge.u].append(edge.v)
        adjacency[edge.v].append(edge.u)
    seen = {vertices[0]}
    stack = [vertices[0]]
    while stack:
        for neighbour in adjacency[stack.pop()]:
            if neighbour not in seen:
                seen.add(neighbour)
                stack.append(neighbour)
    return len(seen) == len(vertices)


def _trim_connected(vertices, edges, selected, target):
    """Delete cycle edges until target size, retaining common independence."""
    selected = set(selected)
    while len(selected) > target:
        removed = next(
            (edge for edge in sorted(selected, reverse=True)
             if _connected(vertices, edges, selected - {edge})),
            None,
        )
        if removed is None:
            raise AssertionError("cannot trim a connected set above tree size")
        selected.remove(removed)
    return sorted(selected)


def audit(width: int, length: int, handle_cut: int | None):
    started = time.monotonic()
    structural = _case(width, length)["length_rows"][-1]
    genus = structural["genus"]
    if handle_cut is None:
        handle_cut = genus // 2
    left_bits = 2 * handle_cut
    right_bits = 2 * (genus - handle_cut)
    target_cycles = width * width - 1
    if min(left_bits, right_bits) < target_cycles:
        raise ValueError("the selected cut has too few coordinates on one side")

    vertices, edges = cubic_box((length, width, width))
    incidence = _incidence_columns(vertices, edges)
    labels = _labels(structural, edges)
    incidence_bits = len(vertices) - 1
    left_mask = (1 << (incidence_bits + left_bits)) - 1
    right_shift = incidence_bits + left_bits
    vectors = []
    for index, (boundary, label) in enumerate(zip(incidence, labels)):
        left = label & ((1 << left_bits) - 1)
        right = label >> left_bits
        packed = boundary | (left << incidence_bits) | (
            (boundary | (right << incidence_bits)) << right_shift
        )
        vectors.append((index, packed))

    certificate = _matroid_intersection(vectors, left_mask, right_shift, True)
    maximum = certificate["selected"]
    selected = [index for index, _ in maximum]
    target_size = len(vertices) - 1 + target_cycles
    enough = len(selected) >= target_size
    selected_connected = _connected(vertices, edges, selected)
    trimmed = _trim_connected(vertices, edges, selected, target_size) if enough else []

    left_columns = [vectors[index][1] & left_mask for index in trimmed]
    right_columns = [vectors[index][1] >> right_shift for index in trimmed]
    incidence_rank = _rank([incidence[index] for index in trimmed])
    return {
        "status": "OBSERVED exact GF(2) lifted-matroid audit",
        "shape": [length, width, width],
        "genus": genus,
        "handle_cut": handle_cut,
        "left_coordinate_dimension": left_bits,
        "right_coordinate_dimension": right_bits,
        "vertex_count": len(vertices),
        "edge_count": len(edges),
        "target_cycle_dimension": target_cycles,
        "target_common_independent_size": target_size,
        "maximum_common_independent_size": len(selected),
        "maximum_is_connected": selected_connected,
        "min_max_partition": {
            "rank_M1_on_complement": certificate["rank_M1_on_complement"],
            "rank_M2_on_reachable": certificate["rank_M2_on_reachable"],
            "reachable_edges": certificate["reachable_indices"],
            "complement_edges": certificate["complement_indices"],
        },
        "criterion_met": enough,
        "trimmed_selected_edges": trimmed,
        "trimmed_connected": bool(trimmed) and _connected(vertices, edges, trimmed),
        "trimmed_incidence_rank": incidence_rank,
        "trimmed_cycle_dimension": len(trimmed) - incidence_rank,
        "trimmed_left_lifted_rank": _rank(left_columns),
        "trimmed_right_lifted_rank": _rank(right_columns),
        "wall_seconds": time.monotonic() - started,
        "claim_boundary": (
            "Meeting the criterion proves one sparse specialization at this finite width. "
            "Finite-width audits do not prove the arbitrary-width G1 theorem."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", type=int, required=True)
    parser.add_argument("--length", type=int, required=True)
    parser.add_argument("--handle-cut", type=int)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit(args.width, args.length, args.handle_cut)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")
