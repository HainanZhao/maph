"""Floating support discovery for C57's frozen homogeneous certificate cone."""
from __future__ import annotations
import csv,json,math
from collections import defaultdict
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/"discovery/out/cycle57-conditional-variance"
target=defaultdict(int)
for r in csv.DictReader(open(OUT/'s3-c3-polynomial.tsv'),delimiter='\t'):
 target[tuple(map(int,(r['a'],r['b'],r['c'],r['t'])))]+=int(r['coefficient'])
keys=sorted(target);cols=[]
for i in range(7):
 for j in range(7-i):
  d=13-2*i-2*j
  for ae in range(d+1):
   for at in range(d-ae+1):
    ac=d-ae-at;v=defaultdict(int)
    for k in range(j+1):v[(ae,at,ac+2*(j-k),2*i+2+2*k)]+=(-1)**k*math.comb(j,k)
    cols.append(v)
allkeys=sorted(set(keys)|{x for v in cols for x in v});A=np.array([[v.get(k,0) for v in cols] for k in allkeys],float);b=np.array([target.get(k,0) for k in allkeys],float)
res=linprog(np.ones(len(cols)),A_eq=A,b_eq=b,bounds=(0,None),method='highs')
OUT.mkdir(exist_ok=True,parents=True);data={'status':res.message,'success':bool(res.success),'columns':len(cols),'rows':len(allkeys)}
if res.success:
 data['support']=[(n,round(float(x),12)) for n,x in enumerate(res.x) if x>1e-9]
else:
 # Farkas normalization: y.A >= 0 and y.b = -1.  Split the free y.
 m=len(allkeys); dual=linprog(np.ones(2*m),A_ub=-np.hstack((A.T,-A.T)),b_ub=np.zeros(len(cols)),A_eq=np.array([np.r_[b,-b]]),b_eq=np.array([-1.]),bounds=(0,None),method='highs')
 data['dual_success']=bool(dual.success)
 if dual.success:data['dual']=[round(float(x),12) for x in dual.x[:m]-dual.x[m:]]
(OUT/'handelman-discovery.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps({'success':data['success'],'columns':len(cols),'rows':len(allkeys),'support':len(data.get('support',[]))}))
