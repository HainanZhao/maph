"""Seal Cycle 35's exact rank-one local product measure."""
from __future__ import annotations

from pathlib import Path

from check_cycle_35_local_product_measure import EXPECTED_NORMALS, audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle35-local-product-measure"
OUTPUT = ROOT / "artifacts/cycle-35-b035-lrc-local-product-measure-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-35-b035-lrc-local-product-measure-preregistration-v1.md", "26ffb74fcd58f430e58d394c998fa1d254df8f40c4ee1e8ffacd4254cebd1fdf"),
    "prior_artifact": (ROOT / "artifacts/cycle-34-b034-lrc-rational-tensor-v1.json", "5c894d635cdd3a53bb31b7529d896a2e23806ad20270aa7421f59b2872f7601c"),
    "idea_selection": (ROOT / "discovery/cycle35_local_product_measure_idea_selection.md", "62751225cfb251402374a02d408b31699c63ad2ed500b68e3c9b5cfd796d7076"),
    "first_engine": (ROOT / "discovery/lrc_local_product_measure.py", "11c211b763641dc07ed29331a1ce6aee7f01405c1c8f39052ee02ae6be0793f6"),
    "optimized_engine": (ROOT / "discovery/lrc_local_product_measure_ondemand.py", "623f908e81495eac57e3775060b0960be9cd157b5e3976af7f22ca6ab20e36e8"),
    "independent_replay": (ROOT / "proof/replay_cycle_35_local_product_measure_independent.py", "73696d0d02a0f06fc821af1bb223cdde6ce499e01b70877173c54e7307e2b8fc"),
    "audit": (ROOT / "proof/check_cycle_35_local_product_measure.py", "6a699263ef547f4f254b54920c76bef352fd66d3bafc0611b1116a7fe6867c10"),
    "soundness": (ROOT / "proof/cycle_35_local_product_measure_soundness.md", "b87dc4a22be55fe41599d0a581d34cdca13956d38bc502915c9283e6eca549b2"),
    "test": (ROOT / "tests/test_cycle_35_local_product_measure.py", "8779d1ce2a9d588ec4be1e78e27d4454546b4400c3c5f88f20ebd4c1d32ca382"),
    "first_result": (OUT / "first-tranche.json", "05986442a15bca0642919a94c3f0d5a4ea0845cd46c0a18d2d42c4497c9af4ba"),
    "primary_result": (OUT / "result.json", "5cd276e434303161fdaef7736e47e24ede5039ba248d04829d141ac97940ae9d"),
    "independent_result": (OUT / "independent-replay.json", "276ed32ca9bd34969cc0bedd70645c4dad490be17a0f54147c69f44801f9277e"),
    "first_timing": (ROOT / "discovery/out/cycle35-local-product-measure-first-tranche.time", "e0676fd9957c96894bc9dd9f9693902516ece566f1c368c6aa06564be211d79e"),
    "second_timing": (ROOT / "discovery/out/cycle35-local-product-measure-second-tranche.time", "23ddb52b2a461ab1f25626f6757d6790b9cd1723b98a0f380f64d634f1d2d5de"),
    "independent_timing": (OUT / "independent-replay.time", "52f814ac1444d4b5fb7a39650e47445b098f15e6ce801c967d22092556bba7f4"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
}


def payload() -> dict[str, object]:
    checked = audit()
    return {
        "artifact_id": "cycle-35-b035-lrc-local-product-measure-v1",
        "budget_ordinal": "B035",
        "cycle": 35,
        "record_type": "PROVED_RANK_ONE_FULL_GRID_OBSTRUCTION",
        "recorded_at_utc": "2026-08-04T15:24:51Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "A compact rank-one integer signed measure on the full p199 base-4/leaf-78 digit grid has mass one and annihilates every one of the 1,394 direct uncovered predicates. Therefore their degree-zero rational span cannot contain the constant function.",
        "claim_boundary": "This is a full-grid structural obstruction for rank-one signed measures and degree-zero direct-predicate identities on one p199 leaf. It is not a leaf exclusion, a positive-degree result, a probability measure, an ownership-calculus result, or a proof of LRC(13).",
        "audit": checked,
        "breakthrough": {
            "epistemic_status": "PROVED",
            "local_normals_by_allowed_option_offset": EXPECTED_NORMALS,
            "local_masses": [1] * 13,
            "global_mass": 1,
            "predicate_columns": 1394,
            "minimum_killing_coordinates": 1,
            "maximum_killing_coordinates": 13,
            "singly_killed_predicates": 181,
            "single_killer_counts_by_coordinate": [27, 19, 50, 13, 4, 12, 4, 9, 17, 5, 9, 9, 3],
            "maximum_absolute_local_coefficient": 5,
            "all_predicates_annihilated": True,
            "independent_direct_mask_replay": "PASS",
        },
        "contained_path": {
            "epistemic_status": "OBSERVED",
            "first_representation": "complete enumeration of all lower local flats",
            "outcome": "CAP at exactly 1,000,000 states; no p199 algebraic claim",
            "optimization": "equivalent on-demand exact matroid cover search",
            "optimized_states": 26,
        },
        "correction_containment": {
            "issue": "The first favorable output labeled span-forced killed-label counts as the final normals' cover counts.",
            "impact": "No predicate-annihilation or mass claim was affected; independently computed actual normal counts are larger on coordinates 3-12.",
            "resolution": "Before sealing, the live output separated span_guaranteed_cover_count from exact cover_count and both direct-mask routes were rerun.",
        },
        "cycle_decision": {
            "companion_identity": "/root/darwin_cycle25_short",
            "outcome": "SEALED_FOR_DEGREE_ONE_PSEUDOEXPECTATION_QUESTION",
            "scope_review": "The rank-one functional is a short symbolic reason for the degree-zero no-go, but negative coefficients prevent probability or entropy interpretations and nothing yet transfers across leaves.",
            "strongest_flaw_resolved": "An independent direct-mask construction verified all 1,394 local-dot annihilations and all thirteen unit masses after the count-label discrepancy was corrected.",
            "independent_ideas": ["lift the signed functional to a degree-one pseudoexpectation", "defer transfer across 60 leaves until a CRT transport law is proved", "use ownership auxiliaries only if escaping degree-one multipliers expose a missing semantic"],
            "falsifier": "Any local mass other than one or any predicate with nonzero local dot product in all coordinates invalidates the product functional.",
            "next_action": "Open Cycle 36 to test an exact degree-one pseudoexpectation extending the product functional, starting from the 181 predicates with a unique killing coordinate.",
        },
        "resources": {"worker_cpus": [0, 1, 2], "reserved_cpu": 3, "aggregate_wall_seconds": 430.48, "largest_peak_rss_kib": 673348, "memory_max_bytes": 4294967296, "temporary_disk_cap_bytes": 5368709120},
        "runtime": check_runtime("Cycle 35 local product measure"),
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "replay": {
            "first_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_local_product_measure.py",
            "optimized_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_local_product_measure_ondemand.py",
            "independent_command": "taskset -c 0-2 .venv/bin/python proof/replay_cycle_35_local_product_measure_independent.py",
            "audit_command": ".venv/bin/python proof/check_cycle_35_local_product_measure.py",
            "test_command": ".venv/bin/python -m unittest tests.test_cycle_35_local_product_measure -v",
            "check_command": ".venv/bin/python proof/build_cycle_35_lrc_local_product_measure.py --check",
        },
        "sealer": {"path": "proof/build_cycle_35_lrc_local_product_measure.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
