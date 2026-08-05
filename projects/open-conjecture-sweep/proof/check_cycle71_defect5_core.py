#!/usr/bin/env python3
"""Independent checker for a D=5 equality-core CSP assignment."""
from __future__ import annotations
import json,sys
from pathlib import Path
def main(path:Path):
 p=json.loads(path.read_text());assert p['status']=='SAT'
 pairs=[tuple(x) for x in p['pairs']];maps=p['maps'];assert len(pairs)==len(maps)==5
 assert all(0<=a<b<6 for a,b in pairs)
 for j,m in enumerate(maps):
  assert len(m)==6 and all(0<=q<5 for q in m)
  for i,q in enumerate(m):
   if i in pairs[j]:assert q==j
   else:assert q!=j and i not in pairs[q]
 for j in range(5):
  for k in range(j):assert sum(a==b for a,b in zip(maps[j],maps[k]))==1
 print(json.dumps({'status':'PASS','epistemic_status':'PROVED','claim':'The supplied 11-edge D=5 equality-core assignment satisfies every frozen partition constraint.','claim_boundary':'Core realization only; tau=6 is not asserted.'},sort_keys=True))
if __name__=='__main__':main(Path(sys.argv[1]))
