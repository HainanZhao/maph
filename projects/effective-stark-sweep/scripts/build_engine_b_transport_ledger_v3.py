#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];P=ROOT/"artifacts/engine-b-transport-ledger-v2.json";B=ROOT/"artifacts/b5022-label-aware-transports-v1.json";O=ROOT/"artifacts/engine-b-transport-ledger-v3.json"
def h(x):return hashlib.sha256(x.read_bytes()).hexdigest()
def main():
 if O.exists():raise RuntimeError("versioned output already exists")
 p=json.loads(P.read_text());b=json.loads(B.read_text())
 if p["counts"]["member_transport_completed"]!=5 or b["claim_tag"]!="PROVED_EXACT_MEMBER_TRANSPORT_BATCH":raise RuntimeError("predecessor drift")
 d={x["case_id"]:x for x in b["records"]};want=["RQ-000425","RQ-000436","RQ-000457","RQ-000459","RQ-000465"]
 if sorted(d)!=want:raise RuntimeError("batch drift")
 rows=[]
 for r in p["members"]:
  x=dict(r)
  if x["case_id"] in d:x.update({"transport_status":"PROVED_EXACT_MEMBER_TRANSPORT","transport_certificate":str(B.relative_to(ROOT)),"source_case_id":"RQ-000419","packet_relation":d[x["case_id"]]["packet_relation"],"artin_labelled_formula_terms":d[x["case_id"]]["artin_labelled_formula_terms"]})
  rows.append(x)
 c=[x for x in rows if x["transport_status"]=="PROVED_EXACT_MEMBER_TRANSPORT"]
 if len(c)!=10:raise RuntimeError("promotion count drift")
 O.write_text(json.dumps({"schema":"effective-stark-engine-b-transport-ledger-v3","claim_tag":"VERIFIED_ENGINE_B_TRANSPORT_LEDGER","supersedes":str(P.relative_to(ROOT)),"counts":{"v5_engine_b_rows":232,"member_transport_completed":10,"member_transport_open":222},"claim_boundary":"only ten named members are promoted; every other member is explicit and unpromoted","members":rows,"source_hashes":{str(x.relative_to(ROOT)):h(x) for x in(P,B,Path(__file__))}},indent=2,sort_keys=True)+"\n");print("ENGINE_B_TRANSPORT_LEDGER_V3=PASS")
if __name__=="__main__":main()
