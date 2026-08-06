#!/usr/bin/env python3
"""Exact edge-pair orbit audit behind C89's rank-one Hessian identity."""
from __future__ import annotations
import json

E = tuple((i, j) for j in range(5) for i in (j % 5, (j+1) % 5, (j+2) % 5))

def main():
    rows = {"shared_left": [], "shared_right": [], "disjoint": []}
    for e in E:
        for f in E:
            if e == f: continue
            rows["shared_left" if e[0] == f[0] else "shared_right" if e[1] == f[1] else "disjoint"].append((e,f))
    assert [len(rows[k]) for k in ("shared_left","shared_right","disjoint")] == [30,30,150]
    print(json.dumps({"status":"PASS","epistemic_status":"PROVED","edges":len(E),
      "ordered_pair_orbits":{k:len(v) for k,v in rows.items()},
      "claim_boundary":"This verifies only the combinatorial coefficients in the rank-one Hessian decomposition."},sort_keys=True))
if __name__ == "__main__": main()
