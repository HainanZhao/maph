#!/usr/bin/env python3
"""Consolidated exact audit for Cycle 50's single deletion-aware theorem."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle50-deletion-aware-packet"
C49 = ROOT / "discovery/out/cycle49-relative-diagonal"


def audit():
    controls = json.loads((OUT / "controls.json").read_text())
    principal = json.loads((OUT / "full-pattern-census.json").read_text())
    independent = json.loads((OUT / "independent-replay.json").read_text())
    c49 = json.loads((C49 / "full-audit.json").read_text())
    assert controls["status"] == "PASS" and independent["status"] == "PASS"
    assert principal["status"] == "THEOREM_FAIL"
    assert principal["counts"] == independent["counts"]
    assert principal["packet_moves"] == independent["packet_moves"] == 5
    principal_failures = [{key: row[key] for key in ("types", "support_sizes", "status", "stage", "pivot")} for row in principal["failures"]]
    assert principal_failures == independent["failures"]
    assert principal["counts"] == {"BUFFER_INCOMPLETE": 2, "CONTRACTED": 29048, "selected_type_triples": 29050}
    assert [row["types"] for row in principal_failures] == [[4, 5, 35], [4, 6, 35]]
    assert all(row["support_sizes"] == [2, 2, 4] and row["stage"] == "PAIR_01" for row in principal_failures)
    assert {tuple(row["types"]) for row in c49["failures"]} == {(4, 4, 5), (4, 4, 6), (4, 4, 64), (4, 5, 35), (4, 6, 35)}
    assert all(tuple(sorted(row["support_sizes"])) in {(2, 2, 2), (2, 2, 4)} for row in c49["failures"])
    return {
        "status": "THEOREM_FAIL", "epistemic_status": "PROVED",
        "selected_type_triples": principal["counts"]["selected_type_triples"],
        "contracted": principal["counts"]["CONTRACTED"], "buffer_incomplete": principal["counts"]["BUFFER_INCOMPLETE"],
        "remaining_failures": principal_failures,
        "reason": "The frozen deletion-aware triple packet fixes three of the five C49 residuals, but the unchanged pair-fiber stage still fails on two (2,2,4) interfaces. The sole authorized theorem is false; no second packet family is permitted.",
        "resources": {
            "packet_moves_principal_and_independent": principal["packet_moves"] + independent["packet_moves"],
            "maximum_fraction_bits": principal["maximum_fraction_bits"],
            "principal_wall_seconds": principal["wall_seconds"],
            "independent_wall_seconds": independent["wall_seconds"],
            "temporary_disk_bytes": sum(path.stat().st_size for path in OUT.iterdir() if path.is_file()),
        },
    }


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True))
