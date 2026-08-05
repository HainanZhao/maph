#!/usr/bin/env python3
"""Cycle 46 exact owner-star Cech quotient on actual Morse residuals."""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
import itertools
import json
import multiprocessing
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_ownership_functional as c38
from lrc_cech_total import owner_star_cover, solve_injected_class
from lrc_morse_critical_projection import build_complex

OUT = ROOT / "discovery/out/cycle46-global-cech-quotient"
TYPE_ID = {}
TARGET_TYPES = set()
TARGET_PAIRS = set()
TARGET_TRIPLES = set()
WORK_DATA = None


def prepare_fast():
    """Cycle 38's exact interface preparation without parsing all p199 bases."""
    c29 = json.loads((ROOT / "discovery/out/cycle29-ownership-blocker/result.json").read_text())["p199"]
    c38._COORDINATES = c29["coordinates"]
    with c38.coupled.P199_INPUT.open(encoding="utf-8") as handle:
        for index, line in enumerate(handle):
            if index == 4:
                base = tuple(map(int, line.split()))
                break
        else:
            raise AssertionError("missing p199 base 4")
    allowed = tuple(tuple(row) for row in c38.direct.allowed_digits(base, 78))
    coverage = c38.width4.raw_coverage(c38.direct.CNFS[4])
    if coverage.shape != (2786, 13, 14):
        raise AssertionError("p199 coverage shape")
    global_types = [
        tuple(sum(1 << offset for offset, digit in enumerate(allowed[coordinate]) if coverage[point, coordinate, digit]) for coordinate in range(13))
        for point in range(2786)
    ]
    c38._ALLOWED = allowed
    c38._COVERAGE = coverage
    c38._TYPE_ROWS = []
    for owner in range(13):
        grouped = defaultdict(lambda: defaultdict(list))
        for point, global_type in enumerate(global_types):
            grouped[global_type[owner]][global_type].append(point)
        frozen = {signature: tuple((global_type, len(points), min(points)) for global_type, points in sorted(types.items())) for signature, types in grouped.items()}
        expected = {int(row["signature"]): int(row["count"]) for row in c38._COORDINATES[owner]["signature_classes"]}
        actual = {signature: sum(row[1] for row in rows) for signature, rows in frozen.items()}
        if actual != expected:
            raise AssertionError("complete-type local signature projection")
        c38._TYPE_ROWS.append(frozen)


def coordinate_target(owner):
    resource.setrlimit(resource.RLIMIT_AS, (1_600_000_000, 1_600_000_000))
    pairs = set()
    triples = set()
    for pattern in c38._COORDINATES[owner]["patterns"]:
        rank = int(pattern["rank"])
        if rank not in (2, 3):
            continue
        groups = []
        for signature in pattern["signatures"]:
            ids = sorted({TYPE_ID[row[0]] for row in c38._TYPE_ROWS[owner][int(signature)] if TYPE_ID[row[0]] in TARGET_TYPES})
            if not ids:
                break
            groups.append(ids)
        if len(groups) != rank:
            continue
        for values in itertools.product(*groups):
            key = tuple(sorted(values))
            if rank == 2 and key in TARGET_PAIRS:
                pairs.add(key)
            elif rank == 3 and key in TARGET_TRIPLES:
                triples.add(key)
    return owner, sorted(pairs), sorted(triples)


def parse_chain(serialized):
    return {
        tuple(tuple(vertex) for vertex in cell): Fraction(numerator, denominator)
        for cell, numerator, denominator in serialized
    }


def reconstruct(records, workers):
    global TYPE_ID, TARGET_TYPES, TARGET_PAIRS, TARGET_TRIPLES
    TARGET_TYPES = {value for record in records for value in record["types"]}
    TARGET_PAIRS = {tuple(sorted((types[a], types[b]))) for record in records for types in [record["types"]] for a, b in itertools.combinations(range(4), 2)}
    TARGET_TRIPLES = {tuple(sorted(types[index] for index in positions)) for record in records for types in [record["types"]] for positions in itertools.combinations(range(4), 3)}
    cache_path = OUT / "target-structure-cache.json"
    if cache_path.is_file():
        cache = json.loads(cache_path.read_text())
        if cache["target_types"] != sorted(TARGET_TYPES) or cache["target_pairs"] != [list(row) for row in sorted(TARGET_PAIRS)] or cache["target_triples"] != [list(row) for row in sorted(TARGET_TRIPLES)]:
            raise AssertionError("target structure cache selector mismatch")
        return cache["masks"], cache["distinguished"], {(left, right): deleted for left, right, deleted in cache["pair_deleted"]}, {(a, b, c): deleted for a, b, c, deleted in cache["triple_deleted"]}
    prepare_fast()
    complete_types = sorted({row[0] for owner_rows in c38._TYPE_ROWS for rows in owner_rows.values() for row in rows})
    TYPE_ID = {value: index for index, value in enumerate(complete_types)}
    if len(complete_types) != 1318:
        raise AssertionError("complete type count")
    masks = [sum(1 << owner for owner, signature in enumerate(value) if signature) for value in complete_types]
    with multiprocessing.Pool(workers) as pool:
        rows = pool.map(coordinate_target, range(13), chunksize=1)
    pair_deleted = defaultdict(int)
    triple_deleted = defaultdict(int)
    for owner, pairs, triples in rows:
        for pair in pairs:
            pair_deleted[tuple(pair)] |= 1 << owner
        for triple in triples:
            triple_deleted[tuple(triple)] |= 1 << owner
    prior = json.loads((ROOT / "discovery/out/cycle41-multiplied-ideal/zero-support-closure.json").read_text())
    distinguished = []
    for values in prior["singleton_marginals_by_complete_type"]:
        if len(values) != 1 or values[0][1:] != [1, 1]:
            raise AssertionError("nonintegral distinguished marginal")
        distinguished.append(int(values[0][0]))
    cache = {
        "status": "PASS", "epistemic_status": "PROVED",
        "target_types": sorted(TARGET_TYPES), "target_pairs": [list(row) for row in sorted(TARGET_PAIRS)], "target_triples": [list(row) for row in sorted(TARGET_TRIPLES)],
        "masks": masks, "distinguished": distinguished,
        "pair_deleted": [[left, right, deleted] for (left, right), deleted in sorted(pair_deleted.items())],
        "triple_deleted": [[a, b, c, deleted] for (a, b, c), deleted in sorted(triple_deleted.items())],
        "claim_boundary": "Target-only exact reconstruction for the frozen Cycle 45 residual type classes.",
    }
    OUT.mkdir(parents=True, exist_ok=True)
    temporary = cache_path.with_suffix(cache_path.suffix + ".tmp")
    temporary.write_text(json.dumps(cache, indent=2, sort_keys=True) + "\n")
    temporary.replace(cache_path)
    return masks, distinguished, dict(pair_deleted), dict(triple_deleted)


def process(record, masks, distinguished, pair_global, triple_global):
    types = tuple(record["types"])
    supports = tuple(tuple(owner for owner in range(13) if masks[value] & (1 << owner)) for value in types)
    pair_deleted = {(a, b): pair_global.get(tuple(sorted((types[a], types[b]))), 0) for a, b in itertools.combinations(range(4), 2)}
    triple_deleted = {parts: triple_global.get(tuple(sorted(types[part] for part in parts)), 0) for parts in itertools.combinations(range(4), 3)}
    cells, all_cells = build_complex(supports, pair_deleted, triple_deleted)
    cycle = parse_chain(record["extended_projection"])
    chosen = None
    coverage = []
    for pivot in range(4):
        owners, cover = owner_star_cover(all_cells, pivot)
        union = set().union(*cover) if cover else set()
        uncovered = sorted(cell for cell in cycle if cell not in union)
        coverage.append({"pivot": pivot, "owners": owners, "cover_members": len(cover), "uncovered_nonzero": len(uncovered), "first_uncovered": uncovered[0] if uncovered else None})
        if not uncovered and chosen is None:
            chosen = (pivot, owners, cover)
    if chosen is None:
        return {"source": record["source"], "ordinal": record["ordinal"], "types": list(types), "status": "UNCOVERED_ALL_PIVOTS", "coverage": coverage}
    pivot, owners, cover = chosen
    total = solve_injected_class(all_cells, cover, cycle)
    return {
        "source": record["source"], "ordinal": record["ordinal"], "types": list(types),
        "status": total["status"], "direct_status": total["status"], "selected_pivot": pivot,
        "selected_owners": owners, "coverage": coverage,
        "complex_cells": {str(dimension): len(values) for dimension, values in cells.items()},
        "total": total,
    }


def worker_init(masks, distinguished, pairs, triples):
    global WORK_DATA
    resource.setrlimit(resource.RLIMIT_AS, (3_000_000_000, 3_000_000_000))
    WORK_DATA = (masks, distinguished, pairs, triples)


def process_worker(record):
    return process(record, *WORK_DATA)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", action="store_true")
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args()
    if not 1 <= args.workers <= 3:
        raise ValueError("workers must be in 1..3")
    started = time.monotonic()
    source = json.loads((ROOT / "discovery/out/cycle45-critical-projection/actual-corpus-layered.json").read_text())
    residuals = sorted((row for row in source["records"] if row["extended_projection_nonzero"]), key=lambda row: (row["source"], row["ordinal"]))
    if len(residuals) != 457:
        raise AssertionError("residual count")
    selected = [residuals[0], residuals[len(residuals) // 2], residuals[-1]] if args.benchmark else residuals
    masks, distinguished, pairs, triples = reconstruct(residuals, args.workers)
    checkpoint_path = OUT / "actual-checkpoint.json"
    selector = [[row["source"], row["ordinal"]] for row in selected]
    rows = []
    if not args.benchmark and checkpoint_path.is_file():
        checkpoint = json.loads(checkpoint_path.read_text())
        if checkpoint["selector"] != selector:
            raise AssertionError("actual checkpoint selector mismatch")
        rows = checkpoint["records"]
        if [[row["source"], row["ordinal"]] for row in rows] != selector[: len(rows)]:
            raise AssertionError("actual checkpoint prefix mismatch")
    remaining = selected[len(rows) :]
    with multiprocessing.Pool(args.workers, initializer=worker_init, initargs=(masks, distinguished, pairs, triples)) as pool:
        for row in pool.imap(process_worker, remaining, chunksize=1):
            rows.append(row)
            if not args.benchmark:
                checkpoint = {"status": "LIVE", "selector": selector, "records": rows}
                temporary_checkpoint = checkpoint_path.with_suffix(checkpoint_path.suffix + ".tmp")
                temporary_checkpoint.write_text(json.dumps(checkpoint, indent=2, sort_keys=True) + "\n")
                temporary_checkpoint.replace(checkpoint_path)
            print(json.dumps({"completed": len(rows), "total": len(selected), "source": row["source"], "ordinal": row["ordinal"], "status": row["status"]}), flush=True)
    result = {
        "status": "PASS",
        "epistemic_status": "OBSERVED" if args.benchmark else "PROVED",
        "stage": "PREFLIGHT_BENCHMARK" if args.benchmark else "ACTUAL_GLOBAL_CECH_QUOTIENT",
        "selected_residuals": len(selected), "complete_residual_corpus": len(residuals),
        "target_types": len(TARGET_TYPES), "target_pair_classes": len(TARGET_PAIRS), "target_triple_classes": len(TARGET_TRIPLES),
        "reconstructed_deleted_pairs": len(pairs), "reconstructed_deleted_triples": len(triples),
        "outcome_counts": {status: sum(row["status"] == status for row in rows) for status in sorted({row["status"] for row in rows})},
        "records": rows,
        "claim_boundary": "The benchmark is outcome-blind performance evidence only." if args.benchmark else "Exact classification of the frozen 457 residuals only; not a universal p199 theorem or LRC(13).",
        "wall_seconds": time.monotonic() - started,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / ("actual-benchmark-fast.json" if args.benchmark else "actual-quotient-localized.json")
    temporary = target.with_suffix(target.suffix + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(target)
    print(json.dumps({key: result[key] for key in result if key not in ("records", "claim_boundary")}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
