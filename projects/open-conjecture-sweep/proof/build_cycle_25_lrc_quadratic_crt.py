"""Seal Cycle 25's finite quadratic CRT-class boundary."""
from __future__ import annotations
from pathlib import Path
from check_cycle_25_quadratic_crt import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle25-quadratic-crt"
OUTPUT = ROOT / "artifacts/cycle-25-b025-lrc-quadratic-crt-v1.json"
INPUTS = {
 "preregistration":(ROOT/"docs/cycle-25-b025-lrc-quadratic-crt-preregistration-v1.md","117d68640834d3348ed9ff7e53a21debe8ed4332e0b65e48f75e78b703872b5b"),
 "crt_interface":(ROOT/"artifacts/cycle-20-b020-lrc-crt-diagonal-v1.json","cd2ced396549a819cd891472a1a71a1072dfbd8b322eb096fb2b2ce1841f62c6"),
 "prior_artifact":(ROOT/"artifacts/cycle-24-b024-lrc-crt-fourier-class-v1.json","8c47f387619a7db99ef664aab4cd3bc4b4fe5ca813bb76515ffffebac985dc62"),
 "soundness":(ROOT/"proof/cycle_25_quadratic_crt_soundness.md","49ea8cdd3702d97356bc72f54c456eb1b433332c9711b5c6b6eaa7ce4a6ad50e"),
 "search":(ROOT/"discovery/lrc_quadratic_crt_class.py","b7a062b166c696ff680e021e95ee5e93d9b271d0ae0d0fccaacb2538155cda46"),
 "core_search":(ROOT/"discovery/lrc_crt_fourier_class.py","9fe6849981871c69ecfe6cc97863536c6fc4f3fab7023cd8b45aaa6cee898b22"),
 "audit":(ROOT/"proof/check_cycle_25_quadratic_crt.py","4d4e5c80413ee3c0560e10d381c9348345179c5adc1871fadee6253d0fd118dd"),
 "test":(ROOT/"tests/test_cycle_25_quadratic_crt.py","2216d44f8ef5c2229c23fbcdfeac99d0f37a5550d12e5de5bf7acb6cd96d1c92"),
 "control":(OUT/"control.json","4873996ce7d73eeb6f4671da210aac7f1d1b2ce6087364a262c149801ea7fc86"),
 "results":(OUT/"results.tsv","aa78578f2e54e7045d6dcf63e1278805d04057e48cd2b3981a4853889074e3d3"),
 "summary":(OUT/"result.txt","fe4f284d97c9928572acdb47afd8ed19400a17263f5a4fbbcddf36864129ddab"),
 "timing":(OUT/"run.time","9738ad07392f8634c8e461dbe4ca3ba1530575d626bf4caf4100e06fd01701bd"),
 "scaffold":(ROOT/"proof/cycle_seal_v1.py","9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
}
def payload():
 return {"artifact_id":"cycle-25-b025-lrc-quadratic-crt-v1","budget_ordinal":"B025","cycle":25,"record_type":"OBSERVED_FINITE_QUADRATIC_CRT_BOUNDARY","recorded_at_utc":"2026-08-04T05:25:00Z","status":"SEALED","epistemic_status":"OBSERVED","outcome":"The complete frozen twelve-class quadratic CRT capacity-dual family left all 60 Cycle-24 survivors unresolved; no direct integer deficit was emitted.","claim_boundary":"Only the stated twelve class space, class-aware selector, one selected width-four partition, floating LP, and integerization rule are assessed. This is not a Fourier, width-four, or LRC no-go theorem.","audit":audit(),"proved_interface":{"epistemic_status":"PROVED","statement":"The prescribed twelve class functions form an invertible integer evaluation basis, and U<W remains a direct leaf-exclusion criterion."},"method_outcome":{"epistemic_status":"OBSERVED","targets":60,"unresolved":60,"objective_min":1.404040404040404,"objective_max":1.5656565656565653,"wall_seconds":56.114432},"companion_decision":{"identity":"/root/darwin_cycle25_short","scope_review":"The complete 12-class family is non-discriminating: 60/60 unresolved, the same objective range as Cycle 24, and a near-total one-class collapse.","recommendation":"Seal Cycle 25 and switch to a compact width-five control.","strongest_flaw":"A width-five class-constant selected-partition LP may miss individual or cyclotomic structure; this negative result is finite.","falsifier":"A width-five control convention or coverage mismatch, or failure to recover the known width-four certificate/interface, halts that branch before interpreting target outcomes.","independent_ideas":["compact width-five control","semantic primal lift","additional character refinement"],"final_action":"Seal the finite quadratic family and open a distinct compact width-five control question."},"resources":{"worker_cpus":[0,1,2],"reserved_cpu":3,"aggregate_wall_seconds":57,"aggregate_wall_cap_seconds":3600,"peak_rss_kib":75356,"temporary_disk_cap_bytes":21474836480},"runtime":check_runtime("Cycle 25 quadratic CRT class"),"frozen_hashes":freeze_inputs(ROOT,INPUTS),"replay":{"run_command":"taskset -c 0-2 .venv/bin/python discovery/lrc_quadratic_crt_class.py","audit_command":"taskset -c 0 .venv/bin/python proof/check_cycle_25_quadratic_crt.py","test_command":".venv/bin/python -m unittest tests.test_cycle_25_quadratic_crt -v","check_command":".venv/bin/python proof/build_cycle_25_lrc_quadratic_crt.py --check"},"sealer":{"path":"proof/build_cycle_25_lrc_quadratic_crt.py","sha256":sha256(Path(__file__))}}
if __name__ == "__main__":
 raise SystemExit(run_cli(description=__doc__,output=OUTPUT,payload_factory=payload))
