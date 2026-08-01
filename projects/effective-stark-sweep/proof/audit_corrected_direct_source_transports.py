#!/usr/bin/env python3
"""Replay audit for the corrected ten-member direct-source batch."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
B=ROOT/'artifacts/corrected-direct-source-transports-v1.json'
L=ROOT/'artifacts/engine-b-transport-ledger-v5.json'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 b=json.loads(B.read_text()); l=json.loads(L.read_text())
 for n,want in b['source_hashes'].items():
  if h(ROOT/n)!=want:raise RuntimeError(f'source hash drift: {n}')
 expected={'RQ-002079':('RQ-002057',1),'RQ-002964':('RQ-002955',1),'RQ-002983':('RQ-002955',5),'RQ-001115':('RQ-001107',1),'RQ-001125':('RQ-001107',1),'RQ-001132':('RQ-001107',1),'RQ-001133':('RQ-001107',1),'RQ-001149':('RQ-001107',1),'RQ-001164':('RQ-001107',1),'RQ-001172':('RQ-001107',7)}
 rows={r['case_id']:r for r in b['records']}
 if b['claim_tag']!='PROVED_EXACT_MEMBER_TRANSPORT_BATCH' or set(rows)!=set(expected):raise RuntimeError('batch population drift')
 for case,(source,c) in expected.items():
  r=rows[case]
  if r['source_case_id']!=source or r['ray_map_generator_coefficient']!=c:raise RuntimeError(f'label drift: {case}')
  if not r['factors'] or len(r['artin_labelled_formula_terms'])!=2**len(r['factors']):raise RuntimeError(f'Euler subset drift: {case}')
  if any(t['target_label_coefficient_to_source']!=c for t in r['artin_labelled_formula_terms']):raise RuntimeError(f'map coefficient drift: {case}')
 done={r['case_id'] for r in l['members'] if r['transport_status']=='PROVED_EXACT_MEMBER_TRANSPORT'}
 if l['counts']!={'v5_engine_b_rows':232,'member_transport_completed':22,'member_transport_open':210} or not set(expected)<=done:raise RuntimeError('successor ledger drift')
 if h(B)!=l['source_hashes']['artifacts/corrected-direct-source-transports-v1.json']:raise RuntimeError('ledger source hash drift')
 print('CORRECTED_DIRECT_SOURCE_TRANSPORT_AUDIT=PASS')
if __name__=='__main__':main()
