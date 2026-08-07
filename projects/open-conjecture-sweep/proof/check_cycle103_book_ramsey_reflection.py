#!/usr/bin/env python3
"""Independent exact checker for the C103 dihedral six-block gate."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

PAIRS=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))
BASES=(("y",-1),("x",-1),("x",1),("x",-1),("x",-1),("y",1))

def character(a: int, p: int) -> int:
 a%=p
 return 0 if a==0 else (1 if pow(a,(p-1)//2,p)==1 else -1)

def blocks(p: int) -> tuple[list[list[int]],list[list[int]]]:
 # For p=7, 3 is a primitive root and 2=3^2 generates the square subgroup.
 m=(p-1)//2
 powers=[pow(2,k,p) for k in range(m)]
 a=[1]+[character(powers[k]-1,p) for k in range(1,m)]
 b=[character(t+1,p) for t in powers]
 return ([[a[(j-i)%m] for j in range(m)] for i in range(m)],
         [[b[(j-i)%m] for j in range(m)] for i in range(m)])

def sign(mask: int, bit: int) -> int:
 return 1 if mask>>bit&1 else -1

def row_filter(mask: int, p: int) -> bool:
 """Direct row-total calculation; R only permutes each inter-block row."""
 _,y=blocks(p); m=len(y); sy=sum(y[0])
 uv=sign(mask,0); u=[sign(mask,1+i) for i in range(4)]; v=[sign(mask,5+i) for i in range(4)]
 d=[sign(mask,9+i)*(1,-1,1,-1)[i] for i in range(4)]
 e=[sign(mask,13+i)*factor for i,(_,factor) in enumerate(BASES)]
 if uv+m*sum(u)!=-1 or uv+m*sum(v)!=-1: return False
 for g in range(4):
  total=u[g]+v[g]+d[g]*(sy-1)
  for k,(left,right) in enumerate(PAIRS):
   if g==left or g==right: total+=e[k]*(1 if BASES[k][0]=='x' else sy)
  if total!=-1: return False
 return True

def seidel(mask: int, reflection_mask: int, p: int) -> list[list[int]]:
 x,y=blocks(p); m=len(x); n=2+4*m; s=[[0]*n for _ in range(n)]
 s[0][1]=s[1][0]=sign(mask,0)
 for g in range(4):
  start=2+g*m
  for i in range(m):
   s[0][start+i]=s[start+i][0]=sign(mask,1+g)
   s[1][start+i]=s[start+i][1]=sign(mask,5+g)
  for i in range(m):
   for j in range(m):
    if i!=j: s[start+i][start+j]=sign(mask,9+g)*(1,-1,1,-1)[g]*y[i][j]
 for k,((left,right),(name,factor)) in enumerate(zip(PAIRS,BASES)):
  block=x if name=='x' else y; flip=reflection_mask>>k&1
  for i in range(m):
   for j in range(m):
    value=sign(mask,13+k)*factor*block[i][(-j if flip else j)%m]
    s[2+left*m+i][2+right*m+j]=value
    s[2+right*m+j][2+left*m+i]=value
 return s

def passes(mask: int, reflection_mask: int, p: int) -> bool:
 s=seidel(mask,reflection_mask,p); n=len(s)
 return (all(s[i][i]==0 and sum(s[i])==-1 for i in range(n)) and
         all(sum(s[i][k]*s[k][j] for k in range(n)) in (0,-4)
             for i in range(n) for j in range(i+1,n)))

def main() -> None:
 parser=argparse.ArgumentParser(); parser.add_argument('result',type=Path); args=parser.parse_args()
 recorded=json.loads(args.result.read_text())
 filtered=[m for m in range(1<<19) if row_filter(m,7)]
 hits=[(m,r) for m in filtered for r in range(64) if passes(m,r,7)]
 expected={'family':'fixed-six-block-19-sign-with-six-interblock-reflections',
           'logical_assignments':1<<25,'row_sum_masks':filtered,
           'seidel_checked_assignments':len(filtered)*64,'q7_hits':hits}
 if recorded!=expected: raise SystemExit('enumeration disagreement')
 print(json.dumps({'logical_assignments':1<<25,'row_sum_masks':len(filtered),
                   'seidel_checked_assignments':len(filtered)*64,'q7_hits':hits},sort_keys=True))

if __name__=='__main__': main()
