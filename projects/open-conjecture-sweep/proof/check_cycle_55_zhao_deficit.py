#!/usr/bin/env python3
"""Audit Cycle 55's frozen exact S3 conjugacy-deficit packet."""
from __future__ import annotations
import csv,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/"discovery/out/cycle55-zhao-deficit"
CL=(0,1,1,2,2,1)
def rows(name):
 with (OUT/name).open() as f:return list(csv.DictReader(f,delimiter="\t"))
def audit():
 p=json.loads((OUT/"summary.json").read_text());q=json.loads((OUT/"independent-summary.json").read_text());a,b=rows("rays.tsv"),rows("independent-rays.tsv")
 assert p["status"]==q["status"]=="PASS" and (p["directions"],p["polynomials"],p["rays"],p["negative_rays"])==(10,80,1360,0)
 assert q["rays"]==1360 and q["negative_rays"]==0 and q["direct_control"]=="PASS"
 assert sorted(tuple(x.items()) for x in a)==sorted(tuple(x.items()) for x in b)
 assert all(int(x["sign"])>=0 for x in a)
 for r in rows("polynomials.tsv"):
  d=[int(x) for x in r["direction"].split(",")];c=[int(x) for x in r["base"].split(",")]
  assert math.gcd(*(abs(x) for x in d if x))==1 and next(x for x in d if x)<0
  assert all(sum(d[z] for z in range(6) if CL[z]==cl)==0 for cl in range(3))
  assert len(r["deficit_coefficients"].split(","))==16 and len(c)==3
 return {"status":"PASS","epistemic_status":"PROVED","directions":10,"polynomials":80,"rays":1360,"negative_rays":0,"claim_boundary":"Exact frozen S3 class-zero ray packet only; neither Zhao's all-group comparison nor Sidorenko."}
if __name__=="__main__":print(json.dumps(audit(),sort_keys=True))
