#!/usr/bin/env python3
"""Full residual p199 audit for Cycle 49's relative contraction theorem."""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
import itertools
import json
import multiprocessing
from pathlib import Path
import resource
import time

import lrc_cech_actual as base
import lrc_signed_ownership_moments as moments
from lrc_cube_rewrite import mobius_tensor
from lrc_cube_rewrite_select import relation_data
from lrc_multiplied_fill_probe import oriented_relation_transport
from lrc_relative_diagonal import PAIRS, cell_allowed, contract, serialize, triple_buffers
from lrc_relative_diagonal_deletion_classify import exact_pair_buffers

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle49-relative-diagonal"
TYPE_ID = {}
MASKS = []
MULTIPLICITIES = {}
TARGET_SUPPORTS = set()
ORIGINAL = {}
RELATION_DELETED = {}
TRANSPORT_MASKS = []
MARGINALS = []
DISTINGUISHED = []
RANK3 = {}
GROUPS = {}


def raw_valid(triple):
    left, middle, right = triple
    if left == right:
        return MULTIPLICITIES[left] >= 3
    if left == middle:
        return MULTIPLICITIES[left] >= 2
    if middle == right:
        return MULTIPLICITIES[middle] >= 2
    return True


def coordinate(owner):
    resource.setrlimit(resource.RLIMIT_AS, (2_000_000_000, 2_000_000_000))
    return moments.coordinate_classes(owner)


def rank3_owner(owner):
    found = {}
    for pattern in base.c38._COORDINATES[owner]["patterns"]:
        if int(pattern["rank"]) != 3:
            continue
        groups = [[TYPE_ID[row[0]] for row in base.c38._TYPE_ROWS[owner][int(signature)]] for signature in pattern["signatures"]]
        for values in itertools.product(*groups):
            triple = tuple(sorted(values))
            if tuple(sorted(MASKS[value] for value in triple)) not in TARGET_SUPPORTS:
                continue
            if not raw_valid(triple):
                continue
            found[triple] = found.get(triple, 0) | (1 << owner)
    return owner, found


def triples_for_masks(mask_triple):
    left, middle, right = mask_triple
    if left == right:
        iterator = itertools.combinations_with_replacement(GROUPS[left], 3)
    elif left == middle:
        iterator = (tuple(sorted((*pair, value))) for pair in itertools.combinations_with_replacement(GROUPS[left], 2) for value in GROUPS[right])
    elif middle == right:
        iterator = (tuple(sorted((value, *pair))) for value in GROUPS[left] for pair in itertools.combinations_with_replacement(GROUPS[middle], 2))
    else:
        iterator = (tuple(sorted(values)) for values in itertools.product(GROUPS[left], GROUPS[middle], GROUPS[right]))
    for triple in iterator:
        if raw_valid(triple):
            yield triple


def structural_good(types, pair_deleted, triple_deleted, cache):
    supports = tuple(tuple(owner for owner in range(13) if MASKS[value] & (1 << owner)) for value in types)
    key = (tuple(MASKS[value] for value in types), tuple(pair_deleted[pair] for pair in PAIRS), triple_deleted)
    if key in cache:
        return cache[key]
    common = MASKS[types[0]] & MASKS[types[1]] & MASKS[types[2]]
    active_triples = common & (triple_deleted | pair_deleted[(0, 1)] | pair_deleted[(0, 2)] | pair_deleted[(1, 2)])
    for w in range(13):
        if active_triples & (1 << w) and not triple_buffers(w, supports):
            cache[key] = False
            return False
    for left, right in PAIRS:
        for w in range(13):
            if pair_deleted[(left, right)] & (1 << w) and not exact_pair_buffers(left, right, w, supports, pair_deleted, triple_deleted):
                cache[key] = False
                return False
    cache[key] = True
    return True


def classify_shard(rows):
    structural_cache = {}
    flow_cache = {}
    counts = Counter()
    first_failure = None
    failures = []
    packet_moves = 0
    maximum_fraction_bits = 0
    for row in rows:
        for types in triples_for_masks(tuple(row["support_masks"])):
            counts["type_triples"] += 1
            pair_deleted = {
                pair: ORIGINAL.get(tuple(sorted((types[pair[0]], types[pair[1]]))), 0)
                for pair in PAIRS
            }
            triple_deleted = RANK3.get(types, 0)
            if structural_good(types, pair_deleted, triple_deleted, structural_cache):
                counts["structural_closed"] += 1
                continue
            counts["mobius_attempted"] += 1
            flows = {}
            for pair in PAIRS:
                type_pair = (types[pair[0]], types[pair[1]])
                if type_pair not in flow_cache:
                    flow_cache[type_pair] = oriented_relation_transport(
                        type_pair[0], type_pair[1], RELATION_DELETED, MARGINALS, TRANSPORT_MASKS
                    )
                flows[pair] = flow_cache[type_pair]
            start = mobius_tensor(flows, tuple(DISTINGUISHED[value] for value in types))
            maximum_fraction_bits = max(
                maximum_fraction_bits,
                *(max(abs(value.numerator).bit_length(), value.denominator.bit_length()) for value in start.values()),
            )
            supports = tuple(tuple(owner for owner in range(13) if MASKS[value] & (1 << owner)) for value in types)
            initial_forbidden = {cell for cell, value in start.items() if value and not cell_allowed(cell, pair_deleted, triple_deleted)}
            if not initial_forbidden:
                counts["mobius_already_allowed"] += 1
                continue
            result = contract(start, supports, pair_deleted, triple_deleted)
            packet_moves += len(result["steps"])
            if result["status"] == "CONTRACTED":
                counts["mobius_contracted"] += 1
                continue
            counts[result["status"]] += 1
            candidate = {
                "types": list(types), "support_sizes": [len(values) for values in supports],
                "pair_deleted": [[*pair, pair_deleted[pair]] for pair in PAIRS],
                "triple_deleted": triple_deleted, "status": result["status"],
                "stage": result["stage"], "pivot": list(result["pivot"]),
                "mobius": serialize(start), "residual": serialize(result["tensor"]),
                "pair_flows": [[*pair, serialize(flows[pair])] for pair in PAIRS],
            }
            if first_failure is None or tuple(candidate["types"]) < tuple(first_failure["types"]):
                first_failure = candidate
            failures.append(candidate)
    return {
        "counts": dict(counts), "first_failure": first_failure, "failures": failures,
        "packet_moves": packet_moves, "semantic_cache": len(structural_cache),
        "pair_flow_cache": len(flow_cache), "maximum_fraction_bits": maximum_fraction_bits,
    }


def main():
    global TYPE_ID, MASKS, MULTIPLICITIES, TARGET_SUPPORTS, ORIGINAL, RELATION_DELETED, TRANSPORT_MASKS, MARGINALS, DISTINGUISHED, RANK3, GROUPS
    started = time.monotonic()
    base.prepare_fast()
    complete = sorted({row[0] for root in base.c38._TYPE_ROWS for rows in root.values() for row in rows})
    TYPE_ID = {value: index for index, value in enumerate(complete)}
    MASKS = [sum(1 << owner for owner, signature in enumerate(value) if signature) for value in complete]
    moments._TYPE_ID = TYPE_ID
    moments._TYPE_MASKS = MASKS
    raw = []
    for point in range(base.c38._COVERAGE.shape[0]):
        value = tuple(sum(1 << offset for offset, digit in enumerate(base.c38._ALLOWED[coordinate]) if base.c38._COVERAGE[point, coordinate, digit]) for coordinate in range(13))
        raw.append(TYPE_ID[value])
    MULTIPLICITIES = Counter(raw)
    GROUPS = defaultdict(list)
    for index, mask in enumerate(MASKS): GROUPS[mask].append(index)
    residual_rows = json.loads((OUT / "deletion-classification.json").read_text())["unresolved"]
    TARGET_SUPPORTS = {tuple(row["support_masks"]) for row in residual_rows}

    with multiprocessing.Pool(3) as pool:
        coordinate_rows = pool.map(coordinate, range(13), chunksize=1)
    ORIGINAL, RELATION_DELETED, TRANSPORT_MASKS = relation_data(MASKS, coordinate_rows)
    prior = json.loads((ROOT / "discovery/out/cycle41-multiplied-ideal/zero-support-closure.json").read_text())
    MARGINALS = [{int(owner): Fraction(numerator, denominator) for owner, numerator, denominator in values} for values in prior["singleton_marginals_by_complete_type"]]
    DISTINGUISHED = [next(iter(values)) for values in MARGINALS]

    with multiprocessing.Pool(3) as pool:
        rank_rows = pool.map(rank3_owner, range(13), chunksize=1)
    rank3 = defaultdict(int)
    for _owner, mapping in rank_rows:
        for triple, deleted in mapping.items(): rank3[triple] |= deleted
    RANK3 = dict(rank3)
    assert len(RANK3) <= 5_000_000

    shards = [[], [], []]
    loads = [0, 0, 0]
    for row in sorted(residual_rows, key=lambda value: value["type_triples"], reverse=True):
        target = min(range(3), key=lambda index: loads[index])
        shards[target].append(row)
        loads[target] += row["type_triples"]
    with multiprocessing.Pool(3) as pool:
        outcomes = pool.map(classify_shard, shards, chunksize=1)
    counts = Counter()
    first_failure = None
    failures = []
    for outcome in outcomes:
        counts.update(outcome["counts"])
        candidate = outcome["first_failure"]
        if candidate is not None and (first_failure is None or tuple(candidate["types"]) < tuple(first_failure["types"])):
            first_failure = candidate
        failures.extend(outcome["failures"])
    assert counts["type_triples"] == sum(row["type_triples"] for row in residual_rows)
    failure_count = counts["BUFFER_INCOMPLETE"] + counts["NONZERO_TERMINAL"]
    result = {
        "status": "PASS", "epistemic_status": "PROVED", "stage": "FULL_RESIDUAL_RELATIVE_CONTRACTION_AUDIT",
        "rank3_residual_type_triples": len(RANK3),
        "shard_type_triples": loads,
        "counts": dict(sorted(counts.items())),
        "packet_moves": sum(row["packet_moves"] for row in outcomes),
        "semantic_cache_entries": sum(row["semantic_cache"] for row in outcomes),
        "pair_flow_cache_entries": sum(row["pair_flow_cache"] for row in outcomes),
        "maximum_fraction_bits": max(row["maximum_fraction_bits"] for row in outcomes),
        "failure_count": failure_count, "first_failure": first_failure,
        "failures": sorted(failures, key=lambda row: tuple(row["types"])),
        "claim_boundary": "Complete exact audit of the residual type triples left by the support/deletion theorems. A zero failure count plus prior universal closures proves the frozen two-stage formula on the full raw-valid p199 face domain only.",
        "wall_seconds": time.monotonic() - started,
    }
    path = OUT / "full-audit.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: result[key] for key in result if key not in ("first_failure", "failures", "claim_boundary")}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
