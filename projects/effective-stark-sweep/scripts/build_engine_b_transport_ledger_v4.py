#!/usr/bin/env python3
"""Promote the Cycle-125 B5-025 label-aware transports in ledger v4."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; P=ROOT/"artifacts/engine-b-transport-ledger-v3.json"; B=ROOT/"artifacts/b5025-label-aware-transports-v1.json"; O=ROOT/"artifacts/engine-b-transport-ledger-v4.json"
def h(x):return hashlib.sha256(x.read_bytes()).hexdigest()
def main():
 if O.exists():raise RuntimeError("versioned output already exists")
 p=json.loads(P.read_text());b=json.loads(B.read_text())
 if p["counts"]["member_transport_completed"]!=10 or b["claim_tag"]!="PROVED_EXACT_MEMBER_TRANSPORT_BATCH":raise RuntimeError("predecessor drift")
 d={x["case_id"]:x for x in b["records"]}
 if sorted(d)!=["RQ-000221","RQ-000228"]:raise RuntimeError("batch drift")
 rows=[]
 for row in p["members"]:
  x=dict(row)
  if x["case_id"] in d:x.update({"transport_status":"PROVED_EXACT_MEMBER_TRANSPORT","transport_certificate":str(B.relative_to(ROOT)),"source_case_id":"RQ-000190","packet_relation":d[x["case_id"]]["packet_relation"],"artin_labelled_formula_terms":d[x["case_id"]]["artin_labelled_formula_terms"]})
  rows.append(x)
 completed=[x for x in rows if x["transport_status"]=="PROVED_EXACT_MEMBER_TRANSPORT"]
 if len(completed)!=12:raise RuntimeError("promotion count drift")
 O.write_text(json.dumps({"schema":"effective-stark-engine-b-transport-ledger-v4","claim_tag":"VERIFIED_ENGINE_B_TRANSPORT_LEDGER","supersedes":str(P.relative_to(ROOT)),"counts":{"v5_engine_b_rows":232,"member_transport_completed":12,"member_transport_open":220},"claim_boundary":"only twelve named members are promoted; every other member is explicit and unpromoted","members":rows,"source_hashes":{str(x.relative_to(ROOT)):h(x) for x in(P,B,Path(__file__))}},indent=2,sort_keys=True)+"\n")
 print("ENGINE_B_TRANSPORT_LEDGER_V4=PASS")
if __name__=="__main__":main()
