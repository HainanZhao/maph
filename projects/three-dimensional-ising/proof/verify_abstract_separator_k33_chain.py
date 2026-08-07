#!/usr/bin/env python3
"""Exact non-grid validation family for the abstract separator theorem."""

from __future__ import annotations

import json
from itertools import permutations
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.verify_lane_b_arbitrary_width_frontier import (  # noqa: E402
    _bilinear,
    _matrix_vector,
    _rank,
    _rows_from_columns,
)
from proof.verify_lane_b_genus3 import (  # noqa: E402
    _cycle_basis,
    _edge_homology_labels,
    _rotation_faces,
)
from proof.verify_lane_b_intersection import (  # noqa: E402
    _cup_product_intersection,
    _gf2_inverse,
    _homology_representatives,
    _tree_cotree_intersection,
)
from proof.verify_lane_b_universal_canonical_ranks import _rank_minor  # noqa: E402
from proof.verify_lane_b_width_scaling import _profiles  # noqa: E402
from src.conventions import Edge  # noqa: E402


PRIMES = (1_000_000_007, 1_000_000_009)
BASE_ROTATION = {
    0: (3, 4, 5),
    1: (3, 4, 5),
    2: (3, 4, 5),
    3: (0, 1, 2),
    4: (0, 1, 2),
    5: (0, 1, 2),
}


def _chain(count: int):
    """Connected-sum rotation of count toroidal K3,3 gadgets."""
    if count < 1:
        raise ValueError("the chain must contain a gadget")
    parent = {(copy, vertex): (copy, vertex) for copy in range(count) for vertex in range(6)}

    def find(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    def union(left, right):
        a, b = find(left), find(right)
        parent[max(a, b)] = min(a, b)

    for copy in range(count - 1):
        union((copy, 1), (copy + 1, 0))
        union((copy, 5), (copy + 1, 3))
    for vertex in list(parent):
        parent[vertex] = find(vertex)

    removed = set()
    for copy in range(count - 1):
        removed.add(frozenset(((copy, 1), (copy, 5))))
        removed.add(frozenset(((copy + 1, 0), (copy + 1, 3))))

    members = {}
    sequences = {}
    retained_edges_by_gadget = [[] for _ in range(count)]
    for copy in range(count):
        for vertex, neighbours in BASE_ROTATION.items():
            original = (copy, vertex)
            members.setdefault(parent[original], []).append(original)
            sequences[original] = [
                (copy, neighbour)
                for neighbour in neighbours
                if frozenset((original, (copy, neighbour))) not in removed
            ]
        for left in range(3):
            for right in range(3, 6):
                original = frozenset(((copy, left), (copy, right)))
                # The two distinguished port edges are excluded from the
                # local homology witness even when an end port remains in the
                # graph.  K3,3 minus both ports has cycle rank exactly two.
                is_port = (left, right) in ((0, 3), (1, 5))
                if original not in removed and not is_port:
                    retained_edges_by_gadget[copy].append(
                        tuple(sorted((parent[(copy, left)], parent[(copy, right)])))
                    )

    rotation = {}
    for vertex in sorted(members):
        cyclic = []
        # Gluing oriented edge-neighbourhood boundaries concatenates the two
        # cyclic orders beginning immediately after each deleted port dart.
        merged = len(members[vertex]) == 2
        for original in sorted(members[vertex]):
            sequence = sequences[original]
            # At the second endpoint the boundary orientation of the removed
            # right-port ribbon is opposite to that of the left port.
            if merged and original[1] == 5:
                sequence = list(reversed(sequence))
            cyclic.extend(parent[neighbour] for neighbour in sequence)
        rotation[vertex] = tuple(cyclic)
    vertices = tuple(sorted(rotation))
    edge_pairs = sorted({
        tuple(sorted((vertex, neighbour)))
        for vertex, neighbours in rotation.items()
        for neighbour in neighbours
    })
    edges = tuple(Edge((u[0], u[1], 0), (v[0], v[1], 0)) for u, v in edge_pairs)
    relabel = {vertex: (vertex[0], vertex[1], 0) for vertex in vertices}
    rotation3 = {
        relabel[vertex]: tuple(relabel[neighbour] for neighbour in neighbours)
        for vertex, neighbours in rotation.items()
    }
    gadget_edges3 = [
        [tuple(sorted((relabel[u], relabel[v]))) for u, v in pairs]
        for pairs in retained_edges_by_gadget
    ]
    return tuple(relabel[vertex] for vertex in vertices), edges, rotation3, gadget_edges3


def _topology(count: int):
    vertices, edges, rotation, gadget_pairs = _chain(count)
    face_masks, face_walks = _rotation_faces(vertices, edges, rotation)
    genus = (2 - (len(vertices) - len(edges) + len(face_walks))) // 2
    if genus != count:
        raise AssertionError("K3,3 chain genus is not additive")
    cycles = _cycle_basis(vertices, edges)
    labels, face_rank = _edge_homology_labels(len(edges), face_masks, cycles, genus)
    representatives = _homology_representatives(cycles, labels, 2 * genus)
    cup, _ = _cup_product_intersection(vertices, edges, face_walks, representatives)
    tree, _ = _tree_cotree_intersection(vertices, edges, rotation, face_walks, labels, 2 * genus)
    if cup != tree:
        raise AssertionError("independent K3,3-chain intersection routes disagree")

    edge_index = {(edge.u, edge.v): index for index, edge in enumerate(edges)}
    local_columns = []
    for pairs in gadget_pairs:
        local_edges = tuple(edges[edge_index[pair]] for pair in pairs)
        local_vertices = tuple(sorted({vertex for edge in local_edges for vertex in (edge.u, edge.v)}))
        local_cycles = _cycle_basis(local_vertices, local_edges)
        if len(local_cycles) != 2:
            raise AssertionError("a port-deleted gadget does not have cycle rank two")
        for local_cycle in local_cycles:
            label = 0
            for local, edge in enumerate(local_edges):
                if (local_cycle >> local) & 1:
                    label ^= labels[edge_index[(edge.u, edge.v)]]
            local_columns.append(label)
    if _rank(local_columns) != 2 * genus:
        raise AssertionError("local gadget cycles do not span surface homology")
    local_intersection = [
        sum(_bilinear(cup, left, right) << column for column, right in enumerate(local_columns))
        for left in local_columns
    ]
    canonical = [1 << (index ^ 1) for index in range(2 * genus)]
    if local_intersection != canonical:
        raise AssertionError("ordered gadget cycles are not canonical handle pairs")
    change = _rows_from_columns(local_columns, 2 * genus)
    inverse = _gf2_inverse(change, 2 * genus)
    local_labels = [_matrix_vector(inverse, label) for label in labels]
    return vertices, edges, face_walks, local_labels, face_rank


def _q0(vector: int, genus: int) -> int:
    return sum(
        ((vector >> (2 * handle)) & 1) & ((vector >> (2 * handle + 1)) & 1)
        for handle in range(genus)
    ) & 1


def _case(count: int, prime: int) -> dict[str, object]:
    vertices, edges, faces, labels, face_rank = _topology(count)
    cycle_basis = _cycle_basis(vertices, edges)
    weights = [2 + (104729 * (index + 1)) % (prime - 3) for index in range(len(edges))]

    def tensor(edge_weights):
        sectors = [0] * (1 << (2 * count))
        for coefficients in range(1 << len(cycle_basis)):
            chain = 0
            for index, cycle in enumerate(cycle_basis):
                if (coefficients >> index) & 1:
                    chain ^= cycle
            homology = 0
            weight = 1
            for edge, label in enumerate(labels):
                if (chain >> edge) & 1:
                    homology ^= label
                    weight = weight * edge_weights[edge] % prime
            sectors[homology] = (sectors[homology] + weight) % prime
        values = []
        for character in range(1 << (2 * count)):
            total = 0
            for homology, weight in enumerate(sectors):
                sign = -1 if _q0(homology, count) ^ ((character & homology).bit_count() & 1) else 1
                total = (total + sign * weight) % prime
            values.append(total)
        return values

    values = tensor(weights)
    profile, _ = _profiles(values, 2 * count, prime)
    pair_ranks = [profile[2 * cut - 1] for cut in range(1, count)]
    if any(rank > 2 for rank in pair_ranks):
        raise AssertionError("K3,3-chain pair cut exceeded bond two")
    internal_minima = []
    internal_permutations = []
    for handle in range(count):
        best_rank = None
        best_permutation = None
        for permutation in permutations(range(4)):
            reindexed = [0] * len(values)
            shift = 2 * handle
            for new_index in range(len(values)):
                new_state = (new_index >> shift) & 3
                old_index = (new_index & ~(3 << shift)) | (permutation[new_state] << shift)
                reindexed[new_index] = values[old_index]
            candidate, _ = _profiles(reindexed, 2 * count, prime)
            rank = candidate[2 * handle]
            if best_rank is None or rank < best_rank:
                best_rank = rank
                best_permutation = list(permutation)
        internal_minima.append(best_rank)
        internal_permutations.append(best_permutation)
    embedded_witness = None
    if count in (2, 3):
        open_weights = weights[:]
        external_ports = {
            ((0, 0, 0), (0, 3, 0)),
            ((count - 1, 1, 0), (count - 1, 5, 0)),
        }
        zeroed = []
        for index, edge in enumerate(edges):
            if (edge.u, edge.v) in external_ports:
                open_weights[index] = 0
                zeroed.append(index)
        if len(zeroed) != 2:
            raise AssertionError("did not find both external witness ports")
        open_values = tensor(open_weights)
        cut = 2 if count == 2 else 3
        matrix = [
            [open_values[row | (column << cut)] for column in range(1 << (2 * count - cut))]
            for row in range(1 << cut)
        ]
        certificate = _rank_minor(matrix, prime)
        expected_rank = 2 if count == 2 else 4
        if certificate["rank"] != expected_rank:
            raise AssertionError("zero-port embeddable witness lost its target rank")
        permutation_ranks = None
        if count == 3:
            permutation_certificates = []
            for permutation in permutations(range(4)):
                reindexed = [0] * len(open_values)
                shift = 2
                for new_index in range(len(open_values)):
                    new_state = (new_index >> shift) & 3
                    old_index = (new_index & ~(3 << shift)) | (permutation[new_state] << shift)
                    reindexed[new_index] = open_values[old_index]
                permuted = [
                    [reindexed[row | (column << cut)] for column in range(1 << (2 * count - cut))]
                    for row in range(1 << cut)
                ]
                permutation_certificates.append({
                    "permutation": list(permutation),
                    "certificate": _rank_minor(permuted, prime),
                })
            permutation_ranks = [row["certificate"]["rank"] for row in permutation_certificates]
            if permutation_ranks != [4] * 24:
                raise AssertionError("an affine symplectic relabeling removed the open witness")
        embedded_witness = {
            "zeroed_external_port_edge_indices": zeroed,
            "cut_after_binary_coordinate": cut,
            "matrix_shape": [1 << cut, 1 << (2 * count - cut)],
            "rank_certificate": certificate,
            "all_24_affine_symplectic_local_relabeling_ranks": permutation_ranks,
            "all_24_relabeling_certificates": permutation_certificates if count == 3 else None,
        }
    return {
        "gadgets": count,
        "vertices": len(vertices),
        "edges": len(edges),
        "faces": len(faces),
        "genus": count,
        "cycle_dimension": len(cycle_basis),
        "face_boundary_rank": face_rank,
        "prime": prime,
        "binary_cut_rank_profile": profile,
        "pair_cut_ranks": pair_ranks,
        "all_pair_ranks_at_most_two": True,
        "all_internal_ranks_at_most_two": all(profile[2 * cut] <= 2 for cut in range(count)),
        "minimum_internal_ranks_under_affine_symplectic_handle_relabeling": internal_minima,
        "minimizing_local_state_permutations": internal_permutations,
        "embeddable_zero_port_witness": embedded_witness,
    }


def verify() -> dict[str, object]:
    # The base rotation has three hexagonal faces: V-E+F=0, hence genus one.
    rows = [_case(count, prime) for prime in PRIMES for count in range(1, 5)]
    return {
        "claim_status": "CERTIFIED_NUMERICAL exact GF(2) topology and finite-field tensor audit",
        "family": "iterated oriented edge-two-sums of toroidal K3,3 gadgets",
        "base_rotation": {str(vertex): list(neighbours) for vertex, neighbours in BASE_ROTATION.items()},
        "ports": {"left": [0, 3], "right": [1, 5]},
        "primes": list(PRIMES),
        "rows": rows,
        "claim_boundary": (
            "The abstract pair-cut theorem proves four-state handle-site bond <=2 for every "
            "chain length, and generic core splitting gives binary bond <=4.  These finite "
            "cases validate the explicit rotation, genus additivity, canonical local handle "
            "basis, pair ranks, and the internal-rank-four H3 obstruction; they are not the "
            "arbitrary-length proof."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
