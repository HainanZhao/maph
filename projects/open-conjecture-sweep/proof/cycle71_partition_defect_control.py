#!/usr/bin/env python3
"""Measure repeated pair co-clustering in the 13-edge equality control."""
from __future__ import annotations
import collections,itertools,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'discovery'))
from cycle69_r6_extremal_control import EDGES
def main():
 m=collections.Counter()
 for a,b in itertools.combinations(range(len(EDGES)),2):
  m[sum(bool(set(EDGES[a])&set(EDGES[b]) & {(p,q) for p,q in set(EDGES[a])&set(EDGES[b])}) for _ in [0])]+=1
 # The direct cardinality is the number of partition blocks co-containing a,b.
 counts=collections.Counter(len(set(EDGES[a])&set(EDGES[b])) for a,b in itertools.combinations(range(len(EDGES)),2))
 assert sum(counts.values())==78 and min(counts)==1
 print(json.dumps({'status':'PASS','epistemic_status':'PROVED','pair_coclustering_multiplicities':dict(sorted(counts.items())),'repeated_pair_defect':sum((k-1)*v for k,v in counts.items()),'claim_boundary':'Exact defect statistic of the published tau=5 equality control only; no defect-to-cover inequality is proved.'},sort_keys=True))
if __name__=='__main__':main()
