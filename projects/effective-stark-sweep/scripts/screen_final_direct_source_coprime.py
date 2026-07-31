#!/usr/bin/env python3
"""Exact final source-prime exclusion screen for B5-021 and B5-033."""
from __future__ import annotations
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; P=ROOT/"data/census-paper-preregistration-amendment-v16.json"; L=ROOT/"artifacts/engine-b-transport-ledger-v3.json"; W=ROOT/"artifacts/w1-full-census-v1.json"; O=ROOT/"artifacts/final-direct-source-coprime-screen-v1.json"
def h(x): return hashlib.sha256(x.read_bytes()).hexdigest()
def gp_screen(poly,a,b):
 q=f'''K=bnfinit({poly},1);F1=[{a[0][0]},{a[0][1]};{a[1][0]},{a[1][1]}];F2=[{b[0][0]},{b[0][1]};{b[1][0]},{b[1][1]}];Q=idealdiv(K,F2,F1);print("PRODUCT=",idealhnf(K,idealmul(K,F1,Q))==idealhnf(K,F2));print("COPRIME=",idealnorm(K,idealadd(K,F1,Q)));print("FACT=",idealfactor(K,Q));'''
 r=subprocess.run(["gp","-q"],input=q,text=True,cwd=ROOT,capture_output=True,check=True,timeout=600)
 return {x.split("=",1)[0]:x.split("=",1)[1] for x in r.stdout.splitlines() if "=" in x}
def main():
 if O.exists():raise RuntimeError("versioned output already exists")
 p=json.loads(P.read_text())
 for n,want in p["source_hashes"].items():
  if h(ROOT/n)!=want:raise RuntimeError(f"hash drift {n}")
 w={r["case_id"]:r for r in json.loads(W.read_text())["records"]}; members=json.loads(L.read_text())["members"]; out=[]
 for source in p["source_cases"]:
  data=json.loads((ROOT/source["data"]).read_text()); transcript=(ROOT/source["transcript"]).read_text()
  if data["verdict"]!="VERIFIED" or data["identification"]["claim_tag"]!="VERIFIED" or source["token"] not in transcript:raise RuntimeError("unsealed source")
  s=w[source["case_id"]]; targets=sorted([r for r in members if r["closure_id"]==source["closure_id"] and r["case_id"]!=source["case_id"]],key=lambda r:(r["finite_norm"],r["case_id"]))
  rs=[]
  for target in targets:
   t=w[target["case_id"]]; exact=gp_screen(source["field_polynomial"],s["finite_ideal_hnf"],t["finite_ideal_hnf"])
   rs.append({"case_id":target["case_id"],"finite_norm":target["finite_norm"],"exact":exact,"euler_deletion_route_eligible":exact["PRODUCT"]=="1" and exact["COPRIME"]=="1"})
  out.append({"source_case_id":source["case_id"],"closure_id":source["closure_id"],"records":rs,"eligible_count":sum(r["euler_deletion_route_eligible"] for r in rs)})
 if sum(x["eligible_count"] for x in out)!=0:raise RuntimeError("unexpected eligible target; requires a new frozen label screen")
 O.write_text(json.dumps({"schema":"effective-stark-final-direct-source-coprime-screen-v1","claim_tag":"PROVED_EXACT_TRANSPORT_GEOMETRY","claim_boundary":"exact source-prime exclusions only; no packet verdict for excluded targets","closures":out,"source_hashes":{str(x.relative_to(ROOT)):h(x) for x in(P,L,W,Path(__file__))}},indent=2,sort_keys=True)+"\n");print("FINAL_DIRECT_SOURCE_COPRIME_SCREEN=PASS")
if __name__=="__main__":main()
