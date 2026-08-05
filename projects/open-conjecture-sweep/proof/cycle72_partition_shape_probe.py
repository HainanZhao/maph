#!/usr/bin/env python3
"""Deterministic generalized-core extension probe, one witness per shape pair."""
from __future__ import annotations
from collections import Counter
from itertools import combinations, product
import json, sys
from pathlib import Path

from check_cycle72_general_core_feasibility import build

def shape(a): return tuple(sorted(Counter(a).values(), reverse=True))

def types(edges):
    alphabets=[]
    universe=set().union(*edges)
    for q in range(6):
        old=tuple(sorted(v for v in universe if v[0]==q))
        alphabets.append(old+((q,'fresh'),))
    return tuple(frozenset(x) for x in product(*alphabets) if all(len(frozenset(x)&e)==1 for e in edges))

def blocker(edges, line_types):
    vertices=tuple(sorted(set().union(*edges))); index={v:i for i,v in enumerate(vertices)}
    family=list(edges)+[frozenset(v for v in line if v in index) for line in line_types]
    coverage=[0]*len(vertices)
    for f,line in enumerate(family):
        for v in line: coverage[index[v]]|=1<<f
    full=(1<<len(family))-1
    for size in range(6):
        for choice in combinations(range(len(vertices)),size):
            value=0
            for v in choice:value|=coverage[v]
            if value==full:return [vertices[v] for v in choice]
    return None

def main():
    rows=[]
    for name in sys.argv[1:]: rows.extend(json.loads(Path(name).read_text())['rows'])
    selected={}
    for row in rows:
        if row['status']!='SAT':continue
        key=(shape(row['sides']),shape(row['central']))
        encoded=json.dumps(row,sort_keys=True)
        if key not in selected or encoded<selected[key][0]:selected[key]=(encoded,row)
    results=[]
    for key,(_,row) in sorted(selected.items()):
        edges=build(row);line_types=types(edges);cover=blocker(edges,line_types)
        results.append({'side_shape':key[0],'central_shape':key[1],'extension_types':len(line_types),'blocker':cover,'blocker_size':None if cover is None else len(cover)})
    print(json.dumps({'status':'PASS','epistemic_status':'OBSERVED','shape_pairs':len(results),'all_blocked':all(r['blocker_size'] is not None for r in results),'rows':results,'claim_boundary':'One deterministic representative per feasible partition-shape pair only; not a classification of all generalized equality cores.'},sort_keys=True))
if __name__=='__main__':main()
