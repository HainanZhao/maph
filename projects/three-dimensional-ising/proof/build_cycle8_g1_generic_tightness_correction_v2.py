#!/usr/bin/env python3
"""Correct the Cycle 8 G1 artifact by removing volatile replay measurements."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.build_cycle8_g1_generic_tightness import payload as v1_payload  # noqa: E402
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256  # noqa: E402


OUTPUT = ROOT / "artifacts/cycle-8-b11-g1-generic-tightness-v2.json"
CORRECTION_HASHES = {
    "superseded_v1": (
        ROOT / "artifacts/cycle-8-b11-g1-generic-tightness-v1.json",
        "58de615a086dd1215fea2950d3c1031e2906189d22effe1d3ce0a6895c2e7f87",
    ),
    "correction_note": (
        ROOT / "docs/cycle8-g1-generic-tightness-correction-v2.md",
        "4c6c33e53a890badfd34709f1df4396435c3911ecaddb289017e9b31d4f373eb",
    ),
    "superseded_builder": (
        ROOT / "proof/build_cycle8_g1_generic_tightness.py",
        "5f4e2a4b568644fa5a5c2c1c37157f28d6711f067afc66e6bd75fce47268addd",
    ),
}
VOLATILE_KEYS = {"wall_seconds", "peak_rss_kib"}


def stable(value):
    if isinstance(value, dict):
        return {
            key: stable(item)
            for key, item in value.items()
            if key not in VOLATILE_KEYS
        }
    if isinstance(value, list):
        return [stable(item) for item in value]
    return value


def payload() -> dict[str, object]:
    result = stable(v1_payload())
    result.update({
        "artifact_id": "cycle-8-b11-g1-generic-tightness-v2",
        "status": "SEALED_CORRECTION",
        "record_type": "LANE_B_GENERIC_NONUNIFORM_TIGHTNESS_CORRECTION",
        "supersedes": "cycle-8-b11-g1-generic-tightness-v1",
        "correction": {
            "error": "v1 embedded volatile wall-time and peak-RSS measurements",
            "mathematical_claims_changed": False,
            "repair": "recursively omit only wall_seconds and peak_rss_kib from replay payloads",
        },
        "correction_inputs": freeze_inputs(ROOT, CORRECTION_HASHES),
        "runtime": check_runtime("cycle-8-g1-generic-tightness-correction-v2"),
        "sealer": {
            "path": "proof/build_cycle8_g1_generic_tightness_correction_v2.py",
            "sha256": sha256(Path(__file__)),
        },
    })
    result["replay"]["artifact_check"] = (
        "python3 proof/build_cycle8_g1_generic_tightness_correction_v2.py --check"
    )
    return result


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
