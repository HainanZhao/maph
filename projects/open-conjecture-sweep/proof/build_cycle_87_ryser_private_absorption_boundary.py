"""Seal C87's private-region absorption method boundary."""
from __future__ import annotations
import json
from pathlib import Path
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256

OUTPUT = ROOT / "artifacts/cycle-87-b087-ryser-private-absorption-boundary-v1.json"
HASHES = {
 "preregistration": ("docs/cycle-87-b087-ryser-private-absorption-preregistration-v1.md", "5c7b34a65a28d8a56adfb99bee89adf1511d6ede33b4c69b0a44c09c53b186c7"),
 "idea_selection": ("discovery/cycle87_ryser_private_absorption_selection.md", "9c4bdb891f1db6eea04d61ab1c05536fbc5ebd4f205e629f2ddebe363d403bfd"),
 "source_audit": ("discovery/cycle87_ryser_private_absorption_source_audit.md", "8cb789dddcbbe288436526c347154b1c5f3f4a2255ae6d5e7a213b5dd0c00859"),
 "checker": ("proof/check_cycle87_private_absorption.py", "5decb3dd800af3683618e5002c5a8b237eb8c454f950282c32ff30be170b6141"),
 "boundary": ("proof/cycle87_private_absorption_boundary.md", "8dd6ba25e6764e4ca1f89b1a4bdc84dba8e20855670e67b134fdfdd4b426235c"),
 "test": ("tests/test_cycle87_private_absorption.py", "081e087d92149d5af3ec369b6d471c38d4f33a8bacb60361205dbd4951125a13"),
 "prior_c72": ("artifacts/cycle-72-b072-defect-core-extension-v2.json", "09f1199d73f4d3b6fa7fe65e348fef45952c3c559ad2d294291f10d40a82d585"),
 "scaffold": ("proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
 "validator": ("../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"), }

def audit():
 r=json.loads(subprocess.check_output([sys.executable,str(ROOT/HASHES['checker'][0])],text=True))
 require(r['status']=='PASS' and r['solver_status']=='SAT','C87 solver failure')
 require(r['lower_bound']['minimum_no_absorption_points']==12,'lower-bound drift')
 c=r['candidate']; require(c['absorbed_pairs']==[] and c['minimum_component_cover']==3,'candidate drift')
 require(c['private_regions']==[[1],[2,3],[4,5],[6,7],[8,9],[10,11]],'private-region drift')
 return r

def payload():
 return {"artifact_id":"cycle-87-b087-ryser-private-absorption-boundary-v1","budget_ordinal":"B087","cycle":87,"record_type":"METHOD_BOUNDARY","recorded_at_utc":"2026-08-06T01:08:53Z","status":"SEALED","epistemic_status":"PROVED","outcome":"The smallest possible no-absorption interface has 12 points, and an exact 12-point pair-covering partition system has no absorbed private-region pair while retaining a three-component cover.","claim_boundary":"This refutes only C87 private-region absorption, not intersecting Ryser at r=6 or other global partition mechanisms.","cycle_decision":{"companion_identity":"/root/oracle_c87_portfolio (Oracle)","companion_advice":"Test the minimal root-normalized interface and pivot on any exact no-absorption system.","decision":"Seal the method boundary; the exact candidate falsifies absorption but is not a Ryser counterexample.","falsifier":"A verified pair-covering partition system with all private regions nonempty and no absorbed pair."},"audit":audit(),"frozen_hashes":freeze_inputs(ROOT,{k:(ROOT/p,d) for k,(p,d) in HASHES.items()}),"runtime":check_runtime('c87'),"sealer":{"path":"proof/build_cycle_87_ryser_private_absorption_boundary.py","sha256":sha256(Path(__file__))},"replay":{"audit":"python3 proof/check_cycle87_private_absorption.py","test":"python3 -c \"import runpy; ns=runpy.run_path('tests/test_cycle87_private_absorption.py'); ns['test_c87_minimal_absorption_countermodel']()\"","check":"python3 proof/build_cycle_87_ryser_private_absorption_boundary.py --check"}}
if __name__=='__main__': raise SystemExit(run_cli(description=__doc__,output=OUTPUT,payload_factory=payload))
