#!/usr/bin/env python3
"""Exact two-sided tree search using a lightweight raw-homology split."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from discovery.search_g1_relative_trees import _side  # noqa: E402
from proof.verify_lane_b_genus3 import (  # noqa: E402
    _cycle_basis,
    _edge_homology_labels,
    _rotation_faces,
)
from src.conventions import cubic_box  # noqa: E402
from src.lane_b_universal_embedding import (  # noqa: E402
    universal_checkerboard_rotation,
    universal_embedding_genus,
)


def _label(mask, labels):
    value = 0
    while mask:
        bit = (mask & -mask).bit_length() - 1
        value ^= labels[bit]
        mask &= mask - 1
    return value


def _side_cycle_labels(vertices, edges, raw_labels, layer, side):
    if side == "left":
        retained_vertices = tuple(vertex for vertex in vertices if vertex[0] <= layer)
        retained_ids = [
            index for index, edge in enumerate(edges)
            if edge.u[0] <= layer and edge.v[0] <= layer
        ]
    else:
        retained_vertices = tuple(vertex for vertex in vertices if vertex[0] >= layer)
        retained_ids = [
            index for index, edge in enumerate(edges)
            if edge.u[0] >= layer and edge.v[0] >= layer
        ]
    retained_edges = tuple(edges[index] for index in retained_ids)
    result = []
    for local_mask in _cycle_basis(retained_vertices, retained_edges):
        global_mask = 0
        for local, global_index in enumerate(retained_ids):
            if (local_mask >> local) & 1:
                global_mask |= 1 << global_index
        result.append(_label(global_mask, raw_labels))
    return result


def _basis(vectors):
    pivots = {}
    selected = []
    for vector in vectors:
        reduced = vector
        while reduced:
            pivot = reduced.bit_length() - 1
            if pivot in pivots:
                reduced ^= pivots[pivot]
            else:
                pivots[pivot] = reduced
                selected.append(vector)
                break
    return selected


def _coordinate_labels(basis_vectors, raw_labels):
    pivots = {}
    for coordinate, vector in enumerate(basis_vectors):
        label = 1 << coordinate
        while vector:
            pivot = vector.bit_length() - 1
            if pivot in pivots:
                old_vector, old_label = pivots[pivot]
                vector ^= old_vector
                label ^= old_label
            else:
                pivots[pivot] = (vector, label)
                break
        else:
            raise AssertionError("adapted homology basis is dependent")
    result = []
    for vector in raw_labels:
        label = 0
        while vector:
            pivot = vector.bit_length() - 1
            if pivot not in pivots:
                raise AssertionError("adapted homology basis does not span")
            old_vector, old_label = pivots[pivot]
            vector ^= old_vector
            label ^= old_label
        result.append(label)
    return result


def search(width, length=9, separator_layer=4):
    started = time.monotonic()
    vertices, edges = cubic_box((length, width, width))
    faces, _ = _rotation_faces(
        vertices, edges, universal_checkerboard_rotation(length, width)
    )
    genus = universal_embedding_genus(length, width)
    raw_labels, face_rank = _edge_homology_labels(
        len(edges), faces, _cycle_basis(vertices, edges), genus
    )
    left = _basis(
        _side_cycle_labels(vertices, edges, raw_labels, separator_layer, "left")
    )
    right = _basis(
        _side_cycle_labels(vertices, edges, raw_labels, separator_layer, "right")
    )
    expected_side_genus = universal_embedding_genus(separator_layer + 1, width)
    if len(left) != 2 * expected_side_genus or len(right) != 2 * expected_side_genus:
        raise AssertionError("prefix homology dimension failed")
    if len(_basis(left + right)) != 2 * genus:
        raise AssertionError("left/right homology spans are not complementary")
    labels = _coordinate_labels(left + right, raw_labels)
    left_result = _side(
        width, vertices, edges, labels, separator_layer, expected_side_genus, "left"
    )
    right_result = _side(
        width, vertices, edges, labels, separator_layer, expected_side_genus, "right"
    )
    return {
        "status": "OBSERVED exact GF(2) globally compatible side-tree search",
        "shape": [length, width, width],
        "separator_layer": separator_layer,
        "genus": genus,
        "side_genus": expected_side_genus,
        "face_boundary_rank": face_rank,
        "left": left_result,
        "right": right_result,
        "both_met": left_result["criterion_met"] and right_result["criterion_met"],
        "wall_seconds": time.monotonic() - started,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "claim_boundary": (
            "A finite-width common-tree result is exact but does not prove a symbolic "
            "right-encoder construction for arbitrary width."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", type=int, required=True)
    parser.add_argument("--length", type=int, default=9)
    parser.add_argument("--separator-layer", type=int, default=4)
    args = parser.parse_args()
    print(json.dumps(search(**vars(args)), indent=2, sort_keys=True))
