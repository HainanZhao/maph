#!/usr/bin/env python3
"""Exact replay of the buffered one-sided-encoder G1 construction.

The arbitrary-width statements are proved from the displayed parity formulas
in the companion proof.  This replay independently checks their finite bases,
shell relations, and their placement in one global canonical coordinate
system.  It never constructs a ``2^(w^2-1)`` flattening.
"""

from __future__ import annotations

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
    extension_pairs as normal_extension_pairs,
)
from discovery.audit_g1_opposite_explicit_all_width import (  # noqa: E402
    audit as opposite_audit,
    base_tree_pairs as opposite_base_tree_pairs,
    exceptional_pairs as opposite_exceptional_pairs,
    extension_pairs as opposite_extension_pairs,
    opposite_checkerboard_rotation,
)
from discovery.search_g1_paired_fundamental_cycles import _labels  # noqa: E402
from proof.verify_g1_arbitrary_width_generic_tightness import verify as normal_verify  # noqa: E402
from proof.verify_lane_b_arbitrary_width_frontier import _case, _rank  # noqa: E402
from proof.verify_lane_b_genus3 import (  # noqa: E402
    _cycle_basis,
    _edge_homology_labels,
    _rotation_faces,
)
from src.conventions import cubic_box  # noqa: E402
from src.lane_b_universal_embedding import universal_embedding_genus  # noqa: E402


def _normal_tree_pairs(width):
    tree = set(_base_tree())
    old = 4
    while old < width:
        tree = _embed(tree, old, old + 1)
        _, edges = cubic_box((5, old + 1, old + 1))
        edge_index = {(edge.u, edge.v): index for index, edge in enumerate(edges)}
        tree |= {edge_index[pair] for pair in normal_extension_pairs(old)}
        old += 1
    _, edges = cubic_box((5, width, width))
    return {(edges[index].u, edges[index].v) for index in tree}


def _opposite_tree_pairs(width):
    tree = opposite_base_tree_pairs()
    for old in range(4, width):
        tree |= opposite_extension_pairs(old)
    return tree


def _gauge_pairs(width):
    _, edges = cubic_box((5, width, width))
    return {
        (edge.u, edge.v)
        for edge in edges
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


def _solve(columns, target):
    pivots = {}
    for coordinate, vector in enumerate(columns):
        coefficient = 1 << coordinate
        while vector:
            pivot = vector.bit_length() - 1
            if pivot in pivots:
                old_vector, old_coefficient = pivots[pivot]
                vector ^= old_vector
                coefficient ^= old_coefficient
            else:
                pivots[pivot] = (vector, coefficient)
                break
    result = 0
    while target:
        pivot = target.bit_length() - 1
        if pivot not in pivots:
            raise AssertionError("target is outside the declared column span")
        vector, coefficient = pivots[pivot]
        target ^= vector
        result ^= coefficient
    return result


def _tree_terminal_columns(vertices, edges, tree, width):
    adjacency = {vertex: [] for vertex in vertices}
    for index in tree:
        edge = edges[index]
        adjacency[edge.u].append((edge.v, index))
        adjacency[edge.v].append((edge.u, index))
    root = (4, 0, 0)
    parent = {root: (None, None)}
    order = [root]
    for vertex in order:
        for neighbour, index in adjacency[vertex]:
            if neighbour not in parent:
                parent[neighbour] = (vertex, index)
                order.append(neighbour)
    if len(parent) != len(vertices):
        raise AssertionError("encoder tree is disconnected")
    subtree = {
        vertex: (
            1 << (vertex[1] * width + vertex[2] - 1)
            if vertex[0] == 4 and vertex != root
            else 0
        )
        for vertex in vertices
    }
    result = {}
    for vertex in reversed(order[1:]):
        previous, index = parent[vertex]
        result[index] = subtree[vertex]
        subtree[previous] ^= subtree[vertex]
    return result


def _exceptional_relation(width):
    vertices, edges = cubic_box((5, width, width))
    edge_index = {(edge.u, edge.v): index for index, edge in enumerate(edges)}
    tree = {edge_index[pair] for pair in _opposite_tree_pairs(width)}
    gauge = {edge_index[pair] for pair in _gauge_pairs(width)}
    exceptional = {edge_index[pair] for pair in opposite_exceptional_pairs(width)}
    if len(exceptional) != 1:
        raise AssertionError("even-width exceptional set is not a singleton")
    exceptional_edge = next(iter(exceptional))
    common = sorted((tree - gauge) - exceptional)
    faces, _ = _rotation_faces(
        vertices, edges, opposite_checkerboard_rotation(width)
    )
    genus = (2 - (len(vertices) - len(edges) + len(faces))) // 2
    labels, _ = _edge_homology_labels(
        len(edges), faces, _cycle_basis(vertices, edges), genus
    )
    terminal = _tree_terminal_columns(vertices, edges, tree, width)
    homology_relation = _solve([labels[index] for index in common], labels[exceptional_edge])
    terminal_relation = _solve([terminal[index] for index in common], terminal[exceptional_edge])
    homology_support = {
        (edges[common[index]].u, edges[common[index]].v)
        for index in range(len(common)) if (homology_relation >> index) & 1
    }
    terminal_support = {
        (edges[common[index]].u, edges[common[index]].v)
        for index in range(len(common)) if (terminal_relation >> index) & 1
    }
    if homology_support & terminal_support:
        raise AssertionError("exceptional rank-one update has nonzero scalar")
    if width >= 6:
        expected_homology = {
            ((4, 2 * row, 1), (4, 2 * row + 1, 1))
            for row in range(width // 2)
        }
        expected_terminal = {((1, width - 1, 1), (1, width - 1, 2))}
        if homology_support != expected_homology or terminal_support != expected_terminal:
            raise AssertionError("even-width exceptional formulas changed")
    return {
        "width": width,
        "homology_relation_support": [list(map(list, pair)) for pair in sorted(homology_support)],
        "terminal_relation_support": [list(map(list, pair)) for pair in sorted(terminal_support)],
        "rank_one_scalar": 0,
    }


def _projected_terminal_rank(width, tree_pairs, labels, edges, side):
    handle_cut = universal_embedding_genus(5, width)
    if side == "left":
        convert = lambda vertex: vertex
        project = lambda value: value & ((1 << (2 * handle_cut)) - 1)
        root = (4, 0, 0)
    else:
        convert = lambda vertex: (10 - vertex[0], vertex[1], vertex[2])
        project = lambda value: value >> (2 * handle_cut)
        root = (6, 0, 0)
    edge_index = {(edge.u, edge.v): index for index, edge in enumerate(edges)}
    tree = {
        edge_index[tuple(sorted((convert(left), convert(right))))]
        for left, right in tree_pairs
    }
    adjacency = {}
    for index in tree:
        edge = edges[index]
        adjacency.setdefault(edge.u, []).append((edge.v, index))
        adjacency.setdefault(edge.v, []).append((edge.u, index))
    values = {root: 0}
    stack = [root]
    while stack:
        vertex = stack.pop()
        for neighbour, index in adjacency.get(vertex, []):
            if neighbour not in values:
                values[neighbour] = values[vertex] ^ project(labels[index])
                stack.append(neighbour)
    terminals = [
        values[(root[0], y, z)]
        for y in range(width) for z in range(width)
        if (y, z) != (0, 0)
    ]
    return _rank(terminals)


def verify(maximum_symbolic_width=20, maximum_global_width=6):
    started = time.monotonic()
    normal = normal_verify(min(maximum_symbolic_width, 12))
    opposite = opposite_audit(maximum_symbolic_width)
    for row in opposite["rows"]:
        width = row["width"]
        target = width * width - 1
        if not (
            row["tree_connected"]
            and row["tree_edge_count"] == row["target_tree_edge_count"]
            and row["common_basis_count"] == target
            and row["terminal_rank"] == target
            and row["each_component_has_one_terminal"]
            and row["dual_complement_connected"]
        ):
            raise AssertionError("opposite-phase encoder regression")

    exceptional = [_exceptional_relation(width) for width in range(4, maximum_symbolic_width + 1, 2)]
    global_rows = []
    for width in range(4, maximum_global_width + 1):
        vertices, edges = cubic_box((11, width, width))
        structural = _case(width, 11)["length_rows"][-1]
        labels = _labels(structural, edges)
        left_rank = _projected_terminal_rank(
            width, _normal_tree_pairs(width), labels, edges, "left"
        )
        right_rank = _projected_terminal_rank(
            width, _opposite_tree_pairs(width), labels, edges, "right"
        )
        target = width * width - 1
        if left_rank != target or right_rank != target:
            raise AssertionError("global buffered encoder placement lost rank")
        suffix_genus = universal_embedding_genus(11, width) - universal_embedding_genus(7, width)
        if suffix_genus != universal_embedding_genus(5, width):
            raise AssertionError("suffix handle-block genus is not the local five-layer genus")
        global_rows.append({
            "shape": [11, width, width],
            "handle_cut": universal_embedding_genus(5, width),
            "left_terminal_rank": left_rank,
            "right_terminal_rank": right_rank,
            "target": target,
            "suffix_handle_genus": suffix_genus,
            "two_slab_buffer": {
                "state_count": 1 << target,
                "specialization": "all transverse weights zero; both longitudinal rails retained",
                "matrix_form": "nonzero monomial diagonal indexed by even masks",
            },
        })
    return {
        "claim_status": "CERTIFIED_NUMERICAL exact GF(2) replay supporting a symbolic proof",
        "theorem": "generic nonuniform G1 for every w>=3, with n_0(w)<=11",
        "normal_encoder": normal,
        "opposite_encoder": opposite,
        "exceptional_rank_one_relations": exceptional,
        "global_coordinate_rows": global_rows,
        "proof": "proof/g1_arbitrary_width_generic_tightness.md",
        "claim_boundary": (
            "The arbitrary-width conclusion comes from the parity-shell proof and buffered "
            "rank factorization, not from extrapolating these finite replay widths.  No "
            "homogeneous anisotropic or isotropic tightness is claimed."
        ),
        "wall_seconds": time.monotonic() - started,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-symbolic-width", type=int, default=20)
    parser.add_argument("--maximum-global-width", type=int, default=6)
    args = parser.parse_args()
    print(json.dumps(verify(**vars(args)), indent=2, sort_keys=True))
