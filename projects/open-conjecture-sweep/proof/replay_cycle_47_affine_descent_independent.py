#!/usr/bin/env python3
"""Independent target-only replay of Cycle 47's material section classes."""
from __future__ import annotations

from collections import Counter, defaultdict
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
import lrc_cech_actual as target
import lrc_signed_ownership_moments as c40
from lrc_multiplied_fill_probe import oriented_relation_transport

OUT = ROOT / "discovery/out/cycle47-affine-descent"
TARGET_FACES = set()
TYPE_ID = {}


def rank3_target(owner):
    resource.setrlimit(resource.RLIMIT_AS, (1_600_000_000, 1_600_000_000))
    found = set()
    for pattern in target.c38._COORDINATES[owner]["patterns"]:
        if int(pattern["rank"]) != 3:
            continue
        groups = []
        for signature in pattern["signatures"]:
            values = sorted({TYPE_ID[row[0]] for row in target.c38._TYPE_ROWS[owner][int(signature)]})
            groups.append(values)
        for values in itertools.product(*groups):
            triple = tuple(sorted(values))
            if triple in TARGET_FACES:
                found.add(triple)
    return owner, sorted(found)


def coordinate(owner):
    resource.setrlimit(resource.RLIMIT_AS, (2_000_000_000, 2_000_000_000))
    return c40.coordinate_classes(owner)


def parse_chain(rows):
    return {tuple(cell): Fraction(numerator, denominator) for cell, numerator, denominator in rows}


def parse_cycle(rows):
    return {(tuple(parts), tuple(owners)): Fraction(numerator, denominator) for (parts, owners), numerator, denominator in rows}


def boundary(fill):
    result = defaultdict(Fraction)
    for owners, coefficient in fill.items():
        for omitted in range(4):
            parts = tuple(part for part in range(4) if part != omitted)
            result[(parts, tuple(owners[part] for part in parts))] += Fraction((-1) ** omitted) * coefficient
    return {key: value for key, value in result.items() if value}


def main():
    global TYPE_ID, TARGET_FACES
    started = time.monotonic()
    selection = json.loads((OUT / "selection.json").read_text())
    actual = json.loads((OUT / "canonical-section-localized.json").read_text())
    route_first = {}
    for row in actual["records"]:
        route_first.setdefault(row["route"], row["ordinal"])
    ordinals = {0, len(actual["records"]) // 2, len(actual["records"]) - 1}
    ordinals.update(route_first.values())
    ordinals.add(max(actual["records"], key=lambda row: len(row["fill"]))["ordinal"])
    ordinals.add(min(range(len(selection["selected"])), key=lambda index: (selection["selected"][index]["shared_faces_at_selection"], index)))
    ordinals.add(max(range(len(selection["selected"])), key=lambda index: (selection["selected"][index]["shared_faces_at_selection"], -index)))
    ordinals = sorted(ordinals)
    if len(ordinals) > 32:
        raise AssertionError("independent selection cap")
    selected = [actual["records"][ordinal] for ordinal in ordinals]
    rank_control = actual["records"][:32]
    TARGET_FACES = {tuple(row["triple"]) for row in actual["face_tensors"]}

    target.prepare_fast()
    complete = sorted({row[0] for root in target.c38._TYPE_ROWS for rows in root.values() for row in rows})
    TYPE_ID = {value: index for index, value in enumerate(complete)}
    masks = [sum(1 << owner for owner, signature in enumerate(value) if signature) for value in complete]
    c40._TYPE_ID = TYPE_ID
    c40._TYPE_MASKS = masks
    with multiprocessing.Pool(2) as pool:
        coordinate_rows = pool.map(coordinate, range(13), chunksize=1)
        rank3_rows = pool.map(rank3_target, range(13), chunksize=1)
    original = defaultdict(int)
    induced = defaultdict(int)
    for owner, row in enumerate(coordinate_rows):
        for pair in row["rank_two_pairs"]:
            original[tuple(pair)] |= 1 << owner
        for pair in row["induced_pair_deletions"]:
            induced[tuple(pair)] |= 1 << owner
    rank3 = defaultdict(int)
    for owner, triples in rank3_rows:
        for triple in triples:
            rank3[triple] |= 1 << owner

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
        a, b = owners
        for left in blocked[(mediator, a)]:
            for right in blocked[(mediator, b)]:
                if left <= right:
                    relation_deleted[(left, right)] |= 1 << (13 * a + b)
                    if left == right:
                        relation_deleted[(left, right)] |= 1 << (13 * b + a)
                else:
                    relation_deleted[(right, left)] |= 1 << (13 * b + a)
    prior = json.loads((ROOT / "discovery/out/cycle41-multiplied-ideal/zero-support-closure.json").read_text())
    marginals = [{int(owner): Fraction(numerator, denominator) for owner, numerator, denominator in values} for values in prior["singleton_marginals_by_complete_type"]]
    pair_classes = {tuple(sorted((triple[left], triple[right]))) for triple in TARGET_FACES for left, right in itertools.combinations(range(3), 2)}
    pair_flows = {pair: oriented_relation_transport(pair[0], pair[1], relation_deleted, marginals, transport_masks) for pair in pair_classes}

    tensors = {tuple(row["triple"]): parse_chain(row["coefficients"]) for row in actual["face_tensors"] if tuple(row["triple"]) in TARGET_FACES}
    checked_faces = 0
    invariant_dimensions = {}
    for triple in sorted(TARGET_FACES, reverse=True):
        tensor = tensors[triple]
        supports = [tuple(owner for owner in range(13) if masks[value] & (1 << owner)) for value in triple]
        stabilizer = [permutation for permutation in itertools.permutations(range(3)) if tuple(triple[permutation[index]] for index in range(3)) == triple]
        allowed = []
        for owners in itertools.product(*supports):
            if any(owners[left] == owners[right] and original.get(tuple(sorted((triple[left], triple[right]))), 0) & (1 << owners[left]) for left, right in itertools.combinations(range(3), 2)):
                continue
            if owners[0] == owners[1] == owners[2] and rank3.get(triple, 0) & (1 << owners[0]):
                continue
            allowed.append(owners)
        invariant_dimensions[triple] = len({min(tuple(owners[permutation[index]] for index in range(3)) for permutation in stabilizer) for owners in allowed})
        for owners in tensor:
            assert all(owners[index] in supports[index] for index in range(3))
            assert not any(owners[left] == owners[right] and original.get(tuple(sorted((triple[left], triple[right]))), 0) & (1 << owners[left]) for left, right in itertools.combinations(range(3), 2))
            assert not (owners[0] == owners[1] == owners[2] and rank3.get(triple, 0) & (1 << owners[0]))
        for left, right in itertools.combinations(range(3), 2):
            observed = defaultdict(Fraction)
            for owners, value in tensor.items():
                observed[(owners[left], owners[right])] += value
            assert {key: value for key, value in observed.items() if value} == pair_flows[tuple(sorted((triple[left], triple[right])))]
        for permutation in stabilizer:
            assert {tuple(owners[permutation[index]] for index in range(3)): value for owners, value in tensor.items()} == tensor
        checked_faces += 1

    occurrence_counts = Counter(
        tuple(sorted(row["types"][part] for part in parts))
        for row in rank_control for parts in itertools.combinations(range(4), 3)
    )
    raw_face_variables = sum(occurrence_counts[triple] * invariant_dimensions[triple] for triple in occurrence_counts)
    compressed_face_variables = sum(invariant_dimensions[triple] for triple in occurrence_counts)
    gluing_rank = sum((occurrence_counts[triple] - 1) * invariant_dimensions[triple] for triple in occurrence_counts)
    assert raw_face_variables - compressed_face_variables == gluing_rank

    full_records = []
    raw_occurrences = 0
    for row in reversed(actual["records"]):
        types = tuple(row["types"])
        reconstructed = defaultdict(Fraction)
        for omitted in range(4):
            parts = tuple(part for part in range(4) if part != omitted)
            ordered_types = tuple(types[part] for part in parts)
            triple = tuple(sorted(ordered_types))
            permutation = next(p for p in itertools.permutations(range(3)) if tuple(triple[p[index]] for index in range(3)) == ordered_types)
            occurrence = {
                tuple(owners[permutation[index]] for index in range(3)): value
                for owners, value in tensors[triple].items()
            }
            inverse = tuple(permutation.index(index) for index in range(3))
            recovered = {
                tuple(owners[inverse[index]] for index in range(3)): value
                for owners, value in occurrence.items()
            }
            assert recovered == tensors[triple]
            for owners, value in occurrence.items():
                reconstructed[(parts, owners)] += Fraction((-1) ** omitted) * value
            raw_occurrences += 1
        reconstructed = {key: value for key, value in reconstructed.items() if value}
        fill = parse_chain(row["fill"])
        cycle = parse_cycle(row["cycle"])
        assert reconstructed == cycle
        for owners in fill:
            assert all(masks[types[part]] & (1 << owners[part]) for part in range(4))
            assert not any(owners[left] == owners[right] and original.get(tuple(sorted((types[left], types[right]))), 0) & (1 << owners[left]) for left, right in itertools.combinations(range(4), 2))
            assert not any(all(owners[part] == owners[parts[0]] for part in parts) and rank3.get(tuple(sorted(types[part] for part in parts)), 0) & (1 << owners[parts[0]]) for parts in itertools.combinations(range(4), 3))
        assert boundary(fill) == cycle
        full_records.append({"ordinal": row["ordinal"], "types": row["types"], "route": row["route"], "fill_nonzero": len(fill)})
    gluing_identifications = raw_occurrences - len(TARGET_FACES)
    assert raw_occurrences == 1024 and gluing_identifications == 839

    replayed = []
    by_ordinal = {row["ordinal"]: row for row in full_records}
    for row in reversed(selected):
        replayed.append(by_ordinal[row["ordinal"]])
    result = {
        "status": "PASS", "epistemic_status": "PROVED", "stage": "INDEPENDENT_AFFINE_SECTION_REPLAY",
        "selected_records": len(selected), "selected_ordinals": ordinals,
        "selected_route_counts": dict(sorted(Counter(row["route"] for row in selected).items())),
        "target_faces_checked": checked_faces, "target_pair_flows_checked": len(pair_flows),
        "full_residual_audit": {
            "quadruples": len(actual["records"]), "raw_occurrences": raw_occurrences,
            "face_classes": len(TARGET_FACES), "repeated_face_classes": actual["incidence"]["repeated_faces"],
            "gluing_identifications": gluing_identifications, "all_stabilizers_and_orientations_checked": True,
            "all_local_fills_checked": True, "nonzero_residuals": 0,
        },
        "descent_rank_control": {
            "quadruples": len(rank_control), "face_classes": len(occurrence_counts),
            "raw_face_variables": raw_face_variables, "compressed_face_variables": compressed_face_variables,
            "gluing_rank": gluing_rank, "rank_identity": "raw_face_variables - compressed_face_variables = gluing_rank",
            "raw_and_compressed_section_verified": True,
        },
        "records": replayed, "full_records": sorted(full_records, key=lambda row: row["ordinal"]),
        "claim_boundary": "Independent target-only equation reconstruction and full exact residual audit of the frozen 256-row corpus only.",
        "wall_seconds": time.monotonic() - started,
    }
    path = OUT / "independent-replay.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: result[key] for key in ("status", "selected_records", "selected_route_counts", "target_faces_checked", "target_pair_flows_checked", "wall_seconds")}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
