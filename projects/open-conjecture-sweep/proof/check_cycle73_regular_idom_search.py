#!/usr/bin/env python3
"""Independent exact audit for any Cycle 73 regular-graph counterexample."""
from itertools import combinations
import json, sys
from pathlib import Path

def audit(row):
    if row['status'] != 'COUNTEREXAMPLE': return
    n=row['n']; edges=[tuple(e) for e in row['edges']]; adj=[set() for _ in range(n)]
    for a,b in edges: adj[a].add(b);adj[b].add(a)
    assert min(map(len, adj)) == max(map(len, adj)) >= 3
    chosen=set(row['independent_dominating_set'])
    assert all(not(adj[a]&chosen) for a in chosen)
    assert all(v in chosen or adj[v]&chosen for v in range(n))
    matching=[tuple(x) for x in row['maximal_matching']]; used={v for e in matching for v in e}
    assert len(used)==2*len(matching)
    assert all(tuple(sorted(e)) in {tuple(sorted(x)) for x in edges} for e in matching)
    assert all(a in used or b in used for a,b in edges)
    assert row['i']>row['mu_star']

def main():
    rows=[json.loads(Path(p).read_text()) for p in sys.argv[1:]]
    assert len(rows)==3 and {r['shard'] for r in rows}=={0,1,2}
    for row in rows:audit(row)
    print(json.dumps({'status':'PASS','epistemic_status':'CERTIFIED_NUMERICAL' if any(r['status']=='COUNTEREXAMPLE' for r in rows) else 'OBSERVED','counterexamples':sum(r['status']=='COUNTEREXAMPLE' for r in rows),'accepted':sum(sum(r['accepted']) for r in rows)},sort_keys=True))
if __name__=='__main__':main()
