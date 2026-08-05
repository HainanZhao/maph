#!/usr/bin/env python3
"""Independent bit-mask enumeration for C53's edge-subset identities."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle53-analytic-local-stability"
E = tuple((i, j) for j in range(5) for i in range(5) if (j - i) % 5 not in (0, 4))


def run():
    adjacent = disjoint = cycles = 0
    mindeg = {}
    for mask in range(1 << len(E)):
        count = mask.bit_count()
        left = [0] * 5
        right = [0] * 5
        for n, (i, j) in enumerate(E):
            if mask & (1 << n):
                left[i] += 1
                right[j] += 1
        positive = [x for x in left + right if x]
        if positive and min(positive) >= 2:
            mindeg[count] = mindeg.get(count, 0) + 1
            cycles += count == 4
        if count == 2:
            picked = [E[n] for n in range(len(E)) if mask & (1 << n)]
            if picked[0][0] == picked[1][0] or picked[0][1] == picked[1][1]:
                adjacent += 1
            else:
                disjoint += 1
    # Direct common-neighbor derivation for C4: select unordered left pair,
    # then unordered common-right pair.
    c4_by_pairs = 0
    for a in range(5):
        for b in range(a + 1, 5):
            common = [j for j in range(5) if (a, j) in E and (b, j) in E]
            c4_by_pairs += len(common) * (len(common) - 1) // 2
    assert adjacent == 30 and disjoint == 75 and cycles == c4_by_pairs
    return {"status": "PASS", "edge_count": len(E), "subsets": 1 << len(E),
            "pair_adjacent": adjacent, "pair_disjoint": disjoint,
            "minimum_degree_two_by_edges": {str(k): v for k, v in sorted(mindeg.items())},
            "four_cycle_count": cycles, "four_cycle_pair_count": c4_by_pairs}


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    result = run()
    (OUT / "independent-summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))
