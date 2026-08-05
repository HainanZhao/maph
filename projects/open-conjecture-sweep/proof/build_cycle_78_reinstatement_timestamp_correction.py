"""Seal the metadata-only timestamp correction for C78 reinstatement."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


OUTPUT = ROOT / "artifacts/cycle-78-b078-compatible-spin-endpoint-correction-v3.json"
HASHES = {
    "correction_note": (
        "docs/cycle78_reinstatement_timestamp_correction.md",
        "70d7dbc4e9fda8e07690a91d69ca3376a65f053fcd62ec8a23851c765e8e3260",
    ),
    "superseded_reinstatement": (
        "artifacts/cycle-78-b078-compatible-spin-endpoint-correction-v2.json",
        "07b348daebd84dc7be8f6593acf9e76f336c64e64dd66681dd13b97ea63fa0a1",
    ),
    "reinstatement_sealer": (
        "proof/build_cycle_78_endpoint_reinstatement.py",
        "c6b38a14acb596dcaacba9f809cdd860571028fd160133b3df609dbf7cd15d14",
    ),
    "c78_checker": (
        "proof/check_cycle78_endpoint_interpolation.py",
        "b949c480c8e8acc89e22f28d92fcd87216fc1031e18719ddce7d3302de2b2976",
    ),
    "c79_checker": (
        "proof/check_cycle79_compatible_endpoint_foundation.py",
        "2532c3ccc9cdb5e671c64895c8e1bddb6fcf9a16064a490e9f0a44376fefc426",
    ),
    "scaffold": (
        "proof/cycle_seal_v1.py",
        "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7",
    ),
    "validator": (
        "../../tools/preregistration_check.py",
        "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
    ),
}


def audit() -> dict:
    c78 = json.loads(subprocess.check_output(
        [sys.executable, str(ROOT / HASHES["c78_checker"][0])], text=True
    ))
    c79 = json.loads(subprocess.check_output(
        [sys.executable, str(ROOT / HASHES["c79_checker"][0])], text=True
    ))
    require(c78["status"] == "PASS" and c79["status"] == "PASS", "endpoint replay failed")
    return {"c78_interpolation_status": c78["status"], "c79_endpoint_status": c79["status"]}


def payload() -> dict:
    result = audit()
    return {
        "artifact_id": "cycle-78-b078-compatible-spin-endpoint-correction-v3",
        "budget_ordinal": "B078",
        "cycle": 78,
        "record_type": "CORRECTION_METADATA_TIMESTAMP",
        "recorded_at_utc": "2026-08-05T18:51:06Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "supersedes": "cycle-78-b078-compatible-spin-endpoint-correction-v2",
        "outcome": (
            "C78 reinstatement remains PROVED; this record corrects only "
            "the future recorded_at_utc value in v2."
        ),
        "claim_boundary": (
            "No mathematical, source, replay, or scope claim changes. The "
            "current theorem remains the C78 compatible three-qubit "
            "pair-support arbitrary-qubit result."
        ),
        "correction": {
            "affected_claims": "v2 recorded_at_utc metadata only.",
            "cause": "A fixed timestamp was chosen ahead of the actual write clock.",
            "repair": "Record the observed write-boundary timestamp in this immutable v3 correction.",
        },
        "audit": result,
        "cycle_decision": {
            "decision": "Correct the sealed metadata through a new record; preserve v2 unchanged.",
            "falsifier": "Any changed theorem hash or replay status would show this is not metadata-only.",
        },
        "frozen_hashes": freeze_inputs(
            ROOT, {label: (ROOT / path, digest) for label, (path, digest) in HASHES.items()}
        ),
        "runtime": check_runtime("c78-timestamp-correction"),
        "sealer": {
            "path": "proof/build_cycle_78_reinstatement_timestamp_correction.py",
            "sha256": sha256(Path(__file__)),
        },
        "replay": {
            "audit": (
                "python3 proof/check_cycle79_compatible_endpoint_foundation.py "
                "&& python3 proof/check_cycle78_endpoint_interpolation.py"
            ),
            "check": "python3 proof/build_cycle_78_reinstatement_timestamp_correction.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
