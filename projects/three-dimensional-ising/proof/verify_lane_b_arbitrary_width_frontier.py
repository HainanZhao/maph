#!/usr/bin/env python3
"""Exact finite-width audit of the universal checkerboard frontier mechanism."""

from __future__ import annotations

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
from proof.verify_lane_b_intersection import (  # noqa: E402
    _gf2_inverse,
    _graph_result,
    _symplectic_basis,
    _transpose,
)
from src.conventions import cubic_box  # noqa: E402
from src.lane_b_recursive_family import cyclically_equal  # noqa: E402
from src.lane_b_universal_embedding import (  # noqa: E402
    interior_atomic_count,
    universal_checkerboard_rotation,
    universal_embedding_genus,
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


def _matrix_vector(rows: list[int], vector: int) -> int:
    return sum(((row & vector).bit_count() & 1) << index for index, row in enumerate(rows))


def _matrix_multiply(left: list[int], right: list[int]) -> list[int]:
    product = []
    for row in left:
        value = 0
        for index in range(len(right)):
            if (row >> index) & 1:
                value ^= right[index]
        product.append(value)
    return product


def _quadratic_standard(vector: int, genus: int) -> int:
    return sum(
        ((vector >> (2 * handle)) & 1) * ((vector >> (2 * handle + 1)) & 1)
        for handle in range(genus)
    ) & 1


def _rows_from_columns(columns: list[int], row_count: int) -> list[int]:
    return [
        sum(((columns[column] >> row) & 1) << column for column in range(len(columns)))
        for row in range(row_count)
    ]


def _bilinear(intersection: list[int], left: int, right: int) -> int:
    return sum(
        ((left >> index) & 1) * ((intersection[index] & right).bit_count() & 1)
        for index in range(len(intersection))
    ) & 1


def _nullspace(rows: list[int], dimension: int) -> list[int]:
    echelon = [row for row in rows if row]
    pivots: list[int] = []
    rank = 0
    for column in range(dimension):
        pivot = next(
            (row for row in range(rank, len(echelon)) if (echelon[row] >> column) & 1),
            None,
        )
        if pivot is None:
            continue
        echelon[rank], echelon[pivot] = echelon[pivot], echelon[rank]
        for row in range(len(echelon)):
            if row != rank and ((echelon[row] >> column) & 1):
                echelon[row] ^= echelon[rank]
        pivots.append(column)
        rank += 1
    free = [column for column in range(dimension) if column not in pivots]
    result = []
    for free_column in free:
        vector = 1 << free_column
        for row, pivot in enumerate(pivots):
            if (echelon[row] >> free_column) & 1:
                vector |= 1 << pivot
        result.append(vector)
    return result


def _symplectic_vectors(vectors: list[int], intersection: list[int]) -> list[int]:
    remaining = vectors[:]
    result: list[int] = []
    while remaining:
        first = remaining.pop(0)
        partner = next(
            (index for index, value in enumerate(remaining) if _bilinear(intersection, first, value)),
            None,
        )
        if partner is None:
            raise AssertionError("orthogonal complement is degenerate")
        second = remaining.pop(partner)
        adjusted = []
        for vector in remaining:
            if _bilinear(intersection, vector, second):
                vector ^= first
            if _bilinear(intersection, vector, first):
                vector ^= second
            adjusted.append(vector)
        result.extend((first, second))
        remaining = adjusted
    return result


def _embedded_mask(mask: int, old_edges, new_edges) -> int:
    index = {(edge.u, edge.v): position for position, edge in enumerate(new_edges)}
    return sum(
        1 << index[(edge.u, edge.v)]
        for position, edge in enumerate(old_edges)
        if (mask >> position) & 1
    )


def _transverse_plaquette_cycle(edges, layer: int, y: int, z: int) -> int:
    edge_index = {(edge.u, edge.v): index for index, edge in enumerate(edges)}
    vertices = (
        (layer, y, z),
        (layer, y + 1, z),
        (layer, y + 1, z + 1),
        (layer, y, z + 1),
    )
    result = 0
    for index in range(4):
        pair = tuple(sorted((vertices[index], vertices[(index + 1) % 4])))
        result |= 1 << edge_index[pair]
    return result


def _label(mask: int, labels: list[int]) -> int:
    result = 0
    for index, value in enumerate(labels):
        if (mask >> index) & 1:
            result ^= value
    return result


def _mode_potential(width: int, transverse_edges, mode: int) -> int | None:
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(width * width)]
    for index, edge in enumerate(transverse_edges):
        left = width * edge.u[1] + edge.u[2]
        right = width * edge.v[1] + edge.v[2]
        value = (mode >> index) & 1
        adjacency[left].append((right, value))
        adjacency[right].append((left, value))
    values: list[int | None] = [None] * (width * width)
    values[0] = 0
    stack = [0]
    while stack:
        left = stack.pop()
        for right, edge_value in adjacency[left]:
            proposed = values[left] ^ edge_value  # type: ignore[operator]
            if values[right] is None:
                values[right] = proposed
                stack.append(right)
            elif values[right] != proposed:
                return None
    if any(value is None for value in values):
        raise AssertionError("transverse slice became disconnected")
    return sum(int(values[index]) << (index - 1) for index in range(1, width * width))


def _graph_mode_potential(vertices, edges, mode: int) -> int | None:
    """Solve eta=delta s on an arbitrary connected pinned subgraph."""
    vertex_index = {vertex: index for index, vertex in enumerate(vertices)}
    adjacency: list[list[tuple[int, int]]] = [[] for _ in vertices]
    for index, edge in enumerate(edges):
        left = vertex_index[edge.u]
        right = vertex_index[edge.v]
        value = (mode >> index) & 1
        adjacency[left].append((right, value))
        adjacency[right].append((left, value))
    values: list[int | None] = [None] * len(vertices)
    values[0] = 0
    stack = [0]
    while stack:
        left = stack.pop()
        for right, edge_value in adjacency[left]:
            proposed = values[left] ^ edge_value  # type: ignore[operator]
            if values[right] is None:
                values[right] = proposed
                stack.append(right)
            elif values[right] != proposed:
                return None
    if any(value is None for value in values):
        raise AssertionError("prefix subgraph became disconnected")
    return sum(int(values[index]) << (index - 1) for index in range(1, len(vertices)))


def _coordinate_map_atomic(atom_vectors: list[int], genus: int) -> list[int]:
    columns = atom_vectors
    column_matrix = _rows_from_columns(columns, genus)
    a_map = _gf2_inverse(column_matrix, genus)
    b_map = _transpose(_gf2_inverse(a_map, genus), genus)
    rows: list[int] = []
    for output in range(2 * genus):
        source_row = a_map[output // 2] if output % 2 == 0 else b_map[output // 2]
        rows.append(sum(((source_row >> index) & 1) << (2 * index + output % 2) for index in range(genus)))
    return rows


def _slice_curl_rows(width: int, transverse_edges, labels: list[int], coordinate_bits: list[int]) -> list[int]:
    edge_index = {(edge.u, edge.v): index for index, edge in enumerate(transverse_edges)}
    rows = []
    for y in range(width - 1):
        for z in range(width - 1):
            vertices = ((0, y, z), (0, y + 1, z), (0, y + 1, z + 1), (0, y, z + 1))
            boundary = []
            for index in range(4):
                pair = tuple(sorted((vertices[index], vertices[(index + 1) % 4])))
                boundary.append(edge_index[pair])
            row = 0
            for output, bit in enumerate(coordinate_bits):
                value = 0
                for edge_position in boundary:
                    value ^= (labels[edge_position] >> bit) & 1
                row |= value << output
            rows.append(row)
    return rows


def _case(width: int, maximum_length: int = 6) -> dict[str, object]:
    prior = None
    transport: list[int] | None = None
    rows = []
    for length in range(2, maximum_length + 1):
        rotation = universal_checkerboard_rotation(length, width)
        vertices, edges = cubic_box((length, width, width))
        faces, _ = _rotation_faces(vertices, edges, rotation)
        genus = (2 - (len(vertices) - len(edges) + len(faces))) // 2
        if genus != universal_embedding_genus(length, width):
            raise AssertionError("universal genus formula failed")
        topology = _graph_result((length, width, width), rotation, genus) if genus else None
        raw_labels, _ = _edge_homology_labels(
            len(edges), faces, _cycle_basis(vertices, edges), genus
        ) if genus else ([0] * len(edges), len(faces) - 1)
        dimension = 2 * genus
        if prior is None:
            transport = _symplectic_basis(topology["intersection_matrix_rows"]) if genus else []
        else:
            old_length, old_genus, old_transport, old_topology, old_edges = prior
            old_dimension = 2 * old_genus
            images = [
                _label(_embedded_mask(mask, old_edges, edges), raw_labels)
                for mask in old_topology["pinned_homology_representatives"]
            ] if old_topology else []
            inclusion = _rows_from_columns(images, dimension)
            old_columns = [
                _matrix_vector(inclusion, vector)
                for vector in _transpose(old_transport, old_dimension)
            ]
            canonical_old = [1 << (index ^ 1) for index in range(old_dimension)]
            restricted = [
                sum(
                    _bilinear(topology["intersection_matrix_rows"], left, right) << column
                    for column, right in enumerate(old_columns)
                )
                for left in old_columns
            ]
            if restricted != canonical_old:
                raise AssertionError("nested inclusion did not preserve the symplectic form")
            functionals = []
            for vector in old_columns:
                functional = 0
                for index in range(dimension):
                    if (vector >> index) & 1:
                        functional ^= topology["intersection_matrix_rows"][index]
                functionals.append(functional)
            if dimension:
                complement = _nullspace(functionals, dimension)
                new_columns = _symplectic_vectors(complement, topology["intersection_matrix_rows"])
                transport = _rows_from_columns(old_columns + new_columns, dimension)
            else:
                transport = []
        if genus:
            inverse = _gf2_inverse(transport, dimension)  # type: ignore[arg-type]
            canonical_labels = [_matrix_vector(inverse, label) for label in raw_labels]
        else:
            canonical_labels = raw_labels


        explicit_lagrangian_cycles = []
        explicit_window_rows = []
        for window in range(length - 1):
            parity = 1 if window % 2 == 0 else 0
            window_cycles = [
                _transverse_plaquette_cycle(edges, window, y, z)
                for y in range(parity, width - 1, 2)
                for z in range(parity, width - 1, 2)
            ]
            window_labels = [_label(cycle, raw_labels) for cycle in window_cycles]
            window_rank = _rank(window_labels)
            expected = (
                ((width - 1) // 2) ** 2
                if width % 2
                else ((width // 2 - 1) ** 2 if parity else (width // 2) ** 2 - 1)
            )
            if window_rank != expected:
                raise AssertionError(
                    f"explicit checkerboard window rank formula failed: "
                    f"w={width}, n={length}, window={window}, rank={window_rank}, expected={expected}"
                )
            explicit_lagrangian_cycles.extend(window_labels)
            explicit_window_rows.append({
                "layers": [window, window + 1],
                "checkerboard_parity": parity,
                "cycle_count": len(window_cycles),
                "rank": window_rank,
                "expected_rank": expected,
            })
        if _rank(explicit_lagrangian_cycles) != genus:
            raise AssertionError("explicit window cycles do not span a genus-dimensional space")
        if genus and any(
            _bilinear(topology["intersection_matrix_rows"], left, right)
            for left in explicit_lagrangian_cycles
            for right in explicit_lagrangian_cycles
        ):
            raise AssertionError("explicit window-cycle space is not isotropic")

        atom_vectors: list[int] = []
        atom_seen: set[int] = set()
        layer_pre_audits = []
        for layer in range(length):
            transverse = [
                (edge, label)
                for edge, label in zip(edges, canonical_labels)
                if edge.u[0] == edge.v[0] == layer
            ]
            nonexact_bits = []
            for bit in range(dimension):
                mode = sum(
                    1 << index for index, (_, label) in enumerate(transverse) if (label >> bit) & 1
                )
                if mode and _mode_potential(width, [edge for edge, _ in transverse], mode) is None:
                    nonexact_bits.append(bit)
                    if bit % 2:
                        raise AssertionError("a nonexact b mode survived")
            for _, label in transverse:
                atom = sum(1 << (bit // 2) for bit in nonexact_bits if (label >> bit) & 1)
                if atom and atom not in atom_seen:
                    atom_seen.add(atom)
                    atom_vectors.append(atom)
            layer_pre_audits.append({"layer": layer, "nonexact_bits": nonexact_bits})
        if len(atom_vectors) != genus or _rank(atom_vectors) != genus:
            raise AssertionError("nonexact transverse atoms are not a homology basis")

        atomic_map = _coordinate_map_atomic(atom_vectors, genus) if genus else []
        atomic_labels = [_matrix_vector(atomic_map, label) for label in canonical_labels] if genus else canonical_labels
        raw_to_atomic = _matrix_multiply(atomic_map, inverse) if genus else []
        canonical = [1 << (index ^ 1) for index in range(dimension)]
        if genus:
            transformed_intersection = _matrix_multiply(
                _matrix_multiply(atomic_map, canonical),
                _transpose(atomic_map, dimension),
            )
            if transformed_intersection != canonical:
                raise AssertionError("atomic coordinate map is not symplectic")
            atomic_inverse = _gf2_inverse(atomic_map, dimension)
            affine_correction = [
                _quadratic_standard(_matrix_vector(atomic_inverse, 1 << bit), genus)
                for bit in range(dimension)
            ]
            for left in range(dimension):
                left_vector = 1 << left
                transported_left = _quadratic_standard(
                    _matrix_vector(atomic_inverse, left_vector), genus
                )
                if transported_left != affine_correction[left]:
                    raise AssertionError("quadratic affine correction failed on a generator")
                for right in range(dimension):
                    right_vector = 1 << right
                    transported_sum = _quadratic_standard(
                        _matrix_vector(atomic_inverse, left_vector ^ right_vector), genus
                    )
                    polarization = transported_left ^ _quadratic_standard(
                        _matrix_vector(atomic_inverse, right_vector), genus
                    ) ^ ((canonical[left] >> right) & 1)
                    if transported_sum != polarization:
                        raise AssertionError("quadratic polarization failed after atomic transport")
            arf = sum(
                affine_correction[2 * handle] * affine_correction[2 * handle + 1]
                for handle in range(genus)
            ) & 1
            if arf:
                raise AssertionError("Arf invariant changed under the atomic symplectic map")
            raw_quadratic_affine_correction = [
                _quadratic_standard(_matrix_vector(raw_to_atomic, 1 << bit), genus)
                for bit in range(dimension)
            ]
            raw_congruence = _matrix_multiply(
                _transpose(raw_to_atomic, dimension),
                _matrix_multiply(canonical, raw_to_atomic),
            )
            if raw_congruence != topology["intersection_matrix_rows"]:
                raise AssertionError("raw-to-atomic symplectic congruence failed")
            for left in range(dimension):
                for right in range(dimension):
                    left_raw = 1 << left
                    right_raw = 1 << right
                    transported_sum = _quadratic_standard(
                        _matrix_vector(raw_to_atomic, left_raw ^ right_raw), genus
                    )
                    expected = (
                        raw_quadratic_affine_correction[left]
                        ^ raw_quadratic_affine_correction[right]
                        ^ ((topology["intersection_matrix_rows"][left] >> right) & 1)
                    )
                    if transported_sum != expected:
                        raise AssertionError("raw-to-atomic quadratic polarization failed")
            raw_transported_arf = 0
        else:
            affine_correction = []
            arf = 0
            raw_quadratic_affine_correction = []
            raw_transported_arf = 0
        layer_audits = []
        all_b_exact = True
        singleton_nonexact = True
        for layer in range(length):
            transverse = [
                (edge, label)
                for edge, label in zip(edges, atomic_labels)
                if edge.u[0] == edge.v[0] == layer
            ]
            potentials: dict[str, int] = {}
            nonexact_bits = []
            for bit in range(dimension):
                mode = sum(
                    1 << index for index, (_, label) in enumerate(transverse) if (label >> bit) & 1
                )
                if not mode:
                    continue
                potential = _mode_potential(width, [edge for edge, _ in transverse], mode)
                if potential is None:
                    nonexact_bits.append(bit)
                    if bit % 2:
                        all_b_exact = False
                else:
                    potentials[str(bit)] = potential
            for _, label in transverse:
                active = [bit for bit in nonexact_bits if (label >> bit) & 1]
                if len(active) > 1:
                    singleton_nonexact = False
            layer_audits.append({
                "layer": layer,
                "nonexact_bits": nonexact_bits,
                "exact_mode_potentials": potentials,
            })
        if not all_b_exact or not singleton_nonexact:
            raise AssertionError("atomic gauge normalization failed")
        slice_a_curl_rows = []
        for layer in range(length):
            transverse = [
                (edge, label)
                for edge, label in zip(edges, atomic_labels)
                if edge.u[0] == edge.v[0] == layer
            ]
            relabeled_edges = [
                type(edge)((0, edge.u[1], edge.u[2]), (0, edge.v[1], edge.v[2]))
                for edge, _ in transverse
            ]
            slice_a_curl_rows.append(
                _slice_curl_rows(
                    width,
                    relabeled_edges,
                    [label for _, label in transverse],
                    list(range(0, dimension, 2)),
                )
            )
        adjacent_window_spaces = []
        for start in range(max(1, length - 1)):
            retained = {start, min(start + 1, length - 1)}
            outside_rows = [
                row
                for layer, curl_rows in enumerate(slice_a_curl_rows)
                if layer not in retained
                for row in curl_rows
            ]
            basis = _nullspace(outside_rows, genus)
            adjacent_window_spaces.append({
                "layers": sorted(retained),
                "dimension": len(basis),
                "basis": basis,
            })
        adjacent_window_span_rank = _rank([
            vector for window in adjacent_window_spaces for vector in window["basis"]
        ])
        a_curl_support = {
            str(handle): [
                [layer, plaquette]
                for layer, curl_rows in enumerate(slice_a_curl_rows)
                for plaquette, row in enumerate(curl_rows)
                if (row >> handle) & 1
            ]
            for handle in range(genus)
        }
        prefix_audits = []
        for cut in range(length):
            prefix_vertices = tuple(vertex for vertex in vertices if vertex[0] <= cut)
            prefix_edges_with_labels = [
                (edge, label)
                for edge, label in zip(edges, atomic_labels)
                if edge.u[0] <= cut and edge.v[0] <= cut
            ]
            prefix_edges = [edge for edge, _ in prefix_edges_with_labels]
            exact_bits = []
            nonexact_bits = []
            for bit in range(dimension):
                mode = sum(
                    1 << index
                    for index, (_, label) in enumerate(prefix_edges_with_labels)
                    if (label >> bit) & 1
                )
                potential = _graph_mode_potential(prefix_vertices, prefix_edges, mode)
                (exact_bits if potential is not None else nonexact_bits).append(bit)
            prefix_audits.append({
                "cut_after_layer": cut,
                "exact_bits": exact_bits,
                "nonexact_bits": nonexact_bits,
                "all_b_modes_exact": all(bit % 2 == 0 for bit in nonexact_bits),
            })
        suffix_audits = []
        for cut in range(length):
            suffix_vertices = tuple(vertex for vertex in vertices if vertex[0] >= cut)
            suffix_edges_with_labels = [
                (edge, label)
                for edge, label in zip(edges, atomic_labels)
                if edge.u[0] >= cut and edge.v[0] >= cut
            ]
            suffix_edges = [edge for edge, _ in suffix_edges_with_labels]
            exact_bits = []
            nonexact_bits = []
            for bit in range(dimension):
                mode = sum(
                    1 << index
                    for index, (_, label) in enumerate(suffix_edges_with_labels)
                    if (label >> bit) & 1
                )
                potential = _graph_mode_potential(suffix_vertices, suffix_edges, mode)
                (exact_bits if potential is not None else nonexact_bits).append(bit)
            suffix_audits.append({
                "cut_before_layer": cut,
                "exact_bits": exact_bits,
                "nonexact_bits": nonexact_bits,
            })
        pair_cut_spatial_witnesses = []
        for handle_cut in range(genus + 1):
            left_bits = set(range(2 * handle_cut))
            right_bits = set(range(2 * handle_cut, dimension))
            witnesses = []
            for spatial_cut in range(length - 1):
                prefix_exact = set(prefix_audits[spatial_cut]["exact_bits"])
                suffix_exact = set(suffix_audits[spatial_cut + 1]["exact_bits"])
                if right_bits <= prefix_exact and left_bits <= suffix_exact:
                    witnesses.append(spatial_cut)
            pair_cut_spatial_witnesses.append({
                "after_handle": handle_cut,
                "layer_cuts": witnesses,
            })
        rows.append({
            "length": length,
            "genus": genus,
            "homology_bits": dimension,
            "canonical_intersection": canonical,
            "atomic_intersection": canonical,
            "raw_intersection": topology["intersection_matrix_rows"] if genus else [],
            "raw_to_atomic_rows": raw_to_atomic,
            "raw_quadratic_affine_correction": raw_quadratic_affine_correction,
            "raw_transported_arf": raw_transported_arf,
            "quadratic_affine_correction": affine_correction,
            "quadratic_polarization_checked_on_generators_and_pairs": True,
            "arf_invariant": arf,
            "nested_symplectic": True,
            "explicit_checkerboard_lagrangian_windows": explicit_window_rows,
            "explicit_checkerboard_lagrangian_rank": _rank(explicit_lagrangian_cycles),
            "explicit_checkerboard_lagrangian_isotropic": True,
            "pre_atomic_layers": layer_pre_audits,
            "atom_count": len(atom_vectors),
            "atom_rank": _rank(atom_vectors),
            "atomic_layers": layer_audits,
            "adjacent_window_spaces": adjacent_window_spaces,
            "adjacent_window_span_rank": adjacent_window_span_rank,
            "a_curl_support": a_curl_support,
            "prefix_exactness": prefix_audits,
            "suffix_exactness": suffix_audits,
            "pair_cut_spatial_witnesses": pair_cut_spatial_witnesses,
            "atomic_coordinate_edge_support": {
                str(bit): [
                    [list(edge.u), list(edge.v)]
                    for edge, label in zip(edges, atomic_labels)
                    if (label >> bit) & 1
                ]
                for bit in range(dimension)
            },
            "all_b_modes_exact": all_b_exact,
            "each_edge_has_at_most_one_nonexact_atom": singleton_nonexact,
        })
        prior = (length, genus, transport, topology, edges)
    return {
        "width": width,
        "physical_carrier_dimension": 1 << (width * width - 1),
        "interior_atomic_count_formula": interior_atomic_count(width),
        "length_rows": rows,
    }


def verify() -> dict[str, object]:
    nesting = []
    for width in range(2, 7):
        for length in range(2, 7):
            old = universal_checkerboard_rotation(length, width)
            new = universal_checkerboard_rotation(length + 1, width)
            for vertex, cyclic in old.items():
                restricted = tuple(neighbour for neighbour in new[vertex] if neighbour[0] < length)
                if not cyclically_equal(cyclic, restricted):
                    raise AssertionError("longitudinal deletion compatibility failed")
        nesting.append({"width": width, "lengths": [2, 3, 4, 5, 6, 7], "nested": True})
    cases = [_case(width) for width in range(2, 7)]
    return {
        "claim_status": "COMPUTATIONALLY VERIFIED exact GF(2) structural audit",
        "embedding": (
            "Restrict the checkerboard-boundary rotation of the next-even box to the requested "
            "n x w x w vertices; cap the ribbon-graph boundary faces."
        ),
        "nesting": nesting,
        "cases": cases,
        "observed_general_pattern": (
            "For w=2..6 and n=2..6, filtration-adapted symplectic normalization leaves only "
            "a-modes nonexact. Their distinct transverse edge atoms form a basis of size genus. "
            "After the induced symplectic GL change, every b-mode is a coboundary and every edge "
            "contains at most one nonexact atom."
        ),
        "claim_boundary": (
            "The embedding and its deletion compatibility are exact constructions. The atom-basis "
            "pattern is only a finite exact audit at w<=6,n<=6 until a general cell-parity proof "
            "and explicit all-q factor cores are supplied. No arbitrary-width theorem is claimed."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
