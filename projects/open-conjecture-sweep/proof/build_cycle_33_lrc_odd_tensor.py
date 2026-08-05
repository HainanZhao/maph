"""Seal Cycle 33's exact degree-zero GF(3)/GF(5) tensor boundaries."""
from __future__ import annotations

from pathlib import Path

from check_cycle_33_odd_tensor import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle33-odd-tensor"
OUTPUT = ROOT / "artifacts/cycle-33-b033-lrc-odd-tensor-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-33-b033-lrc-odd-tensor-preregistration-v1.md", "0f95a5140bc72ba285a02a7c5229623c54a702832dd339835434ba5e92b3b948"),
    "prior_artifact": (ROOT / "artifacts/cycle-32-b032-lrc-gf2-tensor-v1.json", "29dabc1897392ab0f1f7cd97368afbfb4e0f15e10c7d7176efe32e67f1df996f"),
    "idea_selection": (ROOT / "discovery/cycle33_odd_tensor_idea_selection.md", "0af4b61bc460b11ce5de448072a8ba918c3e58c9b0848451d94abaa58d0d0eb5"),
    "primary_engine": (ROOT / "discovery/lrc_odd_tensor.py", "437f7850e33ac851bf114a474b65d87044d7fd674c401d789aa876cf94d391e5"),
    "independent_replay": (ROOT / "proof/replay_cycle_33_odd_tensor_independent.py", "cb37ae3e00a77900dbf84d9bce6e5f076980cb54eca3f59f98dee336038a56d7"),
    "audit": (ROOT / "proof/check_cycle_33_odd_tensor.py", "0f174979684819286cbddb37eda46a671aae545ee899e3b7459fbefb43bc501c"),
    "soundness": (ROOT / "proof/cycle_33_odd_tensor_soundness.md", "610b437df79f0fd0399d47ad2084cfa9a9ee51f9e8b43f470794011476aa0028"),
    "test": (ROOT / "tests/test_cycle_33_odd_tensor.py", "91304d59fdff641eaa75b25bd2e8b2ba68061da0a11e7ed8e6424270c9a20673"),
    "primary_result": (OUT / "result.json", "e74c7a899448c09a5bb56df7717a85bdefc5a718c3d17a4d5ccfa6fff54140d8"),
    "independent_result": (OUT / "independent-replay.json", "d933c275a3eb9b5b04f0e2d4cd7dbf83cba2497e7fcdebf0b2c0ddcec0395eb4"),
    "primary_timing": (ROOT / "discovery/out/cycle33-odd-tensor.time", "c4013410417176298ff2d1bdcc2b8da0a79a7cf69416704065be986719f641c3"),
    "independent_timing": (OUT / "independent-replay.time", "460ca806fa1601c91f35208d544419d14b755b43995e87d56d8122f22789cab5"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
}


def payload() -> dict[str, object]:
    checked = audit()
    return {
        "artifact_id": "cycle-33-b033-lrc-odd-tensor-v1",
        "budget_ordinal": "B033",
        "cycle": 33,
        "record_type": "PROVED_DEGREE_ZERO_ODD_FIELD_BOUNDARIES",
        "recorded_at_utc": "2026-08-04T14:46:17Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "No degree-zero uncovered-tensor identity exists for p199 base 4 / leaf 78 over GF(3) or GF(5): normalized 802-row and 985-row left-null certificates respectively recombine all 1,394 predicate columns to zero and the RHS to one.",
        "claim_boundary": "This classifies only degree-zero combinations over GF(3) and GF(5) of the negation-deduplicated direct uncovered predicates for one H11 control and one p199 leaf. It does not constrain rational coefficients, other characteristics, positive degree, ownership polynomial calculus, the leaf itself, or LRC(13).",
        "audit": checked,
        "finite_results": {
            "epistemic_status": "PROVED",
            "h11": {"base": [1, 1, 1], "assignments": 64, "identity": "F_12=1", "fields": [3, 5]},
            "p199": {
                "base_index": 4,
                "leaf_ordinal": 78,
                "predicate_columns": 1394,
                "evaluation_rows": 4243,
                "assignment_hash": checked["assignment_hash"],
                "GF3": {"rank": 1228, "contradiction_rows": 802, "degree_zero_identity": False},
                "GF5": {"rank": 1228, "contradiction_rows": 985, "degree_zero_identity": False},
                "independent_highest_pivot_replays": "INCONSISTENT_IN_BOTH_FIELDS",
            },
        },
        "cycle_decision": {
            "companion_identity": "/root/darwin_cycle25_short",
            "outcome": "SEALED_FOR_DISTINCT_CHARACTERISTIC_ZERO_QUESTION",
            "scope_review": "The exact provenance replays make these genuine field-specific no-gos. They do not compose into a rational no-go because a rational solution may have denominators divisible by every tested prime.",
            "strongest_flaw": "Coefficient-height growth may defeat exact rational reconstruction; a cap would be computational only and cannot be promoted to nonexistence.",
            "independent_ideas": ["seek an exact integer left-null certificate by sparse fraction-free or modular reconstruction", "defer degree-one GF(2) until an exact column census", "defer ownership auxiliaries because they enlarge the state without demonstrated low-degree benefit"],
            "falsifier": "An independently checked rational solution to the 4,243 restricted equations falsifies the restricted rational obstruction; a lifted null vector is valid only if every integer predicate-column sum is zero and its integer RHS sum is nonzero.",
            "next_action": "Open Cycle 34 for exact rational degree-zero linear algebra on the same frozen 4,243-by-1,394 evaluation interface.",
        },
        "resources": {"worker_cpus": [0, 1, 2], "reserved_cpu": 3, "aggregate_wall_seconds": 11.03, "largest_peak_rss_kib": 30588, "memory_max_bytes": 4294967296, "temporary_disk_cap_bytes": 5368709120},
        "runtime": check_runtime("Cycle 33 odd tensor boundaries"),
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "replay": {
            "primary_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_odd_tensor.py",
            "independent_command": "taskset -c 0-2 .venv/bin/python proof/replay_cycle_33_odd_tensor_independent.py",
            "audit_command": ".venv/bin/python proof/check_cycle_33_odd_tensor.py",
            "test_command": ".venv/bin/python -m unittest tests.test_cycle_33_odd_tensor -v",
            "check_command": ".venv/bin/python proof/build_cycle_33_lrc_odd_tensor.py --check",
        },
        "sealer": {"path": "proof/build_cycle_33_lrc_odd_tensor.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
