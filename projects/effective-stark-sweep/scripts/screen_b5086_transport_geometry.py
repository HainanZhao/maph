#!/usr/bin/env python3
"""Fresh exact B5-086 (cyclic order-ten) transport-geometry screen."""
from __future__ import annotations
import hashlib, json, subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"data/census-paper-preregistration-amendment-v15.json"
L=ROOT/"artifacts/engine-b-transport-ledger-v3.json"
W=ROOT/"artifacts/w1-full-census-v1.json"
O=ROOT/"artifacts/b5086-transport-geometry-v1.json"
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
 if O.exists(): raise RuntimeError("versioned output already exists")
 p=json.loads(P.read_text())
 for n,x in p["source_hashes"].items():
  if h(ROOT/n)!=x: raise RuntimeError(f"hash drift {n}")
 w={r["case_id"]:r for r in json.loads(W.read_text())["records"]}
 members=json.loads(L.read_text())["members"]; s=w["RQ-001107"]
 targets=sorted([r for r in members if r["closure_id"]=="B5-086" and r["case_id"]!="RQ-001107"],key=lambda r:(r["finite_norm"],r["case_id"]))
 if len(targets)!=7: raise RuntimeError("target set drift")
 records=[]
 for m in targets:
  t=w[m["case_id"]]; a=s["finite_ideal_hnf"]; b=t["finite_ideal_hnf"]
  g=f'''default(parisizemax,2000000000);
K=bnfinit(y^2-33,1);
F1=[{a[0][0]},{a[0][1]};{a[1][0]},{a[1][1]}];
F2=[{b[0][0]},{b[0][1]};{b[1][0]},{b[1][1]}];
Q=idealdiv(K,F2,F1);
R1=bnrinit(K,[F1,[1,0]],1); R2=bnrinit(K,[F2,[1,0]],1); M=bnrmap(R2,R1);
S1=bnrisprincipal(R1,idealhnf(K,{s['sign_generator']}),0)[1]; S2=bnrisprincipal(R2,idealhnf(K,{t['sign_generator']}),0)[1];
print("PRODUCT=",idealhnf(K,idealmul(K,F1,Q))==idealhnf(K,F2));
print("COPRIME=",idealnorm(K,idealadd(K,F1,Q)));
print("C1=",Vec(R1.cyc)); print("C2=",Vec(R2.cyc)); print("MAP=",M[1]);
print("S1=",S1); print("S2=",S2); print("MI=",bnrmap(M,[0])); print("MG=",bnrmap(M,[1])); print("MS=",bnrmap(M,[S2])); print("FACT=",idealfactor(K,Q));
'''
  r=subprocess.run(["gp","-q"],input=g,text=True,cwd=ROOT,capture_output=True,check=True,timeout=600)
  v={x.split("=",1)[0]:x.split("=",1)[1] for x in r.stdout.splitlines() if "=" in x}
  good=(v["PRODUCT"]=="1" and v["COPRIME"]=="1" and v["C1"]=="[10]" and v["C2"]=="[10]" and v["MI"]=="[0]" and v["MS"]=="[5]")
  records.append({"case_id":m["case_id"],"finite_norm":m["finite_norm"],"exact":v,"euler_deletion_route_eligible":good})
 out={"schema":"effective-stark-b5086-transport-geometry-v1","claim_tag":"PROVED_EXACT_TRANSPORT_GEOMETRY","source_case_id":"RQ-001107","records":records,"eligible_count":sum(x["euler_deletion_route_eligible"] for x in records),"source_hashes":{str(x.relative_to(ROOT)):h(x) for x in(P,L,W,Path(__file__))}}
 O.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n"); print("B5086_TRANSPORT_GEOMETRY=PASS")
if __name__=="__main__": main()
