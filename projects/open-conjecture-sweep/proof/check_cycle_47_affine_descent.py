#!/usr/bin/env python3
"""Audit Cycle 47's connected selection and serialized global section."""
from __future__ import annotations

from collections import Counter, defaultdict, deque
from fractions import Fraction
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle47-affine-descent"


def parse_chain(rows):
    return {tuple(cell): Fraction(numerator, denominator) for cell, numerator, denominator in rows}


def parse_cycle(rows):
    return {(tuple(parts), tuple(owners)): Fraction(numerator, denominator) for (parts, owners), numerator, denominator in rows}


def faces(types):
    return {tuple(types[index] for index in range(4) if index != omitted) for omitted in range(4)}


def incidence(selected):
    face_rows = defaultdict(list)
    for ordinal, types in enumerate(selected):
        for face in faces(types):
            face_rows[face].append(ordinal)
    adjacency = defaultdict(set)
    for ordinals in face_rows.values():
        for left, right in itertools.combinations(ordinals, 2):
            adjacency[left].add(right)
            adjacency[right].add(left)
    seen = set()
    components = 0
    for start in range(len(selected)):
        if start in seen:
            continue
        components += 1
        seen.add(start)
        queue = deque([start])
        while queue:
            for nxt in adjacency[queue.popleft()]:
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
    edges = sum(len(faces(types)) for types in selected)
    return {
        "components": components, "quadruple_vertices": len(selected), "face_vertices": len(face_rows),
        "incidence_edges": edges, "cycle_rank": edges - len(selected) - len(face_rows) + components,
        "repeated_faces": sum(len(rows) > 1 for rows in face_rows.values()),
        "maximum_face_degree": max(map(len, face_rows.values())),
        "face_degree_counts": {str(key): value for key, value in sorted(Counter(map(len, face_rows.values())).items())},
    }


def boundary(fill):
    result = defaultdict(Fraction)
    for owners, coefficient in fill.items():
        for omitted in range(4):
            parts = tuple(part for part in range(4) if part != omitted)
            face_owners = tuple(owners[part] for part in parts)
            result[(parts, face_owners)] += Fraction((-1) ** omitted) * coefficient
    return {key: value for key, value in result.items() if value}


def audit():
    selection = json.loads((OUT / "selection.json").read_text())
    controls = json.loads((OUT / "generic-controls.json").read_text())
    actual = json.loads((OUT / "canonical-section-localized.json").read_text())
    independent = json.loads((OUT / "independent-replay.json").read_text())
    assert selection["status"] == controls["status"] == actual["status"] == independent["status"] == "PASS"
    selected = [tuple(row["types"]) for row in selection["selected"]]
    assert len(selected) == len(set(selected)) == 256
    old = set()
    for path in (
        ROOT / "discovery/out/cycle43-moment-h2-coupling/canonical-coupling.json",
        ROOT / "discovery/out/cycle44-nonanchor-coupling/coupling.json",
    ):
        data = json.loads(path.read_text())
        old.update(tuple(sorted(row["types"])) for row in data["interface_records"])
    assert not (set(selected) & old)
    checked_incidence = incidence(selected)
    assert checked_incidence == selection["incidence"] == actual["incidence"]
    assert checked_incidence["components"] == 1 and checked_incidence["cycle_rank"] > 0

    tensors = {}
    for row in actual["face_tensors"]:
        triple = tuple(row["triple"])
        assert triple not in tensors
        tensor = parse_chain(row["coefficients"])
        for permutation in itertools.permutations(range(3)):
            if tuple(triple[permutation[index]] for index in range(3)) == triple:
                assert {tuple(cell[permutation[index]] for index in range(3)): value for cell, value in tensor.items()} == tensor
        tensors[triple] = tensor

    routes = Counter()
    maximum_fill = maximum_bits = 0
    for ordinal, (types, row) in enumerate(zip(selected, actual["records"], strict=True)):
        assert row["ordinal"] == ordinal and tuple(row["types"]) == types and row["status"] == "FILLED"
        reconstructed = defaultdict(Fraction)
        for omitted in range(4):
            parts = tuple(part for part in range(4) if part != omitted)
            ordered_types = tuple(types[part] for part in parts)
            triple = tuple(sorted(ordered_types))
            permutation = next(p for p in itertools.permutations(range(3)) if tuple(triple[p[index]] for index in range(3)) == ordered_types)
            for owners, value in tensors[triple].items():
                ordered_owners = tuple(owners[permutation[index]] for index in range(3))
                reconstructed[(parts, ordered_owners)] += Fraction((-1) ** omitted) * value
        reconstructed = {key: value for key, value in reconstructed.items() if value}
        cycle = parse_cycle(row["cycle"])
        fill = parse_chain(row["fill"])
        assert reconstructed == cycle and boundary(fill) == cycle
        routes[row["route"]] += 1
        maximum_fill = max(maximum_fill, len(fill))
        for value in itertools.chain(cycle.values(), fill.values()):
            maximum_bits = max(maximum_bits, abs(value.numerator).bit_length(), value.denominator.bit_length())
    assert dict(sorted(routes.items())) == actual["fill_routes"]
    assert maximum_fill == actual["maximum_fill_nonzero"] and maximum_bits == actual["maximum_coefficient_bits"]
    assert independent["selected_records"] == 7
    assert set(independent["selected_route_counts"]) == set(actual["fill_routes"])
    full = independent["full_residual_audit"]
    assert full == {
        "quadruples": 256, "raw_occurrences": 1024, "face_classes": 185,
        "repeated_face_classes": 175, "gluing_identifications": 839,
        "all_stabilizers_and_orientations_checked": True,
        "all_local_fills_checked": True, "nonzero_residuals": 0,
    }
    assert len(independent["full_records"]) == 256
    for row in independent["records"]:
        source = actual["records"][row["ordinal"]]
        assert row["types"] == source["types"] and row["route"] == source["route"] and row["fill_nonzero"] == len(source["fill"])
    return {
        "status": "PASS", "selected_quadruples": len(selected), "face_classes": len(tensors),
        "incidence_cycle_rank": checked_incidence["cycle_rank"], "repeated_faces": checked_incidence["repeated_faces"],
        "fill_routes": dict(sorted(routes.items())), "maximum_fill_nonzero": maximum_fill,
        "maximum_coefficient_bits": maximum_bits, "independent_records": independent["selected_records"],
        "independent_faces_checked": independent["target_faces_checked"],
        "independent_full_rows": full["quadruples"], "independent_gluing_checks": full["gluing_identifications"],
    }


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True))
