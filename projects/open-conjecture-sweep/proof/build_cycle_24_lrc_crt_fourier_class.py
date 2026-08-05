"""Seal Cycle 24's finite CRT/Ramanujan class-dual boundary."""
from __future__ import annotations
from pathlib import Path
from check_cycle_24_crt_fourier_class import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle24-crt-fourier-class"
OUTPUT = ROOT / "artifacts/cycle-24-b024-lrc-crt-fourier-class-v1.json"
INPUTS = {
 "preregistration":(ROOT/"docs/cycle-24-b024-lrc-crt-fourier-class-preregistration-v1.md","c91cd03784c55b07ed8c05c9df5f72d5f19e4069f3eb8666405d960c2924a19b"),
 "crt_interface":(ROOT/"artifacts/cycle-20-b020-lrc-crt-diagonal-v1.json","cd2ced396549a819cd891472a1a71a1072dfbd8b322eb096fb2b2ce1841f62c6"),
 "coupled_interface":(ROOT/"artifacts/cycle-21-b021-lrc-coupled-incidence-v1.json","360daaf46d9f4442a65cce29d8011d05ea529ad0e59a7f16dc6c12b6b66a0200"),
 "prior_artifact":(ROOT/"artifacts/cycle-23-b023-lrc-adaptive-width-four-v1.json","c1af453bc3e87e4844cf91e462c83df7abc4f5cf2a33639e44819798f69c1a88"),
 "soundness":(ROOT/"proof/cycle_24_crt_fourier_class_soundness.md","fec54cb07cf09af7192bbd89b643d7fd9c62478406bb7c63d58138ab89bcef88"),
 "search":(ROOT/"discovery/lrc_crt_fourier_class.py","9fe6849981871c69ecfe6cc97863536c6fc4f3fab7023cd8b45aaa6cee898b22"),
 "audit":(ROOT/"proof/check_cycle_24_crt_fourier_class.py","0147ccaf86d950cc31fdb814d666afcc2dc06a2dd9857a8a896294d690dc5cd8"),
 "test":(ROOT/"tests/test_cycle_24_crt_fourier_class.py","1eaf8fc55e9a1ea4c16dc0cc92308855575bec6488998c89731e21d56f6df4af"),
 "control":(OUT/"control.json","0d0818cc5dac8bf4da3cb398c0d47760e6b90e8d940d1ca2368dcc6e42aaa8a7"),
 "results":(OUT/"results.tsv","8e022ec85dd3e19a5cef97c7d54601263906ed0d202036a98bc57e67a792096e"),
 "summary":(OUT/"result.txt","cbbf99e7ece4e351e9a4dff393d6e98c3883724d76dca363907a34301a373ff4"),
 "timing":(OUT/"run.time","e8f503750fb18aa0c1868de78e7c392ca6347e7402a0de9b9de85e2d616434d7"),
 "scaffold":(ROOT/"proof/cycle_seal_v1.py","9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
}
def payload():
 return {"artifact_id":"cycle-24-b024-lrc-crt-fourier-class-v1","budget_ordinal":"B024","cycle":24,"record_type":"OBSERVED_FINITE_FOURIER_CLASS_BOUNDARY","recorded_at_utc":"2026-08-04T05:09:29Z","status":"SEALED","epistemic_status":"OBSERVED","outcome":"The complete frozen eight-class CRT/Ramanujan capacity-dual family left all 60 Cycle-23 survivors unresolved; no direct integer deficit was emitted.","claim_boundary":"Only the stated eight class space, class-aggregated selector, one selected width-four partition, floating LP and integerization rule are assessed. This is not a Fourier, width-four, or LRC no-go theorem.","audit":audit(),"proved_interface":{"epistemic_status":"PROVED","statement":"The eight CRT classes are an invertible integer Ramanujan tensor basis and U<W remains a direct leaf-exclusion criterion."},"method_outcome":{"epistemic_status":"OBSERVED","targets":60,"unresolved":60,"objective_min":1.404040404040404,"objective_max":1.5656565656565653,"wall_seconds":52.310638},"companion_decision":{"identity":"/root/darwin_cycle24_review","recommendation":"Seal and open a distinct 12-class quadratic-residue/nonresidue CRT refinement.","strongest_flaw":"58/60 optima collapse to one class, so this family is degenerate and a negative result has only its frozen finite scope.","independent_ideas":["12-class quadratic-residue CRT dual","compact width-five control","later exact cyclotomic-character family"],"final_action":"Seal Cycle 24; do not extend its one-partition/one-LP rule."},"resources":{"worker_cpus":[0,1,2],"reserved_cpu":3,"aggregate_wall_seconds":53,"aggregate_wall_cap_seconds":3600,"peak_rss_kib":75488,"temporary_disk_cap_bytes":21474836480},"runtime":check_runtime("Cycle 24 CRT class"),"frozen_hashes":freeze_inputs(ROOT,INPUTS),"replay":{"run_command":"taskset -c 0-2 .venv/bin/python discovery/lrc_crt_fourier_class.py","audit_command":".venv/bin/python proof/check_cycle_24_crt_fourier_class.py","test_command":".venv/bin/python -m unittest tests.test_cycle_24_crt_fourier_class -v","check_command":".venv/bin/python proof/build_cycle_24_lrc_crt_fourier_class.py --check"},"sealer":{"path":"proof/build_cycle_24_lrc_crt_fourier_class.py","sha256":sha256(Path(__file__))}}
if __name__ == "__main__":
 raise SystemExit(run_cli(description=__doc__,output=OUTPUT,payload_factory=payload))
