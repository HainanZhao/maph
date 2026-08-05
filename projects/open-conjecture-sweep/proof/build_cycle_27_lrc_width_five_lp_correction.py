"""Issue the metadata-only Cycle 27 sealing-timestamp correction."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-27-b027-lrc-width-five-lp-v2.json"
INPUTS = {
    "superseded_record": (ROOT / "artifacts/cycle-27-b027-lrc-width-five-lp-v1.json", "b9d74f33edb435795ee14dba60adcbef80790bd5d603ac8a1914f10cb430538d"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
}


def payload() -> dict[str, object]:
    prior = json.loads(INPUTS["superseded_record"][0].read_text(encoding="utf-8"))
    require(prior["recorded_at_utc"] == "2026-08-04T06:44:00Z", "unexpected v1 timestamp")
    return {
        "artifact_id": "cycle-27-b027-lrc-width-five-lp-v2",
        "budget_ordinal": "B027", "cycle": 27, "record_type": "CORRECTION",
        "recorded_at_utc": "2026-08-04T07:31:56Z", "status": "SEALED",
        "epistemic_status": "OBSERVED", "supersedes": "cycle-27-b027-lrc-width-five-lp-v1",
        "error": "The v1 recorded_at_utc field predated the actual immutable write.",
        "cause": "The builder used a preselected human timestamp rather than the observed clock at write time.",
        "correction": {"field": "recorded_at_utc", "incorrect": "2026-08-04T06:44:00Z", "corrected": "2026-08-04T07:31:27Z", "basis": "Immutable v1 filesystem mtime: 2026-08-04 07:31:27.464218291 +0000."},
        "affected_claims": [],
        "reruns": "Not applicable: this metadata-only correction leaves v1 mathematical checks, frozen hashes, result, and claim boundary unchanged.",
        "runtime": check_runtime("Cycle 27 timestamp correction"),
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "replay": {"check_command": ".venv/bin/python proof/build_cycle_27_lrc_width_five_lp_correction.py --check"},
        "sealer": {"path": "proof/build_cycle_27_lrc_width_five_lp_correction.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
