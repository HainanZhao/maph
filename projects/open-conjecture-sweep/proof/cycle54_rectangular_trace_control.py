#!/usr/bin/env python3
"""Exact rectangular C4 normalization control for Cycle 54."""
from __future__ import annotations
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle54-bipartite-directional"
E = tuple((i, j) for i in range(5) for j in range(5) if (j - i) % 5 not in (0, 4))


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def main():
    b = [[1, -1, 0], [-1, 1, 0]]  # 2x3, every row and column sum is zero.
    assert all(sum(row) == 0 for row in b)
    assert all(sum(b[i][j] for i in range(2)) == 0 for j in range(3))
    bbt = mm(b, list(map(list, zip(*b))))
    trace = sum(x * x for row in bbt for x in row)
    cycle_masks = []
    for mask in range(1 << 15):
        if mask.bit_count() != 4:
            continue
        dl, dr = [0] * 5, [0] * 5
        for n, (i, j) in enumerate(E):
            if mask >> n & 1:
                dl[i] += 1; dr[j] += 1
        if sorted(x for x in dl + dr if x) == [2, 2, 2, 2]:
            cycle_masks.append(mask)
    raw = 0
    for assignment in itertools.product(range(2), repeat=5):
        for right in itertools.product(range(3), repeat=5):
            for mask in cycle_masks:
                product = 1
                for n, (i, j) in enumerate(E):
                    if mask >> n & 1:
                        product *= b[assignment[i]][right[j]]
                raw += product
    result = {"status": "PASS", "left_blocks": 2, "right_blocks": 3, "matrix": b,
              "four_cycle_count": len(cycle_masks), "trace_BBT_squared": trace, "raw_Q4": raw,
              "expected_raw_Q4": len(cycle_masks) * 2**3 * 3**3 * trace}
    assert raw == result["expected_raw_Q4"] == 17280
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "rectangular-control.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
