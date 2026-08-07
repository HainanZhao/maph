"""Seal C104's exact four-bit D14 Cayley family boundary."""
from __future__ import annotations
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256

OUTPUT=ROOT/"artifacts/cycle-104-b104-book-ramsey-dihedral-cayley-boundary-v1.json"
HASHES={
 "preregistration":("docs/cycle-104-b104-book-ramsey-dihedral-cayley-preregistration-v1.md","ebfa46ec8d4441c83632a669e2e9a4a7a48bfd7fe482dd00ceddfd908bb2afde"),
 "oracle_packet":("discovery/cycle104_oracle_post_result_packet.md","33318aeed8c905031bf64fddd5b128c6995611298971eb5783cf07583a208099"),
 "prior_c103":("artifacts/cycle-103-b103-book-ramsey-reflection-boundary-correction-v2.json","93ff897b30292baaa3ddde43cf8f97572487c4bf78cde026a2ae834d129f2159"),
 "engine":("proof/cycle104_book_ramsey_dihedral_cayley.py","2225c3b285019a7fc3c98bcbd401f6838a6c1a9030c1930f287e7cd446ef36b6"),
 "checker":("proof/check_cycle104_book_ramsey_dihedral_cayley.py","dac614a86c60804dc6a7233e235c94cbdc938bf79d349be2ea695f056146ca20"),
 "replay":("proof/replay_cycle104_book_ramsey_dihedral_cayley.py","4212bb90229d4b1b5fbd0ee6ef392c42d317af8676067e4bcdd158c577addad4"),
 "result":("discovery/out/cycle104-book-ramsey-dihedral-cayley/result.json","7986290b2fef9e06e0233ac13bf2f9809da42df55a1314da9a1089557d2dd145"),
 "check":("discovery/out/cycle104-book-ramsey-dihedral-cayley/check.json","c7b17a9e88ec5a405e7cf7d0c5c4d29898361fe978c8bfc199e7d63dfd17d3a7"),
 "scaffold":("proof/cycle_seal_v1.py","9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
 "validator":("../../tools/preregistration_check.py","a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),}

def audit() -> dict:
 result=json.loads((ROOT/HASHES["result"][0]).read_text()); check=json.loads((ROOT/HASHES["check"][0]).read_text())
 require(len(result["q7"])==16 and result["q7_hits"]==[] and result["q23"]==[],"template outcome drift")
 require(all(row["route_agrees"] for row in result["q7"]),"convolution interface drift")
 candidates=[row for row in result["q7"] if row["row_ok"]]
 require([(r["mask"],r["offdiagonal_square_distribution"]) for r in candidates]==[(3,{"-12":7,"-8":42,"8":42}),(14,{"-12":49,"12":42})],"Seidel distribution drift")
 require(all(not row["square_ok"] for row in candidates),"unexpected q7 hit")
 require(check=={"q7_rows":16,"q7_hits":[],"q23_rows":0,"status":"PASS"},"independent checker drift")
 return {"enumerator":result,"independent_checker":check}

def payload() -> dict:
 return {"artifact_id":"cycle-104-b104-book-ramsey-dihedral-cayley-boundary-v1","cycle":104,"budget_ordinal":"B104","status":"SEALED","epistemic_status":"PROVED","record_type":"FINITE_METHOD_FAMILY_BOUNDARY","outcome":"All 16 four-bit inverse-closed D14 Cayley connection sets fail the frozen q=7 Seidel condition; only masks 3 and 14 have row sum -1, and each has a nonpermitted exact off-diagonal S^2 distribution.","claim_boundary":"This proves only the finite four-bit D14 class. q=23 was not tested because the frozen conditional rule permits it only after a q=7 hit. It does not exclude exceptional q=7 treatment, arbitrary dihedral connection sets, other character architectures, or the all-n book-Ramsey conjecture.","audit":audit(),"frozen_hashes":freeze_inputs(ROOT,{k:(ROOT/p,d) for k,(p,d) in HASHES.items()}),"runtime":check_runtime("c104"),"sealer":{"path":"proof/build_cycle104_book_ramsey_dihedral_cayley_boundary.py","sha256":sha256(Path(__file__))},"replay":{"preflight":"source ../../tools/dev-env.sh && research prereg check docs/cycle-104-b104-book-ramsey-dihedral-cayley-preregistration-v1.md --expected-cycle 104","full":"python3 proof/replay_cycle104_book_ramsey_dihedral_cayley.py","check":"python3 proof/build_cycle104_book_ramsey_dihedral_cayley_boundary.py --check"},"cycle_decision":{"decision":"Seal and close the four-bit D14 Cayley gate.","stop":"Do not add orbit bits or enumerate arbitrary reflection subsets. A continuation must change to a compressed group-ring/autocorrelation invariant with an independently checked Seidel equivalence.","falsifier":"A replayed q=7 mask satisfying the frozen Seidel conditions, or a convolution/adjacency disagreement."}}

if __name__=="__main__": raise SystemExit(run_cli(description=__doc__,output=OUTPUT,payload_factory=payload))
