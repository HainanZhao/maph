#!/usr/bin/env python3
"""Exact C83 interval-conditioned-majority control."""
from __future__ import annotations
import json
from check_cycle83_tip_fibers import BASE, closure, c82_predecessors

def run(pre, queries):
    n=len(pre); out=[]; order=[]
    for q in queries: out.append([0,0,0,0])
    total=0
    def go(mask):
        nonlocal total
        if len(order)==n:
            total+=1; p=[0]*n
            for i,v in enumerate(order):p[v]=i
            for r,(x,y,z,w) in zip(out,queries):
                r[0]+=p[z]<p[w]
                if p[x]<p[z]<p[y] and p[x]<p[w]<p[y]:
                    r[1]+=1; r[2]+=p[z]<p[w]; r[3]+=p[w]<p[z]
            return
        for v in range(n):
            if not(mask>>v&1) and pre[v]&~mask==0:
                order.append(v);go(mask|1<<v);order.pop()
    go(0)
    return total,out

def main():
    c=closure(list(BASE)); q81=[]
    for y in range(9):
        for x in range(9):
            if c[y]>>x&1:
                rest=[v for v in range(9) if v not in (x,y)]
                q81 += [(x,y,z,w) for z in rest for w in rest if z!=w]
    q82=[(x,y,10,11) for x,y in ((0,1),(1,2),(3,4),(4,5),(7,8),(8,9))]
    e81,r81=run(list(BASE),q81);e82,r82=run(c82_predecessors(),q82)
    assert e81==1431 and e82==571725
    nonempty=[r for r in r81+r82 if r[1]]
    reversed_rows=sum(r[0]*2>e81 and r[3]>r[2] for r in r81 if r[1]) + sum(r[0]*2>e82 and r[3]>r[2] for r in r82 if r[1])
    print(json.dumps({"epistemic_status":"PROVED","c81_queries":len(q81),"c82_queries":len(q82),"nonempty_fibers":len(nonempty),"reversed_rows":reversed_rows,"status":"PASS"},sort_keys=True))
if __name__=='__main__':main()
