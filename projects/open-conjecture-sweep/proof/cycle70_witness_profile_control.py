#!/usr/bin/env python3
"""Exact deletion-witness profiles in the 13-edge r=6 equality control."""
from __future__ import annotations

import itertools
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'discovery'))
from cycle69_r6_extremal_control import EDGES, cover


def main():
    edges=[set(e) for e in EDGES]
    vertices=sorted(set().union(*edges))
    rows=[]
    for i,e in enumerate(edges):
        rest=edges[:i]+edges[i+1:]
        covers=[C for C in itertools.combinations(vertices,4) if cover(C,rest)]
        for C in covers:
            assert not(set(C)&e)
            multiplicities=tuple(sum(part==p for part,_ in C) for p in range(1,7))
            essentials=[]
            for c in C:
                family=[f for f in rest if set(f)&set(C)=={c}]
                assert family
                common=set(e)
                for f in family: common &= f
                essentials.append({"cover_vertex":c,"family_size":len(family),"common_e_vertices":sorted(common)})
            rows.append({"deleted_edge":i+1,"cover":C,"part_multiplicities":multiplicities,"essential":essentials})
    # For a minimum cover C of H-e, every cover vertex has an essential edge.
    # In a hypothetical tau>=6 counterexample, C has size five; if an essential
    # family had a common e vertex, replacing its cover vertex would give a five-cover of H.
    patterns={tuple(r['part_multiplicities']) for r in rows}
    print(json.dumps({"status":"PASS","epistemic_status":"PROVED","rows":rows,
      "observed_part_patterns":sorted(patterns),
      "general_lemma":"For a minimum cover C of H-e, each c in C has an edge meeting C exactly at c. If all such edges share v in e, then C-c+v covers H.",
      "claim_boundary":"The rows are an exact tau=5 control. They do not establish any profile restriction for hypothetical tau>=6 systems."},sort_keys=True))

if __name__=='__main__': main()
