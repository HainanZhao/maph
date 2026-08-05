#!/usr/bin/env python3
"""Cycle 44 outcome-blind stratified non-anchor holdout selector."""
from __future__ import annotations

from collections import Counter, defaultdict
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
import lrc_ownership_functional as c38
import lrc_signed_ownership_moments as c40

OUT = ROOT / "discovery/out/cycle44-nonanchor-coupling"
SEED = "cycle44-nonanchor-v1"
ANCHORS = {(2, 5, 14), (14, 68, 71), (80, 1306, 1307)}
MASKS = []
TYPE_ID = {}
TARGET_FACES = set()
ORIGINAL = {}
RANK3 = {}


def digest(label):
    return hashlib.sha256(label.encode("ascii")).hexdigest()


def coordinate_rank2(owner):
    resource.setrlimit(resource.RLIMIT_AS, (1_600_000_000, 1_600_000_000))
    pairs = set()
    raw = 0
    for pattern in c38._COORDINATES[owner]["patterns"]:
        if int(pattern["rank"]) != 2:
            continue
        groups = [c38._TYPE_ROWS[owner][int(signature)] for signature in pattern["signatures"]]
        for rows in itertools.product(*groups):
            raw += 1
            pairs.add(tuple(sorted(TYPE_ID[row[0]] for row in rows)))
    return owner, raw, sorted(pairs)


def coordinate_rank3(owner):
    resource.setrlimit(resource.RLIMIT_AS, (1_600_000_000, 1_600_000_000))
    triples = set()
    raw = 0
    for pattern in c38._COORDINATES[owner]["patterns"]:
        if int(pattern["rank"]) != 3:
            continue
        groups = [c38._TYPE_ROWS[owner][int(signature)] for signature in pattern["signatures"]]
        for rows in itertools.product(*groups):
            raw += 1
            triple = tuple(sorted(TYPE_ID[row[0]] for row in rows))
            if triple in TARGET_FACES:
                triples.add(triple)
    return owner, raw, sorted(triples)


def gf2_rank(vectors):
    basis = {}
    for value in vectors:
        while value:
            pivot = value.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = value
                break
            value ^= basis[pivot]
    return len(basis)


def h2_job(types):
    resource.setrlimit(resource.RLIMIT_AS, (2_000_000_000, 2_000_000_000))
    supports = [tuple(owner for owner in range(13) if MASKS[value] & (1 << owner)) for value in types]
    edges = []
    for a, b in itertools.combinations(range(4), 2):
        diagonal = ORIGINAL.get(tuple(sorted((types[a], types[b]))), 0)
        for i in supports[a]:
            for j in supports[b]:
                if not (i == j and diagonal & (1 << i)):
                    edges.append(((a, i), (b, j)))
    edge_id = {edge: index for index, edge in enumerate(edges)}
    triangles = []
    d2 = []
    for parts in itertools.combinations(range(4), 3):
        diagonal = RANK3.get(tuple(sorted(types[p] for p in parts)), 0)
        for owners in itertools.product(*(supports[p] for p in parts)):
            if owners[0] == owners[1] == owners[2] and diagonal & (1 << owners[0]):
                continue
            vertices = tuple(zip(parts, owners))
            candidates = tuple((vertices[x], vertices[y]) for x, y in itertools.combinations(range(3), 2))
            if not all(edge in edge_id for edge in candidates):
                continue
            boundary = 0
            for edge in candidates:
                boundary ^= 1 << edge_id[edge]
            triangles.append(vertices)
            d2.append(boundary)
    triangle_id = {face: index for index, face in enumerate(triangles)}
    d3 = []
    tetrahedra = 0
    for owners in itertools.product(*supports):
        faces = [tuple((part, owners[part]) for part in range(4) if part != omitted) for omitted in range(4)]
        if all(face in triangle_id for face in faces):
            value = 0
            for face in faces:
                value ^= 1 << triangle_id[face]
            d3.append(value)
            tetrahedra += 1
    h2 = len(triangles) - gf2_rank(d2) - gf2_rank(d3)
    if h2 < 0:
        raise AssertionError("negative H2")
    return {"types": list(types), "h2_gf2": h2, "vertices": sum(map(len, supports)), "edges": len(edges), "triangles": len(triangles), "tetrahedra": tetrahedra}


def main():
    global MASKS, TYPE_ID, TARGET_FACES, ORIGINAL, RANK3
    started = time.monotonic()
    OUT.mkdir(parents=True, exist_ok=True)
    c38.prepare()
    complete_types = sorted({row[0] for root in c38._TYPE_ROWS for rows in root.values() for row in rows})
    TYPE_ID = {value: index for index, value in enumerate(complete_types)}
    MASKS = [sum(1 << owner for owner, signature in enumerate(value) if signature) for value in complete_types]
    c40._TYPE_ID = TYPE_ID
    c40._TYPE_MASKS = MASKS
    raw_types = []
    for point in range(c38._COVERAGE.shape[0]):
        value = tuple(sum(1 << offset for offset, digit in enumerate(c38._ALLOWED[coordinate]) if c38._COVERAGE[point, coordinate, digit]) for coordinate in range(13))
        raw_types.append(TYPE_ID[value])
    multiplicities = Counter(raw_types)
    with multiprocessing.Pool(3) as pool:
        rank2_rows = pool.map(coordinate_rank2, range(13), chunksize=1)
    original = defaultdict(int)
    for owner, raw, pairs in rank2_rows:
        for pair in pairs:
            original[tuple(pair)] |= 1 << owner
    if sum(raw for _owner, raw, _pairs in rank2_rows) != 6_684_938:
        raise AssertionError("rank-two census")
    ORIGINAL = dict(original)

    def valid(types):
        counts = Counter(types)
        if any(count > multiplicities[value] for value, count in counts.items()):
            return False
        return not any(tuple(sorted(types[index] for index in positions)) in ANCHORS for positions in itertools.combinations(range(4), 3))

    candidates = {}
    for counter in range(100_000):
        raw = hashlib.sha256(f"{SEED}:{counter}".encode("ascii")).digest()
        types = tuple(sorted(int.from_bytes(raw[2 * index:2 * index + 2], "big") % 1318 for index in range(4)))
        if valid(types):
            candidates.setdefault(types, f"hash:{counter:06d}")
    for t in range(1318):
        families = (
            ("pair", tuple(sorted((t, t, (t + 1) % 1318, (t + 659) % 1318)))),
            ("two-pair", tuple(sorted((t, t, (t + 659) % 1318, (t + 659) % 1318)))),
            ("distinct", tuple(sorted((t, (t + 1) % 1318, (t + 17) % 1318, (t + 257) % 1318)))),
        )
        for family, types in families:
            if valid(types):
                source = f"constructed:{family}:{t:04d}"
                if types not in candidates or source < candidates[types]:
                    candidates[types] = source

    def descriptor(types):
        sizes = tuple(sorted(MASKS[value].bit_count() for value in types))
        repeats = tuple(sorted(Counter(types).values(), reverse=True))
        diagonals = [ORIGINAL.get(tuple(sorted((types[a], types[b]))), 0) for a, b in itertools.combinations(range(4), 2)]
        nonzero = sum(bool(value) for value in diagonals)
        deleted = sum(value.bit_count() for value in diagonals)
        product = math_prod(MASKS[value].bit_count() for value in types)
        density = 0 if product <= 256 else 1 if product <= 2048 else 2 if product <= 8192 else 3
        return sizes, repeats, nonzero, deleted, density

    strata = defaultdict(list)
    rows = {}
    for types, source in candidates.items():
        selection_hash = digest(f"{SEED}:select:{','.join(map(str, types))}")
        desc = descriptor(types)
        row = {"types": list(types), "source": source, "selection_hash": selection_hash, "support_profile": list(desc[0]), "repeat_partition": list(desc[1]), "nonzero_deleted_pairs": desc[2], "deleted_owner_total": desc[3], "density_bin": desc[4]}
        rows[types] = row
        strata[desc].append((selection_hash, types))
    preliminary_types = set()
    for values in strata.values():
        for _hash, types in sorted(values)[:4]:
            preliminary_types.add(types)
    if len(preliminary_types) > 10_000:
        reserves = set()
        repeat_groups = defaultdict(list)
        density_groups = defaultdict(list)
        for types in preliminary_types:
            repeat_groups[tuple(rows[types]["repeat_partition"])].append(types)
            density_groups[rows[types]["density_bin"]].append(types)
        for values in itertools.chain(repeat_groups.values(), density_groups.values()):
            reserves.add(min(values, key=lambda value: (rows[value]["selection_hash"], value)))
        ordered = sorted(preliminary_types - reserves, key=lambda value: (rows[value]["selection_hash"], value))
        preliminary_types = reserves | set(ordered[:10_000 - len(reserves)])
    preliminary = sorted(preliminary_types, key=lambda value: (rows[value]["selection_hash"], value))

    TARGET_FACES = {tuple(sorted(types[p] for p in parts)) for types in preliminary for parts in itertools.combinations(range(4), 3)}
    with multiprocessing.Pool(3) as pool:
        rank3_rows = pool.map(coordinate_rank3, range(13), chunksize=1)
    rank3 = defaultdict(int)
    for owner, raw, triples in rank3_rows:
        for triple in triples:
            rank3[tuple(triple)] |= 1 << owner
    if sum(raw for _owner, raw, _triples in rank3_rows) != 19_661_454:
        raise AssertionError("rank-three census")
    RANK3 = dict(rank3)

    structural_representatives = {}
    structural_members = defaultdict(list)
    for types in preliminary:
        key = (tuple(MASKS[value] for value in types), tuple(ORIGINAL.get(tuple(sorted((types[a], types[b]))), 0) for a, b in itertools.combinations(range(4), 2)), tuple(RANK3.get(tuple(sorted(types[p] for p in parts)), 0) for parts in itertools.combinations(range(4), 3)))
        structural_representatives.setdefault(key, types)
        structural_members[key].append(types)
    with multiprocessing.Pool(3) as pool:
        h2_rows = pool.map(h2_job, list(structural_representatives.values()), chunksize=1)
    h2_by_key = {key: row for key, row in zip(structural_representatives, h2_rows)}
    for key, members in structural_members.items():
        h2 = h2_by_key[key]["h2_gf2"]
        h2_bin = 0 if h2 == 0 else 1 if h2 <= 3 else 2 if h2 <= 15 else 3
        for types in members:
            rows[types]["h2_gf2"] = h2
            rows[types]["h2_bin"] = h2_bin
    refined = defaultdict(list)
    for types in preliminary:
        row = rows[types]
        desc = (tuple(row["support_profile"]), tuple(row["repeat_partition"]), row["nonzero_deleted_pairs"], row["deleted_owner_total"], row["density_bin"], row["h2_bin"])
        refined[desc].append((row["selection_hash"], types))
    selected_types = set()
    for values in refined.values():
        for _hash, types in sorted(values)[:2]:
            selected_types.add(types)
    if len(selected_types) > 2000:
        reserves = set()
        dimensions = ("h2_bin", "density_bin")
        for dimension in dimensions:
            groups = defaultdict(list)
            for types in selected_types:
                groups[rows[types][dimension]].append(types)
            for values in groups.values():
                reserves.add(min(values, key=lambda value: (rows[value]["selection_hash"], value)))
        repeat_groups = defaultdict(list)
        for types in selected_types:
            repeat_groups[tuple(rows[types]["repeat_partition"])].append(types)
        for values in repeat_groups.values():
            reserves.add(min(values, key=lambda value: (rows[value]["selection_hash"], value)))
        ordered = sorted(selected_types - reserves, key=lambda value: (rows[value]["selection_hash"], value))
        selected_types = reserves | set(ordered[:2000 - len(reserves)])
    selected = [rows[types] for types in sorted(selected_types, key=lambda value: (rows[value]["selection_hash"], value))]
    if any(not valid(tuple(row["types"])) for row in selected):
        raise AssertionError("selected validity")
    result = {"status": "PASS", "epistemic_status": "PROVED", "stage": "OUTCOME_BLIND_NONANCHOR_SELECTION", "hash_counter_candidates": 100000, "deduplicated_candidate_pool": len(candidates), "preselection_strata": len(strata), "preliminary_interfaces": len(preliminary), "preliminary_structural_complexes": len(structural_representatives), "target_face_classes": len(TARGET_FACES), "rank_three_target_classes": len(RANK3), "refined_strata": len(refined), "selected_interfaces": len(selected), "selected": selected, "h2_bin_counts": dict(sorted(Counter(row["h2_bin"] for row in selected).items())), "repeat_partition_counts": {str(key): value for key, value in sorted(Counter(tuple(row["repeat_partition"]) for row in selected).items())}, "density_bin_counts": dict(sorted(Counter(row["density_bin"] for row in selected).items())), "claim_boundary": "Outcome-blind deterministic selection only; no moment face or filling result was inspected.", "wall_seconds": time.monotonic() - started}
    temporary = OUT / "selection.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "selection.json")
    print(json.dumps({key: result[key] for key in ("status", "deduplicated_candidate_pool", "preselection_strata", "preliminary_interfaces", "preliminary_structural_complexes", "target_face_classes", "rank_three_target_classes", "refined_strata", "selected_interfaces", "h2_bin_counts", "repeat_partition_counts", "density_bin_counts", "wall_seconds")}, sort_keys=True))


def math_prod(values):
    result = 1
    for value in values:
        result *= value
    return result


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
