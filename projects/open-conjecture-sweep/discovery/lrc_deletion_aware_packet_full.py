#!/usr/bin/env python3
"""Full p199 census of Cycle 50's two frozen support patterns."""
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
from lrc_deletion_aware_packet import contract
from lrc_relative_diagonal import PAIRS, serialize

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle50-deletion-aware-packet"
TYPE_ID = {}
MASKS = []
MULTIPLICITIES = {}
GROUPS = {}
ORIGINAL = {}
RELATION_DELETED = {}
TRANSPORT_MASKS = []
MARGINALS = []
DISTINGUISHED = []
RANK3 = {}


def raw_valid(triple):
    left, middle, right = triple
    if left == right:
        return MULTIPLICITIES[left] >= 3
    if left == middle or middle == right:
        return MULTIPLICITIES[left if left == middle else middle] >= 2
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
            if not raw_valid(triple):
                continue
            found[triple] = found.get(triple, 0) | (1 << owner)
    return found


def triples_for_masks(mask_triple):
    left, middle, right = mask_triple
    if left == right == middle:
        iterator = itertools.combinations_with_replacement(GROUPS[left], 3)
    elif left == middle:
        iterator = (tuple(sorted((*pair, value))) for pair in itertools.combinations_with_replacement(GROUPS[left], 2) for value in GROUPS[right])
    elif middle == right:
        iterator = (tuple(sorted((value, *pair))) for value in GROUPS[left] for pair in itertools.combinations_with_replacement(GROUPS[middle], 2))
    else:
        iterator = (tuple(sorted(values)) for values in itertools.product(GROUPS[left], GROUPS[middle], GROUPS[right]))
    yield from (triple for triple in iterator if raw_valid(triple))


def classify(rows):
    counts = Counter()
    flows_cache = {}
    failures = []
    packet_moves = 0
    max_bits = 0
    for masks in rows:
        for types in triples_for_masks(masks):
            counts["selected_type_triples"] += 1
            pair_deleted = {pair: ORIGINAL.get(tuple(sorted((types[pair[0]], types[pair[1]]))), 0) for pair in PAIRS}
            triple_deleted = RANK3.get(types, 0)
            flows = {}
            for pair in PAIRS:
                type_pair = (types[pair[0]], types[pair[1]])
                if type_pair not in flows_cache:
                    flows_cache[type_pair] = oriented_relation_transport(type_pair[0], type_pair[1], RELATION_DELETED, MARGINALS, TRANSPORT_MASKS)
                flows[pair] = flows_cache[type_pair]
            source = mobius_tensor(flows, tuple(DISTINGUISHED[value] for value in types))
            max_bits = max(max_bits, *(max(abs(value.numerator).bit_length(), value.denominator.bit_length()) for value in source.values()))
            supports = tuple(tuple(owner for owner in range(13) if MASKS[value] & (1 << owner)) for value in types)
            outcome = contract(source, supports, pair_deleted, triple_deleted)
            packet_moves += len(outcome["steps"])
            counts[outcome["status"]] += 1
            if outcome["status"] != "CONTRACTED":
                failures.append({
                    "types": list(types), "support_sizes": [len(values) for values in supports],
                    "support_masks": list(masks), "pair_deleted": [[*pair, pair_deleted[pair]] for pair in PAIRS],
                    "triple_deleted": triple_deleted, "status": outcome["status"], "stage": outcome["stage"],
                    "pivot": list(outcome["pivot"]), "mobius": serialize(source), "residual": serialize(outcome["tensor"]),
                })
    return dict(counts), failures, packet_moves, max_bits


def main():
    global TYPE_ID, MASKS, MULTIPLICITIES, GROUPS, ORIGINAL, RELATION_DELETED, TRANSPORT_MASKS, MARGINALS, DISTINGUISHED, RANK3
    started = time.monotonic()
    OUT.mkdir(parents=True, exist_ok=True)
    base.prepare_fast()
    complete = sorted({row[0] for root in base.c38._TYPE_ROWS for rows in root.values() for row in rows})
    TYPE_ID = {value: index for index, value in enumerate(complete)}
    MASKS = [sum(1 << owner for owner, signature in enumerate(value) if signature) for value in complete]
    moments._TYPE_ID, moments._TYPE_MASKS = TYPE_ID, MASKS
    raw = []
    for point in range(base.c38._COVERAGE.shape[0]):
        value = tuple(sum(1 << offset for offset, digit in enumerate(base.c38._ALLOWED[coordinate]) if base.c38._COVERAGE[point, coordinate, digit]) for coordinate in range(13))
        raw.append(TYPE_ID[value])
    MULTIPLICITIES = Counter(raw)
    GROUPS = defaultdict(list)
    for index, mask in enumerate(MASKS):
        GROUPS[mask].append(index)
    with multiprocessing.Pool(3) as pool:
        coordinate_rows = pool.map(coordinate, range(13), chunksize=1)
    ORIGINAL, RELATION_DELETED, TRANSPORT_MASKS = relation_data(MASKS, coordinate_rows)
    prior = json.loads((ROOT / "discovery/out/cycle41-multiplied-ideal/zero-support-closure.json").read_text())
    MARGINALS = [{int(owner): Fraction(num, den) for owner, num, den in values} for values in prior["singleton_marginals_by_complete_type"]]
    DISTINGUISHED = [next(iter(values)) for values in MARGINALS]
    with multiprocessing.Pool(3) as pool:
        rank_rows = pool.map(rank3_owner, range(13), chunksize=1)
    rank3 = defaultdict(int)
    for mapping in rank_rows:
        for triple, deleted in mapping.items():
            rank3[triple] |= deleted
    RANK3 = dict(rank3)

    selected_masks = [mask for mask in sorted(GROUPS) if mask.bit_count() in (2, 4)]
    rows = [masks for masks in itertools.combinations_with_replacement(selected_masks, 3) if tuple(sorted(mask.bit_count() for mask in masks)) in ((2, 2, 2), (2, 2, 4))]
    shards = [[], [], []]
    for index, masks in enumerate(rows):
        shards[index % 3].append(masks)
    with multiprocessing.Pool(3) as pool:
        outcomes = pool.map(classify, shards, chunksize=1)
    counts = Counter()
    failures = []
    for outcome in outcomes:
        counts.update(outcome[0])
        failures.extend(outcome[1])
    result = {
        "status": "THEOREM_PASS" if not failures else "THEOREM_FAIL", "epistemic_status": "PROVED", "stage": "FULL_DELETION_AWARE_PATTERN_CENSUS",
        "support_patterns": [[2, 2, 2], [2, 2, 4]], "mask_triples": len(rows),
        "counts": dict(sorted(counts.items())), "packet_moves": sum(row[2] for row in outcomes),
        "maximum_fraction_bits": max(row[3] for row in outcomes), "failures": sorted(failures, key=lambda row: tuple(row["types"])),
        "wall_seconds": time.monotonic() - started,
        "claim_boundary": "Complete raw-valid type-triple census only for the two frozen support patterns and the frozen C50 selector plus inherited C49 pair stage.",
    }
    assert result["counts"]["selected_type_triples"] <= 50_000_000
    assert result["packet_moves"] <= 200_000_000
    (OUT / "full-pattern-census.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: result[key] for key in result if key not in ("failures", "claim_boundary")}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
