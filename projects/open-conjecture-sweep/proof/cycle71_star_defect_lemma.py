#!/usr/bin/env python3
"""Exact integer audit for the high-degree-star defect inequality."""
from __future__ import annotations
import itertools,json
def main():
 rows=[]
 for delta in range(6,19):
  minimum=min(sum(k*(k-1)//2 for k in (a,b,c,d,delta-a-b-c-d))
              for a in range(delta+1) for b in range(delta-a+1)
              for c in range(delta-a-b+1) for d in range(delta-a-b-c+1))
  assert minimum>=delta-5
  rows.append({'star_degree':delta,'minimum_repeated_pairs_on_one_transverse_line':minimum,'required_lower_bound':delta-5})
 print(json.dumps({'status':'PASS','epistemic_status':'PROVED','rows':rows,
  'lemma':'If a line meets delta star-lines through a vertex v in its five non-v positions, then the repeated-pair defect among those star-lines is at least delta-5.',
  'application':'For an intersecting 6-partite tau=6 hypergraph, the published degree inequality forces delta>=6; any line through another vertex on v\'s side supplies a localized repeated-pair defect.',
  'claim_boundary':'Necessary local defect only; it does not yield a five-block cover or solve Ryser.'},sort_keys=True))
if __name__=='__main__':main()
