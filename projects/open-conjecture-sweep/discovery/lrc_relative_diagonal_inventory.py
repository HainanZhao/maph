#!/usr/bin/env python3
"""Freeze Cycle 49's complete-type support inventory and residual-domain size."""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import time

import lrc_cech_actual as base

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle49-relative-diagonal"


def valid_triple_count(indices, multiplicities):
    indices = tuple(indices)
    count = len(indices)
    distinct = count * (count - 1) * (count - 2) // 6
    doubled = sum(count - 1 for value in indices if multiplicities[value] >= 2)
    tripled = sum(multiplicities[value] >= 3 for value in indices)
    return distinct + doubled + tripled


def main():
    started = time.monotonic()
    base.prepare_fast()
    complete = sorted({row[0] for root in base.c38._TYPE_ROWS for rows in root.values() for row in rows})
    type_id = {value: index for index, value in enumerate(complete)}
    masks = [sum(1 << owner for owner, signature in enumerate(value) if signature) for value in complete]
    raw = []
    for point in range(base.c38._COVERAGE.shape[0]):
        value = tuple(
            sum(1 << offset for offset, digit in enumerate(base.c38._ALLOWED[coordinate]) if base.c38._COVERAGE[point, coordinate, digit])
            for coordinate in range(13)
        )
        raw.append(type_id[value])
    multiplicities = Counter(raw)
    all_indices = tuple(range(len(complete)))
    large = tuple(index for index, mask in enumerate(masks) if mask.bit_count() >= 5)
    total = valid_triple_count(all_indices, multiplicities)
    large_total = valid_triple_count(large, multiplicities)
    result = {
        "status": "PASS", "epistemic_status": "PROVED", "stage": "FULL_TYPE_SUPPORT_INVENTORY",
        "complete_types": len(complete), "raw_occurrences": len(raw),
        "support_size_counts": dict(sorted(Counter(mask.bit_count() for mask in masks).items())),
        "low_support_types": len(complete) - len(large),
        "raw_valid_unordered_triples": total,
        "automatic_support_five_triples": large_total,
        "residual_low_support_triples": total - large_total,
        "maximum_raw_multiplicity": max(multiplicities.values()),
        "types": [
            {"index": index, "support_mask": mask, "support_size": mask.bit_count(), "raw_multiplicity": multiplicities[index]}
            for index, mask in enumerate(masks)
        ],
        "claim_boundary": "Complete support/multiplicity inventory only; pair transports, deletions, Mobius defects, and active buffers are not classified.",
        "wall_seconds": time.monotonic() - started,
    }
    assert result["residual_low_support_triples"] <= 250_000_000
    path = OUT / "inventory.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: result[key] for key in result if key not in ("types", "claim_boundary")}, sort_keys=True))


if __name__ == "__main__":
    main()
