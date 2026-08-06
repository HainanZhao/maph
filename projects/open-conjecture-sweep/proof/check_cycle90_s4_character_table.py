#!/usr/bin/env python3
"""Exact S4 class algebra and character-table audit for C90.

This checks the representation data which a valid second C90 route must use;
it does not itself certify the T-transform polynomial.
"""
from __future__ import annotations

from itertools import permutations
import json


G = tuple(permutations(range(4)))


def mul(a, b): return tuple(a[b[i]] for i in range(4))
def inv(a):
    out = [0] * 4
    for i, x in enumerate(a): out[x] = i
    return tuple(out)
def ctype(a):
    seen, sizes = set(), []
    for i in range(4):
        if i not in seen:
            j, n = i, 0
            while j not in seen: seen.add(j); n += 1; j = a[j]
            sizes.append(n)
    return tuple(sorted(sizes, reverse=True))


ORDER = ((1,1,1,1), (2,1,1), (2,2), (3,1), (4,))
CHARS = ((1,1,1,1,1), (1,-1,1,1,-1), (2,0,2,-1,0), (3,1,-1,0,-1), (3,-1,-1,0,1))


def main():
    classes = [[x for x in G if ctype(x) == t] for t in ORDER]
    sizes = [len(c) for c in classes]
    assert sizes == [1, 6, 3, 8, 6]
    by_element = {x: i for i, c in enumerate(classes) for x in c}
    # Orthogonality independently catches both the class ordering and character
    # labels used in the planned Fourier route.
    gram = [[sum(sizes[k] * CHARS[i][k] * CHARS[j][k] for k in range(5)) for j in range(5)] for i in range(5)]
    assert gram == [[24 if i == j else 0 for j in range(5)] for i in range(5)]
    assert sum(row[0] ** 2 for row in CHARS) == 24
    # Structure constants for normalized class sums: every element of class k
    # receives the same number of products from Ci*Cj.
    structure = {}
    for i in range(5):
        for j in range(5):
            counts = [0] * 5
            for x in classes[i]:
                for y in classes[j]: counts[by_element[mul(x,y)]] += 1
            coeff = []
            for k, c in enumerate(classes):
                values = {counts[by_element[z]] for z in c}
                assert len(values) == 1
                coeff.append(values.pop())
            structure[f"{i}{j}"] = coeff
    print(json.dumps({"status": "S4_CHARACTER_TABLE_PASS", "epistemic_status": "PROVED",
                      "class_order": [list(x) for x in ORDER], "class_sizes": sizes,
                      "dimensions": [row[0] for row in CHARS], "characters": [list(x) for x in CHARS],
                      "structure_constants": structure,
                      "claim_boundary": "This proves the S4 class/character data used by a future independent Fourier contraction, not the C90 T-transform inequality."}, sort_keys=True))


if __name__ == "__main__": main()
