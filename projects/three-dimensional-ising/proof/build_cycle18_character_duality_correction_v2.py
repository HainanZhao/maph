#!/usr/bin/env python3
"""Correct Cycle 18 by removing volatile peak memory from sealed replay."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof import build_cycle18_character_duality_correction as v1  # noqa: E402
from proof.cycle_seal_v1 import freeze_inputs, run_cli, sha256  # noqa: E402


OUTPUT = ROOT / "artifacts/cycle-18-b18-character-duality-correction-v2.json"
EXTRA = {
    "seal_correction": (
        "discovery/cycle18-character-duality-seal-correction.md",
        "5467db95daefe227f4bd8c0256f10c4bb3031d30af24b1a5f608d60d64b534fc",
    ),
    "v1_artifact": (
        "artifacts/cycle-18-b18-character-duality-correction-v1.json",
        "69714b68f58ca6e5acc74adc367775058780a428fed5cc2d95eed0815d98baf3",
    ),
    "v1_builder": (
        "proof/build_cycle18_character_duality_correction.py",
        "d6700aa8f947785b5a20a3924cf3328d3a779f7370bd80c4916d1558d8658972",
    ),
}


def payload():
    result = v1.payload()
    result["exact_replay"]["polynomial_grid_cores"].pop("peak_rss_kib", None)
    result.update({
        "artifact_id": "cycle-18-b18-character-duality-correction-v2",
        "supersedes": "cycle-18-b18-character-duality-correction-v1",
        "sealing_correction": {
            "error": "v1 included a newly measured peak_rss_kib field",
            "affected_claims": "none",
            "mathematical_fields_changed": False,
        },
        "sealer": {
            "path": "proof/build_cycle18_character_duality_correction_v2.py",
            "sha256": sha256(Path(__file__)),
        },
        "replay": {
            **result["replay"],
            "artifact_check": "python3 proof/build_cycle18_character_duality_correction_v2.py --check",
        },
    })
    result["frozen_hashes"].update(
        freeze_inputs(ROOT, {k: (ROOT / p, h) for k, (p, h) in EXTRA.items()})
    )
    return result


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
