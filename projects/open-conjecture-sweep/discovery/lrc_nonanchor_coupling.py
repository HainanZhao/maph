#!/usr/bin/env python3
"""Cycle 44 exact canonical coupling and explicit cone test on the holdout."""
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
from lrc_multiplied_fill_probe import oriented_relation_transport
from lrc_moment_h2_coupling import sparse_solve

OUT = ROOT / "discovery/out/cycle44-nonanchor-coupling"
MASKS = []
TYPE_ID = {}
TARGET_FACES = set()
ORIGINAL = {}
RANK3 = {}
RELATION_DELETED = {}
TRANSPORT_MASKS = []
MARGINALS = []
PAIR_FLOWS = {}
FACE_TENSORS = {}


def coordinate(index):
    resource.setrlimit(resource.RLIMIT_AS, (1_600_000_000, 1_600_000_000))
    return c40.coordinate_classes(index)


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


def canonical_face(triple):
    resource.setrlimit(resource.RLIMIT_AS, (2_000_000_000, 2_000_000_000))
    triple = tuple(triple)
    supports = [tuple(owner for owner in range(13) if MASKS[value] & (1 << owner)) for value in triple]
    selected = tuple(next(iter(MARGINALS[value])) for value in triple)
    diagonal3 = RANK3.get(triple, 0)

    def allowed(owners):
        if any(owners[x] == owners[y] and ORIGINAL.get(tuple(sorted((triple[x], triple[y]))), 0) & (1 << owners[x]) for x, y in itertools.combinations(range(3), 2)):
            return False
        return not (owners[0] == owners[1] == owners[2] and diagonal3 & (1 << owners[0]))

    delta_pairs = all(PAIR_FLOWS[(triple[x], triple[y])] == {(selected[x], selected[y]): Fraction(1)} for x, y in itertools.combinations(range(3), 2))
    if delta_pairs and allowed(selected):
        symmetric = {selected: Fraction(1)}
        cell_count = sum(allowed(owners) for owners in itertools.product(*supports))
        rank = None
        route = "DELTA_FAST_PATH"
    else:
        cells = [owners for owners in itertools.product(*supports) if allowed(owners)]
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
            raise AssertionError(f"face failure {triple}")
        coefficients = {cells[index]: value for index, value in enumerate(solved["solution"]) if value}
        stabilizer = [permutation for permutation in itertools.permutations(range(3)) if tuple(triple[permutation[index]] for index in range(3)) == triple]
        averaged = defaultdict(Fraction)
        for owners, value in coefficients.items():
            for permutation in stabilizer:
                averaged[tuple(owners[permutation[index]] for index in range(3))] += value / len(stabilizer)
        symmetric = {owners: value for owners, value in averaged.items() if value}
        cell_count = len(cells)
        rank = solved["rank"]
        route = "EXACT_ELIMINATION"
    for x, y in itertools.combinations(range(3), 2):
        observed = defaultdict(Fraction)
        for owners, value in symmetric.items():
            observed[(owners[x], owners[y])] += value
        if {key: value for key, value in observed.items() if value} != PAIR_FLOWS[(triple[x], triple[y])]:
            raise AssertionError("face marginal")
    bits = max((max(abs(value.numerator).bit_length(), value.denominator.bit_length()) for value in symmetric.values()), default=1)
    return {"triple": triple, "allowed_cells": cell_count, "rank": rank, "route": route, "coefficients": symmetric, "bits": bits}


def ordered_tensor(parts, types):
    ordered_types = tuple(types[part] for part in parts)
    sorted_types = tuple(sorted(ordered_types))
    tensor = FACE_TENSORS[sorted_types]["coefficients"]
    permutation = next(permutation for permutation in itertools.permutations(range(3)) if tuple(sorted_types[permutation[index]] for index in range(3)) == ordered_types)
    return {tuple(owners[permutation[index]] for index in range(3)): value for owners, value in tensor.items()}


def tetra_allowed(types, owners):
    for a, b in itertools.combinations(range(4), 2):
        if owners[a] == owners[b] and ORIGINAL.get(tuple(sorted((types[a], types[b]))), 0) & (1 << owners[a]):
            return False
    for parts in itertools.combinations(range(4), 3):
        selected = tuple(owners[part] for part in parts)
        if selected[0] == selected[1] == selected[2] and RANK3.get(tuple(sorted(types[part] for part in parts)), 0) & (1 << selected[0]):
            return False
    return True


def boundary_of_fill(fill):
    boundary = defaultdict(Fraction)
    for owners, coefficient in fill.items():
        for omitted in range(4):
            parts = tuple(part for part in range(4) if part != omitted)
            face_owners = tuple(owners[part] for part in parts)
            boundary[(parts, face_owners)] += Fraction((-1) ** omitted) * coefficient
    return {key: value for key, value in boundary.items() if value}


def exact_fill(types, cycle):
    supports = [tuple(owner for owner in range(13) if MASKS[value] & (1 << owner)) for value in types]
    triangles = sorted(cycle)
    # Include all allowed triangles because a filling may cancel outside cycle support.
    triangle_set = set()
    for parts in itertools.combinations(range(4), 3):
        triple = tuple(sorted(types[part] for part in parts))
        diagonal3 = RANK3.get(triple, 0)
        for owners in itertools.product(*(supports[part] for part in parts)):
            if owners[0] == owners[1] == owners[2] and diagonal3 & (1 << owners[0]):
                continue
            if any(owners[x] == owners[y] and ORIGINAL.get(tuple(sorted((types[parts[x]], types[parts[y]]))), 0) & (1 << owners[x]) for x, y in itertools.combinations(range(3), 2)):
                continue
            triangle_set.add((parts, owners))
    triangles = sorted(triangle_set)
    triangle_id = {face: index for index, face in enumerate(triangles)}
    tetrahedra = [owners for owners in itertools.product(*supports) if tetra_allowed(types, owners)]
    d3 = []
    for owners in tetrahedra:
        d3.append({triangle_id[(tuple(part for part in range(4) if part != omitted), tuple(owners[part] for part in range(4) if part != omitted))]: Fraction((-1) ** omitted) for omitted in range(4)})
    rows = [dict() for _ in triangles]
    for column, values in enumerate(d3):
        for row, value in values.items():
            rows[row][column] = value
    rhs = [cycle.get(face, Fraction(0)) for face in triangles]
    solved = sparse_solve(rows, rhs, len(tetrahedra), track_relation=True)
    if solved["status"] == "CONSISTENT":
        fill = {tetrahedra[index]: value for index, value in enumerate(solved["solution"]) if value}
        if boundary_of_fill(fill) != cycle:
            raise AssertionError("general fill replay")
        return {"status": "FILLED", "fill": fill}
    relation = solved["relation"]
    pairing = sum(relation[index] * rhs[index] for index in relation)
    if not pairing:
        raise AssertionError("zero dual pairing")
    return {"status": "NONBOUNDARY", "dual": {triangles[index]: value for index, value in relation.items()}, "pairing": pairing}


def main():
    global MASKS, TYPE_ID, TARGET_FACES, ORIGINAL, RANK3, RELATION_DELETED, TRANSPORT_MASKS, MARGINALS, PAIR_FLOWS, FACE_TENSORS
    started = time.monotonic()
    c38.prepare()
    complete_types = sorted({row[0] for root in c38._TYPE_ROWS for rows in root.values() for row in rows})
    TYPE_ID = {value: index for index, value in enumerate(complete_types)}
    MASKS = [sum(1 << owner for owner, signature in enumerate(value) if signature) for value in complete_types]
    c40._TYPE_ID = TYPE_ID
    c40._TYPE_MASKS = MASKS
    selection = json.loads((OUT / "selection.json").read_text(encoding="utf-8"))
    selected = [tuple(row["types"]) for row in selection["selected"]]
    TARGET_FACES = {tuple(sorted(types[part] for part in parts)) for types in selected for parts in itertools.combinations(range(4), 3)}
    with multiprocessing.Pool(3) as pool:
        coordinate_rows = pool.map(coordinate, range(13), chunksize=1)
    original = defaultdict(int)
    induced = defaultdict(int)
    for owner, row in enumerate(coordinate_rows):
        for pair in row["rank_two_pairs"]:
            original[tuple(pair)] |= 1 << owner
        for pair in row["induced_pair_deletions"]:
            induced[tuple(pair)] |= 1 << owner
    ORIGINAL = dict(original)
    with multiprocessing.Pool(3) as pool:
        rank3_rows = pool.map(coordinate_rank3, range(13), chunksize=1)
    rank3 = defaultdict(int)
    for owner, raw, triples in rank3_rows:
        for triple in triples:
            rank3[tuple(triple)] |= 1 << owner
    if sum(raw for _owner, raw, _triples in rank3_rows) != 19_661_454:
        raise AssertionError("rank-three census")
    RANK3 = dict(rank3)

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
    if any(values != {next(iter(values)): Fraction(1)} for values in MARGINALS):
        raise AssertionError("non-delta singleton")
    face_classes = sorted(TARGET_FACES)
    pair_classes = sorted({(triple[x], triple[y]) for triple in face_classes for x, y in itertools.combinations(range(3), 2)})
    PAIR_FLOWS = {pair: oriented_relation_transport(pair[0], pair[1], RELATION_DELETED, MARGINALS, TRANSPORT_MASKS) for pair in pair_classes}
    with multiprocessing.Pool(3) as pool:
        face_rows = pool.map(canonical_face, face_classes, chunksize=4)
    FACE_TENSORS = {row["triple"]: row for row in face_rows}

    records = []
    failures = []
    cone_count = elimination_count = h2_zero_existence_count = 0
    maximum_fill = maximum_bits = 0
    for selection_row, types in zip(selection["selected"], selected):
        cycle = defaultdict(Fraction)
        for omitted in range(4):
            parts = tuple(part for part in range(4) if part != omitted)
            tensor = ordered_tensor(parts, types)
            for owners, value in tensor.items():
                cycle[(parts, owners)] += Fraction((-1) ** omitted) * value
        cycle = {key: value for key, value in cycle.items() if value}
        cone = None
        for part in range(4):
            owner = next(iter(MARGINALS[types[part]]))
            opposite = tuple(index for index in range(4) if index != part)
            tensor = ordered_tensor(opposite, types)
            candidate = {}
            for face_owners, value in tensor.items():
                owners = [None] * 4
                owners[part] = owner
                for index, other_part in enumerate(opposite):
                    owners[other_part] = face_owners[index]
                owners = tuple(owners)
                if not tetra_allowed(types, owners):
                    candidate = None
                    break
                candidate[owners] = value
            if candidate is not None and boundary_of_fill(candidate) == cycle:
                cone = {"part": part, "owner": owner, "fill": candidate}
                break
        if cone is not None:
            outcome = {"status": "FILLED", "fill": cone["fill"]}
            cone_count += 1
            route = "EXPLICIT_CONE"
        elif selection_row["h2_gf2"] == 0:
            # Universal coefficients give dim H2(Q) <= dim H2(F_2).
            # Thus GF(2) H2=0 is an exact existence proof for a rational fill;
            # avoid constructing a huge, unnecessary fraction solution.
            outcome = {"status": "FILLED_EXISTENCE", "fill": {}}
            h2_zero_existence_count += 1
            route = "GF2_H2_ZERO_EXISTENCE"
        else:
            outcome = exact_fill(types, cycle)
            route = "EXACT_ELIMINATION"
            if outcome["status"] == "FILLED":
                elimination_count += 1
        record = {"types": list(types), "selection_hash": selection_row["selection_hash"], "h2_gf2": selection_row["h2_gf2"], "h2_bin": selection_row["h2_bin"], "route": route, "cycle": [[[list(parts), list(owners)], value.numerator, value.denominator] for (parts, owners), value in sorted(cycle.items())]}
        if outcome["status"] in ("FILLED", "FILLED_EXISTENCE"):
            fill = outcome["fill"]
            record["status"] = outcome["status"]
            record["fill"] = [[list(owners), value.numerator, value.denominator] for owners, value in sorted(fill.items())]
            if cone is not None:
                record["cone_part"] = cone["part"]
                record["cone_owner"] = cone["owner"]
            maximum_fill = max(maximum_fill, len(fill))
            for value in fill.values():
                maximum_bits = max(maximum_bits, abs(value.numerator).bit_length(), value.denominator.bit_length())
        else:
            record["status"] = "NONBOUNDARY"
            record["dual_cochain"] = [[[list(parts), list(owners)], value.numerator, value.denominator] for (parts, owners), value in sorted(outcome["dual"].items())]
            record["pairing"] = [outcome["pairing"].numerator, outcome["pairing"].denominator]
            failures.append(record)
        records.append(record)
    serialized_faces = [{"triple": list(row["triple"]), "allowed_cells": row["allowed_cells"], "rank": row["rank"], "route": row["route"], "coefficients": [[list(owners), value.numerator, value.denominator] for owners, value in sorted(row["coefficients"].items())]} for row in face_rows]
    result = {"status": "PASS", "epistemic_status": "PROVED", "stage": "STRATIFIED_NONANCHOR_CANONICAL_COUPLING", "selected_interfaces": len(selected), "face_classes": len(face_classes), "pair_classes": len(pair_classes), "rank_three_face_classes": len(RANK3), "delta_fast_faces": sum(row["route"] == "DELTA_FAST_PATH" for row in face_rows), "eliminated_faces": sum(row["route"] == "EXACT_ELIMINATION" for row in face_rows), "face_coefficients": sum(len(row["coefficients"]) for row in face_rows), "canonical_fills": sum(record["status"] in ("FILLED", "FILLED_EXISTENCE") for record in records), "canonical_failures": len(failures), "cone_explained": cone_count, "h2_zero_existence_fills": h2_zero_existence_count, "elimination_only_fills": elimination_count, "first_failure": failures[0] if failures else None, "maximum_fill_nonzero": maximum_fill, "maximum_coefficient_bits": maximum_bits, "coherent_escalation_required": bool(failures), "face_tensors": serialized_faces, "interface_records": records, "claim_boundary": "Exact canonical coupling and explicit cone classification on the frozen 2,000-interface non-anchor holdout only. GF(2)-H2-zero rows prove rational fill existence without serializing a particular fill.", "wall_seconds": time.monotonic() - started}
    if len(selected) > 2000 or len(face_classes) > 8000 or time.monotonic() - started > 14400:
        raise RuntimeError("Cycle 44 cap")
    temporary = OUT / "coupling.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "coupling.json")
    print(json.dumps({key: result[key] for key in ("status", "selected_interfaces", "face_classes", "pair_classes", "rank_three_face_classes", "delta_fast_faces", "eliminated_faces", "canonical_fills", "canonical_failures", "cone_explained", "h2_zero_existence_fills", "elimination_only_fills", "first_failure", "maximum_fill_nonzero", "maximum_coefficient_bits", "wall_seconds")}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
