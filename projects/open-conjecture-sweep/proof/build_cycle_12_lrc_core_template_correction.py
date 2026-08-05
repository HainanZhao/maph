"""Issue the metadata-only Cycle 12 timestamp correction."""

from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-12-b012-lrc-core-template-v2.json"
INPUTS = {
    "superseded_record": (ROOT / "artifacts/cycle-12-b012-lrc-core-template-v1.json", "45a160c8a0f843820daabe6a2305c9c9563f25786a3fd4cc556ce2d90b0515c7"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
}


def payload() -> dict:
    runtime = check_runtime("Cycle 12 correction")
    frozen = freeze_inputs(ROOT, INPUTS)
    prior = json.loads(INPUTS["superseded_record"][0].read_text())
    if prior["recorded_at_utc"] != "2026-08-03T22:13:00Z":
        raise RuntimeError("unexpected superseded timestamp")
    return {
        "artifact_id": "cycle-12-b012-lrc-core-template-v2",
        "budget_ordinal": "B012",
        "cycle": 12,
        "record_type": "CORRECTION",
        "recorded_at_utc": "2026-08-03T19:43:48Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "supersedes": "cycle-12-b012-lrc-core-template-v1",
        "error": "The v1 recorded_at_utc value was copied from an inaccurate session summary and lay after the actual creation time.",
        "cause": "The sealer used a summarized timestamp instead of the observed clock at write time.",
        "correction": {
            "field": "recorded_at_utc",
            "incorrect": "2026-08-03T22:13:00Z",
            "corrected": "2026-08-03T19:32:37Z",
            "basis": "Immutable v1 filesystem mtime: 2026-08-03 19:32:37.561656050 +0000.",
        },
        "affected_claims": [],
        "reruns": "Not applicable: the error is metadata-only; v1's mathematical checks, hashes, outcomes, and claim boundary remain unchanged.",
        "runtime": runtime,
        "frozen_hashes": frozen,
        "replay": {"check_command": "python3 proof/build_cycle_12_lrc_core_template_correction.py --check"},
        "sealer": {"path": "proof/build_cycle_12_lrc_core_template_correction.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
