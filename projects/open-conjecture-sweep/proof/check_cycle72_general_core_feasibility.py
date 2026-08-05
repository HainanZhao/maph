#!/usr/bin/env python3
"""Independently reconstruct and check all feasibility-scan witnesses."""
from __future__ import annotations
from itertools import combinations
import json, sys
from pathlib import Path

def build(row):
    sides=row['sides']; central=row['central']; pairs=[tuple(p) for p in row['pairs']]; maps=row['maps']; edges=[]
    for i in range(6):
        edge={(0,'v')}
        for q in range(5):
            r=[j for j in range(5) if sides[j]==q and i in pairs[j]]
            assert len(r)<=1
            edge.add((q+1,'r'+str(r[0]) if r else 'b%d_%d'%(q,i)))
        edges.append(frozenset(edge))
    for j in range(5):
        edge={(0,'c'+str(central[j]))}
        for q in range(5):
            indices=[i for i in range(6) if maps[j][i]==q]
            if q==sides[j]:
                assert sorted(indices)==sorted(pairs[j]); edge.add((q+1,'r'+str(j)))
            else:
                assert len(indices)==1; i=indices[0]
                assert not any(sides[k]==q and i in pairs[k] for k in range(5))
                edge.add((q+1,'b%d_%d'%(q,i)))
        edges.append(frozenset(edge))
    return tuple(edges)

def main():
    batches=[json.loads(Path(p).read_text()) for p in sys.argv[1:]]
    assert len(batches)==3 and all(b['status']=='DONE' for b in batches)
    rows=[r for b in batches for r in b['rows']]
    assert len(rows)==2704
    assert len({(tuple(r['sides']),tuple(r['central'])) for r in rows})==2704
    sat=[r for r in rows if r['status']=='SAT']
    for row in sat:
        edges=build(row)
        assert all(len(e)==6 and {q for q,_ in e}==set(range(6)) for e in edges)
        assert all(a & b for a,b in combinations(edges,2))
        assert all(len(edges[j]&edges[k])==1 for j in range(6,11) for k in range(6,j))
        assert sum(len(a&b)-1 for a,b in combinations(edges,2))==5
    print(json.dumps({'status':'PASS','epistemic_status':'PROVED','partition_pairs':len(rows),'sat_partition_pairs':len(sat),'pair_codes_checked':sum(b['pair_codes_checked'] for b in batches)},sort_keys=True))
if __name__=='__main__':main()
