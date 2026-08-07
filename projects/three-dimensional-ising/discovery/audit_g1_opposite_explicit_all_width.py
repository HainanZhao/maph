#!/usr/bin/env python3
"""Audit an explicit all-width encoder for the opposite checkerboard phase.

The edge formula was extracted from exact represented-matroid intersection.
Finite checks here are discovery evidence for the two parity-shell lemmas;
they are not, by themselves, an arbitrary-width proof.
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

from discovery.audit_g1_explicit_all_width_induction import _base_tree  # noqa: E402
from discovery.audit_g1_explicit_common_basis import (  # noqa: E402
    _component_terminal_counts,
    _dual_reach,
    _edge_faces,
)
from discovery.audit_g1_gauge_tree_dual import _gauge_tree  # noqa: E402
from discovery.search_g1_opposite_width_induction import (  # noqa: E402
    opposite_checkerboard_rotation,
)
from proof.verify_lane_b_arbitrary_width_frontier import _rank  # noqa: E402
from proof.verify_lane_b_genus3 import (  # noqa: E402
    _cycle_basis,
    _edge_homology_labels,
    _rotation_faces,
)
from src.conventions import cubic_box  # noqa: E402


def edge_pair(axis, x, y, z):
    left = (x, y, z)
    right = list(left)
    right[axis] += 1
    return tuple(sorted((left, tuple(right))))


def base_tree_pairs():
    _, edges = cubic_box((5, 4, 4))
    result = {(edges[index].u, edges[index].v) for index in _base_tree()}
    remove = {
        ((0, 1, 0), (1, 1, 0)), ((0, 1, 3), (1, 1, 3)),
        ((0, 2, 1), (0, 2, 2)), ((1, 0, 1), (1, 1, 1)),
        ((1, 1, 0), (1, 1, 1)), ((1, 1, 2), (1, 1, 3)),
        ((1, 2, 2), (1, 3, 2)), ((2, 0, 1), (2, 0, 2)),
        ((2, 1, 0), (2, 2, 0)), ((2, 1, 3), (2, 2, 3)),
        ((3, 2, 1), (4, 2, 1)), ((4, 1, 0), (4, 1, 1)),
        ((4, 1, 2), (4, 1, 3)),
    }
    add = {
        ((0, 0, 1), (0, 1, 1)), ((0, 1, 0), (0, 1, 1)),
        ((0, 1, 2), (0, 1, 3)), ((1, 0, 1), (1, 0, 2)),
        ((1, 1, 0), (1, 2, 0)), ((1, 1, 3), (1, 2, 3)),
        ((1, 2, 1), (1, 2, 2)), ((2, 1, 0), (2, 1, 1)),
        ((2, 1, 2), (2, 1, 3)), ((2, 2, 2), (2, 3, 2)),
        ((3, 1, 0), (4, 1, 0)), ((3, 1, 3), (4, 1, 3)),
        ((4, 2, 1), (4, 2, 2)),
    }
    if not remove <= result:
        raise AssertionError("opposite base exchange source is absent")
    return (result - remove) | add


def extension_pairs(old_width):
    """Edges added when the transverse width grows from o to o+1."""
    o = old_width
    result = set()

    # Complete new L-shell rails at x=1,2.  At x=0 the odd phase omits
    # one edge, while the even phase retains the entire shell.
    for x in (1, 2):
        result |= {edge_pair(0, x, y, o) for y in range(o)}
        result |= {edge_pair(0, x, o, z) for z in range(o + 1)}

    if o % 2:  # odd old width
        result |= {edge_pair(0, 0, y, o) for y in range(o) if y != 1}
        result |= {edge_pair(0, 0, o, z) for z in range(o + 1)}
        result |= {edge_pair(0, 3, y, o) for y in range(o) if y == 0 or y % 2}
        result |= {edge_pair(0, 3, o, z) for z in (0, o)}

        result |= {edge_pair(1, 0, y, o) for y in range(0, o - 1, 2)}
        result |= {edge_pair(1, 0, o - 1, z) for z in range(2, o + 1)}
        result |= {edge_pair(1, 1, 1, o), edge_pair(1, 1, o - 2, o)}
        result |= {edge_pair(1, 4, y, o) for y in range(1, o, 2)}
        result |= {edge_pair(1, 4, o - 1, z) for z in range(1, o, 2)}

        result |= {edge_pair(2, 0, y, o - 1) for y in range(1, o, 2)}
        result.add(edge_pair(2, 0, o, 0))
        result.add(edge_pair(2, 1, o, 1))
        result |= {edge_pair(2, 4, o, z) for z in range(1, o, 2)}
    else:  # even old width; o=4 has a harmless base-shell exception
        result |= {edge_pair(0, 0, y, o) for y in range(o)}
        result |= {edge_pair(0, 0, o, z) for z in range(o + 1)}
        x3_z = {1, 2, 4} if o == 4 else set(range(1, o, 2)) | {o}
        result |= {edge_pair(0, 3, o, z) for z in x3_z}

        result |= {edge_pair(1, 0, y, o) for y in range(o - 1)}
        if o == 4:
            shell_z = {0, 2, 3, 4}
        else:
            shell_z = {0, 1, 2} | set(range(4, o + 1, 2))
        result |= {edge_pair(1, 0, o - 1, z) for z in shell_z}
        result |= {edge_pair(1, 4, y, o) for y in range(0, o, 2)}
        x4_shell_z = {0, 3} if o == 4 else set(range(0, o, 2))
        result |= {edge_pair(1, 4, o - 1, z) for z in x4_shell_z}

        if o == 4:
            result.add(edge_pair(2, 0, o, 0))
        else:
            result |= {edge_pair(2, 0, o, z) for z in range(2, o, 2)}
        result.add(edge_pair(2, 1, 0, o - 1))
        result |= {edge_pair(2, 4, y, o - 1) for y in range(0, o, 2)}

    if len(result) != 10 * o + 5:
        raise AssertionError((o, len(result), 10 * o + 5))
    return result


def exceptional_pairs(width):
    if width % 2:
        return set()
    if width == 4:
        return {edge_pair(2, 0, 3, 2)}
    return {edge_pair(2, 0, width - 1, 0)}


def row(width, tree_pairs):
    started = time.monotonic()
    vertices, edges = cubic_box((5, width, width))
    edge_index = {(edge.u, edge.v): index for index, edge in enumerate(edges)}
    tree = {edge_index[pair] for pair in tree_pairs}
    faces, face_walks = _rotation_faces(
        vertices, edges, opposite_checkerboard_rotation(width)
    )
    genus = (2 - (len(vertices) - len(edges) + len(faces))) // 2
    cycles = _cycle_basis(vertices, edges)
    labels, face_rank = _edge_homology_labels(len(edges), faces, cycles, genus)
    gauge = _gauge_tree(len(edges), faces, cycles, genus)
    exceptional = {edge_index[pair] for pair in exceptional_pairs(width)}
    common = (tree - gauge) - exceptional
    terminals = [(4, y, z) for y in range(width) for z in range(width)]

    adjacency = {vertex: [] for vertex in vertices}
    for index in tree:
        edge = edges[index]
        adjacency[edge.u].append((edge.v, index))
        adjacency[edge.v].append((edge.u, index))
    paths = {terminals[0]: 0}
    stack = [terminals[0]]
    while stack:
        vertex = stack.pop()
        for neighbour, index in adjacency[vertex]:
            if neighbour not in paths:
                paths[neighbour] = paths[vertex] ^ labels[index]
                stack.append(neighbour)
    terminal_rank = _rank([paths[terminal] for terminal in terminals[1:]]) if len(paths) == len(vertices) else -1

    components = _component_terminal_counts(
        vertices, edges, tree - common, terminals
    )
    dual_reached = _dual_reach(
        len(faces), _edge_faces(edges, face_walks),
        set(range(len(edges))) - gauge - common,
    )
    return {
        "width": width,
        "tree_edge_count": len(tree),
        "target_tree_edge_count": len(vertices) - 1,
        "tree_connected": len(paths) == len(vertices),
        "genus": genus,
        "face_boundary_rank": face_rank,
        "chord_count": len(tree - gauge),
        "exceptional_count": len(exceptional),
        "common_basis_count": len(common),
        "target": width * width - 1,
        "terminal_rank": terminal_rank,
        "each_component_has_one_terminal": components == [1] * (width * width),
        "dual_face_count": len(faces),
        "dual_reached_faces": dual_reached,
        "dual_complement_connected": dual_reached == len(faces),
        "wall_seconds": time.monotonic() - started,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }


def audit(maximum_width):
    tree = base_tree_pairs()
    rows = []
    for width in range(4, maximum_width + 1):
        rows.append(row(width, tree))
        tree |= extension_pairs(width)
    return {
        "status": "OBSERVED exact opposite-phase explicit recursion audit",
        "rows": rows,
        "claim_boundary": (
            "The formulas are defined at every width; finite verification does not "
            "replace symbolic parity-shell proofs."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-width", type=int, default=20)
    args = parser.parse_args()
    print(json.dumps(audit(args.maximum_width), indent=2, sort_keys=True))
