#!/usr/bin/env python3
"""Exact GF(2) audit of the boundary--homology relation behind G1.

This is discovery code.  It asks whether arbitrary partial chains, rather
than the previously tested single-tree specialization, contain a linear
section from even separator masks to distinct emitted homology labels.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.verify_lane_b_arbitrary_width_frontier import _case, _nullspace, _rank
from src.conventions import cubic_box


def _edge_key(edge) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    return edge.u, edge.v


def _atomic_labels(row: dict[str, object], edges) -> list[int]:
    support = row["atomic_coordinate_edge_support"]
    by_edge: dict[tuple[tuple[int, int, int], tuple[int, int, int]], int] = {}
    for bit_text, pairs in support.items():
        bit = int(bit_text)
        for pair in pairs:
            key = tuple(pair[0]), tuple(pair[1])
            by_edge[key] = by_edge.get(key, 0) | (1 << bit)
    return [by_edge.get(_edge_key(edge), 0) for edge in edges]


def _tree_completion(width: int, layer: int, edges, labels) -> list[int]:
    """Return homology labels of root paths in a fixed slice tree."""
    index = {_edge_key(edge): position for position, edge in enumerate(edges)}
    result = [0] * (width * width)
    # Root (0,0); first walk in y at z=0, then in z.
    for y in range(width):
        for z in range(width):
            value = 0
            for yy in range(y):
                key = tuple(sorted(((layer, yy, 0), (layer, yy + 1, 0))))
                value ^= labels[index[key]]
            for zz in range(z):
                key = tuple(sorted(((layer, y, zz), (layer, y, zz + 1))))
                value ^= labels[index[key]]
            result[width * y + z] = value
    return result


def _side_relation(length: int, width: int, row: dict[str, object], cut: int,
                   emitted_bits: int, side: str) -> dict[str, int | bool]:
    vertices, edges = cubic_box((length, width, width))
    labels = _atomic_labels(row, edges)
    if side == "left":
        chosen = [i for i, edge in enumerate(edges) if edge.u[0] <= cut and edge.v[0] <= cut]
        interior = [vertex for vertex in vertices if vertex[0] < cut]
        interface_layer = cut
    else:
        chosen = [i for i, edge in enumerate(edges) if edge.u[0] >= cut and edge.v[0] >= cut]
        interior = [vertex for vertex in vertices if vertex[0] > cut]
        interface_layer = cut
    local_index = {edge_index: local for local, edge_index in enumerate(chosen)}
    incidence_rows = []
    for vertex in interior:
        incidence_rows.append(sum(
            1 << local_index[index]
            for index in chosen
            if edges[index].u == vertex or edges[index].v == vertex
        ))
    partial_basis = _nullspace(incidence_rows, len(chosen))
    completion = _tree_completion(width, interface_layer, edges, labels)
    output_vectors = []
    boundary_vectors = []
    homology_vectors = []
    for chain in partial_basis:
        boundary = 0
        homology = 0
        for local, edge_index in enumerate(chosen):
            if not ((chain >> local) & 1):
                continue
            edge = edges[edge_index]
            homology ^= labels[edge_index]
            if edge.u[0] == interface_layer:
                boundary ^= 1 << (width * edge.u[1] + edge.u[2])
            if edge.v[0] == interface_layer:
                boundary ^= 1 << (width * edge.v[1] + edge.v[2])
        # Close the interface boundary by the fixed root-path tree.  The root
        # contribution vanishes because the boundary mask has even parity.
        for vertex_index in range(1, width * width):
            if (boundary >> vertex_index) & 1:
                homology ^= completion[vertex_index]
        homology &= (1 << emitted_bits) - 1
        boundary_vectors.append(boundary)
        homology_vectors.append(homology)
        output_vectors.append(boundary | (homology << (width * width)))

    mask_rank = _rank(boundary_vectors)
    homology_rank = _rank(homology_vectors)
    relation_rank = _rank(output_vectors)
    target = width * width - 1
    # For a linear relation R <= M+H surjective onto M, an injective linear
    # section M -> H exists iff dim(proj_H R) >= dim M.  This is recorded as
    # a candidate lemma; this script only performs the exact rank audit.
    return {
        "partial_chain_dimension": len(partial_basis),
        "mask_rank": mask_rank,
        "homology_projection_rank": homology_rank,
        "relation_rank": relation_rank,
        "target_mask_dimension": target,
        "injective_section_rank_criterion": mask_rank == target and homology_rank >= target,
    }


def audit(width: int, length: int) -> dict[str, object]:
    case = _case(width, length)
    row = case["length_rows"][-1]
    genus = row["genus"]
    candidates = []
    for witness_row in row["pair_cut_spatial_witnesses"]:
        handle_cut = witness_row["after_handle"]
        if 2 * handle_cut < width * width - 1:
            continue
        if 2 * (genus - handle_cut) < width * width - 1:
            continue
        for cut in witness_row["layer_cuts"]:
            candidates.append({
                "handle_cut": handle_cut,
                "spatial_cut": cut,
                "left": _side_relation(length, width, row, cut, 2 * handle_cut, "left"),
                # Reindexing the future homology bits does not change ranks;
                # retain all bits here, then report the available dimension.
                "right": _side_relation(length, width, row, cut + 1, 2 * genus, "right"),
            })
    return {
        "status": "OBSERVED exact GF(2) discovery audit",
        "width": width,
        "length": length,
        "genus": genus,
        "candidates": candidates,
        "claim_boundary": (
            "The ranks are exact.  The injective-section criterion alone does not yet prove "
            "a nonzero polynomial flattening minor; a noncancelling monomial specialization "
            "is still required."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", type=int, required=True)
    parser.add_argument("--length", type=int, required=True)
    args = parser.parse_args()
    print(json.dumps(audit(args.width, args.length), indent=2, sort_keys=True))
