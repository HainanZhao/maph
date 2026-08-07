#!/usr/bin/env python3
"""Independent matrix-first checker for C104's dihedral Cayley gate."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def legendre(a: int, p: int) -> int:
    a %= p
    return 0 if a == 0 else (1 if pow(a, (p - 1) // 2, p) == 1 else -1)


def product(x: tuple[int, int], y: tuple[int, int], p: int) -> tuple[int, int]:
    return ((x[0] + (1 if x[1] == 0 else -1) * y[0]) % p, (x[1] + y[1]) % 2)


def row(mask: int, p: int) -> dict[str, object]:
    elements = [(a, b) for b in range(2) for a in range(p)]
    place = {g: i for i, g in enumerate(elements)}
    conn = {(a, 0) for a in range(1, p)} if mask & 1 else set()
    conn |= {(a, 1) for a in range(p) if mask & (1 << (1 if a == 0 else 2 if legendre(a, p) == 1 else 3))}
    matrix = [[0] * (2 * p) for _ in elements]
    for i, g in enumerate(elements):
        for h in conn: matrix[i][place[product(g, h, p)]] = 1
    seidel = [[0 if i == j else 1 - 2 * matrix[i][j] for j in range(2 * p)] for i in range(2 * p)]
    common = [[sum(matrix[i][k] * matrix[k][j] for k in range(2 * p)) for j in range(2 * p)] for i in range(2 * p)]
    # Recompute convolution as a multiset product, with a different element order.
    counts = {g: 0 for g in elements}
    for a in conn:
        for b in conn: counts[product(a, b, p)] += 1
    def inv(g: tuple[int, int]) -> tuple[int, int]: return ((-g[0] if g[1] == 0 else g[0]) % p, g[1])
    agrees = all(common[i][j] == counts[product(inv(elements[i]), elements[j], p)] for i in range(2 * p) for j in range(2 * p))
    values = [sum(seidel[i][k] * seidel[k][j] for k in range(2 * p)) for i in range(2 * p) for j in range(i + 1, 2 * p)]
    row_ok = all(sum(r) == -1 for r in seidel)
    square_ok = all(value in (0, -4) for value in values)
    return {"mask": mask, "degree": len(conn), "route_agrees": agrees,
            "row_ok": row_ok,
            "offdiagonal_square_distribution": {str(value): values.count(value) for value in sorted(set(values))},
            "square_ok": square_ok, "hit": agrees and row_ok and square_ok}


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("result", type=Path); args = parser.parse_args()
    q7 = [row(mask, 7) for mask in range(16)]
    hits = [entry["mask"] for entry in q7 if entry["hit"]]
    expected = {"family": "two-orbit-dihedral-cayley-four-bit", "q7": q7, "q7_hits": hits, "q23": [row(mask, 23) for mask in hits]}
    if json.loads(args.result.read_text()) != expected: raise SystemExit("enumeration disagreement")
    print(json.dumps({"q7_rows": len(q7), "q7_hits": hits, "q23_rows": len(hits), "status": "PASS"}, sort_keys=True))


if __name__ == "__main__": main()
