#!/usr/bin/env python3
"""Cycle 45 signature-realizable abstract countermodel lift."""
from __future__ import annotations

from collections import Counter
import hashlib
import itertools
import json
import multiprocessing
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
from lrc_morse_abstract import evaluate

OUT = ROOT / "discovery/out/cycle45-critical-projection"
SEED = "cycle45-critical-projection-v1"
PAIRS = tuple(itertools.combinations(range(4), 2))
TRIPLES = tuple(itertools.combinations(range(4), 3))


def bytes_for(counter):
    return b"".join(hashlib.sha256(f"{SEED}:{counter}:{block}".encode("ascii")).digest() for block in range(3))


def signature_model(counter):
    raw = bytes_for(counter)
    signatures = [[raw[3 * part + owner] & 7 for owner in range(3)] for part in range(4)]
    for part in range(4):
        if not any(signatures[part]):
            owner = raw[12 + part] % 3
            digit = raw[16 + part] % 3
            signatures[part][owner] = 1 << digit
    supports = tuple(tuple(owner for owner in range(3) if signatures[part][owner]) for part in range(4))
    distinguished = tuple(supports[part][raw[20 + part] % len(supports[part])] for part in range(4))
    for left, right in PAIRS:
        if distinguished[left] == distinguished[right]:
            owner = distinguished[left]
            if not signatures[left][owner] & signatures[right][owner]:
                return None
    pair_values = []
    for left, right in PAIRS:
        deleted = 0
        for owner in range(3):
            if signatures[left][owner] and signatures[right][owner] and not signatures[left][owner] & signatures[right][owner]:
                deleted |= 1 << owner
        pair_values.append(deleted)
    triple_values = []
    for parts in TRIPLES:
        deleted = 0
        for owner in range(3):
            values = [signatures[part][owner] for part in parts]
            if not all(values) or values[0] & values[1] & values[2]:
                continue
            if all(values[a] & values[b] for a, b in itertools.combinations(range(3), 2)):
                deleted |= 1 << owner
        triple_values.append(deleted)
    key = (supports, distinguished, tuple(pair_values), tuple(triple_values))
    signature_key = (tuple(tuple(values) for values in signatures), distinguished)
    return signature_key, key


def evaluate_signature(job):
    signature_key, key, counter = job
    row = evaluate((key, counter))
    row["local_signatures"] = [list(values) for values in signature_key[0]]
    return row


def main():
    started = time.monotonic()
    OUT.mkdir(parents=True, exist_ok=True)
    retained = {}
    discarded_selected_pair = 0
    for counter in range(50_000, 100_000):
        model = signature_model(counter)
        if model is None:
            discarded_selected_pair += 1
            continue
        signature_key, key = model
        retained.setdefault(signature_key, (key, counter))
    jobs = [(signature_key, key, counter) for signature_key, (key, counter) in retained.items()]
    jobs.sort(key=lambda item: item[2])
    with multiprocessing.Pool(3) as pool:
        rows = pool.map(evaluate_signature, jobs, chunksize=16)
    counts = Counter(row["status"] for row in rows)
    errors = [row for row in rows if row["status"] not in ("FACE_INCONSISTENT", "ZERO_PROJECTION", "NONZERO_PROJECTION")]
    if errors:
        result = {"status": "ERROR", "epistemic_status": "PROVED", "first_error": errors[0], "hash_counters": 50000, "deduplicated_signature_models": len(jobs), "outcome_counts": dict(sorted(counts.items())), "wall_seconds": time.monotonic() - started}
    else:
        admissible = [row for row in rows if row["status"] != "FACE_INCONSISTENT"]
        countermodels = sorted((row for row in admissible if row["projection_nonzero"]), key=lambda row: (json.dumps(row["local_signatures"]), json.dumps(row["descriptor"], sort_keys=True), row["counter"]))
        nonboundary = [row for row in countermodels if row["projection_status"] == "NONBOUNDARY"]
        aggregate_cells = sum(row["cells"] for row in admissible)
        if aggregate_cells > 10_000_000 or time.monotonic() - started > 7200:
            raise RuntimeError("Cycle 45 signature-lift cap")
        result = {"status": "PASS", "epistemic_status": "PROVED", "stage": "SIGNATURE_REALIZABLE_ABSTRACT_COUNTERMODELS", "hash_counters": 50000, "discarded_selected_pair_models": discarded_selected_pair, "deduplicated_signature_models": len(jobs), "admissible_face_models": len(admissible), "face_inconsistent_models": counts["FACE_INCONSISTENT"], "zero_projection_models": counts["ZERO_PROJECTION"], "nonzero_projection_models": counts["NONZERO_PROJECTION"], "nonboundary_projection_models": len(nonboundary), "extended_zero_projection_models": sum(not row["extended_projection_nonzero"] for row in admissible), "extended_nonzero_projection_models": sum(bool(row["extended_projection_nonzero"]) for row in admissible), "extended_nonboundary_projection_models": sum(row["extended_projection_status"] == "NONBOUNDARY" for row in admissible), "aggregate_simplices": aggregate_cells, "least_countermodel": countermodels[0] if countermodels else None, "least_nonboundary_countermodel": nonboundary[0] if nonboundary else None, "claim_boundary": "Three owner labels and three local digits with distinct labeled parts. Signature realizability is necessary local ownership geometry, not realization by the frozen p199 type corpus or its globally selected marginals.", "wall_seconds": time.monotonic() - started}
    temporary = OUT / "signature-abstract-models.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "signature-abstract-models.json")
    print(json.dumps({key: result[key] for key in result if key not in ("least_countermodel", "least_nonboundary_countermodel", "first_error")}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
