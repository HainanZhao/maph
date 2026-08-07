#!/usr/bin/env python3
"""Exact rotation-system audit on the 2 x 2 x 2 cubic grid graph."""

from __future__ import annotations

from collections import Counter
from itertools import product
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.verify_lane_b_arbitrary_width_frontier import _matrix_vector, _rank  # noqa: E402
from proof.verify_lane_b_genus3 import (  # noqa: E402
    _cycle_basis,
    _edge_homology_labels,
    _rotation_faces,
)
from proof.verify_lane_b_intersection import (  # noqa: E402
    _gf2_inverse,
    _symplectic_basis,
    _tree_cotree_intersection,
)
from src.conventions import cubic_box  # noqa: E402


PRIMES = (1_000_000_007, 1_000_000_009)
SELECTED_BITS = {
    "planar_genus_zero": "01011010",
    "maximum_genus_two": "00000001",
}


def _q0(vector, genus):
    return sum(
        ((vector >> (2 * handle)) & 1) & ((vector >> (2 * handle + 1)) & 1)
        for handle in range(genus)
    ) & 1


def _rotations():
    vertices, edges = cubic_box((2, 2, 2))
    adjacency = {vertex: [] for vertex in vertices}
    for edge in edges:
        adjacency[edge.u].append(edge.v)
        adjacency[edge.v].append(edge.u)
    base = {vertex: tuple(sorted(adjacency[vertex])) for vertex in vertices}

    def rotation(bit_text):
        return {
            vertex: (base[vertex] if bit_text[index] == "0" else tuple(reversed(base[vertex])))
            for index, vertex in enumerate(vertices)
        }

    return vertices, edges, base, rotation


def _case(name, bit_text, prime):
    vertices, edges, _, rotation_from_bits = _rotations()
    rotation = rotation_from_bits(bit_text)
    face_masks, face_walks = _rotation_faces(vertices, edges, rotation)
    genus = (2 - (len(vertices) - len(edges) + len(face_walks))) // 2
    cycles = _cycle_basis(vertices, edges)
    labels, face_rank = _edge_homology_labels(
        len(edges), face_masks, cycles, genus
    ) if genus else ([0] * len(edges), len(face_walks) - 1)
    if genus:
        intersection, _ = _tree_cotree_intersection(
            vertices, edges, rotation, face_walks, labels, 2 * genus
        )
        transport = _symplectic_basis(intersection)
        inverse = _gf2_inverse(transport, 2 * genus)
        labels = [_matrix_vector(inverse, label) for label in labels]
        if _rank(labels) != 2 * genus:
            raise AssertionError("cube graph does not surject onto embedded surface homology")

    weights = [3 + 29 * index for index in range(len(edges))]
    sector_count = 1 << (2 * genus)
    sectors = [0] * sector_count
    direct = 0
    for coefficients in range(1 << len(cycles)):
        chain = 0
        for index, cycle in enumerate(cycles):
            if (coefficients >> index) & 1:
                chain ^= cycle
        homology = 0
        weight = 1
        for index, label in enumerate(labels):
            if (chain >> index) & 1:
                homology ^= label
                weight = weight * weights[index] % prime
        sectors[homology] = (sectors[homology] + weight) % prime
        direct = (direct + weight) % prime
    values = [
        sum(
            (-weight if _q0(homology, genus) ^ ((character & homology).bit_count() & 1) else weight)
            for homology, weight in enumerate(sectors)
        ) % prime
        for character in range(sector_count)
    ]
    arf = sum(
        (-value if _q0(character, genus) else value)
        for character, value in enumerate(values)
    ) % prime
    arf = arf * pow(1 << genus, prime - 2, prime) % prime
    if arf != direct:
        raise AssertionError("cube rotations changed the physical Arf contraction")
    return {
        "rotation": name,
        "bits_in_lexicographic_vertex_order": bit_text,
        "prime": prime,
        "face_count": len(face_walks),
        "face_lengths": sorted(map(len, face_walks)),
        "genus": genus,
        "spin_structure_count": sector_count,
        "face_boundary_rank": face_rank,
        "graph_to_surface_homology_rank": _rank(labels),
        "physical_even_subgraph_value": direct,
        "normalized_arf_sum": arf,
    }


def verify():
    vertices, edges, base, rotation_from_bits = _rotations()
    census = Counter()
    for bits in product((0, 1), repeat=len(vertices)):
        bit_text = "".join(map(str, bits))
        _, faces = _rotation_faces(vertices, edges, rotation_from_bits(bit_text))
        genus = (2 - (len(vertices) - len(edges) + len(faces))) // 2
        census[genus] += 1
    if census != Counter({0: 2, 1: 54, 2: 200}):
        raise AssertionError("cube rotation census changed")
    rows = [
        _case(name, bits, prime)
        for prime in PRIMES
        for name, bits in SELECTED_BITS.items()
    ]
    genera = {row["rotation"]: row["genus"] for row in rows}
    if genera != {"planar_genus_zero": 0, "maximum_genus_two": 2}:
        raise AssertionError("selected cube rotations lost their genera")
    return {
        "claim_status": "CERTIFIED_NUMERICAL exact exhaustive GF(2)/finite-field audit",
        "graph": "G_(2,2)=P_2 square P_2 square P_2 (the cube graph)",
        "vertex_order": [list(vertex) for vertex in vertices],
        "base_cyclic_orders": {
            str(vertex): [list(neighbour) for neighbour in cyclic]
            for vertex, cyclic in base.items()
        },
        "rotation_census": {str(genus): count for genus, count in sorted(census.items())},
        "selected_rotation_bits": SELECTED_BITS,
        "primes": list(PRIMES),
        "rows": rows,
        "interpretation": (
            "The same smallest cubic grid graph has orientable cellular rotations of genus "
            "zero and two, hence pre-Arf families of sizes one and sixteen, while their "
            "normalized Arf contractions equal the same even-subgraph polynomial values."
        ),
        "claim_boundary": (
            "This is an embedding-dependence obstruction for the complete pre-Arf family, "
            "not for the physical Ising polynomial and not for filtration-compatible rotations."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
