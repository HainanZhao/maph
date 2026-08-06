from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
A=R/"artifacts/cycle-102-b102-hadamard-quartic-boundary-v1.json"
O=R/"discovery/out/cycle102-hadamard-quartic/result.json"
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def p():
 r=json.loads(O.read_text()); assert r["parameter_count"]==125 and r["pair_count"]==7875 and r["hits"]==[]
 return {"artifact_id":"cycle-102-b102-hadamard-quartic-boundary-v1","cycle":102,"budget_ordinal":"B102","status":"SEALED","epistemic_status":"PROVED","record_type":"FINITE_METHOD_FAMILY_BOUNDARY","outcome":"No admissible unordered triple from the 125 reciprocal-even quartic-character sequences completes the near-Williamson PAF invariant at order 167.","claim_boundary":"This exact no-hit concerns only B_b(i)=chi(i^4+b i^2+1); it does not exclude other near-Williamson, Hadamard, or character constructions.","audit":r,"frozen_hashes":{k:h(R/v) for k,v in {"preregistration":"docs/cycle-102-b102-hadamard-quartic-character-preregistration-v1.md","selection":"discovery/_004_e001_hadamard_quartic_selection.md","engine":"proof/cycle102_hadamard_quartic_completion.py","checker":"proof/check_cycle102_hadamard_quartic_completion.py","result":"discovery/out/cycle102-hadamard-quartic/result.json"}.items()},"replay":{"engine":"python3 proof/cycle102_hadamard_quartic_completion.py --output discovery/out/cycle102-hadamard-quartic/result.json","checker":"python3 proof/check_cycle102_hadamard_quartic_completion.py discovery/out/cycle102-hadamard-quartic/result.json"},"cycle_decision":{"decision":"Seal and close E001.","stop":"Do not widen the quartic family or run arbitrary-sequence search; a continuation requires a distinct bounded character map.","falsifier":"A replayed admissible triple satisfying the frozen PAF target."}}
if __name__=='__main__':
 x=p(); w=len(sys.argv)==2 and sys.argv[1]=='--write'; c=len(sys.argv)==2 and sys.argv[1]=='--check'
 if w: A.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
 elif not c or json.loads(A.read_text())!=x: raise SystemExit(2)
 print('PASS')
