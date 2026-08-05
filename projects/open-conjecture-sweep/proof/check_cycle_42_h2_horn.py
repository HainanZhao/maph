#!/usr/bin/env python3
"""Lightweight cross-record audit for the sealed Cycle 42 boundary."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle42-h2-horn"


def audit():
    census = json.loads((OUT / "gf2-census.json").read_text(encoding="utf-8"))
    first = json.loads((OUT / "first-rational-coupling.json").read_text(encoding="utf-8"))
    replay = json.loads((OUT / "independent-replay.json").read_text(encoding="utf-8"))
    assert census["status"] == first["status"] == replay["status"] == "PASS"
    assert census["raw_interfaces"] == replay["raw_interfaces"] == 3954
    assert census["distinct_interfaces"] == replay["distinct_interfaces"] == 409
    assert census["nonzero_h2_gf2"] == census["nonzero_h2_q"] == replay["nonzero_h2_gf2"] == replay["nonzero_h2_q"] == 3893
    assert census["maximum_h2_q"] == replay["maximum_h2_q"] == 40
    assert census["field_dimension_disagreements"] == replay["field_dimension_disagreements"] == 0
    assert census["maximum_rational_coefficient_bits"] == replay["maximum_rational_coefficient_bits"] == 1
    assert census["relevant_rank_three_classes"] == 0
    assert first["types"] == replay["first_interface"]["types"] == [2, 5, 14, 5]
    assert first["complex"] == {"vertices": 7, "edges": 17, "triangles": 16, "tetrahedra": 4, "rank_d2_q": 11, "rank_d3_q": 4, "h2_q": 1}
    assert first["canonical_class"]["pairing"] == replay["first_interface"]["canonical_pairing"] == [-1, 1]
    assert first["moment_filling_status"] == replay["first_interface"]["moment_filling_status"] == "CONSISTENT"
    assert len(first["moment_fill"]) == replay["first_interface"]["moment_fill_nonzero"] == 1
    return {"status": "PASS", "raw_interfaces": 3954, "distinct_interfaces": 409, "nonzero_h2_q": 3893, "maximum_h2_q": 40, "first_moment_filling_status": "CONSISTENT"}


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True))
