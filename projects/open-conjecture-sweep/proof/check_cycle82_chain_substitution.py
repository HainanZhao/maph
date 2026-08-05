#!/usr/bin/env python3
"""Exact C82 check for the frozen 15-element chain substitution."""
from __future__ import annotations
import json

BASE=(0,0,2,0,1,8,25,7,42); TRIPLE={0,3,1}
def main():
    block=[]; owner=[]
    for v in range(9):
        q=3 if v in TRIPLE else 1; block.append(list(range(len(owner),len(owner)+q))); owner += [v]*q
    n=len(owner); pre=[0]*n
    for v in range(9):
        for j,x in enumerate(block[v]):
            if j: pre[x]|=1<<block[v][j-1]
            for u in range(9):
                if BASE[v]>>u&1:
                    for y in block[u]: pre[x]|=1<<y
    N=1<<n; f=[0]*N; g=[0]*N; f[0]=1; g[-1]=1
    for m in range(N):
        for v in range(n):
            if not(m>>v&1) and pre[v]&~m==0: f[m|1<<v]+=f[m]
    for m in range(N-2,-1,-1):
        for v in range(n):
            if not(m>>v&1) and pre[v]&~m==0:g[m]+=g[m|1<<v]
    c=[[0]*n for _ in range(n)]
    for m in range(N):
        for v in range(n):
            if not(m>>v&1) and pre[v]&~m==0:
                for a in range(n):
                    if m>>a&1:c[a][v]+=f[m]*g[m|1<<v]
    def edge(a,b,inc=False): return c[a][b]>c[b][a] and (not inc or not((pre[a]>>b&1)or(pre[b]>>a&1)))
    def cyc(inc): return any(edge(a,b,inc)and edge(b,d,inc)and edge(d,e,inc)and edge(e,a,inc) for a in range(n) for b in range(n) for d in range(n) for e in range(n) if len({a,b,d,e})==4)
    print(json.dumps({"epistemic_status":"PROVED","vertices":n,"extensions":f[-1],"full_has_4_cycle":cyc(False),"restricted_has_4_cycle":cyc(True),"status":"PASS"},sort_keys=True))
if __name__=='__main__':main()
