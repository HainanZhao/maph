#!/usr/bin/env python3
"""Cycle 48 outcome-blind structural face selector and frozen input builder."""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import itertools
import json
import multiprocessing
from pathlib import Path
import resource
import time

import lrc_cech_actual as target
import lrc_signed_ownership_moments as c40
from lrc_cube_rewrite import cell_allowed, mobius_tensor, serialize_tensor, triangular_choices
from lrc_multiplied_fill_probe import oriented_relation_transport

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle48-cube-rewrite"
SEED = "cycle48-cube-rewrite-v1"
TYPE_COUNT = 1318
TARGET_FACES = set()
TYPE_ID = {}


def digest(label):
    return hashlib.sha256(label.encode("ascii")).digest()


def coordinate(owner):
    resource.setrlimit(resource.RLIMIT_AS, (2_000_000_000, 2_000_000_000))
    return c40.coordinate_classes(owner)


def rank3_target(owner):
    resource.setrlimit(resource.RLIMIT_AS, (1_600_000_000, 1_600_000_000))
    found = set()
    for pattern in target.c38._COORDINATES[owner]["patterns"]:
        if int(pattern["rank"]) != 3:
            continue
        groups = [[TYPE_ID[row[0]] for row in target.c38._TYPE_ROWS[owner][int(signature)]] for signature in pattern["signatures"]]
        for rows in itertools.product(*groups):
            triple = tuple(sorted(rows))
            if triple in TARGET_FACES:
                found.add(triple)
    return owner, sorted(found)


def relation_data(masks, coordinate_rows):
    original = defaultdict(int)
    induced = defaultdict(int)
    for owner, row in enumerate(coordinate_rows):
        for pair in row["rank_two_pairs"]:
            original[tuple(pair)] |= 1 << owner
        for pair in row["induced_pair_deletions"]:
            induced[tuple(pair)] |= 1 << owner
    binary = {index for index, mask in enumerate(masks) if mask.bit_count() <= 2}
    blocked = defaultdict(list)
    for (left, right), owner_mask in original.items():
        for owner in range(13):
            if owner_mask & (1 << owner):
                if left in binary:
                    blocked[(left, owner)].append(right)
                if right in binary:
                    blocked[(right, owner)].append(left)
    transport_masks = list(masks)
    for mediator in binary:
        owners = [owner for owner in range(13) if masks[mediator] & (1 << owner)]
        if len(owners) == 1:
            for neighbor in blocked[(mediator, owners[0])]:
                transport_masks[neighbor] &= ~(1 << owners[0])
    relation_deleted = defaultdict(int)
    for pair in set(original) | set(induced):
        for owner in range(13):
            if (original.get(pair, 0) | induced.get(pair, 0)) & (1 << owner):
                relation_deleted[pair] |= 1 << (13 * owner + owner)
    for mediator in binary:
        owners = [owner for owner in range(13) if masks[mediator] & (1 << owner)]
        if len(owners) != 2:
            continue
        left_owner, right_owner = owners
        for left in blocked[(mediator, left_owner)]:
            for right in blocked[(mediator, right_owner)]:
                if left <= right:
                    relation_deleted[(left, right)] |= 1 << (13 * left_owner + right_owner)
                    if left == right:
                        relation_deleted[(left, right)] |= 1 << (13 * right_owner + left_owner)
                else:
                    relation_deleted[(right, left)] |= 1 << (13 * right_owner + left_owner)
    return dict(original), dict(relation_deleted), transport_masks


def flow_for(types, pair, relation_deleted, marginals, transport_masks):
    left, right = pair
    return oriented_relation_transport(types[left], types[right], relation_deleted, marginals, transport_masks)


def bin_value(value, cuts):
    for index, cut in enumerate(cuts):
        if value <= cut:
            return index
    return len(cuts)


def main():
    global TYPE_ID, TARGET_FACES
    started = time.monotonic()
    OUT.mkdir(parents=True, exist_ok=True)
    target.prepare_fast()
    complete = sorted({row[0] for root in target.c38._TYPE_ROWS for rows in root.values() for row in rows})
    TYPE_ID = {value: index for index, value in enumerate(complete)}
    masks = [sum(1 << owner for owner, signature in enumerate(value) if signature) for value in complete]
    c40._TYPE_ID = TYPE_ID
    c40._TYPE_MASKS = masks
    raw_types = []
    for point in range(target.c38._COVERAGE.shape[0]):
        value = tuple(sum(1 << offset for offset, digit in enumerate(target.c38._ALLOWED[coordinate]) if target.c38._COVERAGE[point, coordinate, digit]) for coordinate in range(13))
        raw_types.append(TYPE_ID[value])
    multiplicities = Counter(raw_types)

    candidates = set()
    for counter in range(100_000):
        raw = digest(f"{SEED}:triple:{counter}")
        triple = tuple(sorted(int.from_bytes(raw[2 * index:2 * index + 2], "big") % TYPE_COUNT for index in range(3)))
        if all(count <= multiplicities[value] for value, count in Counter(triple).items()):
            candidates.add(triple)
    cycle47 = json.loads((ROOT / "discovery/out/cycle47-affine-descent/selection.json").read_text())
    cycle47_faces = {
        tuple(sorted(row["types"][part] for part in parts))
        for row in cycle47["selected"] for parts in itertools.combinations(range(4), 3)
    }
    candidates.update(cycle47_faces)
    TARGET_FACES = set(candidates)

    with multiprocessing.Pool(2) as pool:
        coordinate_rows = pool.map(coordinate, range(13), chunksize=1)
        rank3_rows = pool.map(rank3_target, range(13), chunksize=1)
    original, relation_deleted, transport_masks = relation_data(masks, coordinate_rows)
    rank3 = defaultdict(int)
    for owner, triples in rank3_rows:
        for triple in triples:
            rank3[triple] |= 1 << owner
    prior = json.loads((ROOT / "discovery/out/cycle41-multiplied-ideal/zero-support-closure.json").read_text())
    marginals = [{int(owner): Fraction(numerator, denominator) for owner, numerator, denominator in values} for values in prior["singleton_marginals_by_complete_type"]]
    distinguished = [next(iter(values)) for values in marginals]

    rows = {}
    strata = defaultdict(list)
    for ordinal, types in enumerate(sorted(candidates)):
        supports = [tuple(owner for owner in range(13) if masks[value] & (1 << owner)) for value in types]
        pair_deleted = {pair: original.get(tuple(sorted((types[pair[0]], types[pair[1]]))), 0) for pair in itertools.combinations(range(3), 2)}
        triple_deleted = rank3.get(types, 0)
        pair_flows = {pair: flow_for(types, pair, relation_deleted, marginals, transport_masks) for pair in itertools.combinations(range(3), 2)}
        mobius = mobius_tensor(pair_flows, tuple(distinguished[value] for value in types))
        forbidden = {cell for cell in itertools.product(*supports) if not cell_allowed(types, cell, pair_deleted, triple_deleted)}
        defects = sorted(cell for cell, value in mobius.items() if value and cell in forbidden)
        first_choices = len(triangular_choices(defects[0], supports, forbidden)) if defects else 0
        descriptor = (
            tuple(sorted(map(len, supports))), tuple(sorted(Counter(types).values(), reverse=True)),
            tuple(pair_deleted[pair].bit_count() for pair in itertools.combinations(range(3), 2)),
            triple_deleted.bit_count(), int(tuple(distinguished[value] for value in types) not in forbidden),
            bin_value(len(defects), (0, 1, 3, 15)), bin_value(first_choices, (0, 1, 7)),
        )
        selection_hash = hashlib.sha256(f"{SEED}:select:{','.join(map(str, types))}".encode("ascii")).hexdigest()
        row = {
            "types": list(types), "selection_hash": selection_hash,
            "support_sizes": list(map(len, supports)), "repeat_partition": list(descriptor[1]),
            "pair_deleted_popcounts": list(descriptor[2]), "rank3_deleted_popcount": descriptor[3],
            "distinguished_allowed": bool(descriptor[4]), "mobius_defects": len(defects),
            "mobius_defect_bin": descriptor[5], "first_pivot_choices": first_choices,
            "first_pivot_choice_bin": descriptor[6], "from_cycle47": types in cycle47_faces,
        }
        rows[types] = row
        strata[descriptor].append((selection_hash, types))
        if ordinal and ordinal % 10000 == 0:
            print(json.dumps({"described": ordinal, "candidates": len(candidates)}), flush=True)
    selected = set()
    for values in strata.values():
        selected.update(types for _hash, types in sorted(values)[:4])
    if len(selected) > 512:
        reserves = set()
        for key in ("repeat_partition", "mobius_defect_bin", "first_pivot_choice_bin"):
            groups = defaultdict(list)
            for types in selected:
                value = tuple(rows[types][key]) if isinstance(rows[types][key], list) else rows[types][key]
                groups[value].append(types)
            for values in groups.values():
                reserves.add(min(values, key=lambda types: (rows[types]["selection_hash"], types)))
        ordered = sorted(selected - reserves, key=lambda types: (rows[types]["selection_hash"], types))
        selected = reserves | set(ordered[:512 - len(reserves)])
    selected_types = sorted(selected, key=lambda types: (rows[types]["selection_hash"], types))

    structures = []
    for types in selected_types:
        supports = [tuple(owner for owner in range(13) if masks[value] & (1 << owner)) for value in types]
        pair_deleted = {pair: original.get(tuple(sorted((types[pair[0]], types[pair[1]]))), 0) for pair in itertools.combinations(range(3), 2)}
        pair_flows = {pair: flow_for(types, pair, relation_deleted, marginals, transport_masks) for pair in itertools.combinations(range(3), 2)}
        structures.append({
            **rows[types], "supports": [list(values) for values in supports],
            "distinguished": [distinguished[value] for value in types],
            "pair_deleted": [[left, right, pair_deleted[(left, right)]] for left, right in itertools.combinations(range(3), 2)],
            "triple_deleted": rank3.get(types, 0),
            "pair_flows": [
                [left, right, serialize_tensor({owners: value for owners, value in pair_flows[(left, right)].items()})]
                for left, right in itertools.combinations(range(3), 2)
            ],
        })
    result = {
        "status": "PASS", "epistemic_status": "PROVED", "stage": "OUTCOME_BLIND_CUBE_REWRITE_SELECTION",
        "hash_counters": 100000, "deduplicated_candidates": len(candidates), "cycle47_face_union": len(cycle47_faces),
        "descriptor_strata": len(strata), "selected_faces": len(structures), "selected": structures,
        "defect_bin_counts": dict(sorted(Counter(row["mobius_defect_bin"] for row in structures).items())),
        "first_choice_bin_counts": dict(sorted(Counter(row["first_pivot_choice_bin"] for row in structures).items())),
        "repeat_partition_counts": {str(key): value for key, value in sorted(Counter(tuple(row["repeat_partition"]) for row in structures).items())},
        "claim_boundary": "Outcome-blind structural selection and frozen face inputs only; no deterministic repair path or critical diamond was classified.",
        "wall_seconds": time.monotonic() - started,
    }
    path = OUT / "selection.json"
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)
    print(json.dumps({key: result[key] for key in ("status", "deduplicated_candidates", "cycle47_face_union", "descriptor_strata", "selected_faces", "defect_bin_counts", "first_choice_bin_counts", "wall_seconds")}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
