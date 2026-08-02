#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import sys
from typing import Any
from cycle_seal_v1 import check_runtime,freeze_inputs,load_record,require,run_cli,sha256,validate_prior
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
if str(REPO) not in sys.path: sys.path.insert(0,str(REPO))
from tools.preregistration_check import validate_preregistration
SELF=Path(__file__).resolve(); OUTPUT=ROOT/"artifacts/cycle-188-nonrational-root-tower-v1.json"
INPUTS={"preregistration":(ROOT/"docs/cycle-188-nonrational-root-tower-preregistration-v1.md","f2a6a5926d4c21e856307bd9a3852c8b910c9db9cbc78614c322288eb7e01c7e"),"document":(ROOT/"docs/cycle-188-nonrational-root-tower-v1.md","5a6c4ffc483ac28297549d4d53839ee883d4063a857c7810838d94e9e9aa5e21"),"conventions":(ROOT/"conventions/nonrational_root_tower_v1.py","af77822bc417740629c418e03c14a61b3d7c75dbd0068913f8eb876251585210"),"tests":(ROOT/"tests/test_cycle_188_nonrational_root_tower_v1.py","e5733dcef9f9d1ada65b3a70500a334f71fa468964d1f33cd84b02317251e2b5"),"cycle184correction":(ROOT/"artifacts/cycle-184-phase-shift-correction-v1.json","2509f737c60a9e2a71bb640a1567676beb7dfe68db33c08a9257924b0259fa89"),"sealing_scaffold":(ROOT/"proof/cycle_seal_v1.py","96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9")}
def exact(x):
 if isinstance(x,dict): return {str(k):exact(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)): return [exact(v) for v in x]
 return x
def seal()->dict[str,Any]:
 require(sha256(REPO/"tools/preregistration_check.py")=="a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359","validator")
 p=validate_preregistration(INPUTS["preregistration"][0],expected_cycle=188,enforce_manifest_head=False)
 validate_prior(INPUTS["cycle184correction"][0],"SEALED_CORRECTION_SHIFTED_SLOPES_NONRATIONAL_TWO_RAY_DEFORMATION")
 theorem=load_record(root=ROOT,path=INPUTS["conventions"][0],module_name="nonrational_root_tower_v1")
 return {"artifact_id":"cycle-188-nonrational-root-tower-v1","epistemic_status":"PROVED","status":"SEALED_SUBCRITICAL_CORRECTED_NONRATIONAL_ROOT_TOWER","claim_boundary":"This rules out only the corrected light rational-root tower family as a critical packet saturator.","runtime":check_runtime("Cycle 188"),"sealer":{"path":str(SELF.relative_to(ROOT)),"sha256":sha256(SELF)},"frozen_hashes":freeze_inputs(ROOT,INPUTS),"preregistration_preflight":{"cycle":p["cycle"],"manifest_sha256":p["manifest_sha256"],"input_hashes":p["input_hashes"],"parameters":p["parameters"]},"root_tower_result":exact(theorem),"density_effect":{"epistemic_status":"OBSERVED","status":"NO_PROMOTION"},"replay":{"check_command":"python3 proof/build_cycle_188_nonrational_root_tower_v1.py --check","test_command":"python3 -m unittest tests/test_cycle_188_nonrational_root_tower_v1.py"}}
if __name__=="__main__": raise SystemExit(run_cli(description="Cycle 188",output=OUTPUT,payload_factory=seal))
