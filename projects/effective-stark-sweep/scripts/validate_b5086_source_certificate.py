#!/usr/bin/env python3
"""Validate the sealed RQ-001107 source evidence for Cycle-120 reuse."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; P=ROOT/"data/census-paper-preregistration-amendment-v15.json"; O=ROOT/"artifacts/b5086-source-certificate-integrity-v1.json"
def h(x): return hashlib.sha256(x.read_bytes()).hexdigest()
def main():
 if O.exists(): raise RuntimeError("versioned output already exists")
 p=json.loads(P.read_text())
 if p["status"]!="FROZEN_BEFORE_B5086_REUSABLE_SOURCE_TRANSPORT_BATCH": raise RuntimeError("preregistration drift")
 for name,want in p["source_hashes"].items():
  if h(ROOT/name)!=want: raise RuntimeError(f"hash drift {name}")
 source=json.loads((ROOT/"data/q33-p11-order10-case-v1.json").read_text()); transcript=(ROOT/"artifacts/rq001107-w3-arb-certificate-v1.transcript").read_text()
 if source["verdict"]!="VERIFIED" or source["identification"]["claim_tag"]!="VERIFIED": raise RuntimeError("source packet not sealed")
 if "RQ001107_PACKET_IDENTITY_VERIFIED=1" not in transcript: raise RuntimeError("certificate token absent")
 O.write_text(json.dumps({"schema":"effective-stark-b5086-source-certificate-integrity-v1","claim_tag":"VERIFIED_SEALED_SOURCE_CERTIFICATE_INTEGRITY","source_case_id":"RQ-001107","claim_boundary":"integrity validation only; not a fresh independent Arb replay","source_hashes":p["source_hashes"]},indent=2,sort_keys=True)+"\n")
 print("B5086_SOURCE_CERTIFICATE_INTEGRITY=PASS")
if __name__=="__main__": main()
