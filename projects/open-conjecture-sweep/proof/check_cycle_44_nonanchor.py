#!/usr/bin/env python3
"""Lightweight cross-record audit for Cycle 44."""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle44-nonanchor-coupling"


def audit():
    selection = json.loads((OUT / "selection.json").read_text(encoding="utf-8"))
    coupling = json.loads((OUT / "coupling.json").read_text(encoding="utf-8"))
    replay = json.loads((OUT / "independent-replay.json").read_text(encoding="utf-8"))
    assert selection["status"] == coupling["status"] == replay["status"] == "PASS"
    assert selection["deduplicated_candidate_pool"] == replay["candidate_pool"] == 103_289
    assert selection["preliminary_interfaces"] == replay["preliminary_interfaces"] == 7_928
    assert selection["selected_interfaces"] == coupling["selected_interfaces"] == replay["selected_interfaces"] == 2_000
    assert coupling["face_classes"] == replay["face_classes"] == 7_754
    assert coupling["pair_classes"] == replay["pair_classes"] == 11_387
    assert coupling["face_coefficients"] == replay["face_coefficients_checked"] == 29_557
    assert sum(len(row["cycle"]) for row in coupling["interface_records"]) == replay["cycle_coefficients_checked"] == 30_677
    assert sum(len(row["fill"]) for row in coupling["interface_records"]) == replay["cone_coefficients_checked"] == 8_291
    routes = Counter(row["route"] for row in coupling["interface_records"])
    assert routes == {"EXPLICIT_CONE": 1_528, "GF2_H2_ZERO_EXISTENCE": 472}
    h2 = Counter(row["h2_gf2"] for row in coupling["interface_records"])
    assert h2[0] == 1_971 and sum(value for key, value in h2.items() if key) == 29
    assert all(row["route"] == "EXPLICIT_CONE" for row in coupling["interface_records"] if row["h2_gf2"])
    assert coupling["canonical_fills"] == 2_000
    assert coupling["canonical_failures"] == replay["nonzero_h2_without_cone"] == 0
    assert coupling["elimination_only_fills"] == 0
    assert coupling["coherent_escalation_required"] is False
    assert replay["selection_replayed"] is True
    return {"status": "PASS", "selected_interfaces": 2_000, "explicit_cones": 1_528, "h2_zero_existence_fills": 472, "nonzero_h2_interfaces": 29, "canonical_failures": 0}


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True))
