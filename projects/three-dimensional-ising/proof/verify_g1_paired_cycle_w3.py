#!/usr/bin/env python3
"""Exact tree+chord G1 specialization certificate at w=3."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.verify_lane_b_arbitrary_width_frontier import _case, _rank, _rows_from_columns  # noqa: E402
from proof.verify_lane_b_universal_canonical_ranks import _rank_minor  # noqa: E402
from src.conventions import cubic_box  # noqa: E402


PRIMES = (1_000_000_007, 1_000_000_009)
N = 10
W = 3
HANDLE_CUT = 5
TREE_EDGES = (
    0,4,6,7,9,10,13,16,20,21,23,25,26,27,29,30,36,37,38,39,41,45,48,49,
    50,51,57,59,60,62,65,67,68,70,73,78,79,80,83,86,88,89,91,94,95,99,
    100,101,104,107,115,116,121,122,125,128,131,133,135,137,138,139,143,
    146,148,149,151,154,155,161,164,165,170,173,175,176,181,182,185,187,
    188,189,192,193,194,195,196,198,200,
)
CHORDS = (44,52,103,110,112,118,120,162)
EXPECTED_LABELS = (104860,6528,1536,121128,65548,130920,128616,222816)


def _labels(row, edges):
    result = [0] * len(edges)
    index = {(edge.u, edge.v): i for i, edge in enumerate(edges)}
    for bit_text, pairs in row["atomic_coordinate_edge_support"].items():
        for pair in pairs:
            result[index[(tuple(pair[0]), tuple(pair[1]))]] |= 1 << int(bit_text)
    return result


def _fundamental_labels(vertices, edges, labels):
    tree = set(TREE_EDGES)
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
            if neighbour in path_label:
                continue
            path_label[neighbour] = path_label[vertex] ^ labels[edge_index]
            stack.append(neighbour)
    if len(path_label) != len(vertices) or len(tree) != len(vertices) - 1:
        raise AssertionError("frozen edge set is not a spanning tree")
    return tuple(
        path_label[edges[chord].u] ^ path_label[edges[chord].v] ^ labels[chord]
        for chord in CHORDS
    )


def _independent_row_positions(columns: list[int], row_count: int) -> list[int]:
    rows = _rows_from_columns(columns, row_count)
    selected = []
    for position, row in enumerate(rows):
        if _rank([rows[index] for index in selected] + [row]) > len(selected):
            selected.append(position)
    return selected


def _q0(vector: int, genus: int) -> int:
    return sum(
        ((vector >> (2 * handle)) & 1) & ((vector >> (2 * handle + 1)) & 1)
        for handle in range(genus)
    ) & 1


def verify() -> dict[str, object]:
    structural = _case(W, N)["length_rows"][-1]
    genus = structural["genus"]
    vertices, edges = cubic_box((N, W, W))
    labels = _labels(structural, edges)
    fundamental = _fundamental_labels(vertices, edges, labels)
    if fundamental != EXPECTED_LABELS:
        raise AssertionError("frozen fundamental-cycle labels changed")
    shift = 2 * HANDLE_CUT
    left_columns = [label & ((1 << shift) - 1) for label in fundamental]
    right_columns = [label >> shift for label in fundamental]
    target = W * W - 1
    if _rank(left_columns) != target or _rank(right_columns) != target:
        raise AssertionError("paired homology projections are not both injective")
    selected_left_coordinates = _independent_row_positions(left_columns, shift)
    selected_right_coordinates = _independent_row_positions(right_columns, 2 * genus - shift)
    if len(selected_left_coordinates) != target or len(selected_right_coordinates) != target:
        raise AssertionError("could not select dual Walsh coordinate bases")

    retained = set(TREE_EDGES) | set(CHORDS)
    if len(retained) - len(vertices) + 1 != target:
        raise AssertionError("specialized connected graph cycle dimension is not eight")

    # Character rows and columns are chosen so their restrictions to the two
    # projected cycle images run through every character of F_2^8.
    left_characters = [
        sum(((character >> j) & 1) << coordinate for j, coordinate in enumerate(selected_left_coordinates))
        for character in range(1 << target)
    ]
    right_characters = [
        sum(((character >> j) & 1) << coordinate for j, coordinate in enumerate(selected_right_coordinates))
        for character in range(1 << target)
    ]
    homologies = []
    for coefficients in range(1 << target):
        value = 0
        for index, label in enumerate(fundamental):
            if (coefficients >> index) & 1:
                value ^= label
        homologies.append(value)
    if len(set(value & ((1 << shift) - 1) for value in homologies)) != 1 << target:
        raise AssertionError("left projected homology map is not bijective")
    if len(set(value >> shift for value in homologies)) != 1 << target:
        raise AssertionError("right projected homology map is not bijective")

    certificates = []
    for prime in PRIMES:
        matrix = []
        for left in left_characters:
            row = []
            for right in right_characters:
                character = left | (right << shift)
                value = 0
                for homology in homologies:
                    sign = _q0(homology, genus) ^ ((character & homology).bit_count() & 1)
                    value += -1 if sign else 1
                row.append(value % prime)
            matrix.append(row)
        certificate = _rank_minor(matrix, prime)
        if certificate["rank"] != 1 << target:
            raise AssertionError("specialized original F flattening is not full rank")
        expected_square = pow(2, target * (1 << target), prime)
        if certificate["minor_determinant"] not in (expected_square, (-expected_square) % prime):
            raise AssertionError("Walsh determinant magnitude identity failed")
        certificates.append({
            "prime": prime,
            "rank": certificate["rank"],
            "determinant": certificate["minor_determinant"],
            "expected_determinant_up_to_sign": expected_square,
            "pivot_rows": certificate["minor_rows"],
            "pivot_columns": certificate["minor_columns"],
            "lu": certificate["minor_lu"],
        })

    return {
        "claim_status": "CERTIFIED_NUMERICAL exact GF(2) and finite-field certificate",
        "shape": [N, W, W],
        "genus": genus,
        "handle_cut": HANDLE_CUT,
        "target_dimension_exponent": target,
        "physical_frontier_dimension": 1 << target,
        "tree_edge_indices": list(TREE_EDGES),
        "chord_edge_indices": list(CHORDS),
        "fundamental_cycle_labels": list(fundamental),
        "left_projection_columns": left_columns,
        "right_projection_columns": right_columns,
        "left_projection_rows": _rows_from_columns(left_columns, shift),
        "right_projection_rows": _rows_from_columns(right_columns, 2 * genus - shift),
        "left_projection_rank": _rank(left_columns),
        "right_projection_rank": _rank(right_columns),
        "selected_left_dual_coordinates": selected_left_coordinates,
        "selected_right_dual_coordinates": selected_right_coordinates,
        "specialized_cycle_dimension": target,
        "sector_relation": "graph of an isomorphism F_2^8 -> F_2^8",
        "walsh_equivalence": "H_left * diag((-1)^q0) * H_right^T up to row/column permutations",
        "finite_field_certificates": certificates,
        "lifting": (
            "Each nonzero modular determinant is a specialization of the integer-polynomial "
            "flattening minor, so that symbolic minor is not identically zero."
        ),
        "claim_boundary": (
            "This reproves generic nonuniform tightness at width three by a structural sparse "
            "specialization. It does not supply the arbitrary-width tree+chord construction "
            "required for G1."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
