#!/usr/bin/env python3
"""Exact C105 group-ring controls for the complement-translate transition."""
from __future__ import annotations
import argparse, json
from pathlib import Path

def mul(x,y,q): return ((x[0]+(-1 if x[1] else 1)*y[0])%q,(x[1]+y[1])%2)
def inv(x,q): return ((-x[0] if not x[1] else x[0])%q,x[1])
def symmetric(seed,q): return {a%q for a in seed}|{(-a)%q for a in seed}

def control(q,A):
    G=[(a,b) for a in range(q) for b in range(2)]; pos={g:i for i,g in enumerate(G)}
    B=set(range(q))-A; C={(a,0) for a in A}|{(b,1) for b in B}; n=2*q
    M=[[0]*n for _ in G]
    for i,g in enumerate(G):
        for h in C:M[i][pos[mul(g,h,q)]]=1
    S=[[0 if i==j else 1-2*M[i][j] for j in range(n)] for i in range(n)]
    conv={g:sum(mul(x,y,q)==g for x in C for y in C) for g in G}
    formula=all(sum(S[0][k]*S[pos[g]][k] for k in range(n)) == (-2*q-2+4*((1 if g in C else 0)+conv[g])) for g in G if g!=(0,0))
    parity=all(sum(1 for x in A if (x-t)%q in A)%2 == (1 if (t*pow(2,-1,q))%q in A else 0) for t in range(1,q))
    return {"q":q,"A":sorted(A),"degree":len(C),"seidel_formula_agrees":formula,"parity_pairing_agrees":parity}

def scalar(q):
    roots=[k for k in range(q+1) if k*(k-1)==(q-1)*(k-(q+1)//4)]
    return {"q":q,"quadratic_roots":roots,"symmetric_nonzero_root":(q+1)//2,"forced_autocorrelation":(q+1)//4,"forced_autocorrelation_even":((q+1)//4)%2==0}

def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True);a=p.parse_args()
 rows=[control(q,symmetric({1},q)) for q in (7,23)]+[control(q,set()) for q in (7,23)]
 data={"family":"dihedral-complement-translate-autocorrelation","scalar":[scalar(q) for q in (7,23)],"controls":rows}
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n")
if __name__=="__main__":main()
