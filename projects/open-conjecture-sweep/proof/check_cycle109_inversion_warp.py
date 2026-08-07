#!/usr/bin/env python3
"""Exact q=7 gate for C109 inversion-warped character states."""
from __future__ import annotations
import json

def chi(a,q):
 a%=q
 return 0 if not a else (1 if pow(a,(q-1)//2,q)==1 else -1)
def inv(a,q): return 0 if a%q==0 else pow(a%q,q-2,q)
def graph(q,a0,a1,c,t,z):
 N=2*q; A=[[False]*N for _ in range(N)]
 for i in range(N):
  x,l=i%q,i//q
  for j in range(i+1,N):
   y,m=j%q,j//q
   red=chi((x-y)*(x-y)-(a0 if l==0 else a1),q)==1 if l==m else chi((inv(x+t,q)+z-y)**2-c,q)==1
   A[i][j]=A[j][i]=red
 return A
def profile(A,q):
 N=len(A); rcap=(q-3)//2;bcap=(q-1)//2; worst=[0,0]
 for i in range(N):
  for j in range(i+1,N):
   cn=sum(A[i][k]==A[i][j] and A[j][k]==A[i][j] for k in range(N) if k not in (i,j))
   if A[i][j]:worst[0]=max(worst[0],cn)
   else:worst[1]=max(worst[1],cn)
 return worst[0]<=rcap and worst[1]<=bcap,tuple(worst)
def main():
 q=7; ns=[a for a in range(q) if chi(a,q)==-1]; hits=[]; tested=0; worst={}
 for a0 in ns:
  for a1 in ns:
   for c in ns:
    for t in range(q):
     for z in range(q):
      tested+=1; ok,p=profile(graph(q,a0,a1,c,t,z),q); worst[p]=worst.get(p,0)+1
      if ok:hits.append((a0,a1,c,t,z))
 assert tested==1323
 print(json.dumps({"status":"PASS","q":q,"states":tested,"hits":hits,"profiles":sorted(([list(k),v] for k,v in worst.items()))},sort_keys=True))
if __name__=='__main__':main()
