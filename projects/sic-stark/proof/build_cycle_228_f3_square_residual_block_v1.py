#!/usr/bin/env python3
from pathlib import Path
from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_228_f3_square_residual_block import audit
ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/"artifacts/cycle-228-b065-f3-square-residual-block-v1.json"
INPUTS={
 "prior":(ROOT/"artifacts/cycle-227-b064-augmented-transport-normal-forms-v1.json","a9e61b575078ff4ad1b3b16b47743cc7325ebec9ae75db746f7395db18c5a88c"),
 "preregistration":(ROOT/"docs/cycle-228-b065-f3-square-residual-block-preregistration-v1.md","6dcaa0a83acf7dac412fe12dd7f96421ff94d1626024203316277e0c6aee2962"),
 "replay":(ROOT/"proof/verify_cycle_228_f3_square_residual_block.py","3419d8d4f0e81cbfc8c970c3c1de5d16f6c79fa793042291156492796f683987"),
 "test":(ROOT/"tests/test_cycle_228_f3_square_residual_block.py","cd2f9ad382a2b15206f62ad0f34ee669f291be661f16764917ce2019f158a67f"),
 "prototype":(ROOT/"discovery/cycle-228-b065-f3-square-residual-block-prototype-v1.json","62381a19ffed326d9d2d59284767b8ea2e3f1f4b1dfa69353095f4c0729d8ad1"),
 "validator":(ROOT/"../../tools/preregistration_check.py","a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
 "scaffold":(ROOT/"proof/cycle_seal_v1.py","92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1")}
def payload():
 r=audit(); require(len(r["reflection_audit"])==8,"reflection census drift"); require(all(not x["reflection_match_available"] for x in r["reflection_audit"]),"unearned reflection"); require(not r["multiplication_audit"]["equation_15_operand_available"],"unearned product decomposition")
 return {"artifact_id":"cycle-228-b065-f3-square-residual-block-v1","cycle":228,"budget_ordinal":"B065","epistemic_status":"PROVED","status":"SEALED_F3_SQUARE_RESIDUAL_REFLECTION_PRODUCT_CONTAINMENT","claim_boundary":"For the two frozen m=0 positive F3^2 blocks, neither S--S equation (32) reflection nor equation (15) decomposition reduces the four ordered ordinary-gamma factors. This excludes only those identity engines, not other ordinary-gamma theorems, signed-k products, AFK covariance, fusion, Stark, or TCC.","outcome":{"epistemic_status":"PROVED","statement":"Both minimal residual blocks remain unreduced under the frozen reflection/(15) identity list."},"residual_audit":r,"companion_decision":{"identity":"/root/decision_companion_2","evidence_scope_review":"Both ordered A/C blocks, all reflection partner constants, equation-(32) convention, and equation-(15) operand condition were reviewed.","recommendation":"Seal C228 and open a distinct divisor-invariant cycle.","known_flaw":"Only two identity engines are excluded.","falsifier":"Any factor/base/partner/(15)-operand/replay discrepancy.","next_action":"Compute full pole/zero lattices and seek an uncancelled divisor.","adopted":True},"preregistration_preflight":{"cycle":228,"manifest_sha256":sha256(ROOT/"docs/cycle-228-b065-f3-square-residual-block-preregistration-v1.md")},"frozen_hashes":freeze_inputs(ROOT,INPUTS),"replay":{"check_command":"python3 proof/build_cycle_228_f3_square_residual_block_v1.py --check"},"runtime":check_runtime("Cycle 228 seal"),"sealer":{"path":"proof/build_cycle_228_f3_square_residual_block_v1.py","sha256":sha256(Path(__file__))}}
if __name__=="__main__": raise SystemExit(run_cli(description=__doc__,output=OUTPUT,payload_factory=payload))
