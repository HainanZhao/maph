#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from proof.cycle_seal_v1 import check_runtime,freeze_inputs,require,run_cli,sha256
OUT=ROOT/'artifacts/cycle-113-b113-book-ramsey-paired-fiber-boundary-v1.json'
H={'prereg':('docs/cycle-113-b113-book-ramsey-paired-fiber-preregistration-v1.md','6f9565ddc5dcc7027f4a99b8bce85bbde9d14b8de9924401b9ef186d0ed0241b'),'proof':('proof/cycle113_paired_fiber_proof.md','7416eba77e7909a3bad5ae60539c46710617d97e7b04682dddffa7e5c4003a0f'),'checker':('proof/check_cycle113_paired_fiber.py','9a6edaf1286ad83970418ebb54b793662a9d6f986c33c7063ae9dd033ff2d7f2'),'replay':('proof/replay_cycle113_paired_fiber.py','d842815e380fb8128922915b0c9448bf6af976bed35cb4acd0b39021c566b8b9'),'result':('discovery/out/cycle113-paired-fiber-check.json','ed2d068b18286c210de91c814ce880ef7f832eca5da9bf4a2adc681fb034e9ba'),'prior':('artifacts/cycle-112-b112-book-ramsey-norm-kernel-boundary-v1.json','b3f185f1e7dcccd3a515fd6065eabeaa055a2c51249da2c252be77120f31ae3b'),'scaffold':('proof/cycle_seal_v1.py','9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7')}
def payload():
 d=json.loads((ROOT/H['result'][0]).read_text())
 require(d['status']=='PASS' and d['normalized_q7_logical_states']==4194304 and d['degree_rejected_logical_states']==4161536 and d['balanced_states_directly_checked']==32768 and not d['formula_disagreements'] and not d['hits'],'drift')
 return {'artifact_id':'cycle-113-b113-book-ramsey-paired-fiber-boundary-v1','cycle':113,'budget_ordinal':'B113','status':'SEALED','epistemic_status':'PROVED','record_type':'FINITE_METHOD_FAMILY_BOUNDARY','outcome':'No q=7 normalized balanced paired-fiber matching state satisfies the asymmetric book caps.','claim_boundary':'Only q=7 paired-fiber matching states with Seidel row sum -1; not a uniform obstruction, general F001 state, or other problem.','audit':d,'frozen_hashes':freeze_inputs(ROOT,{k:(ROOT/p,h)for k,(p,h)in H.items()}),'runtime':check_runtime('c113'),'sealer':{'path':'proof/build_cycle113_paired_fiber_boundary.py','sha256':sha256(Path(__file__))},'replay':{'checker':'python3 proof/check_cycle113_paired_fiber.py','independent':'python3 proof/replay_cycle113_paired_fiber.py','check':'python3 proof/build_cycle113_paired_fiber_boundary.py --check'}}
if __name__=='__main__':raise SystemExit(run_cli(description=__doc__,output=OUT,payload_factory=payload))
