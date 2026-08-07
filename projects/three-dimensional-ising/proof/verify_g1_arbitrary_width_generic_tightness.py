#!/usr/bin/env python3
"""Exact regression for the one-sided arbitrary-width encoder candidate."""

from __future__ import annotations

from collections import Counter, deque
import argparse
import json
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from discovery.audit_g1_explicit_all_width_induction import (  # noqa: E402
    _base_tree,
    _embed,
    extension_pairs,
)
from discovery.audit_g1_explicit_common_basis import excluded_pairs  # noqa: E402
from proof.verify_lane_b_arbitrary_width_frontier import _rank  # noqa: E402
from proof.verify_lane_b_genus3 import (  # noqa: E402
    _cycle_basis,
    _edge_homology_labels,
    _rotation_faces,
)
from src.conventions import cubic_box  # noqa: E402
from src.lane_b_universal_embedding import universal_checkerboard_rotation  # noqa: E402


def _gauge_tree_indices(edges):
    return {
        index
        for index, edge in enumerate(edges)
        if (
            edge.u[0] != edge.v[0]
            or (edge.u[0] == edge.v[0] == 0 and edge.u[1] != edge.v[1])
            or (
                edge.u[0] == edge.v[0] == 0
                and edge.u[1] == edge.v[1] == 0
                and edge.u[2] != edge.v[2]
            )
        )
    }


def _edge_faces(edges, face_walks):
    edge_index = {(edge.u, edge.v): index for index, edge in enumerate(edges)}
    incident = [[] for _ in edges]
    for face, walk in enumerate(face_walks):
        for offset, left in enumerate(walk):
            right = walk[(offset + 1) % len(walk)]
            incident[edge_index[tuple(sorted((left, right)))]] .append(face)
    if any(len(pair) != 2 for pair in incident):
        raise AssertionError("each edge must have two incident face darts")
    return incident


def _components(vertex_count, edge_pairs, retained):
    adjacency = [[] for _ in range(vertex_count)]
    for index in retained:
        left, right = edge_pairs[index]
        adjacency[left].append(right)
        adjacency[right].append(left)
    unseen = set(range(vertex_count))
    result = []
    while unseen:
        start = unseen.pop()
        component = {start}
        stack = [start]
        while stack:
            vertex = stack.pop()
            for neighbour in adjacency[vertex]:
                if neighbour in unseen:
                    unseen.remove(neighbour)
                    component.add(neighbour)
                    stack.append(neighbour)
        result.append(frozenset(component))
    return result


def _vertex_components(vertices, edges, retained):
    index = {vertex: position for position, vertex in enumerate(vertices)}
    pairs = [(index[edge.u], index[edge.v]) for edge in edges]
    return _components(len(vertices), pairs, retained)


def _square_descriptor(walk):
    if len(walk) != 4:
        return None
    fixed = next(
        axis for axis in range(3) if len({vertex[axis] for vertex in walk}) == 1
    )
    lower = tuple(min(vertex[axis] for vertex in walk) for axis in range(3))
    return (fixed, *lower)


def _tree_paths(vertices, edges, tree, root):
    adjacency = {vertex: [] for vertex in vertices}
    for edge_index in tree:
        edge = edges[edge_index]
        adjacency[edge.u].append((edge.v, edge_index))
        adjacency[edge.v].append((edge.u, edge_index))
    paths = {root: 0}
    stack = [root]
    while stack:
        vertex = stack.pop()
        for neighbour, edge_index in adjacency[vertex]:
            if neighbour not in paths:
                paths[neighbour] = paths[vertex] ^ (1 << edge_index)
                stack.append(neighbour)
    if len(paths) != len(vertices):
        raise AssertionError("encoder is not connected")
    return paths


def _expected_primal_types(old_width):
    o = old_width
    if o % 2 == 0:
        changed = o - 2 + 1
        return Counter({
            ("new", 1): 3 * o // 2 + 1,
            ("new", 9): o // 2 - 1,
            ("new", 13): 1,
            ("old", 0): o * o - changed,
            ("old", 4): o - 2,
            ("old", 8): 1,
        })
    half = (o - 1) // 2
    old_four = (o - 3) // 2
    old_eight = (o - 5) // 2
    result = Counter({
        ("new", 1): 3 * half,
        ("new", 5): half,
        ("new", 9): 2,
        ("new", 17): 1,
        ("old", 0): o * o - old_four - old_eight,
        ("old", 4): old_four,
    })
    if old_eight:
        result[("old", 8)] = old_eight
    return result


def _primal_type_counter(width, vertices, edges, retained):
    old = width - 1
    terminals = {vertex for vertex in vertices if vertex[0] == 4}
    result = Counter()
    for component in _vertex_components(vertices, edges, retained):
        actual_vertices = [vertices[index] for index in component]
        anchors = [vertex for vertex in actual_vertices if vertex in terminals]
        if len(anchors) != 1:
            raise AssertionError("a retained-tree component does not have one terminal")
        anchor = anchors[0]
        new_count = sum(vertex[1] >= old or vertex[2] >= old for vertex in actual_vertices)
        kind = "new" if anchor[1] >= old or anchor[2] >= old else "old"
        result[(kind, new_count)] += 1
    return result


def _quotient_layers(width, face_walks, dual_components, edge_faces, retained):
    old_walks = _rotation_faces(
        *cubic_box((5, width - 1, width - 1)),
        universal_checkerboard_rotation(5, width - 1),
    )[1]
    old_squares = {
        _square_descriptor(walk) for walk in old_walks if len(walk) == 4
    }
    descriptors = [_square_descriptor(walk) for walk in face_walks]
    common = {index for index, value in enumerate(descriptors) if value in old_squares}
    changed = set(range(len(face_walks))) - common

    adjacency = [[] for _ in face_walks]
    for edge in retained:
        left, right = edge_faces[edge]
        adjacency[left].append(right)
        adjacency[right].append(left)

    def induced_parts(nodes):
        unseen = set(nodes)
        parts = []
        owner = {}
        while unseen:
            start = unseen.pop()
            part = {start}
            stack = [start]
            while stack:
                face = stack.pop()
                for neighbour in adjacency[face]:
                    if neighbour in unseen:
                        unseen.remove(neighbour)
                        part.add(neighbour)
                        stack.append(neighbour)
            position = len(parts)
            parts.append(part)
            for face in part:
                owner[face] = position
        return parts, owner

    old_parts, old_owner = induced_parts(common)
    new_parts, new_owner = induced_parts(changed)
    offset = len(old_parts)
    quotient = [set() for _ in range(offset + len(new_parts))]
    for face in common:
        for neighbour in adjacency[face]:
            if neighbour in changed:
                left = old_owner[face]
                right = offset + new_owner[neighbour]
                quotient[left].add(right)
                quotient[right].add(left)
    outer_face = next(index for index, walk in enumerate(face_walks) if len(walk) != 4)
    root = offset + new_owner[outer_face]
    distance = {root: 0}
    queue = deque([root])
    while queue:
        vertex = queue.popleft()
        for neighbour in quotient[vertex]:
            if neighbour not in distance:
                distance[neighbour] = distance[vertex] + 1
                queue.append(neighbour)
    edge_count = sum(map(len, quotient)) // 2
    if len(distance) != len(quotient) or edge_count != len(quotient) - 1:
        raise AssertionError("dual shell quotient is not a tree")
    return [Counter(distance.values())[layer] for layer in range(max(distance.values()) + 1)]


def _verify_width(width, tree, previous_square_descriptors):
    started = time.monotonic()
    vertices, edges = cubic_box((5, width, width))
    faces, face_walks = _rotation_faces(
        vertices, edges, universal_checkerboard_rotation(5, width)
    )
    genus = (2 - (len(vertices) - len(edges) + len(faces))) // 2
    gauge = _gauge_tree_indices(edges)
    if len(gauge) != len(vertices) - 1:
        raise AssertionError("closed-form gauge tree has the wrong size")
    edge_index = {(edge.u, edge.v): index for index, edge in enumerate(edges)}
    exceptional = {edge_index[pair] for pair in excluded_pairs(width)}
    if not exceptional <= tree - gauge:
        raise AssertionError("exceptional formula is not contained in the chord set")
    common = (tree - gauge) - exceptional
    target = width * width - 1
    if len(tree) != len(vertices) - 1 or len(common) != target:
        raise AssertionError("tree or common-basis cardinality failed")

    retained_forest = tree - common
    terminal_components = _vertex_components(vertices, edges, retained_forest)
    terminals = {index for index, vertex in enumerate(vertices) if vertex[0] == 4}
    if sorted(len(component & terminals) for component in terminal_components) != [1] * width**2:
        raise AssertionError("terminal component lemma failed")
    primal_types = None
    if width > 4:
        primal_types = _primal_type_counter(width, vertices, edges, retained_forest)
        if primal_types != _expected_primal_types(width - 1):
            raise AssertionError("primal shell type formula failed")

    edge_faces = _edge_faces(edges, face_walks)
    all_edges = set(range(len(edges)))
    dual_p = _components(len(faces), edge_faces, all_edges - gauge - common)
    if len(dual_p) != 1:
        raise AssertionError("P homology-basis dual complement disconnected")
    dual_x = _components(len(faces), edge_faces, all_edges - gauge - exceptional)
    dual_all = _components(len(faces), edge_faces, all_edges - gauge - common - exceptional)
    if set(dual_x) != set(dual_all):
        raise AssertionError("P and X homology spans are not separated")
    k = width // 2
    descriptor_index = {
        _square_descriptor(walk): index
        for index, walk in enumerate(face_walks)
        if len(walk) == 4
    }
    expected_small = [{descriptor_index[(0, 0, y, 2)] for y in range(3)}]
    if k >= 3:
        expected_small.append({descriptor_index[(0, 0, y, 0)] for y in range(5)})
        expected_small.extend(
            {descriptor_index[(0, 0, 2 * r - 1, 0)], descriptor_index[(0, 0, 2 * r, 0)]}
            for r in range(3, k)
        )
    actual_small = {component for component in dual_x if len(component) < len(faces) // 2}
    if actual_small != {frozenset(component) for component in expected_small}:
        raise AssertionError("exceptional dual-island formula failed")
    if len(dual_x) != k:
        raise AssertionError("exceptional dual component count failed")

    quotient_layers = None
    if width > 4:
        quotient_layers = _quotient_layers(
            width, face_walks, dual_p, edge_faces, all_edges - gauge - common
        )
        if width == 5:
            if sum(quotient_layers) != 22:
                raise AssertionError("width-five quotient size failed")
        elif width % 2:
            if quotient_layers != [1, 3 * width - 4, width - 1, width - 1, 1]:
                raise AssertionError("odd-width dual quotient layers failed")
        elif quotient_layers != [1, 3 * width - 6, width - 2, width - 2]:
            raise AssertionError("even-width dual quotient layers failed")

    cycles = _cycle_basis(vertices, edges)
    labels, face_rank = _edge_homology_labels(len(edges), faces, cycles, genus)
    if any(labels[edge] for edge in gauge):
        raise AssertionError("closed-form gauge tree is not the zero-label complement")
    rank_p = _rank([labels[edge] for edge in common])
    rank_x = _rank([labels[edge] for edge in exceptional])
    rank_all = _rank([labels[edge] for edge in common | exceptional])
    if rank_p != target or rank_all != rank_p + rank_x:
        raise AssertionError("independent raw-homology cross-check failed")

    root = (4, 0, 0)
    paths = _tree_paths(vertices, edges, tree, root)
    terminal_labels = []
    for y in range(width):
        for z in range(width):
            terminal = (4, y, z)
            if terminal == root:
                continue
            value = 0
            mask = paths[terminal]
            for edge, label in enumerate(labels):
                if (mask >> edge) & 1:
                    value ^= label
            terminal_labels.append(value)
    if _rank(terminal_labels) != target:
        raise AssertionError("terminal map raw-homology rank failed")

    return {
        "width": width,
        "genus": genus,
        "vertex_count": len(vertices),
        "face_count": len(faces),
        "face_boundary_rank": face_rank,
        "encoder_tree_edges": len(tree),
        "common_basis_edges": len(common),
        "exceptional_edges": len(exceptional),
        "terminal_components": len(terminal_components),
        "primal_shell_types": None if primal_types is None else {
            f"{kind}_{size}": count for (kind, size), count in sorted(primal_types.items())
        },
        "dual_p_components": len(dual_p),
        "dual_x_components": len(dual_x),
        "dual_all_components": len(dual_all),
        "dual_small_component_sizes": sorted(
            len(component) for component in dual_x if len(component) < len(faces) // 2
        ),
        "dual_quotient_layers": quotient_layers,
        "rank_h_P": rank_p,
        "rank_h_X": rank_x,
        "rank_h_P_union_X": rank_all,
        "terminal_homology_rank": _rank(terminal_labels),
        "wall_seconds": time.monotonic() - started,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "square_descriptors": sorted(
            descriptor for descriptor in map(_square_descriptor, face_walks) if descriptor is not None
        ),
    }


def verify(maximum_width=20):
    if maximum_width < 4:
        raise ValueError("maximum width must be at least four")
    width = 4
    tree = set(_base_tree())
    rows = []
    previous = None
    while True:
        row = _verify_width(width, tree, previous)
        previous = set(map(tuple, row.pop("square_descriptors")))
        rows.append(row)
        if width == maximum_width:
            break
        old = width
        width += 1
        tree = _embed(tree, old, width)
        _, edges = cubic_box((5, width, width))
        edge_index = {(edge.u, edge.v): index for index, edge in enumerate(edges)}
        tree |= {edge_index[pair] for pair in extension_pairs(old)}
    return {
        "claim_status": "CERTIFIED_NUMERICAL exact GF(2) one-sided regression",
        "checked_widths": [4, maximum_width],
        "rows": rows,
        "candidate_analysis": "proof/g1_arbitrary_width_generic_tightness.md",
        "claim_boundary": (
            "This regression certifies the normal one-sided prefix construction only.  Naive "
            "reflected gluing fails; the separate buffered-factor proof, not this replay alone, "
            "establishes arbitrary-width G1."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-width", type=int, default=20)
    args = parser.parse_args()
    print(json.dumps(verify(args.maximum_width), indent=2, sort_keys=True))
