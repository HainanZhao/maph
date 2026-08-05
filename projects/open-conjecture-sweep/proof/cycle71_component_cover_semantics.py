#!/usr/bin/env python3
"""Exact semantics checker for monochromatic component covers."""
from __future__ import annotations

import itertools
import json


def components(n: int, coloring: dict[tuple[int,int], int]):
    result=[]
    for color in range(6):
        parent=list(range(n))
        def find(x):
            while parent[x]!=x:
                parent[x]=parent[parent[x]]; x=parent[x]
            return x
        def join(a,b):
            a,b=find(a),find(b)
            if a!=b: parent[b]=a
        seen=[False]*n
        for (a,b), c in coloring.items():
            if c==color: join(a,b); seen[a]=seen[b]=True
        groups={}
        for v in range(n):
            if seen[v]: groups.setdefault(find(v),0); groups[find(v)] |= 1<<v
        result.extend((color,mask) for mask in groups.values())
    return result


def cover_number(n: int, comps):
    full=(1<<n)-1
    for k in range(1,7):
        if any((lambda choice: __import__('functools').reduce(int.__or__,(comps[i][1] for i in choice),0)==full)(choice) for choice in itertools.combinations(range(len(comps)),k)):
            return k
    return None


def main():
    # Exact controls: a monochromatic K_n needs one component; a six-color
    # star coloring is evaluated without imposing distinct colors/components.
    n=7
    mono={(i,j):0 for i in range(n) for j in range(i+1,n)}
    star={(i,j):(j-1 if i==0 else 0) for i in range(n) for j in range(i+1,n)}
    rows=[]
    for name,coloring,expected in [('monochromatic',mono,1),('six_color_star',star,1)]:
        cs=components(n,coloring); value=cover_number(n,cs)
        assert value==expected
        rows.append({'name':name,'components':cs,'cover_number':value})
    print(json.dumps({'status':'PASS','epistemic_status':'PROVED','controls':rows,
      'semantics':'A cover is a collection of arbitrary monochromatic connected components; components may overlap and colors may repeat.',
      'claim_boundary':'Component-cover semantics only; no universal six-color theorem or finite obstruction conclusion.'},sort_keys=True))

if __name__=='__main__': main()
