"""Exact Pólya cap test derived from C57's verified sparse polynomial."""
from __future__ import annotations
import csv,json,math
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'discovery/out/cycle59-polya';SRC=ROOT/'discovery/out/cycle57-conditional-variance/s3-c3-polynomial.tsv'
# variables are x,y,u,v.  C=(u+v)/2 and t=(v-u)/2; D/t^2 has degree 13.
R=defaultdict(int)
for r in csv.DictReader(open(SRC),delimiter='\t'):
 a,b,c,t,q=map(int,(r['a'],r['b'],r['c'],r['t'],r['coefficient']))
 assert t>=2 and t%2==0
 # 2^13 * A^a B^b C^c t^(t-2), expanded in u,v.
 d=t-2
 for i in range(c+1):
  for j in range(d+1):
   # (u+v)^c (v-u)^d; total denominator 2^(c+d).
   coef=q*math.comb(c,i)*math.comb(d,j)*(-1)**(d-j)*(2**(13-c-d))
   R[(a,b,i+d-j,c-i+j)]+=coef
assert all(v==int(v) for v in R.values())
def muls(p):
 q=defaultdict(int)
 for e,v in p.items():
  for k in range(4):
   f=list(e);f[k]+=1;q[tuple(f)]+=v
 return {e:v for e,v in q.items() if v}
p=dict(R);rows=[]
for K in range(25):
 neg=sum(v<0 for v in p.values());rows.append({'K':K,'terms':len(p),'negative_coefficients':neg})
 if not neg:break
 p=muls(p)
OUT.mkdir(parents=True,exist_ok=True);(OUT/'summary.json').write_text(json.dumps({'status':'PASS','scale':'2^13 R','rows':rows},indent=2)+'\n');print(json.dumps(rows[-1]))
