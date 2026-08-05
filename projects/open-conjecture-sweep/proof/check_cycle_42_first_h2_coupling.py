#!/usr/bin/env python3
"""Exact rational H2 and Cycle 41 moment coupling on Cycle 42's first interface."""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
import itertools
import json
import math
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_ownership_functional as c38
from lrc_multiplied_fill_probe import oriented_relation_transport

OUT = ROOT / "discovery/out/cycle42-h2-horn"
TYPES = (2, 5, 14, 5)


def sparse_solve(rows, rhs, variables, track_relations=False):
    basis = {}
    for source, (raw, value) in enumerate(zip(rows, rhs)):
        row = {index: Fraction(coefficient) for index, coefficient in raw.items() if coefficient}
        value = Fraction(value)
        relation = {source: Fraction(1)} if track_relations else None
        while row:
            pivot = min(row)
            if pivot not in basis:
                scale = row[pivot]
                row = {index: coefficient / scale for index, coefficient in row.items()}
                value /= scale
                if relation is not None:
                    relation = {index: coefficient / scale for index, coefficient in relation.items()}
                basis[pivot] = (row, value, relation)
                break
            base_row, base_value, base_relation = basis[pivot]
            factor = row[pivot]
            for index, coefficient in base_row.items():
                row[index] = row.get(index, Fraction(0)) - factor * coefficient
                if not row[index]:
                    del row[index]
            value -= factor * base_value
            if relation is not None:
                for index, coefficient in base_relation.items():
                    relation[index] = relation.get(index, Fraction(0)) - factor * coefficient
                    if not relation[index]:
                        del relation[index]
        else:
            if value:
                return {"status": "INCONSISTENT", "rank": len(basis), "relation": relation, "pairing": value}
    solution = [Fraction(0)] * variables
    for pivot in sorted(basis, reverse=True):
        row, value, _relation = basis[pivot]
        solution[pivot] = value - sum(coefficient * solution[index] for index, coefficient in row.items() if index != pivot)
    for row, value in zip(rows, rhs):
        if sum(Fraction(coefficient) * solution[index] for index, coefficient in row.items()) != value:
            raise AssertionError("solution replay")
    return {"status": "CONSISTENT", "rank": len(basis), "solution": solution, "basis": basis}


def primitive(values):
    denominator = math.lcm(*(value.denominator for value in values))
    integers = [value.numerator * (denominator // value.denominator) for value in values]
    divisor = math.gcd(*(abs(value) for value in integers))
    integers = [value // divisor for value in integers]
    first = next(value for value in integers if value)
    if first < 0:
        integers = [-value for value in integers]
    return integers


def main():
    started = time.monotonic()
    c38.prepare()
    complete_types = sorted({row[0] for root in c38._TYPE_ROWS for rows in root.values() for row in rows})
    type_id = {value: index for index, value in enumerate(complete_types)}
    masks = [sum(1 << owner for owner, signature in enumerate(value) if signature) for value in complete_types]
    signatures = [[set() for _ in complete_types] for _ in range(13)]
    for owner in range(13):
        for signature, rows in c38._TYPE_ROWS[owner].items():
            for row in rows:
                signatures[owner][type_id[row[0]]].add(int(signature))

    pattern_cache = {}
    def blocked(type_tuple, owner):
        key = (tuple(sorted(type_tuple)), owner)
        if key in pattern_cache:
            return pattern_cache[key]
        rank = len(type_tuple)
        answer = False
        for pattern in c38._COORDINATES[owner]["patterns"]:
            if int(pattern["rank"]) != rank:
                continue
            target = tuple(int(value) for value in pattern["signatures"])
            for ordering in set(itertools.permutations(type_tuple)):
                if all(target[index] in signatures[owner][ordering[index]] for index in range(rank)):
                    answer = True
                    break
            if answer:
                break
        pattern_cache[key] = answer
        return answer

    def deletion(type_tuple):
        return sum(1 << owner for owner in range(13) if blocked(type_tuple, owner))

    singleton = [index for index, mask in enumerate(masks) if mask.bit_count() == 1]
    binary = [index for index, mask in enumerate(masks) if mask.bit_count() == 2]
    involved = sorted(set(TYPES))
    transport_masks = list(masks)
    for value in involved:
        for mediator in singleton:
            owner = masks[mediator].bit_length() - 1
            if blocked((mediator, value), owner):
                transport_masks[value] &= ~(1 << owner)
    relation_deleted = defaultdict(int)
    for left, right in set(itertools.combinations_with_replacement(involved, 2)):
        pair = tuple(sorted((left, right)))
        diagonal = deletion(pair)
        cells = 0
        for owner in range(13):
            if diagonal & (1 << owner):
                cells |= 1 << (13 * owner + owner)
        relation_deleted[pair] = cells
        for mediator in singleton:
            owner = masks[mediator].bit_length() - 1
            if blocked((mediator, left, right), owner):
                relation_deleted[pair] |= 1 << (13 * owner + owner)
        for mediator in binary:
            a, b = [owner for owner in range(13) if masks[mediator] & (1 << owner)]
            for x, y in ((a, b), (b, a)):
                if blocked((mediator, left), x) and blocked((mediator, right), y):
                    relation_deleted[pair] |= 1 << (13 * x + y)

    prior = json.loads((ROOT / "discovery/out/cycle41-multiplied-ideal/zero-support-closure.json").read_text(encoding="utf-8"))
    marginals = [
        {int(owner): Fraction(int(numerator), int(denominator)) for owner, numerator, denominator in values}
        for values in prior["singleton_marginals_by_complete_type"]
    ]

    supports = [tuple(owner for owner in range(13) if masks[value] & (1 << owner)) for value in TYPES]
    edges = []
    for a, b in itertools.combinations(range(4), 2):
        deleted = deletion((TYPES[a], TYPES[b]))
        for i in supports[a]:
            for j in supports[b]:
                if not (i == j and deleted & (1 << i)):
                    edges.append(((a, i), (b, j)))
    edge_id = {edge: index for index, edge in enumerate(edges)}
    triangles = []
    triangle_d2 = []
    face_cells = {}
    for parts in itertools.combinations(range(4), 3):
        deleted3 = deletion(tuple(TYPES[p] for p in parts))
        cells = []
        for owners in itertools.product(*(supports[p] for p in parts)):
            if owners[0] == owners[1] == owners[2] and deleted3 & (1 << owners[0]):
                continue
            vertices = tuple(zip(parts, owners))
            boundary_edges = []
            ok = True
            for x, y in itertools.combinations(range(3), 2):
                edge = (vertices[x], vertices[y])
                if edge not in edge_id:
                    ok = False
                    break
                boundary_edges.append(edge)
            if not ok:
                continue
            row = {
                edge_id[boundary_edges[2]]: 1,
                edge_id[boundary_edges[1]]: -1,
                edge_id[boundary_edges[0]]: 1,
            }
            cells.append(len(triangles))
            triangles.append(vertices)
            triangle_d2.append(row)
        face_cells[parts] = cells
    triangle_id = {face: index for index, face in enumerate(triangles)}
    tetrahedra = []
    tetra_d3 = []
    for owners in itertools.product(*supports):
        faces = [tuple((part, owners[part]) for part in range(4) if part != omitted) for omitted in range(4)]
        if not all(face in triangle_id for face in faces):
            continue
        tetrahedra.append(owners)
        tetra_d3.append({triangle_id[face]: (-1) ** omitted for omitted, face in enumerate(faces)})

    # Convert column boundaries to row equations.
    d2_rows = [dict() for _ in edges]
    for triangle_index, boundary in enumerate(triangle_d2):
        for edge_index, coefficient in boundary.items():
            d2_rows[edge_index][triangle_index] = coefficient
    d3_rows = [dict() for _ in triangles]
    for tetra_index, boundary in enumerate(tetra_d3):
        for triangle_index, coefficient in boundary.items():
            d3_rows[triangle_index][tetra_index] = coefficient
    for tetra_index, boundary in enumerate(tetra_d3):
        composed = defaultdict(Fraction)
        for triangle_index, coefficient in boundary.items():
            for edge_index, entry in triangle_d2[triangle_index].items():
                composed[edge_index] += coefficient * entry
        if any(composed.values()):
            raise AssertionError("rational boundary squared")

    # Canonical kernel basis of d2, followed by the first class outside im d3.
    zero = [Fraction(0)] * len(d2_rows)
    d2_solved = sparse_solve(d2_rows, zero, len(triangles))
    pivot_columns = set(d2_solved["basis"])
    kernel = []
    for free in range(len(triangles)):
        if free in pivot_columns:
            continue
        vector = [Fraction(0)] * len(triangles)
        vector[free] = 1
        for pivot in sorted(d2_solved["basis"], reverse=True):
            row, _rhs, _relation = d2_solved["basis"][pivot]
            vector[pivot] = -sum(coefficient * vector[index] for index, coefficient in row.items() if index != pivot)
        kernel.append(vector)
    image_columns = []
    for tetra_index in range(len(tetrahedra)):
        image_columns.append([Fraction(d3_rows[row].get(tetra_index, 0)) for row in range(len(triangles))])
    image_basis = {}
    def reduce_vector(vector, add=False):
        value = {i: x for i, x in enumerate(vector) if x}
        while value:
            pivot = min(value)
            if pivot not in image_basis:
                if add:
                    scale = value[pivot]
                    image_basis[pivot] = {i: x / scale for i, x in value.items()}
                return value
            factor = value[pivot]
            for index, coefficient in image_basis[pivot].items():
                value[index] = value.get(index, Fraction(0)) - factor * coefficient
                if not value[index]:
                    del value[index]
        return value
    for column in image_columns:
        reduce_vector(column, add=True)
    canonical_cycle = None
    for vector in kernel:
        if reduce_vector(vector):
            canonical_cycle = vector
            break
    if canonical_cycle is None:
        raise AssertionError("expected rational H2")
    canonical_test = sparse_solve(d3_rows, canonical_cycle, len(tetrahedra), track_relations=True)
    if canonical_test["status"] != "INCONSISTENT":
        raise AssertionError("canonical class filled")

    # Rebuild one canonical, repeated-type-symmetric Cycle 41 tensor per
    # unordered face, then transport it to each oriented face.
    type_pair_flows = {}
    def type_pair_flow(left, right):
        key = (left, right)
        if key not in type_pair_flows:
            type_pair_flows[key] = oriented_relation_transport(left, right, relation_deleted, marginals, transport_masks)
        return type_pair_flows[key]

    pair_flows = {}
    for a, b in itertools.combinations(range(4), 2):
        pair_flows[(a, b)] = type_pair_flow(TYPES[a], TYPES[b])
    canonical_faces = {}

    def canonical_face(type_tuple):
        sorted_types = tuple(sorted(type_tuple))
        if sorted_types in canonical_faces:
            return canonical_faces[sorted_types]
        local_supports = [tuple(owner for owner in range(13) if masks[value] & (1 << owner)) for value in sorted_types]
        local_cells = []
        deleted3 = deletion(sorted_types)
        for owners in itertools.product(*local_supports):
            if owners[0] == owners[1] == owners[2] and deleted3 & (1 << owners[0]):
                continue
            if any(owners[x] == owners[y] and deletion((sorted_types[x], sorted_types[y])) & (1 << owners[x]) for x, y in itertools.combinations(range(3), 2)):
                continue
            local_cells.append(owners)
        pair_rows = []
        rhs = []
        for x, y in itertools.combinations(range(3), 2):
            flow = type_pair_flow(sorted_types[x], sorted_types[y])
            for i in local_supports[x]:
                for j in local_supports[y]:
                    if i == j and deletion((sorted_types[x], sorted_types[y])) & (1 << i):
                        continue
                    pair_rows.append((x, y, i, j))
                    rhs.append(flow.get((i, j), Fraction(0)))
        row_id = {key: index for index, key in enumerate(pair_rows)}
        equations = [dict() for _ in pair_rows]
        for column, owners in enumerate(local_cells):
            for x, y in itertools.combinations(range(3), 2):
                equations[row_id[(x, y, owners[x], owners[y])]][column] = 1
        filled = sparse_solve(equations, rhs, len(local_cells))
        if filled["status"] != "CONSISTENT":
            raise AssertionError("canonical Cycle 41 face failed")
        coefficients = {local_cells[index]: value for index, value in enumerate(filled["solution"]) if value}
        stabilizer = [permutation for permutation in itertools.permutations(range(3)) if tuple(sorted_types[permutation[index]] for index in range(3)) == sorted_types]
        symmetric = defaultdict(Fraction)
        for owners, value in coefficients.items():
            for permutation in stabilizer:
                symmetric[tuple(owners[permutation[index]] for index in range(3))] += value / len(stabilizer)
        symmetric = {owners: value for owners, value in symmetric.items() if value}
        canonical_faces[sorted_types] = (symmetric, filled["rank"], len(local_cells))
        return canonical_faces[sorted_types]

    moment_cycle = [Fraction(0)] * len(triangles)
    face_summaries = []
    for omitted in range(4):
        parts = tuple(part for part in range(4) if part != omitted)
        cells = face_cells[parts]
        ordered_types = tuple(TYPES[part] for part in parts)
        sorted_types = tuple(sorted(ordered_types))
        coefficients, fill_rank, local_cell_count = canonical_face(ordered_types)
        permutation = next(permutation for permutation in itertools.permutations(range(3)) if tuple(sorted_types[permutation[index]] for index in range(3)) == ordered_types)
        ordered_coefficients = {tuple(owners[permutation[index]] for index in range(3)): value for owners, value in coefficients.items()}
        global_coefficients = {}
        for triangle_index in cells:
            owners = tuple(owner for _part, owner in triangles[triangle_index])
            value = ordered_coefficients.get(owners, Fraction(0))
            if value:
                global_coefficients[triangle_index] = value
        sign = Fraction((-1) ** omitted)
        for triangle_index, value in global_coefficients.items():
            moment_cycle[triangle_index] += sign * value
        face_summaries.append({"omitted_part": omitted, "triangles": len(cells), "canonical_cells": local_cell_count, "rank": fill_rank, "nonzero_coefficients": len(global_coefficients), "fill": [[index, value.numerator, value.denominator] for index, value in sorted(global_coefficients.items())]})
    boundary = [sum(coefficient * moment_cycle[index] for index, coefficient in row.items()) for row in d2_rows]
    if any(boundary):
        raise AssertionError("moment boundary")
    moment_test = sparse_solve(d3_rows, moment_cycle, len(tetrahedra), track_relations=True)

    canonical_relation = canonical_test["relation"]
    canonical_pairing = sum(canonical_relation[index] * canonical_cycle[index] for index in canonical_relation)
    if canonical_pairing != canonical_test["pairing"] or not canonical_pairing:
        raise AssertionError("canonical cochain")
    moment_pairing = None
    moment_relation = None
    if moment_test["status"] == "INCONSISTENT":
        moment_relation = moment_test["relation"]
        moment_pairing = sum(moment_relation[index] * moment_cycle[index] for index in moment_relation)
        if moment_pairing != moment_test["pairing"] or not moment_pairing:
            raise AssertionError("moment cochain")

    payload = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "types": list(TYPES),
        "owner_masks": [masks[value] for value in TYPES],
        "pair_deleted_diagonals": [deletion((TYPES[a], TYPES[b])) for a, b in itertools.combinations(range(4), 2)],
        "rank_three_deleted_diagonals": [deletion(tuple(TYPES[p] for p in parts)) for parts in itertools.combinations(range(4), 3)],
        "complex": {"vertices": sum(map(len, supports)), "edges": len(edges), "triangles": len(triangles), "tetrahedra": len(tetrahedra), "rank_d2_q": d2_solved["rank"], "rank_d3_q": len(image_basis), "h2_q": len(kernel) - len(image_basis)},
        "canonical_class": {"primitive_cycle": [[index, value] for index, value in enumerate(primitive(canonical_cycle)) if value], "dual_cochain": [[index, value.numerator, value.denominator] for index, value in sorted(canonical_relation.items())], "pairing": [canonical_pairing.numerator, canonical_pairing.denominator]},
        "face_fills": face_summaries,
        "pair_flows": {f"{a},{b}": [[i, j, value.numerator, value.denominator] for (i, j), value in sorted(flow.items())] for (a, b), flow in sorted(pair_flows.items())},
        "moment_cycle_nonzero": sum(bool(value) for value in moment_cycle),
        "moment_cycle": [[index, value.numerator, value.denominator] for index, value in enumerate(moment_cycle) if value],
        "moment_filling_status": moment_test["status"],
        "moment_fill": None if moment_test["status"] != "CONSISTENT" else [[index, value.numerator, value.denominator] for index, value in enumerate(moment_test["solution"]) if value],
        "moment_dual_cochain": None if moment_relation is None else [[index, value.numerator, value.denominator] for index, value in sorted(moment_relation.items())],
        "moment_pairing": None if moment_pairing is None else [moment_pairing.numerator, moment_pairing.denominator],
        "claim_boundary": "Exact rational classification of the preregistered first nonzero-GF(2) interface and the deterministic Cycle 41 face-moment cycle only.",
        "wall_seconds": time.monotonic() - started,
    }
    temporary = OUT / "first-rational-coupling.json.tmp"
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "first-rational-coupling.json")
    print(json.dumps({key: payload[key] for key in ("status", "types", "complex", "moment_cycle_nonzero", "moment_filling_status", "moment_pairing", "wall_seconds")}, sort_keys=True))


if __name__ == "__main__":
    main()
