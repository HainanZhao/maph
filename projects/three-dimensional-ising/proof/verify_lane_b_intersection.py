#!/usr/bin/env python3
"""Two exact labeled constructions of the Lane B intersection form.

Route A triangulates every face by a new center and evaluates the
Alexander--Whitney cup product on cohomology classes dual to the pinned
homology coordinates.

Route B performs a deterministic tree--cotree reduction of the combinatorial
map to a one-vertex, one-face map.  Its remaining loops form a chord diagram;
mod-two intersection is endpoint interlacement.  The loop basis is then
transported to the same pinned homology coordinates as Route A.
"""

from __future__ import annotations

from collections import deque
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.verify_lane_b_genus3 import (  # noqa: E402
    _cycle_basis,
    _edge_homology_labels,
    _rotation_faces,
)
from src.conventions import Edge, Vertex, cubic_box  # noqa: E402
from src.embeddings import SLAB_3X3X2_GENUS_ONE_ROTATION  # noqa: E402
from src.lane_b_genus3 import BOX_4X3X3_GENUS_THREE_ROTATION  # noqa: E402


def _parity(integer: int) -> int:
    return integer.bit_count() & 1


def _gf2_rank(rows: list[int]) -> int:
    basis: dict[int, int] = {}
    for row in rows:
        while row:
            pivot = row.bit_length() - 1
            if pivot in basis:
                row ^= basis[pivot]
            else:
                basis[pivot] = row
                break
    return len(basis)


def _gf2_solve(rows: list[tuple[int, int]], variables: int) -> int:
    """Return one solution of an exact GF(2) linear system, free bits zero."""
    basis: dict[int, tuple[int, int]] = {}
    for mask, right in rows:
        while mask:
            pivot = mask.bit_length() - 1
            if pivot in basis:
                old_mask, old_right = basis[pivot]
                mask ^= old_mask
                right ^= old_right
            else:
                basis[pivot] = mask, right
                break
        else:
            if right:
                raise AssertionError("inconsistent GF(2) system")
    solution = 0
    for pivot in sorted(basis):
        mask, right = basis[pivot]
        lower = mask ^ (1 << pivot)
        value = right ^ _parity(lower & solution)
        if value:
            solution |= 1 << pivot
    if any(_parity(mask & solution) != right for mask, right in rows):
        raise AssertionError("GF(2) solver regression")
    return solution


def _gf2_inverse(rows: list[int], dimension: int) -> list[int]:
    """Invert a square matrix represented by row bitmasks."""
    augmented = [rows[row] | (1 << (dimension + row)) for row in range(dimension)]
    for column in range(dimension):
        pivot = next((row for row in range(column, dimension) if (augmented[row] >> column) & 1), None)
        if pivot is None:
            raise AssertionError("matrix is singular over GF(2)")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        for row in range(dimension):
            if row != column and ((augmented[row] >> column) & 1):
                augmented[row] ^= augmented[column]
    if [row & ((1 << dimension) - 1) for row in augmented] != [1 << row for row in range(dimension)]:
        raise AssertionError("GF(2) inversion regression")
    return [row >> dimension for row in augmented]


def _matrix_multiply(left: list[int], right: list[int], dimension: int) -> list[int]:
    """Multiply GF(2) matrices represented as row masks."""
    result = []
    for left_row in left:
        row = 0
        for index in range(dimension):
            if (left_row >> index) & 1:
                row ^= right[index]
        result.append(row)
    return result


def _transpose(rows: list[int], dimension: int) -> list[int]:
    return [
        sum(((rows[row] >> column) & 1) << row for row in range(dimension))
        for column in range(dimension)
    ]


def _quadratic_value(matrix: list[int], left: int, right: int) -> int:
    return _parity(matrix_row_combination(matrix, left) & right)


def matrix_row_combination(matrix: list[int], coefficients: int) -> int:
    result = 0
    for row, mask in enumerate(matrix):
        if (coefficients >> row) & 1:
            result ^= mask
    return result


def _homology_representatives(
    cycles: list[int], edge_labels: list[int], dimension: int
) -> list[int]:
    representatives: list[int | None] = [None] * dimension
    for cycle in cycles:
        label = 0
        for edge, edge_label in enumerate(edge_labels):
            if (cycle >> edge) & 1:
                label ^= edge_label
        if label and label & (label - 1) == 0:
            coordinate = label.bit_length() - 1
            if representatives[coordinate] is None:
                representatives[coordinate] = cycle
    if any(cycle is None for cycle in representatives):
        raise AssertionError("could not recover the pinned homology representatives")
    return [int(cycle) for cycle in representatives]


def _cup_product_intersection(
    vertices: tuple[Vertex, ...],
    edges: tuple[Edge, ...],
    face_walks: list[tuple[Vertex, ...]],
    representatives: list[int],
) -> tuple[list[int], dict[str, object]]:
    """Route A: cup product on the face-center triangulation."""
    vertex_id = {vertex: index for index, vertex in enumerate(vertices)}
    triangulated_edges: dict[tuple[int, int], int] = {}
    triangles: list[tuple[int, int, int]] = []

    def edge_id(left: int, right: int) -> int:
        pair = tuple(sorted((left, right)))
        if pair not in triangulated_edges:
            triangulated_edges[pair] = len(triangulated_edges)
        return triangulated_edges[pair]

    original_edge_to_triangle_edge = []
    for edge in edges:
        original_edge_to_triangle_edge.append(edge_id(vertex_id[edge.u], vertex_id[edge.v]))
    for face, walk in enumerate(face_walks):
        center = len(vertices) + face
        for index, vertex in enumerate(walk):
            left = vertex_id[vertex]
            right = vertex_id[walk[(index + 1) % len(walk)]]
            edge_id(center, left)
            edge_id(center, right)
            triangles.append(tuple(sorted((center, left, right))))

    triangle_boundaries: list[int] = []
    for a, b, c in triangles:
        triangle_boundaries.append(
            (1 << edge_id(a, b)) | (1 << edge_id(a, c)) | (1 << edge_id(b, c))
        )
    cocycles: list[int] = []
    for target in range(len(representatives)):
        equations = [(boundary, 0) for boundary in triangle_boundaries]
        for coordinate, cycle in enumerate(representatives):
            evaluation = 0
            for original_edge, triangle_edge in enumerate(original_edge_to_triangle_edge):
                if (cycle >> original_edge) & 1:
                    evaluation |= 1 << triangle_edge
            equations.append((evaluation, int(coordinate == target)))
        cocycles.append(_gf2_solve(equations, len(triangulated_edges)))

    cup_rows: list[int] = []
    for left in cocycles:
        row = 0
        for column, right in enumerate(cocycles):
            value = 0
            for a, b, c in triangles:
                value ^= ((left >> edge_id(a, b)) & 1) & ((right >> edge_id(b, c)) & 1)
            row |= value << column
        cup_rows.append(row)
    if cup_rows != _transpose(cup_rows, len(cup_rows)):
        raise AssertionError("cup pairing is not symmetric on cohomology")
    if any((row >> index) & 1 for index, row in enumerate(cup_rows)):
        raise AssertionError("cup pairing is not alternating")
    intersection = _gf2_inverse(cup_rows, len(cup_rows))
    return intersection, {
        "triangulated_vertices": len(vertices) + len(face_walks),
        "triangulated_edges": len(triangulated_edges),
        "triangles": len(triangles),
        "cohomology_cup_matrix_rows": cup_rows,
        "homology_intersection_matrix_rows": intersection,
    }


class _DisjointSet:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))

    def find(self, value: int) -> int:
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def union(self, left: int, right: int) -> bool:
        left, right = self.find(left), self.find(right)
        if left == right:
            return False
        self.parent[right] = left
        return True


def _tree_cotree_sets(
    vertices: tuple[Vertex, ...], edges: tuple[Edge, ...], face_walks: list[tuple[Vertex, ...]]
) -> tuple[set[int], set[int], list[int]]:
    edge_index = {(edge.u, edge.v): index for index, edge in enumerate(edges)}
    adjacency: dict[Vertex, list[tuple[Vertex, int]]] = {vertex: [] for vertex in vertices}
    for index, edge in enumerate(edges):
        adjacency[edge.u].append((edge.v, index))
        adjacency[edge.v].append((edge.u, index))
    primal_tree: set[int] = set()
    reached = {vertices[0]}
    queue = deque([vertices[0]])
    while queue:
        vertex = queue.popleft()
        for neighbour, edge in sorted(adjacency[vertex]):
            if neighbour not in reached:
                reached.add(neighbour)
                queue.append(neighbour)
                primal_tree.add(edge)
    if len(primal_tree) != len(vertices) - 1:
        raise AssertionError("primal spanning tree failure")

    incident_faces: list[list[int]] = [[] for _ in edges]
    for face, walk in enumerate(face_walks):
        for index, left in enumerate(walk):
            right = walk[(index + 1) % len(walk)]
            incident_faces[edge_index[tuple(sorted((left, right)))]].append(face)
    if any(len(incidence) != 2 for incidence in incident_faces):
        raise AssertionError("each surface edge must have two incident face sides")
    dual_dsu = _DisjointSet(len(face_walks))
    dual_tree: set[int] = set()
    for edge, faces in enumerate(incident_faces):
        if edge not in primal_tree and dual_dsu.union(faces[0], faces[1]):
            dual_tree.add(edge)
    if len(dual_tree) != len(face_walks) - 1:
        raise AssertionError("dual spanning tree failure")
    leftovers = [edge for edge in range(len(edges)) if edge not in primal_tree | dual_tree]
    return primal_tree, dual_tree, leftovers


def _tree_paths(
    vertices: tuple[Vertex, ...], edges: tuple[Edge, ...], tree: set[int]
) -> dict[tuple[Vertex, Vertex], int]:
    adjacency: dict[Vertex, list[tuple[Vertex, int]]] = {vertex: [] for vertex in vertices}
    for edge_index in tree:
        edge = edges[edge_index]
        adjacency[edge.u].append((edge.v, edge_index))
        adjacency[edge.v].append((edge.u, edge_index))
    paths: dict[tuple[Vertex, Vertex], int] = {}
    for source in vertices:
        queue = deque([(source, 0)])
        reached = {source}
        while queue:
            vertex, mask = queue.popleft()
            paths[source, vertex] = mask
            for neighbour, edge in adjacency[vertex]:
                if neighbour not in reached:
                    reached.add(neighbour)
                    queue.append((neighbour, mask ^ (1 << edge)))
    return paths


def _reduced_boundary_word(
    vertices: tuple[Vertex, ...],
    edges: tuple[Edge, ...],
    rotation: dict[Vertex, tuple[Vertex, ...]],
    primal_tree: set[int],
    dual_tree: set[int],
) -> list[int]:
    dart: dict[tuple[Vertex, Vertex], int] = {}
    alpha: dict[int, int] = {}
    for edge_index, edge in enumerate(edges):
        forward, reverse = 2 * edge_index, 2 * edge_index + 1
        dart[edge.u, edge.v] = forward
        dart[edge.v, edge.u] = reverse
        alpha[forward] = reverse
        alpha[reverse] = forward
    sigma: dict[int, int] = {}
    for vertex in vertices:
        cyclic = rotation[vertex]
        for index, neighbour in enumerate(cyclic):
            sigma[dart[vertex, neighbour]] = dart[vertex, cyclic[(index + 1) % len(cyclic)]]

    def cycle_without(removed: int) -> list[int]:
        result: list[int] = []
        current = sigma[removed]
        while current != removed:
            result.append(current)
            current = sigma[current]
        return result

    def set_cycle(cycle: list[int]) -> None:
        for index, current in enumerate(cycle):
            sigma[current] = cycle[(index + 1) % len(cycle)]

    # Dual-tree deletion merges all faces while preserving the vertex cycles.
    for edge in sorted(dual_tree):
        left, right = 2 * edge, 2 * edge + 1
        left_cycle = cycle_without(left)
        right_cycle = cycle_without(right)
        del sigma[left]
        del sigma[right]
        if left_cycle:
            set_cycle(left_cycle)
        if right_cycle:
            set_cycle(right_cycle)

    # Primal-tree contraction merges all vertex cycles while preserving the face.
    for edge in sorted(primal_tree):
        left, right = 2 * edge, 2 * edge + 1
        left_cycle = cycle_without(left)
        right_cycle = cycle_without(right)
        del sigma[left]
        del sigma[right]
        merged = left_cycle + right_cycle
        if merged:
            set_cycle(merged)

    remaining = sorted(sigma)
    if not remaining:
        raise AssertionError("tree-cotree reduction removed every dart")
    vertex_cycle = []
    current = remaining[0]
    while current not in vertex_cycle:
        vertex_cycle.append(current)
        current = sigma[current]
    if set(vertex_cycle) != set(remaining):
        raise AssertionError("reduced map does not have one vertex")
    face_word: list[int] = []
    current = remaining[0]
    visited: set[int] = set()
    while current not in visited:
        visited.add(current)
        face_word.append(current // 2)
        current = sigma[alpha[current]]
    if set(visited) != set(remaining):
        raise AssertionError("reduced map does not have one face")
    return face_word


def _tree_cotree_intersection(
    vertices: tuple[Vertex, ...],
    edges: tuple[Edge, ...],
    rotation: dict[Vertex, tuple[Vertex, ...]],
    face_walks: list[tuple[Vertex, ...]],
    edge_labels: list[int],
    dimension: int,
) -> tuple[list[int], dict[str, object]]:
    """Route B: tree-cotree reduction and chord interlacement."""
    primal_tree, dual_tree, leftovers = _tree_cotree_sets(vertices, edges, face_walks)
    if len(leftovers) != dimension:
        raise AssertionError("tree-cotree leftover count is not 2g")
    word = _reduced_boundary_word(vertices, edges, rotation, primal_tree, dual_tree)
    if len(word) != 2 * dimension or any(word.count(edge) != 2 for edge in leftovers):
        raise AssertionError("reduced boundary word is not a paired chord word")
    positions = {edge: [index for index, value in enumerate(word) if value == edge] for edge in leftovers}
    chord_rows: list[int] = []
    for left_index, left in enumerate(leftovers):
        first, second = positions[left]
        row = 0
        for right_index, right in enumerate(leftovers):
            between = sum(first < position < second for position in positions[right])
            row |= (between & 1) << right_index
        chord_rows.append(row)
    if chord_rows != _transpose(chord_rows, dimension):
        raise AssertionError("chord interlacement is not symmetric")
    if _gf2_rank(chord_rows) != dimension:
        raise AssertionError("chord interlacement is degenerate")

    tree_paths = _tree_paths(vertices, edges, primal_tree)
    columns: list[int] = []
    for edge_index in leftovers:
        edge = edges[edge_index]
        cycle = tree_paths[edge.u, edge.v] ^ (1 << edge_index)
        label = 0
        for index, edge_label in enumerate(edge_labels):
            if (cycle >> index) & 1:
                label ^= edge_label
        columns.append(label)
    # H maps leftover-loop coordinates to pinned homology coordinates.
    homology_map_rows = [
        sum(((columns[column] >> row) & 1) << column for column in range(dimension))
        for row in range(dimension)
    ]
    inverse = _gf2_inverse(homology_map_rows, dimension)
    # Endpoint interlacement is the cup matrix in the cohomology basis dual
    # to the bouquet edges.  The homology intersection matrix in the bouquet
    # edge basis is its inverse.  The distinction is invisible at genus one,
    # where the standard 2x2 symplectic matrix is self-inverse.
    loop_intersection = _gf2_inverse(chord_rows, dimension)
    transported = _matrix_multiply(
        _transpose(inverse, dimension),
        _matrix_multiply(loop_intersection, inverse, dimension),
        dimension,
    )
    return transported, {
        "primal_tree_edges": sorted(primal_tree),
        "dual_tree_edges": sorted(dual_tree),
        "leftover_edges": leftovers,
        "reduced_boundary_word": word,
        "chord_cohomology_cup_matrix_rows": chord_rows,
        "bouquet_homology_intersection_matrix_rows": loop_intersection,
        "leftover_to_pinned_homology_rows": homology_map_rows,
        "homology_intersection_matrix_rows": transported,
    }


def _symplectic_basis(intersection: list[int]) -> list[int]:
    """Deterministic symplectic Gram--Schmidt; columns are new basis vectors."""
    dimension = len(intersection)
    remaining = [1 << index for index in range(dimension)]
    basis: list[int] = []
    while remaining:
        first = remaining.pop(0)
        partner_index = next(
            (index for index, candidate in enumerate(remaining) if _quadratic_value(intersection, first, candidate)),
            None,
        )
        if partner_index is None:
            raise AssertionError("intersection form became degenerate during symplectic reduction")
        second = remaining.pop(partner_index)
        adjusted = []
        for vector in remaining:
            if _quadratic_value(intersection, vector, second):
                vector ^= first
            if _quadratic_value(intersection, vector, first):
                vector ^= second
            adjusted.append(vector)
        basis.extend((first, second))
        remaining = adjusted
    # Return the matrix whose columns are the symplectic basis vectors.
    transport_rows = [
        sum(((basis[column] >> row) & 1) << column for column in range(dimension))
        for row in range(dimension)
    ]
    canonical = [
        (1 << (index ^ 1)) for index in range(dimension)
    ]
    transformed = _matrix_multiply(
        _transpose(transport_rows, dimension),
        _matrix_multiply(intersection, transport_rows, dimension),
        dimension,
    )
    if transformed != canonical:
        raise AssertionError("symplectic basis transport check failed")
    return transport_rows


def _graph_result(
    shape: tuple[int, int, int],
    rotation: dict[Vertex, tuple[Vertex, ...]],
    genus: int,
) -> dict[str, object]:
    vertices, edges = cubic_box(shape)
    face_masks, face_walks = _rotation_faces(vertices, edges, rotation)
    cycles = _cycle_basis(vertices, edges)
    edge_labels, face_rank = _edge_homology_labels(len(edges), face_masks, cycles, genus)
    dimension = 2 * genus
    representatives = _homology_representatives(cycles, edge_labels, dimension)
    cup, cup_data = _cup_product_intersection(vertices, edges, face_walks, representatives)
    tree_cotree, tree_cotree_data = _tree_cotree_intersection(
        vertices, edges, rotation, face_walks, edge_labels, dimension
    )
    if cup != tree_cotree:
        raise AssertionError(
            f"independent intersection routes disagree: cup={cup}, tree-cotree={tree_cotree}"
        )
    if cup != _transpose(cup, dimension) or any((cup[index] >> index) & 1 for index in range(dimension)):
        raise AssertionError("intersection form is not alternating")
    if _gf2_rank(cup) != dimension:
        raise AssertionError("intersection form is degenerate")
    symplectic = _symplectic_basis(cup)
    return {
        "shape": list(shape),
        "genus": genus,
        "face_boundary_rank": face_rank,
        "pinned_homology_representatives": representatives,
        "intersection_matrix_rows": cup,
        "intersection_matrix_binary": [format(row, f"0{dimension}b")[::-1] for row in cup],
        "rank": _gf2_rank(cup),
        "alternating": True,
        "independent_routes_agree_with_labels": True,
        "symplectic_transport_rows": symplectic,
        "cup_product_route": cup_data,
        "tree_cotree_route": tree_cotree_data,
    }


def verify() -> dict[str, object]:
    slab = _graph_result((3, 3, 2), SLAB_3X3X2_GENUS_ONE_ROTATION, 1)
    if slab["intersection_matrix_rows"] != [2, 1]:
        raise AssertionError("genus-one calibration did not produce the standard symplectic form")
    box = _graph_result((4, 3, 3), BOX_4X3X3_GENUS_THREE_ROTATION, 3)
    return {
        "claim_status": "COMPUTATIONALLY_VERIFIED",
        "conventions": {
            "coefficients": "GF(2)",
            "cup_product": "Alexander-Whitney on vertex-sorted face-center triangles",
            "tree_cotree": "lexicographic BFS primal tree, edge-order Kruskal dual tree",
            "matrix_rows": "bit j of row i is pairing <e_i,e_j>",
            "symplectic_columns": "columns are (a1,b1,a2,b2,...) in pinned coordinates",
        },
        "genus_one_calibration": slab,
        "genus_three_box": box,
        "claim_boundary": (
            "This verifier recovers and cross-checks the labeled mod-two intersection form and "
            "an explicit symplectic transport. Quadratic refinements, Arf reconstruction, and "
            "the exhaustive physical TT-rank search are separate next-gate claims."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
