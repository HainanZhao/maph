#!/usr/bin/env python3
"""Cycle 42 exact GF(2) census of selected four-partite horn complexes."""
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
import lrc_ownership_functional as c38
import lrc_signed_ownership_moments as c40
from lrc_multiplied_fill_probe import gf2_rank, homology_dimension

OUT = ROOT / "discovery/out/cycle42-h2-horn"
ANCHOR_ORDINALS = (0, 34_963, 69_926)
EXPECTED_ANCHORS = ((2, 5, 14), (14, 68, 71), (80, 1306, 1307))
TYPE_MASKS: list[int] = []
ORIGINAL: dict[tuple[int, int], int] = {}
RANK3: dict[tuple[int, int, int], int] = {}


def coordinate_data(owner: int):
    resource.setrlimit(resource.RLIMIT_AS, (1_600_000_000, 1_600_000_000))
    row = c40.coordinate_classes(owner)
    relevant_pairs = {
        tuple(sorted(pair))
        for anchor in EXPECTED_ANCHORS
        for pair in itertools.combinations(anchor, 2)
    }
    rank3 = set()
    raw_rank3 = 0
    for pattern in c38._COORDINATES[owner]["patterns"]:
        if int(pattern["rank"]) != 3:
            continue
        groups = [c38._TYPE_ROWS[owner][int(signature)] for signature in pattern["signatures"]]
        for rows in itertools.product(*groups):
            raw_rank3 += 1
            triple = tuple(sorted(c40._TYPE_ID[value[0]] for value in rows))
            if any(pair in relevant_pairs for pair in itertools.combinations(triple, 2)):
                rank3.add(triple)
    return {
        "owner": owner,
        "rank_two_tuples": row["rank_two_tuples"],
        "rank_three_tuples": raw_rank3,
        "rank_two_pairs": row["rank_two_pairs"],
        "relevant_rank_three": sorted(rank3),
    }


def reconstruct_anchors(multiplicities):
    small = {index for index, mask in enumerate(TYPE_MASKS) if mask.bit_count() <= 6}
    small_types = sorted(small)
    interface_cache = {}
    triples = nonzero = 0
    anchors = []
    targets = set(ANCHOR_ORDINALS)
    for small_index, left in enumerate(small_types):
        for right in small_types[small_index:]:
            for third in range(len(TYPE_MASKS)):
                triple = tuple(sorted((left, right, third)))
                values = [value for value in triple if value in small]
                if tuple(values[:2]) != (left, right):
                    continue
                if any(multiplicities[value] < count for value, count in Counter(triple).items()):
                    continue
                a, b, c = triple
                key = (
                    TYPE_MASKS[a], TYPE_MASKS[b], TYPE_MASKS[c],
                    ORIGINAL.get((a, b), 0), ORIGINAL.get((a, c), 0),
                    ORIGINAL.get((b, c), 0),
                )
                h1 = interface_cache.get(key)
                if h1 is None:
                    h1 = homology_dimension(
                        triple, ORIGINAL, TYPE_MASKS,
                        RANK3.get(triple, 0),
                    )
                    interface_cache[key] = h1
                triples += 1
                if h1:
                    if nonzero in targets:
                        anchors.append((nonzero, triple, h1))
                    nonzero += 1
    if (triples, len(interface_cache), sum(bool(v) for v in interface_cache.values()), nonzero) != (11_279_048, 352_495, 7_892, 69_927):
        raise AssertionError("Cycle 41 boundary reconstruction")
    anchors.sort()
    if tuple(row[1] for row in anchors) != EXPECTED_ANCHORS:
        raise AssertionError("anchor reconstruction")
    return anchors


def allowed_complex(types):
    supports = [tuple(owner for owner in range(13) if TYPE_MASKS[t] & (1 << owner)) for t in types]
    edges = []
    for a, b in itertools.combinations(range(4), 2):
        deleted = ORIGINAL.get(tuple(sorted((types[a], types[b]))), 0)
        for i in supports[a]:
            for j in supports[b]:
                if not (i == j and deleted & (1 << i)):
                    edges.append(((a, i), (b, j)))
    edge_id = {edge: index for index, edge in enumerate(edges)}
    triangles = []
    triangle_boundaries = []
    triangle_boundaries_q = []
    for parts in itertools.combinations(range(4), 3):
        deleted3 = RANK3.get(tuple(sorted(types[p] for p in parts)), 0)
        for owners in itertools.product(*(supports[p] for p in parts)):
            if owners[0] == owners[1] == owners[2] and deleted3 & (1 << owners[0]):
                continue
            candidate = tuple(
                ((parts[x], owners[x]), (parts[y], owners[y]))
                for x, y in itertools.combinations(range(3), 2)
            )
            if not all(edge in edge_id for edge in candidate):
                continue
            boundary = 0
            for edge in candidate:
                boundary ^= 1 << edge_id[edge]
            triangles.append(tuple(zip(parts, owners)))
            triangle_boundaries.append(boundary)
            triangle_boundaries_q.append({edge_id[candidate[2]]: Fraction(1), edge_id[candidate[1]]: Fraction(-1), edge_id[candidate[0]]: Fraction(1)})
    triangle_id = {face: index for index, face in enumerate(triangles)}
    tetra_boundaries = []
    tetra_boundaries_q = []
    for owners in itertools.product(*supports):
        faces = tuple(
            tuple((part, owners[part]) for part in range(4) if part != omitted)
            for omitted in range(4)
        )
        if all(face in triangle_id for face in faces):
            boundary = 0
            for face in faces:
                boundary ^= 1 << triangle_id[face]
            composed = 0
            for face in faces:
                composed ^= triangle_boundaries[triangle_id[face]]
            if composed:
                raise AssertionError("boundary squared")
            tetra_boundaries.append(boundary)
            tetra_boundaries_q.append({triangle_id[face]: Fraction((-1) ** omitted) for omitted, face in enumerate(faces)})
    rank_d2 = gf2_rank(triangle_boundaries)
    rank_d3 = gf2_rank(tetra_boundaries)
    h2 = len(triangles) - rank_d2 - rank_d3
    if h2 < 0:
        raise AssertionError("negative H2")

    def rational_rank(vectors):
        basis = {}
        maximum_bits = 1
        for source in vectors:
            row = dict(source)
            while row:
                pivot = min(row)
                if pivot not in basis:
                    scale = row[pivot]
                    row = {index: coefficient / scale for index, coefficient in row.items()}
                    basis[pivot] = row
                    for coefficient in row.values():
                        maximum_bits = max(maximum_bits, abs(coefficient.numerator).bit_length(), coefficient.denominator.bit_length())
                    break
                factor = row[pivot]
                for index, coefficient in basis[pivot].items():
                    row[index] = row.get(index, Fraction(0)) - factor * coefficient
                    if not row[index]:
                        del row[index]
        return len(basis), maximum_bits

    rank_d2_q, bits_d2 = rational_rank(triangle_boundaries_q)
    rank_d3_q, bits_d3 = rational_rank(tetra_boundaries_q)
    h2_q = len(triangles) - rank_d2_q - rank_d3_q
    if h2_q < 0 or h2_q > h2:
        raise AssertionError("field homology comparison")
    return {
        "vertices": sum(map(len, supports)),
        "edges": len(edges),
        "triangles": len(triangles),
        "tetrahedra": len(tetra_boundaries),
        "rank_d2_gf2": rank_d2,
        "rank_d3_gf2": rank_d3,
        "h2_gf2": h2,
        "rank_d2_q": rank_d2_q,
        "rank_d3_q": rank_d3_q,
        "h2_q": h2_q,
        "maximum_rational_coefficient_bits": max(bits_d2, bits_d3),
    }


def structural_key(types):
    return (
        tuple(TYPE_MASKS[value] for value in types),
        tuple(ORIGINAL.get(tuple(sorted((types[a], types[b]))), 0) for a, b in itertools.combinations(range(4), 2)),
        tuple(RANK3.get(tuple(sorted(types[p] for p in parts)), 0) for parts in itertools.combinations(range(4), 3)),
    )


def scan_row(job):
    anchor_index, fourth = job
    resource.setrlimit(resource.RLIMIT_AS, (2_000_000_000, 2_000_000_000))
    types = EXPECTED_ANCHORS[anchor_index] + (fourth,)
    row = allowed_complex(types)
    row.update({"anchor_index": anchor_index, "fourth_type": fourth, "types": list(types)})
    return row


def main():
    global TYPE_MASKS, ORIGINAL, RANK3
    started = time.monotonic()
    OUT.mkdir(parents=True, exist_ok=True)
    c38.prepare()
    types = sorted({row[0] for root in c38._TYPE_ROWS for rows in root.values() for row in rows})
    c40._TYPE_ID = {value: index for index, value in enumerate(types)}
    TYPE_MASKS = [sum(1 << owner for owner, signature in enumerate(value) if signature) for value in types]
    c40._TYPE_MASKS = TYPE_MASKS
    raw_types = []
    for point in range(c38._COVERAGE.shape[0]):
        value = tuple(
            sum(1 << offset for offset, digit in enumerate(c38._ALLOWED[coordinate]) if c38._COVERAGE[point, coordinate, digit])
            for coordinate in range(13)
        )
        raw_types.append(c40._TYPE_ID[value])
    multiplicities = Counter(raw_types)

    with multiprocessing.Pool(3) as pool:
        coordinate_rows = pool.map(coordinate_data, range(13), chunksize=1)
    original = defaultdict(int)
    rank3 = defaultdict(int)
    for row in coordinate_rows:
        owner = int(row["owner"])
        for pair in row["rank_two_pairs"]:
            original[tuple(pair)] |= 1 << owner
        for triple in row["relevant_rank_three"]:
            rank3[tuple(triple)] |= 1 << owner
    ORIGINAL = dict(original)
    RANK3 = dict(rank3)
    if sum(int(row["rank_two_tuples"]) for row in coordinate_rows) != 6_684_938:
        raise AssertionError("rank-two raw census")
    if sum(int(row["rank_three_tuples"]) for row in coordinate_rows) != 19_661_454:
        raise AssertionError("rank-three raw census")

    anchors = reconstruct_anchors(multiplicities)
    raw_jobs = [(anchor, fourth) for anchor in range(3) for fourth in range(len(types))]
    representatives = {}
    multiplicity = Counter()
    for anchor, fourth in raw_jobs:
        key = structural_key(EXPECTED_ANCHORS[anchor] + (fourth,))
        multiplicity[key] += 1
        representatives.setdefault(key, (anchor, fourth))
    jobs = [representatives[key] for key in representatives]
    with multiprocessing.Pool(3) as pool:
        distinct_rows = pool.map(scan_row, jobs, chunksize=1)
    rows = []
    for row in distinct_rows:
        key = structural_key(tuple(row["types"]))
        row["multiplicity"] = multiplicity[key]
        rows.append(row)
    nonzero = [row for row in rows if row["h2_q"]]
    aggregate = {key: sum(row[key] * row["multiplicity"] for row in rows) for key in ("vertices", "edges", "triangles", "tetrahedra")}
    aggregate_distinct = {key: sum(row[key] for row in rows) for key in ("vertices", "edges", "triangles", "tetrahedra")}
    caps = {"vertices": 250_000, "edges": 10_000_000, "triangles": 100_000_000, "tetrahedra": 500_000_000}
    for key, cap in caps.items():
        if aggregate[key] > cap:
            raise RuntimeError(f"aggregate {key} cap")
    if 3 * aggregate["triangles"] + 4 * aggregate["tetrahedra"] > 2_000_000_000:
        raise RuntimeError("exact matrix nonzero cap")
    if time.monotonic() - started > 3600:
        raise RuntimeError("aggregate wall cap")
    result = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "stage": "SELECTED_FOUR_PARTITE_GF2_H2_CENSUS",
        "anchors": [{"nonzero_ordinal": ordinal, "types": list(triple), "h1_gf2": h1} for ordinal, triple, h1 in anchors],
        "complete_types": len(types),
        "interfaces": len(raw_jobs),
        "raw_interfaces": len(raw_jobs),
        "distinct_interfaces": len(rows),
        "relevant_rank_three_classes": len(RANK3),
        "nonzero_h2_gf2": sum(row["multiplicity"] for row in rows if row["h2_gf2"]),
        "nonzero_h2_q": sum(row["multiplicity"] for row in rows if row["h2_q"]),
        "maximum_h2_gf2": max((row["h2_gf2"] for row in rows), default=0),
        "maximum_h2_q": max((row["h2_q"] for row in rows), default=0),
        "field_dimension_disagreements": sum(row["multiplicity"] for row in rows if row["h2_q"] != row["h2_gf2"]),
        "maximum_rational_coefficient_bits": max(row["maximum_rational_coefficient_bits"] for row in rows),
        "first_nonzero_h2": nonzero[0] if nonzero else None,
        "aggregate_cells": aggregate,
        "aggregate_distinct_cells": aggregate_distinct,
        "rows": rows,
        "claim_boundary": "Exact GF(2) and rational H2 on every distinct structural complex induced by the 3,954 preregistered four-type interfaces. Nonzero topology alone is not a Cycle 41 moment obstruction.",
        "wall_seconds": time.monotonic() - started,
    }
    temporary = OUT / "gf2-census.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "gf2-census.json")
    print(json.dumps({key: result[key] for key in ("status", "raw_interfaces", "distinct_interfaces", "relevant_rank_three_classes", "nonzero_h2_gf2", "nonzero_h2_q", "maximum_h2_q", "field_dimension_disagreements", "maximum_rational_coefficient_bits", "first_nonzero_h2", "aggregate_cells", "wall_seconds")}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
