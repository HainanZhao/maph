#!/usr/bin/env python3
"""Cycle 45 small abstract countermodel search for the Morse invariant."""
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
from lrc_moment_h2_coupling import sparse_solve
from lrc_morse_critical_projection import boundary, build_complex, lexicographic_matching, stabilize

OUT = ROOT / "discovery/out/cycle45-critical-projection"
SEED = "cycle45-critical-projection-v1"
PAIRS = tuple(itertools.combinations(range(4), 2))
TRIPLES = tuple(itertools.combinations(range(4), 3))


def bytes_for(counter):
    return b"".join(hashlib.sha256(f"{SEED}:{counter}:{block}".encode("ascii")).digest() for block in range(2))


def descriptor(counter):
    raw = bytes_for(counter)
    distinguished = tuple(raw[part] % 3 for part in range(4))
    support_masks = tuple((1 << distinguished[part]) | (raw[4 + part] & 7) for part in range(4))
    supports = tuple(tuple(owner for owner in range(3) if support_masks[part] & (1 << owner)) for part in range(4))
    pair_deleted = []
    for index, (left, right) in enumerate(PAIRS):
        value = (raw[8 + index] & 7) & support_masks[left] & support_masks[right]
        if distinguished[left] == distinguished[right]:
            value &= ~(1 << distinguished[left])
        pair_deleted.append(value)
    triple_deleted = []
    for index, parts in enumerate(TRIPLES):
        value = (raw[14 + index] & 7)
        for part in parts:
            value &= support_masks[part]
        triple_deleted.append(value)
    return (supports, distinguished, tuple(pair_deleted), tuple(triple_deleted))


def canonical_face(parts, supports, distinguished, pair_deleted, triple_deleted):
    cells = []
    deleted3 = triple_deleted[TRIPLES.index(parts)]
    for owners in itertools.product(*(supports[part] for part in parts)):
        if any(owners[a] == owners[b] and pair_deleted[PAIRS.index(tuple(sorted((parts[a], parts[b]))))] & (1 << owners[a]) for a, b in itertools.combinations(range(3), 2)):
            continue
        if len(set(owners)) == 1 and deleted3 & (1 << owners[0]):
            continue
        cells.append(owners)
    equations = []
    rhs = []
    for a, b in itertools.combinations(range(3), 2):
        left, right = parts[a], parts[b]
        deleted2 = pair_deleted[PAIRS.index((left, right))]
        for owner_a in supports[left]:
            for owner_b in supports[right]:
                if owner_a == owner_b and deleted2 & (1 << owner_a):
                    continue
                equations.append({column: Fraction(1) for column, owners in enumerate(cells) if owners[a] == owner_a and owners[b] == owner_b})
                rhs.append(Fraction(int(owner_a == distinguished[left] and owner_b == distinguished[right])))
    solved = sparse_solve(equations, rhs, len(cells))
    if solved["status"] != "CONSISTENT":
        return None
    tensor = {owners: value for owners, value in zip(cells, solved["solution"]) if value}
    for a, b in itertools.combinations(range(3), 2):
        observed = defaultdict(Fraction)
        for owners, value in tensor.items():
            observed[(owners[a], owners[b])] += value
        expected = {(distinguished[parts[a]], distinguished[parts[b]]): Fraction(1)}
        if {key: value for key, value in observed.items() if value} != expected:
            raise AssertionError("abstract face marginal")
    return tensor


def exact_projection_status(cells, projection):
    triangles = cells[2]
    row_id = {cell: index for index, cell in enumerate(triangles)}
    rows = [dict() for _ in triangles]
    for column, tetrahedron in enumerate(cells[3]):
        for face, value in boundary({tetrahedron: Fraction(1)}).items():
            rows[row_id[face]][column] = value
    rhs = [projection.get(face, Fraction(0)) for face in triangles]
    solved = sparse_solve(rows, rhs, len(cells[3]), track_relation=True)
    if solved["status"] == "CONSISTENT":
        fill = {cells[3][index]: value for index, value in enumerate(solved["solution"]) if value}
        if boundary(fill) != projection:
            raise AssertionError("abstract projection fill")
        return {"status": "BOUNDARY", "fill_nonzero": len(fill)}
    relation = solved["relation"]
    pairing = sum(relation[index] * rhs[index] for index in relation)
    if not pairing:
        raise AssertionError("abstract zero pairing")
    dual = {triangles[index]: value for index, value in relation.items() if value}
    return {"status": "NONBOUNDARY", "pairing": [pairing.numerator, pairing.denominator], "dual_nonzero": len(dual), "dual": serialize_chain(dual)}


def evaluate(item):
    resource.setrlimit(resource.RLIMIT_AS, (1_600_000_000, 1_600_000_000))
    key, counter = item
    supports, distinguished, pair_values, triple_values = key
    pair_deleted = {pair: value for pair, value in zip(PAIRS, pair_values)}
    triple_deleted = {parts: value for parts, value in zip(TRIPLES, triple_values)}
    faces = {}
    for parts in TRIPLES:
        tensor = canonical_face(parts, supports, distinguished, pair_values, triple_values)
        if tensor is None:
            return {"status": "FACE_INCONSISTENT", "counter": counter}
        faces[parts] = tensor
    cycle = defaultdict(Fraction)
    for omitted in range(4):
        parts = tuple(part for part in range(4) if part != omitted)
        for owners, value in faces[parts].items():
            cycle[tuple(zip(parts, owners))] += Fraction((-1) ** omitted) * value
    cycle = {cell: value for cell, value in cycle.items() if value}
    if boundary(cycle):
        raise AssertionError("abstract moment is not a cycle")
    cells, all_cells = build_complex(supports, pair_deleted, triple_deleted)
    matching = lexicographic_matching(cells, all_cells, distinguished)
    if not matching["acyclic"]:
        return {"status": "MATCHING_CYCLE", "counter": counter, "descriptor": serialize_key(key), "cycle_cells": serialize_cells(matching["cycle_cells"])}
    outcome = stabilize(cycle, matching)
    if outcome["status"] != "STABLE":
        return {"status": outcome["status"], "counter": counter, "descriptor": serialize_key(key)}
    projection = outcome["projection"]
    if boundary(outcome["positive_homotopy"]) != difference(projection, cycle):
        raise AssertionError("abstract cycle homotopy identity")
    projection_status = exact_projection_status(cells, projection) if projection else {"status": "ZERO", "fill_nonzero": 0}
    if projection:
        schedule = tuple((part, distinguished[part]) for part in range(4)) + tuple((part, owner) for part in range(4) for owner in supports[part] if owner != distinguished[part])
        extended_matching = lexicographic_matching(cells, all_cells, distinguished, vertex_schedule=schedule)
        if not extended_matching["acyclic"]:
            return {"status": "EXTENDED_MATCHING_CYCLE", "counter": counter, "descriptor": serialize_key(key), "cycle_cells": serialize_cells(extended_matching["cycle_cells"])}
        extended = stabilize(cycle, extended_matching)
        if extended["status"] != "STABLE":
            return {"status": f"EXTENDED_{extended['status']}", "counter": counter, "descriptor": serialize_key(key)}
        extended_projection = extended["projection"]
        if boundary(extended["positive_homotopy"]) != difference(extended_projection, cycle):
            raise AssertionError("abstract extended homotopy identity")
        extended_status = exact_projection_status(cells, extended_projection) if extended_projection else {"status": "ZERO", "fill_nonzero": 0}
        if projection_status["status"] == "NONBOUNDARY" and extended_status["status"] != "NONBOUNDARY":
            raise AssertionError("homotopy erased nonboundary class")
    else:
        extended_projection = {}
        extended = {"steps": outcome["steps"]}
        extended_status = {"status": "ZERO", "fill_nonzero": 0}
    selected_corner_deleted = sum(bool(triple_values[index] & (1 << distinguished[parts[0]])) for index, parts in enumerate(TRIPLES) if len({distinguished[part] for part in parts}) == 1)
    rank3_deleted_total = sum(value.bit_count() for value in triple_values)
    return {"status": "NONZERO_PROJECTION" if projection else "ZERO_PROJECTION", "counter": counter, "descriptor": serialize_key(key), "cells": sum(len(values) for values in cells.values()), "face_nonzero": sum(len(tensor) for tensor in faces.values()), "cycle_nonzero": len(cycle), "projection_nonzero": len(projection), "projection": serialize_chain(projection), "projection_status": projection_status["status"], "projection_fill_nonzero": projection_status.get("fill_nonzero"), "projection_pairing": projection_status.get("pairing"), "projection_dual": projection_status.get("dual"), "flow_steps": outcome["steps"], "matched_pairs": len(matching["lower_to_upper"]), "critical_cells": len(matching["critical"]), "extended_projection_nonzero": len(extended_projection), "extended_projection": serialize_chain(extended_projection), "extended_projection_status": extended_status["status"], "extended_projection_fill_nonzero": extended_status.get("fill_nonzero"), "extended_projection_pairing": extended_status.get("pairing"), "extended_projection_dual": extended_status.get("dual"), "extended_flow_steps": extended["steps"], "selected_corner_deletions": selected_corner_deleted, "rank3_deleted_total": rank3_deleted_total}


def difference(left, right):
    keys = set(left) | set(right)
    return {key: left.get(key, 0) - right.get(key, 0) for key in keys if left.get(key, 0) != right.get(key, 0)}


def serialize_chain(chain):
    return [[[[part, owner] for part, owner in cell], value.numerator, value.denominator] for cell, value in sorted(chain.items())]


def serialize_cells(cells):
    return [[[part, owner] for part, owner in cell] for cell in cells]


def serialize_key(key):
    supports, distinguished, pair_values, triple_values = key
    return {"supports": [list(values) for values in supports], "distinguished": list(distinguished), "pair_deleted": list(pair_values), "triple_deleted": list(triple_values)}


def main():
    started = time.monotonic()
    OUT.mkdir(parents=True, exist_ok=True)
    retained = {}
    for counter in range(50_000):
        key = descriptor(counter)
        retained.setdefault(key, counter)
    jobs = sorted(retained.items(), key=lambda item: item[1])
    with multiprocessing.Pool(3) as pool:
        rows = pool.map(evaluate, jobs, chunksize=16)
    counts = Counter(row["status"] for row in rows)
    errors = [row for row in rows if row["status"] not in ("FACE_INCONSISTENT", "ZERO_PROJECTION", "NONZERO_PROJECTION")]
    if errors:
        result = {"status": "ERROR", "epistemic_status": "PROVED", "first_error": errors[0], "hash_counters": 50000, "deduplicated_models": len(jobs), "outcome_counts": dict(sorted(counts.items())), "wall_seconds": time.monotonic() - started}
    else:
        countermodels = sorted((row for row in rows if row["status"] == "NONZERO_PROJECTION"), key=lambda row: (json.dumps(row["descriptor"], sort_keys=True), row["counter"]))
        admissible = [row for row in rows if row["status"] != "FACE_INCONSISTENT"]
        aggregate_cells = sum(row["cells"] for row in admissible)
        if aggregate_cells > 10_000_000 or time.monotonic() - started > 7200:
            raise RuntimeError("Cycle 45 abstract cap")
        signatures = Counter((row["selected_corner_deletions"], row["projection_status"]) for row in countermodels)
        nonboundary_countermodels = [row for row in countermodels if row["projection_status"] == "NONBOUNDARY"]
        rank3_free = [row for row in admissible if row["rank3_deleted_total"] == 0]
        rank3_free_nonboundary = sorted((row for row in rank3_free if row["projection_status"] == "NONBOUNDARY"), key=lambda row: (json.dumps(row["descriptor"], sort_keys=True), row["counter"]))
        result = {"status": "PASS", "epistemic_status": "PROVED", "stage": "ABSTRACT_LAYERED_LOCAL_AXIOM_COUNTERMODELS", "hash_counters": 50000, "deduplicated_models": len(jobs), "admissible_face_models": len(admissible), "face_inconsistent_models": counts["FACE_INCONSISTENT"], "zero_projection_models": counts["ZERO_PROJECTION"], "nonzero_projection_models": counts["NONZERO_PROJECTION"], "nonboundary_projection_models": len(nonboundary_countermodels), "extended_zero_projection_models": sum(not row["extended_projection_nonzero"] for row in admissible), "extended_nonzero_projection_models": sum(bool(row["extended_projection_nonzero"]) for row in admissible), "extended_nonboundary_projection_models": sum(row["extended_projection_status"] == "NONBOUNDARY" for row in admissible), "rank3_free_admissible_models": len(rank3_free), "rank3_free_nonzero_projection_models": sum(bool(row["projection_nonzero"]) for row in rank3_free), "rank3_free_nonboundary_projection_models": len(rank3_free_nonboundary), "rank3_free_extended_nonzero_models": sum(bool(row["extended_projection_nonzero"]) for row in rank3_free), "rank3_free_extended_nonboundary_models": sum(row["extended_projection_status"] == "NONBOUNDARY" for row in rank3_free), "aggregate_simplices": aggregate_cells, "least_countermodel": countermodels[0] if countermodels else None, "least_nonboundary_countermodel": nonboundary_countermodels[0] if nonboundary_countermodels else None, "least_rank3_free_nonboundary_countermodel": rank3_free_nonboundary[0] if rank3_free_nonboundary else None, "countermodel_signature_counts": {str(key): value for key, value in sorted(signatures.items())}, "claim_boundary": "Three-owner distinct-part abstract models only. A countermodel proves insufficiency of the named local axioms, not failure on realizable ownership interfaces.", "wall_seconds": time.monotonic() - started}
    temporary = OUT / "abstract-models.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "abstract-models.json")
    print(json.dumps({key: result[key] for key in result if key not in ("least_countermodel", "least_nonboundary_countermodel", "least_rank3_free_nonboundary_countermodel", "first_error")}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
