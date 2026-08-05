#!/usr/bin/env python3
"""Lightweight cross-record audit for Cycle 43's selected coupling theorem."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle43-moment-h2-coupling"


def audit():
    primary = json.loads((OUT / "canonical-coupling.json").read_text(encoding="utf-8"))
    replay = json.loads((OUT / "independent-replay.json").read_text(encoding="utf-8"))
    assert primary["status"] == replay["status"] == "PASS"
    assert primary["raw_interfaces"] == replay["raw_interfaces"] == primary["canonical_fills"] == 3954
    assert primary["structural_complexes"] == replay["structural_complexes"] == 409
    assert primary["unordered_face_classes"] == replay["face_classes"] == 11852
    assert primary["oriented_pair_classes"] == replay["pair_classes"] == 10516
    assert primary["canonical_face_nonzero"] == replay["face_coefficients_checked"] == 11926
    assert sum(len(row["cycle"]) for row in primary["interface_records"]) == replay["cycle_coefficients_checked"] == 15890
    assert sum(len(row["fill"]) for row in primary["interface_records"]) == replay["fill_coefficients_checked"] == 4026
    assert primary["canonical_failures"] == replay["canonical_failures"] == 0
    assert primary["maximum_face_bits"] == primary["maximum_fill_bits"] == 1
    assert primary["maximum_fill_nonzero"] == 7
    assert primary["coherent_escalation_required"] is False
    face_distribution = {}
    for row in primary["face_tensors"]:
        face_distribution[len(row["coefficients"])] = face_distribution.get(len(row["coefficients"]), 0) + 1
    fill_distribution = {}
    for row in primary["interface_records"]:
        fill_distribution[len(row["fill"])] = fill_distribution.get(len(row["fill"]), 0) + 1
    assert face_distribution == {1: 11839, 3: 1, 7: 12}
    assert fill_distribution == {1: 3942, 7: 12}
    return {"status": "PASS", "raw_interfaces": 3954, "canonical_fills": 3954, "canonical_failures": 0, "face_support_distribution": face_distribution, "fill_support_distribution": fill_distribution}


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True))
