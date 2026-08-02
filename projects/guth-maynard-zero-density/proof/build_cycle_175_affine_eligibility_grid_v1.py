#!/usr/bin/env python3
"""Seal Cycle 175 full affine eligibility-grid classifier."""
from __future__ import annotations
from pathlib import Path
from typing import Any
from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT=Path(__file__).resolve().parents[1]
SELF=Path(__file__).resolve()
OUTPUT=ROOT/"artifacts/cycle-175-affine-eligibility-grid-v1.json"
INPUTS={
 "preregistration":(ROOT/"docs/cycle-175-affine-eligibility-grid-preregistration-v1.md","81c19f0249fff9e8a19c9013125f706e07fe84239269e160502d5876063cd3db"),
 "document":(ROOT/"docs/cycle-175-affine-eligibility-grid-v1.md","1d30593a8c19410281d442505dd9f51d7a1dc5adc4edebe594d50c2557db62b9"),
 "conventions":(ROOT/"conventions/affine_eligibility_grid_v1.py","9140913f163e2f5439ca8d780b6dc9268bc9fbbefc6870de5fe5f84a8412e08a"),
 "tests":(ROOT/"tests/test_cycle_175_affine_eligibility_grid_v1.py","aa5d82364ad4f6c49c1ba3c51dc2713bc13f8da657c3533ee2a55b5d06b34822"),
 "sealing_scaffold":(ROOT/"proof/cycle_seal_v1.py","96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
 "cycle174":(ROOT/"artifacts/cycle-174-adaptive-slack-transport-v1.json","a2060558bfc48723a2d5bb418d60252c27fe8f4f45a94031ccb233daadaaab41"),
 "cycle167":(ROOT/"artifacts/cycle-167-affine-fibre-transport-v1.json","7ba12c9d0534c0d0d151bce753fa24191c4e174af839ca12b86d65911779ed1b"),}

def exact_checks()->dict[str,object]:
 m=__import__("conventions.affine_eligibility_grid_v1",fromlist=["verify_all"]); checked=m.verify_all()
 require("eligibility-grid/discrepancy classifier" in checked["boundary"],"boundary")
 x=m.full_ledger(parameters=(0,1,2,3,4),h0=25,slope=1,a=5,q=4,H=20,K=5)
 require(x["eligible"]==(0,) and x["capacity_class"]=="saturated","full grid")
 return checked

def seal()->dict[str,Any]:
 validate_prior(INPUTS["cycle174"][0],"SEALED_CAPACITY_SATURATED_BOUNDED_SLACK_TRANSPORT_OR_LABELLED_DEFICIT_BANK")
 validate_prior(INPUTS["cycle167"][0],"SEALED_DIRECT_AFFINE_CROSS_LABEL_TRANSPORT_OR_OBSTRUCTION_CLASSIFIER")
 theorem=load_record(root=ROOT,path=INPUTS["conventions"][0],module_name="affine_eligibility_grid_v1")
 return {"artifact_id":"cycle-175-affine-eligibility-grid-v1","epistemic_status":"PROVED","status":"SEALED_FULL_AFFINE_ELIGIBILITY_GRID_OR_LABELLED_DISCREPANCY_BANK","claim_boundary":"This proves a finite full-affine eligibility-grid/discrepancy classifier. It proves no actual breadth lower bound, target packet, recurrence, skeleton, density, or interval gain.","runtime":check_runtime("Cycle 175"),"sealer":{"path":str(SELF.relative_to(ROOT)),"sha256":sha256(SELF)},"frozen_hashes":freeze_inputs(ROOT,INPUTS),"prior_context":{"epistemic_status":"PROVED","cycle167_role":"exact residue/range direct-edge interface","cycle174_role":"common capacity class for every eligible row"},"affine_eligibility_grid":{"epistemic_status":"PROVED",**theorem},"density_effect":{"epistemic_status":"OBSERVED","status":"NO_PROMOTION"},"exact_replay":exact_checks(),"remaining_target":{"epistemic_status":"CONJECTURED","statement":"Use actual exponential/fibre information to lower-bound eligible breadth or turn a massed range/residue/capacity discrepancy bank into a quantitative inverse theorem."},"research_stage_review_policy":{"hostile_audit":"DEFERRED_TO_PAPER_STAGE"},"replay":{"write_command":"python3 proof/build_cycle_175_affine_eligibility_grid_v1.py --write","check_command":"python3 proof/build_cycle_175_affine_eligibility_grid_v1.py --check","test_command":"python3 -m unittest tests/test_cycle_175_affine_eligibility_grid_v1.py"}}
if __name__=="__main__": raise SystemExit(run_cli(description=__doc__ or "Cycle 175",output=OUTPUT,payload_factory=seal))
