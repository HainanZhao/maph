#!/usr/bin/env python3
"""Exact second recursive-handle check for the Lane B theta bridge."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import subprocess
import sys
import tempfile


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
from src.lane_b_recursive import (  # noqa: E402
    BOX_5X3X3_RECURSIVE_GENUS_FOUR_ROTATION,
)
from src.lane_b_recursive6 import (  # noqa: E402
    BOX_6X3X3_RECURSIVE_GENUS_FIVE_ROTATION,
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
    """Coordinates in (old eight, defect d=384, conjugate c=512)."""
    defect = (value >> 8) & 1
    return (
        (value & 127)
        | ((((value >> 7) & 1) ^ defect) << 7)
        | (defect << 8)
        | (value & 512)
    )


def _minimum_genus_certificate() -> dict[str, object]:
    source = ROOT / "proof/verify_lane_b_genus4_no_cover_6x3x3.cpp"
    with tempfile.TemporaryDirectory(prefix="lane-b-genus4-") as temporary:
        executable = Path(temporary) / "verify"
        compile_result = subprocess.run(
            [
                "g++", "-O3", "-DNDEBUG", "-std=c++20", "-Wall", "-Wextra",
                str(source), "-o", str(executable),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        run_result = subprocess.run(
            [str(executable)], check=True, capture_output=True, text=True, timeout=1800
        )
    expected = [
        "six=422 eight=3162 ten=29934",
        "ten_survivors=0",
        "eight_six_survivors=0",
        "three_six_survivors=0",
    ]
    lines = run_result.stdout.strip().splitlines()
    if lines != expected:
        raise AssertionError(f"genus-four face-cover census regression: {lines}")
    compiler = subprocess.run(
        ["g++", "--version"], check=True, capture_output=True, text=True
    ).stdout.splitlines()[0]
    return {
        "euler_girth_lower_bound": 4,
        "genus_four_required_face_patterns": [[10], [8, 6], [6, 6, 6]],
        "reduced_walk_counts": {"6": 422, "8": 3162, "10": 29934},
        "candidate_multisets_exhausted": {
            "10": 29934,
            "8+6": 1_334_364,
            "6+6+6": 12_614_424,
        },
        "surviving_face_incidence_covers": 0,
        "positive_genus_five_rotation": "54 elementary squares plus one 18-gon",
        "minimum_orientable_genus": 5,
        "compiler": compiler,
        "compiler_stderr": compile_result.stderr,
    }


def verify() -> dict[str, object]:
    minimum_genus = _minimum_genus_certificate()
    old_vertices, old_edges = cubic_box((5, 3, 3))
    new_vertices, new_edges = cubic_box((6, 3, 3))
    old_rotation = BOX_5X3X3_RECURSIVE_GENUS_FOUR_ROTATION
    new_rotation = BOX_6X3X3_RECURSIVE_GENUS_FIVE_ROTATION
    if any(
        tuple(neighbour for neighbour in new_rotation[vertex] if neighbour[0] < 5)
        != old_rotation[vertex]
        for vertex in old_vertices
    ):
        raise AssertionError("deleting the sixth slice does not recover the fifth")

    old_faces, old_walks = _rotation_faces(old_vertices, old_edges, old_rotation)
    new_faces, new_walks = _rotation_faces(new_vertices, new_edges, new_rotation)
    if sorted(map(len, old_walks)) != [4] * 44 + [16]:
        raise AssertionError("recursive 5x3x3 face census regression")
    if sorted(map(len, new_walks)) != [4] * 54 + [18]:
        raise AssertionError("recursive 6x3x3 face census regression")
    genus = (2 - (len(new_vertices) - len(new_edges) + len(new_faces))) // 2
    if genus != 5:
        raise AssertionError("recursive 6x3x3 genus regression")

    old_cycles = _cycle_basis(old_vertices, old_edges)
    new_cycles = _cycle_basis(new_vertices, new_edges)
    old_labels, old_face_rank = _edge_homology_labels(
        len(old_edges), old_faces, old_cycles, 4
    )
    new_labels, new_face_rank = _edge_homology_labels(
        len(new_edges), new_faces, new_cycles, 5
    )
    embedded_faces = [_embedded_mask(face, old_edges, new_edges) for face in old_faces]
    combined_rank = _rank(new_faces + embedded_faces)
    intersection_dimension = new_face_rank + old_face_rank - combined_rank
    defect_dimension = combined_rank - new_face_rank
    if (old_face_rank, new_face_rank, intersection_dimension, defect_dimension) != (44, 54, 43, 1):
        raise AssertionError("second relative boundary dimensions changed")

    old_topology = _graph_result((5, 3, 3), old_rotation, 4)
    new_topology = _graph_result((6, 3, 3), new_rotation, 5)
    representative_images = [
        _label(_embedded_mask(mask, old_edges, new_edges), new_labels)
        for mask in old_topology["pinned_homology_representatives"]
    ]
    if representative_images != [1, 2, 4, 8, 16, 32, 64, 128]:
        raise AssertionError("old eight homology coordinates are not preserved")
    restricted_intersection = [
        sum(
            _quadratic_value(
                new_topology["intersection_matrix_rows"],
                representative_images[left], representative_images[right],
            ) << right
            for right in range(8)
        )
        for left in range(8)
    ]
    if restricted_intersection != old_topology["intersection_matrix_rows"]:
        raise AssertionError("old genus-four intersection form is not preserved")

    old_face_images = [_label(mask, new_labels) for mask in embedded_faces]
    defect=384
    conjugate=512
    if sorted(set(old_face_images)-{0}) != [defect]:
        raise AssertionError("second boundary defect line regression")
    if any(
        _quadratic_value(new_topology["intersection_matrix_rows"], defect, 1 << index)
        for index in range(8)
    ) or _quadratic_value(new_topology["intersection_matrix_rows"], defect, conjugate) != 1:
        raise AssertionError("second defect is not paired with the new conjugate")

    new_index = {(edge.u, edge.v): index for index, edge in enumerate(new_edges)}
    old_edge_corrections = []
    for old_index, edge in enumerate(old_edges):
        correction = new_labels[new_index[(edge.u, edge.v)]] ^ old_labels[old_index]
        if correction:
            old_edge_corrections.append((old_index, edge, correction))
    if [(index, correction) for index, _, correction in old_edge_corrections] != [(89,384),(94,384)]:
        raise AssertionError("second relative defect cochain support regression")

    defect_support={index for index,_,_ in old_edge_corrections}
    relative_labels=[
        value ^ ((1 << 8) if index in defect_support else 0)
        for index,value in enumerate(old_labels)
    ]
    directly_restricted_labels=[
        _adapted_coordinate(new_labels[new_index[(edge.u,edge.v)]])
        for edge in old_edges
    ]
    if relative_labels != directly_restricted_labels:
        raise AssertionError("second local defect formula disagrees edgewise")

    ordinary_sectors, ordinary_maximum_states = _frontier_sector_polynomials(
        old_vertices, old_edges, old_labels
    )
    relative_sectors, relative_maximum_states = _frontier_sector_polynomials(
        old_vertices, old_edges, relative_labels
    )
    if len(relative_sectors)!=512:
        raise AssertionError("second relative-sector count regression")
    if {sum(polynomial) for polynomial in relative_sectors.values()} != {1 << 43}:
        raise AssertionError("second relative-sector cardinality regression")
    for homology in range(256):
        even=relative_sectors[homology]
        odd=relative_sectors[homology|256]
        length=max(len(even),len(odd))
        reunited=tuple(
            (even[degree] if degree<len(even) else 0)
            +(odd[degree] if degree<len(odd) else 0)
            for degree in range(length)
        )
        if reunited != ordinary_sectors[homology]:
            raise AssertionError("second relative sectors fail coefficientwise reunion")

    added_label_counter: Counter[int]=Counter()
    for edge,value in zip(new_edges,new_labels):
        if edge not in old_edges:
            added_label_counter[_adapted_coordinate(value)]+=1
    expected_added_labels=Counter({0:13,512:4,128:2,384:2})
    if added_label_counter != expected_added_labels:
        raise AssertionError("second added-slice label pattern regression")

    return {
        "claim_status": "CERTIFIED_NUMERICAL",
        "user_workflow_status": "COMPUTATIONALLY VERIFIED",
        "certificate": "exact exhaustive integer/GF(2) computation; radius 0, rank margin 1",
        "claim_boundary": (
            "Two consecutive handle additions have the same one-defect, three-bit local form. "
            "A size-uniform recurrence and thermodynamic compression remain unproved."
        ),
        "minimum_genus_certificate": minimum_genus,
        "rotation_restriction_exact": True,
        "old_embedding": {"faces":len(old_faces),"face_rank":old_face_rank,"genus":4},
        "new_embedding": {
            "faces":len(new_faces),"face_rank":new_face_rank,"genus":genus,
            "face_lengths":sorted(map(len,new_walks)),
            "independent_intersection_routes_agree":new_topology[
                "independent_routes_agree_with_labels"
            ],
        },
        "relative_boundary": {
            "intersection_dimension":intersection_dimension,
            "defect_dimension":defect_dimension,
            "nonzero_old_face_image":defect,
            "defect_conjugate":conjugate,
            "old_face_image_counts":dict(sorted(Counter(old_face_images).items())),
        },
        "old_homology": {
            "representative_images":representative_images,
            "intersection_rows":restricted_intersection,
            "preserved_label_by_label":True,
        },
        "local_support": {
            "old_edge_defect_support":[
                {"edge_index":index,"edge":[list(edge.u),list(edge.v)],"correction":correction}
                for index,edge,correction in old_edge_corrections
            ],
            "added_edge_adapted_label_counts":dict(sorted(added_label_counter.items())),
            "semantic_pattern":{"zero":13,"old_last":2,"old_last_plus_defect":2,"conjugate":4},
            "active_adapted_coordinates":[7,8,9],
        },
        "relative_sector_identity": {
            "ordinary_sectors":len(ordinary_sectors),
            "refined_sectors":len(relative_sectors),
            "kernel_dimension":43,
            "cardinality_per_refined_sector":1 << 43,
            "coefficientwise_reunion_verified":True,
            "restricted_new_labels_verified_edgewise":True,
            "ordinary_frontier_maximum_states":ordinary_maximum_states,
            "relative_frontier_maximum_states":relative_maximum_states,
            "walsh_channels":2,
        },
        "recurrence_control": {
            "steps_compared":["4->5","5->6"],
            "boundary_defect_dimensions":[1,1],
            "active_topological_window_widths":[3,3],
            "added_edge_semantic_pattern_repeats":True,
        },
        "falsifier": (
            "A later compatible minimum-genus slice whose defect dimension exceeds one, whose "
            "label support reaches beyond the last old handle, or whose local semantic pattern changes."
        ),
    }


if __name__=="__main__":
    print(json.dumps(verify(),indent=2,sort_keys=True))
