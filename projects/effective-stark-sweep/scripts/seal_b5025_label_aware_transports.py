#!/usr/bin/env python3
"""Seal the two B5-025 Mat(5) Euler-deletion transports."""
from __future__ import annotations
import hashlib,itertools,json,subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"data/census-paper-preregistration-amendment-v17.json"
G=ROOT/"artifacts/b5025-transport-geometry-v1.json"
W=ROOT/"artifacts/w1-full-census-v1.json"
D=ROOT/"docs/cycle-125-b5025-label-aware-proof.md"
O=ROOT/"artifacts/b5025-label-aware-transports-v1.json"
def h(x): return hashlib.sha256(x.read_bytes()).hexdigest()

def factor_logs(target):
 a=target["finite_ideal_hnf"]
 q=f'''default(parisizemax,2000000000);
K=bnfinit(y^2-7,1);F1=[7,0;0,1];F2=[{a[0][0]},{a[0][1]};{a[1][0]},{a[1][1]}];Q=idealdiv(K,F2,F1);R=bnrinit(K,[F1,[1,0]],1);F=idealfactor(K,Q);
for(i=1,matsize(F)[1],{{print("E",i,"=",F[i,2]);print("L",i,"=",bnrisprincipal(R,F[i,1],0)[1]);}});
'''
 r=subprocess.run(["gp","-q"],input=q,text=True,cwd=ROOT,capture_output=True,check=True,timeout=600)
 v={x.split("=",1)[0]:int(x.split("=",1)[1]) for x in r.stdout.splitlines() if "=" in x}
 return [{"exponent":v[f"E{i}"],"source_ray_log":v[f"L{i}"]} for i in range(1,len(v)//2+1)]

def main():
 if O.exists():raise RuntimeError("versioned output already exists")
 p=json.loads(P.read_text())
 for name,want in p["source_hashes"].items():
  if h(ROOT/name)!=want:raise RuntimeError(f"hash drift {name}")
 source=json.loads((ROOT/"data/q7-p7-case-v1.json").read_text()); transcript=(ROOT/"artifacts/q7-p7-w3-arb-certificate-v1.txt").read_text()
 if source["w3"]["packet_identity_verdict"]!="VERIFIED" or "Q7_P7_PACKET_IDENTITY_VERIFIED=1" not in transcript:raise RuntimeError("sealed source missing")
 geo={r["case_id"]:r for r in json.loads(G.read_text())["records"]}; w={r["case_id"]:r for r in json.loads(W.read_text())["records"]}
 ids=p["selection"]; out=[]
 for ident in ids:
  r=geo[ident]; e=r["exact"]
  if not (e["IDEAL_PRODUCT_MATCH"]=="1" and e["QUOTIENT_COPRIME_NORM"]=="1" and e["SOURCE_CYC"]=="[6]" and e["TARGET_CYC"]=="[6]" and e["MAP_IDENTITY"]=="[0]" and e["MAP_SIGN"]=="[3]" and e["MAP_MATRIX"]=="Mat(5)"):raise RuntimeError(f"geometry gate failed {ident}")
  fs=factor_logs(w[ident])
  if len(fs)!=1:raise RuntimeError(f"unexpected distinct-prime count {ident}")
  terms=[]
  for n in range(2):
   for subset in itertools.combinations(range(len(fs)),n):
    terms.append({"target_label_coefficient_to_source":5,"source_label_shift":(-sum(fs[i]["source_ray_log"] for i in subset))%6,"exponent":-1 if n else 1})
  out.append({"case_id":ident,"source_case_id":"RQ-000190","closure_id":"B5-025","ray_map_generator_coefficient":5,"factors":fs,"artin_labelled_formula_terms":terms,"packet_relation":"label-aware Euler-deletion subset product of sealed RQ-000190 entries","orientation":"positive product/quotient at frozen split embedding","claim_tag":"PROVED_EXACT_MEMBER_TRANSPORT"})
 O.write_text(json.dumps({"schema":"effective-stark-b5025-label-aware-transports-v1","claim_tag":"PROVED_EXACT_MEMBER_TRANSPORT_BATCH","source_case_id":"RQ-000190","record_count":len(out),"records":out,"claim_boundary":"only the two source-coprime Mat(5) B5-025 targets are promoted; source-prime targets remain unpromoted","source_hashes":{str(x.relative_to(ROOT)):h(x) for x in(P,G,W,D,Path(__file__))}},indent=2,sort_keys=True)+"\n")
 print("B5025_LABEL_AWARE_TRANSPORTS=PASS")
if __name__=="__main__":main()
