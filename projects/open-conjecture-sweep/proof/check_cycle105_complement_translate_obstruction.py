#!/usr/bin/env python3
"""Independent scalar/matrix checker for C105."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def prod(g,h,p): return ((g[0]+(1 if g[1]==0 else -1)*h[0])%p,(g[1]+h[1])%2)
def check_control(p,A):
 E=[(a,b) for b in range(2) for a in range(p)]; ix={g:i for i,g in enumerate(E)}; B=set(range(p))-set(A); D={(a,0) for a in A}|{(a,1) for a in B}; n=len(E)
 W=[[0]*n for _ in E]
 for i,g in enumerate(E):
  for h in D:W[i][ix[prod(g,h,p)]]=1
 T=[[0 if i==j else 1-2*W[i][j] for j in range(n)] for i in range(n)]
 co={g:0 for g in E}
 for x in D:
  for y in D:co[prod(x,y,p)]+=1
 formula=True
 for j,g in enumerate(E):
  if g!=(0,0): formula &= sum(T[0][k]*T[j][k] for k in range(n)) == -2*p-2+4*((g in D)+co[g])
 parity=all(sum((x in A and (x-t)%p in A) for x in range(p))%2 == (((t*pow(2,-1,p))%p) in A) for t in range(1,p))
 return {"q":p,"A":sorted(A),"degree":len(D),"seidel_formula_agrees":formula,"parity_pairing_agrees":parity}
def main():
 p=argparse.ArgumentParser();p.add_argument("result",type=Path);a=p.parse_args();out=json.loads(a.result.read_text())
 controls=[check_control(q,{1,(-1)%q}) for q in (7,23)]+[check_control(q,set()) for q in (7,23)]
 roots=[[k for k in range(q+1) if 4*k*k-4*q*k+q*q-1==0] for q in (7,23)]
 expected={"family":"dihedral-complement-translate-autocorrelation","scalar":[{"q":q,"quadratic_roots":r,"symmetric_nonzero_root":(q+1)//2,"forced_autocorrelation":(q+1)//4,"forced_autocorrelation_even":True} for q,r in zip((7,23),roots)],"controls":controls}
 if out!=expected:raise SystemExit("route disagreement")
 print(json.dumps({"status":"PASS","controls":4,"q_values":[7,23],"roots":roots},sort_keys=True))
if __name__=="__main__":main()
