#!/usr/bin/env python3
"""Test the explicit two-end-tree plus longitudinal-wire G1 specialization."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from discovery.audit_g1_lifted_matroids import _incidence_columns  # noqa: E402
from discovery.search_g1_paired_fundamental_cycles import _labels, _random_tree  # noqa: E402
from proof.verify_lane_b_arbitrary_width_frontier import _case, _rank  # noqa: E402
from src.conventions import cubic_box  # noqa: E402


def search(width, length, handle_cut, trials, seed):
    structural = _case(width, length)["length_rows"][-1]
    genus = structural["genus"]
    vertices, edges = cubic_box((length, width, width))
    labels = _labels(structural, edges)
    incidence = _incidence_columns(vertices, edges)
    edge_index = {(edge.u, edge.v): index for index, edge in enumerate(edges)}
    slice_vertices, slice_edges = cubic_box((1, width, width))
    rng = random.Random(seed)
    rails = {
        index for index, edge in enumerate(edges) if edge.u[0] != edge.v[0]
    }
    shift = 2 * handle_cut
    left_mask = (1 << shift) - 1
    best = None
    for trial in range(trials):
        ends = []
        for layer in (0, length - 1):
            local_tree = _random_tree(slice_vertices, slice_edges, rng)
            ends.extend(
                edge_index[((layer, slice_edges[index].u[1], slice_edges[index].u[2]),
                            (layer, slice_edges[index].v[1], slice_edges[index].v[2]))]
                for index in local_tree
            )
        selected = sorted(rails | set(ends))
        graph_rank = _rank([incidence[index] for index in selected])
        left_lifted = _rank([
            incidence[index] | ((labels[index] & left_mask) << (len(vertices) - 1))
            for index in selected
        ])
        right_lifted = _rank([
            incidence[index] | ((labels[index] >> shift) << (len(vertices) - 1))
            for index in selected
        ])
        score = min(left_lifted, right_lifted) - graph_rank
        if best is None or score > best["common_projection_rank"]:
            best = {
                "trial": trial,
                "common_projection_rank": score,
                "left_projection_rank": left_lifted - graph_rank,
                "right_projection_rank": right_lifted - graph_rank,
                "selected_edges": selected,
            }
    return {
        "status": "OBSERVED exact GF(2) two-end encoder search",
        "shape": [length, width, width],
        "genus": genus,
        "handle_cut": handle_cut,
        "target": width * width - 1,
        "trials": trials,
        "seed": seed,
        "best": best,
        "claim_boundary": "Failure only rejects this two-end-tree specialization family.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", type=int, required=True)
    parser.add_argument("--length", type=int, required=True)
    parser.add_argument("--handle-cut", type=int, required=True)
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260807)
    args = parser.parse_args()
    print(json.dumps(search(**vars(args)), indent=2, sort_keys=True))
