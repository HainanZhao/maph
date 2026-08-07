#!/usr/bin/env python3
"""Exact F001 q=7 reflection extension of the D001 block template."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from cycle101_book_ramsey_completion import circulants, row_sum_ok, signs

PAIRS=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))

def valid(sign_mask:int, reflections:int, q:int=7)->bool:
 x,y=circulants(q); m=len(x); n=2+4*m; s=signs(sign_mask); z=[[0]*n for _ in range(n)]
 z[0][1]=z[1][0]=s[0]
 for g in range(4):
  a=2+g*m
  for t in range(m): z[0][a+t]=z[a+t][0]=s[1+g]; z[1][a+t]=z[a+t][1]=s[5+g]
  for r in range(m):
   for c in range(m):
    if r!=c:z[a+r][a+c]=s[9+g]*(1,-1,1,-1)[g]*y[r][c]
 bases=((y,-1),(x,-1),(x,1),(x,-1),(x,-1),(y,1))
 for k,((l,r),(b,f)) in enumerate(zip(PAIRS,bases)):
  a,c=2+l*m,2+r*m; e=(reflections>>k)&1
  for i in range(m):
   for j in range(m):
    v=s[13+k]*f*b[i][(-j if e else j)%m];z[a+i][c+j]=v;z[c+j][a+i]=v
 return all(sum(row)==-1 for row in z) and all(sum(z[i][k]*z[k][j] for k in range(n)) in (0,-4) for i in range(n) for j in range(i+1,n))

def search() -> dict[str, object]:
 masks=[a for a in range(1<<19) if row_sum_ok(a,7)]
 hits=[(a,b) for a in masks for b in range(64) if valid(a,b)]
 return {
  'family':'fixed-six-block-19-sign-with-six-interblock-reflections',
  'logical_assignments':1 << 25,
  'row_sum_masks':masks,
  'seidel_checked_assignments':len(masks)*64,
  'q7_hits':hits,
 }

def main():
 parser=argparse.ArgumentParser()
 parser.add_argument('--output',type=Path,required=True)
 args=parser.parse_args()
 args.output.parent.mkdir(parents=True,exist_ok=True)
 args.output.write_text(json.dumps(search(),indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
