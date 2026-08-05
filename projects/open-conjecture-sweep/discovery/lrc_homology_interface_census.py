#!/usr/bin/env python3
"""Cycle 41 census of support/deletion interfaces for homology reduction."""
from __future__ import annotations

from collections import Counter, defaultdict
import json
import multiprocessing
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_ownership_functional as c38
import lrc_signed_ownership_moments as c40

OUT = ROOT / "discovery/out/cycle41-multiplied-ideal/interface-census.json"


def coordinate(index):
    resource.setrlimit(resource.RLIMIT_AS, (1_600_000_000, 1_600_000_000))
    return c40.coordinate_classes(index)


def main():
    started = time.monotonic()
    c38.prepare()
    complete_types = sorted({row[0] for root in c38._TYPE_ROWS for rows in root.values() for row in rows})
    type_id = {value: index for index, value in enumerate(complete_types)}
    masks = [sum(1 << owner for owner, signature in enumerate(value) if signature) for value in complete_types]
    c40._TYPE_ID = type_id
    c40._TYPE_MASKS = masks
    with multiprocessing.Pool(3) as pool:
        rows = pool.map(coordinate, range(13), chunksize=1)
    deleted = defaultdict(int)
    for owner, row in enumerate(rows):
        for pair in row["rank_two_pairs"]:
            deleted[tuple(pair)] |= 1 << owner
    mask_classes = sorted(set(masks))
    options = defaultdict(set)
    for left_mask in mask_classes:
        for right_mask in mask_classes:
            if left_mask <= right_mask:
                options[(left_mask, right_mask)].add(0)
    for (left, right), diagonal in deleted.items():
        key = tuple(sorted((masks[left], masks[right])))
        options[key].add(diagonal)
    option_counts = Counter(len(values) for values in options.values())
    maximum_key = max(options, key=lambda key: len(options[key]))
    payload = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "complete_types": len(complete_types),
        "owner_mask_classes": len(mask_classes),
        "owner_count_distribution": dict(sorted(Counter(mask.bit_count() for mask in masks).items())),
        "mask_pair_classes": len(options),
        "deletion_option_count_distribution": dict(sorted(option_counts.items())),
        "maximum_deletion_options_for_one_mask_pair": len(options[maximum_key]),
        "maximum_option_mask_pair": list(maximum_key),
        "maximum_option_values": sorted(options[maximum_key]),
        "sum_deletion_options": sum(len(values) for values in options.values()),
        "claim_boundary": "Exact census of owner-support masks and realized rank-two deleted-diagonal options; it does not enumerate compatible type triples or homology classes.",
        "wall_seconds": time.monotonic() - started,
    }
    temporary = OUT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT)
    print(json.dumps({key: payload[key] for key in ("status", "complete_types", "owner_mask_classes", "mask_pair_classes", "deletion_option_count_distribution", "maximum_deletion_options_for_one_mask_pair", "sum_deletion_options", "wall_seconds")}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
