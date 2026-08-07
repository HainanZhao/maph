#!/usr/bin/env python3
"""Target every one-edge tree pivot around a rank-14 width-four witness."""

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
from proof.verify_lane_b_arbitrary_width_frontier import _case  # noqa: E402
from src.conventions import cubic_box  # noqa: E402


def search(source: Path, limit: int, seed: int):
    vertices, edges = cubic_box((10, 4, 4))
    labels = _labels(_case(4, 10)["length_rows"][-1], edges)
    data = json.loads(source.read_text())
    tree = set(data["best"]["tree_edges"])
    handle_cut = data["handle_cut"]
    shift = 2 * handle_cut
    mask = (1 << shift) - 1
    fundamental = _fundamental_labels(vertices, edges, labels, tree)
    label_by_chord = dict(fundamental)
    paths = {
        chord: set(_tree_path_edge_indices(vertices, edges, tree, edges[chord].u, edges[chord].v))
        for chord, _ in fundamental
    }
    neighbours = [
        (added, removed)
        for added, _ in fundamental
        for removed in paths[added]
    ]
    rng = random.Random(seed)
    rng.shuffle(neighbours)
    best = None
    evaluated = 0
    for added, removed in neighbours[:limit]:
        pivot = label_by_chord[added]
        updated = []
        for chord, label in fundamental:
            if chord == added:
                continue
            updated.append((chord, label ^ pivot if removed in paths[chord] else label))
        updated.append((removed, pivot))
        certificate = _matroid_intersection(updated, mask, shift, True)
        evaluated += 1
        score = certificate["min_max_value"]
        if best is None or score > best["score"]:
            proposed_tree = (tree | {added}) - {removed}
            # Independently reconstruct rather than trusting the pivot update.
            reconstructed = _fundamental_labels(vertices, edges, labels, proposed_tree)
            replay = _matroid_intersection(reconstructed, mask, shift, True)
            if replay["min_max_value"] != score:
                raise AssertionError("fundamental-cycle pivot update disagrees with reconstruction")
            best = {
                "score": score,
                "added_chord_to_tree": added,
                "removed_tree_edge_to_chords": removed,
                "tree_edges": sorted(proposed_tree),
                "selected_chords_and_labels": replay["selected"],
                "dual_partition": {
                    "rank_M1_on_complement": replay["rank_M1_on_complement"],
                    "rank_M2_on_reachable": replay["rank_M2_on_reachable"],
                    "reachable_count": len(replay["reachable_indices"]),
                    "complement_count": len(replay["complement_indices"]),
                },
            }
            if score == 15:
                break
    return {
        "status": "OBSERVED exact GF(2) exhaustive-neighbour search",
        "source": str(source.resolve().relative_to(ROOT)),
        "shape": [10, 4, 4],
        "handle_cut": handle_cut,
        "target": 15,
        "total_one_exchange_neighbours": len(neighbours),
        "limit": limit,
        "evaluated": evaluated,
        "seed": seed,
        "best": best,
        "claim_boundary": (
            "A score-15 result is independently reconstructed and exact. Exhausting fewer than "
            "all neighbours without success is not a general tree+chord no-go."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=1000000)
    parser.add_argument("--seed", type=int, default=20260807)
    args = parser.parse_args()
    print(json.dumps(search(args.source, args.limit, args.seed), indent=2, sort_keys=True))
