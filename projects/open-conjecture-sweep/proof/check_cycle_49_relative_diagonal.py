#!/usr/bin/env python3
"""Consolidated audit of Cycle 49's relative diagonal contraction boundary."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle49-relative-diagonal"


def audit():
    controls = json.loads((OUT / "generic-controls.json").read_text())
    inventory = json.loads((OUT / "inventory.json").read_text())
    support = json.loads((OUT / "support-classification.json").read_text())
    deletion = json.loads((OUT / "deletion-classification.json").read_text())
    full = json.loads((OUT / "full-audit.json").read_text())
    independent = json.loads((OUT / "independent-replay.json").read_text())
    terminal = json.loads((OUT / "terminal-audit.json").read_text())
    diagnostic = json.loads((OUT / "independent-diagnostic.json").read_text())
    assert all(row["status"] == "PASS" for row in (controls, inventory, support, deletion, full, independent, terminal))
    total = inventory["raw_valid_unordered_triples"]
    assert total == 382_453_319
    assert support["universally_buffered_type_triples"] + support["residual_type_triples"] == total
    assert support["residual_type_triples"] == deletion["closed_type_triples"] + deletion["unresolved_type_triples"]
    assert deletion["unresolved_type_triples"] == full["counts"]["type_triples"] == 12_208_506
    counts = full["counts"]
    assert counts["structural_closed"] + counts["mobius_attempted"] == counts["type_triples"]
    assert counts["mobius_attempted"] == counts["mobius_already_allowed"] + counts["mobius_contracted"] + counts["BUFFER_INCOMPLETE"]
    independent_counts = dict(independent["counts"])
    assert independent_counts.pop("packet_moves") == full["packet_moves"] == 2
    assert independent_counts == counts
    principal_failures = [row["types"] for row in full["failures"]]
    assert principal_failures == independent["failures"]
    assert len(principal_failures) == full["failure_count"] == counts["BUFFER_INCOMPLETE"] == 5
    assert diagnostic["counts_equal"] and not diagnostic["only_independent"] and not diagnostic["only_principal"]
    assert terminal["types"] == principal_failures[0] == [4, 4, 5]
    assert terminal["classification"] == "BUFFER_INCOMPLETE" and terminal["cube_kernel_dimension"] == 1
    formula_closed = (
        support["universally_buffered_type_triples"]
        + deletion["closed_type_triples"]
        + counts["structural_closed"]
        + counts["mobius_already_allowed"]
        + counts["mobius_contracted"]
    )
    assert formula_closed == total - 5 == 382_453_314
    semantic_upper = (
        support["realizable_support_signatures"]
        + deletion["deletion_combinations_upper"]
        + full["semantic_cache_entries"]
    )
    temporary_disk_bytes = sum(path.stat().st_size for path in OUT.iterdir() if path.is_file())
    conservative_executed_wall_upper = 2_100
    assert semantic_upper < 5_000_000
    assert full["packet_moves"] + independent["counts"]["packet_moves"] < 500_000_000
    assert full["maximum_fraction_bits"] < 131_072
    assert conservative_executed_wall_upper < 7_200
    assert temporary_disk_bytes < 2_147_483_648
    return {
        "status": "PASS", "raw_valid_type_triples": total,
        "frozen_formula_closed": formula_closed, "buffer_incomplete": 5,
        "generic_support_closed": support["universally_buffered_type_triples"],
        "deletion_signature_closed": deletion["closed_type_triples"],
        "residual_counts": counts, "exception_types": principal_failures,
        "first_terminal_classification": terminal["classification"],
        "resources": {
            "semantic_signature_upper": semantic_upper,
            "packet_moves_principal_and_independent": full["packet_moves"] + independent["counts"]["packet_moves"],
            "maximum_fraction_bits": full["maximum_fraction_bits"],
            "conservative_executed_wall_seconds_upper": conservative_executed_wall_upper,
            "temporary_disk_bytes": temporary_disk_bytes,
        },
    }


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True))
