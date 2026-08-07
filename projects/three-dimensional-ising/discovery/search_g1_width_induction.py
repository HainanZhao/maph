#!/usr/bin/env python3
"""Extend the certified w=3 paired-cycle core into width four."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import random
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from discovery.search_g1_paired_fundamental_cycles import (  # noqa: E402
    _fundamental_labels,
    _labels,
    _matroid_intersection,
    _tree_path_edge_indices,
)
from proof.verify_g1_paired_cycle_w3 import CHORDS, TREE_EDGES  # noqa: E402
from proof.verify_lane_b_arbitrary_width_frontier import _case, _rank  # noqa: E402
from src.conventions import cubic_box  # noqa: E402


def _basis(vectors):
    result = {}
    for vector in vectors:
        while vector:
            pivot = vector.bit_length() - 1
            if pivot in result:
                vector ^= result[pivot]
            else:
                result[pivot] = vector
                break
    return result


def _reduce(vector, basis):
    for pivot in sorted(basis, reverse=True):
        if (vector >> pivot) & 1:
            vector ^= basis[pivot]
    return vector


def _random_extension(vertices, edges, fixed_tree, forbidden_chords, rng):
    vertex_index = {vertex: index for index, vertex in enumerate(vertices)}
    parent = list(range(len(vertices)))

    def find(value):
        while parent[value] != value:
            parent[value] = parent[parent[value]]
            value = parent[value]
        return value

    def unite(left, right):
        left, right = find(left), find(right)
        if left == right:
            return False
        parent[right] = left
        return True

    tree = set(fixed_tree)
    for edge_index in fixed_tree:
        edge = edges[edge_index]
        if not unite(vertex_index[edge.u], vertex_index[edge.v]):
            raise AssertionError("embedded old tree acquired a cycle")
    candidates = [
        index for index in range(len(edges))
        if index not in fixed_tree and index not in forbidden_chords
    ]
    rng.shuffle(candidates)
    for edge_index in candidates:
        edge = edges[edge_index]
        if unite(vertex_index[edge.u], vertex_index[edge.v]):
            tree.add(edge_index)
    if len(tree) != len(vertices) - 1:
        raise AssertionError("random extension is not spanning")
    return tree


def search(trials: int, seed: int, hill_steps: int):
    length = 10
    old_width, new_width = 3, 4
    old_vertices, old_edges = cubic_box((length, old_width, old_width))
    vertices, edges = cubic_box((length, new_width, new_width))
    edge_index = {(edge.u, edge.v): index for index, edge in enumerate(edges)}
    fixed_tree = {edge_index[(old_edges[index].u, old_edges[index].v)] for index in TREE_EDGES}
    old_chords = [edge_index[(old_edges[index].u, old_edges[index].v)] for index in CHORDS]
    structural = _case(new_width, length)["length_rows"][-1]
    labels = _labels(structural, edges)
    handle_cut = 9
    shift = 2 * handle_cut
    mask = (1 << shift) - 1
    rng = random.Random(seed)
    best = None

    def evaluate(tree):
        fundamental = _fundamental_labels(vertices, edges, labels, tree)
        by_edge = dict(fundamental)
        old_labels = [by_edge[index] for index in old_chords]
        if _rank([value & mask for value in old_labels]) != 8:
            raise AssertionError("embedded old left core lost rank")
        if _rank([value >> shift for value in old_labels]) != 8:
            raise AssertionError("embedded old right core lost rank")
        left_basis = _basis([value & mask for value in old_labels])
        right_basis = _basis([value >> shift for value in old_labels])
        quotient = []
        original = {}
        for edge, value in fundamental:
            if edge in old_chords:
                continue
            left = _reduce(value & mask, left_basis)
            right = _reduce(value >> shift, right_basis)
            packed = left | (right << shift)
            quotient.append((edge, packed))
            original[edge] = value
        additional = _matroid_intersection(quotient, mask, shift)
        score = 8 + len(additional)
        selected_edges = [edge for edge, _ in additional]
        return score, {
            "total_common_rank": score,
            "old_core_rank": 8,
            "additional_rank": len(additional),
            "tree_edges": sorted(tree),
            "old_chords": old_chords,
            "old_fundamental_labels": old_labels,
            "additional_chords": selected_edges,
            "additional_full_labels": [original[edge] for edge in selected_edges],
            "additional_quotient_labels": [value for _, value in additional],
        }

    for trial in range(trials):
        tree = _random_extension(vertices, edges, fixed_tree, set(old_chords), rng)
        score, payload = evaluate(tree)
        if best is None or score > best["total_common_rank"]:
            best = {"trial": trial, **payload}
            if score == new_width * new_width - 1:
                break
    if best is not None and best["total_common_rank"] < new_width * new_width - 1:
        current_tree = set(best["tree_edges"])
        current_score = best["total_common_rank"]
        for step in range(hill_steps):
            available = [
                index for index in range(len(edges))
                if index not in current_tree and index not in old_chords
            ]
            added = rng.choice(available)
            edge = edges[added]
            path = _tree_path_edge_indices(vertices, edges, current_tree, edge.u, edge.v)
            removable = [index for index in path if index not in fixed_tree]
            if not removable:
                continue
            removed = rng.choice(removable)
            proposed_tree = (current_tree | {added}) - {removed}
            score, payload = evaluate(proposed_tree)
            accept = (
                score > current_score
                or (score == current_score and rng.randrange(4) == 0)
                or (
                    score + 1 == current_score
                    and step < 3 * hill_steps // 4
                    and rng.randrange(64) == 0
                )
            )
            if accept:
                current_tree = proposed_tree
                current_score = score
            if score > best["total_common_rank"]:
                best = {"trial": best["trial"], "hill_step": step, **payload}
            if best["total_common_rank"] == new_width * new_width - 1:
                break
    return {
        "status": "OBSERVED randomized exact GF(2) induction search",
        "shape": [length, new_width, new_width],
        "handle_cut": handle_cut,
        "target": new_width * new_width - 1,
        "old_target": old_width * old_width - 1,
        "new_modes_needed": 2 * new_width - 1,
        "trials": trials,
        "hill_steps": hill_steps,
        "seed": seed,
        "best": best,
        "claim_boundary": (
            "A target witness is an exact width-four construction containing the certified "
            "width-three core. Failure of a bounded randomized extension search is not a no-go."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260807)
    parser.add_argument("--hill-steps", type=int, default=0)
    args = parser.parse_args()
    print(json.dumps(search(args.trials, args.seed, args.hill_steps), indent=2, sort_keys=True))
