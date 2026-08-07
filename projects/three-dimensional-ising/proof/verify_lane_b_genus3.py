#!/usr/bin/env python3
"""Exact growing-genus tests for Lane B spin-structure compression."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys
from typing import Iterable

import sympy


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.verify_stage1_baseline import _gf2_nullspace_basis  # noqa: E402
from proof.verify_cycle2_five_lanes import _cubic_slab_data  # noqa: E402
from src.conventions import Edge, Vertex, cubic_box  # noqa: E402
from src.embeddings import SLAB_3X3X2_GENUS_ONE_ROTATION  # noqa: E402
from src.lane_b_genus3 import BOX_4X3X3_GENUS_THREE_ROTATION  # noqa: E402


Polynomial = tuple[int, ...]


def _edge_masks(edges: tuple[Edge, ...]) -> dict[tuple[Vertex, Vertex], int]:
    return {(edge.u, edge.v): 1 << index for index, edge in enumerate(edges)}


def _rotation_faces(
    vertices: tuple[Vertex, ...],
    edges: tuple[Edge, ...],
    rotation: dict[Vertex, tuple[Vertex, ...]],
) -> tuple[list[int], list[tuple[Vertex, ...]]]:
    masks = _edge_masks(edges)
    seen: set[tuple[Vertex, Vertex]] = set()
    face_masks: list[int] = []
    face_walks: list[tuple[Vertex, ...]] = []
    for source in vertices:
        for target in rotation[source]:
            if (source, target) in seen:
                continue
            walk: list[Vertex] = []
            mask = 0
            dart = source, target
            while dart not in seen:
                seen.add(dart)
                left, right = dart
                walk.append(left)
                mask ^= masks[tuple(sorted((left, right)))]
                cyclic = rotation[right]
                dart = right, cyclic[(cyclic.index(left) + 1) % len(cyclic)]
            face_masks.append(mask)
            face_walks.append(tuple(walk))
    if len(seen) != 2 * len(edges):
        raise AssertionError("rotation does not partition the darts")
    return face_masks, face_walks


def _elementary_squares(shape: tuple[int, int, int]) -> list[tuple[Vertex, ...]]:
    vertices, _ = cubic_box(shape)
    squares: list[tuple[Vertex, ...]] = []
    for vertex in vertices:
        for first, second in combinations(range(3), 2):
            a = list(vertex)
            b = list(vertex)
            opposite = list(vertex)
            a[first] += 1
            b[second] += 1
            opposite[first] += 1
            opposite[second] += 1
            if all(opposite[axis] < shape[axis] for axis in range(3)):
                squares.append((vertex, tuple(a), tuple(opposite), tuple(b)))
    return squares


def _canonical_cycle(cycle: tuple[Vertex, ...]) -> tuple[Vertex, ...]:
    candidates: list[tuple[Vertex, ...]] = []
    for oriented in (cycle, tuple(reversed(cycle))):
        candidates.extend(oriented[offset:] + oriented[:offset] for offset in range(len(cycle)))
    return min(candidates)


def _simple_cycles_of_length_six(
    vertices: tuple[Vertex, ...], edges: tuple[Edge, ...]
) -> list[tuple[Vertex, ...]]:
    adjacency = {vertex: [] for vertex in vertices}
    for edge in edges:
        adjacency[edge.u].append(edge.v)
        adjacency[edge.v].append(edge.u)
    cycles: set[tuple[Vertex, ...]] = set()
    for start in vertices:
        def extend(path: tuple[Vertex, ...]) -> None:
            if len(path) == 6:
                if start in adjacency[path[-1]]:
                    cycles.add(_canonical_cycle(path))
                return
            for neighbour in adjacency[path[-1]]:
                if neighbour not in path:
                    extend(path + (neighbour,))
        extend((start,))
    return sorted(cycles)


def _cycle_edge_indices(
    cycle: tuple[Vertex, ...], edge_index: dict[tuple[Vertex, Vertex], int]
) -> tuple[int, ...]:
    return tuple(
        edge_index[tuple(sorted((cycle[index], cycle[(index + 1) % len(cycle)])))]
        for index in range(len(cycle))
    )


def _square_cover_exists(
    square_edges: list[tuple[int, ...]],
    incident_squares: list[int],
    fixed_edges: Iterable[int],
    edge_count: int,
) -> bool:
    remaining = [2] * edge_count
    for edge in fixed_edges:
        remaining[edge] -= 1
    full_mask = (1 << len(square_edges)) - 1
    memo: set[tuple[tuple[int, ...], int]] = set()

    def search(capacities: tuple[int, ...], undecided: int) -> bool:
        key = capacities, undecided
        if key in memo:
            return False
        current = list(capacities)
        while True:
            forced_in = 0
            forced_out = 0
            for edge, capacity in enumerate(current):
                candidates = incident_squares[edge] & undecided
                available = candidates.bit_count()
                if capacity < 0 or capacity > available:
                    memo.add(key)
                    return False
                if capacity == 0:
                    forced_out |= candidates
                elif capacity == available:
                    forced_in |= candidates
            forced_in &= ~forced_out
            if forced_in & forced_out:
                memo.add(key)
                return False
            if not (forced_in | forced_out):
                break
            for square in range(len(square_edges)):
                bit = 1 << square
                if forced_in & bit:
                    for edge in square_edges[square]:
                        current[edge] -= 1
            undecided &= ~(forced_in | forced_out)
        if all(capacity == 0 for capacity in current):
            return True
        choices = []
        for edge, capacity in enumerate(current):
            if capacity:
                candidates = incident_squares[edge] & undecided
                choices.append((candidates.bit_count(), candidates))
        if not choices:
            memo.add(key)
            return False
        _, candidates = min(choices)
        square_bit = candidates & -candidates
        square = square_bit.bit_length() - 1
        included = current[:]
        for edge in square_edges[square]:
            included[edge] -= 1
        if search(tuple(included), undecided ^ square_bit):
            return True
        if search(tuple(current), undecided ^ square_bit):
            return True
        memo.add(key)
        return False

    return search(tuple(remaining), full_mask)


def _minimum_genus_certificate() -> dict[str, object]:
    vertices, edges = cubic_box((4, 3, 3))
    adjacency = {vertex: set() for vertex in vertices}
    for edge in edges:
        adjacency[edge.u].add(edge.v)
        adjacency[edge.v].add(edge.u)
    rotation = BOX_4X3X3_GENUS_THREE_ROTATION
    if set(rotation) != set(vertices):
        raise AssertionError("rotation vertex set mismatch")
    if any(set(rotation[vertex]) != adjacency[vertex] for vertex in vertices):
        raise AssertionError("rotation neighbour set mismatch")
    face_masks, face_walks = _rotation_faces(vertices, edges, rotation)
    face_lengths = sorted(map(len, face_walks))
    euler_characteristic = len(vertices) - len(edges) + len(face_walks)
    genus = (2 - euler_characteristic) // 2
    if genus != 3 or face_lengths != [4] * 34 + [14]:
        raise AssertionError("pinned rotation is not the claimed genus-three embedding")

    edge_index = {(edge.u, edge.v): index for index, edge in enumerate(edges)}
    squares = _elementary_squares((4, 3, 3))
    square_edges = [_cycle_edge_indices(square, edge_index) for square in squares]
    incident = [0] * len(edges)
    for square, boundary in enumerate(square_edges):
        for edge in boundary:
            incident[edge] |= 1 << square
    hexagons = _simple_cycles_of_length_six(vertices, edges)
    feasible_hexagons = []
    for hexagon in hexagons:
        boundary = _cycle_edge_indices(hexagon, edge_index)
        if _square_cover_exists(square_edges, incident, boundary, len(edges)):
            feasible_hexagons.append(hexagon)
    if feasible_hexagons:
        raise AssertionError("a genus-two face-incidence cover survived")
    long_face = next(walk for walk in face_walks if len(walk) == 14)
    if not _square_cover_exists(
        square_edges,
        incident,
        _cycle_edge_indices(long_face, edge_index),
        len(edges),
    ):
        raise AssertionError("cover solver rejected the pinned genus-three face census")

    return {
        "shape": [4, 3, 3],
        "vertices": len(vertices),
        "edges": len(edges),
        "embedding_faces": len(face_walks),
        "embedding_face_lengths": face_lengths,
        "embedding_genus": genus,
        "elementary_four_cycles": len(squares),
        "simple_six_cycles_exhausted": len(hexagons),
        "genus_two_face_covers": len(feasible_hexagons),
        "positive_cover_solver_control": "34 squares plus pinned 14-gon accepted",
        "minimum_orientable_genus": 3,
    }


def _cycle_basis(vertices: tuple[Vertex, ...], edges: tuple[Edge, ...]) -> list[int]:
    vertex_index = {vertex: index for index, vertex in enumerate(vertices)}
    incidence_rows = [0] * len(vertices)
    for index, edge in enumerate(edges):
        incidence_rows[vertex_index[edge.u]] |= 1 << index
        incidence_rows[vertex_index[edge.v]] |= 1 << index
    return _gf2_nullspace_basis(incidence_rows, len(edges))


def _add_labeled_vector(
    basis: dict[int, tuple[int, int]], vector: int, label: int
) -> bool:
    while vector:
        pivot = vector.bit_length() - 1
        if pivot in basis:
            old_vector, old_label = basis[pivot]
            vector ^= old_vector
            label ^= old_label
        else:
            basis[pivot] = vector, label
            return True
    if label:
        raise AssertionError("inconsistent labeled GF(2) relation")
    return False


def _vector_independent(basis: dict[int, tuple[int, int]], vector: int) -> bool:
    """Test span membership while deliberately ignoring stored labels."""
    while vector:
        pivot = vector.bit_length() - 1
        if pivot not in basis:
            return True
        vector ^= basis[pivot][0]
    return False


def _edge_homology_labels(
    edge_count: int, face_masks: list[int], cycle_basis: list[int], genus: int
) -> tuple[list[int], int]:
    basis: dict[int, tuple[int, int]] = {}
    for face in face_masks:
        _add_labeled_vector(basis, face, 0)
    face_rank = len(basis)
    quotient_count = 0
    for cycle in cycle_basis:
        if _vector_independent(basis, cycle):
            if quotient_count >= 2 * genus:
                raise AssertionError("homology quotient is larger than expected")
            _add_labeled_vector(basis, cycle, 1 << quotient_count)
            quotient_count += 1
    if quotient_count != 2 * genus:
        raise AssertionError("homology quotient dimension mismatch")
    for edge in range(edge_count):
        unit = 1 << edge
        if _vector_independent(basis, unit):
            _add_labeled_vector(basis, unit, 0)

    labels: list[int] = []
    for edge in range(edge_count):
        vector = 1 << edge
        label = 0
        while vector:
            pivot = vector.bit_length() - 1
            old_vector, old_label = basis[pivot]
            vector ^= old_vector
            label ^= old_label
        labels.append(label)
    return labels, face_rank


def _add_shifted(target: list[int], source: Polynomial) -> None:
    if len(target) < len(source) + 1:
        target.extend([0] * (len(source) + 1 - len(target)))
    for degree, coefficient in enumerate(source):
        target[degree + 1] += coefficient


def _frontier_sector_polynomials(
    vertices: tuple[Vertex, ...], edges: tuple[Edge, ...], labels: list[int]
) -> tuple[dict[int, Polynomial], int]:
    vertex_index = {vertex: index for index, vertex in enumerate(vertices)}
    ordered = sorted(
        zip(edges, labels),
        key=lambda pair: (
            max(vertex_index[pair[0].u], vertex_index[pair[0].v]),
            min(vertex_index[pair[0].u], vertex_index[pair[0].v]),
        ),
    )
    last_incident = [-1] * len(vertices)
    for position, (edge, _) in enumerate(ordered):
        last_incident[vertex_index[edge.u]] = position
        last_incident[vertex_index[edge.v]] = position
    states: dict[tuple[int, int], Polynomial] = {(0, 0): (1,)}
    maximum_states = 1
    for position, (edge, label) in enumerate(ordered):
        parity_flip = (1 << vertex_index[edge.u]) | (1 << vertex_index[edge.v])
        updated: dict[tuple[int, int], list[int]] = {
            key: list(polynomial) for key, polynomial in states.items()
        }
        for (parity, homology), polynomial in states.items():
            key = parity ^ parity_flip, homology ^ label
            if key not in updated:
                updated[key] = [0] * (len(polynomial) + 1)
            _add_shifted(updated[key], polynomial)
        forgotten = 0
        for vertex, last in enumerate(last_incident):
            if last == position:
                forgotten |= 1 << vertex
        states = {
            (parity & ~forgotten, homology): tuple(polynomial)
            for (parity, homology), polynomial in updated.items()
            if not (parity & forgotten)
        }
        maximum_states = max(maximum_states, len(states))
        if maximum_states > 2_000_000:
            raise RuntimeError("declared frontier-state cap exceeded")
    sectors = {homology: polynomial for (parity, homology), polynomial in states.items()}
    if any(parity for parity, _ in states):
        raise AssertionError("nonzero parity survived final forgetting")
    return sectors, maximum_states


def _evaluate(polynomial: Polynomial, value: Fraction) -> Fraction:
    result = Fraction(0)
    for coefficient in reversed(polynomial):
        result = result * value + coefficient
    return result


def _character_transfer(
    vertices: tuple[Vertex, ...],
    edges: tuple[Edge, ...],
    labels: list[int],
    character: int,
    value: Fraction,
) -> Fraction:
    vertex_index = {vertex: index for index, vertex in enumerate(vertices)}
    ordered = sorted(
        zip(edges, labels),
        key=lambda pair: (
            max(vertex_index[pair[0].u], vertex_index[pair[0].v]),
            min(vertex_index[pair[0].u], vertex_index[pair[0].v]),
        ),
    )
    last_incident = [-1] * len(vertices)
    for position, (edge, _) in enumerate(ordered):
        last_incident[vertex_index[edge.u]] = position
        last_incident[vertex_index[edge.v]] = position
    states = {0: Fraction(1)}
    for position, (edge, label) in enumerate(ordered):
        flip = (1 << vertex_index[edge.u]) | (1 << vertex_index[edge.v])
        sign = -1 if (character & label).bit_count() % 2 else 1
        updated = dict(states)
        for parity, weight in states.items():
            updated[parity ^ flip] = updated.get(parity ^ flip, Fraction(0)) + sign * value * weight
        forgotten = 0
        for vertex, last in enumerate(last_incident):
            if last == position:
                forgotten |= 1 << vertex
        states = {
            parity & ~forgotten: weight
            for parity, weight in updated.items()
            if not (parity & forgotten)
        }
    return states[0]


def _walsh_reconstruct(
    characters: list[Fraction], dimension: int
) -> list[Fraction]:
    return [
        sum(
            (-value if (character & homology).bit_count() % 2 else value)
            for character, value in enumerate(characters)
        ) / (1 << dimension)
        for homology in range(1 << dimension)
    ]


def _reference_f_values(
    sector_values: list[Fraction], dimension: int
) -> list[Fraction]:
    if dimension % 2:
        raise ValueError("a symplectic reference form needs even dimension")
    quadratic = []
    for homology in range(1 << dimension):
        value = 0
        for handle in range(dimension // 2):
            value ^= ((homology >> (2 * handle)) & 1) & ((homology >> (2 * handle + 1)) & 1)
        quadratic.append(value)
    return [
        sum(
            (-weight if quadratic[h] ^ ((linear & h).bit_count() % 2) else weight)
            for h, weight in enumerate(sector_values)
        )
        for linear in range(1 << dimension)
    ]


def _tt_ranks(values: list[Fraction], dimension: int) -> list[int]:
    ranks = []
    for cut in range(1, dimension):
        rows, columns = 1 << cut, 1 << (dimension - cut)
        matrix = sympy.Matrix(
            rows,
            columns,
            lambda row, column: values[row | (column << cut)],
        )
        ranks.append(matrix.rank())
    return ranks


def _reference_handle_rank_profiles(
    values: list[Fraction], genus: int
) -> dict[str, int]:
    """Ranks under handle permutations and swaps within each handle."""
    profiles: Counter[tuple[int, ...]] = Counter()
    for handle_order in permutations(range(genus)):
        for flips in product((0, 1), repeat=genus):
            bit_order: list[int] = []
            for position, handle in enumerate(handle_order):
                pair = [2 * handle, 2 * handle + 1]
                if flips[position]:
                    pair.reverse()
                bit_order.extend(pair)
            permuted: list[Fraction] = []
            for new_index in range(1 << (2 * genus)):
                old_index = sum(
                    ((new_index >> new_bit) & 1) << old_bit
                    for new_bit, old_bit in enumerate(bit_order)
                )
                permuted.append(values[old_index])
            profiles[tuple(_tt_ranks(permuted, 2 * genus))] += 1
    return {",".join(map(str, profile)): count for profile, count in sorted(profiles.items())}


def _sector_data(
    shape: tuple[int, int, int], rotation: dict[Vertex, tuple[Vertex, ...]], genus: int
) -> dict[str, object]:
    vertices, edges = cubic_box(shape)
    face_masks, _ = _rotation_faces(vertices, edges, rotation)
    labels, face_rank = _edge_homology_labels(
        len(edges), face_masks, _cycle_basis(vertices, edges), genus
    )
    sectors, maximum_states = _frontier_sector_polynomials(vertices, edges, labels)
    dimension = 2 * genus
    if len(sectors) != 1 << dimension:
        raise AssertionError("not every homology sector was produced")
    if {sum(polynomial) for polynomial in sectors.values()} != {1 << face_rank}:
        raise AssertionError("homology sectors do not have equal cardinality")

    evaluations: dict[str, object] = {}
    for value in (Fraction(1, 2), Fraction(1, 3)):
        direct = [_evaluate(sectors[h], value) for h in range(1 << dimension)]
        characters = [
            _character_transfer(vertices, edges, labels, character, value)
            for character in range(1 << dimension)
        ]
        reconstructed = _walsh_reconstruct(characters, dimension)
        if reconstructed != direct:
            raise AssertionError("character/Walsh reconstruction mismatch")
        reference_f = _reference_f_values(direct, dimension)
        evaluations[str(value)] = {
            "independent_character_reconstruction": True,
            "reference_quadratic_TT_ranks": _tt_ranks(reference_f, dimension),
            "reference_handle_ordering_rank_profiles": _reference_handle_rank_profiles(
                reference_f, genus
            ),
        }
    return {
        "shape": list(shape),
        "genus": genus,
        "homology_dimension": dimension,
        "face_boundary_rank": face_rank,
        "cycle_space_dimension": len(edges) - len(vertices) + 1,
        "sector_count": len(sectors),
        "sector_cardinality": 1 << face_rank,
        "maximum_frontier_states": maximum_states,
        "sector_polynomials": {
            format(h, f"0{dimension}b"): {
                str(degree): coefficient
                for degree, coefficient in enumerate(sectors[h])
                if coefficient
            }
            for h in range(1 << dimension)
        },
        "evaluations": evaluations,
    }


def verify() -> dict[str, object]:
    minimum_genus = _minimum_genus_certificate()
    slab = _sector_data((3, 3, 2), SLAB_3X3X2_GENUS_ONE_ROTATION, 1)
    sealed_slab = _cubic_slab_data()["homology_sector_polynomials"]
    calibration_relabeling = {"00": "00", "01": "10", "10": "01", "11": "11"}
    if any(
        slab["sector_polynomials"][new] != sealed_slab[old]
        for new, old in calibration_relabeling.items()
    ):
        raise AssertionError("frontier sectors disagree with sealed direct enumeration")
    slab["sealed_direct_enumeration_reproduced"] = True
    slab["calibration_basis_relabeling"] = calibration_relabeling
    box = _sector_data((4, 3, 3), BOX_4X3X3_GENUS_THREE_ROTATION, 3)
    return {
        "claim_status": "COMPUTATIONALLY_VERIFIED",
        "minimum_genus_certificate": minimum_genus,
        "genus_one_calibration": slab,
        "genus_three_box": box,
        "claim_boundary": (
            "The minimum-genus and sector-polynomial claims use exact finite computation. "
            "The displayed F ranks use a reference symplectic quadratic form on the computed "
            "quotient coordinates; identifying it with the embedding intersection form and "
            "searching all symplectic handle bases remain open."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
