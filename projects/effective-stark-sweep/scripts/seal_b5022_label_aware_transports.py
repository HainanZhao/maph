#!/usr/bin/env python3
"""Seal B5-022 Euler-deletion transports with exact generator relabelling."""
from __future__ import annotations
import hashlib,itertools,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
G=ROOT/"artifacts/b5022-transport-geometry-v1.json";S=ROOT/"artifacts/b5022-source-certificate-integrity-v1.json";P=ROOT/"data/census-paper-preregistration-amendment-v14.json";D=ROOT/"docs/cycle-118-b5022-label-aware-transport-proof.md";W=ROOT/"artifacts/w1-full-census-v1.json";O=ROOT/"artifacts/b5022-label-aware-transports-v1.json"
def h(x):return hashlib.sha256(x.read_bytes()).hexdigest()
def factors(t):
 a=t["finite_ideal_hnf"]; q=f'''default(parisizemax,2000000000);
K=bnfinit(y^2-14,1);F1=[7,0;0,1];F2=[{a[0][0]},{a[0][1]};{a[1][0]},{a[1][1]}];Q=idealdiv(K,F2,F1);R=bnrinit(K,[F1,[1,0]],1);F=idealfactor(K,Q);
for(i=1,matsize(F)[1],{{print("E",i,"=",F[i,2]);print("L",i,"=",bnrisprincipal(R,F[i,1],0)[1]);}});
''';r=subprocess.run(["gp","-q"],input=q,text=True,cwd=ROOT,capture_output=True,check=True,timeout=600);v={x.split("=",1)[0]:int(x.split("=",1)[1]) for x in r.stdout.splitlines() if "=" in x};return [{"exponent":v[f"E{i}"],"source_ray_log":v[f"L{i}"]} for i in range(1,len(v)//2+1)]
def main():
 if O.exists():raise RuntimeError("versioned output already exists")
 if json.loads(S.read_text())["claim_tag"]!="VERIFIED_SEALED_SOURCE_CERTIFICATE_INTEGRITY":raise RuntimeError("source integrity missing")
 geo=json.loads(G.read_text());w={r["case_id"]:r for r in json.loads(W.read_text())["records"]}; rows=[r for r in geo["records"] if r["euler_deletion_route_eligible"]]
 expected=["RQ-000425","RQ-000436","RQ-000457","RQ-000459","RQ-000465"]
 if [r["case_id"] for r in rows]!=expected:raise RuntimeError("eligible set drift")
 out=[]
 for r in rows:
  fs=factors(w[r["case_id"]]); c=1 if r["exact"]["MAP"]=="Mat(1)" else 5
  if not fs:raise RuntimeError("missing factors")
  terms=[]
  for n in range(len(fs)+1):
   for sub in itertools.combinations(range(len(fs)),n):terms.append({"target_label_coefficient_to_source":c,"source_label_shift":(-sum(fs[i]["source_ray_log"] for i in sub))%6,"exponent":-1 if n%2 else 1})
  out.append({"case_id":r["case_id"],"source_case_id":"RQ-000419","closure_id":"B5-022","ray_map_generator_coefficient":c,"factors":fs,"artin_labelled_formula_terms":terms,"packet_relation":"label-aware Euler-deletion subset product of sealed RQ-000419 entries","orientation":"positive product/quotient at frozen split embedding","claim_tag":"PROVED_EXACT_MEMBER_TRANSPORT"})
 O.write_text(json.dumps({"schema":"effective-stark-b5022-label-aware-transports-v1","claim_tag":"PROVED_EXACT_MEMBER_TRANSPORT_BATCH","source_case_id":"RQ-000419","record_count":len(out),"records":out,"claim_boundary":"only five source-coprime B5-022 targets promoted; source-prime targets remain unpromoted","source_hashes":{str(x.relative_to(ROOT)):h(x) for x in(G,S,P,D,W,Path(__file__))}},indent=2,sort_keys=True)+"\n");print("B5022_LABEL_AWARE_TRANSPORTS=PASS")
if __name__=="__main__":main()
