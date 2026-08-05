"""Seal C69's local deletion-cover exchange no-go."""
from pathlib import Path
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from proof.cycle_seal_v1 import check_runtime,freeze_inputs,run_cli,sha256

H={
 "prereg":("docs/cycle-69-b069-ryser-critical-cover-preregistration-v1.md","0de4ab65081eca84ddceb0e16ccfbab2f7081d4b7a63cafafe232497e894ef6c"),
 "idea":("discovery/cycle69_ryser_idea_selection.md","0487df9abd9dcafe6d21e1ae89b15a5d94aae98d8f013bcafbf406f66a4c0aa1"),
 "literature":("discovery/cycle69_literature_scope.md","540539e97818a8012dcb6f19263e11d2d53e49e9e8b0c4b96f0c0e08f3856514"),
 "control":("discovery/cycle69_r6_extremal_control.py","c62edddd382483e1b243e385bfe14ba99a40a0b1e137d3145e995b3223bf2276"),
 "checker":("proof/cycle69_deletion_exchange.py","00914f302c6f102ad2aa866b898d06600a016f07fa28a318c7d9326540e8d40a"),
 "scaffold":("proof/cycle_seal_v1.py","9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
 "validator":("../../tools/preregistration_check.py","a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359")}

def audit():
 p=json.loads(subprocess.check_output([sys.executable,str(ROOT/'proof/cycle69_deletion_exchange.py')]))
 assert p['status']=='PASS' and p['epistemic_status']=='PROVED'
 assert len(p['control_rows'])==13
 assert all(r['all_disjoint_from_deleted_edge'] and not sum(r['all_exchange_move_counts']) for r in p['control_rows'])
 return p

def payload():
 a=audit()
 return {"artifact_id":"cycle-69-b069-deletion-exchange-nogo-v1","budget_ordinal":"B069","cycle":69,"record_type":"PROVED_LOCAL_EXCHANGE_NO_GO","recorded_at_utc":"2026-08-05T14:25:00Z","status":"SEALED","epistemic_status":"PROVED",
 "outcome":"All minimum deletion covers of the published 13-edge r=6 equality system have zero size-preserving exchanges into the deleted edge.",
 "claim_boundary":"This proves only that equal-size local deletion-cover exchanges cannot distinguish a hypothetical tau=6 counterexample from the known tau=5 equality system. It is not a Ryser proof, a fractional-dual no-go, or an exclusion of larger recombination mechanisms.","audit":a,
 "cycle_decision":{"companion_identity":"/root/darwin_cycle25_short","companion_advice":"Seal after correcting the scope; then open a distinct deletion-witness incidence-design cycle.","decision":"Close raw local exchange as non-discriminating and change state space to all (edge, five-cover) witnesses of a hypothetical minimal tau>=6 counterexample.","falsifier":"A verified exchange in the cited tau=5 control would falsify this record; it is absent by exact enumeration and by tau=5 itself."},
 "frozen_hashes":freeze_inputs(ROOT,{k:(ROOT/p,h) for k,(p,h) in H.items()}),"runtime":check_runtime('c69'),"sealer":{"path":"proof/build_cycle_69_exchange_nogo.py","sha256":sha256(Path(__file__))},"replay":{"audit":"python3 proof/cycle69_deletion_exchange.py","check":"python3 proof/build_cycle_69_exchange_nogo.py --check"}}

if __name__=='__main__': raise SystemExit(run_cli(description=__doc__,output=ROOT/'artifacts/cycle-69-b069-deletion-exchange-nogo-v1.json',payload_factory=payload))
