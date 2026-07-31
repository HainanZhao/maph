#!/usr/bin/env python3
"""Validate sealed RQ-000419 source evidence for Cycle-116 reuse."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"data/census-paper-preregistration-amendment-v14.json";O=ROOT/"artifacts/b5022-source-certificate-integrity-v1.json"
def h(x): return hashlib.sha256(x.read_bytes()).hexdigest()
def main():
 if O.exists(): raise RuntimeError("versioned output already exists")
 p=json.loads(P.read_text())
 if p["status"]!="FROZEN_BEFORE_B5022_REUSABLE_SOURCE_TRANSPORT_BATCH": raise RuntimeError("preregistration drift")
 for name,want in p["source_hashes"].items():
  if h(ROOT/name)!=want: raise RuntimeError(f"hash drift {name}")
 source=json.loads((ROOT/"data/q14-p7-case-v1.json").read_text()); transcript=(ROOT/"artifacts/q14-p7-w3-arb-certificate-v1.transcript").read_text()
 if source["verdict"]!="VERIFIED" or source["w3"]["packet_identity_verdict"]!="VERIFIED": raise RuntimeError("source packet not sealed")
 if "Q14_P7_PACKET_IDENTITY_VERIFIED=1" not in transcript: raise RuntimeError("certificate token absent")
 O.write_text(json.dumps({"schema":"effective-stark-b5022-source-certificate-integrity-v1","claim_tag":"VERIFIED_SEALED_SOURCE_CERTIFICATE_INTEGRITY","source_case_id":"RQ-000419","claim_boundary":"integrity validation only; not a fresh independent Arb replay","source_hashes":p["source_hashes"]},indent=2,sort_keys=True)+"\n")
 print("B5022_SOURCE_CERTIFICATE_INTEGRITY=PASS")
if __name__=="__main__":main()
