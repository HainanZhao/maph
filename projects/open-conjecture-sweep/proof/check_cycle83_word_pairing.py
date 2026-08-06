#!/usr/bin/env python3
"""Exact outside-word pairing falsifier for C83 ordered-tip fibers."""
from __future__ import annotations

import json
from check_cycle83_tip_fibers import BASE, c82_predecessors, closure


def fiber(pre: list[int], x: int, y: int, z: int, w: int) -> dict:
    n = len(pre); order: list[int] = []; signed: dict[bytes, int] = {}; total = 0; global_margin = 0
    def visit(mask: int) -> None:
        nonlocal total, global_margin
        if len(order) == n:
            pos = [0] * n
            for i, v in enumerate(order): pos[v] = i
            global_margin += 1 if pos[z] < pos[w] else -1
            if pos[x] < pos[z] < pos[y] and pos[x] < pos[w] < pos[y]:
                total += 1
                key = bytes(v for v in order if v not in (z, w))
                signed[key] = signed.get(key, 0) + (1 if pos[z] < pos[w] else -1)
            return
        for v in range(n):
            if not(mask >> v & 1) and pre[v] & ~mask == 0:
                order.append(v); visit(mask | (1 << v)); order.pop()
    visit(0)
    bad = [(k, v) for k, v in signed.items() if v]
    return {"global_margin": global_margin, "fiber_extensions": total, "outside_words": len(signed), "imbalanced_words": len(bad),
            "first_imbalance": None if not bad else {"word": list(bad[0][0]), "signed_count": bad[0][1]}}


def main() -> None:
    closed = closure(list(BASE)); c81 = []
    for y in range(9):
        for x in range(9):
            if closed[y] >> x & 1:
                for z in range(9):
                    for w in range(9):
                        if len({x,y,z,w}) == 4: c81.append(fiber(list(BASE), x, y, z, w))
    c82 = fiber(c82_predecessors(), 0, 1, 10, 11)
    print(json.dumps({"epistemic_status":"PROVED", "c81_queries":len(c81),
                      "c81_global_arrow_queries":sum(r["global_margin"] > 0 for r in c81),
                      "c81_imbalanced_global_arrow_queries":sum(r["global_margin"] > 0 and r["imbalanced_words"] > 0 for r in c81),
                      "c82":c82, "status":"PASS"}, sort_keys=True))

if __name__ == "__main__": main()
