#!/usr/bin/env python3
"""Search tree+chord specializations coupling past and future homology."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import random
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.verify_lane_b_arbitrary_width_frontier import _case, _rank
from src.conventions import cubic_box


def _labels(row, edges):
    result = [0] * len(edges)
    index = {(edge.u, edge.v): i for i, edge in enumerate(edges)}
    for bit_text, pairs in row["atomic_coordinate_edge_support"].items():
        for pair in pairs:
            result[index[(tuple(pair[0]), tuple(pair[1]))]] |= 1 << int(bit_text)
    return result


def _random_tree(vertices, edges, rng):
    vertex_index = {vertex: i for i, vertex in enumerate(vertices)}
    parent = list(range(len(vertices)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    chosen = []
    order = list(range(len(edges)))
    rng.shuffle(order)
    for edge_index in order:
        edge = edges[edge_index]
        a, b = find(vertex_index[edge.u]), find(vertex_index[edge.v])
        if a != b:
            parent[b] = a
            chosen.append(edge_index)
    return set(chosen)


def _fundamental_labels(vertices, edges, labels, tree):
    adjacency = {vertex: [] for vertex in vertices}
    for edge_index in tree:
        edge = edges[edge_index]
        adjacency[edge.u].append((edge.v, edge_index))
        adjacency[edge.v].append((edge.u, edge_index))
    root = vertices[0]
    parent = {root: None}
    path_label = {root: 0}
    stack = [root]
    while stack:
        vertex = stack.pop()
        for neighbour, edge_index in adjacency[vertex]:
            if neighbour in parent:
                continue
            parent[neighbour] = vertex
            path_label[neighbour] = path_label[vertex] ^ labels[edge_index]
            stack.append(neighbour)
    return [
        (edge_index, path_label[edge.u] ^ path_label[edge.v] ^ labels[edge_index])
        for edge_index, edge in enumerate(edges)
        if edge_index not in tree
    ]


def _tree_path_edge_indices(vertices, edges, tree, source, target):
    adjacency = {vertex: [] for vertex in vertices}
    for edge_index in tree:
        edge = edges[edge_index]
        adjacency[edge.u].append((edge.v, edge_index))
        adjacency[edge.v].append((edge.u, edge_index))
    parent = {source: (None, None)}
    stack = [source]
    while stack and target not in parent:
        vertex = stack.pop()
        for neighbour, edge_index in adjacency[vertex]:
            if neighbour not in parent:
                parent[neighbour] = (vertex, edge_index)
                stack.append(neighbour)
    path = []
    vertex = target
    while vertex != source:
        previous, edge_index = parent[vertex]
        path.append(edge_index)
        vertex = previous
    return path


def _greedy_common(vectors, left_mask, right_shift, target, rng, repetitions=200):
    best = []
    for _ in range(repetitions):
        order = vectors[:]
        rng.shuffle(order)
        selected = []
        left = []
        right = []
        for item in order:
            vector = item[1]
            l = vector & left_mask
            r = vector >> right_shift
            if l and r and _rank(left + [l]) > len(left) and _rank(right + [r]) > len(right):
                selected.append(item)
                left.append(l)
                right.append(r)
                if len(selected) == target:
                    return selected
        if len(selected) > len(best):
            best = selected
    return best


def _matroid_intersection(vectors, left_mask, right_shift, return_certificate=False):
    """Maximum common independent set of the two represented matroids."""
    left = [(vector & left_mask) for _, vector in vectors]
    right = [(vector >> right_shift) for _, vector in vectors]
    chosen: set[int] = set()
    while True:
        inside = sorted(chosen)
        outside = [index for index in range(len(vectors)) if index not in chosen]
        left_basis = [left[index] for index in inside]
        right_basis = [right[index] for index in inside]
        sources = [index for index in outside if _rank(left_basis + [left[index]]) > len(inside)]
        sinks = {index for index in outside if _rank(right_basis + [right[index]]) > len(inside)}
        queue = sources[:]
        predecessor = {index: None for index in sources}
        terminal = next((index for index in queue if index in sinks), None)
        while queue and terminal is None:
            current = queue.pop(0)
            if current in chosen:
                # Starting from an M1-addable outside element, augmentation
                # alternates: inside -> outside is an M1 exchange.
                base = [left[index] for index in inside if index != current]
                neighbours = [
                    index for index in outside
                    if _rank(base + [left[index]]) == len(inside)
                ]
            else:
                # Outside -> inside is an M2 exchange.
                neighbours = []
                for index in inside:
                    base = [right[item] for item in inside if item != index]
                    if _rank(base + [right[current]]) == len(inside):
                        neighbours.append(index)
            for neighbour in neighbours:
                if neighbour in predecessor:
                    continue
                predecessor[neighbour] = current
                queue.append(neighbour)
                if neighbour in sinks:
                    terminal = neighbour
                    break
        if terminal is None:
            result = [vectors[index] for index in sorted(chosen)]
            if _rank([vector & left_mask for _, vector in result]) != len(result):
                raise AssertionError("matroid intersection returned an M1-dependent set")
            if _rank([vector >> right_shift for _, vector in result]) != len(result):
                raise AssertionError("matroid intersection returned an M2-dependent set")
            if return_certificate:
                reachable = set(predecessor)
                complement = [index for index in range(len(vectors)) if index not in reachable]
                first_rank = _rank([left[index] for index in complement])
                second_rank = _rank([right[index] for index in reachable])
                if first_rank + second_rank != len(result):
                    raise AssertionError("matroid-intersection min-max certificate failed")
                return {
                    "selected": result,
                    "reachable_indices": sorted(reachable),
                    "complement_indices": complement,
                    "rank_M1_on_complement": first_rank,
                    "rank_M2_on_reachable": second_rank,
                    "min_max_value": first_rank + second_rank,
                }
            return result
        path = []
        current = terminal
        while current is not None:
            path.append(current)
            current = predecessor[current]
        for index in path:
            if index in chosen:
                chosen.remove(index)
            else:
                chosen.add(index)


def search(width: int, length: int, trials: int, seed: int, hill_steps: int,
           forced_handle_cut: int | None):
    structural = _case(width, length)["length_rows"][-1]
    genus = structural["genus"]
    vertices, edges = cubic_box((length, width, width))
    labels = _labels(structural, edges)
    target = width * width - 1
    rng = random.Random(seed)
    best = []
    best_payload = None
    handle_cuts = (
        [forced_handle_cut]
        if forced_handle_cut is not None
        else range((target + 1) // 2, genus - (target + 1) // 2 + 1)
    )
    for handle_cut in handle_cuts:
        shift = 2 * handle_cut
        left_mask = (1 << shift) - 1
        for trial in range(trials):
            tree = _random_tree(vertices, edges, rng)
            vectors = _fundamental_labels(vertices, edges, labels, tree)
            selected = _matroid_intersection(vectors, left_mask, shift)
            if len(selected) > len(best):
                best = selected
                best_payload = {
                    "handle_cut": handle_cut,
                    "trial": trial,
                    "tree_edges": sorted(tree),
                    "selected_chords_and_labels": selected,
                }
            if len(best) == target:
                break
            current = selected
            current_score = len(current)
            current_tree = tree
            for step in range(hill_steps):
                chord = rng.choice([index for index in range(len(edges)) if index not in current_tree])
                edge = edges[chord]
                path = _tree_path_edge_indices(vertices, edges, current_tree, edge.u, edge.v)
                removed = rng.choice(path)
                proposed_tree = (current_tree | {chord}) - {removed}
                proposed_vectors = _fundamental_labels(vertices, edges, labels, proposed_tree)
                proposed = _matroid_intersection(proposed_vectors, left_mask, shift)
                proposed_score = len(proposed)
                # Exact hill climbing with sparse neutral moves to explore a
                # score plateau; no stochastic rank estimate is used.
                accept = (
                    proposed_score > current_score
                    or (proposed_score == current_score and rng.randrange(4) == 0)
                    or (
                        proposed_score + 1 == current_score
                        and step < 3 * hill_steps // 4
                        and rng.randrange(64) == 0
                    )
                )
                if accept:
                    current_tree = proposed_tree
                    current = proposed
                    current_score = proposed_score
                if current_score > len(best):
                    best = current
                    best_payload = {
                        "handle_cut": handle_cut,
                        "trial": trial,
                        "hill_step": step,
                        "tree_edges": sorted(current_tree),
                        "selected_chords_and_labels": current,
                    }
                if len(best) == target:
                    break
            if len(best) == target:
                break
        if len(best) == target:
            break
    return {
        "status": "OBSERVED randomized exact GF(2) search",
        "width": width,
        "length": length,
        "genus": genus,
        "target": target,
        "best_common_rank": len(best),
        "seed": seed,
        "trials_per_cut": trials,
        "hill_steps_per_tree": hill_steps,
        "witness": best_payload,
        "claim_boundary": (
            "A full witness is an exact specialization candidate. Failure of this randomized "
            "search is not a no-go theorem for tree+chord specializations."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", type=int, required=True)
    parser.add_argument("--length", type=int, required=True)
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260807)
    parser.add_argument("--hill-steps", type=int, default=0)
    parser.add_argument("--handle-cut", type=int)
    args = parser.parse_args()
    print(json.dumps(search(
        args.width, args.length, args.trials, args.seed, args.hill_steps, args.handle_cut
    ), indent=2, sort_keys=True))
