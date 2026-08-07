#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from proof.cycle_seal_v1 import check_runtime,freeze_inputs,require,run_cli,sha256
OUT=ROOT/'artifacts/cycle-114-b114-book-ramsey-two-block-circulant-boundary-v1.json'
H={'prereg':('docs/cycle-114-b114-book-ramsey-two-block-circulant-preregistration-v1.md','0133e8e051e94475871db2d5d11ca5e09474ff1edd39b2d1b0b641286227defa'),'proof':('proof/cycle114_two_block_circulant_proof.md','4a760ee793a9e0f8b4e1b91b4d58f994d02dbb3a1aff5d38282d8cc4c95c2f2c'),'checker':('proof/check_cycle114_two_block_circulant.py','7092db4b26fb5ff2cee22e0a791e9a0d2dde9113fb05b6e3725c06ca457e5fd6'),'replay':('proof/replay_cycle114_two_block_circulant.py','4a38b2d5c7b0407f6dff5e8dccd4e550c6f9a69618e1d472fc184a984b7dc635'),'result':('discovery/out/cycle114-two-block-circulant-check.json','cc777549f2da736cb51f9fbfbf057ce71de533de99b7f4a01a47011e3e7b51b8'),'prior':('artifacts/cycle-113-b113-book-ramsey-paired-fiber-boundary-v1.json','490c9dc32a18aa02310fc9dea6866dcb43369bfeb1a269b90d4066dd8b88e762'),'scaffold':('proof/cycle_seal_v1.py','9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7')}
def payload():
 d=json.loads((ROOT/H['result'][0]).read_text());require(d['status']=='PASS' and d['states']==512 and not d['hits'],'drift')
 return {'artifact_id':'cycle-114-b114-book-ramsey-two-block-circulant-boundary-v1','cycle':114,'budget_ordinal':'B114','status':'SEALED','epistemic_status':'PROVED','record_type':'FINITE_METHOD_FAMILY_BOUNDARY','outcome':'No q=7 degree-seven full two-block-circulant state satisfies the asymmetric book caps.','claim_boundary':'Only the complete q=7 source-native two-block-circulant state; not larger q, non-circulant states, or F001 generally.','audit':d,'frozen_hashes':freeze_inputs(ROOT,{k:(ROOT/p,h)for k,(p,h)in H.items()}),'runtime':check_runtime('c114'),'sealer':{'path':'proof/build_cycle114_two_block_circulant_boundary.py','sha256':sha256(Path(__file__))},'replay':{'checker':'python3 proof/check_cycle114_two_block_circulant.py','independent':'python3 proof/replay_cycle114_two_block_circulant.py','check':'python3 proof/build_cycle114_two_block_circulant_boundary.py --check'}}
if __name__=='__main__':raise SystemExit(run_cli(description=__doc__,output=OUT,payload_factory=payload))
