#!/usr/bin/env python3
"""Exact wild-C3 indecomposable-module lift test."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from verify_cycle_166_fibre_torsor import build_payload as torsor,shintani_step
def add(x,y):return((x[0]+y[0])%6,(x[1]+y[1])%6)
def solve(rows,n):
 p=3;r=0;piv=[]
 for c in range(n):
  q=next((i for i in range(r,len(rows)) if rows[i][c]%p),None)
  if q is None:continue
  rows[r],rows[q]=rows[q],rows[r];iv=pow(rows[r][c]%p,-1,p);rows[r]=[(v*iv)%p for v in rows[r]]
  for i in range(len(rows)):
   if i!=r and rows[i][c]%p: f=rows[i][c]%p;rows[i]=[(v-f*w)%p for v,w in zip(rows[i],rows[r],strict=True)]
  piv.append(c);r+=1
 return r,any(all(v%p==0 for v in row[:n]) and row[n]%p for row in rows)
def build_payload():
 t=torsor();points=sorted(tuple(x["characteristic"]) for x in t["multiplier_rows"]);idx={x:i for i,x in enumerate(points)};g={}
 for o in t["transport_orbits"]:g.update({tuple(x):v for x,v in zip(o["orbit"],o["lift_labels"],strict=True)})
 n=72;rows=[]
 def eq(terms,rhs=(0,0)):
  for coord in range(2):
   row=[0]*(n+1)
   for x,coefs in terms:row[2*idx[x]+coord]+=coefs[coord]
   row[-1]=rhs[coord];rows.append(row)
 for x in points: eq(((shintani_step(x),(1,0)),(x,(-1,0)))); eq(((shintani_step(x),(0,1)),(x,(-1,-1))))
 for x in ((0,0),(3,5),(3,4)):eq(((x,(1,0)),));eq(((x,(0,1)),))
 for x in points:
  for y in points:eq(((add(x,y),(1,0)),(x,(-1,0)),(y,(-1,0))),((0,(g[add(x,y)]-g[x]-g[y])%3)));eq(((add(x,y),(0,1)),(x,(0,-1)),(y,(0,-1))))
 rank,bad=solve(rows,n)
 return {"schema":"sic-stark-cycle-171-wild-c3-module-prototype-v1","epistemic_status":"PROVED","claim_boundary":"Finite wild C3-module test only.","summary":{"states":36,"module_dimension":2,"equations":len(rows),"rank":rank,"inconsistent":bad,"wild_module_lift_exists":not bad},"gate_outcome":{"wild_c3_module":"SURVIVES" if not bad else "FALSIFIED","scope":"canonical indecomposable F3[C3] module"}}
def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=Path);a=p.parse_args();s=json.dumps(build_payload(),indent=2,sort_keys=True)+"\n";a.output.write_text(s) if a.output else print(s,end="")
if __name__=="__main__":main()
