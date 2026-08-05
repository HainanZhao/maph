#!/usr/bin/env python3
"""Exact four-vertex countermodel to dominance-only LEM 4-cycle shortening."""

from itertools import permutations
import json

# x<y is the only nontrivial comparable pair.  The full cycle is
# x->y->z->w->x.  Dominance forces x->z and w->y.
V = range(4)
x, y, z, w = V
order = {(x, y)}
edges = {(x, y), (y, z), (z, w), (w, x), (x, z), (w, y)}


def comparable(a, b):
    return (a, b) in order or (b, a) in order


def cycle4(edge_set):
    return any(
        all((p[j], p[(j + 1) % 4]) in edge_set for j in range(4))
        for p in permutations(V)
    )


def main():
    assert all((b, a) not in edges for a, b in edges)
    for a, b in order:
        for q in V:
            if (q, a) in edges:
                assert (q, b) in edges
            if (b, q) in edges:
                assert (a, q) in edges
    assert all((a, b) in edges for a, b in ((x, y), (y, z), (z, w), (w, x)))
    inc = {(a, b) for a, b in edges if not comparable(a, b)}
    assert not cycle4(inc)
    print(json.dumps({
        "status": "PASS",
        "epistemic_status": "PROVED",
        "vertices": 4,
        "full_cycle": ["x->y", "y->z", "z->w", "w->x"],
        "incomparable_edges": sorted([f"{a}->{b}" for a, b in inc]),
        "restricted_has_4_cycle": False,
        "scope": "abstract dominance model only",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
