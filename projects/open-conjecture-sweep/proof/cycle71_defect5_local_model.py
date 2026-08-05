#!/usr/bin/env python3
"""Construct and audit a local D=5 high-star incidence template."""
from __future__ import annotations
import itertools,json

# Five repeat vertices r_j lie in sides j=1..5 and join adjacent star lines.
PAIRS=[(0,1),(1,2),(2,3),(3,4),(4,5)]

def main():
    star=[]
    for i in range(6):
        line=[(0,'v')]
        for q,(a,b) in enumerate(PAIRS,1):
            line.append((q, f'r{q}' if i in (a,b) else f'x{i}_{q}'))
        star.append(frozenset(line))
    choices=[]
    for j,(a,b) in enumerate(PAIRS,1):
        remaining=[i for i in range(6) if i not in (a,b)]
        other_sides=[q for q in range(1,6) if q!=j]
        choices.append([
            frozenset([(0,f'u{j}'),(j,f'r{j}')]+[(q,f'x{perm[t]}_{q}') for t,q in enumerate(other_sides)])
            for perm in itertools.permutations(remaining)
            if all(perm[t] not in PAIRS[q-1] for t,q in enumerate(other_sides))
        ])
    selected=[]
    def search(j):
        if j==5:return True
        for line in choices[j]:
            if all(line & prior for prior in selected):
                selected.append(line)
                if search(j+1):return True
                selected.pop()
        return False
    assert search(0)
    edges=star+selected
    assert all(a&b for i,a in enumerate(edges) for b in edges[i+1:])
    excess=sum(len(a&b)-1 for i,a in enumerate(edges) for b in edges[i+1:])
    vertices=sorted(set().union(*edges))
    tau=next(k for k in range(1,7) if any(all(set(C)&e for e in edges) for C in itertools.combinations(vertices,k)))
    print(json.dumps({'status':'PASS','epistemic_status':'PROVED','edges':len(edges),'vertices':len(vertices),'excess_pair_intersections':excess,'tau':tau,'claim_boundary':'An exact local equality-template realization only; if tau<6 it is a falsifier for a local-to-global D=5 contradiction, not for Ryser.'},sort_keys=True))
if __name__=='__main__':main()
