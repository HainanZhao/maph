#!/usr/bin/env python3
"""Exact controls for Lane B embedding robustness and its limits."""

from __future__ import annotations

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
    _cup_product_intersection,
    _gf2_inverse,
    _homology_representatives,
    _symplectic_basis,
    _tree_cotree_intersection,
)
from src.conventions import Edge  # noqa: E402


PRIMES = (1_000_000_007, 1_000_000_009)
ROTATIONS = {
    "minimum_genus_one": {
        0: (3, 4, 5), 1: (3, 4, 5), 2: (3, 4, 5),
        3: (0, 1, 2), 4: (0, 1, 2), 5: (0, 1, 2),
    },
    "maximum_genus_two": {
        0: (3, 4, 5), 1: (3, 4, 5), 2: (3, 4, 5),
        3: (0, 1, 2), 4: (0, 1, 2), 5: (0, 2, 1),
    },
}


def _graph():
    vertices = tuple((0, vertex, 0) for vertex in range(6))
    edges = tuple(
        Edge((0, left, 0), (0, right, 0))
        for left in range(3) for right in range(3, 6)
    )
    rotations = {
        name: {
            (0, vertex, 0): tuple((0, neighbour, 0) for neighbour in cyclic)
            for vertex, cyclic in rotation.items()
        }
        for name, rotation in ROTATIONS.items()
    }
    return vertices, edges, rotations


def _q0(vector: int, genus: int) -> int:
    return sum(
        ((vector >> (2 * handle)) & 1) & ((vector >> (2 * handle + 1)) & 1)
        for handle in range(genus)
    ) & 1


def _case(name: str, rotation, prime: int) -> dict[str, object]:
    vertices, edges, _ = _graph()
    face_masks, face_walks = _rotation_faces(vertices, edges, rotation)
    genus = (2 - (len(vertices) - len(edges) + len(face_walks))) // 2
    cycles = _cycle_basis(vertices, edges)
    labels, face_rank = _edge_homology_labels(len(edges), face_masks, cycles, genus)
    tree, _ = _tree_cotree_intersection(
        vertices, edges, rotation, face_walks, labels, 2 * genus
    )
    independent_routes_agree = None
    if all(len(set(face)) == len(face) for face in face_walks):
        representatives = _homology_representatives(cycles, labels, 2 * genus)
        cup, _ = _cup_product_intersection(vertices, edges, face_walks, representatives)
        if cup != tree:
            raise AssertionError("K3,3 robustness intersection routes disagree")
        independent_routes_agree = True
    # The one-face maximum-genus walk repeats vertices, outside the pinned
    # face-center cup verifier's simplicial-input contract.  Tree-cotree is
    # exact there; the unavailable second route is reported, not invented.
    transport = _symplectic_basis(tree)
    inverse = _gf2_inverse(transport, 2 * genus)
    canonical_labels = [_matrix_vector(inverse, label) for label in labels]
    if _rank(canonical_labels) != 2 * genus:
        raise AssertionError("cellular graph does not surject onto surface homology")

    weights = [2 + 37 * index for index in range(len(edges))]
    sectors = [0] * (1 << (2 * genus))
    direct = 0
    for coefficients in range(1 << len(cycles)):
        chain = 0
        for index, cycle in enumerate(cycles):
            if (coefficients >> index) & 1:
                chain ^= cycle
        homology = 0
        weight = 1
        for index, label in enumerate(canonical_labels):
            if (chain >> index) & 1:
                homology ^= label
                weight = weight * weights[index] % prime
        sectors[homology] = (sectors[homology] + weight) % prime
        direct = (direct + weight) % prime
    f_values = []
    for character in range(1 << (2 * genus)):
        f_values.append(sum(
            (-weight if _q0(homology, genus) ^ ((character & homology).bit_count() & 1) else weight)
            for homology, weight in enumerate(sectors)
        ) % prime)
    arf_sum = 0
    for character, value in enumerate(f_values):
        arf = _q0(character, genus)
        arf_sum = (arf_sum + (-value if arf else value)) % prime
    arf_sum = arf_sum * pow(1 << genus, prime - 2, prime) % prime
    if arf_sum != direct:
        raise AssertionError("Arf sum changed the physical even-subgraph value")
    return {
        "rotation": name,
        "prime": prime,
        "faces": len(face_walks),
        "face_lengths": sorted(len(face) for face in face_walks),
        "genus": genus,
        "spin_structure_count": 1 << (2 * genus),
        "face_boundary_rank": face_rank,
        "graph_to_surface_homology_rank": _rank(canonical_labels),
        "independent_intersection_routes_agree": independent_routes_agree,
        "physical_even_subgraph_value": direct,
        "normalized_arf_sum": arf_sum,
        "physical_values_agree": True,
    }


def verify() -> dict[str, object]:
    _, _, rotations = _graph()
    rows = [
        _case(name, rotation, prime)
        for prime in PRIMES
        for name, rotation in rotations.items()
    ]
    genera = {row["rotation"]: row["genus"] for row in rows}
    if genera != {"minimum_genus_one": 1, "maximum_genus_two": 2}:
        raise AssertionError("alternative K3,3 rotation genus control failed")
    return {
        "claim_status": "CERTIFIED_NUMERICAL exact GF(2)/finite-field audit",
        "graph": "K3,3",
        "rotations": {
            name: {str(vertex): list(cyclic) for vertex, cyclic in rotation.items()}
            for name, rotation in ROTATIONS.items()
        },
        "primes": list(PRIMES),
        "rows": rows,
        "interpretation": (
            "The same abstract graph has cellular orientable embeddings of genus one and two, "
            "hence pre-Arf tensors with 4 and 16 entries.  Their normalized Arf contractions "
            "agree with the same direct even-subgraph value."
        ),
        "claim_boundary": (
            "This proves that the complete pre-Arf family is not invariant under arbitrary "
            "rotation changes.  It does not contradict the separator theorem, whose bound is "
            "conditional on a filtration-adapted embedding and basis."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
