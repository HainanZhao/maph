#!/usr/bin/env python3
"""Cycle 45 exact Morse-flow census on the frozen Cycle 43/44 corpus."""
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
from lrc_moment_h2_coupling import sparse_solve
from lrc_morse_critical_projection import boundary, build_complex, lexicographic_matching, stabilize

OUT = ROOT / "discovery/out/cycle45-critical-projection"
MASKS = []
TYPE_ID = {}
TARGET_FACES = set()
ORIGINAL = {}
RANK3 = {}
FACE_TENSORS = {}
DISTINGUISHED = []


def coordinate(index):
    resource.setrlimit(resource.RLIMIT_AS, (1_600_000_000, 1_600_000_000))
    return c40.coordinate_classes(index)


def coordinate_rank3(owner):
    resource.setrlimit(resource.RLIMIT_AS, (1_600_000_000, 1_600_000_000))
    found = set()
    raw = 0
    for pattern in c38._COORDINATES[owner]["patterns"]:
        if int(pattern["rank"]) != 3:
            continue
        groups = [c38._TYPE_ROWS[owner][int(signature)] for signature in pattern["signatures"]]
        for rows in itertools.product(*groups):
            raw += 1
            triple = tuple(sorted(TYPE_ID[row[0]] for row in rows))
            if triple in TARGET_FACES:
                found.add(triple)
    return owner, raw, sorted(found)


def ordered_face(parts, types):
    ordered_types = tuple(types[part] for part in parts)
    sorted_types = tuple(sorted(ordered_types))
    tensor = FACE_TENSORS[sorted_types]
    permutation = next(permutation for permutation in itertools.permutations(range(3)) if tuple(sorted_types[permutation[index]] for index in range(3)) == ordered_types)
    return {tuple(owners[permutation[index]] for index in range(3)): value for owners, value in tensor.items()}


def moment_cycle(types):
    cycle = defaultdict(Fraction)
    for omitted in range(4):
        parts = tuple(part for part in range(4) if part != omitted)
        for owners, value in ordered_face(parts, types).items():
            cycle[tuple(zip(parts, owners))] += Fraction((-1) ** omitted) * value
    return {cell: value for cell, value in cycle.items() if value}


def structure(types):
    supports = tuple(tuple(owner for owner in range(13) if MASKS[value] & (1 << owner)) for value in types)
    distinguished = tuple(DISTINGUISHED[value] for value in types)
    pair_deleted = {(a, b): ORIGINAL.get(tuple(sorted((types[a], types[b]))), 0) for a, b in itertools.combinations(range(4), 2)}
    triple_deleted = {parts: RANK3.get(tuple(sorted(types[part] for part in parts)), 0) for parts in itertools.combinations(range(4), 3)}
    key = (supports, distinguished, tuple(pair_deleted.values()), tuple(triple_deleted.values()))
    return key, supports, distinguished, pair_deleted, triple_deleted


def exact_projection_fill(cells, projection):
    triangles = cells[2]
    triangle_id = {cell: index for index, cell in enumerate(triangles)}
    tetrahedra = cells[3]
    rows = [dict() for _ in triangles]
    for column, tetrahedron in enumerate(tetrahedra):
        for face, value in boundary({tetrahedron: Fraction(1)}).items():
            rows[triangle_id[face]][column] = value
    rhs = [projection.get(face, Fraction(0)) for face in triangles]
    solved = sparse_solve(rows, rhs, len(tetrahedra), track_relation=True)
    if solved["status"] == "CONSISTENT":
        fill = {tetrahedra[index]: value for index, value in enumerate(solved["solution"]) if value}
        if boundary(fill) != projection:
            raise AssertionError("projection fill replay")
        return {"status": "BOUNDARY", "fill_nonzero": len(fill)}
    relation = solved["relation"]
    pairing = sum(relation[index] * rhs[index] for index in relation)
    if not pairing:
        raise AssertionError("zero projection pairing")
    return {"status": "NONBOUNDARY", "pairing": [pairing.numerator, pairing.denominator], "dual_nonzero": len(relation)}


def defect_reasons(cell, missing, distinguished, pair_deleted, triple_deleted, all_cells):
    upper = tuple(sorted(cell + ((missing, distinguished[missing]),)))
    if upper in all_cells:
        return ["EXTENSION_ALLOWED"]
    owner_by_part = dict(cell)
    reasons = []
    selected = distinguished[missing]
    for part, owner in cell:
        pair = tuple(sorted((part, missing)))
        if owner == selected and pair_deleted[pair] & (1 << selected):
            reasons.append(f"R2:{pair}:{selected}")
    for parts in itertools.combinations(range(4), 3):
        if missing not in parts or not all(part in owner_by_part or part == missing for part in parts):
            continue
        owners = tuple(selected if part == missing else owner_by_part[part] for part in parts)
        if len(set(owners)) == 1 and triple_deleted[parts] & (1 << owners[0]):
            reasons.append(f"R3:{parts}:{owners[0]}")
    return reasons or ["UNCLASSIFIED"]


def process_group(job):
    resource.setrlimit(resource.RLIMIT_AS, (2_000_000_000, 2_000_000_000))
    key, members = job
    supports, distinguished, pair_values, triple_values = key
    pair_deleted = {pair: value for pair, value in zip(itertools.combinations(range(4), 2), pair_values)}
    triple_deleted = {parts: value for parts, value in zip(itertools.combinations(range(4), 3), triple_values)}
    cells, all_cells = build_complex(supports, pair_deleted, triple_deleted)
    matching = lexicographic_matching(cells, all_cells, distinguished)
    if not matching["acyclic"]:
        return {"status": "MATCHING_CYCLE", "key": key, "cycle_cells": matching["cycle_cells"], "members": members}
    rows = []
    maximum_steps = 0
    for member in members:
        types = tuple(member["types"])
        cycle = moment_cycle(types)
        if boundary(cycle):
            raise AssertionError("input is not a cycle")
        outcome = stabilize(cycle, matching)
        if outcome["status"] != "STABLE":
            return {"status": outcome["status"], "key": key, "detail": outcome, "member": member}
        projection = outcome["projection"]
        maximum_steps = max(maximum_steps, outcome["steps"])
        positive_h = outcome["positive_homotopy"]
        # For a cycle, pi(z)-z=dH(z).
        if boundary(positive_h) != {cell: projection.get(cell, 0) - cycle.get(cell, 0) for cell in set(projection) | set(cycle) if projection.get(cell, 0) != cycle.get(cell, 0)}:
            raise AssertionError("cycle homotopy identity")
        defects = defaultdict(int)
        for cell in projection:
            missing = next(part for part in range(4) if all(vertex[0] != part for vertex in cell))
            for reason in defect_reasons(cell, missing, distinguished, pair_deleted, triple_deleted, all_cells):
                defects[reason.split(":", 1)[0]] += 1
        projection_status = "BOUNDARY_FROM_PRIOR_AND_HOMOTOPY" if projection else "ZERO"
        if projection:
            schedule = tuple((part, distinguished[part]) for part in range(4)) + tuple((part, owner) for part in range(4) for owner in supports[part] if owner != distinguished[part])
            extended_matching = lexicographic_matching(cells, all_cells, distinguished, vertex_schedule=schedule)
            if not extended_matching["acyclic"]:
                return {"status": "EXTENDED_MATCHING_CYCLE", "key": key, "cycle_cells": extended_matching["cycle_cells"], "member": member}
            extended = stabilize(cycle, extended_matching)
            if extended["status"] != "STABLE":
                return {"status": f"EXTENDED_{extended['status']}", "key": key, "detail": extended, "member": member}
            extended_projection = extended["projection"]
            if boundary(extended["positive_homotopy"]) != {cell: extended_projection.get(cell, 0) - cycle.get(cell, 0) for cell in set(extended_projection) | set(cycle) if extended_projection.get(cell, 0) != cycle.get(cell, 0)}:
                raise AssertionError("extended cycle homotopy identity")
        else:
            extended_projection = {}
            extended = {"steps": outcome["steps"], "positive_homotopy": positive_h}
        rows.append({"source": member["source"], "ordinal": member["ordinal"], "types": list(types), "cycle_nonzero": len(cycle), "projection_nonzero": len(projection), "projection": [[[list(vertex) for vertex in cell], value.numerator, value.denominator] for cell, value in sorted(projection.items())], "projection_status": projection_status, "projection_fill_nonzero": None, "projection_pairing": None, "flow_steps": outcome["steps"], "homotopy_nonzero": len(positive_h), "defect_reason_counts": dict(sorted(defects.items())), "extended_projection_nonzero": len(extended_projection), "extended_projection": [[[list(vertex) for vertex in cell], value.numerator, value.denominator] for cell, value in sorted(extended_projection.items())], "extended_flow_steps": extended["steps"], "extended_homotopy_nonzero": len(extended["positive_homotopy"])})
    return {"status": "PASS", "cells": {str(dimension): len(values) for dimension, values in cells.items()}, "matched_pairs": len(matching["lower_to_upper"]), "critical_cells": len(matching["critical"]), "maximum_steps": maximum_steps, "members": rows}


def main():
    global MASKS, TYPE_ID, TARGET_FACES, ORIGINAL, RANK3, FACE_TENSORS, DISTINGUISHED
    started = time.monotonic()
    OUT.mkdir(parents=True, exist_ok=True)
    c38.prepare()
    complete_types = sorted({row[0] for owner_rows in c38._TYPE_ROWS for rows in owner_rows.values() for row in rows})
    TYPE_ID = {value: index for index, value in enumerate(complete_types)}
    MASKS = [sum(1 << owner for owner, signature in enumerate(value) if signature) for value in complete_types]
    c40._TYPE_ID = TYPE_ID
    c40._TYPE_MASKS = MASKS
    prior = json.loads((ROOT / "discovery/out/cycle41-multiplied-ideal/zero-support-closure.json").read_text(encoding="utf-8"))
    marginals = [{int(owner): Fraction(numerator, denominator) for owner, numerator, denominator in values} for values in prior["singleton_marginals_by_complete_type"]]
    if any(len(values) != 1 or next(iter(values.values())) != 1 for values in marginals):
        raise AssertionError("non-delta marginal")
    DISTINGUISHED = [next(iter(values)) for values in marginals]
    primary43 = json.loads((ROOT / "discovery/out/cycle43-moment-h2-coupling/canonical-coupling.json").read_text(encoding="utf-8"))
    primary44 = json.loads((ROOT / "discovery/out/cycle44-nonanchor-coupling/coupling.json").read_text(encoding="utf-8"))
    for primary in (primary43, primary44):
        for row in primary["face_tensors"]:
            triple = tuple(row["triple"])
            tensor = {tuple(owners): Fraction(numerator, denominator) for owners, numerator, denominator in row["coefficients"]}
            if triple in FACE_TENSORS and FACE_TENSORS[triple] != tensor:
                raise AssertionError("cross-cycle face mismatch")
            FACE_TENSORS[triple] = tensor
    members = []
    for source, primary in (("C43", primary43), ("C44", primary44)):
        for ordinal, row in enumerate(primary["interface_records"]):
            members.append({"source": source, "ordinal": ordinal, "types": row["types"]})
    if len(members) != 5954:
        raise AssertionError("actual corpus size")
    TARGET_FACES = {tuple(sorted(member["types"][part] for part in parts)) for member in members for parts in itertools.combinations(range(4), 3)}
    with multiprocessing.Pool(3) as pool:
        coordinate_rows = pool.map(coordinate, range(13), chunksize=1)
    original = defaultdict(int)
    for owner, row in enumerate(coordinate_rows):
        for pair in row["rank_two_pairs"]:
            original[tuple(pair)] |= 1 << owner
    ORIGINAL = dict(original)
    with multiprocessing.Pool(3) as pool:
        rank3_rows = pool.map(coordinate_rank3, range(13), chunksize=1)
    if sum(raw for _owner, raw, _triples in rank3_rows) != 19_661_454:
        raise AssertionError("rank-three census")
    rank3 = defaultdict(int)
    for owner, _raw, triples in rank3_rows:
        for triple in triples:
            rank3[triple] |= 1 << owner
    RANK3 = dict(rank3)

    groups = defaultdict(list)
    for member in members:
        key, _supports, _distinguished, _pairs, _triples = structure(tuple(member["types"]))
        groups[key].append(member)
    jobs = sorted(groups.items(), key=lambda item: item[0])
    with multiprocessing.Pool(3) as pool:
        group_rows = pool.map(process_group, jobs, chunksize=1)
    failures = [row for row in group_rows if row["status"] != "PASS"]
    if failures:
        result = {"status": "FALSIFIER", "epistemic_status": "PROVED", "first_failure": failures[0], "groups_completed": len(group_rows) - len(failures), "structural_groups": len(group_rows), "wall_seconds": time.monotonic() - started}
    else:
        records = sorted((record for group in group_rows for record in group["members"]), key=lambda row: (row["source"], row["ordinal"]))
        aggregate_cells = sum(sum(group["cells"].values()) * len(group["members"]) for group in group_rows)
        if aggregate_cells > 100_000_000 or time.monotonic() - started > 7200:
            raise RuntimeError("Cycle 45 actual cap")
        defect_counts = sum((Counter(row["defect_reason_counts"]) for row in records), Counter())
        result = {"status": "PASS", "epistemic_status": "PROVED", "stage": "ACTUAL_CORPUS_LAYERED_MORSE_PROJECTION", "actual_interfaces": len(records), "structural_groups": len(groups), "face_classes": len(FACE_TENSORS), "rank_three_target_classes": len(RANK3), "aggregate_allowed_simplices": aggregate_cells, "matching_cycles": 0, "zero_projections": sum(not row["projection_nonzero"] for row in records), "nonzero_projections": sum(bool(row["projection_nonzero"]) for row in records), "nonboundary_projections": sum(row["projection_status"] == "NONBOUNDARY" for row in records), "maximum_projection_nonzero": max(row["projection_nonzero"] for row in records), "maximum_flow_steps": max(row["flow_steps"] for row in records), "extended_zero_projections": sum(not row["extended_projection_nonzero"] for row in records), "extended_nonzero_projections": sum(bool(row["extended_projection_nonzero"]) for row in records), "maximum_extended_projection_nonzero": max(row["extended_projection_nonzero"] for row in records), "maximum_extended_flow_steps": max(row["extended_flow_steps"] for row in records), "defect_reason_counts": dict(sorted(defect_counts.items())), "records": records, "claim_boundary": "Exact layered critical projection on the frozen Cycle 43/44 corpus only; zero projection would not prove the operator works on all actual type multisets.", "wall_seconds": time.monotonic() - started}
    temporary = OUT / "actual-corpus-layered.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "actual-corpus-layered.json")
    print(json.dumps({key: result[key] for key in result if key not in ("records", "first_failure")}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
