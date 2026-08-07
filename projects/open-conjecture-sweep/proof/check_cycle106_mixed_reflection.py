#!/usr/bin/env python3
"""Exact C106 mixed-reflection zero-mode and non-complement controls."""
from __future__ import annotations
import json

def mul(x,y,q):return ((x[0]+(-1 if x[1] else 1)*y[0])%q,(x[1]+y[1])%2)
def control(q,A,B):
 G=[(a,b) for a in range(q) for b in range(2)];ix={g:i for i,g in enumerate(G)};C={(a,0) for a in A}|{(b,1) for b in B};n=2*q
 M=[[0]*n for _ in G]
 for i,g in enumerate(G):
  for h in C:M[i][ix[mul(g,h,q)]]=1
 S=[[0 if i==j else 1-2*M[i][j] for j in range(n)] for i in range(n)]
 co={g:sum(mul(x,y,q)==g for x in C for y in C) for g in G}
 formula=all(sum(S[0][k]*S[ix[g]][k] for k in range(n))==-2*q-2+4*((g in C)+co[g]) for g in G if g!=(0,0))
 Q=[sum((x in A and (t-x)%q in B) for x in range(q)) for t in range(q)]
 reflection=all(co[(t,1)]==2*Q[t] for t in range(q))
 h=(q+1)//4
 equivalence=all((sum(S[0][k]*S[ix[(t,1)]][k] for k in range(n)) in (0,-4)) == (Q[t]+(t in B)==h) for t in range(q))
 return {"q":q,"A":sorted(A),"B":sorted(B),"degree":len(C),"non_complement":B != set(range(q))-A,"seidel_formula_agrees":formula,"reflection_convolution_agrees":reflection,"reflection_equivalence":equivalence}
def symbolic(q):
 h=(q+1)//4; roots=[b for b in range(q+1) if b*b-(q+1)*b+q*h==0]
 square=next((m*m for m in range(q+2) if m*m==q+1),None)
 return {"q":q,"h":h,"roots":roots,"q_plus_one_square":square}
def prime_power(q):
 for p in range(2,q+1):
  if q%p==0:
   if any(p%d==0 for d in range(2,p)): return False
   while q%p==0:q//=p
   return q==1
 return False
def main():
 rows=[symbolic(q) for q in range(7,400,8) if prime_power(q)]
 assert all(x["q_plus_one_square"] is None for x in rows)
 controls=[control(7,{1,6},{0,1,2,3,4}),control(23,{1,22},set(range(23))-{0,2})]
 assert all(x["non_complement"] and x["seidel_formula_agrees"] and x["reflection_convolution_agrees"] and x["reflection_equivalence"] for x in controls)
 print(json.dumps({"status":"PASS","symbolic":rows,"controls":controls},sort_keys=True))
if __name__=="__main__":main()
