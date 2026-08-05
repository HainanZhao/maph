"""Seal Cycle 26's compact width-five transfer boundary."""
from __future__ import annotations
from pathlib import Path
from check_cycle_26_width_five_transfer import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle26-width-five-transfer"
OUTPUT = ROOT / "artifacts/cycle-26-b026-lrc-width-five-transfer-v1.json"
INPUTS = {
 "preregistration":(ROOT/"docs/cycle-26-b026-lrc-width-five-transfer-preregistration-v1.md","bec59f99545f9318646437ea8ddaec91c3ae394b0c5019e7f2520c778ac2992a"),
 "source_artifact":(ROOT/"artifacts/cycle-22-b022-lrc-width-four-v1.json","512ecc6f854e2400b6ee733fd2d91f8860de50a522820703d44290ad53aab58d"),
 "prior_artifact":(ROOT/"artifacts/cycle-25-b025-lrc-quadratic-crt-v1.json","61fa41306155dbc55e6853434f2c0d567a6a6a2409c6847934dda902ebf80c68"),
 "source_results":(ROOT/"discovery/out/cycle22-width-four/stage-b-results.tsv","a89a0532292f188cedc0f5b41a04cb68e2ebcae09ed9514ffba6f0f0941b0c07"),
 "prior_results":(ROOT/"discovery/out/cycle25-quadratic-crt/results.tsv","aa78578f2e54e7045d6dcf63e1278805d04057e48cd2b3981a4853889074e3d3"),
 "cnf_base4":(ROOT/"discovery/out/cycle11-certified-sat/p199/004.cnf","ea4356bd1ff5cdf06fb5504411d0ca57ddc8b3056dc8281c8025d1d24ef60648"),
 "cnf_base3":(ROOT/"discovery/out/cycle11-certified-sat/p199/003.cnf","e07cde8b14f19bf2094e2643ac43c6aad6c6d62ade399db270968a479d0ee6c4"),
 "coupled":(ROOT/"discovery/lrc_coupled_incidence.py","b40d9ff5077b40caaeda0e1622d456ce9e9673c9451bc6cd19d2b58286853469"),
 "direct":(ROOT/"discovery/lrc_pair_choice.py","f3faa9c3152467243ec1acfe27310c857cadbbe40b565c7cf51fb6e47318d55a"),
 "width_four":(ROOT/"discovery/lrc_width_four_stage_a.py","3faee2712066bb15014b87b47f58a7be914298965dbf32678ee36485e9a0a9b9"),
 "soundness":(ROOT/"proof/cycle_26_width_five_transfer_soundness.md","02e79f0f8ae363a1d970332b17b9ac88c2213b0a04d26a4a09a1f6b2096c4d38"),
 "search":(ROOT/"discovery/lrc_width_five_transfer.py","5eae6c4da627a559723e500633868d9f0fbcad8a22f9f82be0807067fd2b9845"),
 "audit":(ROOT/"proof/check_cycle_26_width_five_transfer.py","c4d25155f1edb278b6a033f61b10159c0cd33335e6b294f4c26b271c3ac8c8f0"),
 "test":(ROOT/"tests/test_cycle_26_width_five_transfer.py","8cfa4a5a6992d8598360b31eabac55ac428ca30a9e259200ae1cfb9a0b0be40b"),
 "control":(OUT/"control.json","79ea9450a131e1c1ab2f5ee14bdf1f39f99c43760930d459e5b9ada51248acdb"),
 "results":(OUT/"results.tsv","cbc18286a26ddc1b8c3cc8c2378db211d0c5b400be9c1368393972d8cdbef219"),
 "summary":(OUT/"result.txt","7e0f5fcdd6c2ab157b8fa4a0827fa16fe0e033219b37e6ebe77b38ef4cdc210a"),
 "timing":(OUT/"run.time","776f572f49e1e7d17f5c794acc9b7424056322255f3feed351ebf314029df742"),
 "scaffold":(ROOT/"proof/cycle_seal_v1.py","9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
}
def payload():
 return {"artifact_id":"cycle-26-b026-lrc-width-five-transfer-v1","budget_ordinal":"B026","cycle":26,"record_type":"OBSERVED_FINITE_WIDTH_FIVE_TRANSFER_BOUNDARY","recorded_at_utc":"2026-08-04T05:48:00Z","status":"SEALED","epistemic_status":"OBSERVED","outcome":"The compact 5+4+4 transfer of Cycle 22's proved 176-point weight left all 60 Cycle-25 survivors unresolved; no fresh direct integer deficit was emitted.","claim_boundary":"Only one inherited sparse weight and one deterministic restriction-selected 5+4+4 partition per target are assessed. This is not a width-five, capacity-dual, or LRC no-go theorem.","audit":audit(),"proved_interface":{"epistemic_status":"PROVED","statement":"The Cycle-22 source witness replays exactly and direct U<W remains a named-leaf exclusion criterion for every frozen coordinate partition."},"method_outcome":{"epistemic_status":"OBSERVED","targets":60,"unresolved":60,"minimum_nondeficit_gap":20681,"maximum_nondeficit_gap":49231,"wall_seconds":1.438721},"companion_decision":{"identity":"/root/darwin_cycle25_short","scope_review":"The source certificate is exactly recovered; the all-60 fixed-geometry sweep is independently replayed but tests only one inherited sparse weight.","recommendation":"Seal Cycle 26 and open distinct Cycle 27 for a fresh width-five time-weight LP.","strongest_flaw":"The restriction rule yields the same 0-4|5-8|9-12 geometry for all 60 targets, and source recovery does not validate a fresh optimizer.","falsifier":"A source-mode recovery, independent option/separation, or direct U<W replay mismatch invalidates the affected fresh-LP claim.","independent_ideas":["fresh width-five time-weight LP","semantic primal lift after equivalence theorem","individual/cyclotomic character dual"],"final_action":"Seal this transfer family; do not treat it as a width-five no-go."},"resources":{"worker_cpus":[0,1,2],"reserved_cpu":3,"aggregate_wall_seconds":2,"aggregate_wall_cap_seconds":3600,"peak_rss_kib":132888,"temporary_disk_cap_bytes":21474836480},"runtime":check_runtime("Cycle 26 width-five transfer"),"frozen_hashes":freeze_inputs(ROOT,INPUTS),"replay":{"run_command":"taskset -c 0-2 .venv/bin/python discovery/lrc_width_five_transfer.py","audit_command":"taskset -c 0 .venv/bin/python proof/check_cycle_26_width_five_transfer.py","test_command":".venv/bin/python -m unittest tests.test_cycle_26_width_five_transfer -v","check_command":".venv/bin/python proof/build_cycle_26_lrc_width_five_transfer.py --check"},"sealer":{"path":"proof/build_cycle_26_lrc_width_five_transfer.py","sha256":sha256(Path(__file__))}}
if __name__ == "__main__":
 raise SystemExit(run_cli(description=__doc__,output=OUTPUT,payload_factory=payload))
