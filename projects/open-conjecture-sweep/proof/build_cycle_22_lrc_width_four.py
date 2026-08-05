"""Seal Cycle 22's proved width-four leaf exclusion and performance boundary."""

from __future__ import annotations

from pathlib import Path

from check_cycle_22_width_four import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle22-width-four"
OUTPUT = ROOT / "artifacts/cycle-22-b022-lrc-width-four-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-22-b022-lrc-width-four-preregistration-v1.md", "7055659239bf06d439b78b2417f6de8307b28fa7e16ddb58df23db98119b3ea8"),
    "prior_artifact": (ROOT / "artifacts/cycle-21-b021-lrc-coupled-incidence-v1.json", "360daaf46d9f4442a65cce29d8011d05ea529ad0e59a7f16dc6c12b6b66a0200"),
    "soundness": (ROOT / "proof/cycle_22_width_four_soundness.md", "d93a3e0c5471480c27bf74154759b3d9e01f508371fb1963f11dd90831c9063c"),
    "stage_a": (ROOT / "discovery/lrc_width_four_stage_a.py", "3faee2712066bb15014b87b47f58a7be914298965dbf32678ee36485e9a0a9b9"),
    "stage_b": (ROOT / "discovery/lrc_width_four_stage_b.py", "d114e70f59d7289e0cb97c1747ee0868068d65a7c5567fdc6063ed5a374b89df"),
    "exhaustive_transfer": (ROOT / "discovery/lrc_width_four_exhaustive_transfer.py", "812f271894444c0aa30048ffff5cf59955bd2f8c67ea84af820ddcce5296eded"),
    "audit": (ROOT / "proof/check_cycle_22_width_four.py", "479c7f3728f26b038b6cfc82236ecbcc7549d015ee01099c6edad97d093327c1"),
    "test": (ROOT / "tests/test_cycle_22_width_four.py", "a1d0810af14ae6e86f7a35b7db657ccaa8a6191cb6f326ed3759c49ed4505a96"),
    "stage_a_results": (OUT / "stage-a.tsv", "9fbd72611852d8b3080142174b7bc677282af8ea13eebb7b5a84983489255bd2"),
    "stage_a_summary": (OUT / "stage-a-result.txt", "61ef40c1884d1113d0c635c32f66a35ebc6208fa9b71161e9fe1c27f8b0644e6"),
    "stage_a_timing": (OUT / "stage-a.time", "9ed38b77a362a31ac907247f04b4ae49ea933fc28b188565ebfda8ea228fba2e"),
    "stage_b_trials": (OUT / "stage-b-trials.tsv", "2d1d6004488efed95e4b0c0f69a94dab346b6399191669459f640a2a6e6f37bb"),
    "stage_b_results": (OUT / "stage-b-results.tsv", "a89a0532292f188cedc0f5b41a04cb68e2ebcae09ed9514ffba6f0f0941b0c07"),
    "stage_b_summary": (OUT / "stage-b-result.txt", "5de52f74aa44b12def31d56aeca0eeab00765f85176d24d1147ed19ebfc640fd"),
    "stage_b_timing": (OUT / "stage-b.time", "c2462e15fc99f120e46a8498e460bfb2f24622024ea41c0b290cfd84a1d43d98"),
    "exhaustive_results": (OUT / "exhaustive-transfer.tsv", "ee3eef30911447774dd930197e990fa7eb0bc544c64234581fda72653edbfb84"),
    "exhaustive_summary": (OUT / "exhaustive-transfer-result.txt", "13fbad355512e7a92041bd2c76e9ef8cde1ca45c7f9000a778d04a1a49e216ac"),
    "exhaustive_timing": (OUT / "exhaustive-transfer.time", "d4b82a4162766e7d7e79cdfc36de9657c455a8b6ad4ab683601a22b779937606"),
    "audit_output": (OUT / "audit-final.json", "8572c53a725a426b92aed1bad511f3de668c54dbaf354a47843428d95238e170"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
}


def payload() -> dict:
    return {
        "artifact_id": "cycle-22-b022-lrc-width-four-v1",
        "budget_ordinal": "B022",
        "cycle": 22,
        "record_type": "PROVED_LEAF_CERTIFICATE_AND_METHOD_BOUNDARY",
        "recorded_at_utc": "2026-08-04T01:38:29Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "An independently replayed width-four integer deficit excludes frozen base-4 leaf 952 with W=65,528, U=65,440, and margin 88. Sixty leaves remain unresolved.",
        "claim_boundary": "Exactly one named leaf is newly excluded. Neither base, F_1, J, nor LRC(13) is closed. Stage-A and exhaustive-transfer failures are bounded OBSERVED method outcomes, not width-four no-go theorems.",
        "audit": audit(),
        "stage_a": {"epistemic_status": "OBSERVED", "direct_transfer_trials": 9150, "certificates": 0, "wall_seconds": 109.638946},
        "stage_b": {"epistemic_status": "PROVED", "lp_trials": 602, "certificates": [{"base_index": 4, "leaf_ordinal": 952, "W": 65528, "U": 65440, "margin": 88}], "unresolved": 60, "wall_seconds": 1514.048832},
        "exhaustive_transfer": {"epistemic_status": "OBSERVED", "status": "AGGREGATE_WALL_CAP", "partially_executed": [{"base_index": 4, "leaf_ordinal": 78, "partitions": 339}, {"base_index": 4, "leaf_ordinal": 79, "partitions": 472}, {"base_index": 4, "leaf_ordinal": 80, "partitions": 529}], "unstarted": 57, "certificates": 0, "wall_seconds": 1811.959842, "boundary": "The run does not assess the full all-four-subset transfer family."},
        "companion_decision": {"identity": "/root/decision_companion_2", "scope_review": "One named leaf is proved; negative searches concern only frozen policies and 60 leaves remain.", "recommendation": "Continue Cycle 22 with exhaustive direct replay of the new weight; if sparse, seal and open adaptive width-four column generation.", "strongest_flaw": "The initial policy forces the three most restricted coordinates and misses contradictions centered elsewhere.", "falsifier": "Any target mask, allowed-digit, weight, or U/W replay mismatch invalidates the affected transfer.", "independent_ideas": ["all-four-subset direct transfer", "adaptive width-four column generation", "later Fourier obstruction"], "final_action": "The exhaustive continuation hit its wall cap without a new certificate; seal Cycle 22 and open adaptive column generation."},
        "resources": {"aggregate_wall_seconds": 3435.64762, "aggregate_wall_cap_seconds": 3600, "peak_rss_kib": 2343552, "worker_cpus": [0, 1, 2], "reserved_cpu": 3, "temporary_disk_cap_bytes": 21474836480},
        "runtime": check_runtime("Cycle 22 width four"),
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "replay": {"stage_a_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_width_four_stage_a.py", "stage_b_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_width_four_stage_b.py", "exhaustive_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_width_four_exhaustive_transfer.py", "audit_command": ".venv/bin/python proof/check_cycle_22_width_four.py", "check_command": ".venv/bin/python proof/build_cycle_22_lrc_width_four.py --check", "test_command": ".venv/bin/python -m unittest tests.test_cycle_22_width_four -v"},
        "sealer": {"path": "proof/build_cycle_22_lrc_width_four.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
