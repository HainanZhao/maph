from __future__ import annotations
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'discovery/out/cycle57-conditional-variance'
def audit():
 rows=list(csv.DictReader(open(OUT/'s3-c3-polynomial.tsv'),delimiter='\t'));x={(int(r['a']),int(r['b']),int(r['c']),int(r['t'])):int(r['coefficient']) for r in rows};d=json.load(open(OUT/'handelman-discovery.json'))
 assert x[(3,6,4,2)]==-35400 and d['success'] is False and d['dual_success'] is True
 return {'status':'PASS','epistemic_status':'PROVED','target_coefficient':-35400,'dual_coordinate':[3,6,4,2],'claim_boundary':'Exact no-go only for the frozen 756-column homogeneous positive-monomial Handelman cone.'}
if __name__=='__main__':print(json.dumps(audit(),sort_keys=True))
