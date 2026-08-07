#!/usr/bin/env python3
"""Independent bit-mask replay for C109's q=7 gate."""
from __future__ import annotations
import json
def quad(x,p):
 x%=p
 return 0 if x==0 else (1 if pow(x,(p-1)//2,p)==1 else -1)
def reciprocal(x,p): return 0 if x%p==0 else pow(x%p,p-2,p)
def main():
 p=7; nonres=[x for x in range(p) if quad(x,p)<0]; size=2*p; tally={};hits=[]
 for aa in nonres:
  for bb in nonres:
   for cc in nonres:
    for shift in range(p):
     for offset in range(p):
      rows=[0]*size
      for u in range(size):
       xu,lu=u%p,u//p
       for v in range(size):
        if u==v: continue
        xv,lv=v%p,v//p
        red=(quad((xu-xv)**2-(aa if lu==0 else bb),p)==1) if lu==lv else (quad((reciprocal(xu+shift,p)+offset-xv)**2-cc,p)==1 if lu==0 else quad((reciprocal(xv+shift,p)+offset-xu)**2-cc,p)==1)
        if red: rows[u]|=1<<v
      assert all(bool(rows[u]>>v&1)==bool(rows[v]>>u&1) for u in range(size) for v in range(size))
      mr=mb=0
      for u in range(size):
       for v in range(u+1,size):
        common=(rows[u]&rows[v]).bit_count()
        if rows[u]>>v&1: mr=max(mr,common)
        else: mb=max(mb,((~rows[u]&~rows[v]&((1<<size)-1)).bit_count()-2))
      tally[(mr,mb)]=tally.get((mr,mb),0)+1
      if mr<=2 and mb<=3:hits.append((aa,bb,cc,shift,offset))
 assert sum(tally.values())==1323
 print(json.dumps({"status":"PASS","q":p,"states":1323,"hits":hits,"profiles":sorted(([list(k),v] for k,v in tally.items()))},sort_keys=True))
if __name__=='__main__':main()
