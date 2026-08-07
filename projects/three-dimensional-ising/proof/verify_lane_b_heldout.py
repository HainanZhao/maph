#!/usr/bin/env python3
"""Exact held-out 5x3x3 test of the Cycle 3 rank-seven mechanism."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.verify_lane_b_genus3 import (  # noqa: E402
    _canonical_cycle,
    _cycle_basis,
    _cycle_edge_indices,
    _edge_homology_labels,
    _elementary_squares,
    _frontier_sector_polynomials,
    _rotation_faces,
    _square_cover_exists,
)
from proof.verify_lane_b_intersection import (  # noqa: E402
    _gf2_inverse,
    _graph_result,
    _homology_representatives,
    _matrix_multiply,
    _transpose,
)
from src.conventions import Edge, Vertex, cubic_box  # noqa: E402
from src.lane_b_genus4 import BOX_5X3X3_GENUS_FOUR_ROTATION  # noqa: E402


PRIME = 1_000_000_007
EXTENDED_CYCLE3_BASIS = [1, 34, 4, 8, 17, 32, 64, 128]


def _reduced_closed_walks(
    vertices: tuple[Vertex, ...], edges: tuple[Edge, ...], length: int
) -> list[tuple[Vertex, ...]]:
    adjacency = {vertex: [] for vertex in vertices}
    for edge in edges:
        adjacency[edge.u].append(edge.v)
        adjacency[edge.v].append(edge.u)
    walks: set[tuple[Vertex, ...]] = set()
    for start in vertices:
        def extend(path: tuple[Vertex, ...], darts: frozenset[tuple[Vertex, Vertex]]) -> None:
            if len(path) == length:
                end = path[-1]
                if start not in adjacency[end] or (end, start) in darts:
                    return
                if path[-2] == start or path[1] == end:
                    return
                walks.add(_canonical_cycle(path))
                return
            current = path[-1]
            for neighbour in adjacency[current]:
                if len(path) > 1 and neighbour == path[-2]:
                    continue
                if (current, neighbour) in darts:
                    continue
                extend(path + (neighbour,), darts | {(current, neighbour)})
        extend((start,), frozenset())
    return sorted(walks)


def _minimum_genus() -> dict[str, object]:
    vertices, edges = cubic_box((5, 3, 3))
    rotation = BOX_5X3X3_GENUS_FOUR_ROTATION
    adjacency = {vertex: set() for vertex in vertices}
    for edge in edges:
        adjacency[edge.u].add(edge.v)
        adjacency[edge.v].add(edge.u)
    if set(rotation) != set(vertices) or any(
        set(rotation[vertex]) != adjacency[vertex] for vertex in vertices
    ):
        raise AssertionError("held-out rotation neighbour regression")
    face_masks, face_walks = _rotation_faces(vertices, edges, rotation)
    lengths = sorted(map(len, face_walks))
    genus = (2 - (len(vertices) - len(edges) + len(face_walks))) // 2
    if genus != 4 or lengths != [4] * 44 + [16]:
        raise AssertionError("held-out rotation is not the claimed genus-four embedding")

    edge_index = {(edge.u, edge.v): index for index, edge in enumerate(edges)}
    squares = _elementary_squares((5, 3, 3))
    square_edges = [_cycle_edge_indices(square, edge_index) for square in squares]
    incident = [0] * len(edges)
    for square, boundary in enumerate(square_edges):
        for edge in boundary:
            incident[edge] |= 1 << square
    six_walks = [
        walk for walk in _reduced_closed_walks(vertices, edges, 6)
        if len(set(walk)) == 6
    ]
    eight_walks = _reduced_closed_walks(vertices, edges, 8)
    surviving_eights = [
        walk for walk in eight_walks
        if _square_cover_exists(
            square_edges,
            incident,
            _cycle_edge_indices(walk, edge_index),
            len(edges),
        )
    ]
    surviving_hexagon_pairs = []
    for left, first in enumerate(six_walks):
        first_edges = _cycle_edge_indices(first, edge_index)
        for second in range(left, len(six_walks)):
            second_edges = _cycle_edge_indices(six_walks[second], edge_index)
            if _square_cover_exists(
                square_edges,
                incident,
                first_edges + second_edges,
                len(edges),
            ):
                surviving_hexagon_pairs.append((left, second))
    if surviving_eights or surviving_hexagon_pairs:
        raise AssertionError("a genus-three face census survived")
    long_face = next(walk for walk in face_walks if len(walk) == 16)
    if not _square_cover_exists(
        square_edges,
        incident,
        _cycle_edge_indices(long_face, edge_index),
        len(edges),
    ):
        raise AssertionError("face-cover solver rejected the genus-four positive control")
    return {
        "vertices": len(vertices),
        "edges": len(edges),
        "cycle_space_dimension": len(edges) - len(vertices) + 1,
        "faces": len(face_walks),
        "face_lengths": lengths,
        "elementary_squares": len(squares),
        "reduced_six_walks": len(six_walks),
        "reduced_eight_walks": len(eight_walks),
        "genus_three_eight_face_covers": len(surviving_eights),
        "genus_three_two_hexagon_covers": len(surviving_hexagon_pairs),
        "positive_genus_four_cover_control": True,
        "minimum_orientable_genus": 4,
    }


def _matrix_vector(rows: list[int], vector: int) -> int:
    return sum(((row & vector).bit_count() & 1) << index for index, row in enumerate(rows))


def _basis_image(basis: list[int], index: int) -> int:
    return _xor_vectors(
        vector for bit, vector in enumerate(basis) if (index >> bit) & 1
    )


def _xor_vectors(vectors: object) -> int:
    result = 0
    for vector in vectors:
        result ^= int(vector)
    return result


def _quadratic(homology: int) -> int:
    return sum(
        ((homology >> (2 * handle)) & 1) * ((homology >> (2 * handle + 1)) & 1)
        for handle in range(4)
    ) & 1


def _rank_mod_prime(matrix: list[list[int]]) -> int:
    rows = [[value % PRIME for value in row] for row in matrix]
    rank = 0
    for column in range(len(rows[0])):
        pivot = next((row for row in range(rank, len(rows)) if rows[row][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][column], PRIME - 2, PRIME)
        rows[rank] = [value * inverse % PRIME for value in rows[rank]]
        for row in range(rank + 1, len(rows)):
            if rows[row][column]:
                factor = rows[row][column]
                rows[row] = [
                    (value - factor * pivot_value) % PRIME
                    for value, pivot_value in zip(rows[row], rows[rank])
                ]
        rank += 1
    return rank


def _coordinate_action(
    vertices: tuple[Vertex, ...],
    edges: tuple[Edge, ...],
    face_masks: list[int],
    labels: list[int],
    cycles: list[int],
    transport: list[int],
    *,
    reflect_all: bool,
    swap_yz: bool,
) -> list[int]:
    edge_index = {(edge.u, edge.v): index for index, edge in enumerate(edges)}
    permutation = []
    for edge in edges:
        left = list(edge.u)
        right = list(edge.v)
        if reflect_all:
            left[0] = 4 - left[0]
            right[0] = 4 - right[0]
            left[1] = 2 - left[1]
            right[1] = 2 - right[1]
            left[2] = 2 - left[2]
            right[2] = 2 - right[2]
        if swap_yz:
            left[1], left[2] = left[2], left[1]
            right[1], right[2] = right[2], right[1]
        permutation.append(edge_index[tuple(sorted((tuple(left), tuple(right))))])

    def map_edges(mask: int) -> int:
        return _xor_vectors(1 << permutation[edge] for edge in range(len(edges)) if (mask >> edge) & 1)

    def label(mask: int) -> int:
        return _xor_vectors(labels[edge] for edge in range(len(edges)) if (mask >> edge) & 1)

    if any(label(map_edges(face)) for face in face_masks):
        raise AssertionError("held-out coordinate symmetry does not preserve face boundaries")
    inverse = _gf2_inverse(transport, 8)
    representatives = _homology_representatives(cycles, labels, 8)
    columns = []
    for coordinate in range(8):
        pinned = _matrix_vector(transport, 1 << coordinate)
        cycle = _xor_vectors(
            representative
            for bit, representative in enumerate(representatives)
            if (pinned >> bit) & 1
        )
        columns.append(_matrix_vector(inverse, label(map_edges(cycle))))
    return [
        sum(((columns[column] >> row) & 1) << column for column in range(8))
        for row in range(8)
    ]


def verify() -> dict[str, object]:
    minimum_genus = _minimum_genus()
    vertices, edges = cubic_box((5, 3, 3))
    face_masks, _ = _rotation_faces(vertices, edges, BOX_5X3X3_GENUS_FOUR_ROTATION)
    cycles = _cycle_basis(vertices, edges)
    labels, face_rank = _edge_homology_labels(len(edges), face_masks, cycles, 4)
    sectors, maximum_states = _frontier_sector_polynomials(vertices, edges, labels)
    if len(sectors) != 256 or {sum(polynomial) for polynomial in sectors.values()} != {1 << face_rank}:
        raise AssertionError("held-out sector partition regression")
    topology = _graph_result((5, 3, 3), BOX_5X3X3_GENUS_FOUR_ROTATION, 4)
    transport = topology["symplectic_transport_rows"]
    symplectic_sectors = [sectors[_matrix_vector(transport, h)] for h in range(256)]
    swap = _coordinate_action(
        vertices,
        edges,
        face_masks,
        labels,
        cycles,
        transport,
        reflect_all=False,
        swap_yz=True,
    )
    expected_swap = [9, 2, 38, 8, 152, 32, 96, 128]
    if swap != expected_swap:
        raise AssertionError("held-out y-z homology action regression")
    if any(
        symplectic_sectors[h] != symplectic_sectors[_matrix_vector(swap, h)]
        or _quadratic(h) != _quadratic(_matrix_vector(swap, h))
        for h in range(256)
    ):
        raise AssertionError("held-out symmetry does not preserve W or q")

    f_polynomials = []
    for linear in range(256):
        polynomial = [0] * (len(edges) + 1)
        for homology, sector in enumerate(symplectic_sectors):
            sign = -1 if _quadratic(homology) ^ ((linear & homology).bit_count() & 1) else 1
            for degree, coefficient in enumerate(sector):
                polynomial[degree] += sign * coefficient
        f_polynomials.append(tuple(polynomial))
    distinct_f = len(set(f_polynomials))
    symmetry_actions = []
    for reflect_all, swap_yz in ((False, False), (False, True), (True, False), (True, True)):
        action = _coordinate_action(
            vertices,
            edges,
            face_masks,
            labels,
            cycles,
            transport,
            reflect_all=reflect_all,
            swap_yz=swap_yz,
        )
        if any(
            _quadratic(homology) != _quadratic(_matrix_vector(action, homology))
            for homology in range(256)
        ):
            raise AssertionError("coordinate symmetry does not preserve the quadratic form")
        symmetry_actions.append(_transpose(action, 8))
    orbit_partition: list[tuple[int, ...]] = []
    unseen = set(range(256))
    while unseen:
        seed = min(unseen)
        orbit = tuple(sorted({_matrix_vector(action, seed) for action in symmetry_actions}))
        unseen.difference_update(orbit)
        orbit_partition.append(orbit)
    polynomial_partition = sorted(
        tuple(indices)
        for polynomial in set(f_polynomials)
        for indices in [[index for index, value in enumerate(f_polynomials) if value == polynomial]]
    )
    if sorted(orbit_partition) != polynomial_partition:
        raise AssertionError("F-polynomial equalities are not exactly the coordinate-symmetry orbits")
    orbit_sizes = Counter(map(len, orbit_partition))

    canonical = [1 << (index ^ 1) for index in range(8)]
    basis_rows = [
        sum(((EXTENDED_CYCLE3_BASIS[column] >> row) & 1) << column for column in range(8))
        for row in range(8)
    ]
    if _matrix_multiply(
        _transpose(basis_rows, 8),
        _matrix_multiply(canonical, basis_rows, 8),
        8,
    ) != canonical:
        raise AssertionError("extended Cycle 3 basis is not symplectic")

    evaluations: dict[str, object] = {}
    maximum_profile = [2, 4, 8, 16, 8, 4, 2]
    for denominator in (2, 3):
        f_values = [
            sum(coefficient * denominator ** (len(edges) - degree) for degree, coefficient in enumerate(polynomial))
            for polynomial in f_polynomials
        ]
        profile = []
        for cut in range(1, 8):
            row_count, column_count = 1 << cut, 1 << (8 - cut)
            matrix = [
                [
                    f_values[_basis_image(EXTENDED_CYCLE3_BASIS, row | (column << cut))]
                    for column in range(column_count)
                ]
                for row in range(row_count)
            ]
            profile.append(_rank_mod_prime(matrix))
        if profile != maximum_profile:
            raise AssertionError("held-out direct-extension profile is not maximal")
        old_relation = all(
            f_values[_basis_image(EXTENDED_CYCLE3_BASIS, 4 | (column << 3))]
            == f_values[_basis_image(EXTENDED_CYCLE3_BASIS, 6 | (column << 3))]
            for column in range(32)
        )
        if old_relation:
            raise AssertionError("Cycle 3 row relation unexpectedly survived")
        evaluations[f"1/{denominator}"] = {
            "modular_prime": PRIME,
            "TT_profile": profile,
            "cycle3_row_identity_survives": False,
        }
    return {
        "claim_status": "COMPUTATIONALLY_VERIFIED",
        "minimum_genus_certificate": minimum_genus,
        "intersection": topology,
        "face_boundary_rank": face_rank,
        "homology_dimension": 8,
        "sector_count": 256,
        "sector_cardinality": 1 << face_rank,
        "maximum_frontier_states": maximum_states,
        "y_z_swap_homology_action_rows": swap,
        "exact_distinct_F_polynomials": distinct_f,
        "embedding_symmetry_group_order": len(symmetry_actions),
        "spin_structure_orbits": len(orbit_partition),
        "spin_structure_orbit_size_counts": dict(sorted(orbit_sizes.items())),
        "F_polynomial_equalities_equal_symmetry_orbits": True,
        "tested_basis": EXTENDED_CYCLE3_BASIS,
        "evaluations": evaluations,
        "generic_TT_profile_over_Q(t)": maximum_profile,
        "gate_outcome": "DIRECT_HANDLE_EXTENSION_FALSIFIED",
        "claim_boundary": (
            "The nonzero modular minors prove exact full generic rank for the displayed, "
            "preselected direct extension of the Cycle 3 basis. They do not prove that all "
            "Sp(8,2) bases are full rank. The 100000-basis random discovery screen is not "
            "part of this proof claim."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
