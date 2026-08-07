#!/usr/bin/env python3
"""Exact recursive-embedding and relative-homology checks for Lane B.

This verifier does not claim a size-uniform recurrence.  It checks the first
handle-addition map, from the pinned 4x3x3 ribbon graph to a compatible
5x3x3 ribbon graph, entirely over GF(2).
"""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.verify_lane_b_genus3 import (  # noqa: E402
    _cycle_basis,
    _edge_homology_labels,
    _frontier_sector_polynomials,
    _rotation_faces,
)
from proof.verify_lane_b_intersection import (  # noqa: E402
    _graph_result,
    _quadratic_value,
)
from src.conventions import Edge, cubic_box  # noqa: E402
from src.lane_b_genus3 import BOX_4X3X3_GENUS_THREE_ROTATION  # noqa: E402
from src.lane_b_recursive import (  # noqa: E402
    BOX_5X3X3_RECURSIVE_GENUS_FOUR_ROTATION,
)


def _rank(vectors: list[int]) -> int:
    pivots: dict[int, int] = {}
    for vector in vectors:
        while vector:
            pivot = vector.bit_length() - 1
            if pivot in pivots:
                vector ^= pivots[pivot]
            else:
                pivots[pivot] = vector
                break
    return len(pivots)


def _embedded_mask(mask: int, old_edges: tuple[Edge, ...], new_edges: tuple[Edge, ...]) -> int:
    new_index = {(edge.u, edge.v): index for index, edge in enumerate(new_edges)}
    result = 0
    for index, edge in enumerate(old_edges):
        if (mask >> index) & 1:
            result ^= 1 << new_index[(edge.u, edge.v)]
    return result


def _label(mask: int, labels: list[int]) -> int:
    result = 0
    for edge, value in enumerate(labels):
        if (mask >> edge) & 1:
            result ^= value
    return result


def _adapted_coordinate(value: int) -> int:
    """Coordinates in (old six, defect d=96, conjugate c=128)."""
    defect = (value >> 6) & 1
    return (
        (value & 31)
        | ((((value >> 5) & 1) ^ defect) << 5)
        | (defect << 6)
        | (value & 128)
    )


def verify() -> dict[str, object]:
    old_vertices, old_edges = cubic_box((4, 3, 3))
    new_vertices, new_edges = cubic_box((5, 3, 3))
    old_rotation = BOX_4X3X3_GENUS_THREE_ROTATION
    new_rotation = BOX_5X3X3_RECURSIVE_GENUS_FOUR_ROTATION

    if any(
        tuple(neighbour for neighbour in new_rotation[vertex] if neighbour[0] < 4)
        != old_rotation[vertex]
        for vertex in old_vertices
    ):
        raise AssertionError("deleting the new slice does not recover the old rotation")

    old_faces, old_walks = _rotation_faces(old_vertices, old_edges, old_rotation)
    new_faces, new_walks = _rotation_faces(new_vertices, new_edges, new_rotation)
    if sorted(map(len, old_walks)) != [4] * 34 + [14]:
        raise AssertionError("old face census regression")
    if sorted(map(len, new_walks)) != [4] * 44 + [16]:
        raise AssertionError("recursive face census regression")
    genus = (2 - (len(new_vertices) - len(new_edges) + len(new_faces))) // 2
    if genus != 4:
        raise AssertionError("recursive rotation genus regression")

    old_cycles = _cycle_basis(old_vertices, old_edges)
    new_cycles = _cycle_basis(new_vertices, new_edges)
    old_labels, old_face_rank = _edge_homology_labels(
        len(old_edges), old_faces, old_cycles, 3
    )
    new_labels, new_face_rank = _edge_homology_labels(
        len(new_edges), new_faces, new_cycles, 4
    )
    embedded_faces = [_embedded_mask(face, old_edges, new_edges) for face in old_faces]
    combined_rank = _rank(new_faces + embedded_faces)
    intersection_dimension = new_face_rank + old_face_rank - combined_rank
    defect_dimension = combined_rank - new_face_rank
    if (old_face_rank, new_face_rank, intersection_dimension, defect_dimension) != (34, 44, 33, 1):
        raise AssertionError("relative face-boundary dimensions changed")

    old_topology = _graph_result((4, 3, 3), old_rotation, 3)
    new_topology = _graph_result((5, 3, 3), new_rotation, 4)
    embedded_old_representatives = [
        _embedded_mask(mask, old_edges, new_edges)
        for mask in old_topology["pinned_homology_representatives"]
    ]
    representative_images = [
        _label(mask, new_labels) for mask in embedded_old_representatives
    ]
    if representative_images != [1, 2, 4, 8, 16, 32]:
        raise AssertionError("old pinned homology coordinates are not preserved")
    restricted_intersection = [
        sum(
            _quadratic_value(
                new_topology["intersection_matrix_rows"],
                representative_images[left],
                representative_images[right],
            )
            << right
            for right in range(6)
        )
        for left in range(6)
    ]
    if restricted_intersection != old_topology["intersection_matrix_rows"]:
        raise AssertionError("old labeled intersection form is not preserved")

    old_face_images = [_label(mask, new_labels) for mask in embedded_faces]
    nonzero_face_images = sorted(set(old_face_images) - {0})
    if nonzero_face_images != [96]:
        raise AssertionError("the relative boundary defect is not the pinned line <96>")
    defect = 96
    conjugate = 128
    if any(
        _quadratic_value(new_topology["intersection_matrix_rows"], defect, 1 << index)
        for index in range(6)
    ) or _quadratic_value(new_topology["intersection_matrix_rows"], defect, conjugate) != 1:
        raise AssertionError("defect line is not the first vector of the new symplectic pair")

    new_index = {(edge.u, edge.v): index for index, edge in enumerate(new_edges)}
    old_edge_corrections = []
    for old_index, edge in enumerate(old_edges):
        new_index_value = new_index[(edge.u, edge.v)]
        correction = new_labels[new_index_value] ^ old_labels[old_index]
        if correction:
            old_edge_corrections.append((old_index, edge, correction))
    if [(index, correction) for index, _, correction in old_edge_corrections] != [(69, 96), (71, 96)]:
        raise AssertionError("relative defect cochain support regression")

    # Refine every old homology sector by the defect cochain epsilon.  This is
    # the exact relative-sector identity: in adapted new coordinates an old
    # cycle A has label (h(A), epsilon(A), 0).
    defect_support = {index for index, _, _ in old_edge_corrections}
    relative_labels = [
        value ^ ((1 << 6) if index in defect_support else 0)
        for index, value in enumerate(old_labels)
    ]
    directly_restricted_labels = [
        _adapted_coordinate(new_labels[new_index[(edge.u, edge.v)]])
        for edge in old_edges
    ]
    if relative_labels != directly_restricted_labels:
        raise AssertionError("local defect formula disagrees with restricted new labels")
    ordinary_sectors, ordinary_maximum_states = _frontier_sector_polynomials(
        old_vertices, old_edges, old_labels
    )
    relative_sectors, relative_maximum_states = _frontier_sector_polynomials(
        old_vertices, old_edges, relative_labels
    )
    if len(relative_sectors) != 128:
        raise AssertionError("relative sector count regression")
    if {sum(polynomial) for polynomial in relative_sectors.values()} != {1 << 33}:
        raise AssertionError("relative sectors do not have the predicted K-coset cardinality")
    for homology in range(64):
        even = relative_sectors[homology]
        odd = relative_sectors[homology | 64]
        length = max(len(even), len(odd))
        reunited = tuple(
            (even[degree] if degree < len(even) else 0)
            + (odd[degree] if degree < len(odd) else 0)
            for degree in range(length)
        )
        if reunited != ordinary_sectors[homology]:
            raise AssertionError("relative-sector polynomials do not reunite coefficientwise")

    added_label_counter: Counter[int] = Counter()
    for edge, value in zip(new_edges, new_labels):
        if edge not in old_edges:
            added_label_counter[_adapted_coordinate(value)] += 1
    expected_added_labels = Counter({0: 13, 128: 4, 32: 2, 96: 2})
    if added_label_counter != expected_added_labels:
        raise AssertionError("added-slice adapted label support regression")

    return {
        "claim_status": "CERTIFIED_NUMERICAL",
        "certificate": "exact GF(2) arithmetic; enclosure radius 0 and integer rank margin 1",
        "claim_boundary": (
            "The single 4x3x3 to 5x3x3 step has a one-bit relative boundary defect and "
            "three-bit adapted topological support. No size-uniform recurrence, theta identity, "
            "or thermodynamic compression is proved."
        ),
        "rotation_restriction_exact": True,
        "old_embedding": {"faces": len(old_faces), "face_rank": old_face_rank, "genus": 3},
        "new_embedding": {
            "faces": len(new_faces),
            "face_lengths": sorted(map(len, new_walks)),
            "face_rank": new_face_rank,
            "genus": genus,
            "independent_intersection_routes_agree": new_topology[
                "independent_routes_agree_with_labels"
            ],
        },
        "relative_boundary": {
            "intersection_dimension": intersection_dimension,
            "defect_dimension": defect_dimension,
            "nonzero_old_face_image": defect,
            "defect_conjugate": conjugate,
            "old_face_image_counts": dict(sorted(Counter(old_face_images).items())),
        },
        "old_homology": {
            "representative_images": representative_images,
            "intersection_rows": restricted_intersection,
            "preserved_label_by_label": True,
        },
        "local_support": {
            "old_edge_defect_support": [
                {"edge_index": index, "edge": [list(edge.u), list(edge.v)], "correction": correction}
                for index, edge, correction in old_edge_corrections
            ],
            "added_edge_adapted_label_counts": dict(sorted(added_label_counter.items())),
            "semantic_pattern": {
                "zero": 13,
                "old_last": 2,
                "old_last_plus_defect": 2,
                "conjugate": 4,
            },
            "active_adapted_coordinates": [5, 6, 7],
        },
        "relative_sector_identity": {
            "ordinary_sectors": len(ordinary_sectors),
            "refined_sectors": len(relative_sectors),
            "kernel_dimension": 33,
            "cardinality_per_refined_sector": 1 << 33,
            "coefficientwise_reunion_verified": True,
            "restricted_new_labels_verified_edgewise": True,
            "ordinary_frontier_maximum_states": ordinary_maximum_states,
            "relative_frontier_maximum_states": relative_maximum_states,
            "walsh_channels": 2,
        },
        "falsifier": (
            "A second compatible slice for which the old boundary image has unbounded dimension "
            "or the added-edge labels act on an unbounded number of prior handle coordinates."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
