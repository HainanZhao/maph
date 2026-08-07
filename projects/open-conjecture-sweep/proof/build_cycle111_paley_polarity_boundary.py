#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from proof.cycle_seal_v1 import check_runtime,freeze_inputs,require,run_cli,sha256
OUT=ROOT/'artifacts/cycle-111-b111-book-ramsey-paley-polarity-boundary-v1.json'
H={'prereg':('docs/cycle-111-b111-book-ramsey-paley-polarity-preregistration-v1.md','c1a5d3c69b02ba4b995e770eb1fedc1fb1ac3ac4cb971d8752247f330ffd80fa'),'proof':('proof/cycle111_paley_polarity_proof.md','0a2bbf56d859538d0f3750eb9b65138eba5df13e548564dde96a060ae665951e'),'checker':('proof/check_cycle111_paley_polarity.py','2ecf3613947b822c409393a7bc52ca949512bca08f012e4b43802f6e98796072'),'replay':('proof/replay_cycle111_paley_polarity.py','798b31de36dfb19268ad0ad2be62ea7c5332623b4862c786030aaea719375c5d'),'result':('discovery/out/cycle111-paley-polarity-check.json','acc265baa869bcad0e8931020714c837c1b014498ee6e4c695f9a23751898966'),'prior':('artifacts/cycle-109-b109-book-ramsey-inversion-warp-boundary-v1.json','0b302302656280ade1904b86a92c48f887a1ca6ff419535d88026c66a6687822'),'scaffold':('proof/cycle_seal_v1.py','9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7')}
def payload():
 d=json.loads((ROOT/H['result'][0]).read_text());require(d=={'hits':0,'p0_states':465,'polarities':28,'status':'PASS'},'drift')
 return {'artifact_id':'cycle-111-b111-book-ramsey-paley-polarity-boundary-v1','cycle':111,'budget_ordinal':'B111','status':'SEALED','epistemic_status':'PROVED','record_type':'FINITE_METHOD_FAMILY_BOUNDARY','outcome':'No q=7 completion exists in the fixed Paley-cross nontranslation polarity reconstruction state.','claim_boundary':'Only q=7 fixed-Paley-cross states satisfying the displayed polarity reconstruction; not a uniform obstruction or other kernels.','audit':d,'frozen_hashes':freeze_inputs(ROOT,{k:(ROOT/p,h)for k,(p,h)in H.items()}),'runtime':check_runtime('c111'),'sealer':{'path':'proof/build_cycle111_paley_polarity_boundary.py','sha256':sha256(Path(__file__))},'replay':{'checker':'python3 proof/check_cycle111_paley_polarity.py','independent':'python3 proof/replay_cycle111_paley_polarity.py','check':'python3 proof/build_cycle111_paley_polarity_boundary.py --check'}}
if __name__=='__main__':raise SystemExit(run_cli(description=__doc__,output=OUT,payload_factory=payload))
