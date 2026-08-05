#!/usr/bin/env python3
"""Conservatively close residual support signatures using exact pair deletions."""
from __future__ import annotations

from collections import defaultdict
import itertools
import json
import multiprocessing
from pathlib import Path
import resource
import time

import lrc_cech_actual as base
import lrc_signed_ownership_moments as moments
from lrc_cube_rewrite import normalized_cube
from lrc_relative_diagonal import PAIRS, cell_allowed, triple_buffers

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle49-relative-diagonal"
DELETION_VARIANTS = {}


def coordinate(owner):
    resource.setrlimit(resource.RLIMIT_AS, (2_000_000_000, 2_000_000_000))
    return moments.coordinate_classes(owner)


def exact_pair_buffers(left, right, w, supports, pair_deleted, triple_deleted):
    other = 3 - left - right
    for terminal in supports[other]:
        if terminal == w:
            continue
        for c in supports[other]:
            if c in (w, terminal):
                continue
            pivot = tuple(w if index in (left, right) else c for index in range(3))
            terminal_cell = tuple(w if index in (left, right) else terminal for index in range(3))
            found = False
            for a in supports[left]:
                if a == w:
                    continue
                for b in supports[right]:
                    if b == w:
                        continue
                    alternatives = [None, None, None]
                    alternatives[left], alternatives[right], alternatives[other] = a, b, terminal
                    cube = normalized_cube(pivot, tuple(alternatives))
                    forbidden = {cell for cell in cube if not cell_allowed(cell, pair_deleted, triple_deleted)}
                    if forbidden <= {pivot, terminal_cell}:
                        found = True
                        break
                if found:
                    break
            if not found:
                break
        else:
            return True
    return False


def status_for(support_masks, deletions):
    supports = tuple(tuple(owner for owner in range(13) if mask & (1 << owner)) for mask in support_masks)
    pair_deleted = {pair: deletions[index] for index, pair in enumerate(PAIRS)}
    # Conservative: treat every common owner as triple-deleted. Exact rank-three
    # information can only remove an obligation from this audit.
    common = support_masks[0] & support_masks[1] & support_masks[2]
    active_triples = common & (deletions[0] | deletions[1] | deletions[2] | common)
    for w in range(13):
        if active_triples & (1 << w) and not triple_buffers(w, supports):
            return False, {"stage": "TRIPLE", "owner": w}
    for index, (left, right) in enumerate(PAIRS):
        for w in range(13):
            if deletions[index] & (1 << w) and not exact_pair_buffers(left, right, w, supports, pair_deleted, common):
                return False, {"stage": f"PAIR_{left}{right}", "owner": w}
    return True, None


def classify(row):
    masks = tuple(row["support_masks"])
    variants = [
        DELETION_VARIANTS[tuple(sorted((masks[0], masks[1])))],
        DELETION_VARIANTS[tuple(sorted((masks[0], masks[2])))],
        DELETION_VARIANTS[tuple(sorted((masks[1], masks[2])))],
    ]
    tested = 0
    for deletions in itertools.product(*variants):
        tested += 1
        good, failure = status_for(masks, deletions)
        if not good:
            return {"closed": False, "tested": tested, "first_deletions": list(deletions), "first_failure": failure}
    return {"closed": True, "tested": tested}


def main():
    global DELETION_VARIANTS
    started = time.monotonic()
    base.prepare_fast()
    complete = sorted({row[0] for root in base.c38._TYPE_ROWS for rows in root.values() for row in rows})
    type_id = {value: index for index, value in enumerate(complete)}
    masks = [sum(1 << owner for owner, signature in enumerate(value) if signature) for value in complete]
    moments._TYPE_ID = type_id
    moments._TYPE_MASKS = masks
    with multiprocessing.Pool(3) as pool:
        coordinate_rows = pool.map(coordinate, range(13), chunksize=1)
    original = defaultdict(int)
    for owner, data in enumerate(coordinate_rows):
        for pair in data["rank_two_pairs"]:
            original[tuple(pair)] |= 1 << owner
    grouped = defaultdict(list)
    for index, mask in enumerate(masks):
        grouped[mask].append(index)
    variants = defaultdict(set)
    support_masks = sorted(grouped)
    for ordinal, left_mask in enumerate(support_masks):
        for right_mask in support_masks[ordinal:]:
            key = (left_mask, right_mask)
            for left in grouped[left_mask]:
                for right in grouped[right_mask]:
                    pair = tuple(sorted((left, right)))
                    variants[key].add(original.get(pair, 0))
    DELETION_VARIANTS = {key: tuple(sorted(values)) for key, values in variants.items()}

    support_result = json.loads((OUT / "support-classification.json").read_text())
    residual = support_result["residual"]
    combination_upper = 0
    for row in residual:
        m = row["support_masks"]
        combination_upper += (
            len(DELETION_VARIANTS[tuple(sorted((m[0], m[1])))])
            * len(DELETION_VARIANTS[tuple(sorted((m[0], m[2])))])
            * len(DELETION_VARIANTS[tuple(sorted((m[1], m[2])))])
        )
    assert combination_upper <= 5_000_000
    with multiprocessing.Pool(3) as pool:
        classified = pool.map(classify, residual, chunksize=32)
    rows = [{**source, **outcome} for source, outcome in zip(residual, classified, strict=True)]
    closed = [row for row in rows if row["closed"]]
    unresolved = [row for row in rows if not row["closed"]]
    result = {
        "status": "PASS", "epistemic_status": "PROVED", "stage": "CONSERVATIVE_PAIR_DELETION_SIGNATURE_AUDIT",
        "pair_support_classes": len(DELETION_VARIANTS),
        "maximum_deletion_variants": max(map(len, DELETION_VARIANTS.values())),
        "deletion_combinations_upper": combination_upper,
        "input_residual_signatures": len(residual),
        "closed_signatures": len(closed),
        "unresolved_signatures": len(unresolved),
        "closed_type_triples": sum(row["type_triples"] for row in closed),
        "unresolved_type_triples": sum(row["type_triples"] for row in unresolved),
        "unresolved": unresolved,
        "claim_boundary": "Conservative over all pair-deletion combinations for each support signature and treats every common owner as triple-deleted. Closure is universal; unresolved rows require correlated type/rank-three/Mobius analysis.",
        "wall_seconds": time.monotonic() - started,
    }
    path = OUT / "deletion-classification.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: result[key] for key in result if key not in ("unresolved", "claim_boundary")}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
