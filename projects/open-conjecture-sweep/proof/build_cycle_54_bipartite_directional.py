#!/usr/bin/env python3
"""Seal Cycle 54's bipartite directional-local-stability theorem."""
from __future__ import annotations
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from proof.check_cycle_54_bipartite_directional import audit
from proof.cycle_seal_v1 import check_runtime,freeze_inputs,require,run_cli,sha256
INPUTS={
"cycle53_artifact":(ROOT/"artifacts/cycle-53-b053-analytic-local-stability-v1.json","a25b2d013536be472b2fe07a8a7a27217176b1c002fd30def6f53cbbce44718f"),
"preregistration":(ROOT/"docs/cycle-54-b054-bipartite-directional-preregistration-v1.md","ca709aa0bb9ccb636b989443b5be9c45c2dd1dbb72d44dbe8661d8e61f8524f4"),
"idea_selection":(ROOT/"discovery/cycle54_bipartite_directional_idea_selection.md","dd0844145ac80a3d31b9909a2f1033eb0a05795f0f927e918f723036fd0fa760"),
"control":(ROOT/"proof/cycle54_rectangular_trace_control.py","f428f83f0cf3e4c984bfcf097b817e7ca1c8a512a84a8fff4e2e7400563a194a"),
"audit":(ROOT/"proof/check_cycle_54_bipartite_directional.py","d10f119320804e955387d700e7b3b13ce1d389317052a5cea594dc7027679363"),
"soundness":(ROOT/"proof/cycle_54_bipartite_directional_soundness.md","b9d856b9ca2198a0ba0c3db7ed5a6195f56f66521f71a0ea2fdb959729fc8c31"),
"test":(ROOT/"tests/test_cycle_54_bipartite_directional.py","63457eec9e32ea3d2a61faaf915e94c58213b13c6c5e3737c9961c39c69b47b0"),
"control_output":(ROOT/"discovery/out/cycle54-bipartite-directional/rectangular-control.json","b394ff4da83505b950b9411a7937a02501942262f1c0b368ffa30c46cbd5383b"),
"control_timing":(ROOT/"discovery/out/cycle54-bipartite-directional/run-control.time","c465e7919868e9ea78a39940263d5177a7986c700c5026d5e966fac2aaeb2f0f"),
"scaffold":(ROOT/"proof/cycle_seal_v1.py","9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
"preregistration_validator":(ROOT/"../../tools/preregistration_check.py","a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359")}
def payload():
 r=audit();sec,kib=(ROOT/"discovery/out/cycle54-bipartite-directional/run-control.time").read_text().split('\t');require(float(sec)<300 and int(kib)<256*1024,"resource cap exceeded")
 return {"artifact_id":"cycle-54-b054-bipartite-directional-v1","budget_ordinal":"B054","cycle":54,"record_type":"PROVED_BIPARTITE_DIRECTIONAL_LOCAL_STABILITY_THEOREM","recorded_at_utc":"2026-08-05T08:51:00Z","status":"SEALED","epistemic_status":"PROVED","outcome":"For every fixed p in (0,1), every nonzero bounded mean-zero bipartite kernel has strictly larger Möbius-graph density than p^15 along all sufficiently small admissible positive perturbations.","claim_boundary":r["claim_boundary"],"audit":r,"cycle_decision":{"companion_identity":"/root/darwin_cycle25_short","companion_advice":"Seal C54. Next open a genuinely nonlocal symbolic Zhao conjugacy-averaging-deficit engine, not another local refinement or unbounded group census.","next_question":"Can the Zhao conjugacy-averaging deficit be decomposed sign-definitely in the smallest nonabelian representation blocks for the Möbius graph?","falsifier":"A finite group and rational non-class nonnegative function reversing the deficit, or an exact symbolic term with indefinite sign."},"frozen_hashes":freeze_inputs(ROOT,INPUTS),"resources":{"control_wall_seconds":float(sec),"control_peak_rss_kib":int(kib),"temporary_disk_bytes":sum(p.stat().st_size for p in (ROOT/"discovery/out/cycle54-bipartite-directional").iterdir() if p.is_file())},"runtime":check_runtime("cycle 54 sealer"),"sealer":{"path":"proof/build_cycle_54_bipartite_directional.py","sha256":sha256(Path(__file__))},"replay":{"control_command":".venv/bin/python proof/cycle54_rectangular_trace_control.py","audit_command":".venv/bin/python proof/check_cycle_54_bipartite_directional.py","test_command":".venv/bin/python -m unittest tests.test_cycle_54_bipartite_directional -v","check_command":".venv/bin/python proof/build_cycle_54_bipartite_directional.py --check"}}
if __name__=="__main__":raise SystemExit(run_cli(description=__doc__,output=ROOT/"artifacts/cycle-54-b054-bipartite-directional-v1.json",payload_factory=payload))
