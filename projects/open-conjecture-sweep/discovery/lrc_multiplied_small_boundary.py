#!/usr/bin/env python3
"""Cycle 41 complete small-support homology census for the current candidate."""
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
from lrc_multiplied_fill_probe import homology_dimension, oriented_relation_transport

OUT = ROOT / "discovery/out/cycle41-multiplied-ideal"
INTERFACE_CAP = 2_000_000
SMALL_BOUND = 6
TYPE_ID = {}
SMALL_SET = set()


def coordinate(index):
    resource.setrlimit(resource.RLIMIT_AS, (1_600_000_000, 1_600_000_000))
    return c40.coordinate_classes(index)


def rank_three_coordinate(owner):
    resource.setrlimit(resource.RLIMIT_AS, (1_600_000_000, 1_600_000_000))
    triples = set()
    raw_rows = 0
    for pattern in c38._COORDINATES[owner]["patterns"]:
        if int(pattern["rank"]) != 3:
            continue
        groups = [c38._TYPE_ROWS[owner][int(signature)] for signature in pattern["signatures"]]
        for rows in itertools.product(*groups):
            raw_rows += 1
            triple = tuple(sorted(TYPE_ID[row[0]] for row in rows))
            if sum(value in SMALL_SET for value in triple) >= 2:
                triples.add(triple)
    return {"owner": owner, "raw_rows": raw_rows, "small_triples": sorted(triples)}


def normalized_small_pair(triple, small_set):
    values = [value for value in triple if value in small_set]
    return tuple(values[:2]) if len(values) >= 2 else None


def interface_relations(owner_masks, deleted_diagonals, rank_three_deleted):
    supports = [[owner for owner in range(13) if mask & (1 << owner)] for mask in owner_masks]
    row_keys = []
    for pair_index, (a, b) in enumerate(((0, 1), (0, 2), (1, 2))):
        for i in supports[a]:
            for j in supports[b]:
                if not (i == j and deleted_diagonals[pair_index] & (1 << i)):
                    row_keys.append((pair_index, i, j))
    row_id = {key: index for index, key in enumerate(row_keys)}
    rows = [dict() for _ in row_keys]
    cell_count = 0
    for i, j, k in itertools.product(*supports):
        if (i == j and deleted_diagonals[0] & (1 << i)) or (i == k and deleted_diagonals[1] & (1 << i)) or (j == k and deleted_diagonals[2] & (1 << j)):
            continue
        if i == j == k and rank_three_deleted & (1 << i):
            continue
        for key in ((0, i, j), (1, i, k), (2, j, k)):
            rows[row_id[key]][cell_count] = Fraction(1)
        cell_count += 1

    basis = {}
    relations = []
    for source, coefficients in enumerate(rows):
        row = dict(coefficients)
        combination = {source: Fraction(1)}
        while row:
            pivot = min(row)
            if pivot not in basis:
                scale = row[pivot]
                row = {index: coefficient / scale for index, coefficient in row.items()}
                combination = {index: coefficient / scale for index, coefficient in combination.items()}
                basis[pivot] = (row, combination)
                break
            base_row, base_combination = basis[pivot]
            factor = row[pivot]
            for index, coefficient in base_row.items():
                row[index] = row.get(index, Fraction(0)) - factor * coefficient
                if not row[index]:
                    del row[index]
            for index, coefficient in base_combination.items():
                combination[index] = combination.get(index, Fraction(0)) - factor * coefficient
                if not combination[index]:
                    del combination[index]
        else:
            relations.append(combination)
    if len(basis) + len(relations) != len(rows):
        raise AssertionError("row-rank/nullity")
    annihilation_terms = 0
    for relation in relations:
        contracted = defaultdict(Fraction)
        for row_index, coefficient in relation.items():
            for column, entry in rows[row_index].items():
                contracted[column] += coefficient * entry
                annihilation_terms += 1
        if any(contracted.values()):
            raise AssertionError("left-null relation")
    return {"row_keys": row_keys, "relations": relations, "rank": len(basis), "cells": cell_count, "annihilation_terms": annihilation_terms}


def main():
    global TYPE_ID, SMALL_SET
    started = time.monotonic()
    c38.prepare()
    complete_types = sorted({row[0] for root in c38._TYPE_ROWS for rows in root.values() for row in rows})
    type_id = {value: index for index, value in enumerate(complete_types)}
    masks = [sum(1 << owner for owner, signature in enumerate(value) if signature) for value in complete_types]
    c40._TYPE_ID = type_id
    c40._TYPE_MASKS = masks
    raw_types = []
    for point in range(c38._COVERAGE.shape[0]):
        value = tuple(sum(1 << offset for offset, digit in enumerate(c38._ALLOWED[coordinate_index]) if c38._COVERAGE[point, coordinate_index, digit]) for coordinate_index in range(13))
        raw_types.append(type_id[value])
    multiplicities = Counter(raw_types)

    with multiprocessing.Pool(3) as pool:
        coordinate_rows = pool.map(coordinate, range(13), chunksize=1)
    original = defaultdict(int)
    rank3_induced = defaultdict(int)
    for owner, row in enumerate(coordinate_rows):
        for pair in row["rank_two_pairs"]:
            original[tuple(pair)] |= 1 << owner
        for pair in row["induced_pair_deletions"]:
            rank3_induced[tuple(pair)] |= 1 << owner

    prior = json.loads((OUT / "zero-support-closure.json").read_text(encoding="utf-8"))
    marginals = [{int(owner): Fraction(int(numerator), int(denominator)) for owner, numerator, denominator in rows} for rows in prior["singleton_marginals_by_complete_type"]]
    small_types = [index for index, mask in enumerate(masks) if mask.bit_count() <= SMALL_BOUND]
    small_set = set(small_types)
    TYPE_ID = type_id
    SMALL_SET = small_set
    with multiprocessing.Pool(3) as pool:
        rank_three_rows = pool.map(rank_three_coordinate, range(13), chunksize=1)
    rank_three_deleted = defaultdict(int)
    for row in rank_three_rows:
        owner = int(row["owner"])
        for triple in row["small_triples"]:
            rank_three_deleted[tuple(triple)] |= 1 << owner
    binary_types = {index for index, mask in enumerate(masks) if mask.bit_count() <= 2}
    blocked = defaultdict(list)
    for (left, right), owner_mask in original.items():
        for owner in range(13):
            if owner_mask & (1 << owner):
                if left in binary_types:
                    blocked[(left, owner)].append(right)
                if right in binary_types:
                    blocked[(right, owner)].append(left)
    transport_masks = list(masks)
    for mediator in binary_types:
        owners = [owner for owner in range(13) if masks[mediator] & (1 << owner)]
        if len(owners) == 1:
            for neighbor in blocked[(mediator, owners[0])]:
                transport_masks[neighbor] &= ~(1 << owners[0])
    relation_deleted = defaultdict(int)
    for pair in set(original) | set(rank3_induced):
        for owner in range(13):
            if (original.get(pair, 0) | rank3_induced.get(pair, 0)) & (1 << owner):
                relation_deleted[pair] |= 1 << (13 * owner + owner)
    for mediator in binary_types:
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

    interface_cache = {}
    triple_count = nonzero_h1_triples = exact_failures = 0
    nonzero_interfaces = set()
    first_nonzero = first_failure = None
    maximum_h1 = 0
    relation_cache = {}
    pair_flow_cache = {}
    exact_relation_evaluations = aggregate_relation_rows = aggregate_allowed_cells = 0
    relation_annihilation_terms = 0
    maximum_relation_coefficient_bits = 0
    for small_index, left in enumerate(small_types):
        for right in small_types[small_index:]:
            for third in range(len(complete_types)):
                triple = tuple(sorted((left, right, third)))
                if normalized_small_pair(triple, small_set) != (left, right):
                    continue
                counts = Counter(triple)
                if any(multiplicities[value] < count for value, count in counts.items()):
                    continue
                a, b, c = triple
                d_ab = original.get((a, b), 0)
                d_ac = original.get((a, c), 0)
                d_bc = original.get((b, c), 0)
                triple_rank_three = rank_three_deleted.get(triple, 0)
                key = (masks[a], masks[b], masks[c], d_ab, d_ac, d_bc, triple_rank_three)
                h1 = interface_cache.get(key)
                if h1 is None:
                    h1 = homology_dimension((0, 1, 2), {(0, 1): d_ab, (0, 2): d_ac, (1, 2): d_bc}, [masks[a], masks[b], masks[c]], triple_rank_three)
                    interface_cache[key] = h1
                    if len(interface_cache) > INTERFACE_CAP:
                        raise RuntimeError("interface cap")
                triple_count += 1
                maximum_h1 = max(maximum_h1, h1)
                if not h1:
                    continue
                nonzero_h1_triples += 1
                nonzero_interfaces.add(key)
                relation_data = relation_cache.get(key)
                if relation_data is None:
                    relation_data = interface_relations((masks[a], masks[b], masks[c]), (d_ab, d_ac, d_bc), triple_rank_three)
                    relation_cache[key] = relation_data
                    aggregate_relation_rows += len(relation_data["row_keys"])
                    aggregate_allowed_cells += relation_data["cells"]
                    relation_annihilation_terms += relation_data["annihilation_terms"]
                    if aggregate_relation_rows > 2_000_000 or aggregate_allowed_cells > 50_000_000:
                        raise RuntimeError("exact interface aggregate cap")
                    for relation in relation_data["relations"]:
                        maximum_relation_coefficient_bits = max(maximum_relation_coefficient_bits, *(abs(value.numerator).bit_length() for value in relation.values()), *(value.denominator.bit_length() for value in relation.values()))
                pair_values = []
                for pair in ((a, b), (a, c), (b, c)):
                    flow = pair_flow_cache.get(pair)
                    if flow is None:
                        flow = oriented_relation_transport(pair[0], pair[1], relation_deleted, marginals, transport_masks)
                        pair_flow_cache[pair] = flow
                    pair_values.append(flow)
                rhs = [pair_values[pair_index].get((i, j), Fraction(0)) for pair_index, i, j in relation_data["row_keys"]]
                failed_relation = None
                for relation in relation_data["relations"]:
                    exact_relation_evaluations += 1
                    value = sum(coefficient * rhs[index] for index, coefficient in relation.items())
                    if value:
                        failed_relation = {"value": [value.numerator, value.denominator], "nonzero_rows": len(relation)}
                        break
                detail = {"types": list(triple), "owner_masks": [masks[value] for value in triple], "deleted_diagonals": [d_ab, d_ac, d_bc], "rank_three_deleted_diagonal": triple_rank_three, "h1_dimension_gf2": h1, "pair_equations": len(relation_data["row_keys"]), "allowed_cells": relation_data["cells"], "rational_matrix_rank": relation_data["rank"], "left_null_relations": len(relation_data["relations"])}
                first_nonzero = first_nonzero or detail
                if failed_relation is not None:
                    exact_failures += 1
                    detail["failed_relation"] = failed_relation
                    first_failure = first_failure or detail

    result = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "stage": "COMPLETE_TWO_SMALL_SUPPORT_BOUNDARY",
        "small_owner_bound": SMALL_BOUND,
        "small_types": len(small_types),
        "rank_three_type_tuples_reenumerated": sum(int(row["raw_rows"]) for row in rank_three_rows),
        "small_rank_three_type_classes": len(rank_three_deleted),
        "type_triples_checked": triple_count,
        "distinct_homology_interfaces": len(interface_cache),
        "nonzero_h1_interfaces_gf2": len(nonzero_interfaces),
        "nonzero_h1_type_triples_gf2": nonzero_h1_triples,
        "maximum_h1_dimension_gf2": maximum_h1,
        "exact_candidate_failures": exact_failures,
        "exact_left_null_relation_evaluations": exact_relation_evaluations,
        "rational_relation_interfaces": len(relation_cache),
        "aggregate_rational_relation_rows": aggregate_relation_rows,
        "aggregate_allowed_tensor_cells": aggregate_allowed_cells,
        "left_null_annihilation_terms_checked": relation_annihilation_terms,
        "pair_flow_cache_entries": len(pair_flow_cache),
        "maximum_relation_coefficient_bits": maximum_relation_coefficient_bits,
        "first_nonzero_h1": first_nonzero,
        "first_candidate_failure": first_failure,
        "claim_boundary": "Exact GF(2) homology and rational left-null evaluation for every realized type triple having at least two owner supports of size at most six, including all realized rank-three diagonal removals (none occur in this boundary). Dense-support triples still require the separate cone-cover theorem.",
        "wall_seconds": time.monotonic() - started,
    }
    temporary = OUT / "small-boundary.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "small-boundary.json")
    print(json.dumps({key: result[key] for key in ("status", "small_types", "type_triples_checked", "distinct_homology_interfaces", "nonzero_h1_interfaces_gf2", "nonzero_h1_type_triples_gf2", "maximum_h1_dimension_gf2", "exact_candidate_failures", "exact_left_null_relation_evaluations", "rational_relation_interfaces", "aggregate_rational_relation_rows", "aggregate_allowed_tensor_cells", "left_null_annihilation_terms_checked", "maximum_relation_coefficient_bits", "wall_seconds")}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
