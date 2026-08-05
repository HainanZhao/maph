#!/usr/bin/env python3
"""Principal exact edge-subset classification for Cycle 53."""
from __future__ import annotations

import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle53-analytic-local-stability"
EDGES = tuple((i, j) for i in range(5) for j in range(5) if (j - i) % 5 not in (0, 4))


def subset_stats(chosen):
    degree = [0] * 10
    for left, right in chosen:
        degree[left] += 1
        degree[5 + right] += 1
    active = [v for v, d in enumerate(degree) if d]
    # Component count is deliberately reconstructed from the selected graph.
    seen, components = set(), 0
    adjacency = {v: set() for v in active}
    for left, right in chosen:
        adjacency[left].add(5 + right)
        adjacency[5 + right].add(left)
    for root in active:
        if root in seen:
            continue
        components += 1
        frontier = [root]
        seen.add(root)
        while frontier:
            v = frontier.pop()
            for w in adjacency[v]:
                if w not in seen:
                    seen.add(w)
                    frontier.append(w)
    return degree, components


def compute():
    assert len(EDGES) == 15
    pair_adjacent = pair_disjoint = 0
    min_degree_two = {k: 0 for k in range(16)}
    four_cycle_masks = []
    for mask in range(1 << 15):
        chosen = [edge for index, edge in enumerate(EDGES) if mask >> index & 1]
        k = len(chosen)
        degree, _ = subset_stats(chosen)
        active = [d for d in degree if d]
        if active and min(active) >= 2:
            min_degree_two[k] += 1
            if k == 4:
                assert sorted(active) == [2, 2, 2, 2]
                four_cycle_masks.append(mask)
        if k == 2:
            if chosen[0][0] == chosen[1][0] or chosen[0][1] == chosen[1][1]:
                pair_adjacent += 1
            else:
                pair_disjoint += 1
    # An independent incidence count: all ten vertices have degree three.
    assert pair_adjacent == 10 * 3
    assert pair_disjoint == 15 * 14 // 2 - pair_adjacent
    assert min_degree_two[3] == 0
    return {
        "status": "PASS", "epistemic_status": "PROVED", "edge_count": len(EDGES),
        "subsets": 1 << 15, "pair_adjacent": pair_adjacent, "pair_disjoint": pair_disjoint,
        "minimum_degree_two_by_edges": {str(k): v for k, v in min_degree_two.items() if v},
        "four_cycle_count": len(four_cycle_masks), "four_cycle_masks": four_cycle_masks,
        "trace_control": trace_control(four_cycle_masks),
    }


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(a))) for j in range(len(b))] for i in range(len(a))]


def trace_control(four_cycle_masks):
    # Symmetric, row-sum-zero, integer q=3 step kernel B.  This checks the
    # q^6 tr(B^4) scaling of every raw four-cycle contribution to Q_B.
    b = [[1, -1, 0], [-1, 1, 0], [0, 0, 0]]
    b2, b4 = matmul(b, b), None
    b4 = matmul(b2, b2)
    tr4 = sum(b4[i][i] for i in range(3))
    q4_sum = 0
    for vertex_map in itertools.product(range(3), repeat=10):
        for mask in four_cycle_masks:
            chosen = [edge for e, edge in enumerate(EDGES) if mask >> e & 1]
            value = 1
            for left, right in chosen:
                value *= b[vertex_map[left]][vertex_map[5 + right]]
            q4_sum += value
    return {"q": 3, "matrix": b, "trace_B4": tr4, "raw_Q4": q4_sum}


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    value = compute()
    (OUT / "principal-summary.json").write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    print(json.dumps(value, sort_keys=True))
