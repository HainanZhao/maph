#!/usr/bin/env python3
"""Exact six-partition encoding of the published r=6 equality system."""
from __future__ import annotations
import itertools,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'discovery'))
from cycle69_r6_extremal_control import EDGES
def main():
    blocks=[]
    for part in range(1,7):
        groups={}
        for edge_id,edge in enumerate(EDGES):
            v=next(vertex for vertex in edge if vertex[0]==part)
            groups.setdefault(v[1],set()).add(edge_id)
        blocks.append(list(groups.values()))
    n=len(EDGES)
    assert all(any(any(i in b and j in b for b in partition) for partition in blocks) for i,j in itertools.combinations(range(n),2))
    all_blocks=[b for partition in blocks for b in partition]
    for k in range(1,7):
        if any(set().union(*(all_blocks[i] for i in choice))==set(range(n)) for choice in itertools.combinations(range(len(all_blocks)),k)):
            tau=k;break
    assert tau==5
    print(json.dumps({'status':'PASS','epistemic_status':'PROVED','points':n,'partitions':6,'blocks_per_partition':[len(p) for p in blocks],'pair_coclustering':'PASS','minimum_block_cover':tau,'claim_boundary':'Exact encoding of the published tau=5 equality system only; no universal six-partition theorem.'},sort_keys=True))
if __name__=='__main__':main()
