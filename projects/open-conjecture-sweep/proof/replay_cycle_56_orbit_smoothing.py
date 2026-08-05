#!/usr/bin/env python3
"""Independent reverse-order exact S3 orbit-smoothing replay."""
from __future__ import annotations
import json
from itertools import permutations
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/"discovery/out/cycle56-orbit-smoothing"
P=list(permutations(range(3)));IX={p:i for i,p in enumerate(P)}
M=[[IX[tuple(P[i][P[j][k]] for k in range(3))] for j in range(6)] for i in range(6)]
IV=[next(j for j in range(6) if M[i][j]==M[j][i]==0) for i in range(6)]
CL=[]
for i in range(6):
 z=i;n=1
 while z:z=M[z][i];n+=1
 CL.append(0 if n==1 else 1 if n==2 else 2)
E=((2,3,4),(0,3,4),(0,1,4),(0,1,2),(1,2,3))
def num(a):
 total=0
 for x1 in range(6):
  for x2 in range(6):
   for x3 in range(6):
    for x4 in range(6):
     x=(0,x1,x2,x3,x4);v=1
     for nb in E:
      s=0
      for y in range(6):
       z=1
       for i in nb:z*=a[M[IV[x[i]]][y]]
       s+=z
      v*=s
     total+=v
 return total
def run():
 rows=[];neg=0
 for code in range(728,-1,-1):
  z=code;a=[]
  for _ in range(6):a.append(z%3);z//=3
  n=num(a)
  for cl in (2,1):
   den=2 if cl==2 else 3;sm=sum(a[i] for i in range(6) if CL[i]==cl)
   b=[sm if CL[i]==cl else den*a[i] for i in range(6)]
   d=n*den**15-num(b);s=(d>0)-(d<0);neg+=s<0;rows.append((code,cl,s))
 OUT.mkdir(parents=True,exist_ok=True)
 with (OUT/"independent-rows.tsv").open("w") as f:
  f.write("code\tclass\tsign\n");f.writelines(f"{c}\t{k}\t{s}\n" for c,k,s in rows)
 result={"status":"PASS","rows":len(rows),"negative_rows":neg};(OUT/"independent-summary.json").write_text(json.dumps(result)+"\n");return result
if __name__=="__main__":print(json.dumps(run(),sort_keys=True))
