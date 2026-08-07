#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from proof.cycle_seal_v1 import check_runtime,freeze_inputs,require,run_cli,sha256
OUT=ROOT/'artifacts/cycle-112-b112-book-ramsey-norm-kernel-boundary-v1.json'
H={'prereg':('docs/cycle-112-b112-book-ramsey-norm-kernel-preregistration-v1.md','fbfbde47f482ed16c2a533003435850b01450739f9b91a126b55c1276ec2f4a0'),'proof':('proof/cycle112_norm_kernel_proof.md','3f34f1f854da8db16e44e78ae566e130011839f11c2bba9f0d1fd6907e12256b'),'checker':('proof/check_cycle112_norm_kernel.py','0df72843507b292e67ee75aff8015e6afcdb2fa41684b3984803b44ae7d54737'),'replay':('proof/replay_cycle112_norm_kernel.py','2ca03d42bc5323ae8d0a8125eb8d4d27f61807bbe04f9c80ba8f7cf5cb04aba5'),'result':('discovery/out/cycle112-norm-kernel-check.json','b3eaf95254618b17dc6f037d24a39bf780f7f4c3d7136064f2a9b482b940a244'),'prior':('artifacts/cycle-111-b111-book-ramsey-paley-polarity-boundary-v1.json','98629680c865f10e01d16605ae052d2199bdcdd30b7ee97d354a32757490a1f0'),'scaffold':('proof/cycle_seal_v1.py','9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7')}
def payload():
 d=json.loads((ROOT/H['result'][0]).read_text());require(d['status']=='PASS'and d['states']==54 and not d['hits'],'drift')
 return {'artifact_id':'cycle-112-b112-book-ramsey-norm-kernel-boundary-v1','cycle':112,'budget_ordinal':'B112','status':'SEALED','epistemic_status':'PROVED','record_type':'FINITE_METHOD_FAMILY_BOUNDARY','outcome':'No q=7 anisotropic norm-kernel state in the declared 54-state family satisfies the asymmetric caps.','claim_boundary':'Only q=7 norm-kernel family; not q=23 or other cross kernels.','audit':d,'frozen_hashes':freeze_inputs(ROOT,{k:(ROOT/p,h)for k,(p,h)in H.items()}),'runtime':check_runtime('c112'),'sealer':{'path':'proof/build_cycle112_norm_kernel_boundary.py','sha256':sha256(Path(__file__))},'replay':{'checker':'python3 proof/check_cycle112_norm_kernel.py','independent':'python3 proof/replay_cycle112_norm_kernel.py','check':'python3 proof/build_cycle112_norm_kernel_boundary.py --check'}}
if __name__=='__main__':raise SystemExit(run_cli(description=__doc__,output=OUT,payload_factory=payload))
