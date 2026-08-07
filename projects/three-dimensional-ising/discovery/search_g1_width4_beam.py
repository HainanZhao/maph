#!/usr/bin/env python3
"""Beam edge-exchange search for the width-four paired-cycle tree."""

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
from proof.verify_lane_b_arbitrary_width_frontier import _case, _rank  # noqa: E402
from src.conventions import cubic_box  # noqa: E402


def search(source: Path, handle_cut: int, generations: int, beam_size: int,
           children: int, seed: int):
    vertices, edges = cubic_box((10, 4, 4))
    labels = _labels(_case(4, 10)["length_rows"][-1], edges)
    source_data = json.loads(source.read_text())
    witness = source_data.get("witness") or source_data.get("best")
    initial_tree = frozenset(witness["tree_edges"])
    shift = 2 * handle_cut
    mask = (1 << shift) - 1
    rng = random.Random(seed)

    cache = {}

    def evaluate(tree):
        key = tuple(sorted(tree))
        if key in cache:
            return cache[key]
        vectors = _fundamental_labels(vertices, edges, labels, set(tree))
        certificate = _matroid_intersection(vectors, mask, shift, True)
        mixed = sum(bool(value & mask) and bool(value >> shift) for _, value in vectors)
        left_mixed_rank = _rank([value & mask for _, value in vectors if value >> shift])
        right_mixed_rank = _rank([value >> shift for _, value in vectors if value & mask])
        result = {
            "score": certificate["min_max_value"],
            "secondary": [min(left_mixed_rank, right_mixed_rank), mixed],
            "selected_chords_and_labels": certificate["selected"],
            "dual_partition": {
                "rank_M1_on_complement": certificate["rank_M1_on_complement"],
                "rank_M2_on_reachable": certificate["rank_M2_on_reachable"],
                "reachable_count": len(certificate["reachable_indices"]),
                "complement_count": len(certificate["complement_indices"]),
            },
        }
        cache[key] = result
        return result

    beam = [initial_tree]
    best_tree = initial_tree
    best_result = evaluate(initial_tree)
    for generation in range(generations):
        candidates = set(beam)
        for tree in beam:
            tree_set = set(tree)
            non_tree = [index for index in range(len(edges)) if index not in tree_set]
            for _ in range(children):
                proposed = set(tree_set)
                exchanges = 1 + (rng.randrange(4) == 0)
                for _ in range(exchanges):
                    added = rng.choice([index for index in non_tree if index not in proposed])
                    edge = edges[added]
                    path = _tree_path_edge_indices(vertices, edges, proposed, edge.u, edge.v)
                    removed = rng.choice(path)
                    proposed.add(added)
                    proposed.remove(removed)
                candidates.add(frozenset(proposed))
        ranked = []
        for tree in candidates:
            result = evaluate(tree)
            ranked.append((result["score"], *result["secondary"], rng.random(), tree))
            if (result["score"], result["secondary"]) > (
                best_result["score"], best_result["secondary"]
            ):
                best_tree, best_result = tree, result
        ranked.sort(reverse=True)
        # Keep the strongest half and a diverse sample within two ranks of
        # the best, allowing paths that temporarily descend.
        elite = [row[-1] for row in ranked[: beam_size // 2]]
        floor = max(0, best_result["score"] - 2)
        pool = [row[-1] for row in ranked[beam_size // 2:] if row[0] >= floor]
        rng.shuffle(pool)
        beam = elite + pool[: beam_size - len(elite)]
        if best_result["score"] == 15:
            break
    return {
        "status": "OBSERVED exact GF(2) beam search",
        "source": str(source.resolve().relative_to(ROOT)),
        "shape": [10, 4, 4],
        "handle_cut": handle_cut,
        "target": 15,
        "generations_requested": generations,
        "beam_size": beam_size,
        "children_per_tree": children,
        "seed": seed,
        "evaluated_trees": len(cache),
        "best": {
            **best_result,
            "tree_edges": sorted(best_tree),
        },
        "claim_boundary": (
            "Every score and min-max certificate is exact. Failure to reach 15 is bounded-search "
            "evidence only, not a tree+chord no-go theorem."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--handle-cut", type=int, required=True)
    parser.add_argument("--generations", type=int, default=40)
    parser.add_argument("--beam-size", type=int, default=24)
    parser.add_argument("--children", type=int, default=8)
    parser.add_argument("--seed", type=int, default=20260807)
    args = parser.parse_args()
    print(json.dumps(search(
        args.source, args.handle_cut, args.generations, args.beam_size, args.children, args.seed
    ), indent=2, sort_keys=True))
