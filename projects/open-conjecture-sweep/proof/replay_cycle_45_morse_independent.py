#!/usr/bin/env python3
"""Independent direct-signature replay of Cycle 45 actual Morse projections."""
from __future__ import annotations

from collections import defaultdict
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

OUT = ROOT / "discovery/out/cycle45-critical-projection"
MASKS = []
DISTINGUISHED = []
PAIR_DELETED = {}
TRIPLE_DELETED = {}
FACES = {}


def tidy(chain):
    return {cell: value for cell, value in chain.items() if value}


def plus(left, right):
    out = defaultdict(Fraction, left)
    for cell, value in right.items():
        out[cell] += value
    return tidy(out)


def cell_boundary(cell):
    return {cell[:index] + cell[index + 1:]: Fraction((-1) ** index) for index in range(len(cell))} if cell else {}


def chain_boundary(chain):
    out = defaultdict(Fraction)
    for cell, coefficient in chain.items():
        for face, incidence in cell_boundary(cell).items():
            out[face] += coefficient * incidence
    return tidy(out)


def complex_for(types):
    supports = [tuple(owner for owner in reversed(range(13)) if MASKS[value] & (1 << owner)) for value in types]
    cells = {-1: [()]}
    all_cells = {()}
    for dimension in range(4):
        values = []
        for parts in reversed(tuple(itertools.combinations(range(4), dimension + 1))):
            for owners in itertools.product(*(supports[part] for part in parts)):
                if any(owners[a] == owners[b] and PAIR_DELETED[tuple(sorted((types[parts[a]], types[parts[b]])))] & (1 << owners[a]) for a, b in itertools.combinations(range(dimension + 1), 2)):
                    continue
                blocked = False
                for positions in itertools.combinations(range(dimension + 1), 3):
                    triple_types = tuple(sorted(types[parts[index]] for index in positions))
                    triple_owners = tuple(owners[index] for index in positions)
                    if len(set(triple_owners)) == 1 and TRIPLE_DELETED[triple_types] & (1 << triple_owners[0]):
                        blocked = True
                        break
                if blocked:
                    continue
                cell = tuple(zip(parts, owners))
                values.append(cell)
                all_cells.add(cell)
        cells[dimension] = sorted(values, reverse=True)
    return supports, cells, all_cells


def make_matching(cells, all_cells, schedule):
    free = {cell: True for cell in all_cells}
    pairs = {}
    reverse = {}
    for part, owner in schedule:
        for dimension in range(-1, 3):
            for lower in reversed(cells[dimension]):
                if not free[lower] or any(vertex[0] == part for vertex in lower):
                    continue
                upper = tuple(sorted(lower + ((part, owner),)))
                if upper in free and free[upper]:
                    pairs[lower] = upper
                    reverse[upper] = lower
                    free[lower] = free[upper] = False
    graph = {cell: [] for cell in all_cells}
    for upper in all_cells:
        for lower in cell_boundary(upper):
            source, target = (lower, upper) if pairs.get(lower) == upper else (upper, lower)
            graph[source].append(target)
    color = {}

    def visit(cell):
        color[cell] = 1
        for target in graph[cell]:
            if color.get(target) == 1:
                return False
            if color.get(target, 0) == 0 and not visit(target):
                return False
        color[cell] = 2
        return True

    if not all(color.get(cell, 0) or visit(cell) for cell in sorted(all_cells, reverse=True)):
        raise AssertionError("independent matching cycle")
    return pairs


def vector(chain, pairs):
    out = defaultdict(Fraction)
    for lower, coefficient in chain.items():
        if lower in pairs:
            upper = pairs[lower]
            out[upper] -= coefficient / cell_boundary(upper)[lower]
    return tidy(out)


def project(chain, pairs, cap):
    current = tidy(chain)
    accumulated = defaultdict(Fraction)
    seen = set()
    for step in range(cap + 1):
        key = tuple(sorted(current.items()))
        if key in seen:
            raise AssertionError("independent flow cycle")
        seen.add(key)
        moved = vector(current, pairs)
        for cell, value in moved.items():
            accumulated[cell] += value
        following = plus(plus(current, chain_boundary(moved)), vector(chain_boundary(current), pairs))
        if following == current:
            return current, tidy(accumulated), step
        current = following
    raise AssertionError("independent flow cap")


def ordered_face(parts, types):
    ordered_types = tuple(types[part] for part in parts)
    sorted_types = tuple(sorted(ordered_types))
    permutation = next(permutation for permutation in itertools.permutations(range(3)) if tuple(sorted_types[permutation[index]] for index in range(3)) == ordered_types)
    return {tuple(owners[permutation[index]] for index in range(3)): value for owners, value in FACES[sorted_types].items()}


def moment(types):
    out = defaultdict(Fraction)
    for omitted in reversed(range(4)):
        parts = tuple(part for part in range(4) if part != omitted)
        for owners, value in ordered_face(parts, types).items():
            out[tuple(zip(parts, owners))] += Fraction((-1) ** omitted) * value
    return tidy(out)


def parse_projection(values):
    return {tuple((int(part), int(owner)) for part, owner in cell): Fraction(int(numerator), int(denominator)) for cell, numerator, denominator in values}


def replay_group(job):
    resource.setrlimit(resource.RLIMIT_AS, (1_600_000_000, 1_600_000_000))
    types, records = job
    supports, cells, all_cells = complex_for(types)
    distinguished = tuple(DISTINGUISHED[value] for value in types)
    initial_schedule = tuple((part, distinguished[part]) for part in range(4))
    initial_pairs = make_matching(cells, all_cells, initial_schedule)
    extended_schedule = initial_schedule + tuple((part, owner) for part in range(4) for owner in sorted(supports[part]) if owner != distinguished[part])
    extended_pairs = make_matching(cells, all_cells, extended_schedule)
    checked = []
    for record in records:
        cycle = moment(types)
        if chain_boundary(cycle):
            raise AssertionError("independent input cycle")
        projection, homotopy, steps = project(cycle, initial_pairs, len(all_cells) + 1)
        if projection != parse_projection(record["projection"]):
            raise AssertionError("independent initial projection")
        if chain_boundary(homotopy) != {cell: projection.get(cell, 0) - cycle.get(cell, 0) for cell in set(projection) | set(cycle) if projection.get(cell, 0) != cycle.get(cell, 0)}:
            raise AssertionError("independent initial homotopy")
        extended, extended_h, extended_steps = project(cycle, extended_pairs, len(all_cells) + 1)
        if extended != parse_projection(record["extended_projection"]):
            raise AssertionError("independent extended projection")
        if chain_boundary(extended_h) != {cell: extended.get(cell, 0) - cycle.get(cell, 0) for cell in set(extended) | set(cycle) if extended.get(cell, 0) != cycle.get(cell, 0)}:
            raise AssertionError("independent extended homotopy")
        checked.append((len(cycle), len(projection), len(extended), steps, extended_steps))
    return {"interfaces": len(records), "cells": len(all_cells) * len(records), "checked": checked}


def main():
    global MASKS, DISTINGUISHED, PAIR_DELETED, TRIPLE_DELETED, FACES
    started = time.monotonic()
    c38.prepare()
    complete_types = sorted({row[0] for owner_rows in c38._TYPE_ROWS for rows in owner_rows.values() for row in rows})
    MASKS = [sum(1 << owner for owner, signature in enumerate(value) if signature) for value in complete_types]
    patterns = [{rank: {tuple(sorted(int(value) for value in row["signatures"])) for row in c38._COORDINATES[owner]["patterns"] if int(row["rank"]) == rank} for rank in (2, 3)} for owner in range(13)]
    primary = json.loads((OUT / "actual-corpus-layered.json").read_text(encoding="utf-8"))
    types_list = [tuple(record["types"]) for record in primary["records"]]
    target_pairs = {tuple(sorted((types[a], types[b]))) for types in types_list for a, b in itertools.combinations(range(4), 2)}
    target_triples = {tuple(sorted(types[part] for part in parts)) for types in types_list for parts in itertools.combinations(range(4), 3)}
    PAIR_DELETED = {pair: sum(1 << owner for owner in range(13) if tuple(sorted(complete_types[value][owner] for value in pair)) in patterns[owner][2]) for pair in target_pairs}
    TRIPLE_DELETED = {triple: sum(1 << owner for owner in range(13) if tuple(sorted(complete_types[value][owner] for value in triple)) in patterns[owner][3]) for triple in target_triples}
    prior = json.loads((ROOT / "discovery/out/cycle41-multiplied-ideal/zero-support-closure.json").read_text(encoding="utf-8"))
    marginals = [{int(owner): Fraction(numerator, denominator) for owner, numerator, denominator in values} for values in prior["singleton_marginals_by_complete_type"]]
    DISTINGUISHED = [next(iter(values)) for values in marginals]
    for path in (ROOT / "discovery/out/cycle43-moment-h2-coupling/canonical-coupling.json", ROOT / "discovery/out/cycle44-nonanchor-coupling/coupling.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        for row in data["face_tensors"]:
            triple = tuple(row["triple"])
            tensor = {tuple(owners): Fraction(numerator, denominator) for owners, numerator, denominator in row["coefficients"]}
            if triple in FACES and FACES[triple] != tensor:
                raise AssertionError("independent cross-cycle face")
            FACES[triple] = tensor
    groups = defaultdict(list)
    for record in primary["records"]:
        groups[tuple(record["types"])].append(record)
    jobs = sorted(groups.items())
    with multiprocessing.Pool(3) as pool:
        rows = pool.map(replay_group, jobs, chunksize=1)
    checked = [value for row in rows for value in row["checked"]]
    payload = {"status": "PASS", "epistemic_status": "PROVED", "actual_interfaces": sum(row["interfaces"] for row in rows), "distinct_type_multisets": len(rows), "aggregate_allowed_simplices": sum(row["cells"] for row in rows), "initial_zero_projections": sum(value[1] == 0 for value in checked), "initial_nonzero_projections": sum(value[1] != 0 for value in checked), "extended_zero_projections": sum(value[2] == 0 for value in checked), "extended_nonzero_projections": sum(value[2] != 0 for value in checked), "maximum_initial_projection": max(value[1] for value in checked), "maximum_extended_projection": max(value[2] for value in checked), "maximum_initial_steps": max(value[3] for value in checked), "maximum_extended_steps": max(value[4] for value in checked), "direct_signature_pair_classes": len(PAIR_DELETED), "direct_signature_triple_classes": len(TRIPLE_DELETED), "wall_seconds": time.monotonic() - started}
    expected = (primary["actual_interfaces"], primary["zero_projections"], primary["nonzero_projections"], primary["extended_zero_projections"], primary["extended_nonzero_projections"], primary["maximum_projection_nonzero"], primary["maximum_extended_projection_nonzero"])
    observed = (payload["actual_interfaces"], payload["initial_zero_projections"], payload["initial_nonzero_projections"], payload["extended_zero_projections"], payload["extended_nonzero_projections"], payload["maximum_initial_projection"], payload["maximum_extended_projection"])
    if expected != observed:
        raise AssertionError((expected, observed))
    temporary = OUT / "independent-actual-replay.json.tmp"
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "independent-actual-replay.json")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
