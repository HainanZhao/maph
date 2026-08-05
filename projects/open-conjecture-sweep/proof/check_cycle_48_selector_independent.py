#!/usr/bin/env python3
"""Independent streaming reconstruction of Cycle 48's structural selector."""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import itertools
import json
import multiprocessing
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_cech_actual as base
import lrc_signed_ownership_moments as moments
from lrc_multiplied_fill_probe import oriented_relation_transport

OUT = ROOT / "discovery/out/cycle48-cube-rewrite"
SEED = "cycle48-cube-rewrite-v1"
TYPE_ID = {}
TARGET = set()


def coordinate(owner):
    resource.setrlimit(resource.RLIMIT_AS, (2_000_000_000, 2_000_000_000))
    return moments.coordinate_classes(owner)


def rank3(owner):
    found = set()
    for pattern in base.c38._COORDINATES[owner]["patterns"]:
        if int(pattern["rank"]) != 3:
            continue
        groups = [[TYPE_ID[row[0]] for row in base.c38._TYPE_ROWS[owner][int(signature)]] for signature in reversed(pattern["signatures"])]
        for values in itertools.product(*groups):
            triple = tuple(sorted(values))
            if triple in TARGET:
                found.add(triple)
    return owner, found


def relations(masks, rows):
    original = defaultdict(int)
    induced = defaultdict(int)
    for owner in reversed(range(13)):
        for pair in reversed(rows[owner]["rank_two_pairs"]):
            original[tuple(pair)] |= 1 << owner
        for pair in reversed(rows[owner]["induced_pair_deletions"]):
            induced[tuple(pair)] |= 1 << owner
    binary = {index for index, mask in enumerate(masks) if mask.bit_count() <= 2}
    blocked = defaultdict(list)
    for pair, owner_mask in original.items():
        for owner in reversed(range(13)):
            if owner_mask & (1 << owner):
                if pair[0] in binary:
                    blocked[(pair[0], owner)].append(pair[1])
                if pair[1] in binary:
                    blocked[(pair[1], owner)].append(pair[0])
    transport_masks = list(masks)
    for mediator in sorted(binary, reverse=True):
        owners = [owner for owner in range(13) if masks[mediator] & (1 << owner)]
        if len(owners) == 1:
            for neighbor in blocked[(mediator, owners[0])]:
                transport_masks[neighbor] &= ~(1 << owners[0])
    deleted = defaultdict(int)
    for pair in set(original) | set(induced):
        for owner in range(13):
            if (original.get(pair, 0) | induced.get(pair, 0)) & (1 << owner):
                deleted[pair] |= 1 << (13 * owner + owner)
    for mediator in binary:
        owners = [owner for owner in range(13) if masks[mediator] & (1 << owner)]
        if len(owners) != 2:
            continue
        a, b = owners
        for left in blocked[(mediator, a)]:
            for right in blocked[(mediator, b)]:
                if left <= right:
                    deleted[(left, right)] |= 1 << (13 * a + b)
                    if left == right:
                        deleted[(left, right)] |= 1 << (13 * b + a)
                else:
                    deleted[(right, left)] |= 1 << (13 * b + a)
    return dict(original), dict(deleted), transport_masks


def allowed(cell, pair_deleted, triple_deleted):
    return not any(cell[a] == cell[b] and pair_deleted[(a, b)] & (1 << cell[a]) for a, b in itertools.combinations(range(3), 2)) and not (cell[0] == cell[1] == cell[2] and triple_deleted & (1 << cell[0]))


def mobius(flows, distinguished):
    values = defaultdict(Fraction)
    for (a, b), value in flows[(0, 1)].items(): values[(a, b, distinguished[2])] += value
    for (a, c), value in flows[(0, 2)].items(): values[(a, distinguished[1], c)] += value
    for (b, c), value in flows[(1, 2)].items(): values[(distinguished[0], b, c)] += value
    values[distinguished] -= 2
    return {cell: value for cell, value in values.items() if value}


def first_choice_bin(pivot, supports, pair_deleted, triple_deleted):
    if pivot is None:
        return 0
    count = 0
    for alternatives in itertools.product(*(tuple(owner for owner in supports[index] if owner != pivot[index]) for index in range(3))):
        pairs = [tuple(sorted((pivot[index], alternatives[index]))) for index in range(3)]
        cells = {tuple(pairs[index][bits[index]] for index in range(3)) for bits in itertools.product((0, 1), repeat=3)}
        if all(cell == pivot or allowed(cell, pair_deleted, triple_deleted) or cell > pivot for cell in cells):
            count += 1
            if count >= 8:
                return 3
    return 0 if count == 0 else 1 if count == 1 else 2


def defect_bin(count):
    return 0 if count == 0 else 1 if count == 1 else 2 if count <= 3 else 3 if count <= 15 else 4


def main():
    global TYPE_ID, TARGET
    started = time.monotonic()
    expected = json.loads((OUT / "selection.json").read_text())
    base.prepare_fast()
    complete = sorted({row[0] for root in base.c38._TYPE_ROWS for rows in root.values() for row in rows})
    TYPE_ID = {value: index for index, value in enumerate(complete)}
    masks = [sum(1 << owner for owner, signature in enumerate(value) if signature) for value in complete]
    moments._TYPE_ID = TYPE_ID
    moments._TYPE_MASKS = masks
    raw = []
    for point in range(base.c38._COVERAGE.shape[0]):
        value = tuple(sum(1 << offset for offset, digit in enumerate(base.c38._ALLOWED[coordinate]) if base.c38._COVERAGE[point, coordinate, digit]) for coordinate in range(13))
        raw.append(TYPE_ID[value])
    multiplicities = Counter(raw)
    candidates = set()
    for counter in reversed(range(100000)):
        data = hashlib.sha256(f"{SEED}:triple:{counter}".encode("ascii")).digest()
        triple = tuple(sorted(int.from_bytes(data[2 * index:2 * index + 2], "big") % 1318 for index in range(3)))
        if all(count <= multiplicities[value] for value, count in Counter(triple).items()):
            candidates.add(triple)
    c47 = json.loads((ROOT / "discovery/out/cycle47-affine-descent/selection.json").read_text())
    c47_faces = {tuple(sorted(row["types"][part] for part in parts)) for row in c47["selected"] for parts in itertools.combinations(range(4), 3)}
    candidates |= c47_faces
    TARGET = candidates
    with multiprocessing.Pool(2) as pool:
        coordinate_rows = pool.map(coordinate, range(13), chunksize=1)
        rank3_rows = pool.map(rank3, range(13), chunksize=1)
    original, deleted, transport_masks = relations(masks, coordinate_rows)
    triple_deleted = defaultdict(int)
    for owner, triples in rank3_rows:
        for triple in triples: triple_deleted[triple] |= 1 << owner
    prior = json.loads((ROOT / "discovery/out/cycle41-multiplied-ideal/zero-support-closure.json").read_text())
    marginals = [{int(owner): Fraction(numerator, denominator) for owner, numerator, denominator in values} for values in prior["singleton_marginals_by_complete_type"]]
    distinguished = [next(iter(values)) for values in marginals]
    strata = defaultdict(list)
    rows = {}
    mobius_nonzeros = 0
    maximum_mobius_fraction_bits = 0
    for ordinal, types in enumerate(sorted(candidates, reverse=True)):
        supports = [tuple(owner for owner in range(13) if masks[value] & (1 << owner)) for value in types]
        pair_deleted = {pair: original.get(tuple(sorted((types[pair[0]], types[pair[1]]))), 0) for pair in itertools.combinations(range(3), 2)}
        flows = {pair: oriented_relation_transport(types[pair[0]], types[pair[1]], deleted, marginals, transport_masks) for pair in itertools.combinations(range(3), 2)}
        start = mobius(flows, tuple(distinguished[value] for value in types))
        mobius_nonzeros += len(start)
        maximum_mobius_fraction_bits = max(
            maximum_mobius_fraction_bits,
            *(max(abs(value.numerator).bit_length(), value.denominator.bit_length()) for value in start.values()),
        )
        triple_mask = triple_deleted.get(types, 0)
        defects = sorted(cell for cell, value in start.items() if value and not allowed(cell, pair_deleted, triple_mask))
        distinguished_cell = tuple(distinguished[value] for value in types)
        descriptor = (tuple(sorted(map(len, supports))), tuple(sorted(Counter(types).values(), reverse=True)), tuple(pair_deleted[pair].bit_count() for pair in itertools.combinations(range(3), 2)), triple_mask.bit_count(), int(allowed(distinguished_cell, pair_deleted, triple_mask)), defect_bin(len(defects)), first_choice_bin(defects[0] if defects else None, supports, pair_deleted, triple_mask))
        selection_hash = hashlib.sha256(f"{SEED}:select:{','.join(map(str, types))}".encode("ascii")).hexdigest()
        row = {"selection_hash": selection_hash, "repeat_partition": descriptor[1], "mobius_defect_bin": descriptor[5], "first_pivot_choice_bin": descriptor[6]}
        rows[types] = row
        strata[descriptor].append((selection_hash, types))
        if ordinal and ordinal % 20000 == 0:
            print(json.dumps({"independent_described": ordinal}), flush=True)
    selected = set()
    for values in strata.values(): selected.update(types for _hash, types in sorted(values)[:4])
    if len(selected) > 512:
        reserves = set()
        for key in ("repeat_partition", "mobius_defect_bin", "first_pivot_choice_bin"):
            groups = defaultdict(list)
            for types in selected: groups[rows[types][key]].append(types)
            for values in groups.values(): reserves.add(min(values, key=lambda types: (rows[types]["selection_hash"], types)))
        ordered = sorted(selected - reserves, key=lambda types: (rows[types]["selection_hash"], types))
        selected = reserves | set(ordered[:512-len(reserves)])
    ordered = sorted(selected, key=lambda types: (rows[types]["selection_hash"], types))
    expected_types = [tuple(row["types"]) for row in expected["selected"]]
    assert ordered == expected_types and len(strata) == expected["descriptor_strata"] and len(candidates) == expected["deduplicated_candidates"]
    result = {
        "status":"PASS", "epistemic_status":"PROVED", "candidates":len(candidates),
        "descriptor_strata":len(strata), "selected_faces":len(ordered),
        "mobius_nonzeros":mobius_nonzeros,
        "maximum_mobius_fraction_bits":maximum_mobius_fraction_bits,
        "wall_seconds":time.monotonic()-started,
    }
    (OUT / "independent-selection.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
