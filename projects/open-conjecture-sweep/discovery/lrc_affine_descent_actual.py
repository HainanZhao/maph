#!/usr/bin/env python3
"""Cycle 47 exact canonical global section on the connected p199 patch."""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
import itertools
import json
import multiprocessing
from pathlib import Path
import time

import lrc_nonanchor_coupling as core
from lrc_cech_total import direct_boundary_solve
from lrc_morse_critical_projection import build_complex

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle47-affine-descent"


def initialize(selected):
    core.c38.prepare()
    complete = sorted({row[0] for root in core.c38._TYPE_ROWS for rows in root.values() for row in rows})
    core.TYPE_ID = {value: index for index, value in enumerate(complete)}
    core.MASKS = [sum(1 << owner for owner, signature in enumerate(value) if signature) for value in complete]
    core.c40._TYPE_ID = core.TYPE_ID
    core.c40._TYPE_MASKS = core.MASKS
    core.TARGET_FACES = {
        tuple(sorted(types[part] for part in parts))
        for types in selected for parts in itertools.combinations(range(4), 3)
    }
    with multiprocessing.Pool(2) as pool:
        coordinate_rows = pool.map(core.coordinate, range(13), chunksize=1)
    original = defaultdict(int)
    induced = defaultdict(int)
    for owner, row in enumerate(coordinate_rows):
        for pair in row["rank_two_pairs"]:
            original[tuple(pair)] |= 1 << owner
        for pair in row["induced_pair_deletions"]:
            induced[tuple(pair)] |= 1 << owner
    core.ORIGINAL = dict(original)
    with multiprocessing.Pool(2) as pool:
        rank3_rows = pool.map(core.coordinate_rank3, range(13), chunksize=1)
    rank3 = defaultdict(int)
    for owner, raw, triples in rank3_rows:
        for triple in triples:
            rank3[tuple(triple)] |= 1 << owner
    if sum(raw for _owner, raw, _triples in rank3_rows) != 19_661_454:
        raise AssertionError("rank-three census")
    core.RANK3 = dict(rank3)

    binary = {index for index, mask in enumerate(core.MASKS) if mask.bit_count() <= 2}
    blocked = defaultdict(list)
    for (left, right), owner_mask in core.ORIGINAL.items():
        for owner in range(13):
            if owner_mask & (1 << owner):
                if left in binary:
                    blocked[(left, owner)].append(right)
                if right in binary:
                    blocked[(right, owner)].append(left)
    core.TRANSPORT_MASKS = list(core.MASKS)
    for mediator in binary:
        owners = [owner for owner in range(13) if core.MASKS[mediator] & (1 << owner)]
        if len(owners) == 1:
            for neighbor in blocked[(mediator, owners[0])]:
                core.TRANSPORT_MASKS[neighbor] &= ~(1 << owners[0])
    relation_deleted = defaultdict(int)
    for pair in set(core.ORIGINAL) | set(induced):
        for owner in range(13):
            if (core.ORIGINAL.get(pair, 0) | induced.get(pair, 0)) & (1 << owner):
                relation_deleted[pair] |= 1 << (13 * owner + owner)
    for mediator in binary:
        owners = [owner for owner in range(13) if core.MASKS[mediator] & (1 << owner)]
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
    core.RELATION_DELETED = dict(relation_deleted)
    prior = json.loads((ROOT / "discovery/out/cycle41-multiplied-ideal/zero-support-closure.json").read_text())
    core.MARGINALS = [
        {int(owner): Fraction(int(numerator), int(denominator)) for owner, numerator, denominator in values}
        for values in prior["singleton_marginals_by_complete_type"]
    ]
    if any(values != {next(iter(values)): Fraction(1)} for values in core.MARGINALS):
        raise AssertionError("non-delta singleton")
    face_classes = sorted(core.TARGET_FACES)
    pair_classes = sorted({(triple[x], triple[y]) for triple in face_classes for x, y in itertools.combinations(range(3), 2)})
    core.PAIR_FLOWS = {
        pair: core.oriented_relation_transport(pair[0], pair[1], core.RELATION_DELETED, core.MARGINALS, core.TRANSPORT_MASKS)
        for pair in pair_classes
    }
    with multiprocessing.Pool(2) as pool:
        face_rows = pool.map(core.canonical_face, face_classes, chunksize=4)
    core.FACE_TENSORS = {row["triple"]: row for row in face_rows}
    return face_rows, pair_classes


def moment_cycle(types):
    cycle = defaultdict(Fraction)
    for omitted in range(4):
        parts = tuple(part for part in range(4) if part != omitted)
        for owners, value in core.ordered_tensor(parts, types).items():
            cycle[(parts, owners)] += Fraction((-1) ** omitted) * value
    return {key: value for key, value in cycle.items() if value}


def cone_fill(types, cycle):
    for part in range(4):
        owner = next(iter(core.MARGINALS[types[part]]))
        opposite = tuple(index for index in range(4) if index != part)
        candidate = {}
        for face_owners, value in core.ordered_tensor(opposite, types).items():
            owners = [None] * 4
            owners[part] = owner
            for index, other_part in enumerate(opposite):
                owners[other_part] = face_owners[index]
            owners = tuple(owners)
            if not core.tetra_allowed(types, owners):
                candidate = None
                break
            candidate[owners] = value
        if candidate is not None and core.boundary_of_fill(candidate) == cycle:
            return part, owner, candidate
    return None


def localized_fill(types, cycle):
    supports = tuple(tuple(owner for owner in range(13) if core.MASKS[value] & (1 << owner)) for value in types)
    pair_deleted = {
        (left, right): core.ORIGINAL.get(tuple(sorted((types[left], types[right]))), 0)
        for left, right in itertools.combinations(range(4), 2)
    }
    triple_deleted = {
        parts: core.RANK3.get(tuple(sorted(types[part] for part in parts)), 0)
        for parts in itertools.combinations(range(4), 3)
    }
    _cells, all_cells = build_complex(supports, pair_deleted, triple_deleted)
    simplicial_cycle = {
        tuple((part, owner) for part, owner in zip(parts, owners)): value
        for (parts, owners), value in cycle.items()
    }
    solved = direct_boundary_solve(all_cells, simplicial_cycle)
    if solved["status"] != "BOUNDARY":
        return solved
    fill = {tuple(owner for _part, owner in tetrahedron): value for tetrahedron, value in solved["witness"].items()}
    if core.boundary_of_fill(fill) != cycle:
        raise AssertionError("localized fill replay")
    return {**solved, "fill": fill}


def serialize_chain(chain):
    return [[list(cell), value.numerator, value.denominator] for cell, value in sorted(chain.items())]


def main():
    started = time.monotonic()
    selection = json.loads((OUT / "selection.json").read_text())
    selected = [tuple(row["types"]) for row in selection["selected"]]
    face_rows, pair_classes = initialize(selected)
    records = []
    routes = defaultdict(int)
    maximum_fill = maximum_bits = 0
    for ordinal, types in enumerate(selected):
        cycle = moment_cycle(types)
        cone = cone_fill(types, cycle)
        if cone is not None:
            part, owner, fill = cone
            route = "EXPLICIT_CONE"
            detail = {"cone_part": part, "cone_owner": owner}
        else:
            outcome = localized_fill(types, cycle)
            if outcome["status"] != "BOUNDARY":
                raise RuntimeError(f"canonical section fails locally at {ordinal}")
            fill = outcome["fill"]
            route = outcome["route"]
            detail = {"solve_radius": outcome["radius"], "solve_triangles": outcome["local_triangles"], "solve_tetrahedra": outcome["local_tetrahedra"]}
        if core.boundary_of_fill(fill) != cycle:
            raise AssertionError("fill replay")
        routes[route] += 1
        maximum_fill = max(maximum_fill, len(fill))
        for value in itertools.chain((value for _key, value in cycle.items()), (value for _key, value in fill.items())):
            maximum_bits = max(maximum_bits, abs(value.numerator).bit_length(), value.denominator.bit_length())
        records.append({
            "ordinal": ordinal, "types": list(types), "status": "FILLED", "route": route,
            "cycle": [[[list(parts), list(owners)], value.numerator, value.denominator] for (parts, owners), value in sorted(cycle.items())],
            "fill": serialize_chain(fill), **detail,
        })
    serialized_faces = [
        {"triple": list(row["triple"]), "allowed_cells": row["allowed_cells"], "rank": row["rank"], "route": row["route"],
         "coefficients": serialize_chain(row["coefficients"])}
        for row in face_rows
    ]
    result = {
        "status": "PASS", "epistemic_status": "PROVED", "stage": "CANONICAL_GLOBAL_AFFINE_SECTION",
        "selected_quadruples": len(selected), "face_classes": len(face_rows), "pair_classes": len(pair_classes),
        "incidence": selection["incidence"], "local_stalks_nonempty": len(records), "global_section": True,
        "section_route": "OUTCOME_INDEPENDENT_CANONICAL_TRIPLE_FACE_RULE",
        "face_routes": dict(sorted(Counter(row["route"] for row in face_rows).items())),
        "fill_routes": dict(sorted(routes.items())), "maximum_fill_nonzero": maximum_fill,
        "maximum_coefficient_bits": maximum_bits, "face_tensors": serialized_faces, "records": records,
        "claim_boundary": "Exact global rational section on the frozen 256-quadruple connected patch only; not a universal descent theorem, leaf certificate, or LRC(13).",
        "wall_seconds": time.monotonic() - started,
    }
    target = OUT / "canonical-section-localized.json"
    temporary = target.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(target)
    print(json.dumps({key: result[key] for key in ("status", "selected_quadruples", "face_classes", "pair_classes", "local_stalks_nonempty", "global_section", "face_routes", "fill_routes", "maximum_fill_nonzero", "maximum_coefficient_bits", "wall_seconds")}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
