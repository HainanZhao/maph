#!/usr/bin/env python3
"""Expose the exact shell Schur block in the recursive prefix encoder.

This is a discovery diagnostic.  It eliminates the old terminal columns from
the atomic-coordinate terminal path matrix and records pivots for the new
L-shaped terminal shell.  It does not promote a finite-width pattern.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from discovery.audit_g1_explicit_all_width_induction import (  # noqa: E402
    _base_tree,
    _embed,
    extension_pairs,
)
from discovery.search_g1_paired_fundamental_cycles import _labels  # noqa: E402
from proof.verify_lane_b_arbitrary_width_frontier import _case  # noqa: E402
from src.conventions import cubic_box  # noqa: E402


def _insert(basis: dict[int, int], vector: int) -> tuple[int | None, int]:
    while vector:
        pivot = vector.bit_length() - 1
        if pivot in basis:
            vector ^= basis[pivot]
        else:
            basis[pivot] = vector
            return pivot, vector
    return None, 0


def _terminal_vectors(width: int, tree: set[int]):
    vertices, edges = cubic_box((5, width, width))
    labels = _labels(_case(width, 5)["length_rows"][-1], edges)
    adjacency = {vertex: [] for vertex in vertices}
    for edge_index in tree:
        edge = edges[edge_index]
        adjacency[edge.u].append((edge.v, edge_index))
        adjacency[edge.v].append((edge.u, edge_index))
    root = (4, 0, 0)
    paths = {root: 0}
    stack = [root]
    while stack:
        vertex = stack.pop()
        for neighbour, edge_index in adjacency[vertex]:
            if neighbour not in paths:
                paths[neighbour] = paths[vertex] ^ labels[edge_index]
                stack.append(neighbour)
    if len(paths) != len(vertices):
        raise AssertionError("tree is disconnected")
    return {
        (y, z): paths[(4, y, z)]
        for y in range(width)
        for z in range(width)
        if (y, z) != (0, 0)
    }


def audit(maximum_width: int):
    width = 4
    tree = set(_base_tree())
    rows = []
    while width < maximum_width:
        old_vectors = _terminal_vectors(width, tree)
        old_width = width
        width += 1
        tree = _embed(tree, old_width, width)
        _, edges = cubic_box((5, width, width))
        edge_index = {(edge.u, edge.v): i for i, edge in enumerate(edges)}
        tree |= {edge_index[pair] for pair in extension_pairs(old_width)}
        vectors = _terminal_vectors(width, tree)

        # Use embedded old terminal columns first.  Atomic width nesting makes
        # this a legitimate exact elimination, though their coordinate rows
        # need not occupy an initial interval.
        basis: dict[int, int] = {}
        old_pivots = []
        for terminal in sorted(old_vectors):
            pivot, _ = _insert(basis, vectors[terminal])
            if pivot is None:
                raise AssertionError("old terminal columns lost independence")
            old_pivots.append(pivot)
        shell_rows = []
        shell = [
            terminal for terminal in sorted(vectors)
            if terminal[0] == old_width or terminal[1] == old_width
        ]
        for terminal in shell:
            pivot, reduced = _insert(basis, vectors[terminal])
            shell_rows.append({
                "terminal": list(terminal),
                "pivot_bit": pivot,
                "pivot_handle": None if pivot is None else pivot // 2,
                "pivot_kind": None if pivot is None else ("a" if pivot % 2 == 0 else "b"),
                "reduced_support": [
                    bit for bit in range(reduced.bit_length()) if (reduced >> bit) & 1
                ],
            })
        rows.append({
            "old_width": old_width,
            "new_width": width,
            "old_rank": len(old_pivots),
            "shell_count": len(shell),
            "shell_rank_increment": sum(row["pivot_bit"] is not None for row in shell_rows),
            "shell": shell_rows,
        })
    return {
        "status": "OBSERVED exact GF(2) shell-Schur diagnostic",
        "rows": rows,
        "claim_boundary": "Finite atomic-coordinate pivots are pattern data, not an arbitrary-width proof.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-width", type=int, default=9)
    args = parser.parse_args()
    print(json.dumps(audit(args.maximum_width), indent=2, sort_keys=True))
