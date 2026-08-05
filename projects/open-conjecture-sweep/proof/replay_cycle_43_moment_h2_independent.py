#!/usr/bin/env python3
"""Independent direct-signature replay of every Cycle 43 face and fill."""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
import itertools
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_ownership_functional as c38

OUT = ROOT / "discovery/out/cycle43-moment-h2-coupling"


def main():
    started = time.monotonic()
    c38.prepare()
    types = sorted({row[0] for root in c38._TYPE_ROWS for rows in root.values() for row in rows})
    type_id = {value: index for index, value in enumerate(types)}
    masks = [sum(1 << owner for owner, signature in enumerate(value) if signature) for value in types]
    memberships = [[set() for _ in types] for _ in range(13)]
    for owner in reversed(range(13)):
        for signature, rows in c38._TYPE_ROWS[owner].items():
            for row in reversed(rows):
                memberships[owner][type_id[row[0]]].add(int(signature))
    deletion_cache = {}

    def deleted(type_tuple):
        type_tuple = tuple(sorted(type_tuple))
        if type_tuple in deletion_cache:
            return deletion_cache[type_tuple]
        value = 0
        permutations = tuple(set(itertools.permutations(type_tuple)))
        for owner in reversed(range(13)):
            for pattern in reversed(c38._COORDINATES[owner]["patterns"]):
                if int(pattern["rank"]) != len(type_tuple):
                    continue
                signatures = tuple(int(item) for item in pattern["signatures"])
                if any(all(signatures[index] in memberships[owner][ordering[index]] for index in range(len(ordering))) for ordering in permutations):
                    value |= 1 << owner
                    break
        deletion_cache[type_tuple] = value
        return value

    primary = json.loads((OUT / "canonical-coupling.json").read_text(encoding="utf-8"))
    prior = json.loads((ROOT / "discovery/out/cycle41-multiplied-ideal/zero-support-closure.json").read_text(encoding="utf-8"))
    marginals = [{int(owner): Fraction(int(numerator), int(denominator)) for owner, numerator, denominator in values} for values in prior["singleton_marginals_by_complete_type"]]
    singleton_types = [index for index, mask in enumerate(masks) if mask.bit_count() == 1]
    binary_types = [index for index, mask in enumerate(masks) if mask.bit_count() == 2]

    def effective_owner_allowed(type_index, owner):
        if not masks[type_index] & (1 << owner):
            return False
        for mediator in singleton_types:
            mediator_owner = masks[mediator].bit_length() - 1
            if mediator_owner == owner and deleted((mediator, type_index)) & (1 << owner):
                return False
        return True

    def relation_forbidden(left, right, i, j):
        if i == j and deleted((left, right)) & (1 << i):
            return True
        if i == j:
            for mediator in singleton_types:
                owner = masks[mediator].bit_length() - 1
                if owner == i and deleted((mediator, left, right)) & (1 << i):
                    return True
        for mediator in binary_types:
            owners = [owner for owner in range(13) if masks[mediator] & (1 << owner)]
            for x, y in (owners, owners[::-1]):
                if (i, j) == (x, y) and deleted((mediator, left)) & (1 << x) and deleted((mediator, right)) & (1 << y):
                    return True
        return False

    face_tensors = {}
    pair_flows = {}
    face_coefficients = 0
    for row in reversed(primary["face_tensors"]):
        triple = tuple(int(value) for value in row["triple"])
        if triple != tuple(sorted(triple)) or triple in face_tensors:
            raise AssertionError("face identity")
        coefficients = {tuple(int(owner) for owner in owners): Fraction(int(numerator), int(denominator)) for owners, numerator, denominator in row["coefficients"]}
        face_coefficients += len(coefficients)
        for owners in coefficients:
            for position, owner in enumerate(owners):
                if not masks[triple[position]] & (1 << owner):
                    raise AssertionError("rank-one face support")
            if any(owners[x] == owners[y] and deleted((triple[x], triple[y])) & (1 << owners[x]) for x, y in itertools.combinations(range(3), 2)):
                raise AssertionError("rank-two face support")
            if owners[0] == owners[1] == owners[2] and deleted(triple) & (1 << owners[0]):
                raise AssertionError("rank-three face support")
        stabilizer = [permutation for permutation in itertools.permutations(range(3)) if tuple(triple[permutation[index]] for index in range(3)) == triple]
        for owners, value in coefficients.items():
            for permutation in stabilizer:
                if coefficients.get(tuple(owners[permutation[index]] for index in range(3)), Fraction(0)) != value:
                    raise AssertionError("face stabilizer")
        for x, y in itertools.combinations(range(3), 2):
            observed = defaultdict(Fraction)
            for owners, value in coefficients.items():
                observed[(owners[x], owners[y])] += value
            observed = {key: value for key, value in observed.items() if value}
            pair = (triple[x], triple[y])
            if pair in pair_flows and pair_flows[pair] != observed:
                raise AssertionError("shared pair moment")
            pair_flows[pair] = observed
        face_tensors[triple] = coefficients
    if len(face_tensors) != primary["unordered_face_classes"] or face_coefficients != primary["canonical_face_nonzero"]:
        raise AssertionError("face census")
    if len(pair_flows) != primary["oriented_pair_classes"]:
        raise AssertionError("pair census")
    for (left, right), flow in pair_flows.items():
        for (i, j), value in flow.items():
            if not value or not effective_owner_allowed(left, i) or not effective_owner_allowed(right, j) or relation_forbidden(left, right, i, j):
                raise AssertionError("forced pair support")
        for i in range(13):
            if sum(value for (x, _y), value in flow.items() if x == i) != marginals[left].get(i, 0):
                raise AssertionError("left singleton marginal")
        for j in range(13):
            if sum(value for (_x, y), value in flow.items() if y == j) != marginals[right].get(j, 0):
                raise AssertionError("right singleton marginal")

    def structural_key(type_tuple):
        return (tuple(masks[value] for value in type_tuple), tuple(deleted((type_tuple[a], type_tuple[b])) for a, b in itertools.combinations(range(4), 2)))

    def build_complex(type_tuple):
        supports = [tuple(owner for owner in range(13) if masks[value] & (1 << owner)) for value in type_tuple]
        edges = []
        for a, b in itertools.combinations(range(4), 2):
            diagonal = deleted((type_tuple[a], type_tuple[b]))
            for i in supports[a]:
                for j in supports[b]:
                    if not (i == j and diagonal & (1 << i)):
                        edges.append(((a, i), (b, j)))
        edge_id = {edge: index for index, edge in enumerate(edges)}
        triangles = []
        d2 = []
        for parts in itertools.combinations(range(4), 3):
            for owners in itertools.product(*(supports[p] for p in parts)):
                vertices = tuple(zip(parts, owners))
                candidates = tuple((vertices[x], vertices[y]) for x, y in itertools.combinations(range(3), 2))
                if not all(edge in edge_id for edge in candidates):
                    continue
                triangles.append(vertices)
                d2.append({edge_id[candidates[2]]: Fraction(1), edge_id[candidates[1]]: Fraction(-1), edge_id[candidates[0]]: Fraction(1)})
        triangle_id = {face: index for index, face in enumerate(triangles)}
        tetrahedra = []
        d3 = []
        for owners in itertools.product(*supports):
            faces = [tuple((part, owners[part]) for part in range(4) if part != omitted) for omitted in range(4)]
            if all(face in triangle_id for face in faces):
                tetrahedra.append(owners)
                d3.append({triangle_id[face]: Fraction((-1) ** omitted) for omitted, face in enumerate(faces)})
        return triangles, d2, tetrahedra, d3

    records = primary["interface_records"]
    if len(records) != 3954 or [(row["anchor_index"], row["fourth_type"]) for row in records] != [(anchor, fourth) for anchor in range(3) for fourth in range(1318)]:
        raise AssertionError("raw interface order")
    complex_cache = {}
    structural_counts = Counter()
    total_cycle = total_fill = 0
    controls = []
    control_ordinals = {0, 1976, 3953}
    for ordinal, record in enumerate(records):
        type_tuple = tuple(int(value) for value in record["types"])
        key = structural_key(type_tuple)
        structural_counts[key] += 1
        if key not in complex_cache:
            complex_cache[key] = build_complex(type_tuple)
        triangles, d2, tetrahedra, d3 = complex_cache[key]
        triangle_id = {face: index for index, face in enumerate(triangles)}
        expected_cycle = defaultdict(Fraction)
        for omitted in range(4):
            parts = tuple(part for part in range(4) if part != omitted)
            ordered_types = tuple(type_tuple[part] for part in parts)
            sorted_types = tuple(sorted(ordered_types))
            tensor = face_tensors[sorted_types]
            permutation = next(permutation for permutation in itertools.permutations(range(3)) if tuple(sorted_types[permutation[index]] for index in range(3)) == ordered_types)
            sign = Fraction((-1) ** omitted)
            for owners, value in tensor.items():
                ordered_owners = tuple(owners[permutation[index]] for index in range(3))
                expected_cycle[triangle_id[tuple(zip(parts, ordered_owners))]] += sign * value
        expected_cycle = {index: value for index, value in expected_cycle.items() if value}
        recorded_cycle = {int(index): Fraction(int(numerator), int(denominator)) for index, numerator, denominator in record["cycle"]}
        if expected_cycle != recorded_cycle or record["status"] != "FILLED":
            raise AssertionError("recorded cycle")
        for edge in range(max((max(column, default=-1) for column in d2), default=-1) + 1):
            if sum(column.get(edge, 0) * recorded_cycle.get(index, 0) for index, column in enumerate(d2)):
                raise AssertionError("cycle boundary")
        fill = {int(index): Fraction(int(numerator), int(denominator)) for index, numerator, denominator in record["fill"]}
        replay = defaultdict(Fraction)
        for tetrahedron, coefficient in fill.items():
            for triangle, value in d3[tetrahedron].items():
                replay[triangle] += coefficient * value
        if {index: value for index, value in replay.items() if value} != recorded_cycle:
            raise AssertionError("tetrahedral fill")
        total_cycle += len(recorded_cycle)
        total_fill += len(fill)
        if ordinal in control_ordinals:
            controls.append({"ordinal": ordinal, "types": list(type_tuple), "cycle_nonzero": len(recorded_cycle), "fill_nonzero": len(fill)})
    if len(complex_cache) != primary["structural_complexes"] or len(complex_cache) != 409:
        raise AssertionError("structural census")
    if total_cycle != sum(len(row["cycle"]) for row in records) or total_fill != sum(len(row["fill"]) for row in records):
        raise AssertionError("coefficient census")
    payload = {"status": "PASS", "epistemic_status": "PROVED", "raw_interfaces": len(records), "structural_complexes": len(complex_cache), "face_classes": len(face_tensors), "pair_classes": len(pair_flows), "face_coefficients_checked": face_coefficients, "cycle_coefficients_checked": total_cycle, "fill_coefficients_checked": total_fill, "canonical_failures": 0, "controls": controls, "wall_seconds": time.monotonic() - started}
    temporary = OUT / "independent-replay.json.tmp"
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "independent-replay.json")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
