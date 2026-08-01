#!/usr/bin/env python3
"""Promote the ten corrected direct-source transports in ledger v5."""
from __future__ import annotations
import hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'artifacts/engine-b-transport-ledger-v4.json'
B=ROOT/'artifacts/corrected-direct-source-transports-v1.json'
O=ROOT/'artifacts/engine-b-transport-ledger-v5.json'
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if O.exists(): raise RuntimeError('versioned output already exists')
 p=json.loads(P.read_text()); b=json.loads(B.read_text())
 if p['counts']['member_transport_completed']!=12 or b['claim_tag']!='PROVED_EXACT_MEMBER_TRANSPORT_BATCH' or b['record_count']!=10: raise RuntimeError('predecessor drift')
 promoted={r['case_id']:r for r in b['records']}; rows=[]
 for row in p['members']:
  x=dict(row)
  if x['case_id'] in promoted:
   r=promoted[x['case_id']]
   x.update({'transport_status':'PROVED_EXACT_MEMBER_TRANSPORT','transport_certificate':str(B.relative_to(ROOT)),'source_case_id':r['source_case_id'],'packet_relation':r['packet_relation'],'artin_labelled_formula_terms':r['artin_labelled_formula_terms']})
  rows.append(x)
 if len([x for x in rows if x['transport_status']=='PROVED_EXACT_MEMBER_TRANSPORT'])!=22: raise RuntimeError('promotion count drift')
 payload={'schema':'effective-stark-engine-b-transport-ledger-v5','claim_tag':'VERIFIED_ENGINE_B_TRANSPORT_LEDGER','supersedes':str(P.relative_to(ROOT)),'counts':{'v5_engine_b_rows':232,'member_transport_completed':22,'member_transport_open':210},'claim_boundary':'only twenty-two named members are promoted; every other member is explicit and unpromoted','members':rows,'source_hashes':{str(x.relative_to(ROOT)):h(x) for x in(P,B,Path(__file__))}}
 O.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
 print('ENGINE_B_TRANSPORT_LEDGER_V5=PASS')
if __name__=='__main__': main()
