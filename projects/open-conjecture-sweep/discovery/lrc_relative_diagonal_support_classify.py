#!/usr/bin/env python3
"""Classify every realizable p199 support-mask triple by the generic buffers."""
from __future__ import annotations

from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path
import time

from lrc_relative_diagonal import PAIRS, terminal_choice, triple_buffers

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle49-relative-diagonal"


def within_group_triples(rows):
    n = len(rows)
    return n * (n - 1) * (n - 2) // 6 + sum(n - 1 for row in rows if row["raw_multiplicity"] >= 2) + sum(row["raw_multiplicity"] >= 3 for row in rows)


def signature_multiplicity(masks, groups):
    counts = Counter(masks)
    if len(counts) == 3:
        result = 1
        for mask in masks: result *= len(groups[mask])
        return result
    if len(counts) == 2:
        repeated = next(mask for mask, count in counts.items() if count == 2)
        single = next(mask for mask, count in counts.items() if count == 1)
        rows = groups[repeated]
        repeated_pairs = len(rows) * (len(rows) - 1) // 2 + sum(row["raw_multiplicity"] >= 2 for row in rows)
        return repeated_pairs * len(groups[single])
    return within_group_triples(groups[masks[0]])


def buffer_status(mask_triple):
    supports = tuple(tuple(owner for owner in range(13) if mask & (1 << owner)) for mask in mask_triple)
    for w in set(supports[0]) & set(supports[1]) & set(supports[2]):
        if not triple_buffers(w, supports):
            return False, {"stage": "TRIPLE", "owner": w}
    for left, right in PAIRS:
        for w in set(supports[left]) & set(supports[right]):
            other = 3 - left - right
            if terminal_choice(left, right, w, supports[other], supports) is None:
                return False, {"stage": f"PAIR_{left}{right}", "owner": w}
    return True, None


def main():
    started = time.monotonic()
    inventory = json.loads((OUT / "inventory.json").read_text())
    groups = defaultdict(list)
    for row in inventory["types"]:
        groups[row["support_mask"]].append(row)
    masks = sorted(groups)
    automatic_type_triples = 0
    residual_type_triples = 0
    good_signatures = 0
    bad = []
    signature_count = 0
    for signature in itertools.combinations_with_replacement(masks, 3):
        multiplicity = signature_multiplicity(signature, groups)
        if not multiplicity:
            continue
        signature_count += 1
        good, failure = buffer_status(signature)
        if good:
            good_signatures += 1
            automatic_type_triples += multiplicity
        else:
            residual_type_triples += multiplicity
            bad.append({"support_masks": list(signature), "support_sizes": [mask.bit_count() for mask in signature], "type_triples": multiplicity, "first_failure": failure})
    assert automatic_type_triples + residual_type_triples == inventory["raw_valid_unordered_triples"]
    result = {
        "status": "PASS", "epistemic_status": "PROVED", "stage": "FULL_SUPPORT_SIGNATURE_CLASSIFICATION",
        "unique_support_masks": len(masks), "realizable_support_signatures": signature_count,
        "universally_buffered_signatures": good_signatures,
        "residual_support_signatures": len(bad),
        "universally_buffered_type_triples": automatic_type_triples,
        "residual_type_triples": residual_type_triples,
        "residual": bad,
        "claim_boundary": "Complete support-level sufficient-hypothesis classification. Residual signatures may still start allowed or have active-specific buffers; no Mobius outcome is inferred.",
        "wall_seconds": time.monotonic() - started,
    }
    assert result["realizable_support_signatures"] <= 5_000_000
    path = OUT / "support-classification.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: result[key] for key in result if key not in ("residual", "claim_boundary")}, sort_keys=True))


if __name__ == "__main__":
    main()
