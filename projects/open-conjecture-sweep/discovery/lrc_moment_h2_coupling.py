#!/usr/bin/env python3
"""Cycle 43 canonical moment-H2 coupling on all Cycle 42 interfaces."""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
import itertools
import json
import math
import multiprocessing
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_ownership_functional as c38
import lrc_signed_ownership_moments as c40
from lrc_multiplied_fill_probe import oriented_relation_transport

OUT = ROOT / "discovery/out/cycle43-moment-h2-coupling"
ANCHORS = ((2, 5, 14), (14, 68, 71), (80, 1306, 1307))
MASKS = []
ORIGINAL = {}
RELATION_DELETED = {}
TRANSPORT_MASKS = []
MARGINALS = []
PAIR_FLOWS = {}
FACE_TENSORS = {}


def coordinate(index):
    resource.setrlimit(resource.RLIMIT_AS, (1_600_000_000, 1_600_000_000))
    return c40.coordinate_classes(index)


def sparse_solve(rows, rhs, variables, track_relation=False):
    basis = {}
    for source, (raw, raw_rhs) in enumerate(zip(rows, rhs)):
        row = {index: Fraction(value) for index, value in raw.items() if value}
        value = Fraction(raw_rhs)
        relation = {source: Fraction(1)} if track_relation else None
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
            base, base_rhs, base_relation = basis[pivot]
            factor = row[pivot]
            for index, coefficient in base.items():
                row[index] = row.get(index, Fraction(0)) - factor * coefficient
                if not row[index]:
                    del row[index]
            value -= factor * base_rhs
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
    return {"status": "CONSISTENT", "rank": len(basis), "solution": solution}


def canonical_face(triple):
    resource.setrlimit(resource.RLIMIT_AS, (2_000_000_000, 2_000_000_000))
    triple = tuple(triple)
    supports = [tuple(owner for owner in range(13) if MASKS[value] & (1 << owner)) for value in triple]
    cells = []
    for owners in itertools.product(*supports):
        if any(owners[x] == owners[y] and ORIGINAL.get(tuple(sorted((triple[x], triple[y]))), 0) & (1 << owners[x]) for x, y in itertools.combinations(range(3), 2)):
            continue
        cells.append(owners)
    pair_rows = []
    rhs = []
    for x, y in itertools.combinations(range(3), 2):
        flow = PAIR_FLOWS[(triple[x], triple[y])]
        diagonal = ORIGINAL.get(tuple(sorted((triple[x], triple[y]))), 0)
        for i in supports[x]:
            for j in supports[y]:
                if i == j and diagonal & (1 << i):
                    continue
                pair_rows.append((x, y, i, j))
                rhs.append(flow.get((i, j), Fraction(0)))
    row_id = {key: index for index, key in enumerate(pair_rows)}
    equations = [dict() for _ in pair_rows]
    for column, owners in enumerate(cells):
        for x, y in itertools.combinations(range(3), 2):
            equations[row_id[(x, y, owners[x], owners[y])]][column] = 1
    solved = sparse_solve(equations, rhs, len(cells))
    if solved["status"] != "CONSISTENT":
        raise AssertionError(f"Cycle 41 face failure {triple}")
    coefficients = {cells[index]: value for index, value in enumerate(solved["solution"]) if value}
    stabilizer = [permutation for permutation in itertools.permutations(range(3)) if tuple(triple[permutation[index]] for index in range(3)) == triple]
    symmetric = defaultdict(Fraction)
    for owners, value in coefficients.items():
        for permutation in stabilizer:
            symmetric[tuple(owners[permutation[index]] for index in range(3))] += value / len(stabilizer)
    symmetric = {owners: value for owners, value in symmetric.items() if value}
    # Exact post-symmetrization marginal check.
    for x, y in itertools.combinations(range(3), 2):
        observed = defaultdict(Fraction)
        for owners, value in symmetric.items():
            observed[(owners[x], owners[y])] += value
        expected = PAIR_FLOWS[(triple[x], triple[y])]
        if {key: value for key, value in observed.items() if value} != expected:
            raise AssertionError(f"symmetric face marginal {triple} {(x, y)}")
    bits = max((max(abs(value.numerator).bit_length(), value.denominator.bit_length()) for value in symmetric.values()), default=1)
    return {"triple": triple, "cells": len(cells), "rank": solved["rank"], "coefficients": symmetric, "nonzero": len(symmetric), "bits": bits}


def structural_key(types):
    return (
        tuple(MASKS[value] for value in types),
        tuple(ORIGINAL.get(tuple(sorted((types[a], types[b]))), 0) for a, b in itertools.combinations(range(4), 2)),
    )


def build_complex(types):
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
    face_triangle_ids = {}
    for parts in itertools.combinations(range(4), 3):
        ids = []
        for owners in itertools.product(*(supports[p] for p in parts)):
            vertices = tuple(zip(parts, owners))
            candidates = tuple((vertices[x], vertices[y]) for x, y in itertools.combinations(range(3), 2))
            if not all(edge in edge_id for edge in candidates):
                continue
            ids.append(len(triangles))
            triangles.append(vertices)
            d2.append({edge_id[candidates[2]]: Fraction(1), edge_id[candidates[1]]: Fraction(-1), edge_id[candidates[0]]: Fraction(1)})
        face_triangle_ids[parts] = ids
    triangle_id = {face: index for index, face in enumerate(triangles)}
    tetrahedra = []
    d3 = []
    for owners in itertools.product(*supports):
        faces = [tuple((part, owners[part]) for part in range(4) if part != omitted) for omitted in range(4)]
        if all(face in triangle_id for face in faces):
            tetrahedra.append(owners)
            d3.append({triangle_id[face]: Fraction((-1) ** omitted) for omitted, face in enumerate(faces)})
    basis = {}
    for column_index, raw in enumerate(d3):
        row = dict(raw)
        combination = {column_index: Fraction(1)}
        while row:
            pivot = min(row)
            if pivot not in basis:
                scale = row[pivot]
                row = {index: value / scale for index, value in row.items()}
                combination = {index: value / scale for index, value in combination.items()}
                basis[pivot] = (row, combination)
                break
            base, base_combination = basis[pivot]
            factor = row[pivot]
            for index, value in base.items():
                row[index] = row.get(index, Fraction(0)) - factor * value
                if not row[index]:
                    del row[index]
            for index, value in base_combination.items():
                combination[index] = combination.get(index, Fraction(0)) - factor * value
                if not combination[index]:
                    del combination[index]
    return {"supports": supports, "edges": edges, "triangles": triangles, "d2": d2, "tetrahedra": tetrahedra, "d3": d3, "basis": basis, "face_triangle_ids": face_triangle_ids}


def oriented_face_coefficients(parts, ordered_types):
    sorted_types = tuple(sorted(ordered_types))
    tensor = FACE_TENSORS[sorted_types]["coefficients"]
    permutation = next(permutation for permutation in itertools.permutations(range(3)) if tuple(sorted_types[permutation[index]] for index in range(3)) == ordered_types)
    return {tuple(owners[permutation[index]] for index in range(3)): value for owners, value in tensor.items()}


def test_group(job):
    resource.setrlimit(resource.RLIMIT_AS, (2_400_000_000, 2_400_000_000))
    _key, raw_interfaces = job
    representative = raw_interfaces[0]
    complex_data = build_complex(tuple(representative["types"]))
    triangle_id = {face: index for index, face in enumerate(complex_data["triangles"])}
    failures = []
    records = []
    fill_count = max_fill_nonzero = max_bits = 0
    first_fill = None
    for raw in raw_interfaces:
        types = tuple(raw["types"])
        cycle = defaultdict(Fraction)
        for omitted in range(4):
            parts = tuple(part for part in range(4) if part != omitted)
            ordered_types = tuple(types[part] for part in parts)
            tensor = oriented_face_coefficients(parts, ordered_types)
            sign = Fraction((-1) ** omitted)
            for owners, value in tensor.items():
                face = tuple(zip(parts, owners))
                if face not in triangle_id:
                    raise AssertionError(f"face support {types} {face}")
                cycle[triangle_id[face]] += sign * value
        cycle = {index: value for index, value in cycle.items() if value}
        boundary = defaultdict(Fraction)
        for triangle, coefficient in cycle.items():
            for edge, value in complex_data["d2"][triangle].items():
                boundary[edge] += coefficient * value
        if any(boundary.values()):
            raise AssertionError(f"moment boundary {types}")
        residual = dict(cycle)
        fill = defaultdict(Fraction)
        while residual:
            pivot = min(residual)
            if pivot not in complex_data["basis"]:
                break
            base, combination = complex_data["basis"][pivot]
            factor = residual[pivot]
            for index, value in base.items():
                residual[index] = residual.get(index, Fraction(0)) - factor * value
                if not residual[index]:
                    del residual[index]
            for index, value in combination.items():
                fill[index] += factor * value
                if not fill[index]:
                    del fill[index]
        if residual:
            # Produce an exact dual certificate only for failures.
            rows = [dict() for _ in complex_data["triangles"]]
            for column, values in enumerate(complex_data["d3"]):
                for row, value in values.items():
                    rows[row][column] = value
            rhs = [cycle.get(index, Fraction(0)) for index in range(len(rows))]
            tested = sparse_solve(rows, rhs, len(complex_data["tetrahedra"]), track_relation=True)
            if tested["status"] != "INCONSISTENT":
                raise AssertionError("residual/certificate disagreement")
            relation = tested["relation"]
            pairing = sum(relation[index] * rhs[index] for index in relation)
            if not pairing or pairing != tested["pairing"]:
                raise AssertionError("dual pairing")
            failures.append({"anchor_index": raw["anchor_index"], "fourth_type": raw["fourth_type"], "types": list(types), "cycle": [[index, value.numerator, value.denominator] for index, value in sorted(cycle.items())], "dual_cochain": [[index, value.numerator, value.denominator] for index, value in sorted(relation.items())], "pairing": [pairing.numerator, pairing.denominator]})
            records.append({"anchor_index": raw["anchor_index"], "fourth_type": raw["fourth_type"], "types": list(types), "status": "NONBOUNDARY", "cycle": [[index, value.numerator, value.denominator] for index, value in sorted(cycle.items())], "dual_cochain": [[index, value.numerator, value.denominator] for index, value in sorted(relation.items())], "pairing": [pairing.numerator, pairing.denominator]})
        else:
            replay = defaultdict(Fraction)
            for tetrahedron, coefficient in fill.items():
                for triangle, value in complex_data["d3"][tetrahedron].items():
                    replay[triangle] += coefficient * value
            if {index: value for index, value in replay.items() if value} != cycle:
                raise AssertionError("tetrahedral fill replay")
            fill_count += 1
            max_fill_nonzero = max(max_fill_nonzero, len(fill))
            for value in fill.values():
                max_bits = max(max_bits, abs(value.numerator).bit_length(), value.denominator.bit_length())
            if first_fill is None:
                first_fill = {"types": list(types), "cycle_nonzero": len(cycle), "fill": [[index, value.numerator, value.denominator] for index, value in sorted(fill.items())]}
            records.append({"anchor_index": raw["anchor_index"], "fourth_type": raw["fourth_type"], "types": list(types), "status": "FILLED", "cycle": [[index, value.numerator, value.denominator] for index, value in sorted(cycle.items())], "fill": [[index, value.numerator, value.denominator] for index, value in sorted(fill.items())]})
    return {"raw_interfaces": len(raw_interfaces), "fills": fill_count, "failures": failures, "records": records, "first_fill": first_fill, "maximum_fill_nonzero": max_fill_nonzero, "maximum_fill_bits": max_bits, "triangles": len(complex_data["triangles"]), "tetrahedra": len(complex_data["tetrahedra"])}


def main():
    global MASKS, ORIGINAL, RELATION_DELETED, TRANSPORT_MASKS, MARGINALS, PAIR_FLOWS, FACE_TENSORS
    started = time.monotonic()
    OUT.mkdir(parents=True, exist_ok=True)
    c38.prepare()
    types = sorted({row[0] for root in c38._TYPE_ROWS for rows in root.values() for row in rows})
    c40._TYPE_ID = {value: index for index, value in enumerate(types)}
    MASKS = [sum(1 << owner for owner, signature in enumerate(value) if signature) for value in types]
    c40._TYPE_MASKS = MASKS
    with multiprocessing.Pool(3) as pool:
        rows = pool.map(coordinate, range(13), chunksize=1)
    original = defaultdict(int)
    induced = defaultdict(int)
    for owner, row in enumerate(rows):
        for pair in row["rank_two_pairs"]:
            original[tuple(pair)] |= 1 << owner
        for pair in row["induced_pair_deletions"]:
            induced[tuple(pair)] |= 1 << owner
    ORIGINAL = dict(original)
    binary_types = {index for index, mask in enumerate(MASKS) if mask.bit_count() <= 2}
    blocked = defaultdict(list)
    for (left, right), owner_mask in ORIGINAL.items():
        for owner in range(13):
            if owner_mask & (1 << owner):
                if left in binary_types:
                    blocked[(left, owner)].append(right)
                if right in binary_types:
                    blocked[(right, owner)].append(left)
    TRANSPORT_MASKS = list(MASKS)
    for mediator in binary_types:
        owners = [owner for owner in range(13) if MASKS[mediator] & (1 << owner)]
        if len(owners) == 1:
            for neighbor in blocked[(mediator, owners[0])]:
                TRANSPORT_MASKS[neighbor] &= ~(1 << owners[0])
    relation_deleted = defaultdict(int)
    for pair in set(ORIGINAL) | set(induced):
        for owner in range(13):
            if (ORIGINAL.get(pair, 0) | induced.get(pair, 0)) & (1 << owner):
                relation_deleted[pair] |= 1 << (13 * owner + owner)
    for mediator in binary_types:
        owners = [owner for owner in range(13) if MASKS[mediator] & (1 << owner)]
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
    RELATION_DELETED = dict(relation_deleted)
    prior = json.loads((ROOT / "discovery/out/cycle41-multiplied-ideal/zero-support-closure.json").read_text(encoding="utf-8"))
    MARGINALS = [{int(owner): Fraction(int(numerator), int(denominator)) for owner, numerator, denominator in values} for values in prior["singleton_marginals_by_complete_type"]]

    raw_interfaces = [{"anchor_index": anchor_index, "fourth_type": fourth, "types": list(anchor + (fourth,))} for anchor_index, anchor in enumerate(ANCHORS) for fourth in range(len(types))]
    face_classes = sorted({tuple(sorted(row["types"][part] for part in range(4) if part != omitted)) for row in raw_interfaces for omitted in range(4)})
    pair_classes = sorted({(triple[x], triple[y]) for triple in face_classes for x, y in itertools.combinations(range(3), 2)})
    PAIR_FLOWS = {pair: oriented_relation_transport(pair[0], pair[1], RELATION_DELETED, MARGINALS, TRANSPORT_MASKS) for pair in pair_classes}
    with multiprocessing.Pool(3) as pool:
        face_rows = pool.map(canonical_face, face_classes, chunksize=4)
    FACE_TENSORS = {row["triple"]: row for row in face_rows}

    groups = defaultdict(list)
    for row in raw_interfaces:
        groups[structural_key(tuple(row["types"]))].append(row)
    jobs = list(groups.items())
    with multiprocessing.Pool(3) as pool:
        group_rows = pool.map(test_group, jobs, chunksize=1)
    failures = [failure for row in group_rows for failure in row["failures"]]
    canonical_fills = sum(row["fills"] for row in group_rows)
    aggregate_face_cells = sum(row["cells"] for row in face_rows)
    aggregate_tetrahedra = sum(row["tetrahedra"] * row["raw_interfaces"] for row in group_rows)
    if len(raw_interfaces) != 3954 or len(groups) != 409:
        raise AssertionError("Cycle 42 interface reconstruction")
    if aggregate_face_cells > 100_000_000 or aggregate_tetrahedra > 500_000_000:
        raise RuntimeError("cell cap")
    if time.monotonic() - started > 3600:
        raise RuntimeError("wall cap")
    serialized_faces = [{"triple": list(row["triple"]), "allowed_cells": row["cells"], "rank": row["rank"], "coefficients": [[list(owners), value.numerator, value.denominator] for owners, value in sorted(row["coefficients"].items())]} for row in face_rows]
    interface_records = sorted((record for row in group_rows for record in row["records"]), key=lambda record: (record["anchor_index"], record["fourth_type"]))
    result = {"status": "PASS", "epistemic_status": "PROVED", "stage": "CANONICAL_SELECTED_MOMENT_COUPLING", "raw_interfaces": len(raw_interfaces), "structural_complexes": len(groups), "unordered_face_classes": len(face_classes), "oriented_pair_classes": len(pair_classes), "canonical_face_cells": aggregate_face_cells, "canonical_face_nonzero": sum(row["nonzero"] for row in face_rows), "maximum_face_bits": max(row["bits"] for row in face_rows), "canonical_fills": canonical_fills, "canonical_failures": len(failures), "first_failure": failures[0] if failures else None, "first_fill": next(row["first_fill"] for row in group_rows if row["first_fill"] is not None), "maximum_fill_nonzero": max(row["maximum_fill_nonzero"] for row in group_rows), "maximum_fill_bits": max(row["maximum_fill_bits"] for row in group_rows), "aggregate_tetrahedra_raw": aggregate_tetrahedra, "coherent_escalation_required": bool(failures), "face_tensors": serialized_faces, "interface_records": interface_records, "claim_boundary": "Exact canonical repeated-type-symmetric Cycle 41 moment coupling on the 3,954 Cycle 42 selected interfaces. Canonical failure is not coherent infeasibility; canonical filling is not a full degree-four functional.", "wall_seconds": time.monotonic() - started}
    temporary = OUT / "canonical-coupling.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "canonical-coupling.json")
    print(json.dumps({key: result[key] for key in ("status", "raw_interfaces", "structural_complexes", "unordered_face_classes", "oriented_pair_classes", "canonical_face_cells", "canonical_fills", "canonical_failures", "first_failure", "maximum_fill_nonzero", "maximum_fill_bits", "wall_seconds")}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
