#!/usr/bin/env python3
"""Independent high-pivot replay of Cycle 42's H2 census and first coupling."""
from __future__ import annotations

from collections import Counter, defaultdict
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

OUT = ROOT / "discovery/out/cycle42-h2-horn"
ANCHORS = ((2, 5, 14), (14, 68, 71), (80, 1306, 1307))


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
    cache = {}

    def deleted(type_tuple):
        ordered_types = tuple(sorted(type_tuple))
        if ordered_types in cache:
            return cache[ordered_types]
        value = 0
        for owner in range(12, -1, -1):
            found = False
            for pattern in reversed(c38._COORDINATES[owner]["patterns"]):
                if int(pattern["rank"]) != len(ordered_types):
                    continue
                signatures = tuple(int(item) for item in pattern["signatures"])
                if any(all(signatures[index] in memberships[owner][ordering[index]] for index in range(len(ordering))) for ordering in set(itertools.permutations(ordered_types))):
                    found = True
                    break
            if found:
                value |= 1 << owner
        cache[ordered_types] = value
        return value

    def key(type_tuple):
        return (
            tuple(masks[value] for value in type_tuple),
            tuple(deleted((type_tuple[a], type_tuple[b])) for a, b in itertools.combinations(range(4), 2)),
            tuple(deleted(tuple(type_tuple[p] for p in parts)) for parts in itertools.combinations(range(4), 3)),
        )

    def rank_gf2(vectors):
        basis = {}
        for value in vectors:
            while value:
                pivot = value.bit_length() - 1
                if pivot not in basis:
                    basis[pivot] = value
                    break
                value ^= basis[pivot]
        return len(basis)

    def rank_q(vectors):
        basis = {}
        bits = 1
        for raw in reversed(vectors):
            row = dict(raw)
            while row:
                pivot = max(row)
                if pivot not in basis:
                    scale = row[pivot]
                    row = {index: value / scale for index, value in row.items()}
                    basis[pivot] = row
                    for value in row.values():
                        bits = max(bits, abs(value.numerator).bit_length(), value.denominator.bit_length())
                    break
                factor = row[pivot]
                for index, value in basis[pivot].items():
                    row[index] = row.get(index, Fraction(0)) - factor * value
                    if not row[index]:
                        del row[index]
        return len(basis), bits

    def complex_data(type_tuple, full=False):
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
            diagonal = deleted(tuple(type_tuple[p] for p in parts))
            for owners in itertools.product(*(supports[p] for p in parts)):
                if owners[0] == owners[1] == owners[2] and diagonal & (1 << owners[0]):
                    continue
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
        for column in d3:
            composed = defaultdict(Fraction)
            for triangle, coefficient in column.items():
                for edge, value in d2[triangle].items():
                    composed[edge] += coefficient * value
            if any(composed.values()):
                raise AssertionError("boundary squared")
        gf2_d2 = rank_gf2([sum(1 << index for index in column) for column in d2])
        gf2_d3 = rank_gf2([sum(1 << index for index in column) for column in d3])
        q_d2, bits2 = rank_q(d2)
        q_d3, bits3 = rank_q(d3)
        row = {"vertices": sum(map(len, supports)), "edges": len(edges), "triangles": len(triangles), "tetrahedra": len(tetrahedra), "rank_d2_gf2": gf2_d2, "rank_d3_gf2": gf2_d3, "h2_gf2": len(triangles) - gf2_d2 - gf2_d3, "rank_d2_q": q_d2, "rank_d3_q": q_d3, "h2_q": len(triangles) - q_d2 - q_d3, "maximum_rational_coefficient_bits": max(bits2, bits3)}
        if full:
            row.update({"supports": supports, "edges_list": edges, "triangles_list": triangles, "d2": d2, "tetrahedra_list": tetrahedra, "d3": d3})
        return row

    primary = json.loads((OUT / "gf2-census.json").read_text(encoding="utf-8"))
    frozen_controls = json.loads((ROOT / "discovery/out/cycle41-multiplied-ideal/independent-replay.json").read_text(encoding="utf-8"))["exact_reversed_pivot_controls"]
    if tuple(tuple(row["types"]) for row in frozen_controls) != ANCHORS:
        raise AssertionError("frozen anchors")
    multiplicities = Counter()
    representatives = {}
    for anchor_index, anchor in enumerate(ANCHORS):
        for fourth in range(len(types)):
            interface = anchor + (fourth,)
            structural = key(interface)
            multiplicities[structural] += 1
            representatives.setdefault(structural, (anchor_index, fourth))
    if len(representatives) != 409:
        raise AssertionError("distinct structural interfaces")
    primary_rows = {(int(row["anchor_index"]), int(row["fourth_type"])): row for row in primary["rows"]}
    totals = Counter()
    nonzero2 = nonzeroq = disagreements = 0
    maximum_h2 = maximum_bits = 0
    for structural, representative in reversed(list(representatives.items())):
        anchor_index, fourth = representative
        row = complex_data(ANCHORS[anchor_index] + (fourth,))
        expected = primary_rows[representative]
        for name in ("vertices", "edges", "triangles", "tetrahedra", "rank_d2_gf2", "rank_d3_gf2", "h2_gf2", "rank_d2_q", "rank_d3_q", "h2_q", "maximum_rational_coefficient_bits"):
            if row[name] != expected[name]:
                raise AssertionError(f"row mismatch {representative} {name}")
        count = multiplicities[structural]
        if count != expected["multiplicity"]:
            raise AssertionError("multiplicity")
        for name in ("vertices", "edges", "triangles", "tetrahedra"):
            totals[name] += count * row[name]
        nonzero2 += count * bool(row["h2_gf2"])
        nonzeroq += count * bool(row["h2_q"])
        disagreements += count * (row["h2_gf2"] != row["h2_q"])
        maximum_h2 = max(maximum_h2, row["h2_q"])
        maximum_bits = max(maximum_bits, row["maximum_rational_coefficient_bits"])
    if dict(totals) != primary["aggregate_cells"] or (nonzero2, nonzeroq, disagreements, maximum_h2, maximum_bits) != (3893, 3893, 0, 40, 1):
        raise AssertionError("aggregate census")
    if any(deleted(tuple((anchor + (fourth,))[p] for p in parts)) for anchor in ANCHORS for fourth in range(len(types)) for parts in itertools.combinations(range(4), 3)):
        raise AssertionError("unexpected rank-three deletion")

    # Certificate and semantic replay on the first rational interface.
    first = json.loads((OUT / "first-rational-coupling.json").read_text(encoding="utf-8"))
    data = complex_data(tuple(first["types"]), full=True)
    if {name: data[name] for name in ("vertices", "edges", "triangles", "tetrahedra", "rank_d2_q", "rank_d3_q", "h2_q")} != first["complex"]:
        raise AssertionError("first complex")
    cycle = [Fraction(0)] * data["triangles"]
    for index, value in first["canonical_class"]["primitive_cycle"]:
        cycle[int(index)] = Fraction(int(value))
    for edge in range(data["edges"]):
        if sum(column.get(edge, 0) * cycle[index] for index, column in enumerate(data["d2"])):
            raise AssertionError("canonical cycle boundary")
    cochain = {int(index): Fraction(int(numerator), int(denominator)) for index, numerator, denominator in first["canonical_class"]["dual_cochain"]}
    if any(sum(cochain.get(index, 0) * value for index, value in column.items()) for column in data["d3"]):
        raise AssertionError("cochain on boundary")
    pairing = sum(cochain.get(index, 0) * value for index, value in enumerate(cycle))
    if [pairing.numerator, pairing.denominator] != first["canonical_class"]["pairing"] or not pairing:
        raise AssertionError("canonical pairing")

    prior = json.loads((ROOT / "discovery/out/cycle41-multiplied-ideal/zero-support-closure.json").read_text(encoding="utf-8"))
    marginals = [{int(owner): Fraction(int(numerator), int(denominator)) for owner, numerator, denominator in values} for values in prior["singleton_marginals_by_complete_type"]]
    supports = data["supports"]
    singleton_types = [index for index, mask in enumerate(masks) if mask.bit_count() == 1]
    binary_types = [index for index, mask in enumerate(masks) if mask.bit_count() == 2]

    def effective_owner_allowed(type_index, owner):
        if not masks[type_index] & (1 << owner):
            return False
        return not any((masks[mediator].bit_length() - 1 == owner) and (deleted((mediator, type_index)) & (1 << owner)) for mediator in singleton_types)

    def relation_cell_forbidden(left, right, i, j):
        if i == j and deleted((left, right)) & (1 << i):
            return True
        if i == j and any((masks[mediator].bit_length() - 1 == i) and (deleted((mediator, left, right)) & (1 << i)) for mediator in singleton_types):
            return True
        for mediator in binary_types:
            owners = [owner for owner in range(13) if masks[mediator] & (1 << owner)]
            for x, y in (owners, owners[::-1]):
                if (i, j) == (x, y) and deleted((mediator, left)) & (1 << x) and deleted((mediator, right)) & (1 << y):
                    return True
        return False

    pair_flows = {tuple(map(int, name.split(","))): {(int(i), int(j)): Fraction(int(numerator), int(denominator)) for i, j, numerator, denominator in values} for name, values in first["pair_flows"].items()}
    for (a, b), flow in pair_flows.items():
        diagonal = deleted((first["types"][a], first["types"][b]))
        for i, j in flow:
            if i not in supports[a] or j not in supports[b] or (i == j and diagonal & (1 << i)) or not effective_owner_allowed(first["types"][a], i) or not effective_owner_allowed(first["types"][b], j) or relation_cell_forbidden(first["types"][a], first["types"][b], i, j):
                raise AssertionError("pair support")
        for i in supports[a]:
            if sum(value for (x, _y), value in flow.items() if x == i) != marginals[first["types"][a]].get(i, 0):
                raise AssertionError("left marginal")
        for j in supports[b]:
            if sum(value for (_x, y), value in flow.items() if y == j) != marginals[first["types"][b]].get(j, 0):
                raise AssertionError("right marginal")
    rebuilt_moment = [Fraction(0)] * data["triangles"]
    for face in first["face_fills"]:
        omitted = int(face["omitted_part"])
        coefficients = {int(index): Fraction(int(numerator), int(denominator)) for index, numerator, denominator in face["fill"]}
        parts = tuple(part for part in range(4) if part != omitted)
        for a, b in itertools.combinations(parts, 2):
            observed = defaultdict(Fraction)
            for triangle_index, coefficient in coefficients.items():
                vertices = dict(data["triangles_list"][triangle_index])
                observed[(vertices[a], vertices[b])] += coefficient
            if {key: value for key, value in observed.items() if value} != pair_flows[(a, b)]:
                raise AssertionError("face pair marginal")
        for index, value in coefficients.items():
            rebuilt_moment[index] += Fraction((-1) ** omitted) * value
    recorded_moment = [Fraction(0)] * data["triangles"]
    for index, numerator, denominator in first["moment_cycle"]:
        recorded_moment[int(index)] = Fraction(int(numerator), int(denominator))
    if rebuilt_moment != recorded_moment:
        raise AssertionError("moment assembly")
    fill = {int(index): Fraction(int(numerator), int(denominator)) for index, numerator, denominator in first["moment_fill"]}
    boundary = [Fraction(0)] * data["triangles"]
    for tetrahedron, coefficient in fill.items():
        for triangle, value in data["d3"][tetrahedron].items():
            boundary[triangle] += coefficient * value
    if boundary != recorded_moment:
        raise AssertionError("moment fill")

    payload = {"status": "PASS", "epistemic_status": "PROVED", "raw_interfaces": 3954, "distinct_interfaces": 409, "nonzero_h2_gf2": nonzero2, "nonzero_h2_q": nonzeroq, "maximum_h2_q": maximum_h2, "field_dimension_disagreements": disagreements, "maximum_rational_coefficient_bits": maximum_bits, "first_interface": {"types": first["types"], "h2_q": data["h2_q"], "canonical_pairing": [pairing.numerator, pairing.denominator], "moment_filling_status": "CONSISTENT", "moment_fill_nonzero": len(fill)}, "wall_seconds": time.monotonic() - started}
    temporary = OUT / "independent-replay.json.tmp"
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "independent-replay.json")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
