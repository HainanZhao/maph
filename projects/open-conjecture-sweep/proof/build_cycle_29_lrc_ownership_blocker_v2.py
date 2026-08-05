"""Correct Cycle 29 v1's future recorded-at timestamp; preserve its mathematics."""
from __future__ import annotations

from pathlib import Path

from build_cycle_29_lrc_ownership_blocker import payload as v1_payload
from cycle_seal_v1 import run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-29-b029-lrc-ownership-blocker-v2.json"
PRIOR = ROOT / "artifacts/cycle-29-b029-lrc-ownership-blocker-v1.json"
PRIOR_SHA256 = "faf6df7c21d0dd09a83528c158970dee29d80acb9a7aa4c0de35c256bd93757c"


def payload() -> dict[str, object]:
    if sha256(PRIOR) != PRIOR_SHA256:
        raise RuntimeError("Cycle 29 v1 changed")
    value = v1_payload()
    value.update({
        "artifact_id": "cycle-29-b029-lrc-ownership-blocker-v2",
        "record_type": "CORRECTED_PROVED_SEMANTIC_INTERFACE",
        "recorded_at_utc": "2026-08-04T14:04:38Z",
        "correction": {
            "epistemic_status": "PROVED",
            "supersedes": "cycle-29-b029-lrc-ownership-blocker-v1",
            "prior_sha256": PRIOR_SHA256,
            "error": "v1 recorded_at_utc was accidentally set eleven minutes in the future.",
            "cause": "A timestamp was typed rather than read from the pre-seal UTC clock.",
            "affected_claims": "Metadata only; no mathematical statement, input, output, hash, audit, or decision changed.",
        },
        "sealer": {"path": "proof/build_cycle_29_lrc_ownership_blocker_v2.py", "sha256": sha256(Path(__file__))},
    })
    value["replay"] = dict(value["replay"])
    value["replay"]["check_command"] = ".venv/bin/python proof/build_cycle_29_lrc_ownership_blocker_v2.py --check"
    return value


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
